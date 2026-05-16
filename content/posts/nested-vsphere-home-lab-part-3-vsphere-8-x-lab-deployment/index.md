{
  "title": "Nested vSphere Home Lab – Part 3 – vSphere 8.x Lab Deployment",
  "date": "2024-01-06T20:22:55",
  "lastmod": "2025-01-08T19:33:24",
  "slug": "nested-vsphere-home-lab-part-3-vsphere-8-x-lab-deployment",
  "url": "/posts/nested-vsphere-home-lab-part-3-vsphere-8-x-lab-deployment/",
  "draft": false,
  "description": "",
  "wordpress_id": 1882,
  "wordpress_url": "https://ithinkvirtual.com/2024/01/06/nested-vsphere-home-lab-part-3-vsphere-8-x-lab-deployment/",
  "featured_image": "/uploads/2024/01/2024-01-06_15-14-52.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "vExpert",
    "VMware",
    "vSphere"
  ],
  "years": [
    "2024"
  ],
  "aliases": [
    "/2024/01/06/nested-vsphere-home-lab-part-3-vsphere-8-x-lab-deployment/"
  ],
  "comments": []
}

## Intro

Welcome back! In my [previous](/2023/04/23/nested-vsphere-home-lab-part-2-active-directory-certificate-authority/) post, I covered the deployment and configuration of an Active Directory and Microsoft Certificate Authority server(s) for the nested lab environment.

Next, I will cover the steps used to deploy the nested lab via William Lam's Automated Nested Lab Deployment [script](https://github.com/lamw/vsphere-8-lab-deployment).  This script makes it easy to deploy a set of vSphere Hypervisor (ESXi) VMs, along with a VMware vCenter Server Appliance virtual machine to manage the nested lab environment.

I will not go into detail here on how to use William's script, as he's done a fine job documenting the process on both his [blog](https://williamlam.com/2022/10/automated-vsphere-vsan-8-lab-deployment-script.html) and [GitHub](https://github.com/lamw/vsphere-8-lab-deployment) pages.  However, what I will cover are the tweaks I've made to deploy and configure the lab environment to my needs for this series.  So let's get to it!

![](/uploads/2024/01/2024-01-05_19-56-57.png)

### Physical Hardware

As I've stated in an earlier post, I am deploying this nested lab on a Dell PowerEdge R720 server. I swapped out the original dual CPUs in favor of dual Intel(R) Xeon(R) CPU E5-2697 v2 @ 2.70GHz CPUs so that I could leverage my 768GB of available RAM that I was able to score fairly cheap on eBay.

I also swapped out the RAID controller for an H710p which I also scored for cheap on eBay, so that the server would recognize the local disks with ESXi 8.0.

For shared storage, I have some SSDs configured as an NFS datastore from my Synology RS3618xs. I also have configured some local direct-attached storage (DAS) where I'll be deploying the nested lab to; a 1TB Timetec SSD housed in a CDROM/SATA to M.2 adapter, as well as a 2TB Samsung 970 Evo Plus M.2 in a PCI-E adapter. This is where the router and domain controller VMs reside. The latter is reserved for future use with nested VMware Cloud Foundation via the Holodeck Toolkit!

### vSphere Lab Deployment

#### Prerequisites

- [William Lam's vSphere 8 Lab Deployment Script](https://github.com/lamw/vsphere-8-lab-deployment)
- [William Lam's Nested Hypervisor OVA Appliance](https://download3.vmware.com/software/vmw-tools/nested-esxi/Nested_ESXi8.0_IA_Appliance_Template_v2.ova)
- [vCenter Server 8](https://customerconnect.vmware.com/downloads/get-download?downloadGroup=VC800)
- [PowerCLI ≥ 12.1](https://developer.vmware.com/docs/15315/GUID-ACD2320C-D00F-4CCE-B968-B3C41A95C085.html)
- [PowerShell Core](https://github.com/PowerShell/PowerShell)

#### Tweaks & Configuration

After obtaining and modifying the deployment script to point to the required binaries and networking set to the nested trunked portgroup, I ran the deployment and was provided with deployed and configured vCenter Server Appliance and a number of ESXi host VMs. I then modified the script again, this time changing the ESXi VM hostnames and IP addresses so that I can deploy a second cluster of hosts for the lab environment. I also modified the following and redeployed the script:

<aside class="info-block"><p>Modifying the following is not normally recommended. Do this at your own risk.</p></aside>
```powershell
$preCheck = 1
$confirmDeployment = 1
$deployNestedESXiVMs = 1
$deployVCSA = 0
$setupNewVC = 0
$addESXiHostsToVC = 1
$configureVSANDiskGroup = 1
$configureVDS = 1
$clearVSANHealthCheckAlarm = 1
$moveVMsIntovApp = 0
```

Once the script completed successfully, I logged into vCenter and verified that the additional hosts were present. Afterwards, I moved some things around, created/renamed and configured clusters to my liking.

I also decided to reconfigure the networking on each ESXi host VM and add some additional vmkernel ports for proper network traffic for vMotion & vSAN.

The final thing that I did was upgrade the entire environment, vCenter Server and all ESXi hosts, to their latest respective versions which, at the time of this writing, was vSphere 8.0 U2a.

<figure class="image-gallery">
<img src="/uploads/2024/01/2024-01-05_19-57-14.png" alt="" loading="lazy">
<img src="/uploads/2024/01/2024-01-06_15-05-26.png" alt="" loading="lazy">
</figure>

Now, with all this complete, I now have a readily available and stable nested lab platform to begin working with various VMware products! Up next, I'll go over the deployment of the VMware Aria Suite in this nested lab for Cloud Management. Thanks for reading!
