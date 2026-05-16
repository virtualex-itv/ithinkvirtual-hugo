{
  "title": "Nested vSphere Home Lab – Part 4 – VMware Aria Suite Lifecycle Deployment & Configuration",
  "date": "2025-01-12T17:21:45",
  "lastmod": "2025-01-12T17:23:00",
  "slug": "nested-vsphere-home-lab-part-4-vmware-aria-suite-lifecycle-deployment-configuration",
  "url": "/posts/nested-vsphere-home-lab-part-4-vmware-aria-suite-lifecycle-deployment-configuration/",
  "draft": false,
  "description": "",
  "wordpress_id": 1904,
  "wordpress_url": "https://ithinkvirtual.com/2025/01/12/nested-vsphere-home-lab-part-4-vmware-aria-suite-lifecycle-deployment-configuration/",
  "featured_image": "/uploads/2025/01/848b3966-c49c-4d31-adcc-75a69204bc67.webp",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "vExpert",
    "VMware"
  ],
  "years": [
    "2025"
  ],
  "aliases": [
    "/2025/01/12/nested-vsphere-home-lab-part-4-vmware-aria-suite-lifecycle-deployment-configuration/"
  ],
  "comments": []
}

## Intro

Welcome back!  I know it's been some time since my last post where I covered the deployment of the nested vSphere lab, but I'd like to take a moment to thank you for coming back and supporting me! Life hits at times, and I just didn't have the time to dedicate to creating content as my family expanded and the responsibilities took over.  While time is still of the essence, I didn't want to miss out on following up the series.  In this post, I will cover the deployment and configuration of the VMware Aria Suite Lifecycle appliance to help facilitate the deployment of the remaining Aria Suite solutions.  Let's get to it!

## Objective And Tasks

Deploy and configure VMware Aria Suite Lifecycle 8.18.0.

- Deploy VMware Aria Suite Lifecycle.
- Add certificates, licenses, and passwords to the Locker.
- Replace the VMware Aria Suite Lifecycle certificate.
- Update/Patch VMware Aria Suite Lifecycle.
- Add a Datacenter and configure vCenter in VMware Aria Suite Lifecycle.
- Map VMware Aria Suite product binaries and patches.

## Deployment

Download the VMware Aria Suite Lifecycle product binaries from the Broadcom Support portal.

<aside class="info-block"><p>Download VMware Aria Suite Lifecycle 8.18 Easy Installer version.</p></aside>

Mount the VMware Aria Suite Lifecycle Installer.

Launch the installer (**InstallerLite.exe**) from the **<*Drive_Letter*>:\vrlcm-ui-installer\win32-lite** directory.

When the **VMware Aria Easy Installer** launches, click **INSTALL**.  On the **Introduction** tab, click **NEXT**.

On the **End User License Agreement** tab, select the checkbox to accept the terms of the license agreement and click **NEXT**.

<aside class="info-block"><p>Optionally, deselect the checkbox to Join the VMware Customer Experience Program.</p></aside>

On the **Appliance Deployment Target** tab, fill out the required fields and click **NEXT**.  Click **ACCEPT** on the **Certificate Warning** pop-up.

**Select a Location** to deploy the VMware Aria Suite Lifecycle appliance and click **NEXT**.   **Select a Compute Resource** and click **NEXT**.  **Select a Storage Location** and click **NEXT**.

On the **Network Configuration** tab, fill in the required fields and click **NEXT**.  Enter a password on the **Password Configuration** tab and click **NEXT**.

On the **VMware Aria Suite Lifecycle Configuration** tab, fill in the required fields and click **NEXT**.

<aside class="info-block"><p>Optional: Set the Increase Disk Size in GB to a value other than 0. This will add additional space for the VMware Aria Suite binaries and/or updates and patches.</p></aside>

Review the **Summary** and click **Submit**.

Monitor the deployment until it completes successfully. Once complete, you'll be presented with a URL to access the solutions web user interface.

At this point you should now be able to access the VMware Aria Suite Lifecycle web user interface, and can login with admin@local and the password specified at the time of deployment.

## Configuration

### Locker

Login to the VMware Aria Suite Lifecycle application and click on Locker.

On the Certificates tab, this is where you can GENERATE CSR, GENERATE a certificate, or IMPORT a certificate.  
  
I have already created a signed certificate to use for all of the VMware Aria Suite solutions for this lab.
  
This was created as a wildcard certificate and I generated the CSR externally using openssl on a Windows machine with the following configuration file, and then I generated and signed the certificate against my lab's Microsoft Certificate Authority.

```ini
[ req ]
default_bits = 4096
distinguished_name = req_distinguished_name
req_extensions = v3_req_ext
prompt = no

[ req_distinguished_name ]
countryName = US
stateOrProvinceName = New Jersey
localityName = Hopatcong
organizationName = DEMO
organizationalUnitName = DEMO
commonName = aria.demo.lab

[ v3_req_ext ]
basicConstraints = CA:false
keyUsage = digitalSignature, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = *.demo.lab
IP.1 = 10.100.10.100 # lcm
IP.2 = 10.100.10.101 # idm
IP.3 = 10.100.10.102 # ops
IP.4 = 10.100.10.103 # logs
IP.5 = 10.100.10.104 # logs-vip
IP.6 = 10.100.10.106 # networks
IP.7 = 10.100.10.107 # automation
IP.8 = 10.100.10.108 # automation config
IP.9 = 10.100.10.109 # ops cloud proxy
```

The following are my rough notes on the process to generate my required files for signing the certificate and then converting it to the required format for use with VMware Aria Suite.

<aside class="info-block"><p>This is in PowerShell format but this is not an actual script so do not attempt to run this as is.</p></aside>
```powershell
$remotehost = 'demo_lab_aria'
cd "..\..\Program Files\OpenSSL-Win64"
$inOutPath = ".\bin\certs\aria"
openssl req -out $inOutPath\$remotehost.csr -newkey rsa:4096 -nodes -keyout $inOutPath\$remotehost.key -config $inOutPath\$($remotehost)_ssl.conf -sha256
```

- Sign the cert with CA.
- Download cert and chain.
- Combine the .cer, .key, and root_ca.cer into a new .pem for use with vRealize/Aria.

```powershell
$remotehost_cer = "$inOutPath\$($remotehost).cer"
$remotehost_key = "$inOutPath\$($remotehost).key"
$remotehost_ca_cer = "$inOutPath\$($remotehost_ca).cer"
$remotehost_pem = "$inOutPath\$($remotehost).pem"
```

Check if all required files exist before proceeding.

```powershell
if (Test-Path $remotehost_cer -and Test-Path $remotehost_key -and Test-Path $remotehost_ca_cer) {
    Get-Content $remotehost_cer, $remotehost_key, $remotehost_ca_cer | Set-Content $remotehost_pem -Verbose
} else {
    Write-Error "One or more required files are missing. Please check the paths."
}
```

Once this was complete, I had my new lab wildcard certificate ready for use.  
  
Click on IMPORT.  
  
Provide a Name for the certificate and click on BROWSE, then locate your generated certificate.  
  
If the certificate is valid, it will auto-populate the Private Key and Certificate Chain information.  
  
Click IMPORT and the certificate should then be successfully added.

Next, click on the Licenses tab and then click ADD LICENSE MANUALLY.  
  
Provide an License Alias name and add your License Key then click VALIDATE.  
  
This may take some time to complete the validation but once it does, click on ADD.

Next, click on the Passwords tab.  
  
There should be already be a few aliases present as they were created at the time of deployment.  
  
It is recommended best practice to create new aliases with their respective credentials for each solution.  
  
For the purposes of this lab, I am just going to create a single new password alias for all my needs.  
  
Click ADD, the enter the information into the required fields and click ADD. (Leave User Name blank)

### Replace Certificate

The VMware Aria Suite Lifecycle solution is deployed is a self-signed certificate, and I am going to change that to use the Microsoft CA-signed certificate that I created earlier.  
  
In the upper right-hand side of the screen, click the Services menu button and click on Lifecycle Operations, then click Settings > Change Certificate.  
  
Click REPLACE CERTIFICATE > NEXT.  
  
Select the certificate from the Select Certificate dropdown and click NEXT.  
  
Click on RUN PRECHECK. Once that completes successfully, click FINISH.  
  
This will switch us over to the Requests tab in Lifecycle Operations and display the current workflow to replace the certificate.  
  
If you stay on this page, the workflow will not progress since we'd need to refresh our browser session to utilize the new certificate.  
  
Refresh your browser.  
  
If you're presented with a warning, click Advanced then click Continue to  (unsafe) and you should be authenticated back in and see a successful workflow completion.  
  
In order to no longer receive this message I would also need to install the certificate locally on my machine in the [Trusted Root Certification Authorities Certificate Store](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/trusted-root-certification-authorities-certificate-store), but I will take care of that later as it is not in scope for this post.  
  
When I look at the browser certificate, I can see that it is indeed using the Microsoft CA-signed certificate that I had applied.

### Update/Patch

Navigate again to Lifecycle Operations > Settings > Product Support Pack.  
  
While, at the time of this writing, there is a [VMware Aria Suite Lifecycle 8.18 Patch 1](https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-suite-lifecycle/8-18/release-notes/vmware-aria-suite-lifecycle-818-patch-1-release-notes.html) available, updates and Product Support Packs are cumulative incorporating all updates from previous product support packs as well as patches into the latest version.  
  
At the time of this writing, the latest [Product Support Pack (PSPack4)](https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-suite-lifecycle/8-18/release-notes/vmware-aria-suite-lifecycle-818-product-support-pack-release-notes.html) is available and is newer than the patch, so those fixes are included as well.  
  
Now, anytime you plan to apply a new PSPack, it is recommended to take a snapshot of the appliance. In this case we are first only performing an upload of the PSPack4 binary, and not making any system changes.  
  
Click on UPLOAD > SELECT FILE. Select the vrlcm-8.18.0-PSPACK4.pspak file and click IMPORT.  
  
After a few moments, you'll see the request was successfully submitted with a Click here hyperlink that will open a new tab and bring you to the request workflow.  
  
Once the workflow completes, navigate back to Lifecycle Operations > Settings > Product Support Pack.  
  
Allow some time for it to load the information, and you will eventually see the new PSPack and supported Aria Suite solution versions listed under the Support for Additional Product Versions section.  
  
Click on CREATE SNAPSHOT.  
  
Enter the vCenter Hostname information and click Select vCenter Credential the select the installervCenter alias credential and click SUBMIT.  
  
Again, monitor the workflow to ensure it completes successfully. You may also login to vCenter and see a task created for the snapshot action.  
  
Back in Lifecycle Operations > Settings > Product Support Pack, click on APPLY VERSION and select the checkbox confirming that you took a snapshot and click SUBMIT.  
  
Monitor the request workflow until it completes.  
  
The user interface will change while the system applies the pspack and restarts any required services.  
  
When it completes, you'll be presented with the login screen.

### Add Datacenter and vCenter Server

Login to VMware Aria Suite Lifecycle and navigate to Lifecycle Operations >Datacenters tab in the left-hand pane.  
  
We can see here that there already is a Datacenter and a vCenter server configured and this was done for us automagically at the time of deployment.  
  
All that is needed here is to change the location of the datacenter, and for this lab, this specific vCenter is used for Management instead of being consolidated which houses both management and VI workloads. I have a separate vCenter server that I will use for VI workloads.  
  
Click the pencil icon on the right-hand side of the page next to where it says "1 vCenter" to update the datacenter's location.  
  
Update the Location field, change the Datacenter Name if you'd like, and click SAVE.  
  
Next, click the other pencil icon in the middle right-hand side of the page to modify the configured vCenter.  
  
Select Management from the vCenter Type field, then click VALIDATE.  
  
Upon successful validation, then click SAVE.

### Binary Mapping

Navigate to Lifecycle Operations > Settings > Binary Mapping.  
  
This is where we will manually map any Aria products and patch binaries and use them to deploy and/or patch any of the products managed by VMware Aria Suite Lifecycle Manager.  
  
Previously, there was a My VMware integration which allowed for providing and storing your credentials to download the binaries directly from VMware.  
  
Since the Broadcom acquisition and migration to the Broadcom portal, this integration was removed from VMware Aria Suite Lifecycle 8.18.  
  
Moving forward, for now at least, you will need to download the bits from the Broadcom Support portal manually and either upload them directly to the VMware Aria Suite Lifecycle appliance via SCP or place them on an NFS share.  
  
In my case, I have already downloaded the needed binaries and placed them on my Synology NAS so that I can leverage NFS to map the binaries.  
  
From the Product Binaries tab, click ADD BINARIES.  
  
Select NFS for the Location Type and specify the full path to the folder where the binaries are located in the Base Location field, then click DISCOVER.  
  
Select all of the products that you'd like to map and click ADD.  
  
These are all of the latest supported versions for PSPack4 as of the time of this writing.  
  
Monitor the request until it completes successfully. This will take some time to complete.  
  
Once it eventually finishes, you will see all of the products mapped and available for deployment.  
  
Next, click on Patch Binaries > ADD PATCH BINARY.  
  
Now, the only supported method of mapping patches is to upload them locally to the VMware Aria Suite Lifecycle appliance.  
  
I used WinSCP to copy the patch binary to the /data directory.  
  
With the patch uploaded to the local appliance, specify /data in the Source Location field and click DISCOVER.  
  
Select the patch binary and click ADD.  
  
Monitor the request until it is completed successfully and then you'll see the patch binary listed.

In the next post, I will cover the deployment and configuration of VMware Identity Manager for authentication.  
  
Then I will come back and configure VMware Aria Suite Lifecycle to use this Identity Source/Provider for authentication!  
  
Well, that about sums up this post! I hope you've found this information useful, and thanks for stopping by!
