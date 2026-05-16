{
  "title": "NSX-T Home Lab - Part 3: Deploying NSX-T Appliances",
  "date": "2019-02-12T23:22:25",
  "lastmod": "2019-02-15T19:45:40",
  "slug": "nsx-t-home-lab-part-3-deploying-nsx-t-appliances",
  "url": "/posts/nsx-t-home-lab-part-3-deploying-nsx-t-appliances/",
  "draft": false,
  "description": "",
  "wordpress_id": 1438,
  "wordpress_url": "https://ithinkvirtual.com/2019/02/12/nsx-t-home-lab-part-3-deploying-nsx-t-appliances/",
  "featured_image": "/uploads/2019/02/2019-02-12_18-09-16.png",
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
    "/2019/02/12/nsx-t-home-lab-part-3-deploying-nsx-t-appliances/"
  ],
  "comments": []
}

## Intro

Welcome to Part 3 of my NSX-T Home Lab Series. In my [previous post](/2019/01/21/nsx-t-home-lab-part-2-configuring-esxi-vms/), I went over the process of setting up the Sophos XG firewall/router VM for my nested lab environment. In this post, we'll cover the process of deploying the required NSX-T Appliances. There are 3 main appliances that need to be deployed, the first is the NSX-T Manager, followed by a single or multiple Controllers, and lastly, a single or multiple Edge appliances. For the purposes of this nested lab demo, I will only be deploying a single instance of each appliance, but please follow recommended best practices if you are leveraging this series for a production deployment. With all that said, let's get to it!

## NSX-T Manager Appliance

Prior to deploying the appliance VM's, it's recommended to create DNS entries for each component. I've already done this on my Domain Controller. Additionally, if you need to obtain the OVA's, please download them from [here](https://my.vmware.com/web/vmware/details?downloadGroup=NSX-T-231&productId=673&rPId=29868). At the time of this writing, NSX-T 2.3.1 is the latest version.

We'll begin by deploying the NSX Manager appliance to our Management Cluster using the vSphere (HTML5) Web Client and deploying the NSX Unified Appliance OVA. You can also deploy via the command line and/or PowerCLI, but for the purposes of this demo, I am going to leverage the GUI. Please use the following installation [instructions](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-FA0ABBBD-34D8-4DA9-882D-085E7E0D269E.html) to deploy the NSX Manager Appliance. I've used the following configuration options for my deployment:

- "Small" configuration - consumes 2 vCPU and 8GB RAM.
  - The default "Medium" configuration consumes 4 vCPU and 16GB RAM
- Thin Provision for storage
- Management Network port group on VLAN 110
- Role - nsx-manager
- Enable SSH
- Allow root SSH Logins

![](/uploads/2019/02/2019-02-12_10-34-21.png)

Once the appliance has been deployed, edit its settings and remove the CPU and Memory reservations by setting the values to 0 "zero". Normally, these would be left to guarantee those resources for the appliance but since this is a resource-constrained nested lab, I'm choosing to remove them.

![](/uploads/2019/02/2019-02-12_11-20-19.png)

At this point, power on the appliance and wait a few minutes for the Web UI to be ready, then open a browser to the IP or FQDN of the NSX Manager and log in using the credentials provided during the deployment *(admin/the_configured_passwd)*. Accept the EULA and choose whether or not to participate in the CEIP.

![](/uploads/2019/02/2019-02-12_16-35-10.png)
![](/uploads/2019/02/2019-02-12_16-40-42.png)

## NSX-T Controller Appliance

Next up is the NSX Controller. There are several ways that this appliance can be deployed such as via the command line, PowerCLI, vSphere Web Client, or directly from the NSX Controller. For this demo, I am opting to continue my deployment via the vSphere Web Client for the sake of simplicity and comfortability. As was done with the NSX Manager, deploy the NSX Controller OVA by following these [instructions](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-24428FD4-EC8F-4063-9CF9-D8136740963A.html). Again, since this is a resource-constrained nested lab, I am going to choose the following configuration options and remove the CPU and Memory reservations after the deployment has completed.

- "Small" configuration - consumes 2 vCPU and 8GB RAM.
  - The default "Medium" configuration consumes 4 vCPU and 16GB RAM
- Thin Provision for storage
- Management Network port group on VLAN 110
- Enable SSH
- Allow root SSH Logins
- Ignore the "Internal Properties" section as it's optional

![](/uploads/2019/02/2019-02-12_11-24-02.png)
![](/uploads/2019/02/2019-02-12_11-29-09.png)

With this part of the deployment complete, go ahead and power on the appliance. The next step is to join the controller to the management plane (NSX Manager) since we deployed the controller manually. Follow these [instructions](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-05434745-7D74-4DA8-A68E-9FE17093DA7B.html#GUID-05434745-7D74-4DA8-A68E-9FE17093DA7B) to perform this step, but I'll also post screenshots below. These steps can either be done from the appliance console or via SSH. I'll opt for the latter since we chose the option to allow SSH during the previous deployments. Be mindful of the appliances I am running commands on in the screenshots below as some are done on the manager while others are done on the controller.

![](/uploads/2019/02/2019-02-12_17-02-53.png)
![](/uploads/2019/02/2019-02-12_17-04-39.png)
![](/uploads/2019/02/2019-02-12_17-10-14.png)
![](/uploads/2019/02/2019-02-12_17-10-53.png)

In the last image above, we can see that the Control cluster status reports "***UNSTABLE***". This is to be expected in this deployment scenario as we only deployed a single controller instance. Nothing for us to worry about here.

Now that we've joined the Controller to the Manager (management plane), there is one last thing to do which is to initialize the Control Cluster to create a Control Cluster Master. To do so, follow these [instructions](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-273F6344-7212-4105-9FBA-A872CD75803F.html).

![](/uploads/2019/02/2019-02-12_17-21-15.png)

Now, if we log in to the NSX Manager again and click the Dashboard view, we can see that we now have both a Manager and a Controller Node configured.

![](/uploads/2019/02/2019-02-12_17-22-33.png)

## NSX-T Edge Appliance

Are you still with me? Good! The final component to deploy is the NSX Edge. As we've done with the other appliance, I will continue deploying the Edge via the vSphere GUI instead of leveraging the NSX Manager and I'll tell you why. Deploying via the NSX Manager is the easiest method, but there is a caveat. Deploying from the NSX Manager will only allow you to select a "Medium" or "Large" configuration deployment and will automatically power on the appliance post-deployment thus keeping the set CPU and Memory reservations. I've heard there is a way to trick the UI to deploy a "Small" configuration, but I've yet to confirm this nor have I seen it done. Additionally, there is a prerequisite for deploying via the NSX Manager which is to configure a Compute Manager which we've yet to cover and will be covered in the next post of this series. Follow these [instructions](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-AECC66D0-C968-4EF2-9CAD-7772B0245BF6.html) to deploy the appliance. By deploying via the vSphere Web Client, I have the ability to select "small" for the deployment and then remove the reservations before powering on the appliance, but feel free to use your method of choice.

As we've done with the other deployments, use the following options.

- "Small" configuration - consumes 2 vCPU and 4GB RAM.
  - The default "Medium" configuration consumes 4 vCPU and 8GB RAM
- Thin Provision for storage
- Management Network port group on VLAN 110
- Enable SSH
- Allow root SSH Logins
- Ignore the "Internal Properties" section as it's optional and any other non-relevant fields

When we get to the networking section, select the Management port group for "Network 0", select the Overlay port group for "Network 1", and select the Uplink portgroup for "Network 2" and "Network 3".

![](/uploads/2019/02/2019-02-12_11-33-31.png)
![](/uploads/2019/02/2019-02-12_11-36-02.png)
![](/uploads/2019/02/2019-02-12_11-39-23.png)

Power on the appliance, and when the console is ready, either log in to the console or connect via SSH as we'll need to also join this appliance to the management place as we did previously with the controller. Follow these [instructions](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.3/com.vmware.nsxt.install.doc/GUID-11BB4CF9-BC1D-4A76-A32A-AD4C98CBF25B.html) to complete this process. Again, be mindful of which appliances the commands are executed against.

![](/uploads/2019/02/2019-02-12_17-02-53.png)
![](/uploads/2019/02/2019-02-12_17-56-31.png)

Again, if we log into the NSX Manager and click the Dashboard view, we'll now see that we also have an Edge Node configured. Woo-hoo!!

![](/uploads/2019/02/2019-02-12_18-00-50.png)

Well, this completes this post and I hope you had fun following along. In the next post, I'll cover adding hosts to our NSX-T fabric along with creating all the required transport nodes, zones, edge clusters, profiles, and routing stuff so that we can get everything ready to have workloads run in NSX-T!
