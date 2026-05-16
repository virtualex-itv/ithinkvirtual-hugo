{
  "title": "NSX-T Home Lab - Part 4: Configuring NSX-T Fabric",
  "date": "2019-02-15T15:15:18",
  "lastmod": "2019-02-18T18:09:18",
  "slug": "nsx-t-home-lab-part-4-configuring-nsx-t-fabric",
  "url": "/posts/nsx-t-home-lab-part-4-configuring-nsx-t-fabric/",
  "draft": false,
  "description": "",
  "wordpress_id": 1487,
  "wordpress_url": "https://ithinkvirtual.com/2019/02/15/nsx-t-home-lab-part-4-configuring-nsx-t-fabric/",
  "featured_image": "/uploads/2019/02/2019-02-15_9-59-56.png",
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
    "/2019/02/15/nsx-t-home-lab-part-4-configuring-nsx-t-fabric/"
  ],
  "comments": []
}

## Intro

Welcome to Part 4 of my NSX-T Home Lab series. In my [previous post](/2019/02/12/nsx-t-home-lab-part-3-deploying-nsx-t-appliances/), I covered the process of deploying the NSX-T appliances and joining them to the management plane to have the foundational components ready for us to continue the configuration. In this post, I will cover all the configurations required to get NSX-T Fabric ready for network configurations in order to run workloads on it. So sit back, buckle up, and get ready for a lengthy read!

## Compute Manager

A compute manager, for example, a vCenter Server, is an application that manages resources such as hosts and VMs. NSX-T polls compute managers to find out about changes such as the addition or removal of hosts or VMs and updates its inventory accordingly. I briefly touched on this in my previous post, stating that one is required if deploying an NSX Edge appliance directly from the NSX Manager. Otherwise, the need for one of these is completely optional but I find value in it for retrieving my labs' inventory and is the first thing I like to do in my deployments. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-D225CAFC-04D4-44A7-9A09-7C365AAFCA0E.html).

To configure a Compute Manager, log into you NSX Manager UI and navigate to **Fabric > Compute Managers > +ADD**. Enter the required information, leaving the SHA-256 Thumbprint field empty, and click **ADD**. You should receive an error because a thumbprint was not provided but will ask you if you want to use the server provided thumbprint, so click **ADD**. Allow a brief 30-60 seconds for the Compute Manager to connect to the vCenter server, click refresh if needed, until you see that it's "**Registered**" and "**Up**".

![](/uploads/2019/02/2019-02-14_12-23-13.png)
![](/uploads/2019/02/2019-02-14_12-25-16.png)
![](/uploads/2019/02/2019-02-14_12-33-55.png)

## Tunnel EndPoint (TEP) IP Pool

As stated in the official documentation, Tunnel endpoints are the source and destination IP address used in the external IP header to uniquely identify the hypervisor hosts originating and terminating the NSX-T encapsulations of overlay frames. DHCP or IP pools can be configured for TEP IP addresses, so I'll create a dedicated pool to be used instead of using DHCP and they'll reside in the Overlay network VLAN **150**. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-E7F7322D-D09B-481A-BD56-F1270D7C9692.html).

To add a Tunnel EndPoint IP Pool, navigate to **Inventory > Groups > IP Pools > +ADD**. Provide a Name then click **+ADD** underneath the Subnets section and provide the required information for the IP pool then click **ADD**.

![](/uploads/2019/02/2019-02-14_14-07-13.png)

## Uplink Profiles

An uplink profile defines policies for the links from the hypervisor hosts to NSX-T logical switches or from NSX Edge nodes to top-of-rack switches. The settings defined by these profiles might include teaming policies, active/standby links, transport VLAN ID, and MTU setting. Uplink profiles allow you to consistently configure identical capabilities for network adapters across multiple hosts are nodes. By default, there are two uplink profiles already provided with NSX-T but they cannot be edited, therefore I am going to create new ones for the Edge uplink as well as for my hosts' uplinks. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-50FDFDFB-F660-4269-9503-39AE2BBA95B4.html).

### Edge Uplink Profile

To create an Edge uplink profile, navigate to **Fabric > Profiles > Uplink Profiles > +ADD**. Provide a Name, optional description then, under Teamings, set the Teaming Policy to **Failover Order**, set the Active Uplinks to **uplink-1**. Set the Transport VLAN to **0** as we are tagging at the port group level for our Edge, and either leave the MTU at the default 1600 or set it to a higher value supported for your Jumbo Frames configuration. In my setup, I will set the MTU to **9000**, then click **ADD**.

![](/uploads/2019/02/2019-02-14_13-19-00.png)

### Host Uplink Profile

Next, I'll repeat the process to create an uplink profile for my ESXi hosts. This time, I'll keep the same settings for Teaming but will set the Standby Uplinks as **uplink-2**, the Transport VLAN will be my Overlay VLAN ID **150** since these uplinks are connected directly to the hosts and need to be tagged accordingly, and again I'll set the MTU to **9000** and click **ADD**.

![](/uploads/2019/02/2019-02-14_13-27-38.png)

## Transport Zones

Transport Zones dictate which hosts, and therefore, which VMs can participate in the use of a particular network. There are two types of transport zones, an overlay, and a VLAN. The overlay transport zone is used by both host transport nodes and NSX Edges and is responsible for communication over the overlay network. The VLAN transport zone is used by the NSX Edge for it's VLAN uplinks. Both types create an N-VDS on the host or Edge to allow for virtual-to-physical packet flow by binding logical router uplinks and downlinks to physical NICs. For more information please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-F739DC79-4358-49F4-9C58-812475F33A66.html).

### Overlay Transport Zone

To create an overlay transport zone, navigate to **Fabric > Transport Zones > +ADD**. Provide a Name, an N-VDS Name, select **Standard**or **Enhanced Data Path** for the N-VDS Mode, set the Traffic Type as **Overlay** and click **ADD**.

Enhanced Data Path is a networking stack mode, which when configured provides superior network performance and is primarily targeted for NFV workloads. This requires you to install an additional VIB, as per your physical NICs, onto your hosts and reboot them before this can be configured, but this is out of scope for this demo. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-F459E3E4-F5F2-4032-A723-07D4051EFF8D.html).

I'll be choosing **Standard** for this demonstration as it's a nested lab and only sees the Physical NICs as traditional VMware VMXNET3 adapters.

![](/uploads/2019/02/2019-02-14_13-58-05.png)

### VLAN Transport Zone

To create a VLAN uplink transport zone, I'll repeat the same process as above by providing a Name, an N-VDS Name, but will change the Traffic Type to **VLAN** before clicking **ADD**.

![](/uploads/2019/02/2019-02-14_13-59-41.png)

## Transport Node

There are two types of transport nodes that need to be configured in NSX-T, a host transport node and an edge transport node. A host transport node is a node that participates in an NSX-T overlay or NSX-T VLAN networking whereas an edge transport node is a node that capable of participating in an NSX-T overlay or NSX-T VLAN networking. In short, they simply facilitate communication in an NSX-T Overlay and/or NSX-T VLAN network. For more information, please see the documentation [here](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-D7CA778B-6554-4A23-879D-4BC336E01031.html) and [here](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-53295329-F02F-44D7-A6E0-2E3A9FAE6CF9.html).

I'll be automatically creating the host transport nodes when I add them to the fabric but will be manually creating a single edge transport node with two N-VDS' for my overlay and VLAN uplink transport zones respectively.

### Host Transport Node

This part is pretty simple and is where having the Compute Manager that I configured earlier comes in handy. But this process can also be done manually. You'll need to ensure you have at least 1 Physical NIC (pNIC) available for NSX-T, and you can see here that my hosts were configured with 4 pNICs and I have 2 available, **vmnic2** and **vmnic3**.

![](/uploads/2019/02/2019-02-15_9-07-36.png)

Navigate to **Fabric > Nodes > Hosts** and from the "Managed By" dropdown menu, select the compute manager. Select a cluster and then click **Configure Cluster**. Toggle both switches to **Enabled** to **Automatically Install NSX** and **Automatically Create Transport Node**. From the Transport Zone dropdown menu, select the Overlay transport zone created earlier, from the Uplink Profile dropdown menu select the host uplink profile created earlier, from the IP Pool dropdown menu select the TEP IP Pool created earlier. Lastly, enter in the pNIC names and choose their respective uplinks. If you have 2 pNICs, click **add PNIC** and then modify the information before clicking **ADD** to complete the process.

![](/uploads/2019/02/2019-02-15_9-14-33.png)

This will start the host preparation process so allow a few minutes for the NSX VIBs to be installed on the hosts and for the transport nodes to be configured, clicking the refresh button as needed until you see "NSX Installed" and the statuses are "Up".

![](/uploads/2019/02/2019-02-15_9-16-38.png)
![](/uploads/2019/02/2019-02-15_9-48-27.png)

Click on the Transport Nodes tab, and we can see that the nodes have been automatically created and are ready to go. And if we look back at the physical NICs in vCenter, we can see that they have now been added to the N-VDS-Overlay.

![](/uploads/2019/02/2019-02-15_9-49-25.png)
![](/uploads/2019/02/2019-02-15_9-54-26.png)

### Edge Transport Node

Begin by navigating to **Fabric > Nodes > Transport Nodes > +ADD**. Provide a Name, from the Node dropdown menu select the Edge that we deployed and joined to the management plane in the previous post, in the "Available" column select the two transport zones we previously created and click the **>** arrow to move them over to the "Selected" column, then click the **N-VDS** heading tab at the top of the window.

![](/uploads/2019/02/2019-02-14_14-53-29.png)

From the Edge Switch Name dropdown menu, select the N-VDS we created earlier for the **Overlay**. From the Uplink Profile dropdown menu, select the **edge uplink profile** we created earlier. From the IP Assignment dropdown menu, select **Use IP Pool**, from the IP Pool dropdown menu, select the **TEP IP Pool** created earlier, and finally, from the Virtual NICs dropdown menus, select **fp****-eth0** which is the 2nd NIC on the Edge VM and then select **uplink-1**.

![](/uploads/2019/02/2019-02-14_15-18-45.png)

But we're not done yet! Next, click **+ADD N-VDS** so that we can add the additional one needed for the remaining transport zone. From the Edge Switch Name dropdown menu, select the N-VDS we created earlier for the **VLAN Uplink**. From the Uplink Profile dropdown menu, select the **edge uplink profile** again. And from the Virtual NICs dropdown menus, select **fp-eth1** which is the 3rd NIC on the Edge VM and then select **uplink-1**. Now we can finally click **ADD**.

![](/uploads/2019/02/2019-02-14_15-29-29.png)

Allow a few minutes for the configuration state and status to report "Success" and "Up" and click the refresh button as needed.

![](/uploads/2019/02/2019-02-14_15-32-38.png)

## Edge Cluster

Having a multi-node cluster of NSX Edges helps ensure that at least one NSX Edge is always available. In order to create a tier-0 logical router or a tier-1 router with stateful services such as NAT, load balancer, and so on. You must associate it with an NSX Edge cluster. Therefore, even if you have only one NSX Edge, it must still belong to an NSX Edge cluster to be useful. For more information, please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-898099FC-4ED2-4553-809D-B81B494B67E7.html).

To create an edge cluster, navigate to **Fabric > Nodes > Edge Clusters > +ADD**. Enter a Name, and in the "Available" column select the **edge transport zone** created earlier and click the > arrow to move it to the "Selected" column and click **ADD**. Well, that was easy!

![](/uploads/2019/02/2019-02-14_16-48-17.png)

Wow! That seemed like a lot of work but it was exciting to get the components configured and ready for setting up the Logical Routers and switches, which I'll cover in the next post, so we can start running VMs in NSX-T. I hope you've found this post useful and I thank you for reading.
