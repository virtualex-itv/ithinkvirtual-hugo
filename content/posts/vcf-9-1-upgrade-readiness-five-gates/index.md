{
  "title": "Before You Upgrade to VCF 9.1.x: Five Readiness Gates",
  "date": "2026-09-29T12:00:00-04:00",
  "lastmod": "2026-10-01T13:19:32-04:00",
  "slug": "vcf-9-1-upgrade-readiness-five-gates",
  "url": "/posts/vcf-9-1-upgrade-readiness-five-gates/",
  "draft": false,
  "description": "A VCF 9.1.x readiness checklist: prove the upgrade path, plan the management services network, own the sequence, verify recovery, and test your automation before the maintenance window.",
  "featured_image": "readiness-gates.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "VCF",
    "VMware",
    "vSphere",
    "Upgrade",
    "Lifecycle Management",
    "PowerCLI"
  ],
  "years": [
    "2026"
  ],
  "aliases": [],
  "comments": []
}

VCF 9.1.1 has been out since September 3rd, and the 9.1.1.0100 patches for fleet lifecycle and SDDC lifecycle landed on the 21st, so the upgrade guidance has finally settled enough to plan against.  Downloading the binaries is the easy part.  The hard part is being able to say exactly what will change, why the path is supported, and how you'll know the environment is healthy afterward.

This is the checklist I'd want in front of anyone booking a maintenance window for a 9.0.x to 9.1.x upgrade: five gates, each with a pass condition you can actually check.  I'm about to publish a series that runs the upgrade end to end in a nested lab, which makes it a great rehearsal but not production evidence.  This checklist is the production-side companion, built from the current Broadcom documentation.

The reason this deserves a checklist is that 9.1 changes more than version numbers.  Lifecycle management for VCF Operations, Operations for Logs, Operations for Networks, VCF Automation, and the Identity Broker moves to the new fleet lifecycle and SDDC lifecycle components, and during the VCF Operations upgrade the process migrates your component inventory, certificates, and service accounts and then decommissions the fleet management appliance for you ([Upgrading to VMware Cloud Foundation 9.1.x](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation.html)).  That's a new management plane, not a patch.

## Gate 1: Prove the upgrade path

"9 is newer than 5" is not an upgrade plan.  VCF enforces forward-only upgrade validation by release date, and it applies that rule to every component in your source bill of materials, not just the VCF version on the label.  The documentation's own example makes the point: VCF 5.2.4, released May 27th, cannot upgrade to VCF 9.1.0, released May 11th, but it can upgrade to VCF 9.1.1, released September 3rd.  The same goes for the vCenter and ESX builds inside that 5.2.4 BoM.  One more consequence worth knowing is that following the current guidance takes you straight to 9.1.1 without installing 9.1.0 first and patching afterward.

So the first deliverable is a short inventory: every component with its exact version and build, the target version and build, the upgrade-path and interoperability references you checked for that combination (the [Broadcom Interoperability Matrix](https://interopmatrix.broadcom.com/Upgrade?productId=851) is the one the docs point to), and the date you checked them.  The [VCF Upgrade Planning Tool](https://blogs.vmware.com/cloud-foundation/2026/05/28/announcing-the-vmware-cloud-foundation-9-1-upgrade-planning-tool) is a great place to start, since it takes your deployed products and versions and generates a phased plan with resource and networking requirements, pitfalls, and documentation links, and you can export the whole thing or individual phases to PDF.  Use it to structure the work, then validate it against the documentation for the exact target you intend to deploy.

One more check if your source isn't already on 9.x.  Coming from VCF 5.x, or from a vSphere environment you plan to converge, two things in your current setup can stop you cold.  First, vSphere Lifecycle Manager baselines aren't supported in VCF 9.0 or later, so every cluster has to be managed with vLCM images before you upgrade to ESX 9, and the docs have you start that transition as soon as SDDC Manager reaches 9 ([baseline to image transition](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/upgrade-the-management-domain-to-vmware-cloud-foundation-5-2/vlcm-baseline-to-vlcm-image-cluster-transition-.html)).  Second, Enhanced Linked Mode is deprecated in VCF 9.0.  It doesn't block an upgrade from 5.x by itself, but you have to deactivate it for all of your vCenter instances through the SDDC Manager API before you can use VCF Single Sign-On or vCenter linking ([deactivating ELM](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/fleet-management/what-is/points-to-consider-while-setting-up-vmware-cloud-foundation-sso/deactivate-enhanced-link-mode--elm--for-upgraded-vmware-cloud-foundation-vcenters.html)), and pulling vCenters out of ELM outside of SDDC Manager leaves drift that blocks some workflows until you reconcile it.  If you're converging a vSphere environment instead, ELM isn't supported at all, so you'd upgrade the vCenters to 9.1 and break ELM first, and that workaround only applies when there are no existing NSX registrations ([supported and unsupported configurations](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/converging-your-existing-vsphere-infrastructure-to-a-vcf-or-vvf-platform-/supported-and-not-supported-configurations.html)).

**Pass condition:** you can explain why the path is supported for this specific environment without pointing at a generic version chart, and if you're coming from 5.x or converging vSphere, every cluster is on vLCM images and ELM has been dealt with.

## Gate 2: Treat the management network as a deployment dependency

An available subnet is not an address plan.  The VCF management services deployment needs a minimum of 12 IP addresses for the services runtime pool (a /28) and recommends 30 (a /27) so you have room for new components and scale-out.  Separately, you need up to five FQDNs, one each for the services runtime, the fleet component, the instance component, the Identity Broker, and the License Server (the Identity Broker one only applies if you don't already have an appliance-mode broker), and every one of them has to resolve to a unique, unused IP that sits outside the pool but on the same network as the runtime.  The runtime pool minimum is not your total IP budget.

The FQDN rules are strict too.  No capital letters, and no `.local`, which the docs say the validator rejects because it isn't an internet top-level domain.  Test your own domain in the validation step before you commit to it.  Then there's the internal network the runtime uses, `198.18.0.0/15` by default.  If that overlaps anything in your management, VM, or IP pool networks you get routing conflicts that break connectivity to the runtime cluster, and the documented alternatives are `240.0.0.0/15` and `250.0.0.0/15`.

What you can actually configure depends on your target version, and this is where older walkthroughs bite.  The July [upgrade guide on the VCF blog](https://blogs.vmware.com/cloud-foundation/2026/07/28/modernizing-infrastructure-vmware-cloud-foundation-9-0-x-to-9-1-upgrade-guide) describes staging the pool with strict CIDR notation in the UI, which is accurate for 9.1.0.0 through 9.1.0.300.  From 9.1.0.400 the UI also accepts exclusions and comma-separated IP lists, and from 9.1.1 the UI lets you pick the deployment network and the internal CIDR.  If your management network is tight on addresses, the API's `xRegionNetwork` parameter lets you deploy onto a VLAN-backed network instead ([Deploy VCF Management Services and License Server](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/deploy-vcf-management-services.html)).  The upcoming series walks through a real allocation from my lab.

**Pass condition:** your network worksheet matches the current documentation for your exact target, with DNS records, pool ranges, and the internal CIDR all reviewed together.

## Gate 3: Turn the component list into an owned sequence

A list of products to upgrade is not a change plan.  Fleet-level components and the management domain are a mandatory part of the 9.1.x upgrade, while workload domains can follow later as a Day-N task once their management domain is done.  The 9.0.x table in the docs gives you the order, starting with VCF Operations and the cloud proxy, then SDDC Manager, then the new management services and License Server, and on down through NSX, vCenter, ESX, and the NSX Edge finalize.  It also carries conditions that will catch you if you skim.

Two of them deserve a spot on the change record.  First, if your appliance-mode Identity Broker 9.0.x sits on an NSX overlay segment, or on a network or datastore different from where the management services will land, you have to redeploy it before the VCF Operations upgrade, because the new services runtime and the Identity Broker must live on the same network.  Second, once VCF Operations reaches 9.1 you cannot manage certificates and passwords for VCF Automation, the Identity Broker, Operations for Logs, and Operations for Networks until each of those is upgraded too.  Any rotation due on those components needs to happen before the window opens or wait until after their turn in the sequence.  The upcoming series digs into that freeze window, and you'll also want a cloud proxy in the instance that hosts VCF Operations, since the management services deployment depends on it.

For each phase, write down four things: who executes and verifies it, what must already be true, what evidence proves it finished, and what stops you from moving to the next phase.  The goal isn't fewer steps, it's making every step someone's job.

**Pass condition:** every phase has a named owner and an observable exit condition, and every conditional component in your environment has been accounted for.

## Gate 4: Prove recovery and hand off the Day-2 rules

Before the window, confirm that recent backups exist and that you know where they live and who can restore from them.  For this upgrade that means native file-based backups for the vCenter appliances and SFTP backup targets for SDDC Manager and VCF Operations, plus your NSX Managers.  The evidence goes in the change record along with the recovery owner and the product-specific restore procedure.  A snapshot of everything is not a recovery plan.

Then read the post-deployment restrictions, because they belong in the operational handoff.  After the management services are deployed, don't move their VMs to a different resource pool or VM folder, because later patching, deployment, and scale-out operations will fail.  Storage vMotion of those nodes to a different datastore is unsupported for the same reason.  The docs also note that Storage DRS is disabled by default on the deployment starting with VCF 9.1 EP2, so if your runtime was deployed on an earlier build, confirm that setting yourself instead of assuming it.  One more handoff item: the SDDC Manager UI is being deprecated, and after the upgrade completes the docs point you to VCF Operations for lifecycle work.

**Pass condition:** recovery responsibility is assigned and backed by evidence, and the team that runs the platform knows which housekeeping tasks are now off limits.

## Gate 5: Put the automation workstation in the change

The platform isn't the only thing that moves.  Your PowerCLI modules, SDKs, language runtimes, and scheduled scripts all have compatibility boundaries of their own, and the September [VCF 9.1.1 automation update](https://blogs.vmware.com/cloud-foundation/2026/09/18/strengthening-the-programmable-infrastructure-security-and-hardening-in-vcf-9-1-1) spells them out.  The VCF Python SDK 9.1.1.0 supports Python 3.10 through 3.14, and the Java SDK now requires Java 17 or later.  VCF PowerCLI 9.1.1 adds Python 3.14 support for Image Builder, drops Python 3.7 through 3.9, and raises the minimum PowerShell Core version to 7.0.13.  It also fixes Open-VMConsoleWindow failures against servers using newer certificate checksum algorithms, which is a good reminder that certificate handling is part of your automation testing too.

Those are boundaries, not a recommendation to install the oldest runtime that still qualifies.  Keep the validation small.  Capture the versions on the machine that actually runs your scheduled jobs, not just your interactive shell.  Test your chosen SDK, module, and runtime combination in a separate environment, run representative authentication and inventory workflows read-only first, and only then move on to the write operations you've approved.

**Pass condition:** the automation you use to operate the platform has its own test evidence, instead of inheriting a green status from the infrastructure upgrade.

## The readiness packet

Keep it short enough that somebody will read it at the change review:

- Exact source and target inventory, with builds
- Dated upgrade-path and interoperability references
- Phase sequence with owners, exit conditions, and stop conditions
- Network, DNS, certificate, and address-allocation evidence
- Backup and recovery evidence, plus the Day-2 placement rules
- Automation validation results
- Post-upgrade checks for authentication, licensing, monitoring, and lifecycle operations

A worksheet version of this packet is available if you'd rather fill something in than build it from scratch.  It has one page per gate with owner, evidence, pass, and stop fields, plus a go/no-go page and a post-upgrade validation table.  Grab the [PDF](ithinkvirtual-vcf-9-1-upgrade-readiness-checklist.pdf) to print or the [editable DOCX](ithinkvirtual-vcf-9-1-upgrade-readiness-checklist.docx) to adapt.

None of this is paperwork for its own sake.  It's about surfacing the assumptions while there's still time to fix them, and about building the plan around the exact target you're deploying instead of a familiar version label.

If you run this against your own environment and find a gate I missed, drop a comment and let me know.

-virtualex-
