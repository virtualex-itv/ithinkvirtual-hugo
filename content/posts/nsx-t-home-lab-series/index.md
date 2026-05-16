{
  "title": "NSX-T Home Lab Series",
  "date": "2019-01-21T22:09:16",
  "lastmod": "2019-02-19T17:26:23",
  "slug": "nsx-t-home-lab-series",
  "url": "/posts/nsx-t-home-lab-series/",
  "draft": false,
  "description": "",
  "wordpress_id": 1367,
  "wordpress_url": "https://ithinkvirtual.com/2019/01/21/nsx-t-home-lab-series/",
  "featured_image": "/uploads/2019/01/2019-01-20_23-00-06.png",
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
    "vSphere"
  ],
  "years": [
    "2019"
  ],
  "aliases": [
    "/2019/01/21/nsx-t-home-lab-series/"
  ],
  "comments": []
}

## Intro

I recently upgraded my Home Lab "Datacenter" to support all-flash VSAN and 10Gb networking with the plan to deploy [NSX-T](https://www.vmware.com/products/nsx.html) so that I can familiarize myself with the solution and use it to better prepare me for the VMware [VCP-NV](https://www.vmware.com/education-services/certification/vcp-nv-2019.html) exam certification.  Since this is all brand new to me, I've decided that I'll first deploy it in a nested lab environment in order to learn the deployment process as well as to minimize the risk of accidentally messing up my Home Lab environment.

Now, I know there are a few blogs out in the wild already that go over the installation and setup of NSX-T, but I wanted to write my own as it will better help me retain the information that I am learning.  Additionally, others may have a different setup than I have and/or may have deployed the solution differently that the way I intend to do which is by following the published documentation.  I'd like to take this time to first shout out some of my colleagues, [William Lam](https://twitter.com/lamw), [Keith Lee](https://twitter.com/keithrichardlee), [Cormac Hogan](https://twitter.com/cormacjhogan), and [Sam McGeown](https://twitter.com/sammcgeown), as their own blogs are what inspired me to deploy the solution for myself and document the process.

This post will serve as the main page where I'll post the hyperlinks to each post in the series.  I'll be deploying a virtual router/firewall, 3x ESXi VMs, and a witness appliance so that I can configure a virtual 2-node VSAN compute cluster.  I'll be managing the environment via a vCenter Server Appliance or VCSA, and a Windows Server 2019 Core OS Domain Controller or DC.  I won't cover the installation and configuration of the DC as it's out of scope for this series, nor will I go over the deployment of the VCSA or VSAN configuration as this can be done by following the [documentation](https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.vcenter.install.doc/GUID-8DC3866D-5087-40A2-8067-1361A2AF95BD.html).  And, since this is just a small nested lab, the remaining host that isn't a part of the VSAN cluster will serve as a single-node Management cluster host where the DC, VCSA, and NSX-T Appliances will reside.

I will cover the router setup, ESXi VM configuration, and NSX-T deployment.  For my setup, I am going to leverage a [Sophos XG firewall Home Edition](https://www.sophos.com/en-us/products/free-tools/sophos-xg-firewall-home-edition.aspx) since I've always had an interest in learning more about these firewalls, but also because I typically see [pfSense](https://www.pfsense.org/) being used for virtual routers and I wanted to try something different.  If you are using this as a guide for your own deployment, feel free to use your router/firewall of choice as there are plenty out there like [FreeSCO](http://www.freesco.org/), [Quagga](https://www.quagga.net/), or [VyOS](https://vyos.io/), just to name a few.  So, with that said, I hope you all enjoy the content in this series!

**NSX-T Home Lab Series**

- [NSX-T Home Lab - Part 1: Configuring Sophos XG firewall](https://wp.me/p7k0Z6-m4)
- [NSX-T Home Lab - Part 2: Configuring ESXi VMs](https://wp.me/p7k0Z6-mV)
- [NSX-T Home Lab - Part 3: Deploying NSX-T Appliances](/2019/02/12/nsx-t-home-lab-part-3-deploying-nsx-t-appliances/)
- [NSX-T Home Lab - Part 4: Configuring NSX-T Fabric](/2019/02/15/nsx-t-home-lab-part-4-configuring-nsx-t-fabric/)
- [NSX-T Home Lab - Part 5: Configuring NSX-T Networking](/2019/02/19/nsx-t-home-lab-part-5-configuring-nsx-t-networking/)
- NSX-T Home Lab - Part 6: Upgrading NSX-T
- NSX-T Home Lab - Part 7: Uninstalling NSX-T

**References:**

- [Keith Lee](http://keithlee.ie/2018/10/30/pks-nsx-t-homelab-part-1-shopping-list/)
- [Cormac Hogan](https://cormachogan.com/2018/04/11/building-a-simple-esxi-host-overlay-network-with-nsx-t/)
- [Sam McGeown](https://www.definit.co.uk/2017/09/nsx-t-2-0-lab-build-deploying-nsx-manager/)
- [William Lam](https://www.virtuallyghetto.com/2017/10/vghetto-automated-nsx-t-2-0-lab-deployment.html)
