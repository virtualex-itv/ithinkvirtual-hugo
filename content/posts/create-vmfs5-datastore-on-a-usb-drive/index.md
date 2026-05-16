{
  "title": "How To: Create A VMFS5 Datastore On A USB Drive",
  "date": "2016-08-14T21:45:09",
  "lastmod": "2018-02-10T14:33:36",
  "slug": "create-vmfs5-datastore-on-a-usb-drive",
  "url": "/posts/create-vmfs5-datastore-on-a-usb-drive/",
  "draft": false,
  "description": "Create A VMFS5 Datastore On A USB Drive Ever wondered if it was possible to use a USB Drive as a VMFS5 datastore in VMware vSphere 6.0?  I sure know that I have!  Not that I would like to run any VM’s on said datastore, as I’m sure performance would not be optimal, but instead…",
  "wordpress_id": 603,
  "wordpress_url": "https://ithinkvirtual.com/2016/08/14/create-vmfs5-datastore-on-a-usb-drive/",
  "featured_image": "/uploads/2016/08/VMFS5_USB.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Troubleshooting",
    "USB_VMFS5"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/08/14/create-vmfs5-datastore-on-a-usb-drive/"
  ],
  "comments": []
}

***Create A VMFS5 Datastore On A USB Drive***

Ever wondered if it was possible to use a USB Drive as a VMFS5 datastore in VMware vSphere 6.0?  I sure know that I have!  Not that I would like to run any VM’s on said datastore, as I’m sure performance would not be optimal, but instead to test its functionality and use it for storing ESXi host logs for example.  Well, I ran into an issue today where I needed to unmount all of my NFS mounts on ESXi 6.0 U2 in order to recreate some of the volumes before remounting them.  The problem was that I was unable to unmount one of my volumes because it was bound to the ESXi host for scratch logs.  As I didn’t have a spare drive of any sort to attach to my host so that I could reconfigure the location for scratch logs, I began tinkering with the idea of using a small USB drive as a temporary datastore for these logs.

After doing a little research, I came across a post from [Florian Grehl](https://de.linkedin.com/in/fgrehl/en) aka [@virten](https://twitter.com/virten?lang=en)  showing exactly how to accomplish this so I figured I’d share the process of doing so.  Keep in mind that this should only be used for testing purposes and should not be used in production environments.  This is unsupported by VMware.  Here we go!

Ensure that the USB device is unplugged from the ESXi host then begin by connecting to your ESXi host and stopping the USB arbitrator service.  This service is responsible for allowing USB device passthrough from an ESXi host to a virtual machine, so keep in mind that you will no longer be able to pass through USB devices to VM’s until this is restarted.  (Note: restarting service after creating and mounting USB datastore will break connectivity and recognition of the USB datastore).   To stop the service, run the following command:

```shell
/etc/init.d/usbarbitrator stop
```

![2016-08-11_17-12-19](/uploads/2016/08/2016-08-11_17-12-19-300x192.png)![2016-08-11_17-12-35](/uploads/2016/08/2016-08-11_17-12-35-300x192.png)

Optionally, if you’d like to permanently disable the service so it persists thru reboots, run the following command:

```shell
chkconfig usbarbitrator off
```

Plug the USB drive into your ESXi host.  For the purposes of this tutorial, I am using a small Lexar 8GB USB device.  If you navigate to the storage devices section on your host, you should now see the connected USB device is recognized by the hypervisor.  Make note of the device identifier number (mpx.vmhbaXX) for this device.

vSphere Client:

![2016-08-14_16-53-34](/uploads/2016/08/2016-08-14_16-53-34-300x141.png)

vSphere Web Client:

![2016-08-14_17-02-22](/uploads/2016/08/2016-08-14_17-02-22-300x152.png)

vSphere HTML5 Web Client:

![2016-08-14_17-02-44](/uploads/2016/08/2016-08-14_17-02-44-300x152.png)

You can also list the device information to determine the identifier by running the following command:

```bash
ls /dev/disks/
```

![2016-08-11_17-13-09](/uploads/2016/08/2016-08-11_17-13-09-300x192.png)

As we can see, my identifier is ***mpx.vmhba40:C0:T0:L0***for this device which also matches the identifier from the GUI pics above.  Note: The other USB (mpx.vmhba32:C0:T0:L0) is a separate USB where ESXi is installed on.

![2016-08-14_16-48-33](/uploads/2016/08/2016-08-14_16-48-33-300x277.png)

Next, we need to create a GPT (GUID Partition Table) label on the device.  To do so, run the following command using the correct identifier for the drive.  In my case, I will run with **mpx.vmhba40** for all of the following commands.  Be sure to change this to your correct ID.

```shell
partedUtil mklabel /dev/disks/mpx.vmhba40\:C0\:T0\:L0 gpt
```

![2016-08-14_17-04-20](/uploads/2016/08/2016-08-14_17-04-20-300x192.png)

Now run the following command to get the partition table information.

```shell
partedUtil getptbl /dev/disks/mpx.vmhba40\:C0\:T0\:L0
```

![2016-08-14_17-05-36](/uploads/2016/08/2016-08-14_17-05-36-300x192.png)

This returned the following output for me…

```text
gpt

973 255 63 15634432
```

![2016-08-14_17-06-01](/uploads/2016/08/2016-08-14_17-06-01-300x192.png)

Next, we need to create a partition in which you will need to know the start sector and end sector which all depend on the size of the device drive and GUID.  As an FYI…

- The start sector is always ***2048***
- The GUID for VMFS is always ***AA31E02A400F11DB9590000C2911D1B8***
- The end sector is calculated using the values obtained by running the previous command.
  - Formula: 973 x 255 x 63 – 1 = **15631244**

![2016-08-11_17-33-01](/uploads/2016/08/2016-08-11_17-33-01-300x223.png)

We can also run the following command to calculate the end sector value.  This should return an identical value that matches the previous calculation.

```bash
eval expr $(partedUtil getptbl /dev/disks/mpx.vmhba40\:C0\:T0\:L0 | tail -1 | awk '{print $1 " \\* " $2 " \\* " $3}') - 1
```

![2016-08-14_17-10-05](/uploads/2016/08/2016-08-14_17-10-05-300x159.png)![2016-08-14_17-10-45](/uploads/2016/08/2016-08-14_17-10-45-300x159.png)

If everything has gone smoothly so far, you should be ready to create the VMFS partition.  Run the following command, ensuring to replace the identifier and end sector values with your own.

```shell
partedUtil setptbl /dev/disks/mpx.vmhba40\:C0\:T0\:L0 gpt "1 2048 15631244 AA31E02A400F11DB9590000C2911D1B8 0"
```

![2016-08-14_17-12-02](/uploads/2016/08/2016-08-14_17-12-02-300x159.png)![2016-08-14_17-12-42](/uploads/2016/08/2016-08-14_17-12-42-300x159.png)

Lastly, we need to format the partition with VMFS using ***vmkfstools***.  Do so by running the following (Note: “” in the command below can be any name you like so feel free to use a different name for your datastore):

```shell
vmkfstools -C vmfs5 -S USB_Datastore /dev/disks/mpx.vmhba40\:C0\:T0\:L0:1
```

![2016-08-14_17-13-58](/uploads/2016/08/2016-08-14_17-13-58-300x162.png)

Sit tight…wait about one minute…and…voila!

![2016-08-14_17-16-35](/uploads/2016/08/2016-08-14_17-16-35-300x162.png)

After a quick rescan/refresh you should now have and see your mounted VMFS5 USB Datastore!

vSphere Client:

![2016-08-14_17-17-40](/uploads/2016/08/2016-08-14_17-17-40-300x141.png)

vSphere Web Client:

![2016-08-14_17-18-21](/uploads/2016/08/2016-08-14_17-18-21-300x152.png)

vSphere HTML5 Web Client:

![2016-08-14_17-18-52](/uploads/2016/08/2016-08-14_17-18-52-300x152.png)

After I changed the “Syslog” configuration for my scratch logs to use this new datastore, I was finally able to unmount my NFS datastores.  I hope this helps so please feel free to comment below.

Shoutout to Florian Grehl for his wonderful post!

Cheers!

-virtualex-

## Pingbacks

- [USB Devices as VMFS Datastore in vSphere ESXi 6.0](http://www.virten.net/2015/10/usb-devices-as-vmfs-datastore-in-vsphere-esxi-6-0/)
