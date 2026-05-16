{
  "title": "Upgrading VMware vSphere Data Protection (VDP)",
  "date": "2017-03-27T21:20:59",
  "lastmod": "2017-03-27T21:20:59",
  "slug": "upgrading-vmware-vsphere-data-protection",
  "url": "/posts/upgrading-vmware-vsphere-data-protection/",
  "draft": false,
  "description": "Having a backup solution is imperative in any IT environment, whether it be Production or a simple Home Lab like I have.  There are many different brands and companies that offer backup solutions, such as Veeam or Nakivo, to name a few.  But I personally like to stick with the VMware product line so that I…",
  "wordpress_id": 872,
  "wordpress_url": "https://ithinkvirtual.com/2017/03/27/upgrading-vmware-vsphere-data-protection/",
  "featured_image": "/uploads/2017/03/VDP_BG.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "VDP",
    "vSphere Data Protection",
    "vSphere"
  ],
  "years": [
    "2017"
  ],
  "aliases": [
    "/2017/03/27/upgrading-vmware-vsphere-data-protection/"
  ],
  "comments": []
}

Having a backup solution is imperative in any IT environment, whether it be Production or a simple Home Lab like I have.  There are many different brands and companies that offer backup solutions, such as Veeam or Nakivo, to name a few.  But I personally like to stick with the VMware product line so that I can build the necessary skills and knowledge of their software, required to successfully grow and advance my career.  My personal choice, and preferred backup solution, is VMware vSphere Data Protection (VDP) since it’s fairly simple to deploy, configure, and manage.

VDP is a robust, simple-to-deploy, disk-based backup and recovery solution that delivers storage-efficient backups through patented variable-length deduplication, rapid recovery, and WAN-optimized replication for disaster recovery (DR).  Plus, it’s vSphere-integration and simple user interface makes it an easy and effective backup tool.  Additionally, it is now bundled with vSphere Standard, Enterprise Plus, and vSphere with Operations Management Enterprise Plus by default.

Since I have recently rebuilt by personal home-datacenter, I opted to deploy VDP 6.1.3 in my environment.  Version 6.1.3 was released back in November 2016, and just recently, version 6.1.4 was released on March 16, 2017.  Of course, as I always like to be on the latest and greatest versions of software, I just had to upgrade my appliance.  So before starting any upgrade, I always like to refer to the official documentation for upgrade procedures and best practices, but I wasn’t really able to find anything out there on the “inter-webs”.  So I figured, “what the heck, why not just give it a go and make my own documentation?”.  Not only will this be beneficial to me, but I hope that it will also help others in the community who’d like to update their appliances as well.  Let’s get to it!…

Prerequisites:

- Snapshot of your current VDP appliance

If you do not take a snapshot, you will be prompted to do so before you’re even allowed to perform the upgrade.

As previously mentioned, I will be upgrading my appliance from 6.1.3 to 6.1.4.

![](/uploads/2017/03/vdp1-300x196.png)

Begin by taking a snapshot of your current appliance, then attach the VDP Upgrade .ISO media to the appliance.

![](/uploads/2017/03/vdp3-300x151.png) ![](/uploads/2017/03/vdp4-300x151.png) ![](/uploads/2017/03/vdp5-300x151.png)

Login to the application’s web UI and click on the Upgrade tab.  It should automatically detect the presence of the ISO and begin reading it for updates but if it does not, click the Check Upgrades button.  Allow up to 15 minutes or more for the scan to complete before you can proceed with the upgrade.

![](/uploads/2017/03/vdp6-300x151.png)

Once the appliance has detected the available upgrade, click on the upgrade version to select it, then click the Upgrade VDP button.

![](/uploads/2017/03/vdp7-300x151.png) ![](/uploads/2017/03/vdp8-300x151.png)

If you had not taken a snapshot prior to upgrading the appliance, you will be presented with the following, hence the reason I listed this step as a prerequisite.

![](/uploads/2017/03/vdp9-300x151.png)

The upgrade process will now begin by first preparing the package for installation, which can take about 15 minutes or so, so now would be a good time to grab a beer or some coffee!

![](/uploads/2017/03/vdp10-300x151.png)

Afterwards, the actual installation will begin and you shall see the following set of instructions.

![](/uploads/2017/03/vdp11-300x151.png)

From my experience, I did not see the progress bar complete to 100%.  Instead, it disconnected itself from the web UI.  I realized that this meant it was beginning to stop its services and shut itself down.

![](/uploads/2017/03/vdp12-300x151.png)

Before having come to this realization, I tried to reload the web UI but would simply get a blank screen.

![](/uploads/2017/03/vdp13-300x151.png)

Eventually, I took a look at the VDP appliance console I had previously opened, and noticed the appliance was indeed powered off.   I confirmed by also checking the current status via the Web Client.  This is a good sign as the instructions stated the appliance will shut itself down after the upgrade has completed.

![](/uploads/2017/03/vdp14-300x196.png) ![](/uploads/2017/03/vdp15-300x151.png)

So now that the appliance was shutdown, the instructions explicitly stated to delete the snapshot before restarting the appliance.  Normally, I would wait until after to machine has booted up successfully before I delete a snapshot, just in case something went wrong, but in this case VMware stated this for a reason so I went ahead and deleted the snapshot.

![](/uploads/2017/03/vdp16-300x151.png)

It also stated to reconfigure the disk mode for any disks used by the VDP datastore to “Independent-Persistent”.  I went ahead and checked and saw that it was already set to that mode by default so I didn’t have to change anything there.

Finally, I booted up the appliance and to my delight, the appliance was now running version 6.1.4!  This turned out to be easier than expected!

![](/uploads/2017/03/vdp17-300x196.png)

I’d like to thank you for reading, and hope that you’ve found this content to be useful.  Please rank this post, feel free to comment, and subscribe to my blog!

-virtualex
