{
  "title": "PernixData FVP Freedom Woes With Missing Supermicro System UUID",
  "date": "2016-08-06T22:44:03",
  "lastmod": "2018-02-10T14:36:14",
  "slug": "pernixdata-fvp-freedom-woes-with-missing-supermicro-system-uuid",
  "url": "/posts/pernixdata-fvp-freedom-woes-with-missing-supermicro-system-uuid/",
  "draft": false,
  "description": "PernixData FVP Freedom Woes With Missing System UUID Recently, I’ve been wanting to give PernixData FVP Freedom a run in my HomeLab Datacenter to better familiarize myself with the product and see how much of a performance improvement I’d get if any at all.  I’ve heard from so many people how much they love the product so…",
  "wordpress_id": 580,
  "wordpress_url": "https://ithinkvirtual.com/2016/08/06/pernixdata-fvp-freedom-woes-with-missing-supermicro-system-uuid/",
  "featured_image": "/uploads/2016/08/FVP2.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "PernixData",
    "Troubleshooting"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/08/06/pernixdata-fvp-freedom-woes-with-missing-supermicro-system-uuid/"
  ],
  "comments": []
}

**PernixData FVP Freedom Woes With Missing System UUID**

Recently, I’ve been wanting to give PernixData FVP Freedom a run in my HomeLab Datacenter to better familiarize myself with the product and see how much of a performance improvement I’d get if any at all.  I’ve heard from so many people how much they love the product so I figured “why not”?

For those who are not familiar with [PernixData FVP](http://pernixdata.com/pernixdata-fvp-software), it accelerates Storage and Virtual Machines by moving read and write operations to the server tier, instead of the storage tier, using Flash or RAM to ensure the fastest VM performance.  This, in turn, reduces VM latency by a claimed 10x and overall SAN utilization by over 80%.

 To start off, I visited the [PernixData website](http://pernixdata.com/free-software#trial-form) and went ahead to register for the free FVP Freedom product.  A short time later  I received an email and obtained my download and license key information, along with all the documentation needed to get it up and running.  I installed the ESXi host VIBs and opted to deploy the .ova appliance version so that the deployment would be a piece of cake.  Once I got the product up and running, I logged into the Management appliance and attempted to configure my cluster and add resources, but for some reason, none of my hosts’ were showing up.  I kept getting the “*No PernixData compatible hosts have been detected in the cluster*“, and only (1) of my (5) hosts was detected but it was not part of the cluster that I was configuring yet.

This is where I ran into a snag that took quite a bit of time to research and find a fix.  Luckily, another blogger by the moniker “***vWilmo***” who’d experienced this same issue and described how to fix it, so I figured I’d write a similar entry for my own reference, and to help others who may frequent my blog.  I will also be sharing his link at the bottom of this page.

Ultimately, the issue stemmed from the fact that Supermicro did not generate any system UUIDs for my boards and FVP needs them to detect the hosts to use as resources.  [KB 1006250](https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1006250) references the situation of an ESXi host not having a unique UUID but did not offer a solution other than to contact the manufacturer (*which I did via email and am still awaiting a reply*).  To confirm this, I ran a script I found online called **Get-VMHostUUID** to pull the UUID’s from all of my hosts connected to my vCenter server.  Upon review, it only returned a value for my “white box” host, and returned all “zero” values for my remaining (4) Supermicro systems.  I also ran ***prnxcli*** via SSH connection to my host which returned an error as well.

![2016-08-05_15-10-50](/uploads/2016/08/2016-08-05_15-10-50-300x159.png) ![2016-08-05_19-20-02](/uploads/2016/08/2016-08-05_19-20-02-300x192.png)

As my Supermicro systems run an AMI (American Megatrends) BIOS, there is a BIOS utility that can be used to generate a new UUID for the system which can be found here.  Download [this](http://download.lenovo.com/ibmdl/pub/pc/pccbbs/thinkcentre_bios/90jt18usa.zip) file and extract the contents.  The file we need to use is named ***AMIDEDOS.exe***, so I took this file and placed it on a DOS formatted USB drive that I had created with [Rufus](http://rufus.akeo.ie) back when I needed to flash my BIOS and upgrade my Intel NIC firmware.

![2016-08-05_19-39-09](/uploads/2016/08/2016-08-05_19-39-09-300x184.png)

Insert and boot into the USB, then navigate to the directory that houses the file mentioned above.

![2016-08-05_20-18-14](/uploads/2016/08/2016-08-05_20-18-14-300x190.png)

Enter the following command:

```batch
AMIDEDOS.exe /su auto
```

![2016-08-05_20-18-25](/uploads/2016/08/2016-08-05_20-18-25-300x190.png)

If successful, this will generate a new system UUID for you and you should then receive an output like this:

![2016-08-05_20-19-25](/uploads/2016/08/2016-08-05_20-19-25-300x190.png)

Reboot your host, SSH into it and run the ***prnxcli*** command.  If it runs successfully you should see an output like this:

![2016-08-05_20-30-04](/uploads/2016/08/2016-08-05_20-30-04-300x192.png)

After I completed this process on all of my (4) impacted hosts, I ran the **Get-VMHostUUID** script again and was happy to see that I now had a valid UUID for each host which match each ***prnxcli*** output.

![2016-08-05_20-52-42](/uploads/2016/08/2016-08-05_20-52-42-300x159.png)

Upon logging into the vCenter Web Client, I noticed that there is now a PernixData plugin icon in the vCenter Web Client interface which can be selected to launch the PernixData Management Console or access the FVP dashboard from within the Web Client.

![2016-08-06_11-02-46](/uploads/2016/08/2016-08-06_11-02-46-300x157.png)![2016-08-06_11-03-07](/uploads/2016/08/2016-08-06_11-03-07-300x157.png)

Lastly, I logged into the PernixData FVP Management console again, and I was now able to create my cluster and assist hosts as resources.  The only caveat is that there is a single-cluster limitation with the FVP Freedom version license, so if have all of your hosts in a single cluster then you are good.  Unfortunately for me, I have (3) clusters so I need to pick which one I want to use FVP with.  I decided to use my Management Cluster since that houses the majority of my VMs at the moment.

![2016-08-05_20-54-12](/uploads/2016/08/2016-08-05_20-54-12-300x167.png)

After letting it work its magic for a few hours, I noticed that the VM latency had reduced drastically to an average ~ +/- 2.0 ms and overall performance was great!  I must say that I am really impressed, satisfied, and glad that I gave this program a shot!

![2016-08-06_16-18-52](/uploads/2016/08/2016-08-06_16-18-52-300x147.png) ![2016-08-06_16-19-00](/uploads/2016/08/2016-08-06_16-19-00-300x147.png) ![2016-08-06_16-19-25](/uploads/2016/08/2016-08-06_16-19-25-300x147.png)

Well,  I hope that you have found this useful, thanks for stopping by!

Special thanks to Geoff Wilmington aka [@vWilmo](https://twitter.com/vWilmo?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor) for helping me to solve this as I am lucky I found your post.  Another shout out to Andy Daniel aka [@vNephologist](https://twitter.com/vnephologist) from PernixData for his willingness to communicate with and try to assist me with this problem.

## Pingbacks

- [Script to pull host UUID for VMware PowerCLI](http://thephuck.com/scripts/script-to-pull-host-uuid-for-vmware-powercli/)
- [All 0s UUID, PernixData and the AMIDEDOS Fix](https://vwilmo.wordpress.com/2014/06/29/all-0s-uuid-pernixdata-and-the-amidedos-fix/)
