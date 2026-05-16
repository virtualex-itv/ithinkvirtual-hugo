{
  "title": "Home Lab 2016 – Part 2",
  "date": "2016-03-15T23:36:15",
  "lastmod": "2018-02-10T16:19:48",
  "slug": "homelab-pt2",
  "url": "/posts/homelab-pt2/",
  "draft": false,
  "description": "Home Lab 2016 – Part 2 Welcome back for Part 2 of my Home Lab 2016 Series.  I hope that you enjoyed my previous post, Part 1 from last week, where I covered the basis of my home lab and presented the Bill of Materials (BOM) for my mini-datacenter environment. Today I am bringing you Part…",
  "wordpress_id": 185,
  "wordpress_url": "https://ithinkvirtual.com/2016/03/15/homelab-pt2/",
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
    "/2016/03/15/homelab-pt2/"
  ],
  "comments": [
    {
      "author": "Alex",
      "date": "2016-04-07T17:37:00",
      "content": "<p>Thanks much @superjoepez:disqus!  Please be sure to subscribe and share!</p>\n"
    },
    {
      "author": "Superjoepez",
      "date": "2016-04-07T12:29:00",
      "content": "<p>Keep up the good work, I was just turned onto your blog and absolutely love it. I have been trying to find something like this for a long time. I cant wait to see more on the home lab!</p>\n"
    }
  ]
}

**Home Lab 2016 – Part 2**

Welcome back for Part 2 of my Home Lab 2016 Series.  I hope that you enjoyed my previous post, [Part 1](/posts/homelab-pt1/) from last week, where I covered the basis of my home lab and presented the Bill of Materials (BOM) for my mini-datacenter environment.

Today I am bringing you Part 2 and will cover the actual physical build process, putting together the components to build each ESXi host server.  I hope you’re as excited as I am!

Beginning with the case, I chose to go with the Supermicro [CSE-504-203B](https://www.supermicro.com/products/chassis/1u/504/sc504-203.cfm) which has the motherboard backplane and all connections at the rear of the case, instead of the [CSE-505-203B](https://www.supermicro.com/products/chassis/1u/505/sc505-203.cfm) which has everything in the front of the case.  I wanted to have more of a cleaner look to my rack enclosure, and the best thing about these cases is that they come with a 200W High-efficiency “80 Gold Level Certified” power supply!

![2_1_FullSizeRender2](/uploads/2016/03/2_1_FullSizeRender2-300x97.jpg) ![FullSizeRender](/uploads/2016/03/FullSizeRender-300x91.jpg)

The next component to go into this case is the motherboard.  I chose the Supermicro [A1SAi-2750](https://www.supermicro.com/products/motherboard/ATOM/X10/A1SAi-2750F.cfm) with an Intel ATOM “System on a Chip” (SoC) CPU.  This is a 20W, 8-Core processor, is compatible with “Westmere” VMware Enhanced vMotion Compatibility mode, and supports a maximum of 64GB DDR3  RAM in (4) DIMM sockets!  I went ahead and maxed the RAM on each board with (4) 16GB Micron [MEM-DR316L-CL02-ES16](https://www.supermicro.com/support/resources/memory/display.cfm?sz=16.0&mspd=1.6&mtyp=65&id=7E096BDEAE63A2AC69D703E672D8BE05&prid=83743&type=DDR3%201.35V%20SODIMM&ecc=1&reg=0&fbd=0) DDR3 1600MHz ECC 204-pin 1.35V SO-DIMM chips.

![IMG_1667](/uploads/2016/03/IMG_1667-300x178.jpg) ![IMG_1670](/uploads/2016/03/IMG_1670-300x147.jpg)

Since I wanted to have redundancy for all my network connections, as per “best practices”, I decided to install an [Intel I350-T4](https://ark.intel.com/products/59063/Intel-Ethernet-Server-Adapter-I350-T4) quad-port NIC.  Unfortunately, even with the low-profile mounting brackets that come with the cards, they simply would not fit in a small 1U case, as they are designed to be installed horizontally.  I picked up a couple of Supermicro [RSC-RR1u-E8](https://www.supermicro.com/ResourceApps/Riser.aspx) PCI-E x8 riser cards which would allow me to insert the NICs properly.

[![](/uploads/2016/03/IMG_1675-225x300.jpg)](/uploads/2016/03/IMG_1675-e1458083961467.jpg) [![](/uploads/2016/03/IMG_1674-225x300.jpg)](/uploads/2016/03/IMG_1674-e1458083987470.jpg)

Next, came the disk drives to run ESXi as well as VM’s, in a VSAN cluster, for management machines if I wanted to move them off of my shared storage device.  I also wanted to have the ability to create a VSAN environment for testing and educational purposes (i.e.: VCP/VCAP certifications).  I decided to utilize the onboard USB 3.0 socket and installed a [SanDisk Ultra Fit 16GB USB 3.0](https://www.sandisk.com/home/usb-flash/ultra-fit-usb) flash drive to run ESXi, after all…this is a lab right?  For my VSAN drives, I decided to pair a [Kingston SSDNow V300 series 120GB SATA III SSD](https://www.kingston.com/us/ssd/v#sv300s3) with an [HGST Travelstar Z7K500 500GB 7200RPM HDD](https://www.hgst.com/products/hard-drives/travelstar-z7k500).

[![](/uploads/2016/03/IMG_1668-205x300.jpg)](/uploads/2016/03/IMG_1668-e1458084228659.jpg) [![](/uploads/2016/03/IMG_1671-230x300.jpg)](/uploads/2016/03/IMG_1671-e1458084216176.jpg) [![](/uploads/2016/03/IMG_1672-225x300.jpg)](/uploads/2016/03/IMG_1672-e1458084016838.jpg)

In order to stack them together, I picked up a Supermicro [MCP-220-00044-0N HDD Converter bracket](https://www.supermicro.com/products/accessories/index.cfm?Type=22).

[![](/uploads/2016/03/IMG_1673-300x264.jpg)](/uploads/2016/03/IMG_1673-e1458084000881.jpg)

Here is the end result of the insides after all the components above were installed.

[![](/uploads/2016/03/FullSizeRender-3-188x300.jpg)](/uploads/2016/03/FullSizeRender-3-e1458084242745.jpg)

Once I had the first server built, I powered it on to ensure it was in working order before continuing on and building the remaining (3) hosts.  Afterwards, I decided to tidy things up a bit further, zip-tying cables, etc. for a cleaner look, before closing up the cases to place them in my rack enclosure.

Please stay tuned for Part 3, where I will quickly cover my networking and storage solutions!  Thanks for stopping by!
