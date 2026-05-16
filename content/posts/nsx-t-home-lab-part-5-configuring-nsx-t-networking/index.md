{
  "title": "NSX-T Home Lab - Part 5: Configuring NSX-T Networking",
  "date": "2019-02-19T17:25:44",
  "lastmod": "2019-02-22T23:04:29",
  "slug": "nsx-t-home-lab-part-5-configuring-nsx-t-networking",
  "url": "/posts/nsx-t-home-lab-part-5-configuring-nsx-t-networking/",
  "draft": false,
  "description": "",
  "wordpress_id": 1519,
  "wordpress_url": "https://ithinkvirtual.com/2019/02/19/nsx-t-home-lab-part-5-configuring-nsx-t-networking/",
  "featured_image": "/uploads/2019/02/2019-02-19_12-06-26.png",
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
    "/2019/02/19/nsx-t-home-lab-part-5-configuring-nsx-t-networking/"
  ],
  "comments": []
}

## Intro

Welcome to Part 5 of my NSX-T Home Lab series. In my [previous post](/2019/02/15/nsx-t-home-lab-part-4-configuring-nsx-t-fabric/), I went over the lengthy process of configuring the NSX-T fabric. In this post, I am going to cover the process of configuring the networking so we can get the logical routers and logical switches in place and ready to attach VMs to them and begin running workloads on NSX. Let get to it, shall we?

## Logical Switch

An NSX-T Data Center logical switch reproduces switching functionality, broadcast, unknown unicast, multicast (BUM) traffic, in a virtual environment completely decoupled from the underlying hardware.
Logical switches are similar to VLANs, in that they provide network connections to which you can attach virtual machines. For more information, please see the documentation.

I am going to start off by creating a Logical Switch to serve as my uplink from the external network to my Tier-0 router, which I'll create afterward. To create a logical switch, select **Networking > Switching > +ADD**. Enter a Name, then from the Transport Zone drop-down menu select the VLAN uplink transport zone that was created in the previous post. Since I'll be tagging VLANs at the port group level, enter a **0** (zero) for the VLAN ID and click **ADD**.

![](/uploads/2019/02/2019-02-18_17-07-01.png)

And that's all there is to it! After a logical switch is created, we need to create a port for it to connect it to a logical router, but we first need a Tier-0 Logical Router.

## Tier-0 Logical Router

An NSX-T Data Center logical router reproduces routing functionality in a virtual environment completely decoupled from the underlying hardware. The tier-0 logical router provides an on and off gateway service between the logical and physical network. Tier-0 logical routers have downlink ports to connect to NSX-T Data Center tier-1 logical routers and uplink ports to connect to external networks. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.admin.doc/GUID-3F163DEE-1EE6-4D80-BEBF-8D109FDB577C.html).

To create a Tier-0 Logical Router, select **Networking > Routers > +ADD** and select **Tier-0 Router** from the drop-down menu. Provide a Name for the router and from the Edge Cluster drop-down menu, select the edge cluster that was created in the previous post then click **ADD**. Changing the High Availability setting is optional and I'm choosing to leave the default Active-Active setting.

![](/uploads/2019/02/2019-02-18_16-52-55.png)

With the Tier-0 logical router created, click on the router and from the Configuration drop-down menu, select **Router Ports** then click **+ADD** under **Logical Router Ports**.

![](/uploads/2019/02/2019-02-18_16-59-07.png)

Enter a Name, leave the Type as "Uplink", optionally change the MTU value to support a configured Jumbo Frame, otherwise leave the default 1500 value (I am using 9000 for Jumbo Frames in my environment). From the Transport Node drop-down menu, select the edge transport node created in the previous post. From the Logical Switch drop-down menu, select the logical switch that was created in the previous step, then provide a name for the Logical Switch Port and provide an address on the "Uplink" VLAN **160** for the router port and click **ADD**.

![](/uploads/2019/02/2019-02-18_17-18-46.png)

Now, with the Tier-0 Logical router created and attached to an uplink Logical Switch, I have the option of either setting up a Static Route to send/receive data to/from or to configure Border Gateway Protocol also known simply as BGP. Until one of these is configured, I won't be able to ping my Tier-0 router. I am going to opt to configure BGP so that any network I add later on down the road will get advertised properly to the neighbor router (Sophos XG) on my external network instead of using a wide-open static route. I'll come back to BGP configuration a little later on, but first, I'd like to set up a Tier-1 to connect to my Tier-0. Any VLAN-based logical switches I create from this point on will be attached to the Tier-1 logical router.

## Tier-1 Logical Router

Similar to Tier-0 Logical Routers, Tier-1 logical routers have downlink ports to connect to NSX-T Data Center logical switches and uplink ports to connect to NSX-T Data Center tier-0 logical routers. The tier-1 logical router must be connected to the tier-0 logical router to get the northbound physical router access. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.admin.doc/GUID-DAEF8457-8363-4F33-84DA-68AA36A2DE3C.html).

As was done when creating the tier-0 logical router, repeat the same process by selecting **Networking > Routing > +ADD** but select **Tier-1 Router** from the drop-down menu instead. Provide a Name, from the Tier-0 Router drop-down menu, select the Tier-0 router that was created in the previous step to attach the Tier-1 to it. Next, from the edge cluster drop-down menu, select the edge cluster that was created in the previous post, leave the default Failover Mode then from the Edge Cluster Members drop-down menu, select the edge transport node that was created in the previous post and click **ADD**.

![](/uploads/2019/02/2019-02-18_17-35-47.png)

## BGP Configuration

To take full advantage of the tier-0 logical router, the topology must be configured with redundancy and symmetry with BGP between the tier-0 routers and the external top-of-rack peers. To enable access between your VMs and the outside world, you can configure an external BGP (eBGP) connection between a tier-0 logical router and a router in your physical infrastructure. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.admin.doc/GUID-4BC07C6A-DC62-496B-A6A9-7219ACF5AC7B.html).

To configure BGP on a Tier-0 logical router, select **Networking > Routing** and select the **Tier-0 router**. From the **Routing** drop-down menu, select **BGP** and click **+ADD** under the Neighbors section. Enter the neighbor router address, in this case since I am using a VLAN for my Uplink network, I will specify the gateway address of my **VLAN 160** configured on my Sophos XG firewall/router. Next, select the Max Hop count needed to reach the neighbor router. In my case, my Tier-0 router is configured with the IP address of *10.254.160.2* and is one hop away from the gateway at *10.254.160.1* so I'll leave the count set to **1**. Finally, provide a **Remote AS** number which will be configured on the neighbor router (Sophos XG) and click **ADD**.

![](/uploads/2019/02/2019-02-18_18-00-45.png)

Next, click EDIT next to BGP Configuration. Toggle the **Status** switch to **Enabled** and enter a **Local AS** number for the Tier-0 router. Optionally, toggle the **Graceful Restart** switch to **Enabled** only if the Edge Cluster has one member, which is the case in this nested lab environment, then click **SAVE**.

![](/uploads/2019/02/2019-02-18_18-06-25.png)

Pretty straight forward right? But we're not done just yet. In order for routes to be advertised properly to the neighbor router, there are a few more things required one of which is to enable Route Redistribution. To do so, select the Tier**-0 Logical Router > Routing dro**p-down menu, and select **Route Redistribution**. Click **EDIT** and toggle the **Status** switch to **Enabled** and click **SAVE**. Next, click +ADD and enter a name for the route redistribution configuration, then from the "Sources" choices, select **NSX Static** and click **ADD**. NSX sees any advertised routes as a "dynamic" static route, therefore, this setting needs to be enabled to properly advertise routes to the neighbor router.

![](/uploads/2019/02/2019-02-18_18-19-01.png)

With BGP now configured on the virtual NSX side, I need to also configure BGP on physical side meaning on my Sophos XG. Log into the Sophos XG firewall and navigate to **Routing > BGP**. Here, I will add my VLAN 160 gateway IP address as the Router ID and set the Local AS number for my router and click **Apply**.

- ![](/uploads/2019/02/2019-02-18_18-23-44.png)

Next, I'll click **Add** under the Neighbors section and will add the Tier-0 router IP address along with the AS number I configured it and click **Save**.

![](/uploads/2019/02/2019-02-18_18-27-09.png)
![](/uploads/2019/02/2019-02-18_18-28-55.png)

Lastly, I'll head over to **Administration > Device Access** and check the boxes for **LA**N & **WAN** under Dynamic Routing then click **Apply**. I believe that only **WAN** is required to mimic a true production environment but since this is a lab, it won't cause any harm to enable both.

![](/uploads/2019/02/2019-02-19_8-59-18.png)

Now, it's time to test our configurations. I'll start off by running a ping test from my jump-box or desktop computer on an external network to the Tier-0 logical router.

![](/uploads/2019/02/2019-02-18_18-31-28.png)

Success!! Next, I will check to see that my Sophos XG can see it's BGP neighbor but navigating to **Routing > Information > BGP > Neighbors** or **Summary**

![](/uploads/2019/02/2019-02-18_18-34-23.png)
![](/uploads/2019/02/2019-02-18_18-36-10.png)

Success again!! I am on a roll!! It's also a good idea to check the same on the NSX Edge appliance. To do so, open an SSH connection to the NSX Edge appliance and run the following commands.

```bash
get logical-routers
```

This will list the available Tier-0 and Tier-1 routers.

![](/uploads/2019/02/2019-02-18_18-48-42.png)

Copy the UUID of the Tier-0 router and run the following.

```bash
get logical-router <paste-UUID-here> bgp neighbor
```

![](/uploads/2019/02/2019-02-18_18-50-12.png)

Perfect! At this point, I can't see any advertised routes in BGP because I have yet to create any. In order for the Tier-1 router to advertise any new routes, I need to enable Route Advertisements. To do so, navigate to **Networking > Routing** and select the **Tier-1 Logical Router** then from the **Routing** drop-down menu, select **Route Advertisement**. Click **EDIT** and toggle the **Status** switch to **Enabled** and the **Advertise All NSX Connected Routes** to **Yes** and click **SAVE**.

![](/uploads/2019/02/2019-02-18_19-10-24.png)

Now, I'll go ahead and create a new Logical Switch and will attach it to a Router Port on my Tier-1 Logical Router.

![](/uploads/2019/02/2019-02-18_18-55-14.png)
![](/uploads/2019/02/2019-02-18_18-57-01.png)

As you can see above, I've assigned the router port and IP address of ***192.168.254.1/24*** so now I should be able to see this route being advertised from the NSX Edge and received on the Sophos XG. I'll first check the NSX Edge.

```bash
get logical-router <paste_UUID_here> route static
```

![](/uploads/2019/02/2019-02-18_19-13-33.png)

Excellent! Remember, NSX-T treats the advertised routes as static routes hence the reason that "static" was used in the command syntax on the NSX Edge. Next, I'll check the routes from the Sophos XG.

![](/uploads/2019/02/2019-02-18_19-16-44.png)

BOOM!! Now we're cooking with gas! BGP is up and running, advertising routes as expected. The only caveat at this point is that I cannot ping this network from my jump-box or local desktop on my external network (not connected to the Sophos XG) unless I create a static route on my physical router. But I should be able to ping from a VM connected to an external network on the Sophos XG (VLAN 140) since the route is advertised and the router knows about it. Let's test it from the nested lab's domain controller.

![](/uploads/2019/02/2019-02-18_19-47-41.png)

Nice! At this point, why not spin up a VM and attach it to the new Logical Switch and see if we can access the outside world, right? I'll quickly deploy a Linux VM from a template that I have which is configured to obtain an IP address via DHCP. But wait! I'll first need a DHCP server within NSX to handle the distribution of dynamic host IPs. While my VM is deploying from a template, let's cover the process of creating a DHCP server in NSX-T.

## DHCP Server

DHCP (Dynamic Host Configuration Protocol) allows clients to automatically obtain network configuration, such as IP address, subnet mask, default gateway, and DNS configuration, from a DHCP server. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.admin.doc/GUID-1409548E-C26E-4AAE-9B6F-CFDCC6798175.html).

To create a DHCP Server, I first need a DHCP Profile. I'll create one by navigating to **Networking > DHCP > Server Profiles > +ADD**. Provide a Name, from the Edge Cluster drop-down menu select the edge cluster that was previously created, and from the Members drop-down menu select the NSX edge transport node that was previously created and click **ADD**.

![](/uploads/2019/02/2019-02-18_20-57-34.png)

Next, click **Networking > DHCP > Servers > +ADD**. Provide a Name, an IP Address and netmask for the DHCP server and select the DHCP profile that was just created and click **ADD**. The Common Options, etc. are not required as we can set these in the next step when creating the IP address pool, but you can set it now if you'd like.

![](/uploads/2019/02/2019-02-18_21-10-52.png)

Now, click on the newly created DHCP server and under the IP Pool section click **+ADD**. Provide a Name, an IP address range, a Gateway IP address, and fill out the Common Options then click **ADD**.

![](/uploads/2019/02/2019-02-18_21-07-51.png)

Lastly, I need to attach the DHCP server to the Logical Switch so that it can begin handing out addresses to VMs connected to it. Click the DHCP server and from the "**Actions** drop-down menu, select **Attach to Logical Switch**. Select the logical switch from the drop-down menu and click **ATTACH**. The DHCP server is now ready to hand out IP addresses!

- ![](/uploads/2019/02/2019-02-18_21-23-57.png)

## Running Workloads on NSX-T

With the DHCP Server created and a new VM deployed, I'll attach the VM to the Logical switch and power it on. Select the VM, right-click it and select **Edit Settings**. Change the network adapter port group to the new Logical Switch that was created and click **OK**.

![](/uploads/2019/02/2019-02-18_21-16-37.png)

Power on the VM and once it's up, log in and check that it has grabbed an IP address from the DHCP servers IP pool.

![](/uploads/2019/02/2019-02-18_21-27-30.png)

Just what I wanted to see! The VM successfully grabbed an IP address from the DHCP server! Woo-Hoo!! I can also ping the VM from the domain controller.

![](/uploads/2019/02/2019-02-18_21-29-54.png)

Now, the only thing left is to see if we can ping the outside world like Google's DNS server. In order for this to work properly, the router would need to know how to NAT this VMs IP address to the outside otherwise, this can be expected to fail as seen below.

![](/uploads/2019/02/2019-02-18_21-33-43.png)

There are a couple of options. The recommended way would be to create a SNAT rule on the Sophos XG firewall/router so it knows how to route traffic out to the WAN. Another way would be to set up a SNAT rule in NSX. This can be a bit tricky in a nested lab setup like this one due to it basically being "Double NAT'ed". I'd prefer to do the rule on the Sophos but as I'm still learning my way around its interface and settings, so it may be easier to simply create a SNAT rule in NSX until I figure out how to do it on the Sophos XG. The one caveat here is that when a SNAT rule is created in NSX, it will break access to the network from an external network, meaning I won't be able to ping the VM anymore unless I also set up a DNAT rule and ping it's NAT address to reach the VM. Let me show you how to create the SNAT rule.

## Source NAT (SNAT)

Source NAT (SNAT) changes the source address in the IP header of a packet. It can also change the source port in the TCP/UDP headers. The typical usage is to change a private (rfc1918) address/port into a public address/port for packets leaving your network. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.admin.doc/GUID-31CEF010-0C34-4C10-9443-13A0EAAABFD6.html).

To create a SNAT rule, navigate to **Networking > Routing**. Click the tier-1 logical router and from the **Services** drop-down menu, select **NAT**. Click **+ADD**. For the Source IP, add the network that you want to Source NAT. For the Translated IP, pick an IP address on the Uplink VLAN, in my case, this is VLAN **160**. My Tier-0 router uses *10.254.160.2* so I will set this Translated IP to *10.254.160.3* then click **ADD**.

![](/uploads/2019/02/2019-02-19_10-31-54.png)

Next, from the **Routing** drop-down menu, select **Route Advertisement**. Click **EDIT** and toggle the **Advertise All NAT Routes** to **Enabled** and click **SAVE**.

![](/uploads/2019/02/2019-02-19_10-40-58.png)

Lastly, click the **Tier-0 router** and from the **Routing** drop-down menu, select **Route Redistribution**. Select the route redistribution criteria that was created earlier in this post and click **EDIT**. Click the checkbox for **Tier-1 NAT** and click **SAVE**.

![](/uploads/2019/02/2019-02-19_10-46-14.png)

In theory, this all should've allowed me to access the outside world but I wasn't able to do so and I'm thinking there are additional firewall rules required on the Sophos XG to allow it. Of course, things like this are to be expected when working in nested environments but I'll continue to tinker with this until I get it to work in the nested lab and will update the post should I figure it out.

Well, that about does it for this one! In the next post, I'll cover the process of upgrading NSX-T. It will be a while before I get to that since the version I just deployed is the latest release. Thanks as always for your support!
