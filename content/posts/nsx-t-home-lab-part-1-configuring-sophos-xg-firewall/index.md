{
  "title": "NSX-T Home Lab - Part 1: Configuring Sophos XG Firewall",
  "date": "2019-01-21T22:10:49",
  "lastmod": "2019-02-15T19:38:19",
  "slug": "nsx-t-home-lab-part-1-configuring-sophos-xg-firewall",
  "url": "/posts/nsx-t-home-lab-part-1-configuring-sophos-xg-firewall/",
  "draft": false,
  "description": "",
  "wordpress_id": 1368,
  "wordpress_url": "https://ithinkvirtual.com/2019/01/21/nsx-t-home-lab-part-1-configuring-sophos-xg-firewall/",
  "featured_image": "/uploads/2019/01/2019-01-20_23-00-36.png",
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
    "/2019/01/21/nsx-t-home-lab-part-1-configuring-sophos-xg-firewall/"
  ],
  "comments": []
}

## Intro

Welcome to Part 1 of my NSX-T Home Lab Series.  In my [previous post](/2019/01/21/nsx-t-home-lab-series/), I went over the gist of what I plan to do for my nested [NSX-T](https://www.vmware.com/products/nsx.html) Home Lab.  In this post, I will cover the setup and configuration of a [Sophos XG firewall Home Edition](https://www.sophos.com/en-us/products/free-tools/sophos-xg-firewall-home-edition.aspx) which will serve as the router for my nested lab environment.  My physical Home Lab is configured with Virtual Distributed Switches, or VDS (sometimes seen as DVS) for short, and since this is a nested lab environment that will not have any physical uplinks connected, I will need to create a new VDS without physical uplinks connected to it along with a portgroup for the nested environment and then configure access to the environment from my LAN.  All traffic will flow through virtual router/firewall to communicate to and from the nested lab.

**Prerequisites:**

- VDS and portgroup without physical uplinks
  - Set the VLAN type for this portgroup to VLAN Trunking with the range of 0-4094 to allow all VLANs to trunk through
- Static route to access the nested lab from my LAN
  - Once you determine the subnets you'd like to use for the nested lab, add a static route summary on your physical router

![](/uploads/2019/01/2019-01-21_11-16-07-1024x559.png)

I have a bunch of VLANs created for my physical Home Lab as I've yet to deploy NSX-T in there, but once I do, I'll be removing the majority of said VLANs and only keeping the required ones needed to run the lab.  With that said, one of the VLANs I have is for "Development" work, such as this so I'll be connecting one uplink from the router to this VLAN which will serve as the WAN interface while the other uplink will be connected to the new nested portgroup to serve as the LAN for the nested lab.  I'll describe the basics for deploying the Sophos XG firewall, but will not go into full detail as this is pretty trivial and can be deployed using the following [guide](https://www.linkedin.com/pulse/configuring-sophos-xg-firewall-vmware-esxi-kelvin-charles?trk=pulse_spock-articles) as a reference.

- OS: Other Linux 3.x or higher
- CPU: 1 (add more as needed - max supported is 4 in the home edition)
- RAM: 2GB (add more as needed - max supported is 6GB in the home edition)
- Disk: 40GB thin (you may make this smaller if you'd like)
- Network Adapter 1: LAN portgroup (nested)
- Network Adapter 2: WAN portgroup
- Boot: BIOS (will not boot if you keep as EFI)

![](/uploads/2019/01/2019-01-21_10-08-39.png)

Once the VM has been deployed, the Sophos XG will be configured with a **172.16.1.1** address by default.  This will need to be changed to the subnet you're using for your nested LAN interface.  Login to the console with the default (**admin - admin**) credentials, and choose the option for Network Configuration to change the IP for your nested LAN port.

![](/uploads/2019/01/2019-01-20_23-11-09.png)

Once this is done, you would normally navigate to that address on port **4444** to access the admin GUI.  Unfortunately, this will not work since the LAN side has no physical uplinks.  So what do we do?  We need to run a command to enable admin access on the WAN port.  To do so, choose **option 4** to enter the device console and enter the following command:

```bash
system appliance_access enable
```

The WAN port is set to grab an address from DHCP so you'll need to determine which IP address this is either by going into your physical router, or using a tool like Angry IP.  Once in the Admin GUI, navigate to **Administration > Device Access** and tick the box for WAN under the HTTPS column.  See this [post](https://community.sophos.com/kb/en-us/123542) for reference.

![](/uploads/2019/01/2019-01-20_17-23-05-1024x559.png)

Now, we can create our VLANs for our nested environment.  I'm using the following for my lab:

|  |  |  |
| --- | --- | --- |
| **VLAN** | **Subnet** | **Purpose** |
| 110 | 10.254.110.1/24 | Management |
| 120 | 10.254.120.1/24 | vMotion |
| 130 | 10.254.130.1/24 | VSAN |
| 140 | 10.254.140.1/24 | VM Network |
| 150 | 10.254.150.1/24 | Overlay |
| 160 | 10.254.160.1/24 | Uplink |

Navigate to **Networking** and select **Add Interface > VLAN** to create each of your networks.

![](/uploads/2019/01/2019-01-20_23-05-52-1024x559.png)

With our VLANs created, we'll need to create two firewall rules to allow traffic from the WAN port to access the LAN, as well as to allow traffic from LAN to LAN. Navigate to **Firewall > Add firewall rule** and create the following rules.  Choose something easy to label them as which makes sense to you:

![](/uploads/2019/01/2019-01-20_23-02-09-1024x559.png)

This is where the static route will now be useful to access your nested lab.  I've configured a route summary of **10.254.0.0/16** to go through the IP address of the WAN interface as the gateway so that I can access the Admin UI at `https://10.254.1.1:4444` as well.  I'll now also be able to access the ESXi UI and VCSA UI, once they are stood up.

![](/uploads/2019/01/2019-01-21_11-37-19-1024x559.png)

The final thing I will be doing is enabling the native **MAC Learning** functionality that is now built into vSphere 6.7 so that I do not need to enable Promiscuous Mode, which has normally been a requirement for the Nested portgroup and nested labs in general.  To learn more about how to do this, see this [thread](https://www.virtuallyghetto.com/2018/04/native-mac-learning-in-vsphere-6-7-removes-the-need-for-promiscuous-mode-for-nested-esxi.html).  In my setup, I ran the following to enable this on my nested VDS portgroup:

```powershell
Set-MacLearn -DVPortgroupName @("VDS1-254-NESTED") -EnableMacLearn $true -EnablePromiscuous $false -EnableForgedTransmit $true -EnableMacChange $false
```

To check that it was indeed set correctly, I ran the following:

```powershell
Get-MacLearn -DVPortgroupName @("VDS1-254-NESTED")
```

![](/uploads/2019/01/2019-01-21_14-08-49.png)

And there you have it!  In the next post, I will go over configuring our ESXi VMs for our nested lab!
