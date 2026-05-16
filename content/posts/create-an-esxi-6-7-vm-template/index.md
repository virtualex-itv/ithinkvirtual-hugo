{
  "title": "Create an ESXi 6.7 VM Template",
  "date": "2019-01-21T21:21:31",
  "lastmod": "2019-02-20T02:50:28",
  "slug": "create-an-esxi-6-7-vm-template",
  "url": "/posts/create-an-esxi-6-7-vm-template/",
  "draft": false,
  "description": "",
  "wordpress_id": 1393,
  "wordpress_url": "https://ithinkvirtual.com/2019/01/21/create-an-esxi-6-7-vm-template/",
  "featured_image": "/uploads/2019/01/2019-01-21_16-14-09.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "Template",
    "vExpert",
    "VMware",
    "vSphere"
  ],
  "years": [
    "2019"
  ],
  "aliases": [
    "/2019/01/21/create-an-esxi-6-7-vm-template/"
  ],
  "comments": []
}

***Disclaimer:  The following is not supported by VMware.***

Nested virtualization is nothing new, and many of us use it for test or demonstration purposes since they can quickly be stood up or torn down.  William Lam has an ESXi VM which can be downloaded from here, but I wanted to go ahead and create my own for use within my nested lab environments.

In this post, I am going to show you the steps I ran through to create an ESXi 6.7 VM that I can convert to a template for later use.  Props to William for his excellent content on nested virtualization, which I've used a ton and will be leveraging here as well.  So without further ado, let's get to it!

For my ESXi VM, I will be configuring the following:

- CPU: 2 (Expose hardware assisted virtualization to the guest OS - checked on)
- RAM: 8GB
- Disk0: 16GB (bound to the default SCSI controller; thin provisioned)
- New virtual NVME Controller
- Disk1: 10GB (for VSAN cache tier bound to NVME Controller; thin provisioned)
- Disk2: 100GB (for VSAN capacity tier bound to NVME Controller; thin provisioned)
- 2x Network Adapters (VMXNET3)
- Some advance configuration settings

Build the VM as follows:

![](/uploads/2019/01/2019-01-21_13-23-57.png)
![](/uploads/2019/01/2019-01-21_13-25-37.png)
![](/uploads/2019/01/2019-01-21_13-26-18.png)
![](/uploads/2019/01/2019-01-21_14-39-42.png)
![](/uploads/2019/01/2019-01-21_13-29-40.png)
![](/uploads/2019/01/2019-01-21_14-14-41.png)
![](/uploads/2019/01/2019-01-21_14-15-24.png)
![](/uploads/2019/01/2019-01-21_14-17-39.png)
![](/uploads/2019/01/2019-01-21_14-20-17.png)
![](/uploads/2019/01/2019-01-21_14-21-24.png)
![](/uploads/2019/01/2019-01-21_14-22-23.png)
![](/uploads/2019/01/2019-01-21_14-23-39.png)

Be sure you connect the ESXi installation media and power on the VM to begin the installation.

![](/uploads/2019/01/2019-01-21_14-33-21.png)
![](/uploads/2019/01/2019-01-21_14-36-02.png)
![](/uploads/2019/01/2019-01-21_14-36-17.png)
![](/uploads/2019/01/2019-01-21_14-36-45.png)
![](/uploads/2019/01/2019-01-21_14-37-03.png)
![](/uploads/2019/01/2019-01-21_14-37-18.png)
![](/uploads/2019/01/2019-01-21_14-45-03.png)
![](/uploads/2019/01/2019-01-21_14-45-21.png)
![](/uploads/2019/01/2019-01-21_14-46-45.png)
![](/uploads/2019/01/2019-01-21_14-47-21.png)

Once the VM powers back on, log in and enable SSH so that we can run some additional commands to update the OS and prepare it for cloning use

![](/uploads/2019/01/2019-01-21_14-51-26.png)
<aside class="info-block"><p>Optional: To update ESXi to the latest version, connect to the host via SSH and run the following:</p></aside>

***At the time of this writing, the latest version is Build 11675023 as per profile used below, be sure to change the profile number***

```bash
esxcli network firewall ruleset set -e true -r httpClient
esxcli software profile update -p ESXi-6.7.0-20190104001-standard \
-d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml
esxcli network firewall ruleset set -e false -r httpClient
```

<aside class="info-block"><p>Optional: To update the latest version of the ESXi Host client, run the following:</p></aside>
```bash
esxcli software vib install -v "http://download3.vmware.com/software/vmw-tools/esxui/esxui-signed-latest.vib"
```

To prepare the VM for cloning use, run the following:

```bash
esxcli system settings advanced set -o /Net/FollowHardwareMac -i 1
sed -i 's#/system/uuid.*##' /etc/vmware/esx.conf
./sbin/auto-backup.sh
```

At this point, you can shutdown the VM and convert it to a template for cloning use.

After cloning a VM, if you plan on joining it to a vCenter Server you will need to run the following on each cloned instance via SSH.

```bash
esxcli storage vmfs snapshot resignature -l datastore1
```

Well, that about does it!  Hope you all enjoyed this post!

-virtualex-

References:

- [How to properly clone nested ESXi VM](https://www.virtuallyghetto.com/2013/12/how-to-properly-clone-nested-esxi-vm.html)
- [Nested ESXi enhancements in vSphere 6.5](https://www.virtuallyghetto.com/2016/10/nested-esxi-enhancements-in-vsphere-6-5.html)
