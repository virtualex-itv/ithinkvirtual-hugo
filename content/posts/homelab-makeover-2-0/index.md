{
  "title": "Homelab Makeover 2.0",
  "date": "2018-01-01T01:20:14",
  "lastmod": "2018-02-10T16:33:16",
  "slug": "homelab-makeover-2-0",
  "url": "/posts/homelab-makeover-2-0/",
  "draft": false,
  "description": "Hello and first off, thank so much for visiting my blog!  If you have followed any part of my “Homelab” series, you will be familiar with the components that make up my home “Datacenter”.  If not, take some time to catch up on those posts! In this post, I am quickly going to cover my lab…",
  "wordpress_id": 1057,
  "wordpress_url": "https://ithinkvirtual.com/2017/12/31/homelab-makeover-2-0/",
  "featured_image": "/uploads/2017/02/Ubiquiti-UniFi-VMware-vSphere.png",
  "categories": [
    "Home Lab"
  ],
  "tags": [
    "Cisco",
    "homelab",
    "Supermicro",
    "Synology",
    "UniFi"
  ],
  "years": [
    "2018"
  ],
  "aliases": [
    "/2017/12/31/homelab-makeover-2-0/"
  ],
  "comments": []
}

Hello and first off, thank so much for visiting my blog!  If you have followed any part of my “[Homelab](/categories/home-lab/)” series, you will be familiar with the components that make up my home “Datacenter”.  If not, take some time to catch up on those posts!

In this post, I am quickly going to cover my lab makeover as I decided to get some new equipment and redo a bunch of my networking.  So without any further hesitation, let’s get to it!

Beginning with my networking equipment, I wanted to move my Cisco SG300-10 out of my home network enclosure cabinet and into my Navepoint rack enclosure.  But then I realized I would have to replace that switch with another to feed the rest of my homes connections.  Currently, I am using Ubiquiti’s UniFi equipment for my home networking and since I’m already running Ubiquiti gear, I figured I would purchase a few more of their 8-port switches to do the job so that I can manage those devices from a “single-pane-of-glass” via the controller.  So I went ahead and purchased 2 US-8 switches, in which 1 will feed the home networking and the other will extend to the lab primarily serving as a trunk for my VLANs to reach the labs Cisco switches.

So now, my UniFi network consists of:

- 1 x [USG-3](http://amzn.to/2H2ievo)
- 1 x [UC-CK](http://amzn.to/2EQUl9r)
- 1 x [US-8-60W](http://amzn.to/2Ekqfhu)
- 2 x [US-8](http://amzn.to/2EkayqH)
- 1 x [UAP-AC-Pro](http://amzn.to/2H0MXch)

![](/uploads/2017/12/2017-12-31_18-51-23.png)

On to the lab network…

The US-8-LAB switch connects to my SG300-10 which I’ve configured 2-ports as a LAG “Trunk” between the switches for VLAN traffic, 2-ports as another LAG “Trunk” connection to the SG300-52 switch, and the others as “Access” ports which connect to the IPMI interfaces of my servers.  The IPMI connections were previously on my SG300-52 switch.  On to the SG300-52 switch, I have configured all of my ESXi management ports, vMotion ports, iSCSI & NFS ports, VSAN ports, and data ports for my servers, along with a few LAG connections which connect to my storage devices, and a few which connect my UPS and ATS/PDU units.  I also configured an additional LAG “Trunk” which connects to a Netgear Prosafe GS108T that I had laying around.  I’ve dedicated that switch and it’sports for my ex-gaming PC turned “DEV” ESXi host.  Eventually, that host will be decommissioned when I add a new host to my rack enclosure.

So now, my lab network consists of:

- 1 x [Cisco SG300-10](http://amzn.to/2BQDwwC)
- 1 x [Cisco SG300-52](http://amzn.to/2Cc0E4p)
- 1 X [Netgear GS108Tv2](http://amzn.to/2H0MfvD) PROSafe 8-port Managed switch

Now for the storage devices.  Previously, I was running my lab VMs using a Synology DS415+ storage unit via NFS mounts.  This was all fine and dandy, except for the fact that it would randomly shut itself down for no apparent reason, leading to eventual corruption of my VMs.  I got tired of spending hours trying to recover my machines and eventually discovered that my device was plagued by the Intel ATOM C2000 CPU issue described [here](https://www.anandtech.com/show/11110/semi-critical-intel-atom-c2000-flaw-discovered).  I then reached out to Synology and they quickly responded and issued an immediate RMA of the device.  Again this was fine, but where was I going to move my VMs and data too?  I didn’t have another storage device with an ample amount of free space to accommodate all my data, so I decided to bite the bullet and pick up a brand new Synology RS815+ which I could now mount in my rack enclosure.  I also scooped up some 1TB SSDs from their compatibility matrix to populate the drive bays.  The difference here is that with the new RackStation, I opted to configure my LUNs via iSCSI instead of NFS like I had previously done with the DiskStation.  Once set up and connected, I vMotion’d all of my machines to the new device, and disconnected the DS415+ while I waited for the replacement device to arrive.  That replacement unit eventually came, so I swapped my SSD’s from the old unit into the new unit and fired it back up.  I will eventually recreate some NFS mounts and reconnect them to the vSphere environment.

Now, my lab storage consists of:

- 1 x [Synology RackStation RS815+](http://amzn.to/2Ejg3WV)
- 1 x [Synology DiskStation DS415+](http://amzn.to/2G3fbSF)
- 1 x [Synology DiskStation Expansion DX513](http://amzn.to/2G2IUuL)

Finally, the cabinet.  I became rather displeased with the amount of space I had with my Navepoint 9U 450mm enclosure.  The case itself was great, but I just needed some more room in the event I needed to un-rack a server or do anything else in there.  Also, I started to do some “forward-thinking” about eventual future expansion, and the current 9U enclosure was no longer going to suffice.  I decided to upgrade to a new Navepoint 18U 600mm enclosure, and now I have plenty of room for all of my equipment and future expansion.  After relocating my servers to the new rack enclosure, I now have the following equipment mounted in the rack and, still, have room for growth.

- 2 x Cat6 keystone patch panels
- 2 x Cisco SG300 switches
- 4 x Supermicro servers
- 1 x Synology storage unit
- 1 x UPS
- 1 x ATS/PDU
- 1 x CyberPower Surge power strip (in the event I need to plug-in some other stuff)

![](/uploads/2017/12/image-732x1024.jpg)

Thanks for stopping by!  Please do leave some comments as feedback is always appreciated!  Until next time!

-virtualex-

## Pingbacks

- [Home Lab 2017 – Part 1 (Network and Lab Overhaul)](/posts/home-lab-2017-part-1-network-and-lab-overhaul/)
- [Home Lab 2016 – Part 3](/posts/home-lab-2016-part-3/)
