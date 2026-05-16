{
  "title": "System Center Configuration Manager: Step-by-Step - Server Preparation and Prerequisites Installation",
  "date": "2018-03-31T19:23:21",
  "lastmod": "2019-01-17T22:12:16",
  "slug": "system-center-configuration-manager-server-preparation-and-prerequisites",
  "url": "/posts/system-center-configuration-manager-server-preparation-and-prerequisites/",
  "draft": true,
  "description": "",
  "wordpress_id": 946,
  "wordpress_url": "https://ithinkvirtual.com/?p=946",
  "featured_image": "/uploads/2017/11/2017-11-05_17-38-26-1024x592.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "System Center Configuration Manager"
  ],
  "years": [
    "2018"
  ],
  "aliases": [],
  "comments": []
}

To kick things off, I will quickly cover the prerequisites for proper server configuration and preparation.  In this guide, System Center Configuration Manager will be installed on Microsoft Windows Server 2016 running as a VMware virtual machine.  This server will need to be joined to a domain, and my domain controller is also running on Windows Server 2016.

To conform with best practices, even for this lab environment, I have configured this Primary Site Server as follows:

## Compute Resources:

- 2 vCPU
  - Hot Add not enabled
- 16GB RAM
  - Hot Plug not enabled

## Disk Layout: (I will let you determine the proper sizes for your disks, as I am demonstrating in a lab, my sizes are much smaller due to storage limitations)

- Disk 0 - OS
  - Controller 0:0
- Disk 1 - Data
  - Controller 1:0
  - 1024k aligned
  - 64K unit size
- Disk 2 - SQL DB
  - Controller 1:1
  - 1024k aligned
  - 64K unit size
- Disk 3 - User DB
  - Controller 2:0
  - 1024k aligned
  - 64K unit size
- Disk 4 - User DB Logs
  - Controller 3:0
  - 1024k aligned
  - 64K unit size
- Disk 5 - TempDB & Logs
  - Controller 1:2
  - 1024k aligned
  - 64K unit size
- Disk 6 - Backups
  - Controller 1:3
  - 1024k aligned
  - 64K unit size

![](/uploads/2017/11/2017-11-05_17-38-26-1024x592.png)

## Prerequisites:

### Active Directory Schema Extension

- Login to your Domain Controller as a member of the **Schema Admins** global security group
- Mount the SCCM installation media and run **.\SMSSETUP\BIN\extadsch.exe**
- Check the results by opening the **ExtADSch.log** located on the root of the system drive

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_17-44-34-300x174.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_17-48-39-300x174.png" alt="" loading="lazy">
</figure>

### Create the System Management Container

- On your Domain Controller, launch **ADSI Edit**
- Expand the containers structure tree on the left, select the **CN=System** container, right-click and select **New > Object**

![](/uploads/2017/11/2017-11-05_17-50-33-300x174.png)

- Select **Container**
- Enter **System Management**

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_17-51-31-300x261.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_17-52-16-300x261.png" alt="" loading="lazy">
</figure>

### Set Security Permissions

- Right-click the new **CN=System Management** container and select **Properties**

![](/uploads/2017/11/2017-11-05_17-52-56-300x174.png)

- Select the **Security** tab, and add the SCCM Site Server computer account and grant it **Full Control**, then click **Advanced**

![](/uploads/2017/11/2017-11-05_17-54-43-265x300.png)

- Select the Site Server computer account and click **Edit**

![](/uploads/2017/11/2017-11-05_17-57-13-300x205.png)

- In the Applies to list, select **This object and all descendant objects**, then click **OK,** then **OK** again and close the ADSIEdit console

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_17-57-57-300x196.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_18-00-44-300x205.png" alt="" loading="lazy">
</figure>

### Create SCCM Domain and Service Accounts

In this lab demonstration, I have created the following Groups and Users/Service Accounts.  Feel free to create the same accounts or change at your own discretion.

- **SCCM Admins (Group)**
- **SCCM Site Servers (Group)**
- **SCCM Admin (User)**
- **SCCM Client Push (User)**
- **SCCM Join Domain (User)**
- **SCCM Network Access Authority (User)**
- **SCCM SQL Reporting Service (User)**
- **SCCM SQL Service (User)**

![](/uploads/2017/11/2017-11-05_18-05-34-300x213.png)

### Network Configuration

I'll assume this has already been done prior to joining the Site Server to the domain but just in case, please ensure that you have set a static IP address for the SCCM Site Server.

### Firewall Configuration

I have created the following batch script and posted it on my GitHub [here](https://github.com/virtualex-itv/itv-lib/blob/master/batch/bat/sccm-fw_cfg.bat).  Ensure that your Firewall is on and run this script via an elevated command prompt or PowerShell on your Site Server.

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_18-16-37-300x188.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_18-15-18-300x190.png" alt="" loading="lazy">
</figure>

### Hidden Files

You can prevent SCCM from placing content on drives you don't want content on.  You can do so by creating an empty file called **no_sms_on_drive.sms** and then place the file in the root of each drive that you want to prevent SCCM from putting content.  I choose to place this file on the root of all my drives except for the **D:** drive.  You can read more about hidden files [here](https://blogs.technet.microsoft.com/configurationmgr/2012/09/17/controlling-configuration-manager-2012-using-hidden-files/).

![](/uploads/2017/11/2017-11-05_18-19-01-300x174.png)

### Roles and Features

Before you can install SCCM on your server, you will need to install the following Windows Server Roles and Features.

- **.Net Framework 3.5**
- **.Net Framework 4**
- **IIS**
- **Remote Differential Compression (RDC)**
- **BITS**
- **ASP.Net**

Rather than using the GUI to install these, I've created the following PowerShell script to install said Roles and Features.  You can find this on my GitHub as well [here](https://github.com/virtualex-itv/itv-lib/blob/master/powershell/powershell/sccm-roles_features.ps1).

![](/uploads/2017/11/2017-11-05_18-46-19-300x238.png)

### Local Administrator Accounts

Add the following groups to the Local Administrator group on the Site Server.

- **SCCM Admins** (Be sure to add SCCM Admin and any other Domain User accounts you need to this group)
- **SCCM Site Servers** (Be sure to add the SCCM Servers' Computer Object account to this group)

![](/uploads/2017/11/2017-11-05_19-29-24-300x174.png)

### System CLR Types for SQL Server 2014

This version is compatible with SQL Server 2017.  Download from [here](https://www.microsoft.com/en-us/download/details.aspx?id=42295) and install.

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_18-58-44-300x231.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_18-59-16-300x231.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_18-59-52-300x231.png" alt="" loading="lazy">
</figure>

### Report Viewer 2015 Runtime

This version is compatible with SQL Server 2017.  Download from [here](https://www.microsoft.com/en-us/download/details.aspx?id=45496) and install.

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_19-00-17-300x231.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-00-34-300x231.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-01-09-300x231.png" alt="" loading="lazy">
</figure>

### Windows ADK - Windows 10 (1709)

Download from [here](https://developer.microsoft.com/en-us/windows/hardware/windows-assessment-deployment-kit) and install

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_19-05-07-300x222.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-05-34-300x222.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-06-39-300x222.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-24-26-300x222.png" alt="" loading="lazy">
</figure>

### Windows SDK - Windows 10 (1709)

<aside class="info-block"><p>Optional** - I chose to install this just for the MSI Tools</p></aside>

Download from [here](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk) and install

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_19-24-54-300x222.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-25-10-300x222.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-25-42-300x222.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_19-26-08-300x222.png" alt="" loading="lazy">
</figure>

And that's that!  Now you're ready to install and configure Microsoft SQL Server.  I hope you've found this helpful, thanks for reading and I'll catch you all on the next one!

Next |

[Previous](/posts/system-center-configuration-manager-current-branch-step-by-step-installation-guide/) |
