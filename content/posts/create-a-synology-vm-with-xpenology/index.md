{
  "title": "Create a Synology VM with XPEnology",
  "date": "2016-04-30T05:44:02",
  "lastmod": "2018-02-10T15:07:52",
  "slug": "create-a-synology-vm-with-xpenology",
  "url": "/posts/create-a-synology-vm-with-xpenology/",
  "draft": false,
  "description": "Create a Synology VM with XPEnology   I’m a huge fan of Synology NAS systems, but I must say, they do often put a gaping hole in your wallet.  Well, fortunately the folks over at XPEnology have created an alternative way for us to create your own Synology devices, whether it be deployed on a…",
  "wordpress_id": 326,
  "wordpress_url": "https://ithinkvirtual.com/2016/04/30/create-a-synology-vm-with-xpenology/",
  "featured_image": "/uploads/2016/04/141209-DS3615xs_enu.jpg",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "Synology",
    "XPEnology"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/04/30/create-a-synology-vm-with-xpenology/"
  ],
  "comments": [
    {
      "author": "Victor H",
      "date": "2017-01-04T15:10:00",
      "content": "<p>I&#8217;ve been following the XPEnology project since beginning of 2013 and I could start first that xpenology.me is just another website belonging to one of the forum members. The website is not updated and all updates appear first on the xpenology.com forum. DSM6 is working but not supported by anyone as it&#8217;s a hack, but it&#8217;s working for me since 2013, so it&#8217;s a great hack 🙂</p>\n"
    },
    {
      "author": "Rob",
      "date": "2016-12-14T21:56:00",
      "content": "<p>I found the web client but how are you creating that virtual machine with exsi 6.0.2 update? thanks</p>\n"
    },
    {
      "author": "Rob",
      "date": "2016-12-14T21:35:00",
      "content": "<p>hi, it looks like you have a very complete tutorial. My problem is I haven&#8217;t ever use vshpere or exsi. In the first part of the tutorial what are you using to create the vm. I have downloaded vpshere hypervisor 6.5, but can&#8217;t find the web client. thanks.</p>\n"
    }
  ]
}

**Create a Synology VM with XPEnology**

I’m a huge fan of Synology NAS systems, but I must say, they do often put a gaping hole in your wallet.  Well, fortunately the folks over at [XPEnology](http://xpenology.me/) have created an alternative way for us to create your own Synology devices, whether it be deployed on a bare-metal system or as a virtual machine.  I currently own a few Synology NAS devices, but I love having the ability to spin up a working VM version quickly and with ease, for use in my nested lab environments.

In this post, I am going to show you how to create your very own Synology VM on VMware ESXi, Workstation, and Fusion hypervisors.  As I mentioned previously, you can also deploy this onto a bare-metal system, but since I do not have a spare system to test this with, I will not cover that deployment.  So without any further hesitation, let’s get to it!

Prerequisites:

- VMware ESXi
- VMware Workstation
- VMware Fusion
- XPEnology files
  - DSM 5.x PAT file – (please note that DSM 6.0 remains unsupported with XPEnology at this time)
  - XPEnoboot 5.x VMDK file
  - Synology Assistant (optional but recommended)
  - NFS Plug-in for VMware VAAI (optional but recommended)
  - Open-VM-tools (optional but recommended)

The type of Synology system that XPEnology emulates is a [DS3615xs](https://www.synology.com/en-us/products/DS3615xs) 12-bay unit.  Let’s begin by heading over to the [XPEnology](http://xpenology.me/downloads/) website and grabbing what we need.  At the time of this writing, the current version of DSM is the newly released DSM 5.2-5967, but the XPEnology team has not yet created an updated bootloader (XPEnoboot) that supports this version.  The current stable version is DSM 5.2.-5644 Update 5 (and can be manually updated to Update 8 at a later time).  The current stable version of XPEnoboot is 5.2-5644.5 so I’ve downloaded the following files…

![2016-04-29_19-13-15](/uploads/2016/04/2016-04-29_19-13-15-1024x523.png)

Now the fun begins, and I will start with the VMware ESXi deployment.  I will be deploying on the newest version of ESXi 6.0 Update 2 via the vSphere Web Client.  For those of you using the vSphere C# client, the directions are the same just the interface is different.

***ESXi 6.0 Update 2***

**Part 1:**

Create a new virtual machine

![2016-04-29_19-43-31](/uploads/2016/04/2016-04-29_19-43-31-300x178.png)

Give it a name and select a folder to place the VM in

![2016-04-29_19-48-30](/uploads/2016/04/2016-04-29_19-48-30-300x178.png)

Select a compute resource

![2016-04-29_19-49-15](/uploads/2016/04/2016-04-29_19-49-15-300x178.png)

Select a storage location

![2016-04-29_19-50-35](/uploads/2016/04/2016-04-29_19-50-35-300x178.png)

Select the proper Compatibility version

![2016-04-29_19-52-01](/uploads/2016/04/2016-04-29_19-52-01-300x178.png)

Select the following Guest OS settings

![2016-04-29_19-55-03](/uploads/2016/04/2016-04-29_19-55-03-300x178.png)

Customize the VM with the following settings, remove the floppy, and select the appropriate network

![2016-04-29_19-57-01](/uploads/2016/04/2016-04-29_19-57-01-300x178.png)

Finish and let it build the “Shell” VM

![2016-04-29_19-58-42](/uploads/2016/04/2016-04-29_19-58-42-300x178.png)

**Part 2:**

Now that the VM has been built, we need to add the XPEnboot VMDK that we downloaded earlier to the VM

Browse to the datastore where you created the VM and upload the XPEnoboot VMDK

![2016-04-29_22-27-40](/uploads/2016/04/2016-04-29_22-27-40-300x145.png)

Once uploaded, we need to add the disk to the VM

![2016-04-29_22-29-15](/uploads/2016/04/2016-04-29_22-29-15-288x300.png) ![2016-04-29_22-29-56](/uploads/2016/04/2016-04-29_22-29-56-300x227.png)![2016-04-29_22-30-58](/uploads/2016/04/2016-04-29_22-30-58-288x300.png)

At this point, I also like to add an additional SCSI disk which will be used as an NFS volume, or iSCSI LUN.  You can make this any size you like but for the purposes of this post, I’m just going to add a simple 50GB Thin Provisioned disk. The 16GB disk we created with the VM will be used to install application packages (i.e. – VMware Tools, etc.)

Keep in mind that this is a 12-bay device, so you can technically add 10 more disks to fill all the drive bays

![2016-04-29_22-37-21](/uploads/2016/04/2016-04-29_22-37-21-288x300.png)

Now power-on the VM and open the console window.  Keep an eye on the window for the IP address assigned to the VM.  You can connect to this IP using a web browser instead of using the Synology Assistant to detect and connect to it.

![2016-04-29_22-51-55](/uploads/2016/04/2016-04-29_22-51-55-300x245.png)

Open you favorite web browser and type in the IP address of the VM, and hit enter.  This will connect you to the VM’s Synology Web UI

Click the Set up button, then click the Manual Install link and browse for the DSM .pat file we downloaded earlier. Then click the Install Now button

![2016-04-29_23-03-38](/uploads/2016/04/2016-04-29_23-03-38-285x300.png)![2016-04-29_23-04-27](/uploads/2016/04/2016-04-29_23-04-27-300x286.png) ![2016-04-29_23-06-12](/uploads/2016/04/2016-04-29_23-06-12-300x286.png)

This will prompt you that it will erase all data on all disks, ***including*** the XPEnoboot disk we uploaded and attached earlier.  Note, I have experienced failures at this point and received a message that the .pat file may be corrupt.  In the even this also happens to you, please use this alternative XPEnology download [link](https://download.xpenology.fr/).

![2016-04-29_23-11-55](/uploads/2016/04/2016-04-29_23-11-55-300x287.png)

Once complete, the VM will be rebooted.  But since we erased all of the disks during installation, the VM will fail to boot properly and this is expected

![2016-04-29_23-17-15](/uploads/2016/04/2016-04-29_23-17-15-300x286.png) ![2016-04-29_23-17-36](/uploads/2016/04/2016-04-29_23-17-36-300x196.png)

Power off the VM and access the datastore that the VM is stored on.  Delete the XPEnoboot VMDK then re-upload the VMDK that we originally downloaded

![2016-04-29_23-19-41](/uploads/2016/04/2016-04-29_23-19-41-300x152.png) ![2016-04-29_22-27-40](/uploads/2016/04/2016-04-29_22-27-40-300x145.png)

Power on the VM and select the Install/Upgrade option

![2016-04-29_23-24-42](/uploads/2016/04/2016-04-29_23-24-42-300x196.png)

When it finishes it boot, this time you will notice that it will not display the IP address we saw the last time.  The IP should have remained the same but I’m going to use the Synology Assistant to detect it and help me connect since my web browser was not connecting to the same address

![2016-04-29_23-25-50](/uploads/2016/04/2016-04-29_23-25-50-300x245.png) ![2016-04-29_23-44-17](/uploads/2016/04/2016-04-29_23-44-17-300x262.png)

Now we are presented with the Web UI screen and we can login with admin and a blank password

![2016-04-29_23-45-29](/uploads/2016/04/2016-04-29_23-45-29-300x300.png)

Click next and give the Synology VM a name and change the admin user password or enter a new username and password then click Next

![2016-04-29_23-48-13](/uploads/2016/04/2016-04-29_23-48-13-300x300.png) ![2016-04-29_23-50-20](/uploads/2016/04/2016-04-29_23-50-20-300x300.png)

In order to prevent updates from installing automatically and possibly breaking the boot up of the Synology VM, I chose “Download DSM updates but let me choose whether to install them” and clicked next

![2016-04-29_23-52-26](/uploads/2016/04/2016-04-29_23-52-26-300x300.png)

I also chose to skip the “Set up QuickConnect”

![2016-04-29_23-53-44](/uploads/2016/04/2016-04-29_23-53-44-300x300.png)![2016-04-29_23-54-26](/uploads/2016/04/2016-04-29_23-54-26-300x300.png)

And….You’re Done!  You now have a fully functional Synology virtual machine.  You can feel free to add additional disks or what have you.

![2016-04-29_23-57-16](/uploads/2016/04/2016-04-29_23-57-16-1024x498.png)

At this point, I like to go ahead and install the Open-VM-Tools package so that I can use the VMware tools to gracefully power off the VM as needed.  To do so, you will need to have downloaded the package from the XPEnology website.

Open Package Center, then click the Settings button.

![2016-04-30_0-02-06](/uploads/2016/04/2016-04-30_0-02-06-300x170.png)

On the General tab, set the Trust Level to Any Publisher and click OK

![2016-04-30_0-03-04](/uploads/2016/04/2016-04-30_0-03-04-300x250.png)

Back in the Package Center, click Manual Install.  Browse to the package and click Next

![2016-04-30_0-04-51](/uploads/2016/04/2016-04-30_0-04-51-300x216.png)

Since we have yet to create a volume, it will prompt you to click OK to launch Storage Manager and create a volume to install the package on.

![2016-04-30_0-07-21](/uploads/2016/04/2016-04-30_0-07-21-300x75.png)

In Storage Manager, click Volume the click Create.  Keep the default of “Quick”, Next, select Disk 3, Next, OK to the warning message, Yes for disk check, Next, Apply….Done!

![2016-04-30_0-08-57](/uploads/2016/04/2016-04-30_0-08-57-150x150.png) ![2016-04-30_0-11-08](/uploads/2016/04/2016-04-30_0-11-08-150x150.png) ![2016-04-30_0-12-02](/uploads/2016/04/2016-04-30_0-12-02-150x150.png) ![2016-04-30_0-13-10](/uploads/2016/04/2016-04-30_0-13-10-150x150.png) ![2016-04-30_0-14-49](/uploads/2016/04/2016-04-30_0-14-49-150x150.png) ![2016-04-30_0-15-13](/uploads/2016/04/2016-04-30_0-15-13-150x150.png)

Now, repeat step 3 above, click Apply, and you will have VMware tools installed.

![2016-04-30_0-17-23](/uploads/2016/04/2016-04-30_0-17-23-300x170.png)

Wow, that seemed like an awful lot of steps, but it really wasn’t all that much.  In the next sections, I will just go over the deployment of the “Shell VMs”  and the steps to add the XPEnoboot VMDK to the VMs in VMware Workstation and VMware Fusion as the rest of the post-boot setup steps are the same.

***VMware Workstation Pro 12.1.1***

**Part 1:**

Create the Shell VM…

![2016-04-30_1-07-28](/uploads/2016/04/2016-04-30_1-07-28-300x279.png) ![2016-04-30_1-07-43](/uploads/2016/04/2016-04-30_1-07-43-300x279.png) ![2016-04-30_1-08-01](/uploads/2016/04/2016-04-30_1-08-01-300x279.png) ![2016-04-30_1-08-17](/uploads/2016/04/2016-04-30_1-08-17-300x279.png) ![2016-04-30_1-10-34](/uploads/2016/04/2016-04-30_1-10-34-300x279.png) ![2016-04-30_1-10-46](/uploads/2016/04/2016-04-30_1-10-46-300x279.png) ![2016-04-30_1-11-05](/uploads/2016/04/2016-04-30_1-11-05-300x279.png) ![2016-04-30_1-11-47](/uploads/2016/04/2016-04-30_1-11-47-300x279.png) ![2016-04-30_1-12-14](/uploads/2016/04/2016-04-30_1-12-14-300x279.png) ![2016-04-30_1-12-27](/uploads/2016/04/2016-04-30_1-12-27-300x279.png) ![2016-04-30_1-12-39](/uploads/2016/04/2016-04-30_1-12-39-300x279.png) ![2016-04-30_1-13-17](/uploads/2016/04/2016-04-30_1-13-17-300x279.png) ![2016-04-30_1-13-40](/uploads/2016/04/2016-04-30_1-13-40-300x279.png) ![2016-04-30_1-15-42](/uploads/2016/04/2016-04-30_1-15-42-300x279.png)

**Part 2:**

Add the XPEnoboot VMDK to the VM…

![2016-04-30_1-17-08](/uploads/2016/04/2016-04-30_1-17-08-300x165.png)

![2016-04-30_1-18-32](/uploads/2016/04/2016-04-30_1-18-32-300x270.png) ![2016-04-30_1-18-46](/uploads/2016/04/2016-04-30_1-18-46-300x263.png) ![2016-04-30_1-19-02](/uploads/2016/04/2016-04-30_1-19-02-300x263.png) ![2016-04-30_1-19-14](/uploads/2016/04/2016-04-30_1-19-14-300x263.png) ![2016-04-30_1-19-54](/uploads/2016/04/2016-04-30_1-19-54-300x263.png) ![2016-04-30_1-21-00](/uploads/2016/04/2016-04-30_1-21-00-300x270.png)

![2016-04-30_1-21-20](/uploads/2016/04/2016-04-30_1-21-20-300x165.png)

Power on the VM and continue with same process outlined above for ESXi deployment.  Use the Synology Assistant to find and connect as the VM may not display the IP address right away.

***VMware Fusion Pro 8.1.1***

**Part 1:**

Create the Shell VM…

![2016-04-30_09-21-41](/uploads/2016/04/2016-04-30_09-21-41-300x250.png) ![2016-04-30_09-22-04](/uploads/2016/04/2016-04-30_09-22-04-300x250.png) ![2016-04-30_09-22-36](/uploads/2016/04/2016-04-30_09-22-36-300x250.png) ![2016-04-30_09-22-58](/uploads/2016/04/2016-04-30_09-22-58-300x250.png) ![2016-04-30_09-24-14](/uploads/2016/04/2016-04-30_09-24-14-300x263.png)

**Part 2:**

Add the XPEnoboot VMDK to the VM…

![2016-04-30_09-25-28](/uploads/2016/04/2016-04-30_09-25-28-300x182.png) ![2016-04-30_09-26-35](/uploads/2016/04/2016-04-30_09-26-35-300x165.png) ![2016-04-30_09-27-02](/uploads/2016/04/2016-04-30_09-27-02-300x182.png) ![2016-04-30_09-29-08](/uploads/2016/04/2016-04-30_09-29-08-300x86.png) ![2016-04-30_09-30-49](/uploads/2016/04/2016-04-30_09-30-49-300x158.png) ![2016-04-30_09-31-51](/uploads/2016/04/2016-04-30_09-31-51-300x261.png) ![2016-04-30_09-32-41](/uploads/2016/04/2016-04-30_09-32-41-300x86.png) ![2016-04-30_09-33-14](/uploads/2016/04/2016-04-30_09-33-14-300x172.png) ![2016-04-30_09-34-58](/uploads/2016/04/2016-04-30_09-34-58-300x144.png) ![2016-04-30_09-36-10](/uploads/2016/04/2016-04-30_09-36-10-300x219.png) ![2016-04-30_09-36-45](/uploads/2016/04/2016-04-30_09-36-45-300x200.png) ![2016-04-30_09-37-39](/uploads/2016/04/2016-04-30_09-37-39-300x251.png)

Power on the VM and continue with same process outlined above for ESXi deployment.  Use the Synology Assistant to find and connect as the VM may not display the IP address right away.

Now you should all feel confident in creating your own Synology VM systems for whatever your use case may be and hopefully you will all love using Synology products as much as I do.  If you would like the true experience, I’d recommend purchasing a real system.  But in the interim, this will give you a way to create your own and play around with it.

Keep in mind that when updates are released, it is always wise to first check on the XPEnology site and/or forum to see if the updates break anything as sometimes they will cause the boot process to break since the XPEnoboot cannot support it yet.  Usually you are safe to update as long as the update is within the same DSM version, but consult the site/forum first as I am not responsible for any upgrade impacts.

Well, I hope that you all have enjoyed this read/guide and come back for more!

And giving credit where it is due, I’d like to give a shout out to [Erik Bussink](https://twitter.com/erikbussink) as his [guide](http://www.bussink.ch/?p=1672) is what inspired me to write this updated guide for all of you!

Cheers!

-virtualex-
