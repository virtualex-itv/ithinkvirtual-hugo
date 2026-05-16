{
  "title": "Nested vSphere Home Lab Series",
  "date": "2023-03-24T20:37:53",
  "lastmod": "2025-01-08T19:28:35",
  "slug": "nested-vsphere-home-lab-series",
  "url": "/posts/nested-vsphere-home-lab-series/",
  "draft": false,
  "description": "",
  "wordpress_id": 1783,
  "wordpress_url": "https://ithinkvirtual.com/2023/03/24/nested-vsphere-home-lab-series/",
  "featured_image": "/uploads/2023/03/vSphere-8-1850999778.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "NSX-T",
    "VMware",
    "VMware Aria",
    "VMware Fusion",
    "VMware Workstation",
    "vRealize Suite",
    "vSAN",
    "vSphere"
  ],
  "years": [
    "2023"
  ],
  "aliases": [
    "/2023/03/24/nested-vsphere-home-lab-series/"
  ],
  "comments": []
}

## Intro

Hey there!  I'd taken a hiatus from writing as my personal life got in the way...got married, had a child, and changed employer(s), just to name a few!

But now I am back, I've rejoined VMware now as a Technical Account Manager, and I am looking forward to publishing some new content for the vCommunity and fellow TAMs!

In this series, I will cover how to deploy a fully nested vSphere home lab running on top of [vSphere 8.0/ESXi 8.0](https://core.vmware.com/vmware-vsphere-8) running on a Dell PowerEdge R720, but the same can be done leveraging [VMware Workstation Pro](https://www.vmware.com/content/vmware/vmware-published-sites/us/products/workstation-pro.html.html) or [VMware Fusion Pro](https://www.vmware.com/products/fusion.html)!

<aside class="info-block"><p>Nested Virtualization is not supported by VMware.</p></aside>

Due to some unfortunate circumstances, my previous lab environment was lost and required a rebuild that, at the time, I hadn't the time for.  Fast-forward about 1-year later, life settled back down, and I finally had the time to start rebuilding my *physical* home lab.  I was fortunate to have acquired quite a bit of lab gear over the years, most no longer supported by VMware, but still manage to work with later versions of vSphere and this is the perfect use case for a lab environment!

Now that my physical lab is up and running, I wanted to document the way I typically set up my lab environment but in a nested fashion that I can destroy and rebuild to test VMware products and solutions, without worrying about doing something possibly detrimental to my real lab.

The environment will consist of a virtual router appliance, a domain controller (which will also serve as my jump box for the lab), a [VMware vCenter Server](https://www.vmware.com/products/vcenter.html) Appliance, and several [VMware ESXi](https://www.vmware.com/products/esxi-and-esx.html) hypervisor virtual machines which will be configured to serve up a [vSAN](https://www.vmware.com/products/vsan.html) datastore for each respective cluster.

I will cover how to deploy [NSX](https://www.vmware.com/products/nsx.html), [NSX Advanced Load Balancer](https://www.vmware.com/products/nsx-advanced-load-balancer.html), [vSphere with Tanzu](https://www.vmware.com/products/vsphere/vsphere-with-tanzu.html)/[Tanzu Kubernetes Grid (TKG)](https://tanzu.vmware.com/kubernetes-grid), and the [VMware Aria Suite](https://www.vmware.com/products/aria.html) of products.  I also have plans for a nested [VMware Cloud Foundation](https://www.vmware.com/products/cloud-foundation.html) series after this one so stay tuned!

This is basically a follow-up and updated replacement series to my previously abandoned [NSX-T Home Lab Series](/2019/01/21/nsx-t-home-lab-series/) and I may reference certain posts from that series throughout this one...so grab some coffee and enjoy the series!

--virtualex

##### Home Lab Series (subject to change...)

- - [Nested vSphere Home Lab - Part 1 - Sophos Firewall](/2023/04/23/nested-vsphere-home-lab-part-1-sophos-firewall/)
  - [Nested vSphere Home Lab - Part 2 - Active Directory & Certificate Authority](/2023/04/23/nested-vsphere-home-lab-part-2-active-directory-certificate-authority/)
  - [Nested vSphere Home Lab - Part 3 - vSphere 8.x Lab Deployment](/2024/01/06/nested-vsphere-home-lab-part-3-vsphere-8-x-lab-deployment/)
  - Nested vSphere Home Lab - Part 4 - VMware Aria Suite Lifecycle Manager Deployment
  - Nested vSphere Home Lab - Part 4.1 - VMware Identity Manger Deployment
  - Nested vSphere Home Lab - Part 4.2 - VMware Aria Operations Deployment
  - Nested vSphere Home Lab - Part 4.3 - VMware Aria Operations for Logs Deployment
  - Nested vSphere Home Lab - Part 4.4 - VMware Aria Operations for Networks Deployment
  - Nested vSphere Home Lab - Part 4.5 - VMware Aria Automation Deployment
  - Nested vSphere Home Lab - Part 4.6 - VMware Aria Automation Config Deployment
  - Nested vSphere Home Lab - Part 5 - NSX 4.x Lab Deployment
  - Nested vSphere Home Lab - Part 5.1 - NSX 4.x Fabric Configuration
  - Nested vSphere Home Lab - Part 5.2 - NSX 4.x Network Configuration
  - Nested vSphere Home Lab - Part 5.3 - NSX 4.x Upgrade
  - Nested vSphere Home Lab - Part 5.4 - NSX 4.x Uninstall
  - Nested vSphere Home Lab - Part 6 - NSX ALB Deployment & Configuration
  - Nested vSphere Home Lab - Part 7 - Tanzu w/ NSX Networking Deployment
  - Nested vSphere Home Lab - Part 7.1 - Tanzu w/ VDS (NSX ALB) Networking Deployment

PS: Shout out to [William Lam](https://williamlam.com/about) for his awesome work on his [nested ESXi appliances](https://williamlam.com/nested-virtualization/nested-esxi-virtual-appliance) and [lab automation script](https://github.com/lamw/vsphere-8-lab-deployment)(s).  These are what will be used to deploy the core nested lab infrastructure in this series.  Also, shout out to the [vExpert](https://vexpert.vmware.com/) program for providing us with access to VMware software licensing!

![](/uploads/2023/03/2023-03-24_14-32-16.png)
