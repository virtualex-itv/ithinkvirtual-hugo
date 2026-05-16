{
  "title": "VMware Software Manager: The Good...The Bad...The Alternative!",
  "date": "2018-03-07T18:00:51",
  "lastmod": "2019-01-17T22:57:48",
  "slug": "vmware-software-manager-the-good-the-bad-the-alternative",
  "url": "/posts/vmware-software-manager-the-good-the-bad-the-alternative/",
  "draft": false,
  "description": "",
  "wordpress_id": 1210,
  "wordpress_url": "https://ithinkvirtual.com/2018/03/07/vmware-software-manager-the-good-the-bad-the-alternative/",
  "featured_image": "/uploads/2018/03/VSM_BG.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "CentOS",
    "How-To's",
    "NFS",
    "Synology",
    "VMHGFS",
    "VMware",
    "VMware Fusion",
    "VMware Software Manager",
    "VMware Workstation",
    "VSM",
    "vSphere"
  ],
  "years": [
    "2018"
  ],
  "aliases": [
    "/2018/03/07/vmware-software-manager-the-good-the-bad-the-alternative/"
  ],
  "comments": []
}

In this post, I am going to discuss a little, "not-so-well-known" utility, called [VMware Software Manager](https://www.vmware.com/products/software-manager.html).  This little "beast" was first released as v1.0 back on 2015-03-12, and its most current release, v1.5, came out on 2016-08-25.  So as you can see, it's been quite a while since this tool has seen a new update release.  The problem now is that this utility seems to have been forgotten and/or neglected by VMware, but I will get into more of that a little later.  Let's start off with the positive stuff.

***The Good:***

The VMware Software Manager allowed valid VMware-account holders the ability to download various software, such as ESXi or vCenter server, quickly and easily.  The installation was a breeze, the interface was clean and downloading software was effortless.  It basically just worked flawlessly!  The new software was readily available for download shortly after it was announced/released since this utility would read configuration files to see what software is available from the VMware repository and then provided that software for download.

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_20-35-20-150x150.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_20-36-59-150x150.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_20-38-38-150x150.png" alt="" loading="lazy">
</figure>

So, having said that, what could possibly be wrong with this thing?  Let's continue...

***The Bad:***

My main gripe with this utility was that support was only community-based, so if you had issues, you could forget about raising an official SR with support.  You had to rely patiently on the VMTN community and hope that users were knowledgeable enough and willing to help out.  Not saying anything bad about the community though, it's a great forum full of some really smart people and it provides a wealth of information.

As I mentioned earlier, when this thing worked...it just plain WORKED!  Then, vSphere 6.0U3A was released with some bad/corrupt or missing files and upon launching the utility, it would simply hang at login or error out due to the missing files not being available! (Shhhh!..someone never updated the configuration files... ¯\_(ツ)_/¯  )  There is a [thread](https://communities.vmware.com/thread/553547) over on the VMTN community that myself and others have contributed to and [another](https://communities.vmware.com/thread/568541) describing this issue and a workaround method to ultimately get you to log in again.  This involved looking at log files to find which missing file was causing the error, then editing the configuration file to remove the missing files, and it was a major pain!

Lastly, it's become extremely out of date and it seems as if VMware has completed forgotten about and/or decided to neglect and give up on it as there has not been any new software available for download in at least 6 months.  It's also possible that the original responsible for this thing disbanded or moved onto other roles...who really knows?  Luckily, a friend and fellow community/vExpert member has provided a solution!

***The Alternative:***

Fellow vExpert, [Edward Haletky aka Texiwill](https://twitter.com/Texiwill), has created a Linux-based port of the utility, titled "***VSM***", which he updates almost daily to add new software and simply improve the appliance and it runs on an RHEL type distro like CentOS.  You can hit the ground running with this appliance in about 30 mins or less.  I have been fortunate enough to serve as a beta tester for him and have been doing so since he released v0.95, just shortly after the initial public launch.  At the time of this writing, the most recent release was v3.7.7 but has now been updated to the newest 4.5.3.  Screenshots may reflect previous versions.

![](/uploads/2018/03/2018-03-07_16-26-29-1024x394.png)

***Well...How do you get it?***

In this post, I am going to cover how to install this bad-boy on a CentOS 7 minimal installation on ESXi using NFS, and on VMware Workstation leveraging the "Shared Folders" feature using VMHGFS.  Another vExpert, [Michael White](https://twitter.com/mwVme), has a similar [post](https://notesfrommwhite.net/2017/10/30/installing-the-linux-vmware-software-manager-tool/) on setting up this appliance and using SMB/CIFS for storing the downloaded software.  Let's get to it, shall we!

Prerequisites:

- CentOS 7 x64 (Minimal) w/ open-vm-tools installed
- a non-root user account
- NFS storage or Local Storage (if running this on VMware Workstation/Fusion)

I will assume that you already have a basic installation of CentOS 7 running, or know how to set up a minimal installation, so that process is out of scope for this post.

If you plan on running this on VMware Workstation/Fusion, run the following command to install the prerequisites needed for installing VMware Tools to get the vmhgfs driver for Shared Folders support.

```bash
sudo yum install -y perl gcc binutils make fuse kernel-headers kernel-devel net-tools policycoreutils-python
```

Otherwise, if you plan on using NFS to store the software, run the following command to install the NFS utilities.

```bash
sudo yum install -y nfs-utils
```

***VMware Tools Installation:***

<aside class="info-block"><p>Enables vmhgfs driver support for Shared Folders on VMware Workstation or VMware Fusion</p></aside>

I will be installing the latest version of VMware Tools, version 10.2.0.  This can be obtained [here](https://my.vmware.com/web/vmware/details?productId=614&downloadGroup=VMTOOLS1020).  Extract the .zip and attach the linux.iso to your CentOS VM in Workstation or Fusion.  Once connected, do the following.

Make a directory to mount the cdrom to.

```bash
sudo mkdir /mnt/cdrom
```

Mount the cdrom to this new directory.

```bash
sudo mount /dev/cdrom /mnt/cdrom
```

With the cdrom now mounted, let take a look at whats on the .iso

```bash
sudo ls /mnt/cdrom
```

We can see the compressed file that we will need to extract

![](/uploads/2018/03/2018-03-04_19-51-43-1024x373.png)

Extract/Uncompress this file by running the following.  This is going to extract the file to my current working directory, ***$HOME***

```bash
sudo tar zxpf /mnt/cdrom/VMwareTools-10.2.0-7253323.tar.gz
```

When that completes, we can see what was extracted by running

```bash
ls
```

![](/uploads/2018/03/2018-03-04_19-53-08-1024x373.png)

At this point, we are done with the .iso and can unmount it by running.

```bash
sudo umount /dev/cdrom
```

Now, let's navigate to the extracted folder and see what we've got.

```bash
cd vmware-tools-distrib/
ls
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_19-54-02-1024x373.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_19-54-19-1024x373.png" alt="" loading="lazy">
</figure>

The Perl script is what we're looking for here to install VMware Tools.  This will uninstall "*open-vm-tools*" if that is already installed on this machine.  Let's go ahead and run it.

```bash
sudo ./vmware-install.pl
```

Proceed to answer all the questions asked and select all of the defaults until the installation completes.

<aside class="info-block"><p>Optional: If you&#x27;d prefer to bypass the questions and force-install with all defaults run the following instead</p></aside>
```bash
sudo ./vmware-install.pl --force-install --default
```
<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_19-55-16-1024x373.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_19-55-35-1024x373.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_20-13-08-1024x373.png" alt="" loading="lazy">
</figure>

This completes the VMware Tools installation and not the vmhgfs driver is installed.  Onto the good stuff!

***VSM Installation:***

Texiwill has provided an installation [script](https://github.com/Texiwill/aac-lib/blob/master/vsm/install.sh) on his GitHub page which will take care of the installation and its prerequisites. This is the preferred installation method so I'd advise that you download this script, and run it.  You'll first have to make the script "executable" by running

```bash
chmod +x install.sh
```

For those who prefer the manual approach, you'll first need to install "*wget*", then run the following commands to install the utility.

<aside class="info-block"><p>please change timezone location to your respective location</p></aside>
```bash
sudo yum install -y wget
mkdir aac-base
cd aac-base
wget -O aac-base.install https://raw.githubusercontent.com/Texiwill/aac-lib/master/base/aac-base.install
chmod +x aac-base.install
./aac-base.install -u America/New_York
sudo ./aac-base.install -i vsm America/New_York
```

Congrats!  You've successfully installed the utility.  Now to configure it for use.

By default, the VSM script will save the config file (*.vsmrc*) to "***$HOME***".  It will also save the ***index.html*** and ***credstore*** files in "***/tmp/vsm***".  I highly recommend you create an alternate directory to store these files in if you are using a system that has multiple users or change it to save them in the users ***$HOME*** directory.  Again, this is optional and can be skipped, but if you'd like to do so, run the following

```bash
mkdir /tmp/my_vsm
```

***VSM Initial Configuration:***

The last step before you can use the VSM script utility is to configure it.  To list the all available parameters, execute the script with the help parameter.

```bash
vsm.sh -h
```

Based on the help info, the required parameters to set are:

- -v | --vsmdir VSMDirectory (this will be the "my_vsm" directory we created earlier)
- --repo repopath (this will be the path to the directory we'll create to save our download)

When first executing the script utility, you will be required to enter valid MyVMware credentials which will be saved to the configuration file.

Let's go ahead and create our repo directories first.  Feel free to use my examples or anything else you'd like.  We will also use the same steps mentioned about to take ownership of these directories and then mount our physical storage to the newly created mount point directory.

<aside class="info-block"><p>Be sure to enable &quot;Shared Folders&quot; on Workstation or Fusion and select the shared folder to mount it to the VM. Commands may be different from screenshots as I&#x27;ve updated some commands.</p></aside>

For VMHGFS:

```bash
sudo mkdir -pvm 755 /mnt/vmhgfs/depot/content
sudo chown -R <non-root_username>.<non-root_username> /mnt/vmhgfs
```

![](/uploads/2018/03/2018-03-07_7-28-50-1024x373.png)

For NFS:

```bash
sudo mkdir -pvm 755 /mnt/nfs/depot/content
sudo chown -R <non-root_username>.<non-root_username> /mnt/nfs
```

![](/uploads/2018/03/2018-03-07_7-29-28-1024x373.png)

With our directories ready, let's go ahead and mount our storage to them!

For VMHGFS:

<aside class="info-block"><p>I have mounted the following shared folder to the VM to use for this command.</p></aside>
![](/uploads/2018/03/2018-03-07_7-55-39-300x176.png)
```bash
sudo mount -t fuse.vmhgfs-fuse .host:/content /mnt/vmhgfs/depot/content -o allow_other
```
![](/uploads/2018/03/2018-03-07_8-36-50-1024x373.png)

For NFS:

```bash
sudo mount -t nfs <IP_address>:/<volume#>/<path_to_share> /mnt/nfs/depot/content
```

![](/uploads/2018/03/2018-03-07_8-56-36-1024x373.png)

For NFS 4.1 (optional):

```bash
sudo mount -t nfs4 -o vers=4,minorversion=1 <IP_address>:/<volume#>/<path_to_share> /mnt/nfs/depot/content
```

Now, with our storage mounted we can run the VSM script and configure for use.

<aside class="info-block"><p>You will be prompted to enter your VMware credentials unless you supply the &quot;-u&quot; and &quot;-p&quot; parameters</p></aside>

For VMHGFS:

```bash
vsm.sh -y -v /tmp/my_vsm --repo /mnt/vmhgfs/depot/content --save
```

![](/uploads/2018/03/2018-03-07_9-15-20-1024x373.png)

For NFS:

```bash
vsm.sh -y -v /tmp/my_vsm --repo /mnt/nfs/depot/content --save
```

![](/uploads/2018/03/2018-03-07_9-15-39-1024x373.png)

That about does it!  The appliance is ready to use and you can navigate through the menus to find your desired software.

***Extras:***

To make your mount points persistent through reboots, edit the "***fstab***" file with your editor of choice.  I prefer to use vi or vim, but many may choose to use nano instead.

```bash
sudo vi /etc/fstab
```

Then, add the following line and save the file.

For VMHGFS:

```properties
.host:/content /mnt/vmhgfs/depot/content    fuse.vmhgfs-fuse        allow_other     0 0
```

![](/uploads/2018/03/2018-03-07_9-22-54-1024x373.png)

For NFS:

```properties
<IP_address>:/<volume#>/<path_to_share> /mnt/nfs/depot/content    nfs      soft,bg,rsize=8192,wsize=8192       0 0
```

![](/uploads/2018/03/2018-03-07_9-24-34-1024x373.png)

For NFS 4.1 (optional):

```properties
<IP_address>:/<volume#>/<path_to_share> /mnt/nfs/depot/content    nfs      nfsvers=4.1,soft,bg,rsize=8192,wsize=8192       0 0
```

Updates are released quite frequently.  To update VSM to the latest version, you can run the following commands manually or add them to a shell script within "***/etc/cron.daily***" which will run around 3 AM.

<aside class="info-block"><p>please change timezone location to your respective location</p></aside>
```bash
cd /home/<user_name>/aac-base; ./aac-base.install -u; ./aac-base.install -i vsm America/New_York
```

Additionally, if you'd like to keep your favorite download repository up-to-date, edit ***crontab***

<aside class="info-block"><p>This requires that you first &quot;mark&quot; a repository by using that menu option</p></aside>
```bash
crontab -e
```

Then add the following line to it and save.  This will run daily at 6 AM.

```crontab
0 6 * * * /usr/local/bin/vsm.sh -y -mr -c --favorite
```

![](/uploads/2018/03/2018-03-07_9-29-41-1024x373.png)

***My Preference:***

I tend to use the following command when running VSM to get missing suites and packages from MyVMware.  If you do not use the "*-m*" parameter, it will only pull the same software available in the original VMware Software Manager tool from VMware.  The "*-mr*" parameter resets the "MyVMware" software info and implies "*-m*" hence why this is also used in the crontab line above.  The "-c" tells VSM to generate sha256sum checks against each downloaded file.

```bash
vsm.sh -y -mr -c
```

<aside class="info-block"><p>Depending on what you downloaded, there may be certain .txt files that will fail the checksum. This is expected and can be safely ignored.</p></aside>

Well, I hope you've found this post useful and I thank you for reading!  Special thanks again to Texiwill for making this awesome utility, as well as Mike White for posting his similar article using SMB/CIFS.

-virtualex-

- [Installing the Linux VMware Software Manager tool](https://notesfrommwhite.net/2017/10/30/installing-the-linux-vmware-software-manager-tool/)
- [vSphere Upgrade Saga: Linux VMware Software Manager (VSM)](https://www.astroarch.com/2018/01/vsphere-upgrade-saga-linux-vmware-software-manager-vsm/)
- [Texiwill's VSM GitHub](https://github.com/Texiwill/aac-lib/tree/master/vsm)

Updates:

- **03.23.18** - Updated to reflect changes in manual install commands for VSM v4.0.2, and cron.daily entry since cron runs as root so no need to use sudo
- **04.12.18** - Added TZ (Time Zone) setting to manual install commands and modified /etc/fstab command for NFS mounts
- **04.15.18** - Added "-c" parameter reference
- **01.17.19** - Added some command syntaxes for NFS 4.1
