{
  "title": "VMware Cloud Foundation 9.1 Upgrade - Series Overview and Planning",
  "date": "2026-09-30T12:45:00-04:00",
  "lastmod": "2026-09-30T12:45:00-04:00",
  "slug": "vcf-9-1-upgrade-series-overview",
  "url": "/posts/vcf-9-1-upgrade-series-overview/",
  "draft": false,
  "description": "The overview and planning post for my VMware Cloud Foundation 9.0.2 to 9.1 upgrade series: the roadmap, my lab environment, what's new in 9.1, the cert/password freeze window, and the prerequisites that gate the whole upgrade.",
  "featured_image": "series-overview.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "VCF",
    "VMware",
    "vSphere",
    "NSX",
    "vSAN",
    "SDDC Manager",
    "VCF Operations",
    "Upgrade",
    "homelab"
  ],
  "years": [
    "2026"
  ],
  "aliases": [],
  "comments": []
}

VMware Cloud Foundation 9.1 dropped on May 12th, and since most of my focus these days lives squarely in the VCF world, I figured there's no better way to put it through its paces than to upgrade my own lab from 9.0.2 and document the whole thing along the way.

VCF 9.1 isn't a single button press.  It's a sequenced upgrade across a whole stack of components, and 9.1 reshapes the management layer.  So rather than cram it all into one monster post, I'm running it as a series, split the way the upgrade actually flows.  This post is the home base: the roadmap, my lab, the big changes to expect, the freeze window warning, and the prerequisites that gate everything.

## The series

Here's how I'm breaking this down, following the order I'm actually running it in my lab:

- **[Part 1](/posts/vcf-9-1-upgrade-part-1-vcf-operations/):** Upgrading VCF Operations to 9.1
- **[Part 2](/posts/vcf-9-1-upgrade-part-2-sddc-manager-management-services/):** Upgrading SDDC Manager, then deploying VCF Management Services and the License Server
- **[Part 3](/posts/vcf-9-1-upgrade-part-3-automation-logs/):** Upgrading VCF Automation and VCF Operations for Logs
- **[Part 4](/posts/vcf-9-1-upgrade-part-4-nsx-vcenter/):** Upgrading NSX and vCenter
- **[Part 5](/posts/vcf-9-1-upgrade-part-5-esxi-nsx-edge/):** Upgrading the ESX hosts and completing the NSX upgrade
- **[Part 6](/posts/vcf-9-1-upgrade-part-6-housekeeping-workload-domain/):** Post-upgrade housekeeping (the distributed switch, the vSAN on-disk format, and the configuration upgrade) and the workload domain

<aside class="info-block"><p>The screenshots throughout this series come from my own lab and reflect my environment's names and values.</p></aside>

## Where I'm starting from

My lab is running **VCF 9.0.2.0**, and since 9.1.1 landed on September 3rd, I'm skipping 9.1.0 entirely and going straight to **VCF 9.1.1.0100**.  The good news up front: that direct jump is supported, no intermediate hop required.

The rule that makes it work is simple.  VCF only lets you upgrade to a target that was released *after* your current version, and you can go straight to a patch release as long as you could also go to its parent maintenance release.  9.1.1 shipped on September 3rd, well after 9.0.2, so it's a clean path.  You can upgrade directly to 9.1.1 without going to 9.1.0 first and patching, and 9.1.1 also fixes a few things that sit on this path, including VCF Automation install and upgrade failures when an FQDN is entered in mixed case and a VCF Automation upgrade that could hang at its backup stage for up to two hours ([VCF Automation 9.1.1 release notes](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/release-notes/vmware-cloud-foundation-9-1-1-0-release-notes/vcfautomation-9-1-1-0-release-notes.html)).  Skipping 9.1.0 also spares an extra step: with only the day one components deployed, a management services runtime deployed on 9.1.0 and then upgraded to 9.1.1 keeps its larger 9.1.0 sizing until a Broadcom script is run, and I cover that in [Part 2](/posts/vcf-9-1-upgrade-part-2-sddc-manager-management-services/).

<aside class="info-block"><p>One more thing worth being explicit about, because it's the part of that rule that matters here.  My 9.0.2.0 environment is running mostly straight GA builds, with vCenter, ESX, and VCF Operations all on the GA builds.  The exceptions are Fleet Management and VCF Automation, which both carry the 9.0.2.0100 Express Patch, and the forward-only rule hasn't blocked me on either.  The rule is enforced per component against each component's release date, so an environment with 9.0.2 Express Patches applied needs them checked first.  vCenter and ESX 9.0.2.0100, for example, shipped on July 29th, after 9.1.0 but before 9.1.1, so an environment carrying them can't go to 9.1.0 but can go to 9.1.1.</p></aside>

The `.0100` part needs a quick explanation, because it doesn't touch everything.  vCenter, ESX, NSX, SDDC Manager, and VCF Operations all land on 9.1.1.0, released September 3rd, so that's the date that matters for them, not the .0100 date.  Fleet Lifecycle, SDDC Lifecycle, and a VCF Automation component called the migration service engine carry a 9.1.1.0100 patch on top, released September 21st, and the VCF Automation upgrade in my lab targets 9.1.1.0100 as well.  Here's what I'm targeting:

| Component | Target |
| --- | --- |
| VCF Operations | `9.1.1.0.25679751` |
| SDDC Manager | `9.1.1.0.25713928` |
| vCenter | `9.1.1.0.25712839` |
| ESX | `9.1.1.0.25714478` |
| NSX | `9.1.1.0.25691509` |
| Fleet Lifecycle, SDDC Lifecycle | 9.1.1.0100 |
| VCF Automation, migration service engine | 9.1.1.0100 |
| VMware Tools | 13.1.5 |

Here's the shape of the environment so the rest of the series makes sense:

| Domain | Type | vCenter | NSX |
| --- | --- | --- | --- |
| `vcf-m01` | Management | `vcf-m01-vc01.demo.lab` | `vcf-m01-nsx01.demo.lab` |
| `vcf-w01` | Workload (VI) | `vcf-w01-vc01.demo.lab` | `vcf-w01-nsx01.demo.lab` |

Each domain has its own NSX instance, nothing shared between them.  The workload domain also runs a two-node NSX Edge cluster, `vcf-w01-ec01`, while the management domain has no Edges at all, which is why the Edge upgrade shows up in Part 6 rather than Part 5.

Both clusters are vLCM **Image-based** (not baseline-based), which is a hard prerequisite for 9.1, and neither is stretched.  I'll be upgrading the management domain (`vcf-m01`) end to end first, then circling back to the workload domain as a Day-N exercise later in the series.

Credit where it's due: my lab is fully nested, and I deployed it with my own customized version of William Lam's [VCF Fleet Automated Lab Deployment](https://github.com/lamw/vcf-fleet-automated-lab-deployment) script, a project I've also contributed to.  The whole thing runs on a single 14th Gen Dell PowerEdge R740 with 768 GB of RAM and two 24-core Intel Xeon Platinum 8168 CPUs at 2.70 GHz, connected to my vSphere 8.0 U3 lab.  A handful of VMs make up the core of my nested lab infrastructure, and they're persistent, untouched by any future rebuild or redeployment: a pfSense router, a NAS running Synology DSM (via Xpenology), my domain controller, a Docker host running Traefik, Pi-hole with Unbound, phpIPAM, and Dockhand, and the depot VM I'll get to in the prerequisites.  William's script is a great place to start for a nested lab of your own, and [Holodeck](https://vmware.github.io/Holodeck/latest/) is the VMware by Broadcom option.  Either way, a nested lab is for learning and testing, not production, and a few of my choices later in the series, like running the management cluster at FTT = 0, come straight from that.

## What's new in 9.1 (and why this upgrade is more interesting than most)

A few changes make this more than a routine bundle-and-go.

**The Fleet Management appliance goes away.**  In 9.0.x, VCF Operations was fronted by a separate Fleet Management appliance (`vcf-m01-vopsfm01.demo.lab` in my lab).  In 9.1, its work is taken over by Fleet Lifecycle and SDDC Lifecycle, which are part of VCF Management Services.  During the VCF Operations upgrade in Part 1, VCF Operations collects the appliance's inventory, certificates, and service accounts, and the appliance is decommissioned and powers off ([upgrade docs](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/upgrade-backup-and-restore.html)).  The powered-off VM stays in vCenter until it's deleted.

**Lifecycle management moves into VCF Management Services.**  That work lands in a new runtime that Part 2 deploys.  It stands up Fleet Lifecycle and SDDC Lifecycle, a Software Depot, Salt master and Salt RaaS, Telemetry, and, depending on your identity setup, an Identity Broker, and a new dedicated License Server is deployed alongside it.  The licenses move onto the new License Server.

**The VCF Operations navigation gets reorganized.**  9.1 reorganizes the top nav into Build, Manage, Operate, and Protect.  The Lifecycle pages I live in for most of this series now sit under **Build → Lifecycle** instead of the Fleet Management menu from 9.0.  Same pages, new address.  Fleet Management itself hasn't gone anywhere, though.  It lives on under **Manage → Fleet Management**, which is where certificates, passwords, and the rest of the fleet-level settings now are.  The upgrade in Part 1 runs from the VCF Operations admin interface, so the **Build → Lifecycle** path first matters in Part 2.

## A note on planning: the docs and the official planner

VMware publishes a useful [VCF Upgrade Planner](https://vmware.github.io/vcf-upgrade-planner/) (the source is [up on GitHub](https://github.com/vmware/vcf-upgrade-planner)) that walks through a specific scenario and generates a tailored, phased plan plus a PDF for reference.  I ran it for my own environment, and it's great for visualizing the overall flow and for surfacing the networking and resource requirements up front.  I also put together a readiness checklist to go with it in [Before You Upgrade to VCF 9.1.x: Five Readiness Gates](/posts/vcf-9-1-upgrade-readiness-five-gates/), covering the upgrade path, network planning, sequencing, recovery, and automation tooling.

For my run I generated a 9.0.2 to 9.1.1.0100 plan with VCF Automation included.  It lays out eight phases, VCF Operations, SDDC Manager, the VCF Management Services deployment, VCF Automation, NSX Managers, vCenter, ESX, and the NSX finalize, then closes with a table of the effective patch version each component should land on.  It also flags a pre-update check warning specific to 9.1.1 for vCenter, which I cover in Part 4.

<aside class="info-block"><p>One thing I noticed: <strong>VCF Operations for Logs</strong> only appears in the plan if it's ticked as an optional component, and when I did that on an earlier run, the planner put it last.  The official <a href="https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation.html">Upgrading Cloud Foundation</a> documentation slots log management in with the rest of the management components instead, ahead of NSX and vCenter.  Where the two disagree, this series follows the <strong>official documentation</strong>, since that's the authoritative, maintained procedure, so Logs lives in Part 3.</p></aside>

## The cert and password freeze window

This one shaped how I planned the whole run.  Paraphrasing the official documentation:

<aside class="info-block"><p>After you upgrade VCF Operations to 9.1, you cannot manage certificates and passwords for VCF Automation, VCF Identity Broker, VCF Operations for Logs, and VCF Operations for Networks until you upgrade those components to 9.1, because they are now managed by VCF Operations fleet management.</p></aside>

In plain terms: the moment the VCF Operations upgrade in Part 1 finishes, I lose the ability to rotate certs or reset passwords on those downstream components from VCF Operations until *they* are also at 9.1.  So any cert rotations or password resets due on VCF Automation, the Identity Broker, Logs, or Networks have to happen **before** Part 1, or wait until **after** that specific component reaches 9.1 later in the series.

Automation and Logs come back in Part 3.  The Identity Broker depends on how yours is deployed: an appliance-mode broker gets upgraded on its own ahead of Automation, while an embedded one rides along with the vCenter upgrade in Part 4.

## Prerequisites

These gate the entire upgrade, and they all come before Part 1:

- **Broadcom Support Portal entitlement** to 9.1.1, with download access to the VCF Operations 9.1.1 PAK, the install binaries for VCF Management Services, the License Server, and log management, the VCF Automation upgrade binaries, and the NSX, vCenter, and ESX bundles.  I pulled the 9.1.1.0100 builds wherever they exist, because the guidance is to use the latest available binaries for anything deployed, upgraded, or patched.  The 9.1.1 VCF Download Tool has a `--latest` argument that pulls the latest build of every component, Express Patches included.  For an older version of the tool, William Lam has a [script](https://williamlam.com/2026/07/quick-tip-automatically-generate-vcf-download-tool-commands-with-express-patches-for-vcf-9-0-2-and-9-1-0.html) that generates the right commands for you.
- **A working software depot.**  The upgrade pulls every 9.1 bundle (vCenter, NSX, ESX, and the rest) from your configured depot, so the depot sync has to be green *before* the upgrade starts, or the later stages have nothing to install.  An **online depot** needs a valid download token, which becomes an activation code once you're on 9.1 ([KB 443647](https://knowledge.broadcom.com/external/article/443647/download-token-has-been-replaced-by-acti.html)).  My lab uses an **offline depot**: a small Ubuntu VM that's one of the few permanent pieces of my nested lab, running nginx in front of a share on my NAS.  The same VM runs the [VCF Download Tool](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/binary-management-for-vmware-cloud-foundation/download-bundles-to-an-offline-depot.html), so pulling new binaries and serving them happen in one place.  Broadcom covers building an offline depot in [KB 312168](https://knowledge.broadcom.com/external/article/312168/vcf-offline-depot-deployment.html) and filling it for 9.1 in [Download Bundles to an Offline Depot](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/binary-management-for-vmware-cloud-foundation/download-bundles-to-an-offline-depot.html), and William Lam's [VCF Download Tool cheatsheet](https://williamlam.com/2026/05/vcf-9-1-vcf-download-tool-vcfdt-cheatsheet.html) covers the commands.
- **A Cloud Proxy in your first VCF Instance, in a unified state.**  This is a hard gate, not a nice-to-have: without a cloud proxy in the instance where VCF Operations lives, you *cannot* complete the upgrade to 9.1, because Management Services depends on it for the integration between VCF Operations, SDDC Manager, and the new runtime.  Without one, upgrade VCF Operations first and deploy a new cloud proxy before Part 2.  Pre-validation also checks that every proxy collector is in a unified state, and a legacy one fails that check outright rather than warning ([KB 443797](https://knowledge.broadcom.com/external/article/443797/unable-to-upgrade-vcf-operations-from-90.html)).  Existing proxies upgrade themselves during Part 1.
- **Certificates with complete Subject Alternative Names.**  9.1 tightens certificate validation and **incomplete SANs are no longer supported**.  The SANs on the VCF Operations, VCF Automation, and VCF Operations for Networks certificates have to be complete before the upgrade starts.  The Automation certificate in particular needs every node FQDN and IP plus the load balancer VIP in its SAN field ([upgrade docs](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/phase-3-import-and-upgrade-aria-automation-8-to-vcf-automation-9.html)), and there's a documented case where an incomplete SAN on a legacy VCF Operations for Networks fails the Management Services deployment in Part 2 ([KB 440459](https://knowledge.broadcom.com/external/article/440459/upgrading-vcf-90-environment-to-91-fai.html)).
- **VCF Automation deployed in the management domain**, not in a workload domain.  That's a hard precondition for the overall upgrade.
- **Recent, verified backups** of SDDC Manager, VCF Operations, both NSX Managers, and both vCenters.  Broadcom's upgrade prerequisites call for file-based or image-based backups and a cold snapshot of SDDC Manager ([upgrade prerequisites](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/upgrade-the-management-domain-to-vmware-cloud-foundation-5-2/upgrade-prequisites.html)).
- **vLCM Image mode** confirmed on every cluster.  Baselines are no longer supported in 9.x ([How to Upgrade to VMware Cloud Foundation 9.1](https://blogs.vmware.com/cloud-foundation/2026/06/18/how-to-upgrade-to-vmware-cloud-foundation-9-1/)).
- **Management cluster capacity** with real headroom.  Part 2 deploys the new VCF Management Services runtime, and Part 3 provisions a second VCF Automation instance while the existing one stays active, so there has to be room for both to coexist.
- **New IPs and DNS records, reserved up front.**  9.1 brings a lot of new pieces with it, and every one of them wants an address.  For a Simple deployment that's **seven new lowercase FQDNs**, each on its own free IP with both A and PTR records: five for VCF Management Services in Part 2 (the services runtime, fleet component, instance component, Identity Broker, and License Server, though the Identity Broker one drops out when an appliance-mode broker already exists), plus one for the dedicated runtime behind VCF Automation and one for log management in Part 3.  On top of those come **two address pools**, which I reserved in IPAM without DNS records: at least 12 addresses for the Management Services runtime (30 is recommended, and it's what I gave it) and 5 for the new Automation nodes.  The Management Services addresses go on the network you pick at deployment (9.1.1 lets you choose), and the Automation addresses go on the network your current Automation nodes use.  None of the FQDNs can point into either pool.
- **An internal network that doesn't collide.**  The VCF services runtime uses `198.18.0.0/15` internally.  If that overlaps the management, VM, or IP pool networks, routing conflicts result, and the alternatives are `240.0.0.0/15` or `250.0.0.0/15`.
- **A DNS domain the validator accepts.**  Management services FQDN validation follows RFC 1034 and RFC 1123, and `.local` is rejected because it isn't an internet top-level domain.
- **Cert and password work done** per the freeze-window callout above.

I'll walk through the exact allocation from my lab, and the rules that come with it, in Parts 2 and 3 where each piece actually gets used.

## Ready?

With the lay of the land covered, **[Part 1](/posts/vcf-9-1-upgrade-part-1-vcf-operations/)** is where the operations layer gets onto 9.1.

Thanks as always for stopping by, and I hope this series saves you some time and a few headaches on your own 9.1 upgrade.

-virtualex-
