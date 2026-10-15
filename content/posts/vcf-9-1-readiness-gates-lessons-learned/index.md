{
  "title": "VCF 9.1 Readiness Gates: What Held Up and What Didn't",
  "date": "2026-10-13T20:30:00-04:00",
  "lastmod": "2026-10-13T20:30:00-04:00",
  "slug": "vcf-9-1-readiness-gates-lessons-learned",
  "url": "/posts/vcf-9-1-readiness-gates-lessons-learned/",
  "draft": false,
  "description": "I ran my nested lab through the five readiness gates while upgrading VCF 9.0.2 to 9.1.1. Here is what held up, where the lab pushed back, and the one gate I would add.",
  "featured_image": "readiness-gates-lessons-learned.png",
  "categories": [
    "Home Lab",
    "VMware Cloud Foundation"
  ],
  "tags": [
    "VCF",
    "VMware",
    "Upgrade",
    "Lifecycle Management",
    "homelab"
  ],
  "years": [
    "2026"
  ],
  "aliases": [],
  "comments": []
}

Before I started the [upgrade series](/posts/vcf-9-1-upgrade-series-overview/), I wrote down [five readiness gates](/posts/vcf-9-1-upgrade-readiness-five-gates/) I'd want in front of anyone booking a window for a 9.0.x to 9.1.x upgrade.  Now that I've run the whole thing end to end, here's what held up and what didn't.  This is a nested lab, not production, so read it as a rehearsal and not as evidence.

## Gate 1: Prove the upgrade path

The path itself was fine.  I went straight from 9.0.2 to 9.1.1, and I took the planner's vCenter warning for 9.1.1 at face value: the vCenter NTP precheck fails on appliances with a non-UTC time zone, so I put both vCenters on UTC before I started and never found out whether it would have bitten me ([Part 4](/posts/vcf-9-1-upgrade-part-4-nsx-vcenter/)).  Where the gate fell short was the build.  "9.1.1" isn't specific enough.  My first ESX image was on the 9.1.1.0100 patch build, and **Assign Image** only offered images on the BOM build, `9.1.1.0.25714478` ([Part 5](/posts/vcf-9-1-upgrade-part-5-esxi-nsx-edge/)).  The inventory in your readiness packet should record the build the upgrade expects, not the newest one you can download.

## Gate 2: Treat the management network as a deployment dependency

This one held.  The `/27` I reserved for the services runtime was enough, and my `demo.lab` domain passed the FQDN validator, so the `.local` rejection never applied to me ([Part 2](/posts/vcf-9-1-upgrade-part-2-sddc-manager-management-services/)).  What I'd add is that the address plan isn't finished after the management services.  VCF Automation wanted its own runtime pool and FQDN, and so did log management, so the second round of planning lands in [Part 3](/posts/vcf-9-1-upgrade-part-3-automation-logs/).

## Gate 3: Turn the component list into an owned sequence

The sequence worked, and the capacity part of it is where my lab pushed back.  The VCF Automation and log management upgrades stand up new instances beside the old ones, and the upgrade powers the old ones off without deleting them.  My management cluster ran short of space, and the prechecks said so: three vSAN what-if errors in [Part 4](/posts/vcf-9-1-upgrade-part-4-nsx-vcenter/), and two "Are enough resources for EMM present" errors on the ESX precheck in [Part 5](/posts/vcf-9-1-upgrade-part-5-esxi-nsx-edge/).  I ended up deleting the old appliances and the SDDC Manager snapshot sooner than I'd planned, and the precheck came back clean afterward.  Put the cleanup, and the room you need before it, in the change record.

## Gate 4: Prove recovery and hand off the Day-2 rules

Most of the evidence was there: SFTP backups for SDDC Manager, file-based backups for both vCenters, NSX Manager backups, and a cold SDDC Manager snapshot.  The gap was the components that move to the new lifecycle plane.  The on-demand **Back Up Now** failed for VCF Automation and log management on 9.0.2 with "invalid for backup generation", so I had no VCF-level backup of either one going into [Part 3](/posts/vcf-9-1-upgrade-part-3-automation-logs/).  If you can't back a component up before the window, say so in the packet and decide who accepts that.

## Gate 5: Put the automation workstation in the change

Nothing needed attention.  I used PowerCLI on PowerShell 7 for the snapshots and the deletes, and it behaved.

## What the gates didn't cover

Two things hurt that none of the gates asked about.

The first is the health of each component before the window.  My first VCF Automation precheck failed on a platform health check, and I traced it to 976 pods stuck in Pending on the old Automation node (the scheduler had stopped, and nothing restarted it).  The log management upgrade failed too, with "Fleet LCM migrate task timed out", and I ended up deploying log management fresh instead of upgrading it.  A pre-window health check of every component, on the component's own terms, would have caught the first one.  It would be my sixth gate.

The second is the platform under the platform.  My workload hosts are nested ESX VMs on an NFS datastore, and their virtual NVMe disks had been rejecting UNMAP requests.  The ESX remediation failed twice before I found it ([Part 6](/posts/vcf-9-1-upgrade-part-6-housekeeping-workload-domain/)).  If you run nested hosts, check the hosts' own health before the window and not just VCF's.

## The short version

The five gates held up.  They didn't fail me anywhere, but the lab showed me that three of them need more than a pass condition: Gate 1 needs the exact build, Gate 3 needs the room to clean up, and Gate 4 needs a plan for components you can't back up.  If one of them bit you differently, drop a comment and let me know.

-virtualex-
