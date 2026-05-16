{
  "title": "vSphere…Synology…NFS v4.1",
  "date": "2018-01-01T03:39:14",
  "lastmod": "2018-02-10T13:59:35",
  "slug": "vsphere-synology-nfs-v4-1",
  "url": "/posts/vsphere-synology-nfs-v4-1/",
  "draft": false,
  "description": "Welcome, and thanks for visiting my blog! In this post, I am going to cover how to enable NFS v4.1 on a Synology device and then mount and NFS v4.1 datastore in VMware vSphere 6.5.  By default, Synology devices support NFS v4 natively, and although they can also support NFS v4.1, it is not enabled. …",
  "wordpress_id": 1062,
  "wordpress_url": "https://ithinkvirtual.com/2017/12/31/vsphere-synology-nfs-v4-1/",
  "featured_image": "/uploads/2017/12/NFS41.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "NFS",
    "Synology",
    "VMware",
    "vSphere"
  ],
  "years": [
    "2018"
  ],
  "aliases": [
    "/2017/12/31/vsphere-synology-nfs-v4-1/"
  ],
  "comments": []
}

Welcome, and thanks for visiting my blog!

In this post, I am going to cover how to enable NFS v4.1 on a Synology device and then mount and NFS v4.1 datastore in VMware vSphere 6.5.  By default, Synology devices support NFS v4 natively, and although they can also support NFS v4.1, it is not enabled.  Well, not to worry because I am going to show you just how to enable the feature on your device.

NFS v4 and v4.1 have been around for quite a few years but it has not taken off then way NFS v3 did way back when.  There were some major flaws pointed out with NFSv4 so NFSv4.1 was created to rectify those flaws, and VMware was one of the first major companies to adopt and support the new Network File System.  But unless your storage device supported the newer NFS versions, you would be stuck mounting NFSv3 volumes by default.

In this demo, I will be using my new replacement Synology DiskStation DS415+ and my homelab “datacenter” running the latest version vSphere 6.5.  So let’s jump right in!

Using a terminal application like PuTTY, connect to your Synology device via SSH using an admin user account.  This can be the default “admin” account and any new user account with Administrator privileges.  Once connected enter the following command to change the directory:

```bash
cd /usr/syno/etc/rc.sysv
```

Once in this directory, run the following command (enter the account password if prompted):

```bash
sudo cat /proc/fs/nfsd/versions
```

This will show us the current NFS version currently enabled and supported by the Synology device.

![](/uploads/2017/12/2017-12-31_21-44-10.png)

We can see that all versions prior to 4.1 have a “+” sign next to them and 4.1 has a “-” sign next to it.  Let’s change that!

In order to change this, we will need to edit a shell (S83nfsd.sh) file using “vi”.  Run the following command to open the file with VI Editor:

```bash
sudo vi S83nfsd.sh
```

![](/uploads/2017/12/2017-12-31_18-09-32.png)

This will open the shell file and will place the cursor at Line 1, Character 1 as depicted in the following screenshot.

![](/uploads/2017/12/2017-12-31_18-10-04.png)

Navigate down to line 90 using the down arrow and you will see the following line of text.

![](/uploads/2017/12/2017-12-31_18-10-25.png)

This is where the magic happens!  To edit the file now, press the “I” key on your keyboard to initiate an “Insert” then add the following to the end of the text so the line looks like the following screenshot.

```text
-V 4.1
```

![](/uploads/2017/12/2017-12-31_18-10-53.png)

To commit and save this change, first press the Esc key.  Next type the following command and hit “Enter” to write and then quit vi editor.

```text
:wq
```

![](/uploads/2017/12/2017-12-31_18-11-07.png)

Next, we need to restart the NFS service.  To do so enter the following command:

```bash
sudo ./S83nfsd.sh restart
```

If we again run the following command, we will see that there is now a “+” sign next to 4.1.  Hooray!

```bash
sudo cat /proc/fs/nfsd/versions
```

![](/uploads/2017/12/2017-12-31_18-12-56.png)

Now that we have enabled NFSv4.1 functionality on your storage device, let’s go ahead and mount an NFS volume to our hosts in vSphere.

I have enabled NFS and NFS v4 support then created the following shares with assigned permissions on my device, and am going to mount the ISOs share first in this example by issuing a command via PowerCLI.  We can also see that I do not have any NFS mounts currently in my environment

![](/uploads/2017/12/2017-12-31_22-01-38-300x196.png) ![](/uploads/2017/12/2017-12-31_20-51-35-300x196.png) ![](/uploads/2017/12/2017-12-31_20-50-36-300x196.png)

I’ve launched PowerCLI and connected to my vCenter Server using the **Connect-VIServer** cmdlet then issued the following command:

```powershell
Get-VMHost | New-Datastore -Nfs -FileSystemVersion '4.1' -Name SYN-NFS04-ISOs -Path "/volume3/NFS04-ISOs" -NfsHost DS415 -ReadOnly
```

****Note:*** an important argument here in the “-FileSystemVersion”.  If I do not specify the version, it will assume version 3.0 by default.*

![](/uploads/2017/12/2017-12-31_20-54-07-1024x422.png)

If I go back and look at my datastores via the Web Client, I can see that my new NFS 4.1 datastore has been mounted to each one of my ESXi hosts. Nice!

![](/uploads/2017/12/2017-12-31_20-54-43-1024x669.png)

***Bonus:*** If I’d like to easily remove this datastore from all of my hosts, I can issue the following command via PowerCLI.

```powershell
Get-VMHost | Remove-Datastore -Datastore SYN-NFS04-ISOs -Confirm:$false
```

![](/uploads/2017/12/2017-12-31_20-56-43-1024x422.png)

Now I can see that the host has been removed successfully!

![](/uploads/2017/12/2017-12-31_21-01-40-1024x669.png)

Well, that about wraps this one up.  I hope that this has been useful and informative for you and I’d like to thank you for reading!  Until next time!

-virtualex-
