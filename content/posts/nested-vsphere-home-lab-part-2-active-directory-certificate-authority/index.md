{
  "title": "Nested vSphere Home Lab - Part 2 - Active Directory & Certificate Authority",
  "date": "2023-04-23T21:05:13",
  "lastmod": "2023-04-28T12:49:08",
  "slug": "nested-vsphere-home-lab-part-2-active-directory-certificate-authority",
  "url": "/posts/nested-vsphere-home-lab-part-2-active-directory-certificate-authority/",
  "draft": false,
  "description": "",
  "wordpress_id": 1826,
  "wordpress_url": "https://ithinkvirtual.com/2023/04/23/nested-vsphere-home-lab-part-2-active-directory-certificate-authority/",
  "featured_image": "/uploads/2023/04/2023-04-23_16-29-33.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Nested Virtualization",
    "sophos xg",
    "vExpert",
    "VMware",
    "vSphere",
    "Windows Server"
  ],
  "years": [
    "2023"
  ],
  "aliases": [
    "/2023/04/23/nested-vsphere-home-lab-part-2-active-directory-certificate-authority/"
  ],
  "comments": []
}

## Intro

Welcome back! In my [previous](/2023/04/23/nested-vsphere-home-lab-part-1-sophos-firewall/) post, I covered the deployment and configuration of a virtual [Sophos XG Firewall](https://www.sophos.com/en-us/products/free-tools/sophos-xg-firewall-home-edition.aspx) router appliance to provide routing services for the nested lab environment.

### Active Directory

Next, I will cover the way I like to quickly configure my Active Directory Server and respective services.  Typically, I leverage [Windows Server Core](https://learn.microsoft.com/en-us/windows-server/get-started/install-options-server-core-desktop-experience) OS for my needs but as this server will also serve as a "jump host" for the nested lab, I decided to install the Desktop Experience (GUI) version of [Windows Server 2022](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022) Datacenter Edition.

![](/uploads/2023/04/2023-03-24_14-36-29.png)
<aside class="info-block"><p>The following section(s) assume that you have a working Windows Server virtual machine as creating a Windows Server VM is out-of-scope for this post, so I will not cover that.</p></aside>

As mentioned, since I typically use Core versions of Windows Server, thus it is managed via PowerShell commands so to set up my server as a Domain Controller, I'll run the following from an elevate PowerShell session.

```powershell
###1st DC###
Import-Module ServerManager
Add-WindowsFeature -Name RSAT-AD-Tools

Install-WindowsFeature -Name AD-Domain-Services, DNS -IncludeManagementTools -Verbose

Import-Module ADDSDeployment -Verbose

# Create password
$Password = Read-Host -Prompt 'Enter SafeMode Admin Password' -AsSecureString 

Install-ADDSForest -CreateDnsDelegation:$false -DatabasePath "C:\Windows\NTDS" -DomainMode "WinThreshold" -DomainName "demo.lab" -DomainNetbiosName "DEMO" -ForestMode "WinThreshold" -InstallDns:$true -LogPath "C:\Windows\NTDS" -NoRebootOnCompletion:$true -SysvolPath "C:\Windows\SYSVOL" -SafeModeAdministratorPassword $Password -Force:$true -Verbose

# Install DHCP
Install-WindowsFeature DHCP -IncludeManagementTools -Verbose
netsh dhcp add securitygroups
Restart-Service dhcpserver -Verbose

Add-DhcpServerInDC -DnsName "dc1.demo.lab" -Verbose
Get-DhcpServerInDC

Set-ItemProperty -Path registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ServerManager\Roles\12 -Name ConfigurationState -Value 2

Set-DhcpServerv4DnsSetting -ComputerName "dc1.demo.lab" -DynamicUpdates "Always" -DeleteDnsRRonLeaseExpiry $True

$Credential = Get-Credential
Set-DhcpServerDnsCredential -Credential $Credential -ComputerName "dc1.demo.lab"

# Enable Sysvol for GPO shared store
Get-Itemproperty -path 'HKLM:SYSTEM\CurrentControlSet\Services\Netlogon\Parameters' -Name 'SysVolReady' -Verbose
Set-Itemproperty -path 'HKLM:SYSTEM\CurrentControlSet\Services\Netlogon\Parameters' -Name 'SysVolReady' -Value '1' -Verbose

# Enable Recycle Bin
$Params = @{
    "Identity" = 'Recycle Bin Feature'
    "Scope"    = 'ForestOrConfigurationSet'
    "Target"   = 'demo.lab'
  }
  
Enable-ADOptionalFeature @Params -Verbose
```

As I mentioned previously, this lab will use a single server for all Active Directory services but in my physical lab, I tend to run (2) Domain Controllers so if you'd like to configure a second server for the nested lab, you can do so by standing up a 2nd Windows Server OS and running the following on the 2nd server (DC2):

<aside class="info-block"><p>: Be sure to modify the IP&#x27;s and Domain Name.</p></aside>

```powershell
###2nd DC###
Import-Module ServerManager
Add-WindowsFeature -Name RSAT-AD-Tools

Install-WindowsFeature -Name AD-Domain-Services, DNS -IncludeManagementTools -Verbose

Import-Module ADDSDeployment -Verbose

# Create password

$Password = Read-Host -Prompt 'Enter SafeMode Admin Password' -AsSecureString

Get-DnsClientServerAddress

# Set the correct InterfaceIndex from previous command
Set-DnsClientServerAddress -InterfaceIndex 5 -ServerAddresses ("10.100.1.10","127.0.0.1") -Verbose

Install-ADDSDomainController -NoGlobalCatalog:$false -CreateDnsDelegation:$false -Credential (Get-Credential "LAB\Administrator") -CriticalReplicationOnly:$false -DatabasePath "C:\Windows\NTDS" -DomainName "demo.lab" -InstallDns:$true -LogPath "C:\Windows\NTDS" -NoRebootOnCompletion:$true -SiteName "Default-First-Site-Name" -ReplicationSourceDC "dc1.demo.lab" -SysvolPath "C:\Windows\SYSVOL" -SafeModeAdministratorPassword $Password -Force:$true -Verbose

# Install DHCP Services

Install-WindowsFeature DHCP -IncludeManagementTools -Verbose
netsh dhcp add securitygroups
Restart-Service dhcpserver -Verbose

Add-DhcpServerInDC -DnsName "dc2.demo.lab" -Verbose
Get-DhcpServerInDC

Set-ItemProperty -Path registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ServerManager\Roles\12 -Name ConfigurationState -Value 2

Set-DhcpServerv4DnsSetting -ComputerName "dc2.demo.lab" -DynamicUpdates "Always" -DeleteDnsRRonLeaseExpiry $True

$Credential = Get-Credential
Set-DhcpServerDnsCredential -Credential $Credential -ComputerName "dc2.demo.lab"

# Enable Sysvol for GPO shared store

Get-Itemproperty -path 'HKLM:SYSTEM\CurrentControlSet\Services\Netlogon\Parameters' -Name 'SysVolReady' -Verbose
Set-Itemproperty -path 'HKLM:SYSTEM\CurrentControlSet\Services\Netlogon\Parameters' -Name 'SysVolReady' -Value '1' -Verbose

```

Then switch back to DC1 and run the following so set its DNS configuration to point to DC2 as the primary and itself as the secondary, this way bother servers are pointing to the opposite server as it's primary:

```powershell
###1st DC###
Get-DnsClientServerAddress

#Set the correct InterfaceIndex from previous command
Set-DnsClientServerAddress -InterfaceIndex 5 -ServerAddresses ("10.100.1.20","127.0.0.1") -Verbose
```

### Certificate Authority

In this lab setup, I am also going to configure this Jumpbox / Active Directory Domain Controller to serve as an Enterprise Root Certificate Authority, but in a traditional lab, I would separate this on it's own VM.

To configure the server as a Certificate Authority for the lab, I will run the following PowerShell commands while logged in as the domain "Administrator" account:

```powershell
Get-DnsClientServerAddress

# Set the correct InterfaceIndex from previous command
Set-DnsClientServerAddress -InterfaceIndex 5 -ServerAddresses ("127.0.0.1") -Verbose

# Run the following if you have an external CA with (2) DNS Servers
Set-DnsClientServerAddress -InterfaceIndex 5 -ServerAddresses ("10.100.1.10","10.100.1.20") -Verbose

# Join pc to domain if needed
Add-Computer -DomainName "demo.lab" -Credential (Get-Credential "DEMO\Administrator") -Restart -Confirm:$false -Verbose

Import-Module ServerManager
Add-WindowsFeature -Name RSAT-AD-Tools

#region
# Install IIS Remote Mgmt if CA is installed on Server Core OS
Install-WindowsFeature Web-Mgmt-Service
Enable-NetFirewallRule -DisplayGroup "Windows Remote Management"
Set-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\WebManagement\Server -Name EnableRemoteManagement -Value 1
Set-Service -Name WMSVC -StartupType Automatic
Start-Service WMSVC 

# Run the following on the remote system used to manage IIS
# Desktop OS
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-WebServerManagementTools" -All -Verbose 
# Server OS
Install-WindowsFeature Web-Mgmt-Service -IncludeManagementTools -Verbose
#endregion

# Install ADCS
Install-WindowsFeature Adcs-Cert-Authority -IncludeManagementTools -Verbose

$CA_Name = "demo-lab-ca"
$CP_Name = "RSA#Microsoft Software Key Storage Provider"
Install-AdcsCertificationAuthority -CACommonName $CA_Name -CAType EnterpriseRootCa -CryptoProviderName $CP_Name -Credential (Get-Credential "DEMO\Administrator") -KeyLength 2048 -HashAlgorithmName SHA256 -ValidityPeriod Years -ValidityPeriodUnits 10 -Force -Verbose

Install-WindowsFeature ADCS-Web-Enrollment -IncludeManagementTools -Verbose

Install-AdcsWebEnrollment -Force -Verbose
```

At this point, if you navigate to the URL of the CA server at `http://[IP or FQDN]/certsrv` , you should be prompted to authenticate and see the following page(s).

![](/uploads/2023/04/2023-04-23_15-37-05-1024x595.png)
![](/uploads/2023/04/2023-04-23_15-37-21-1024x595.png)

From here, I usually download and install the CA Certificate locally and then create a GPO and push the certificate to all windows machines in the domain.

![](/uploads/2023/04/2023-04-23_15-43-00.png)

**Right-click** the downloaded certificate file and click **Install Certificate**. Choose **Local Machine** as the store location and click **Next**. Select **Place all certificates in the following store:** then **Browse** and select **Trusted Root Certification Authorities**, then click **OK**, **Next**, **Finish**.

To create a GPO, open the Group Policy Management utility. I already had the admin MMC console configured with this snap-in so I was able to access this quickly and setup a GPO.

![](/uploads/2023/04/2023-04-23_16-27-31-1024x595.png)

This at least gets us started so we can hop back in and configure additional users, groups, GPOs, DNS record, DHCP Scopes, etc. as needed later on, but we're not done just yet! I like to configure a secure connection to the Web Enrollment Server URL so to do so, I'll need to configure that in IIS.

Open up **IIS Manager** on the CA Server, navigate to the **Default Web Site** and click on **Bindings**, then click **Add**. Set the **Type** to **https**, then select the **SSL certificate** that is named after the CA server from the dropdown menu, in my case **dc.demo.lab** and click **OK**, then **Close**. Next, **CertSrv**, then double-click **SSL Settings**. Enable the **Require SSL** checkbox, then click **Apply**. Afterwards, navigate again to the Web Enrollment Server URL, this time using `https://[FQDN]/certsrv`, Authenticate if asked to do so, and now we can see that we have a certificate securing our connection.

![](/uploads/2023/04/2023-04-26_17-50-58.png)
![](/uploads/2023/04/2023-04-26_17-51-45.png)
![](/uploads/2023/04/2023-04-26_17-52-45.png)
![](/uploads/2023/04/2023-04-26_17-53-38.png)
![](/uploads/2023/04/2023-04-26_17-55-05.png)

I also like to generate Certificate Signing Requests (CSRs) using the [OpenSSL](https://www.openssl.org/) utility which is commonly used to generate CSRs or certificates for VMware products, so I will install via my favorite CLI driven application/package management tool...[Chocolatey](https://community.chocolatey.org/)!

To install Chocolatey, from an elevated shell run the following:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Then, install OpenSSL with the following command:

```powershell
# Optional
choco feature enable -n allowGlobalConfirmation
choco feature enalbe -n useRememberedArgumentsForUpgrades

# Install OpenSSL
choco install openssl

# Install IIS Manager if remotely managing IIS
choco install inetmgr
```

Next, I will create a certificate template which will be used to sign CSRs with later on by following the instructions in VMware KB Article [2112009](https://kb.vmware.com/s/article/2112009). And to round things off, the last thing I will do is enable certificate auto-enrollment following the instructions in this [guide](https://learn.microsoft.com/en-us/windows-server/networking/core-network-guide/cncg/server-certs/configure-server-certificate-autoenrollment).

In the next post, I will cover how to deploy the nested ESXi VMs and vCenter Server.

I hope you've enjoyed the material thus far, and I thank you for reading!

--virtualex
