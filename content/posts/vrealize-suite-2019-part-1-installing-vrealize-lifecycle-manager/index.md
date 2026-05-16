{
  "title": "vRealize Suite 2019 - Part 1: Installing vRealize Lifecycle Manager",
  "date": "2020-01-05T04:18:58",
  "lastmod": "2020-01-05T04:19:01",
  "slug": "vrealize-suite-2019-part-1-installing-vrealize-lifecycle-manager",
  "url": "/posts/vrealize-suite-2019-part-1-installing-vrealize-lifecycle-manager/",
  "draft": false,
  "description": "",
  "wordpress_id": 1636,
  "wordpress_url": "https://ithinkvirtual.com/2020/01/04/vrealize-suite-2019-part-1-installing-vrealize-lifecycle-manager/",
  "featured_image": "/uploads/2020/01/2020-01-04_21-52-12.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "VMware",
    "vRealize Suite",
    "vSphere"
  ],
  "years": [
    "2020"
  ],
  "aliases": [
    "/2020/01/04/vrealize-suite-2019-part-1-installing-vrealize-lifecycle-manager/"
  ],
  "comments": []
}

## Intro

Welcome to Part 1 of my vRealize Suite 2019 Series.  In my [previous post](/2020/01/04/vrealize-suite-2019-series), I went over the gist of what I plan to deploy in my nested Home Lab.  In this post, I will cover the installation of [vRealize Suite Lifecycle Manager](https://docs.vmware.com/en/VMware-vRealize-Suite-Lifecycle-Manager/index.html) using the new vRealize [Easy Installer](https://docs.vmware.com/en/vRealize-Automation/8.0/installing-vrealize-automation-easy-installer/GUID-CEF1CAA6-AD6F-43EC-B249-4BA81AA2B056.html) released with the v8.0 of the solution.

With vRealize Easy Installer, you can:

- Install vRealize Suite Lifecycle Manager
- Install a new instance of vRealize Automation
- Register vRealize Automation with Workspace ONE Access

Please note that as of the time of this writing, the latest version of vRealize Suite Lifecycle Manager is v8.0.1. I will focus on deploying v8.0.0 and eventually cover the upgrade to v8.0.1. Let's get right to it, shall we?

## Obtain and Access the Easy Installer

The vRealize Easy installer can be downloaded from My VMware download page. The media comes in the form of a .iso file. Once the .iso has been downloaded, either mount the ISO or extract its contents and launch the **Installer.exe** file located in the **\vrlcm-ui-installer\win32** directory.

![](/uploads/2020/01/2020-01-04_20-55-02.png)

## Install vRealize Suite Lifecycle Manager

You are required to first define the vCenter Server details, resource location to deploy your appliance, specify resources and then access vRealize Suite Lifecycle Manager. The following steps are outlined in the official [documentation](https://docs.vmware.com/en/VMware-vRealize-Suite-Lifecycle-Manager/8.0/com.vmware.vrsuite.lcm.80.doc/GUID-4D23B793-4EC8-4449-8B3A-34CB1D9A8609.html).

### Procedure

- Click **Install** on the **vRealize Easy Installer**window.
- Click **Next** after reading the introduction.
- Accept the License Agreement and click **Next**.
- Read the **Customer Experience Improvement Program** and select the checkbox to join the program.
- To specify vCenter Server details.
  - Enter the **vCenter Server Hostname**.
  - Enter the **HTTPs Port** number.
  - Enter the **vCenter Server Username**, and **Password.**

![](/uploads/2020/01/2020-01-03_23-21-43-1024x640.png)

- Click **Next** and you are prompted with a Certificate Warning, click **Yes** to proceed.
- You must specify a location to deploy virtual appliances.
  - Expand the vCenter Server tree.
  - Expand to any data center and map your deployment to a specific VM folder.

![](/uploads/2020/01/2020-01-03_23-22-24-1024x640.png)

- Specify a resource cluster
  - Expand the data center tree to an appropriate resource location and click **Next**.

![](/uploads/2020/01/2020-01-03_23-22-42-1024x640.png)

- Store your deployment, allocate a datastore and click **Next**.

![](/uploads/2020/01/2020-01-03_23-23-35-1024x640.png)

- Set up **Network** and **Password configuration**, enter the required fields, and click **Next**.
  - Enter the **NTP Server** for the appliance and click **Next**.  The network configurations provided for all products are a one time entry for your configuration settings. The password provided is also common for all products and you need not enter the password again while you are installing the products.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-03_23-25-10-1024x640.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-03_23-25-50-1024x640.png" alt="" loading="lazy">
</figure>

- Set up vRealize Suite Lifecycle Manager configuration settings.
  - Enter a **Virtual Machine Name**, **IP Address**, and **Hostname**.
  - Click **Next**.  With easy installer, you either import an existing VMware Identity Manager into vRealize Suite Lifecycle Manager or a new instance of VMware Identity Manager can be deployed.  For new VMware Identity Manager installation through easy installer only VMware Identity Manager 3.3.1 is allowed.  This is a mandatory step for a vRealize Suite Lifecycle Manager deployment.  vRealize Automation installation is optional and I am choosing to **Skip** this installation at this time.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-03_23-27-07-1024x640.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-03_23-28-29-1024x640.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-03_23-29-03-1024x640.png" alt="" loading="lazy">
</figure>

- Review the summary page that contains the vRealize Suite Lifecycle Manager, VMware Identity Manager, and vRealize Automation installation details and click **Submit**.

![](/uploads/2020/01/2020-01-03_23-29-42-1024x640.png)

The installation will now begin to deploy vRealize Suite Lifecycle Manager followed by Workspace One Access, formerly known as VMware Identity Manager.  This will take some time to complete but once it's done, you can now login to both applications using the credentials specified in the Easy Installer.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-03_23-30-02-1024x640.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_12-34-08-1024x640.png" alt="" loading="lazy">
</figure>

## Entending Storage Volume

Now, before installing any additional solutions, we first need to increase the storage where vRealize Lifecycle Manager stores the binaries and then import the binaries for each of the solutions we're going to deploy with vRSLCM.  When first logging into vRealize Suite Lifecycle Manager, you'll see the following dashboard.

### Procedure

- Click **Lifecycle Operations**, then click the **gear icon** on the left side to enter the **Settings** menu.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-04_21-52-12-1024x615.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_21-57-43-1024x615.png" alt="" loading="lazy">
</figure>

- Click **System Details**, and you can see that by default, the storage is set to 20GB.
  - I'm going to add 40GB to it so I have enough storage space to house the other product binaries.
- Click **Extend Volume**.
  - Enter the **vCenter Server Host Name**, select the correct **Credential**, and enter the amount in **GB** that you'd like to add and click **Extend**.  Allow some time for the request to complete and refresh the page if necessary.  Once it completed, we can see that the volume has been increased.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-04_21-58-16-1024x615.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_22-04-58-1024x615.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_22-06-42-1024x615.png" alt="" loading="lazy">
</figure>

## Add Product Binaries

Before I can deploy any product other than VMware Identity Manager and vRealize Automation, I need to configure the binary mapping for those additional products.  The two products I mentioned before are already mapped as they come with the Easy Installer.

### Procedure

- From the **Settings** menu, click **Binary Mappings**, then click **Add Binaries**.

![](/uploads/2020/01/2020-01-04_22-27-03-1024x615.png)

- Select your **Location Type**, and provide the **Base Location** path to the shared folder and click **Discover**.
  - There are a few options you can choose from here and I'm going to select **NFS** since I've already placed the binaries in an NFS shared folder.
- Once it's discovered the binaries, select the ones that you want to map and click **Add**.  Allow some time for this to complete and if you'd like, monitor the **Request Status** until you see it has completed.
  - At this time, I'm not selecting any of the v8.0.1 upgrade binaries.  I'll add them at a later time.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-04_22-38-45-1024x615.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_22-41-57-1024x615.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_22-46-25-1024x615.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-04_22-46-47-1024x615.png" alt="" loading="lazy">
</figure>

## Conclusion

In the next one, I'll quickly cover accessing the Workspace One Access (VMware Identity Manager) deployment and configure it so that we can use an Identity Manager account to login to vRealize Suite Lifecycle Manager and the other solutions I'll be deploying in this series.

Well, I hope that you've enjoyed this post and hopefully you'll be back for more.  Thanks for reading!
