{
  "title": "vRealize Suite 2019 Series",
  "date": "2020-01-05T04:14:28",
  "lastmod": "2020-01-17T22:04:18",
  "slug": "vrealize-suite-2019-series",
  "url": "/posts/vrealize-suite-2019-series/",
  "draft": false,
  "description": "",
  "wordpress_id": 1625,
  "wordpress_url": "https://ithinkvirtual.com/2020/01/04/vrealize-suite-2019-series/",
  "featured_image": "/uploads/2020/01/vrs19.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "vExpert",
    "VMware",
    "vRealize Suite",
    "vSphere"
  ],
  "years": [
    "2020"
  ],
  "aliases": [
    "/2020/01/04/vrealize-suite-2019-series/"
  ],
  "comments": []
}

## Intro

Hello, and thank you for visiting my blog! I'd decided to take some time away from writing in order to focus on my role as a Solutions Engineer at VMware, and enhance my skillset by getting more acclimated and accustomed to some of the most utilized solutions by VMware customers.  Almost one full year has passed since I last wrote anything, and with the new year underway, what better time to get back into writing some material for myself and the vCommunity.

In this series, I'm going to cover how to easily deploy, and eventually update, each of the solutions that make up the [vRealize Suite 2019](https://docs.vmware.com/en/vRealize-Suite/2019/rn/VMware-vRealize-Suite-2019.html) set of products. The products that will be covered are as follows:

- [vRealize Suite Lifecycle Manager 8.x](https://docs.vmware.com/en/VMware-vRealize-Suite-Lifecycle-Manager/2019/rn/VMware-vRealize-Suite-Lifecycle-Manager-80-Release-Notes.html) with VMware Identity Manager 3.3.1 (required for the new vRealize Automation 8.x release)
- [vRealize Automation 8.x](https://docs.vmware.com/en/vRealize-Automation/8.0/rn/vRealize-Automation-80-release-notes.html) with embedded [vRealize Orchestrator 8.x](https://docs.vmware.com/en/vRealize-Orchestrator/8.0/rn/VMware-vRealize-Orchestrator-80-Release-Notes.html)
- [vRealize Operations Manager 8.x](https://docs.vmware.com/en/vRealize-Operations-Manager/8.0/rn/vRealize-Operations-Manager-80.html)
- [vRealize Log Insight 8.x](https://docs.vmware.com/en/vRealize-Log-Insight/8.0/rn/vRealize-Log-Insight-80.html)
- vRealize Network Insight 5.x (Bonus)

If anyone has followed my [NSX-T Home Lab Series](/2019/01/21/nsx-t-home-lab-series/) from last year, I again will be leveraging a nested lab environment to deploy each of these solutions since I already have these solutions installed and running in my physical lab infrastructure. I did, however, rebuild this nested lab environment since that series was written and only installed Site Recovery Manager which was used to demonstrate to a customer.

For the purposes of this series, my nested lab consists of the following VMs:

- Sophos XG (serves as my virtual router)
- Synology DS918+ (NFS Storage for the nested lab)
- 4 ESXi VMs
  - 2 for Management
  - 1 for Site A
  - 1 for Site B

Once this series is finished up, I plan on revisiting my NSX-T series with a bunch of updated content since the entire deployment has changed since NSX-T 2.3.x (which is the version used in that series).

Enjoy!!

### vRealize Suite 2019 Series:

I'll continually add links in the series below as they're published.

- [vRealize Suite 2019 - Part 1: Installing vRealize Lifecycle Manager](/2020/01/04/vrealize-suite-2019-part-1-installing-vrealize-lifecycle-manager)
- [vRealize Suite 2019 - Part 2: Configuring VMware Identity Manager](/2020/01/05/vrealize-suite-2019-part-2-configuring-vmware-identity-manager/)
- [vRealize Suite 2019 - Part 3: Installing vRealize Automation](/2020/01/17/vrealize-suite-2019-part-3-installing-vrealize-automation/)
