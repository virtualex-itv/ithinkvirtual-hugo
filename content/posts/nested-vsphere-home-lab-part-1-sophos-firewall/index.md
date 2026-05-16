{
  "title": "Nested vSphere Home Lab – Part 1 – Sophos Firewall",
  "date": "2023-04-23T21:03:00",
  "lastmod": "2023-04-26T22:57:39",
  "slug": "nested-vsphere-home-lab-part-1-sophos-firewall",
  "url": "/posts/nested-vsphere-home-lab-part-1-sophos-firewall/",
  "draft": false,
  "description": "",
  "wordpress_id": 1794,
  "wordpress_url": "https://ithinkvirtual.com/2023/04/23/nested-vsphere-home-lab-part-1-sophos-firewall/",
  "featured_image": "/uploads/2023/04/2023-04-23_15-09-59.png",
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
    "vSphere"
  ],
  "years": [
    "2023"
  ],
  "aliases": [
    "/2023/04/23/nested-vsphere-home-lab-part-1-sophos-firewall/"
  ],
  "comments": []
}

## Intro

Welcome to Part 1 of my Nested vSphere Home Lab Series.  In my [previous post](/posts/nested-vsphere-home-lab-series/), I went over the gist of what I plan to do for my Nested [vSphere](https://www.vmware.com/products/vsphere.html) Home Lab.  In this post, I will cover the setup and configuration of a [Sophos XG Firewall Home Edition](https://www.sophos.com/en-us/products/free-tools/sophos-xg-firewall-home-edition.aspx) which will serve as the router for my nested lab environment.  My physical Home Lab is configured with Virtual Distributed Switches, or VDS (sometimes seen as DVS) for short, and since this is a nested lab environment that will not have any physical uplinks connected, I will need to create a new VDS without physical uplinks connected to it along with a portgroup for the nested environment and then configure access to the environment from my LAN.  This can also be configured on a Virtual Standard Switch, or VSS for short, in the same fashion.  All network traffic will flow through the virtual router/firewall to communicate to and from the nested lab.  Afterward, I'll cover the Active Directory Server setup.

### Router

**Prerequisites:**

- VDS and portgroup without physical uplinks
  - Set the VLAN type for this portgroup to VLAN Trunking with the range of 0-4094 to allow all VLANs to trunk through
- Static route to access the nested lab from my LAN
  - Once you determine the subnets you’d like to use for the nested lab, add a static route summary on your physical router

![](/uploads/2023/04/2023-03-24_14-34-35.png)

I have a bunch of VLANs created for my physical Home Lab along with a little VMware [NSX](https://www.vmware.com/products/nsx.html) in there as well, serving physical and virtual network portgroups/segments to my lab.  With that said, one of the VLANs I have is for “lab” work, such as this so I’ll be connecting one uplink from the router to this VLAN which will serve as the WAN interface while the other uplink will be connected to the new nested portgroup to serve as the LAN for the nested lab.  I’ll describe the basics for deploying the Sophos XG firewall, but will not go into full detail as this is pretty trivial and can be deployed using the following [guide](https://www.linkedin.com/pulse/configuring-sophos-xg-firewall-vmware-esxi-kelvin-charles?trk=pulse_spock-articles) as a reference.

- OS: Other 6.x or later Linux
- CPU: 1 (add more as needed – max supported is 4 in the home edition)
- RAM: 4GB (add more as needed – max supported is 6GB in the home edition)
- Disk: 16GB thin (you may make this smaller if you’d like)
- Network Adapter 1: LAN portgroup (nested)
- Network Adapter 2: WAN portgroup
- Boot: BIOS (will not boot if you keep as EFI)

![](/uploads/2023/04/2023-04-21_22-15-53.png)

Once the VM has been deployed, the Sophos XG will be configured with a **172.16.16.1**6 address by default.  This will need to be changed to the subnet you’re using for your nested LAN interface.  Login to the console with the default (**admin – admin**) credentials, and choose the option for Network Configuration to change the IP for your nested LAN port.

![](/uploads/2023/04/2023-04-21_22-19-50.png)

Once this is done, you would normally navigate to that address on port **4444** to access the admin GUI.  Unfortunately, this will not work since the LAN side has no physical uplinks.  So what do we do?  We need to run a command to enable admin access on the WAN port.  To do so, choose **option 4** to enter the device console and enter the following command:

```bash
system appliance_access enable
```

The WAN port is set to grab an address from DHCP so you’ll need to determine which IP address this is either by going into your physical router, or using a tool like Angry IP.  Once in the Admin GUI, navigate to **Administration > Device Access** and tick the box for WAN under the HTTPS column.  See this [post](https://community.sophos.com/kb/en-us/123542) for reference.

![](/uploads/2023/04/2023-04-21_22-48-22.png)

Now, we can create our VLANs for our nested environment.  I’m using the following for my lab:

|  |  |  |
| --- | --- | --- |
| **VLAN** | **Subnet** | **Purpose** |
| 0 | 10.100.1.1/24 | Management |
| 1010 | 10.100.10.1/24 | vMotion |
| 1020 | 10.100.20.1/24 | VSAN |
| 1030 | 10.100.30.1/24 | TEP |
| 1040 | 10.100.40.1/24 | Uplink |

Navigate to **Networking** and select **Add Interface > VLAN** to create each of your networks.

![](/uploads/2023/04/2023-04-21_23-05-50.png)

With our VLANs created, we’ll need to create two firewall rules to allow traffic from the WAN port to access the LAN, as well as to allow traffic from LAN to LAN. Navigate to **Rules and policies > Add firewall rule** and create the following rules.  Choose something easy to label them as which makes sense to you.

![](/uploads/2023/04/2023-04-21_23-09-20.png)

This is where the static route will now be useful to access your nested lab.  I’ve configured a route summary of **10.100.0.0/16** to go through the IP address of the WAN interface as the gateway so that I can access the Admin UI at `https://10.100.1.1:4444` as well.  I’ll now also be able to access the ESXi UI and VCSA UI, once they are stood up.

![](/uploads/2023/04/2023-04-21_23-23-44.png)

The final thing I will be doing is enabling the native **MAC Learning** functionality that was introduced in vSphere 6.7, so that I do not need to enable Promiscuous Mode, which has normally been a requirement for the Nested portgroup and nested labs in general...and in some cases it still is!  To learn more about how to do this, see this [thread](https://www.virtuallyghetto.com/2018/04/native-mac-learning-in-vsphere-6-7-removes-the-need-for-promiscuous-mode-for-nested-esxi.html).  In my setup, I ran the following to enable this on my nested VDS portgroup:

```powershell
Set-MacLearn -DVPortgroupName @("vds1-nested-trunk") -EnableMacLearn $true -EnablePromiscuous $false -EnableForgedTransmit $true -EnableMacChange $false
```

To check that it was indeed set correctly, I ran the following:

```powershell
Get-MacLearn -DVPortgroupName @("vds1-nested-trunk")
```

![](/uploads/2023/04/2023-04-21_23-40-06.png)

Alternatively - now available in vSphere 8.0, you have the ability to enable MAC Leaning directly via the vCenter UI as well!!

![](/uploads/2023/04/2023-04-21_23-28-52.png)

 And there you have it!  In the next post, I will go over configuring an Active Directory server for the nested lab!

--virtualex
