{
  "title": "Intel NIC not detected by ESXi",
  "date": "2016-03-22T03:48:41",
  "lastmod": "2018-02-10T15:14:31",
  "slug": "intel-nic-not-detected-by-esxi",
  "url": "/posts/intel-nic-not-detected-by-esxi/",
  "draft": false,
  "description": "Intel NIC Not Detected by ESXi   In this post I am going to cover a random issue I encountered after installing ESXi 6.0 Update 2 on one of my new Home Lab 2016 hosts.  The actual installation of ESXi was extremely easy and painless (I may cover that in another post).  After I had completed…",
  "wordpress_id": 237,
  "wordpress_url": "https://ithinkvirtual.com/2016/03/21/intel-nic-not-detected-by-esxi/",
  "featured_image": "/uploads/2016/03/2016-03-18_18-02-50.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "Troubleshooting"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/03/21/intel-nic-not-detected-by-esxi/"
  ],
  "comments": []
}

Intel NIC Not Detected by ESXi

In this post I am going to cover a random issue I encountered after installing ESXi 6.0 Update 2 on one of my new Home Lab 2016 hosts.  The actual installation of ESXi was extremely easy and painless (I may cover that in another post).  After I had completed the installation, I was attempting to configure my Management network interfaces and suddenly noticed that only 4 network interfaces were being detected!

![2016-03-18_19-07-54](/uploads/2016/03/2016-03-18_19-07-54-300x226.png)

As I then thought to myself, “I wonder what is going on here since I didn’t get any POST issues?”, I noticed that I was getting a message during POST regarding the initialization of the Intel Boot Agent for PXE booting.  The message stated:

> “…PXE-E05: The LAN adapter’s NVM configuration is corrupted or has not been initialized.  The Boot Agent cannot continue.”

![2016-03-18_18-02-50](/uploads/2016/03/2016-03-18_18-02-50-300x169.png)

Immediately, I began to consult “Mr. Google” and see if there was anything I could find related to this particular problem.  After reading a few threads, many users had mentioned and/or suggested that the NIC’s firmware was corrupted and needed to be “re-flashed”.  I quickly got to work and researched a bit further to understand the process of flashing the NIC firmware.  I downloaded the latest version of [PREBOOT](https://downloadcenter.intel.com/download/19186/Intel-Ethernet-Connections-Boot-Utility-Preboot-Images-and-EFI-Drivers) (at the time of this writing, it was version 20.7)which contains the “BootUtility” needed to perform the flash.

Next, I prepared myself a DOS-bootable USB using [Rufus](https://rufus.akeo.ie/).  I then extracted the PREBOOT.exe file using 7zip and placed the contents on the newly created USB.  This would allow me to either boot into the USB and access DOS or boot into the UEFI: Built-in Shell on Supermicro motherboards, and access the necessary files.  Once I had my drive ready, I went ahead and plugged it into my server and initiated a reboot.  During POST, I invoked the boot menu so and chose the option to boot into the Built-in Shell.

![2016-03-21_21-19-54](/uploads/2016/03/2016-03-21_21-19-54-300x226.png)

Once in the shell, I determined that my USB was mounted at **fs4:**

![2016-03-21_21-21-36](/uploads/2016/03/2016-03-21_21-21-36-300x226.png)

I navigated through the directories so I can see the contents of each folder until I saw the **BootIMG.FLB** file which is the new flash image I want to apply.  I then navigated to the location of the BootUtility.  Since I am using the built-in shell, I needed to ensure that I used the BootUtil for x64-bit EFI so I navigated to the following location:

```text
...\PREBOOT\APPS\BootUtil\EFIx64
```

![2016-03-21_21-24-17](/uploads/2016/03/2016-03-21_21-24-17-300x226.png)

Running the BOOTUTIL64E.EFI file will simply list your network interfaces and I could then see the current firmware version for all of my interfaces, although for some reason the ones in question are displaying “Not Present”.  Adding a “**-?**” suffix will bring up the help and list all the parameters to execute the commands properly.  I found a great reference article [here](ftp://supermicro.com/CDR-X9_1.23_for_Intel_X9_platform/Intel/LAN/v18.8/APPS/BOOTAGNT/DOCS/boot_util.htm) which made it easier for me to see what parameters I needed in my command.

![2016-03-21_21-25-48](/uploads/2016/03/2016-03-21_21-25-48-300x226.png)

To begin, I entered the following command since I wanted to enable flash on all of my NICs.

```batch
BOOTUTIL64E.EFI -ALL -FLASHENABLE
```

![2016-03-21_21-29-17](/uploads/2016/03/2016-03-21_21-29-17-300x226.png)

Or, if you wanted to do each one individually, you could specify the NIC  number (referenced as X below) manually.

```batch
BOOTUTIL64E.EFI -NIC=X -FLASHENABLE
```

A reboot is required after successful completion of this command before proceeding, so I went ahead and rebooted my system and then booted back into my USB via the built-in shell.

![2016-03-21_21-29-51](/uploads/2016/03/2016-03-21_21-29-51-300x226.png)

Afterwards, simply running the utility again showed that NIC ports 1-4 were all PXE ready.

![2016-03-21_21-34-35](/uploads/2016/03/2016-03-21_21-34-35-300x226.png)

Now it was time to run the following flash command.  ***Note***: Specifying the file parameter is optional.  Without it, it will assume that the BOOTIMG.FLB file is in the same location you are executing the command from.  Since I left the file in its originating location, I had to specify it manually.

```batch
BOOTUTIL64E.EFI -UP=PXE -ALL -FILE=\SuperMicro\PREBOOT\APPS\BootUtil\BOOTIMG.FLB
```

You will then be prompted to create a restore image, in the event something goes awry but I chose not to create a restore image.

![2016-03-21_21-38-31](/uploads/2016/03/2016-03-21_21-38-31-300x226.png)

Upon successful completion, I can now see that my firmware version has been upgraded from version **1.3.98** and is now running version **1.5.78**!

![2016-03-21_21-40-55](/uploads/2016/03/2016-03-21_21-40-55-300x226.png)

Now that my firmware has been upgraded, I rebooted the host and accessed the Management Network settings screen, and to my delight, ESXi was now detecting all of my network interfaces!  Woohoo!!

![2016-03-21_22-17-38](/uploads/2016/03/2016-03-21_22-17-38-300x226.png)

I am still trying to figure out why flash is not present on the NICs that previously were not detected, and my assumption is that it’s due to these being relatively cheap $80 network cards instead of full priced (~$300) network cards.  In any case, they still work and I am quite happy with them.  I hope you have found this information useful.  Thanks for reading!
