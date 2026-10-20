{
  "title": "Patching VMware Cloud Foundation 9.1.1, Part 1: Management Components",
  "date": "2026-10-19T23:08:00-04:00",
  "lastmod": "2026-10-19T23:08:00-04:00",
  "slug": "vcf-9-1-1-patch-part-1-management-components",
  "url": "/posts/vcf-9-1-1-patch-part-1-management-components/",
  "draft": false,
  "description": "Part 1 of my VCF 9.1.1 patch series: getting the lab ready, then patching Fleet Lifecycle, SDDC Manager, and the other VCF management components from VCF Operations.",
  "featured_image": "part-1-management-components.png",
  "categories": [
    "Home Lab",
    "How-To's",
    "VMware Cloud Foundation"
  ],
  "tags": [
    "VCF",
    "VMware",
    "Patching",
    "Lifecycle Management",
    "homelab"
  ],
  "years": [
    "2026"
  ],
  "aliases": [],
  "comments": []
}

In the [series overview](/posts/vcf-9-1-1-patch-series-overview/) I covered what's in the October 12th patch set and the caveats to know first.  This part patches the management plane.

<aside class="tested-on"><strong>Tested on</strong><dl><div><dt>Environment</dt><dd>Nested VCF 9.1.1 lab</dd></div><div><dt>Depot</dt><dd>Offline, VCF Download Tool</dd></div><div><dt>Covers</dt><dd>Fleet Lifecycle, SDDC Manager, VCF management components</dd></div></dl></aside>

## Patch binaries

On the instance's **Binary Management** tab, **Patch binaries** for VCF version 9.1 lists five patches, and I downloaded the vCenter, SDDC Manager, NSX, and ESX ones before planning anything.

![The patch binaries downloaded in Binary Management](binary-management-patch.png)

## Fleet Lifecycle first

The VCF management services Fleet Lifecycle component gets patched before any other VCF component, which is also the planner's first step ([Lifecycle Management of VCF Components](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/lifecycle-management-of-vcf-components.html)).  That guidance is written for 9.1.0.x environments and my lab is already on 9.1.1.0, so I'm treating the order as the safe one.

<aside class="info-block"><p>The <a href="https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/release-notes/vmware-cloud-foundation-9-1-1-0-release-notes.html">9.1.1 release notes</a>, under <strong>Getting to 9.1.1</strong>, say not to use the Upgrade All button in VCF Operations before you've met the 9.1.1 patching dependencies between components.</p></aside>

The Upgrade tab lists Fleet Lifecycle in its own section at the top, above the management components, and it already showed that an upgrade was available.

![The Upgrade tab with Fleet Lifecycle at the top](fleet-lifecycle-upgrade-tab.png)

1. In the **Fleet Lifecycle** section, click **Select version**.
2. In the **Fleet Lifecycle Component Target Version** dialog, pick the target version, 9.1.1.0200, and click **Set target version**.

![Picking the Fleet Lifecycle target version](fleet-lifecycle-target-version.png)

The dialog says the required binaries download from the depot automatically if they're available there.  Once the target was set, the section showed the move from 9.1.1.0100 to 9.1.1.0200, with **Upgrade** and **Check binary availability** buttons next to it.

![Fleet Lifecycle ready to upgrade](fleet-lifecycle-ready.png)

Then I clicked **Upgrade**.  The Fleet Lifecycle section changed to **Upgrade in progress** with an **Upgrade details** link.

![Fleet Lifecycle upgrade in progress](fleet-lifecycle-upgrade-in-progress.png)

Upgrade details shows the Fleet lifecycle Upgrade Workflow.  It started with two subtasks, setting the upgrade context for the workflow and staging the Fleet lifecycle plugin in the VCF services runtime.

![The Fleet lifecycle upgrade workflow](fleet-lifecycle-upgrade-workflow.png)

The workflow ran the prechecks, then staged the Fleet lifecycle package in the VCF services runtime, prepared Fleet lifecycle for the upgrade, performed the upgrade, and finished with an inventory sync.  Every subtask ended **Completed**.

<aside class="info-block"><p>The prechecks ran for a long time.  A stale cleanup workflow, <code>wal-s3-cleanup</code>, in my VCF services runtime had been holding the <code>vmsp-backuprestore</code> lock, and the precheck's backup check sat in Pending behind it.  I connected to the runtime over <a href="https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/fleet-management/configuring-management-components/enable-ssh-access-to-the-vcf-services-runtime-cluster.html">SSH</a>, found the workflow with <code>kubectl -n vmsp-platform get workflows</code>, and deleted it.  The lock was released and the precheck moved on.</p></aside>

![The Fleet lifecycle Upgrade Workflow completed](fleet-lifecycle-upgrade-completed.png)

Back on the **Upgrade** tab, the Fleet Lifecycle section now shows 9.1.1.0200 as the current version.

![Fleet Lifecycle on 9.1.1.0200](fleet-lifecycle-new-version.png)

## SDDC Manager

SDDC Manager is patched from the management domain's **Upgrades** tab with a component upgrade plan, not from the VCF Management tab.  Updating only SDDC Manager doesn't change the management domain's version.  The target version has to be compatible with every BOM version in the instance, and the patch binary has to be in the software depot ([Upgrade or Patch SDDC Manager from VCF Operations](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/lifecycle-management-of-vcf-components/upgrade-sddc-manager-without-upgrading-vcf.html)).

1. In VCF Operations, go to **Build → Lifecycle**, expand **VCF Instances**, and select the management domain, **vcf-m01**.
2. On the **Upgrades** tab, click **Plan component upgrade**.
3. On **Select components and target version**, select **SDDC Manager**, **VMware ESX**, **VMware NSX**, and **VMware vCenter**, keep the target versions it offers, and click **Next**.
4. On **vCenter and NSX upgrade options**, pick the sequential option and click **Next**.
5. On **Plan overview**, click **Submit plan**.

I put all four components in one plan so the whole management domain follows one sequence.  The target versions were 9.1.1.0200 for SDDC Manager and 9.1.1.0100 for the other three.

![Selecting the components and target versions](plan-select-components.png)

The overview lists the steps in order and says SDDC Manager goes first to keep the rest compatible and orchestrated.

![The plan overview](plan-overview.png)

Once the plan was submitted, the **Upgrades** tab summarized it and offered **Edit plan** and **Cancel plan**.  The **Upgrade Sequence** showed 0 of 5 steps completed, with **Upgrade now** and **Schedule** available for SDDC Manager and the steps after it grayed out.

![The submitted plan](plan-submitted.png)

Before upgrading anything, I ran a precheck against the whole domain.  In the **Run Prechecks** dialog I chose **Upgrade readiness** with the **Entire Workload Domain** scope.  That checked four components, among them the vCenter, the cluster, and NSX.

<aside class="info-block"><p>The dialog's <strong>Target version precheck</strong> option didn't give me anything to select.  When pending upgrade binaries are available, the <a href="https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/upgrade-the-management-domain-to-vmware-cloud-foundation-5-2/perform-upgrade-precheck.html">Target version drop-down</a> lists the available VCF versions to upgrade to, and none were offered for this domain.</p></aside>

![The Run Prechecks dialog with Upgrade readiness selected](precheck-run-dialog.png)

It came back clean.

![The upgrade readiness precheck results](precheck-results.png)

<aside class="info-block"><p>I didn't take a snapshot or backup first.</p></aside>

I clicked **Upgrade now** on the SDDC Manager step.  The upgrade runs through 16 steps, from the VCF prerequisite check to stopping the Common Appliance platform service, with the SDDC Manager reboot and a cleanup along the way.

![The SDDC Manager upgrade steps](sddc-manager-upgrade-steps.png)

After I clicked **Finish**, the domain version still read 9.1.1.0, as the patch page says it would, and **Component Versions** showed SDDC Manager **On Target**.  NSX, vCenter, and ESX still show **Version Drift** until I patch them.

![Component Versions after the SDDC Manager upgrade](component-versions-after-sddc-manager.png)

## The other management components

A few dependencies fix the order for the rest, and otherwise it's up to you ([Lifecycle Management of VCF Components](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/lifecycle-management-of-vcf-components.html)).  VCF Operations is the first of them.  It has to be patched on its own, before any ESX host, and no other lifecycle operation can run while it patches.

### VCF Operations

VCF Operations was next.

<aside class="info-block"><p>The Upgrade tab warns that VCF Operations must be patched independently from the other management components, and to wait for the patch to complete before proceeding with them.</p></aside>

1. In VCF Operations, go to **Build → Lifecycle → VCF Management** and open the **Upgrade** tab.
2. Next to **Target VCF version**, click **Select version**.
3. In the **Set Target Version** dialog, pick **9.1.1.0100.25795063** for VCF Operations and click **Set Version**.  I left every other component as it was.

![Picking the VCF Operations target version](vcf-operations-target-version.png)

The VCF Operations row then showed the move from 9.1.1.0.25679751 to 9.1.1.0100.25795063 and **Ready for upgrade**.

![VCF Operations ready for upgrade](vcf-operations-ready.png)

I ran the precheck first, and it passed.

![The VCF Operations precheck passed](vcf-operations-prechecks-passed.png)

Then I started the upgrade, and the row showed **Upgrade in progress** with an **Upgrade details** link.

![VCF Operations upgrade in progress](vcf-operations-upgrade-in-progress.png)

<aside class="info-block"><p>The upgrade logged me out of VCF Operations.  Once I could log in again, the upgrade had finished.</p></aside>

Upgrade details shows the VCF Operations Upgrade workflow, and every subtask ended **Completed**, from staging the precheck binaries to the inventory sync after the upgrade.

![The VCF Operations upgrade workflow completed](vcf-operations-upgrade-completed.png)

On the **Components** tab, VCF Operations now shows 9.1.1.0100.25795063.

![VCF Operations on 9.1.1.0100](vcf-operations-new-version.png)

The Cloud Proxy doesn't appear on the Components tab, so I checked **Administration → Cloud Proxies**.  It was **Online** and its OVA version read 9.1.1.0100.25795064.  The [VCF Operations 9.1.1.0100 release notes](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/release-notes/patch-releases-9-1-1-x/vcf-operations/9100100/vcf-operations-9-1-1-0100-release-notes.html) say the cloud proxy and license server are patched automatically with VCF Operations, so there was no step of its own.

![The Cloud Proxy on 9.1.1.0100 and Online](cloud-proxy-patched.png)

### The rest of the management components

With VCF Operations patched, I opened **Select version** again.  The **Set Target Version** dialog lists every management component with a target version, and I picked targets for the rest.

![Target versions for the remaining management components](remaining-components-target-versions.png)

I ran the prechecks on all of them before upgrading any.  Every row came back **Ready for upgrade** with its own precheck details.

![Prechecks complete on the remaining components](remaining-components-prechecks.png)

I ran them one at a time in this order.

| Order | Component | Why here |
| --- | --- | --- |
| 1 | **VCF services runtime** | It has to go before an Identity Broker or Salt RaaS instance it hosts. |
| 2 | **Identity broker** | After the runtime. |
| 3 | **Salt master** | Not required, but the master and RaaS are the same 9.1.1.0100 patch, so I kept them together. |
| 4 | **Salt RaaS** | After the runtime. |
| 5 | **VCF Automation** | It has to go before the Migration service engine. |
| 6 | **Migration service engine** | After VCF Automation. |
| 7 | **SDDC lifecycle** | Free of ordering rules, so it goes here. |
| 8 | **Log management** | Security enhancements only. |
| 9 | **Telemetry** | Security enhancements only. |
| 10 | **Software depot** | Last, because patching it blocks patching anything else. |

### VCF services runtime

The precheck had already passed on the **VCF services runtime** row, which showed the move from 9.1.1.0.25714471 to 9.1.1.0100.25801571, so I clicked **Upgrade** on that row.  I left **Upgrade (All)** alone and the other components stayed as they were.

Upgrade details shows the VCF services runtime Upgrade Workflow.  It sets the upgrade context, stages the runtime plugin, runs its own prechecks, stages the package, and prepares the runtime before it performs the upgrade.

![The VCF services runtime upgrade workflow in progress](vcf-services-runtime-upgrade-in-progress.png)

![The VCF services runtime upgrade workflow completed](vcf-services-runtime-upgrade-completed.png)

With the runtime done, its row dropped off the **Upgrade** tab and the rest of the components stayed **Ready for upgrade**.

![The Upgrade tab with the runtime row gone](upgrade-tab-after-runtime.png)

### Identity broker

I clicked **Upgrade** on the **Identity broker** row, which showed the move from 9.1.1.0.25679886 to 9.1.1.0100.25796677.  The workflow ran through the same subtasks as the runtime.

![The Identity broker upgrade workflow in progress](identity-broker-upgrade-in-progress.png)

![The Identity broker upgrade workflow completed](identity-broker-upgrade-completed.png)

### Salt master and Salt RaaS

I took Salt master first and clicked **Upgrade** on its row, which showed the move from 9.1.1.0.25679895 to 9.1.1.0100.25795075.  The workflow stopped at **Run Salt master prechecks** and the task showed **Failed**.

![The Salt master precheck failed on the backup workflow](salt-master-precheck-failed.png)

<aside class="info-block"><p>The error reads <strong>Backup workflow failed for component: salt</strong>.  I went looking for the failure in the backup that writes to the SFTP server under <strong>Backup &amp; Restore</strong>.  I connected to a runtime node over <a href="https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/fleet-management/configuring-management-components/enable-ssh-access-to-the-vcf-services-runtime-cluster.html">SSH</a>, and <code>kubectl -n vmsp-platform get workflows</code> showed a failed <code>component-backup</code> workflow.  Its <code>set-backup-globals</code> pod log reported an SSH fingerprint mismatch for the backup destination, and the stored fingerprint matched my NAS's RSA key.  I clicked <strong>Retry</strong>.</p></aside>

The retry passed, and the workflow ran on to the end.  The failed precheck stays in the list above the one that passed.

![The Salt master upgrade workflow completed after the retry](salt-master-upgrade-completed.png)

Salt RaaS was next, and it went through without a failed precheck.  I selected its row and clicked **Upgrade**, which moved it from 9.1.1.0.25679895 to 9.1.1.0100.25795075.

![The Salt RaaS row showing Upgrade in progress](salt-raas-upgrade-in-progress.png)

![The Salt RaaS upgrade workflow completed](salt-raas-upgrade-completed.png)

### VCF Automation and the Migration service engine

VCF Automation went first, since the Migration service engine has to wait for it.  I selected the VCF Automation row and clicked **Upgrade**, which moved it from 9.1.1.0100.25757808 to 9.1.1.0200.25801570.

![The VCF Automation row showing Upgrade in progress](vcf-automation-upgrade-in-progress.png)

The **Tasks** tab for this workflow shows each of the staging, precheck, and upgrade subtasks twice.

<aside class="info-block"><p>The last subtask, <strong>Inventory sync post VCF Automation upgrade</strong>, failed after the upgrade had already run, and the workflow went to <strong>Failed</strong>.  Every subtask before it had completed, so I clicked <strong>Retry</strong>.</p></aside>

![The VCF Automation workflow with the inventory sync subtask failed](vcf-automation-inventory-sync-failed.png)

The retry ran the inventory sync again and the workflow completed.  The failed subtask stays in the list above the two that passed.

![The VCF Automation upgrade workflow completed after the retry](vcf-automation-upgrade-completed.png)

With VCF Automation patched, the Migration service engine was next.  I selected its row and clicked **Upgrade**, which moved it from 9.1.1.0100.25757808 to 9.1.1.0200.25801570.

![The Migration service engine row showing Upgrade in progress](migration-service-engine-upgrade-in-progress.png)

The workflow on the **Tasks** tab calls it VCD_MIGRATOR.

![The Migration service engine upgrade workflow completed](migration-service-engine-upgrade-completed.png)

### SDDC lifecycle

SDDC lifecycle was next, and **Upgrade** on its row took it from 9.1.1.0100.25761870 to 9.1.1.0200.25801981.

![The SDDC lifecycle row showing Upgrade in progress](sddc-lifecycle-upgrade-in-progress.png)

![The SDDC lifecycle upgrade workflow completed](sddc-lifecycle-upgrade-completed.png)

### Log management and Telemetry

Log management went the same way, from 9.1.1.0.25679624 to 9.1.1.0100.25795095.

![The Log management row showing Upgrade in progress](log-management-upgrade-in-progress.png)

![The Log management upgrade workflow completed](log-management-upgrade-completed.png)

Telemetry was next, from 9.1.1.0.25671600 to 9.1.1.0100.25741214.

![The Telemetry row showing Upgrade in progress](telemetry-upgrade-in-progress.png)

![The Telemetry upgrade workflow completed](telemetry-upgrade-completed.png)

### Software depot

The Software depot went last, since a depot patch blocks patching anything else.  It was the only component left on the Upgrade tab.  I selected its row and clicked **Upgrade**, which moved it from 9.1.1.0.25713941 to 9.1.1.0200.25801072.

![The Software depot row showing Upgrade in progress](software-depot-upgrade-in-progress.png)

![The Software depot upgrade workflow completed](software-depot-upgrade-completed.png)

## Verifying

With the depot done, the Upgrade tab had nothing left to offer.  It reads "All components are at their target versions."

![The Upgrade tab showing all components at their target versions](all-components-at-target-versions.png)

The Components tab lists all 11 management components on their patched versions.

![The Components tab showing the patched versions of all 11 management components](component-versions-after-patching.png)

## What's next

In **[Part 2](/posts/vcf-9-1-1-patch-part-2-core-components/)**, I patch NSX Manager, vCenter, and ESX in both the management and workload domains, and finish the NSX Edge and finalize step.

-virtualex-
