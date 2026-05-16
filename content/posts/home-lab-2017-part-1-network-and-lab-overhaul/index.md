{
  "title": "Home Lab 2017 – Part 1 (Network and Lab Overhaul)",
  "date": "2017-02-12T18:53:49",
  "lastmod": "2017-02-13T12:41:47",
  "slug": "home-lab-2017-part-1-network-and-lab-overhaul",
  "url": "/posts/home-lab-2017-part-1-network-and-lab-overhaul/",
  "draft": false,
  "description": "For the last 6+ months, I haven’t had much time to dedicate to my home lab and overall home network.  Between holidays, transitioning to a new employer/role, and everyday life getting in the way, I found that I had to put everything on the back burner for a bit…so I inevitably shutdown by home lab….",
  "wordpress_id": 821,
  "wordpress_url": "https://ithinkvirtual.com/2017/02/12/home-lab-2017-part-1-network-and-lab-overhaul/",
  "featured_image": "/uploads/2017/02/Ubiquiti-UniFi-VMware-vSphere.png",
  "categories": [
    "Home Lab"
  ],
  "tags": [
    "homelab",
    "Ubiquiti",
    "UniFi",
    "vSphere"
  ],
  "years": [
    "2017"
  ],
  "aliases": [
    "/2017/02/12/home-lab-2017-part-1-network-and-lab-overhaul/"
  ],
  "comments": [
    {
      "author": "Paul Braren",
      "date": "2017-02-12T22:09:00",
      "content": "<p>Fantastic article, Alex, love the screenshots, wow!</p>\n"
    }
  ]
}

For the last 6+ months, I haven’t had much time to dedicate to my home lab and overall home network.  Between holidays, transitioning to a new employer/role, and everyday life getting in the way, I found that I had to put everything on the back burner for a bit…so I inevitably shutdown by home lab. Well now I am back and am looking forward to writing up some new material that I have been meaning to do for a while.  I will start this by saying this is a continuation of my [Home Lab 2016 Series](/categories/home-lab/), now being dubbed as “***Home Lab 2017***“!

So first and foremost, I powered up my home lab once again and I intend to leave it up and running at 100% uptime.  While doing so, my Synology NAS decided to reboot itself for an auto-update, right in the middle of a VM’s (my domain controller to be exact) boot process.  This would eventually cause my VMDK file to become corrupted and I could no longer boot my DC and reconnect my home lab.  I also had not yet backed anything up since the environment was still fairly new so I figured why not take this opportunity to rebuild everything and get some new components.

I decided to add a few more (3 per host to be exact), extremely quiet, [Noctua NF-A4x10 FLX](http://noctua.at/en/nf-a4x10-flx) 40mm  fans.  This will help to keep my ATOM CPU cool as well as exhaust any hot air from out of each case.  I had also been contemplating on doing a Network equipment overhaul.  Last year I upgraded my ASUS RT-AC68U SOHO Router with a Ubiquiti ERLite-3 EdgeRouter, and turned the ASUS into a wireless AP only.  I do not have a single complaint in the performance and overall stability of that setup.  But I recently began looking at the Ubiquiti UniFi gear, and noticed that it the Unified Security Gateway basically runs the same EdgeOS found in the ERLite-3, just with a different web-interface.  Realizing that we are in this new wave of cloud-managed networking, and seeing that the USG-3P was basically on-par with the ERLite-3, I bit the bullet and ordered my new Ubiquiti UniFi gear to replace my current setup.  The featureset in the EdgeRouter series of routers still has the edge over the UniFi’s features but it’s only a matter of time before they are equal, or UniFi surpasses the EdgeRouters.

I decided on the following products:

- [UniFi Controller Cloud Key](https://www.ubnt.com/unifi/unifi-cloud-key/) (UC-CK)
- [UniFi Security Gateway](https://www.ubnt.com/unifi-routing/usg/) (USG-3P)
- [UniFi Switch 8-60W](https://www.ubnt.com/unifi-switching/unifi-switch-8/) (US-8-60W)
- [UniFi AP-AC-Pro](https://www.ubnt.com/unifi/unifi-ap-ac-pro/) (UAP-AC-Pro)

After getting everything connected, I will say that I was extremely impressed with the ease of setup, current feature set, and the presentation of the Web UI.  I am not going to go into the specifics of how to set it all up, etc. as this is not a UniFi tutorial, but I will say that the little quick start guides tell you everything you need to know.  One can also consult “Mr. Google” for more information.

![](/uploads/2017/02/2017-02-12_13-08-05-150x150.png) ![](/uploads/2017/02/2017-02-12_13-08-59-150x150.png) ![](/uploads/2017/02/2017-02-12_13-09-25-150x150.png) ![](/uploads/2017/02/2017-02-12_13-09-49-150x150.png)

My only gripe with the current feature set of the USG-3P is that there is no support for Jumbo Frames…yet!…but hopefully that will come in a future firmware release.  The US-8-60W does indeed support Jumbo Frames so I enabled in on there at least for now.  Additionally, the VOIP LAN port on the USG-3P is there for a future release to add support for it.  I have also read some threads were feature requests have been submitted to allow said port to be used as a secondary LAN/WAN port instead of just for VOIP.  This is currently in beta, but once these settings are added, I feel it would bring the device closer to the capabilities of the ERLite-3 in terms of features. Only time will tell…

Now that I had my basic home network configured, LAN & WiFi-LAN, I powered on my Cisco lab switches and began migrating all of my VLANs over to the new USG-3P, thus removing the need for any static routing which I relied on with my previous setup.  Next, I powered on all of my hosts, and began upgrading them to ESXi 6.5.  Finally, I was finally on my way to getting up to the latest release of vSphere!  Once all of my hosts were upgraded, with the exception of my dev-host as the CPU is not supported in ESXi 6.5, I began spinning up a few new VMs.  I took this time to install Windows Server 2016 for my Domain Controllers, and decided to ditch the Windows-based vCenter server in favor of the vCenter Server Appliance (vCSA) since it now has vSphere Update Manager (vUM) integration and the appliance runs on VMware’s Photon OS.

Once my vSphere environment was minimally setup, I started to deploy some more VM’s with the vSphere Web Client, and I must say the speed and performance of the Web Client in 6.5 is “night-and-day” as compared to the Web Client in 6.0!  No more need for the Client Integration Plugin as the newer version for 6.5 runs as a service.  This is the way the web client should have been designed from the very beginning instead of making us all suffer because of how slow the Flash-based version previously was.  Although I always preferred to use the Web Client because of the features within it, I can see why so many users still used the C# “fat-client” instead.  Who wants to wait forever and a year just for the Hosts and Clusters view, or VM’s and Templates view to load?!?!?  I know that I dreaded the loading times.  Currently, my vSphere lab consists of the following machines…for now.

- 2 – Domain Controllers (I’ve learned my lesson and the consequences of only having one DC…)
- 1 – vCenter Server Appliance
- 1 – vSphere Data Protection Appliance
- 1 – Windows 10 Management Jumpbox
- 1 – IP Address Management Server (phpIPAM)
- 1 – Mail Server (hMailServer)
- 1 – WSUS Server
- 1 – SCCM Server ( I am currently teaching this to myself and may eventually leverage SUP, thus replacing/repurposing my current WSUS server)
- 1 – vRealize Configuration Manager (vCM) Server ( I am also teaching this to myself as to become more familiar with the product and its capabilities)
- 1 – OpenVPN Appliance

![](/uploads/2017/02/2017-02-12_13-06-33-300x151.png) ![](/uploads/2017/02/2017-02-12_13-07-02-300x151.png)

So now that my Home Lab has been upgraded and completely rebuilt, I look forward to spending more time tinkering with it and putting it to good use for exam studies and personal knowledge.  I am dedicating my Sundays as “Home Lab Fun-days”!  Thanks for stopping by and I hope you enjoyed the read! Please comment below and subscribe!
