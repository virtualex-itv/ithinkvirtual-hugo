{
  "title": "Creating a Single-Node VSAN",
  "date": "2016-05-02T14:00:54",
  "lastmod": "2018-02-10T15:06:31",
  "slug": "creating-a-single-node-vsan",
  "url": "/posts/creating-a-single-node-vsan/",
  "draft": false,
  "description": "Creating a Single-Node VSAN   Many of us homelab enthusiasts tend to build “whitebox” systems from spare PC parts and a few internal hard drives for local storage that we’ve either ordered or had laying around in order install ESXi and run a single-node lab environment.  VMware Virtual SAN (VSAN) enables the ability to build…",
  "wordpress_id": 443,
  "wordpress_url": "https://ithinkvirtual.com/2016/05/02/creating-a-single-node-vsan/",
  "featured_image": "/uploads/2016/05/CNvYkfJUEAEwlBb.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "vSAN"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/05/02/creating-a-single-node-vsan/"
  ],
  "comments": [
    {
      "author": "Danny Estevez",
      "date": "2017-03-14T16:42:00",
      "content": "<p>Thanks for the reply.<br />\nI was able to figure it out and got it working.<br />\nOn to trying to Register a vCenter Appliance.</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-03-14T11:53:00",
      "content": "<p>@dannyestevez:disqus &#8211; it seems like you are on the right track but missing part of the command.  Just like the error states, you need to add the -d (or &#8211;disks) parameter.  When I look at what you entered, you only added the -s for the &#8220;cache disk&#8221;.  Even though both disks are SSD&#8217;s, 1 needs to be used as &#8220;cache&#8221; and the other needs to be used for &#8220;data&#8221; hence the -d parameter needs to be specified.  </p>\n<p>Example:<br />\nesxcli vsan storage add -s  -d </p>\n<p>Your correct statement/syntax should be as follows:<br />\nesxcli vsan storage add -s t10.NVMe____Samsung_SSD_950_PRO_512GB_______________4C8AB06158382500 -d t10.ATA_____Samsung_SSD_850_EVO_1TB_________________S2RENX0HB08493A_____</p>\n<p>Try this and let me know of you are successful, then you can continue following the how-to.</p>\n"
    },
    {
      "author": "Danny Estevez",
      "date": "2017-03-13T16:35:00",
      "content": "<p>I am trying to create a vSan using only SSD drives but am running into some issues. </p>\n<p>I have 2 Intel NUC&#8217;s. </p>\n<p>Here are the specs:<br />\n2 &#8211; Intel NUC i5 6th Gen</p>\n<p>32GB Memory in each</p>\n<p>2 &#8211; Samsung NVMe M.2 512GB</p>\n<p>2 &#8211; Samsung 850 EVO 1TB SSD</p>\n<p>2 &#8211; SanDisk 16GB Ultra Fit USB</p>\n<p>ESXi 6.5</p>\n<p>I was able to install ESXi 6.5 on the USB drives and the servers boot up with no issues. </p>\n<p>When I attempt to create the vSan this is what I am seeing:</p>\n<p>vdq -q command:</p>\n<p>[root@ESXi-1:~] vdq -q<br />\n[<br />\n   {<br />\n      &#8220;Name&#8221;     : &#8220;t10.SanDisk00Ultra_Fit000000000000004C530001151112120280&#8221;,<br />\n      &#8220;VSANUUID&#8221; : &#8220;&#8221;,<br />\n      &#8220;State&#8221;    : &#8220;Ineligible for use by VSAN&#8221;,<br />\n      &#8220;Reason&#8221;   : &#8220;Has partitions&#8221;,<br />\n      &#8220;IsSSD&#8221;    : &#8220;0&#8221;,<br />\n&#8220;IsCapacityFlash&#8221;: &#8220;0&#8221;,<br />\n      &#8220;IsPDL&#8221;    : &#8220;0&#8221;,<br />\n   },</p>\n<p>   {<br />\n      &#8220;Name&#8221;     : &#8220;t10.ATA_____Samsung_SSD_850_EVO_1TB_________________S2RENX0HB08493A_____&#8221;,<br />\n      &#8220;VSANUUID&#8221; : &#8220;&#8221;,<br />\n      &#8220;State&#8221;    : &#8220;Eligible for use by VSAN&#8221;,<br />\n      &#8220;Reason&#8221;   : &#8220;None&#8221;,<br />\n      &#8220;IsSSD&#8221;    : &#8220;1&#8221;,<br />\n&#8220;IsCapacityFlash&#8221;: &#8220;1&#8221;,<br />\n      &#8220;IsPDL&#8221;    : &#8220;0&#8221;,<br />\n   },</p>\n<p>   {<br />\n      &#8220;Name&#8221;     : &#8220;t10.NVMe____Samsung_SSD_950_PRO_512GB_______________4C8AB06158382500&#8221;,<br />\n      &#8220;VSANUUID&#8221; : &#8220;&#8221;,<br />\n      &#8220;State&#8221;    : &#8220;Eligible for use by VSAN&#8221;,<br />\n      &#8220;Reason&#8221;   : &#8220;None&#8221;,<br />\n      &#8220;IsSSD&#8221;    : &#8220;1&#8221;,<br />\n&#8220;IsCapacityFlash&#8221;: &#8220;1&#8221;,<br />\n      &#8220;IsPDL&#8221;    : &#8220;0&#8221;,<br />\n   },</p>\n<p>When attempting to add the flash drives to the vSan Datastore:</p>\n<p>[root@ESXi-1:~] esxcli vsan storage add -s t10.NVMe____Samsung_SSD_950_PRO_512GB<br />\n_______________4C8AB06158382500<br />\nError: Missing required parameter -d|&#8211;disks</p>\n<p>Usage: esxcli vsan storage add [cmd options]</p>\n<p>Description:<br />\n  add                   Add physical disk for VSAN usage.</p>\n<p>Cmd options:<br />\n  -d|&#8211;disks=[  &#8230; ]<br />\n                        Specify hdds to add for use by VSAN. Expects an empty<br />\n                        disk with no partitions in which case the disk will be<br />\n                        partitioned and formatted. Otherwise this operation<br />\n                        will fail. The command expects the device name for the<br />\n                        disk to be provided, e.g.: mpx.vmhba2:C0:T1:L0.<br />\n                        Multiple hdds can be provided using format -d hdd1 -d<br />\n                        hdd2 -d hdd3 (required)<br />\n  -s|&#8211;ssd=        Specify ssd to add for use by VSAN. Expects an empty<br />\n                        ssd with no partitions in which case the ssd will be<br />\n                        partitioned and formatted. Otherwise this operation<br />\n                        will fail. If an ssd which is already added for use by<br />\n                        VSAN, is provided along with &#8216;-d/&#8211;disks&#8217;, then the<br />\n                        disk mentioned with &#8216;-d&#8217; will be added to the existing<br />\n                        diskgroup created under this ssd and in which case,<br />\n                        the ssd won&#8217;t be partitioned and formatted. The<br />\n                        command expects the device name for the disk to be<br />\n                        provided, e.g.: mpx.vmhba2:C0:T1:L0 (required)</p>\n<p>Not sure what I am doing wrong. </p>\n<p>Let me know if you require more information.</p>\n<p>Any help will be greatly appreciated. </p>\n<p>Thanks,<br />\nDanny</p>\n"
    },
    {
      "author": "Danny Estevez",
      "date": "2017-03-13T16:08:00",
      "content": "<p>I am trying to create a vSan datastore using all Flash drives.<br />\nI have 2 Intel Nuc&#8217;s i5 6th Gen.<br />\nI have the following drives installed locally on each:<br />\n1 Samsung SSD 850EVO 1TB<br />\n1 Samsung NVMe SSD 950 512GB M.2</p>\n<p>When I run &#8220;vdq -q&#8221; the following names are displayed for my drives:<br />\nt10.ATA_____Samsung_SSD_850_EVO_1TB_________________S2RENX0HB08493A_____</p>\n<p>t10.NVMe____Samsung_SSD_950_PRO_512GB_______________4C8AB06158382500</p>\n<p>When I run the following command: &#8220;esxcli vsan storage add -s t10.NVMe____Samsung_SSD_950_PRO_512GB<br />\n_______________4C8AB06158382500&#8221;</p>\n<p>I get the following message: </p>\n<p>&#8220;Error: Missing required parameter -d|&#8211;disks</p>\n<p>Usage: esxcli vsan storage add [cmd options]&#8221;</p>\n<p>What am I doing wrong?</p>\n<p>Any help is greatly appreciated.<br />\nThanks,<br />\nDanny</p>\n"
    },
    {
      "author": "Claudio",
      "date": "2017-03-03T09:38:00",
      "content": "<p>Hi,<br />\ni have this problem when i add the 2 disks to vsan:<br />\nCOMMAND: esxcli vsan storage add -s t10.ATA_____XXXXX -d t10.ATA_____YYYY</p>\n<p>This is error:<br />\nUnable to add device: Disk with VSAN uuid 52c716ea-&#8230;&#8230;.. failed to appear in CMMDS</p>\n<p>Anyone have the same problem?<br />\nthank you</p>\n"
    }
  ]
}

**Creating a Single-Node VSAN**

Many of us homelab enthusiasts tend to build “whitebox” systems from spare PC parts and a few internal hard drives for local storage that we’ve either ordered or had laying around in order install ESXi and run a single-node lab environment.  VMware Virtual SAN (VSAN) enables the ability to build a local SAN environment utilizing the local hard drives in the host.  The only downside/caveat is that you need a minimum of (3) ESXi hosts in a cluster to enable and configure VSAN.  ***Bummer!***

Well, thanks to some very smart people in the community, there is a way to create a VSAN on your single-node host!

Keep in mind that this is not supported by VMware and is recommended for testing purposes only and should not be done in a production environment so use at your own risk.

I will mention that this topic has been covered by other bloggers (one of my favorites, [William Lam](http://www.virtuallyghetto.com/2016/03/quick-tip-vsan-6-2-vsphere-6-0-update-2-now-supports-creating-all-flash-diskgroup-using-esxcli.html), and a few others…) in the community but for my own knowledge and sharing, I decided to write this post detailing how I configured this in my environment.

Below, I will show you how to configure a hybrid and an all-flash VSAN on your ESXi host.  Again, I remind you that running a single-node VSAN is not supported by VMware and you run the risk losing all your data in the event of a disaster scenario (system crash, etc.)  Please be sure to understand the risks when deciding to use this in your own home lab.

**Prerequisites:**

- (1) vCenter Server (Windows-based or VCSA)
- (1)ESXi host in a cluster
- (1) vmk for VSAN Traffic
- (1) SSD for Caching Tier
- (1) SSD for Capacity Tier (All-Flash configuration)…or…
- (1) HDD for Capacity Tier (Hybrid Configuration)
- SSH access to Host

For simplicity’s sake, I will be using a VCSA and ESXi VM deployed in VMware Workstation 12.1.1 Pro on Windows 10 for this demonstration.

![1](/uploads/2016/05/1-300x225.png) ![2](/uploads/2016/05/2-300x225.png)

Be sure that you have connected your ESXi host to your vCenter Server and have added it to a cluster, you ***do not*** need to enable VSAN on the cluster yet.  Add an additional vmk to your vSwitch for VSAN traffic.  Also ensure you have started the SSH service on the ESXi host.

Open an SSH session to your ESXi Host.  If you’ve added a vmk for VSAN but have not enabled it for VSAN traffic yet, enter the following command.

```shell
esxcli vsan network ipv4 add -i vmkN
```

(Where “N” is the number of your vmk port – ie: vmk1)

In my environment, I already created a VSAN vmk and enabled it for VSAN traffic so I was able to skip the command above.

![3](/uploads/2016/05/3-300x151.png)

Using the vSphere Web Client or C# client, verify the hard drive that you want to use for your VSAN datastore.  I will be using these drives, the 30GB will be my cache disk and the 120GB will be the capacity disk.

![4](/uploads/2016/05/4-300x151.png) ![5](/uploads/2016/05/5-300x140.png)

Back in your SSH session, enter the following command to determine and confirm the eligibility of the disks intended for use to create your VSAN.

```shell
vdq -q
```

![6](/uploads/2016/05/6-300x272.png)

Next, enter the following command to get the current default VSAN policy.

```shell
esxcli vsan policy getdefault
```

![7](/uploads/2016/05/7-300x272.png)

We will need to change the current policy by running the following commands.

```shell
esxcli vsan policy setdefault -c cluster -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1) (\"stripeWidth\" i1))"
esxcli vsan policy setdefault -c vdisk -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1) (\"stripeWidth\" i1))"
esxcli vsan policy setdefault -c vmnamespace -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1) (\"stripeWidth\" i1))"
esxcli vsan policy setdefault -c vmswap -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1) (\"stripeWidth\" i1))"
```

![8](/uploads/2016/05/8-300x195.png)

Run this command again to confirm that the policy has been changed.

```shell
esxcli vsan policy getdefault
```

![9](/uploads/2016/05/9-300x195.png)

Run the following command to create a new VSAN cluster

```shell
esxcli vsan cluster new
```

![10](/uploads/2016/05/10-300x195.png)

Now, since my disks are all SSD, I am creating an All-Flash VSAN configuration.  I need to run the following command to tag the capacity SSD as the data disk.  The “-d” represents the “capacity disk” and you need to specify the identifier of the disk to tag.  You can simply copy the identifier number directly from the ESXi hosts storage devices section in Web Client/C# Client, or from the SSH session where we ran the “vdq -q” command.

***Note*** – If you are deploying a Hybrid VSAN, this command is not needed so you can skip to the next command to add the “cache & capacity” disks to your VSAN.

```shell
esxcli vsan storage tag add -d <disk identifier> -t capacityFlash
```

![11](/uploads/2016/05/11-300x195.png)

If you’d like to confirm that the disk has been tagged for “capacityFlash” simply run the “vdq -q” command again and check the disk.

![12](/uploads/2016/05/12-300x201.png)

Next, run the following command to add both your disks (cache & capacity) to your VSAN storage volume.  The “-s” represents the SSD “cache disk”, and the “-d” represents the “capacity disk”.  Be sure to enter the correct identifier number for the respective disks.

```shell
esxcli vsan storage add -s <disk identifier> -d <disk identifier>
```

![13](/uploads/2016/05/13-300x201.png)

 Run the following command to show the VSAN cluster info.

```shell
esxcli vsan cluster get
```

![14](/uploads/2016/05/14-300x195.png)

Run the following command to list the VSAN storage

```shell
esxcli vsan storage list
```

![15](/uploads/2016/05/15-300x195.png)

Congratulations, if everything has been followed correctly, you should now have created a single-node VSAN datastore!

![16](/uploads/2016/05/16-300x151.png) ![17](/uploads/2016/05/17-300x164.png)

But we are not quite finished just yet.  Even though I can see the VSAN datastore, I still want to officially enable VSAN on the cluster in vCenter.  Do the following…

![18](/uploads/2016/05/18-300x151.png) ![19](/uploads/2016/05/19-300x151.png) ![20](/uploads/2016/05/20-300x151.png)

In my environment, I have an extra disk in my host, but I do not want to claim this as part of my VSAN.  So, from the drop-down menu, I selected “Do not claim” and hit Next then Finish.

![21](/uploads/2016/05/21-300x151.png) ![22](/uploads/2016/05/22-300x151.png)

Now I can see that VSAN is “Turned On” and can see the disks that are associated with the Disk Group.

![23](/uploads/2016/05/23-300x151.png) ![24](/uploads/2016/05/24-300x151.png)

But, there’s still a bit more to be done for me to be able to provision VMs on this datastore.  I need to edit the VSAN VM Storage Policy.  Personally, I prefer to leave the default policies intact and instead create a new policy for my single-node datastore.  I will show both editings of the default policy, for those who do not want to bother with creating a new policy, as well as creating a new policy.  First, let’s check the VASA storage provider and ensure it has been synchronized so that we can edit/create our VSAN Storage policy.

![25](/uploads/2016/05/25-300x151.png) ![26](/uploads/2016/05/26-300x151.png)

**Editing Virtual SAN Default Storage Policy**

![27](/uploads/2016/05/27-300x151.png)

Here we need to simply change:

- Number of failures to tolerate = 0 (Default is 1)
- Force provisioning = Yes (Default is No)

![28](/uploads/2016/05/28-300x151.png)

**Creating a new Virtual SAN Storage Policy**

![30](/uploads/2016/05/30-300x151.png)

Give it a Name and a Description then hit **Next**.

![29](/uploads/2016/05/29-300x151.png)

Select VSAN from the “Rules based on data services” drop-down, then add all the rules from the drop-down and configure the same settings mentioned above, then hit **Next** and **Finish**.

- Number of failures to tolerate = 0 (Default is 1)
- Force provisioning = Yes (Default is No)

![31](/uploads/2016/05/31-300x151.png) ![32](/uploads/2016/05/32-300x151.png)

And, there you have it!  A fully functional Single-Node VSAN to provision VMs on.  You still have to add a VSAN license, but that will not be covered here as you should already be familiar with the licensing process.

![33](/uploads/2016/05/33-300x151.png)

**The Finishing touches**

The following optimizations commands are optional but highly recommended for better performance and stability in your VSAN environment.

Since this is a homelab, the disks I used may not be on the official VMware HCL and can potentially impact the performance of the lab environment.  Corman Hogan wrote a great [blog](http://cormachogan.com/2015/09/22/vsan-6-1-new-feature-problematic-disk-handling/) and included a tip on how to disable VSAN device monitoring.  Open an SSH session to your host again and run the following command.

```shell
esxcli system settings advanced set -o /LSOM/VSANDeviceMonitoring -i 0
```

To confirm that the command was successful, run the following command.  It should return a value of “0” as the default value is “1”.

```shell
esxcfg-advcfg -g /LSOM/VSANDeviceMonitoring
```

![34](/uploads/2016/05/34-300x201.png)

Cormac Hogan also wrote another great [post](http://cormachogan.com/2016/02/22/vsan-6-2-part-5-new-sparse-vm-swap-object/) about the new “Sparse VM Swap Object”.  ESXi 6.0 Update 2 (aka 6.2) brings a new setting in VSAN 6.2 which allows VSAN to provision a VM swap object as thin instead of thick, where thick has historically been the default.  So if you’d like to disable thick provisioning and use thin, run the following command.

```shell
esxcli system settings advanced set -o /VSAN/SwapThickProvisionDisabled -i 1
```

To confirm, run the following command.  It should return a value of “1” as the default value is “0”.

```shell
esxcfg-advcfg -g /VSAN/SwapThickProvisionDisabled
```

![35](/uploads/2016/05/35-300x201.png)

And last, but definitely not least, if you intend on running any Nested ESXi VMs on your newly created VSAN, be sure to run the following command to prevent any errors when trying to create SCSI disks for your ESXi VM.  This will enable an advanced ESXi setting that will “fake” SCSI reservations.  William Lam has a nice post about this [here](http://www.virtuallyghetto.com/2013/11/how-to-run-nested-esxi-on-top-of-vsan.html).

```shell
esxcli system settings advanced set -o /VSAN/FakeSCSIReservations -i 1
```

And to confirm it took, run the following command.  It should return a value of “1” as the default value is “0”.

```shell
esxcfg-advcfg -g /VSAN/FakeSCSIReservations
```

![36](/uploads/2016/05/36-300x201.png)

That’s all folks!  I hope that you’ve found this post to be of use to you and I hope you come back for more content.  Feel free to comment, share, and subscribe!

Giving credit where it is due, shout out to [William Lam](https://twitter.com/lamw) and [Cormac Hogan](https://twitter.com/cormacjhogan)!

-virtualex-
