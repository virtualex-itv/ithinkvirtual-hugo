{
  "title": "Create a macOS/OS X VM on VMware ESXi 6.5 & VMware Workstation 12.x",
  "date": "2017-02-12T06:15:42",
  "lastmod": "2019-03-22T12:29:18",
  "slug": "create-macos-os-x-vm-on-vmware-esxi-6-5-vmware-workstation-12-x",
  "url": "/posts/create-macos-os-x-vm-on-vmware-esxi-6-5-vmware-workstation-12-x/",
  "draft": false,
  "description": "Create a macOS/OS X VM on VMware ESXi 6.5 & VMware Workstation 12.5.2 Pro   **NOTE: This is completely for experimental purposes and is unsupported by both Apple and VMware** Running a MacOS/ OS X virtual machine is not anything new and has been supported for quite some time, as long as you are running…",
  "wordpress_id": 683,
  "wordpress_url": "https://ithinkvirtual.com/2017/02/12/create-macos-os-x-vm-on-vmware-esxi-6-5-vmware-workstation-12-x/",
  "featured_image": "/uploads/2017/02/macos-vmware.jpg",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "macOS"
  ],
  "years": [
    "2017"
  ],
  "aliases": [
    "/2017/02/12/create-macos-os-x-vm-on-vmware-esxi-6-5-vmware-workstation-12-x/"
  ],
  "comments": [
    {
      "author": "VirtuAlex",
      "date": "2017-09-30T21:04:00",
      "content": "<p>What kind of hardware are you trying to run the VM on?  After running the unlocker utility, did you make sure to reboot the host?  Just asking the obvious stuff of course.  I am not having any issues running my VM on ESXi 6.5U1.  As you can see in the attached shots, I&#8217;ve even just started to spin up a new macOS 10.13 High Sierra VM.  Check the date/timestamp&#8230;it&#8217;s today. 🙂<br />\n <a href=\"https://uploads.disquscdn.com/images/29823c73fe758c231d3d533c179b804bacb013ad705a066b3588bea08da0ef80.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/29823c73fe758c231d3d533c179b804bacb013ad705a066b3588bea08da0ef80.png</a><br />\n <a href=\"https://uploads.disquscdn.com/images/391711a33f78bb27a4d4912c8760d08d8cad29ea6d575d986b1b329f89c88a4e.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/391711a33f78bb27a4d4912c8760d08d8cad29ea6d575d986b1b329f89c88a4e.png</a><br />\n <a href=\"https://uploads.disquscdn.com/images/a5136d59d41123d1690cca2bfa7a097905f395ddce1d26c9ecd19620e93c9b53.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/a5136d59d41123d1690cca2bfa7a097905f395ddce1d26c9ecd19620e93c9b53.png</a></p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-09-30T20:56:00",
      "content": "<p>As I mentioned in a previous reply, what is different between the hosts you are trying to run the VM on.  I am not having any issues running on my hardware which is using Intel processors, etc.</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-09-30T20:50:00",
      "content": "<p>I wouldn&#8217;t necessarily say that there is a problem running on ESXi 6.5U1, as I am currently running my macOS 10.12 VM on that same version.  Is there anything different between the 6.5a and 6.5U1 hosts in regards to their hardware and/or configurations?</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-09-30T20:48:00",
      "content": "<p>Can you share a screen shot of your KP?  If anything, it could be related to the hardware of your host.</p>\n"
    },
    {
      "author": "Barry Jester Pearce",
      "date": "2017-09-27T07:56:00",
      "content": "<p>Cant for the life of me get this to work under esxi 6.5u1 w/ Sierra or El Capitan</p>\n"
    },
    {
      "author": "Barry Jester Pearce",
      "date": "2017-09-26T22:50:00",
      "content": "<p>Cant make this work on ESXi 6.5 U1 w/ Mac El Capitan or Sierra  <a href=\"https://uploads.disquscdn.com/images/561ee3a2e88c71751c17f98a167651f8016873a65f7608d3e593551e4eb969ae.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/561ee3a2e88c71751c17f98a167651f8016873a65f7608d3e593551e4eb969ae.png</a></p>\n"
    },
    {
      "author": "Rolf Bartels",
      "date": "2017-09-21T07:31:00",
      "content": "<p>FYI: Currently ESXi 6.5U1 is not supported or not working, the VM gets stuck at the apple logo.<br />\n6.5d works fine, same vm and same setup.</p>\n"
    },
    {
      "author": "Rolf Bartels",
      "date": "2017-09-21T05:04:00",
      "content": "<p>So ESX 6.5U1 is currently a problem, MacOSX 10.12 does not go past the apple logo at boot, as soon as we moved the VM to a ESX 6.5a host all was well.</p>\n"
    },
    {
      "author": "Andreas Gundlack",
      "date": "2017-09-15T10:57:00",
      "content": "<p>I had the same problem/screen while trying to install mac os on ESXi with Pentium Processors. I switched to a machine running Xeon Processors and it works fine!</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-09-04T09:15:00",
      "content": "<p>What exactly are you looking for?</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-08-20T11:21:00",
      "content": "<p>Hi Phil &#8211; Which platform are you installing this on, ESXi or Workstation? Be sure to reboot your host after running the Unlocker utility if installing on ESXi and also be sure to add the extra parameter to your configuration file if installing on Workstation.  Please carefully complete each step in the tutorial again and let me know if you still have issues. I have not been able to reproduce your error.</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-08-20T11:15:00",
      "content": "<p>Hi Nick, any word on what exactly?</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-08-20T11:14:00",
      "content": "<p>Hi.  Please keep in mind that this is a VM running on Non-Apple hardware.  It&#8217;s not a hackintosh and there are certain features that simply will not work which is to be expected unfortunately.</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-08-20T11:10:00",
      "content": "<p>Which platform are you installing this on, ESXi or Workstation? Be sure to reboot your host after running the Unlocker utility if installing on ESXi and also be sure to add the extra parameter to your configuration file if installing on Workstation. Please carefully complete each step in the tutorial again and let me know if you still have issues.  I have not been able to reproduce your error.</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-08-20T11:08:00",
      "content": "<p>Honestly not too sure about this error as I am unable to reproduce this on my end.  Which platform are you installing this on, ESXi or Workstation?   Be sure to reboot your host after running the Unlocker utility if installing on ESXi and also be sure to add the extra parameter to your configuration file if installing on Workstation.  Please carefully complete each step in the tutorial.</p>\n"
    },
    {
      "author": "Nick Howard",
      "date": "2017-07-11T15:49:00",
      "content": "<p>any word on this?</p>\n"
    },
    {
      "author": "Serkan Polat",
      "date": "2017-07-04T08:34:00",
      "content": "<p>on vmware esxi 6.5 , i installed sierra 10.12.5</p>\n<p>how can i change the system definition? app store is not working.. system definition is unknown </p>\n<p>on<br />\nhackintosh systems we use clover configurator and add system definition<br />\nto config.plist</p>\n"
    },
    {
      "author": "Ryan",
      "date": "2017-06-30T23:29:00",
      "content": "<p>I have followed the steps here when I power on the VM I&#8217;m stuck at an apple logo indefinitely. Any suggestions?</p>\n"
    },
    {
      "author": "Doug Teal",
      "date": "2017-06-20T07:44:00",
      "content": "<p>Thanks for the great write up!  I&#8217;m getting the attached error when I power up the MAC VM.  Any ideas?  </p>\n<p><a href=\"https://uploads.disquscdn.com/images/d9379b7364bf285460c6df16ae2017652007c64b77d76753d762f79086ac60bd.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/d9379b7364bf285460c6df16ae2017652007c64b77d76753d762f79086ac60bd.png</a></p>\n"
    },
    {
      "author": "Doug Teal",
      "date": "2017-06-19T20:28:00",
      "content": "<p>Thanks for sharing the information.  I&#8217;m receiving the attached error when I power up the VM.  I&#8217;m running ESXi 6.5.0, 4887370.</p>\n<p><a href=\"https://uploads.disquscdn.com/images/d9379b7364bf285460c6df16ae2017652007c64b77d76753d762f79086ac60bd.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/d9379b7364bf285460c6df16ae2017652007c64b77d76753d762f79086ac60bd.png</a></p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-06-06T22:21:00",
      "content": "<p>@jamesschramm:disqus &#8211; absolutely!  Keep in mind that MacOS Server is simply an add-on application. <a href=\"https://uploads.disquscdn.com/images/b86a02f8506c3573f06549cee0e248f74f8cdae1aef873496bfb2273a544ed19.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/b86a02f8506c3573f06549cee0e248f74f8cdae1aef873496bfb2273a544ed19.png</a>  <a href=\"https://uploads.disquscdn.com/images/0799e6da3456f045cac073ad6f5eeb5d4f9473ae0fb6c178f7675160379746af.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/0799e6da3456f045cac073ad6f5eeb5d4f9473ae0fb6c178f7675160379746af.png</a></p>\n"
    },
    {
      "author": "Schrammbo",
      "date": "2017-05-30T10:29:00",
      "content": "<p>Will this process work for installing MacOS Server on ESXi 6.5a?</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-04-26T21:39:00",
      "content": "<p>@disqus_ZaJcgDrJGd:disqus &#8211; thx for commenting.  Is your VM running on ESXi or on Workstation?  Please keep in mind that that this method of using a MacOS VM is not supported by VMware nor by Apple on non-Apple hardware. Issues are to be expected and unfortunately I really cannot provide support for any issues you may experience while using said VM.</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-04-26T21:32:00",
      "content": "<p>@disqus_T69MntdwwV:disqus &#8211; this is great!  Thx for pointing out this workaround!</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-04-26T21:30:00",
      "content": "<p>@martin_jessop:disqus &#8211; thx for commenting and pointing this out for the community!</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-04-26T21:28:00",
      "content": "<p>@matthewtoye:disqus &#8211; thanks for commenting.  I honestly have not experimented with this as I do not use any PCI GPU&#8217;s in my ESXi hosts.  I am curious about it though so I will reach out to a friend of mine who does use PCI Passthrough in his setup and see if he can create a MacOS VM and test this out!</p>\n"
    },
    {
      "author": "John Smith",
      "date": "2017-04-24T09:24:00",
      "content": "<p>im having issue  with connecting a usb iphone device. it appears in xcode then disappears after 10-15 secs. i see in the console log that device gets disconnected error 61&#8230;  also initially I never had a problem .. it happened when i created a new vm</p>\n"
    },
    {
      "author": "dan f",
      "date": "2017-04-11T20:45:00",
      "content": "<p>thanks for the walk through as well!!<br />\nadding the following lines  to the .vmx files worked for me.. they came from a vmware KB article on changing resolutions for windows clients. I have both Sierra and ElCapitan working</p>\n<p>svga.autodetect = &#8220;FALSE&#8221;<br />\nsvga.vramSize = 20971520<br />\nsvga.maxWidth = 1400<br />\nsvga.maxHeight = 900<br />\nit won&#8217;t auto size; just drag the VMRC window ( like you are resizing)  and it should fix itself.</p>\n"
    },
    {
      "author": "Martin Jessop",
      "date": "2017-04-10T17:30:00",
      "content": "<p>A warning to anyone who has edited their local.sh file the unlocker install blows away any change you may have made.  Also worth noting that the unlocker files should go on persistent storage for ease of access.</p>\n"
    },
    {
      "author": "Matthew Toye",
      "date": "2017-04-03T21:50:00",
      "content": "<p>This is very interesting.. Have you experimented with using pci passthrough on a dedicated graphics card to the OS? i would be interested in if you can run a fully functional workstation off this with qe/ci enabled..</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-03-31T09:35:00",
      "content": "<p>@ajschot:disqus &#8211; thx for taking the time to check out this post and comment.  I am assuming that you have successfully ran the unlocker 2.0.9 script on your ESXi host.  When the script is executed, it connects to the VMware tools repository for VMware Fusion in order to download the darwin.iso which is the VMware Tools media for MacOS.  It places the downloaded darwin.iso back into the unlocker scripts folder under a newly created &#8220;tools&#8221; directory.  Go ahead and check the datastore where you placed the unlocker script, and see if there is a tools folder within.  Hope this helps!<br />\n <a href=\"https://uploads.disquscdn.com/images/3b554bbd09089607d9e5c36c1dfc29eb2147a89fe8c08373f529ce0a00445539.png\" rel=\"nofollow ugc\">https://uploads.disquscdn.com/images/3b554bbd09089607d9e5c36c1dfc29eb2147a89fe8c08373f529ce0a00445539.png</a></p>\n"
    },
    {
      "author": "AJSchot",
      "date": "2017-03-31T05:04:00",
      "content": "<p>How to get latest version of VMware Tools??? becuase i get a alert that this is an old version (it is for El capitan) and it does load in ESXi 6.5a so the guest tools does not work!!! anymbody have a newer verison or know how to upgrade?</p>\n"
    },
    {
      "author": "AJSchot",
      "date": "2017-03-31T04:38:00",
      "content": "<p>I installed OSX 10.12 on ESXi 6.5a and try to find a working VMware Tools&#8230; but finding only old version and in ESXi it does not work when selecting VMware tools installer&#8230; where to find latest darwin.iso??</p>\n"
    },
    {
      "author": "VirtuAlex",
      "date": "2017-03-05T19:07:00",
      "content": "<p>@disqus_1HbK3aGTeU:disqus &#8211; thanks much for the feedback and for pointing this out!  I will test on my end as well and update the post.</p>\n"
    },
    {
      "author": "TimB",
      "date": "2017-03-05T19:02:00",
      "content": "<p>Great walkthrough, thanks for the effort. The 1176&#215;885 resolution limit on ESXi is down to only allocating 4MB Video RAM. Increasing it to 16MB allowed me to go full screen on my 1600&#215;900 laptop.</p>\n"
    }
  ]
}

### *Create a macOS/OS X VM on VMware ESXi 6.5 & VMware Workstation 12.5.2 Pro*

*****NOTE: This is completely for experimental purposes and is unsupported by both Apple and VMware*****

Running a MacOS/ OS X virtual machine is not anything new and has been supported for quite some time, as long as you are running said VM on a supported hypervisor with Apple Hardware.  But many of the “Non-Apple” users in the world would not be able to take advantage of this without owning some type of Apple Computer.  Luckily, there is an alternative method for running a Mac-based VM on non-apple hardware-based VMware ESXi and/or VMware Workstation for Windows!  In this tutorial, I am going to show you just how to do so.  Please keep in mind that the methods described in this article are not supported nor endorsed by Apple or VMware in any way, so please use at your own risk.

Before we can begin, there are a few tools required to ensure this works flawlessly.

- macOS Sierra installation media in .iso format (You can use an older OS as well but for this demo, I will be installing macOS Sierra 10.12.3)
  - This media will have to be created as the OS comes as a .app by default.
  - This [link](http://www.insanelymac.com/forum/topic/315967-how-to-create-a-bootable-sierra-iso-for-vmware/) has a good tutorial for creating said media.
- Unlocker Utility
  - Current Stable version [2.0.8](http://www.daveparsons.net/downloads/unlocker208.zip) works up to OS X Yosemite on ESXi 6.0 and Workstation 11
  - Version [2.0.9](https://github.com/DrDonk/unlocker/archive/master.zip) RC adds support for macOS Sierra on ESXi 6.5 and Workstation 12.x
- Type 1 Hypervisor (ESXi) or a Type 2 Hypervisor (VMware Workstation)

Ready? Here we go!  I’ll start by showing you how to create a macOS Sierra VM on VMware Workstation 12.5.2 Pro…

##### ***VMware Workstation 12.5.2 Pro***

- Make sure that VMware Workstation is installed but not running.
- Extract the contents on the Unlocker 2.0.9RC.
- Open a command prompt and navigate to the extracted folder
- Run win-install.cmd.  This will patch your VMware Workstation to unlock the capabilities to run a Mac OS.  It will also download the latest VMware Tools (darwin.iso) for macOS into the extracted directory.

![](/uploads/2017/02/2017-02-10_7-39-05-150x150.png) ![](/uploads/2017/02/2017-02-10_7-41-06-150x150.png) ![](/uploads/2017/02/2017-02-10_7-41-34-150x150.png)

- Launch VMware Workstation and create the shell VM

![](/uploads/2017/02/2017-02-10_7-42-35-150x150.png) ![](/uploads/2017/02/2017-02-10_7-42-49-1-150x150.png) ![](/uploads/2017/02/2017-02-10_7-43-19-150x150.png)

- When choosing the hardware compatibility, you can optionally change this to version 10 so that you do not need to manually edit the .vmx file after the shell has been created.

![](/uploads/2017/02/2017-02-10_7-44-08-150x150.png) ![](/uploads/2017/02/2017-02-10_7-44-16-150x150.png)

- I am going to leave it at version 12 and manually edit the .vmx file afterwards.  Continue creating your shell by following along…

![](/uploads/2017/02/2017-02-10_7-44-37-150x150.png) ![](/uploads/2017/02/2017-02-10_7-45-11-150x150.png) ![](/uploads/2017/02/2017-02-10_7-45-19-150x150.png) ![](/uploads/2017/02/2017-02-10_7-45-32-150x150.png) ![](/uploads/2017/02/2017-02-10_7-45-39-150x150.png) ![](/uploads/2017/02/2017-02-10_7-45-50-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-00-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-09-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-17-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-26-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-37-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-45-150x150.png) ![](/uploads/2017/02/2017-02-10_7-46-52-150x150.png)![](/uploads/2017/02/2017-02-10_7-47-13-150x150.png)

- Now that we have the shell created, we still need to attach the ISO to the VM.  Click on the CD/DVD (SATA) option on the left side in the Devices pane.  Once in the settings, select the ISO image.

![](/uploads/2017/02/2017-02-10_7-47-25-150x150.png)![](/uploads/2017/02/2017-02-10_7-47-57-150x150.png)![](/uploads/2017/02/2017-02-10_7-48-33-150x150.png)

- Next, navigate to the directory that houses the virtual machine’s files.  Edit the .vmx file with your preferred text editor.  I personally love using NotePad++.  Scroll to the bottom of the text and add the following line.  This will enable the VM to boot up.
  - If you opted to change the hardware version to version 10 in the earlier steps, disregard this and move on to the next step.

```text
smc.version = "0"
```

![](/uploads/2017/02/2017-02-10_7-49-39-150x150.png) ![](/uploads/2017/02/2017-02-10_7-50-11-150x150.png) ![](/uploads/2017/02/2017-02-10_10-08-44-150x150.png)

- At this point, the VM is ready to be powered on to install macOS Sierra.  I will cover the installation steps further down in this tutorial, but first, let me cover the procedures for enabling this on ESXi.  I will be showing how to do so on ESXi 6.5a (Build 48872370)

![](/uploads/2017/02/2017-02-10_7-52-47-150x150.png)

##### ***VMware ESXi 6.5a (Build 48872370)***

![](/uploads/2017/02/2017-02-11_21-32-07-150x150.png)

- For ESXi we first need to copy the unlocker utility to a local or shared datastore.  You can accomplish this by using vCenter, ESXi Host UI, or WinSCP.  For simplicity, I opted to use WinSCP and copied the folder into a newly created “Tools” folder on a local datastore.  You can also take this time to upload the .ISO to the local datastore for use later in this tutorial.

![](/uploads/2017/02/2017-02-11_21-38-05-150x150.png) ![](/uploads/2017/02/2017-02-11_21-42-40-150x150.png) ![](/uploads/2017/02/2017-02-11_21-45-34-150x150.png) ![](/uploads/2017/02/2017-02-11_21-46-14-150x150.png) ![](/uploads/2017/02/2017-02-11_21-46-32-150x150.png)

- Now that the files have been copied, open an SSH connection to your ESXi host, and navigate to the unlocker directory.

![](/uploads/2017/02/2017-02-11_21-52-28-150x150.png) ![](/uploads/2017/02/2017-02-11_21-52-47-150x150.png) ![](/uploads/2017/02/2017-02-11_21-53-26-150x150.png)

- We can then type “***ls***” to view the contents of the directory.

![](/uploads/2017/02/2017-02-11_21-57-26-150x150.png)

- Next, we must make the installation script executable.  I also like to make the uninstallation script executable as well.  Do so by running the following commands.

```bash
chmod +x esxi-install.sh

chmod +x esxi-uninstall.sh
```

![](/uploads/2017/02/2017-02-11_22-00-56-150x150.png) ![](/uploads/2017/02/2017-02-11_22-01-22-150x150.png)

- Typing “***ls***” again will now display the (2) scripts in green text, indicating that they are now executable.

![](/uploads/2017/02/2017-02-11_22-01-56-150x150.png)

- Run the installer script by running the following command

```bash
./esxi-install.sh
```

![](/uploads/2017/02/2017-02-11_22-07-16-150x150.png)

- The script will only take a brief moment to run, afterward, a reboot is required.  Once it has finished type

```bash
reboot
```

![](/uploads/2017/02/2017-02-11_22-08-24-150x150.png)

- After the ESXi host has restarted, connect to the ESXi Host UI and begin building the shell VM by following along.

![](/uploads/2017/02/2017-02-11_22-15-44-150x150.png) ![](/uploads/2017/02/2017-02-11_22-16-56-150x150.png) ![](/uploads/2017/02/2017-02-11_22-17-12-150x150.png) ![](/uploads/2017/02/2017-02-11_22-17-46-150x150.png) ![](/uploads/2017/02/2017-02-11_22-18-01-150x150.png) ![](/uploads/2017/02/2017-02-11_22-18-48-150x150.png) ![](/uploads/2017/02/2017-02-11_22-19-58-150x150.png)

- Now that the shell VM is created, we need to go back into the VM’s settings and attach the .ISO that you uploaded to the datastore in a previous step.

![](/uploads/2017/02/2017-02-11_22-20-21-150x150.png) ![](/uploads/2017/02/2017-02-11_22-21-45-150x150.png) ![](/uploads/2017/02/2017-02-11_22-28-05-150x150.png) ![](/uploads/2017/02/2017-02-11_22-28-17-150x150.png)

- At this point, the VM is ready to be powered on to install macOS Sierra!  Unlike with the VMware Workstation instructions, there is no need to change the hardware version to version 10 or manually modify the .vmx file.

![](/uploads/2017/02/2017-02-11_22-28-41-150x150.png)

- In the next section, I will cover the installation steps for MacOS Sierra.

##### ***Installing macOS Sierra***

***The following instructions apply to both an ESXi and Workstation built macOS VM***

- Start by powering on the virtual machine and opening the Remote Console view

![](/uploads/2017/02/2017-02-11_22-51-38-150x150.png) ![](/uploads/2017/02/2017-02-11_22-51-49-150x150.png) ![](/uploads/2017/02/2017-02-11_22-52-47-150x150.png)

- Once the VM has booted the .ISO, you will be presented with this screen.  Click next and then go to the taskbar and open Disk Utility.  We need to create a partition to install macOS onto.

![](/uploads/2017/02/2017-02-11_22-54-21-150x150.png) ![](/uploads/2017/02/2017-02-11_22-54-56-150x150.png) ![](/uploads/2017/02/2017-02-11_22-55-23-150x150.png) ![](/uploads/2017/02/2017-02-11_22-55-51-150x150.png) ![](/uploads/2017/02/2017-02-11_22-56-10-150x150.png) ![](/uploads/2017/02/2017-02-11_22-57-02-150x150.png)

- After the partition has been created, we can actually start the macOS installation.

![](/uploads/2017/02/2017-02-11_22-57-26-150x150.png) ![](/uploads/2017/02/2017-02-11_22-57-42-150x150.png) ![](/uploads/2017/02/2017-02-11_22-58-16-150x150.png) ![](/uploads/2017/02/2017-02-11_22-58-36-150x150.png) ![](/uploads/2017/02/2017-02-11_22-58-54-150x150.png) ![](/uploads/2017/02/2017-02-11_23-10-42-150x150.png)

- After the VM has rebooted, we can continue the installation/configuration of macOS.

![](/uploads/2017/02/2017-02-11_23-46-38-150x150.png) ![](/uploads/2017/02/2017-02-11_23-47-26-150x150.png) ![](/uploads/2017/02/2017-02-11_23-47-43-150x150.png) ![](/uploads/2017/02/2017-02-11_23-47-57-150x150.png) ![](/uploads/2017/02/2017-02-11_23-48-18-150x150.png) ![](/uploads/2017/02/2017-02-11_23-48-36-150x150.png) ![](/uploads/2017/02/2017-02-11_23-48-55-150x150.png) ![](/uploads/2017/02/2017-02-11_23-49-09-150x150.png) ![](/uploads/2017/02/2017-02-11_23-49-48-150x150.png) ![](/uploads/2017/02/2017-02-11_23-50-11-150x150.png) ![](/uploads/2017/02/2017-02-11_23-51-23-150x150.png) ![](/uploads/2017/02/2017-02-11_23-52-05-150x150.png)

- Finally, the macOS VM is ready to use!  For the finishing touches, it is recommended to install VMware Tools on this VM.  When we ran the installation script at the start of this procedure, it downloaded a “tools” folder inside of the unlocker tool folder and inside it contains the darwin.iso which is used to install VMware tools.  This should be the latest release of VMware Tools 10.1.0.  Optionally, you can always download the tools from VMware’s website.
- In order to install the VMware Tools, we first need to eject the mounted install media.  Afterwards, connect the CD/DVD drive to the darwin.iso file.

![](/uploads/2017/02/2017-02-12_0-08-25-150x150.png) ![](/uploads/2017/02/2017-02-12_0-09-51-150x150.png) ![](/uploads/2017/02/2017-02-12_0-10-41-150x150.png) ![](/uploads/2017/02/2017-02-12_0-11-28-150x150.png)

- Once the VMware Tools (darwin.iso) is mounted, double-click the “Install VMware Tools” package to begin the installation.  After it completes, reboot the VM for the changes to take effect.

![](/uploads/2017/02/2017-02-12_0-11-56-150x150.png) ![](/uploads/2017/02/2017-02-12_0-12-29-150x150.png) ![](/uploads/2017/02/2017-02-12_0-12-51-150x150.png) ![](/uploads/2017/02/2017-02-12_0-13-15-150x150.png) ![](/uploads/2017/02/2017-02-12_0-13-28-150x150.png) ![](/uploads/2017/02/2017-02-12_0-13-46-150x150.png) ![](/uploads/2017/02/2017-02-12_0-14-11-150x150.png)

##### ***Optional Tweaks***

###### ***Adjusting Screen Resolution***

- By default, the macOS VM will only support (1) resolution natively, 1024 x 768.

![](/uploads/2017/02/2017-02-12_0-28-51-150x150.png)

- If you’d like to change this to support a higher resolution for say…a larger monitor, please download the following [file](https://idmedia.no/wp-content/uploads/2015/10/VMware-Fix-resolution.zip) on the macOS VM.  Once the file has been downloaded to the “Downloads” folder in the VM. Open the “Terminal” application and navigate to the folder.  We need to make the script executable, just as we did earlier with the unlocker scripts.

```bash
cd Downloads/VMware-Fix-resolution/

chmod +x vmware-resolutionSet
```

![](/uploads/2017/02/2017-02-12_0-35-36-150x150.png) ![](/uploads/2017/02/2017-02-12_0-36-13-150x150.png)

- Now we can run the script and specify the desired resolution.  In this example, I am going to choose a 1440 x 900 resolution.  Do so by running the following

```bash
./vmware-resolutionSet 1440 900
```

![](/uploads/2017/02/2017-02-12_0-38-28-150x150.png)

- On the ESXi-based VM, I did notice that it does not set a resolution higher than 1176 x 885 while in the Remote Console.  But, the VMware Workstation-based VM does indeed set the desired resolution.

![](/uploads/2017/02/2017-02-12_0-38-55-150x150.png) ![](/uploads/2017/02/2017-02-12_0-50-44-150x150.png)

###### ***Disable Beam Synchronization to Improve VM Performance***

- Download the following [application](https://www.sendspace.com/file/sm9sf7) and place it in the “Applications” folder.  Double-click it to launch the application.  Afterwards, add it to the user’s “Logon Option” so it runs every time at login.

![](/uploads/2017/02/2017-02-12_0-57-28-150x150.png) ![](/uploads/2017/02/2017-02-12_1-00-58-150x150.png) ![](/uploads/2017/02/2017-02-12_1-02-10-150x150.png)

I hope that you’ve found this information useful.  Please do leave comments below and subscribe to my blog!  Thanks for stopping by!

-virtualex-

## Pingbacks

- [macOS 10.13 High Sierra on ESXi 6.5](/posts/macos-10-13-high-sierra-on-esxi-6-5/)
