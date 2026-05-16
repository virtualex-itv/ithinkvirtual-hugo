{
  "title": "Home Lab 2016 – Part 3",
  "date": "2016-04-23T22:11:29",
  "lastmod": "2018-02-10T16:21:21",
  "slug": "home-lab-2016-part-3",
  "url": "/posts/home-lab-2016-part-3/",
  "draft": false,
  "description": "Home Lab 2016 – Part 3   Hello all!  My sincere apologies for the brief hiatus, but I am back to continue my Home Lab 2016 series.  In my previous posts, I covered the components that make up my new Home Lab.  In this post I will quickly cover my Storage and Network solutions that…",
  "wordpress_id": 301,
  "wordpress_url": "https://ithinkvirtual.com/2016/04/23/home-lab-2016-part-3/",
  "featured_image": "/uploads/2016/03/imgres12.jpg",
  "categories": [
    "Home Lab"
  ],
  "tags": [
    "homelab"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/04/23/home-lab-2016-part-3/"
  ],
  "comments": []
}

**Home Lab 2016 – Part 3**

Hello all!  My sincere apologies for the brief hiatus, but I am back to continue my Home Lab 2016 series.  In my previous posts, I covered the components that make up my new Home Lab.  In this post I will quickly cover my Storage and Network solutions that connect my lab.  Let’s get to it!

I will begin by covering my networking components used in my home LAN and LAB.

- ISP Modem
- [Ubiquiti EdgeRouter Lite](https://www.ubnt.com/edgemax/edgerouter-lite/) – ERLite-3
- [ASUS RT-AC68U Router](https://www.asus.com/us/Networking/RTAC68U/) – AC68U
- [Cisco SG300-10 SMB Managed Switch](https://www.cisco.com/c/en/us/support/switches/sg300-10-10-port-gigabit-managed-switch/model.html) – Core1
- [Cisco SG300-52 SMB Managed Switch](https://www.cisco.com/c/en/us/support/switches/sg300-52-52-port-gigabit-managed-switch/model.html) – Core2

My WAN connects to my ISP modem, which then connects to my amazing Ubiquiti EdgeRouter Lite (ERLite-3) via **eth0**.  My hardwired LAN connects from **eth1** on the ERLite-3 to port 1 on the SG300-10 (core1).   Lastly, I changed my ASUS router to Access Point mode and connected my Wifi LAN from port 1 of the ASUS to **eth2** on my ERLite-3.

![2016-04-23_17-34-38](/uploads/2016/04/2016-04-23_17-34-38-300x206.png)

EdgeRouter Connections:

- eth0 – WAN
- eth1 – LAN (configured as a 192.x.x.x network)
- eth2 – WLAN (configured as a 172.x.x.x network)

![2016-04-23_17-57-47](/uploads/2016/04/2016-04-23_17-57-47-300x150.png)![2016-04-23_17-59-46](/uploads/2016/04/2016-04-23_17-59-46-300x150.png)

On to the Cisco SG300-10 (core1), 10-port managed switch, this is configured in Layer 3 (L3) mode and is where I created all of my VLANs and DHCP scopes, etc….

![2016-04-23_17-19-20](/uploads/2016/04/2016-04-23_17-19-20-300x54.png)

- port 1 – connects to ERLite-3
- ports 2-5 configured in an LACP/EtherChannel trunk to Cisco SG300-52 (core 2)
- ports 6-10 connect to different rooms in my home LAN

I created the following VLANs on core 1 and allowed them to traverse the trunk to core 2.

- VLAN10 – IPMI
- VLAN20 – ESXi Management
- VLAN30 – vMotion
- VLAN40 – VM Traffic
- VLAN50 – NFS Traffic
- VLAN55 – VSAN Traffic
- VLAN60 – DEV-VM Traffic
- VLAN65 – DEMO-VM Traffic
- VLAN99 – UPS/ATS/DPU

The Cisco SG300-52 is configured in its default Layer 2 (L2) mode and I set up the proper settings, trunk ports, and access ports for each VLAN.  I understand that I could’ve also configured this in L3-mode and reduce the extra hop to core 1, but I didn’t feel the need to do so for my use case. I may change my mind at some point, but it works for me…for now.

Due to the way the ethernet cables connected from the switch to each ESXi host, I started configuring the switch ports at the end of the switch and worked my way towards to the beginning of the switch ports.

![2016-04-23_16-42-35](/uploads/2016/04/2016-04-23_16-42-35-300x35.png)

- ports 49-52 (LAG 8): LACP/EtherChannel trunk from SG300-10 (core 1)
- ports 23-24, 47-48: IMPI
- ports 1, 19-22, 43-47: ESXi Management Traffic
- ports 15-18, 25, 39-42: vMotion Traffic
- ports 11-14, 26: NFS Traffic
- ports 26, 35-38: VSAN/iSCSI Traffic
- ports 2, 7-10, 31-34: VM Traffic
- ports 6, 30 (LAG 7): Synology
- ports 5, 29: UPS/ATS/DPU
- ports 3-4, 27-28: Unassigned

![Switch_Connections_clean](/uploads/2016/04/Switch_Connections_clean-300x231.png)

Next, let’s take a look at Shared Storage.  I run my shared storage infrastructure on Synology DiskStation hardware, because…they’re flat out awesome, and give you a ton of bang for your buck!

- [Synology DS415+](https://www.synology.com/en-us/products/DS415+)
- [Synology DX213](https://www.synology.com/en-us/products/DX213)
- 2 x 800GB [Micron 500DC](https://www.micron.com/products/solid-state-storage/product-lines/m500dc#/) SSD’s
- 2x 480GB [Micron 510DC](https://www.micron.com/products/solid-state-storage/product-lines/m510dc#/) SSD’s
- 2 x 6TB [HGST Deskstar](https://www.hgst.com/products/hard-drives/nas-desktop-drive-kit) HDD’s

I have to say I absolutely love the Synology products, and my DS415+ rocks!  I have this running 4 SSD’s and a DX213 expansion unit attached with 2 HDD’s in it.  It runs DSM 6.0-*update*. The interface is slick and setting up the device is a breeze.  I am currently using NFS only in my lab, and plan to incorporate VSAN soon, as well as testing out iSCSI vs NFS performance.  For my disk setup, I decided to use the Micron 500DC SSD drives as my first Disk Group (Disk Group 1) for my performance volume (Volume 1), the Micron 510DC drives for SSD Cache, and the HGST drives as my 2nd Disk Group (Disk Group 2) for all other storage volumes (Volume 2-x; ISOs, Backups, etc.)

![2016-04-23_17-26-53](/uploads/2016/04/2016-04-23_17-26-53-300x150.png)![2016-04-23_17-31-30](/uploads/2016/04/2016-04-23_17-31-30-300x152.png)

Well, there you have it.  In my next posts, I will go over the basic setup and configurations of my Home Lab.

I hope you enjoyed the read!

Don’t forget to comment and subscribe!
