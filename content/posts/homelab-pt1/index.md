{
  "title": "Home Lab 2016 – Part 1",
  "date": "2016-03-05T00:18:50",
  "lastmod": "2018-02-10T16:17:43",
  "slug": "homelab-pt1",
  "url": "/posts/homelab-pt1/",
  "draft": false,
  "description": "Home Lab 2016 – Part 1     Having a home lab is every IT enthusiasts dream come true, and now I can finally say that I have fulfilled that dream!  I previously was (and currently still am…) using a 1-node “white box” system I had built from a spare gaming machine I had laying…",
  "wordpress_id": 100,
  "wordpress_url": "https://ithinkvirtual.com/2016/03/04/homelab-pt1/",
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
    "/2016/03/04/homelab-pt1/"
  ],
  "comments": [
    {
      "author": "virtualex",
      "date": "2016-03-06T19:19:45",
      "content": "<p>Thx much Paul!!</p>\n"
    },
    {
      "author": "paulbraren",
      "date": "2016-03-06T19:17:44",
      "content": "<p>Damn that&#8217;s beautiful Alex, so organized too, way to go!</p>\n"
    },
    {
      "author": "virtualex",
      "date": "2016-03-05T17:47:07",
      "content": "<p>Supermicro 16GB DDR3 PC3-14900 (1866MHz)204p SODIMM x 4 per node = 64GB per node</p>\n"
    },
    {
      "author": "Mike",
      "date": "2016-03-05T17:39:36",
      "content": "<p>What type and how much RAM per node?</p>\n"
    }
  ]
}

Home Lab 2016 – Part 1

Having a home lab is every IT enthusiasts dream come true, and now I can finally say that I have fulfilled that dream!  I previously was (and currently still am…) using a 1-node “white box” system I had built from a spare gaming machine I had laying around, running on an open-air tech bench from [TopDeck](http://www.highspeedpc.com/).  It’s comprised of the following:

- 1 x [ASUS Maximus Gene V](http://amzn.to/2nPReaq) motherboard w/ Intel 82579 LOM NIC
- 1 x [Intel Core i5-3570K](http://amzn.to/2EgDSOL)
- 1 x ADATA SP600 32GB SSD
- 1 x [Samsung Evo 840 1TB](http://amzn.to/2EVljgf) SSD
- 1 x Seagate 1TB HDD
- 1 x Intel 82574 (single-port) NIC
- 1 x Intel 82576 (dual-port) NIC
- 1 x Corsair HX650 PSU

And even though it runs great, I simply felt it wasn’t enough as I basically wanted to replicate a mini-datacenter for my lab which would help tremendously with my VMware studies and overall VMware knowledge.

So I quickly got to work and embarked on the adventure of creating my new lab.  I started off by opening a [Feedly](https://feedly.com/i/welcome) account and subscribing to numerous other user and community blogs, reading what others did to create and build/setup their homelabs, and also checked out some youtube channels.

Lot’s of good reads out there…

[TinkerTry](https://tinkertry.com/)

[Wahl Network](http://wahlnetwork.com/)

[VMware Front Experience](http://www.v-front.de/)

[VirtualJad](http://www.virtualjad.com/)

[virtuallyGhetto](http://www.virtuallyghetto.com/)

Just to name a few…

I also spent the last year+ researching, planning, designing, and purchasing the equipment for my new lab.  And since I wanted somewhat of a low power solution (as to not incur outrageous electric bill charges) I settled on SuperMicro’s A1SAi-2750 ATOM SOC (System-on-a-chip) Mini-ITX motherboards.  Boy, do these things boast a boatload of features (not getting into specifics as you guys know how to use Google I’m sure…)!  Since I also wanted to have them in a rack to replicate a mini-datacenter, I went with a Navepoint 9U rack enclosure.  I bought some Sandisk USB’s, some SSD’s & HDD’s (for eventual VSAN setup), and extra NIC’s (for redundancy and best practices), 1U cases, and some Synology NAS devices.  Here’s my entire part’s list…

- 1 x [Navepoint 9U Rack Enclosure](http://amzn.to/2Eg4RtU)
- 1 x [ICC 48-port feed-thru Cat6 Patch Panel](http://amzn.to/2smwEn0) – 1U
- 1 x [Cyberpower PR1000LCDRT2U UPS](http://amzn.to/2socA3A)
- 1 x [Cyberpower PDU15SW10ATNET ATS/PDU](http://amzn.to/2CaWXft)
- 4 x [SuperMicro A1SAi-2750](http://amzn.to/2BkLCNa)
- 4 X [SuperMicro 504-203B 1U rackmount cases](http://amzn.to/2G3bkVo) (contains a 200W PSU in each case)
- 4 x [Sandisk UltraFit 16GB USB 3.0](http://amzn.to/2EjcjVn)
- 4 x [Kingston 120GB SSD](http://amzn.to/2EhCStT)
- 4 x [HGST 500GB 7200RPM 2.5” HDD](http://amzn.to/2EipvcK)
- 4 x [SuperMicro 1×3.5” to 2×2.5” Converter Brackets](http://amzn.to/2EhtoyX)
- 4 x [SuperMicro PCI-E x8 L-shape riser cards](http://amzn.to/2EfKTiQ)
- 4 x [Intel I350-T4 (quad-port) NIC](http://amzn.to/2EzOkjV)
- 16 x [16GB Micron 1600MHz DDR3 204-pin SO-DIMM RAM](http://amzn.to/2ExpJvS)

And for NAS storage…..

- 1 x [Synology DS415+](http://amzn.to/2H3lnv9)
- 1 x Synology DX213 Expansion Unit
- 2 x [Micron M500DC 800GB SSD](http://amzn.to/2Ewh3pH)
- 2 x [Micron M500 480GB SSD](http://amzn.to/2H5xCak)
- 4 x [Sabrent 2.5” to 3.5” Bay Converter](http://amzn.to/2EuRh5g)
- 2 x [HGST 6TB 7200RPM 3.5” HDD](http://amzn.to/2BS4fZV)

The Networking components…

- 1 x [Ubiquiti EdgeRouter ERLite-3](http://amzn.to/2H6AUu3)
- 1 x [ASUS RT-AC68U wifi router](http://amzn.to/2EgjA89)
- 1 x [Cisco SG300-10 SMB L2/L3 switch](http://amzn.to/2Ey0Xfq)
- 1 x [Cisco SG300-52 SMB L2/L3 switch](http://amzn.to/2EiWaiD)

And last, but definitely not least…. a slew of Monoprice Cat6 24AWG Flexboot cables (various lengths)

Phew!…what a list!  Wait!…am I missing anything??

The end result…my new mini-datacenter homelab 2016!! (with previous Dev “white box” system to the side)

![](/uploads/2016/03/img_1719.jpg)

Stay tuned for Part 2 ( I hope) where I plan on “Putting it all together”!

Feel free to comment and let me know your thoughts/feedback…and words of encouragement so I can continue on this new blogging adventure!
