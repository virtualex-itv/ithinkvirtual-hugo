{
  "title": "NSX-T Home Lab - Part 6: Upgrading NSX-T",
  "date": "2019-03-22T00:00:25",
  "lastmod": "2019-03-22T01:14:15",
  "slug": "nsx-t-home-lab-part-6-upgrading-nsx-t",
  "url": "/posts/nsx-t-home-lab-part-6-upgrading-nsx-t/",
  "draft": false,
  "description": "",
  "wordpress_id": 1586,
  "wordpress_url": "https://ithinkvirtual.com/2019/03/21/nsx-t-home-lab-part-6-upgrading-nsx-t/",
  "featured_image": "/uploads/2019/03/2019-03-21_18-44-33.png",
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
    "vSphere"
  ],
  "years": [
    "2019"
  ],
  "aliases": [
    "/2019/03/21/nsx-t-home-lab-part-6-upgrading-nsx-t/"
  ],
  "comments": []
}

## Intro

Welcome to Part 6 of my NSX-T Home Lab series.  In my [previous](/2019/02/19/nsx-t-home-lab-part-5-configuring-nsx-t-networking/) post, I covered how to configure NSX-T networking to be able to start migrating and running workloads on the NSX-T fabric. In this post, I am going to cover the process of upgrading to the newly released version of NSX-T 2.4. Are you excited? Good!... So am I! Let's jump right in!

## Prerequisites

### Upgrade Checklist

Please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-E35506A7-8050-482A-BABA-F356D2AC3B65.html) to follow best practices for upgrading NSX-T. You must follow the prescribed order and upgrade the hosts, NSX Edge cluster, NSX Controller cluster, and Management plane.

### Operational Impact

The duration for the NSX-T Data Center upgrade process depends on the number of components you have to upgrade in your infrastructure. It is important to understand the operational state of NSX-T Data Center components during an upgrade, such as when some hosts have been upgraded, or when NSX Edge nodes have not been upgraded.  
  
The upgrade process is as follows:

Hosts > NSX Edge cluster > Management plane.
Please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-4CD72B28-0EF3-49F8-9F85-556A37FCE206.html) for more information.

### Supported Hypervisor Upgrade Path

The supported hypervisor upgrade paths for the NSX-T Data Center product versions. Adhere to the following upgrade paths for each NSX-T Data Center release version.

- NSX-T Data Center 2.3 > NSX-T Data Center 2.4.
- NSX-T Data Center 2.2 > NSX-T Data Center 2.3 > NSX-T Data Center 2.4.
- NSX-T Data Center 2.1 > NSX-T Data Center 2.3 > NSX-T Data Center 2.4

Please see the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-FAFED150-0652-4B7D-9B5E-5F655C22FE48.html) for more information.

### Upgrade ESXi Hosts

If your ESXi host is unsupported, manually upgrade your ESXi host to the supported version. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-A9A8EF26-08C9-4D33-90E9-5232A57326F1.html) for more information. Since my hosts are already running the latest version of ESXi 6.7 U1, I am good to continue.

### Download the NSX-T Upgrade Bundle

The upgrade bundle contains all the files to upgrade the NSX-T Data Center infrastructure. Before you begin the upgrade process, you must download the correct upgrade bundle version.  
  
You can also navigate to the upgrade bundle and save the URL. When you upgrade the upgrade coordinator, paste the URL so that the upgrade bundle is uploaded from the VMware download portal. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-68A09AEC-D270-4172-830A-B7D971047DA9.html) for more information.

## Upgrading NSX-T Data Center

After you finish the prerequisites for upgrading, your next step is to update the upgrade coordinator to initiate the upgrade process.  
  
After the upgrade, based on your input, the upgrade coordinator updates the hosts, NSX Edge cluster, NSX Controller cluster, and Management plane.
  
You can use REST APIs to upgrade your NSX-T Data Center appliance. Identify the NSX-T Data Center version you are upgrading to. Refer to the API guide with your product version in [code.vmware.com](https://code.vmware.com/apis?socv=0&numPerPage=159&sorter=pv&products=TlNYLVQ7Mi4zLE5TWC1UOzIuMixOU1gtVDsyLjEuMCxOU1gtVDsyLjEsTlNYLVQ7Mi4wLE5TWC1UOzEuMQ==) to find the latest upgrade-related APIs.  
  
See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-3B986F37-94FE-4CAC-B4AD-9B55D8FE1EC2.html) for more information.

### Update the Upgrade Coordinator

See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-D54B64CF-9242-4D68-85BD-CBB566EFC1FE.html) for more information. From your browser, log in with admin privileges to you NSX Manager and navigate to **System > Utilities > Upgrade** then click **Proceed to Upgrade**.

![](/uploads/2019/03/2019-03-20_14-42-55.png)

Browse to the upgrade bundle .mub file that was downloaded as part of the prerequisites steps and then click **Upload**.

![](/uploads/2019/03/2019-03-20_14-44-18.png)
![](/uploads/2019/03/2019-03-20_16-14-28.png)

The upload may take up to 20 minutes or more to complete. Once the upload has completed, click **Begin Upgrade**. Accept the **EULA**, then click **Continue** to begin the upgrade.

![](/uploads/2019/03/2019-03-21_9-53-59.png)
![](/uploads/2019/03/2019-03-21_9-54-33.png)
![](/uploads/2019/03/2019-03-21_12-57-39.png)

Once, the upgrade completes, click the **Run Pre Checks** link. All pre checks should come back green but since this is a demo nested lab, I am expecting to see some sort of warning as evident in the image below. The reason for this warning is because I've configured my current NSX Manager VM with 4 vCPUs and 16GB RAM, sufficient for my lab and aligns with the "small" deployment. I could've left it with 2 vCPUs and 8GB RAM satisfying the "extra small" deployment model had I wanted to leave it alone. In a production environment, you'd want to deploy this at a minimum with a "medium" deployment model which requires 6 vCPUs and 24GB RAM.

![](/uploads/2019/03/2019-03-21_13-55-49.png)
![](/uploads/2019/03/2019-03-21_13-20-33.png)
![](/uploads/2019/03/2019-03-21_13-57-59.png)

At this point, I'm ready to move on to the next part to begin upgrading the NSX-T VIBs on my ESXi hosts. Click **Next** to proceed.

### Upgrade Hosts

This part is fairly simple. Just click the blue **Start** button to begin upgrading the hosts. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-377CFB74-5333-4417-A609-FAD4542C118C.html) for more information.

![](/uploads/2019/03/2019-03-21_14-00-19.png)
![](/uploads/2019/03/2019-03-21_14-01-42.png)
![](/uploads/2019/03/2019-03-21_18-05-54.png)

Once Complete click **Next**, to proceed to the next phase in the upgrade process...upgrading the Edges.

### Upgrade NSX Edge Cluster

Here, it will be the same process as before. Click the blue **Start** button to begin upgrading the Edge Cluster. Once complete, click **Next** to move onto the next phase...upgrading the Controller Nodes. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-B2B7B0C1-E2B4-46F6-9DA7-CC807C219E82.html) for more information.

![](/uploads/2019/03/2019-03-21_18-13-34.png)

### Upgrade NSX Controller Cluster

This is by far the easiest part of the upgrade because...well...there's nothing to do! Beginning with NSX-T 2.4.0, the Controllers are migrated into the NSX Manager. But just for informational purposes, you should see the following screen. Click **Next** to continue to the final part of the upgrade process...upgrading the Management plane.

![](/uploads/2019/03/2019-03-21_18-14-37.png)

### Upgrade Management Plane

As was done with each previous step, simply click the blue Start button to begin the upgrade. You'll then be presented with another window, which we go ahead and click Start to kick off the upgrade. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-1E70CEB1-340C-4880-8B03-BEECB641E817.html) for more information.

This process will take about 10-15 minutes as it will upgrade the Manager Appliance VM then reboot it. It's possible that it may look like the upgrade fails but just sit tight as the Manager UI will eventually become inaccessible. Let the VM reboot and allow about 10 minutes for services to start. Afterward, go ahead an log into the NSX Manager UI and you should now be presented with the new simplified NSX-T 2.4.0 interface.

![](/uploads/2019/03/2019-03-21_18-18-34.png)
![](/uploads/2019/03/2019-03-21_18-44-33.png)

Having a single Manager Appliance is sufficient for my nested lab but it a production environment, you will want to follow this [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-1E70CEB1-340C-4880-8B03-BEECB641E817.html) (Step 12) to deploy two more manager appliances and cluster the 3 together. In the image above, you can see the highlighted warning about this. If you are not familiar with the process, you can also follow this official [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/installation/GUID-FA0ABBBD-34D8-4DA9-882D-085E7E0D269E.html).

## Post Upgrade Tasks

### Verify the Upgrade

After you upgrade NSX-T Data Center, you can verify whether the versions of the upgraded components have been updated. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-F8749F44-EF43-46AE-872C-25A80B6055FD.html) for more information. Navigate to **System > Upgrade** and confirm that all components are running 2.4.x.

![](/uploads/2019/03/2019-03-21_19-32-21.png)

### Delete NSX Controllers

After successfully upgrading to NSX-T Data Center 2.4, you can delete the NSX-T Data Center 2.3 NSX Controllers. See the [documentation](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/2.4/upgrade/GUID-D946F58F-BFB2-4F8E-A979-4C07393299E8.html) for more information. Simply locate the NSX Controller VM(s) inside your vCenter Server and power them off, then right-click on them and select **Delete from Disk**. Click **Yes** to confirm.

![](/uploads/2019/03/2019-03-21_19-44-35.png)

That about wraps up this post. In my next post, I will go over the process of completely uninstalling NSX-T so stay tuned!
