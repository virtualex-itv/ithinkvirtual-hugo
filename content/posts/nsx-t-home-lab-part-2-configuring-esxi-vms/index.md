{
  "title": "NSX-T Home Lab - Part 2: Configuring ESXi VMs",
  "date": "2019-01-21T22:11:56",
  "lastmod": "2019-02-18T20:19:59",
  "slug": "nsx-t-home-lab-part-2-configuring-esxi-vms",
  "url": "/posts/nsx-t-home-lab-part-2-configuring-esxi-vms/",
  "draft": false,
  "description": "",
  "wordpress_id": 1421,
  "wordpress_url": "https://ithinkvirtual.com/2019/01/21/nsx-t-home-lab-part-2-configuring-esxi-vms/",
  "featured_image": "/uploads/2019/01/2019-01-21_01-15-38.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "NSX-T",
    "vExpert",
    "VMware",
    "vSAN",
    "vSphere"
  ],
  "years": [
    "2019"
  ],
  "aliases": [
    "/2019/01/21/nsx-t-home-lab-part-2-configuring-esxi-vms/"
  ],
  "comments": []
}

## Intro

Welcome to Part 2 of my NSX-T Home Lab Series.  In my [previous post](/2019/01/21/nsx-t-home-lab-part-1-configuring-sophos-xg-firewall/), I went over the installation and configuration of a Sophos XG firewall for my nested [NSX-T](https://www.vmware.com/products/nsx.html) Home Lab.  In this post, I will cover the setup and configuration of the ESXi 6.7 VMs.

I recently wrote a post on how to [Create an ESXi 6.7 VM Template](https://wp.me/p7k0Z6-mt), which is what I used to deploy my VMs from.  After cloning to new VMs, I changed the disk sizes for my cache and capacity disks, increased the CPUs and RAM, and added 2 additional network adapter to give me a total of 4 adapters.  The reason I did this is so that I can keep my management and other vmkernel ports on their VDS and have two new ones to use for NSX-T.  I may do a follow-up post using only two adapters where I'll migrate my vmkernel networks over to NSX-T as in the real world, I'm sure there are many customers using dual 10Gb cards in their servers.

Now, I will not be covering how to actually install ESXi as you can follow the [documentation](https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.esxi.install.doc/GUID-B2F01BF5-078A-4C7E-B505-5DFFED0B8C38.html) for that, or you can reference my post mentioned above.  There really isn't much to that installation...it's pretty trivial.  Instead, I am just going to quickly state the specs used for my ESXi VMs from a resource perspective, and give some additional pointers.

**Single-Node Management Cluster VM**

- CPUs: 8
- RAM: 32GB
- Disk1: Increased to 500GB (This will serve as a local VMFS6 datastore)
- Disk2: Removed (As I will not be running VSAN)
- Network Adapters: 2 (connected to the Nested VDS port group we created earlier)

On this host, I deployed a Windows Server 2019 Core OS to serve as my domain controller for the nested lab.  I also deployed a VCSA to manage the environment.

**2-Node VSAN Compute Cluster (with a Witness Appliance)**

- CPUs: 8 on each host
- RAM: 16GB on each host
- Network Adapters: 4 on each host (connected to the Nested VDS port group we created earlier)

I used the new Quick Start feature to create and configure my VSAN cluster along with all the networking required, and this has now become one of my favorite new features in vSphere 6.7.  There were some nuances I had to fix which were super simple.  During the creation of the VDS and process of migrating vmkernel ports to the VDS, my nested ESXi VMs would lose connectivity.  Simply restarting the management network from the console proved to fix the issue and I was able to proceed.

![](/uploads/2019/01/2019-01-21_16-52-29-1024x823.png)

I then used VUM to update each host to the latest version (**Build 11675023**) that was released on **1/17/19**.  Once everything was configured, I had a nice little, nested playground ready for NSX-T!

![](/uploads/2019/01/2019-01-21_16-53-28.png)
![](/uploads/2019/01/2019-01-21_16-58-03-1024x559.png)

In the next post, I will go over the deployment of the NSX-T appliances in the nested lab.  Be sure to come back!

-virtualex-
