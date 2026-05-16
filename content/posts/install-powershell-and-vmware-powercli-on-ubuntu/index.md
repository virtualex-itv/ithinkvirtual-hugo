{
  "title": "Install PowerShell and VMware PowerCLI on Ubuntu",
  "date": "2018-03-04T20:55:41",
  "lastmod": "2018-03-31T11:27:42",
  "slug": "install-powershell-and-vmware-powercli-on-ubuntu",
  "url": "/posts/install-powershell-and-vmware-powercli-on-ubuntu/",
  "draft": false,
  "description": "",
  "wordpress_id": 1197,
  "wordpress_url": "https://ithinkvirtual.com/2018/03/04/install-powershell-and-vmware-powercli-on-ubuntu/",
  "featured_image": "/uploads/2018/03/Ubuntu_PCLI_BG.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "PowerCLI",
    "Ubuntu",
    "VMware",
    "vSphere"
  ],
  "years": [
    "2018"
  ],
  "aliases": [
    "/2018/03/04/install-powershell-and-vmware-powercli-on-ubuntu/"
  ],
  "comments": []
}

Just a few days ago, [PowerShell Core v6.0](https://docs.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-core-60?view=powershell-6) was released for Windows, Linux, and macOS systems.  Alongside this release came the release of [VMware PowerCLI 10.0.0.78953](https://www.powershellgallery.com/packages/VMware.PowerCLI/10.0.0.7895300) which is VMware's own "PowerShell-like" utility.

In my previous posts ([here](/2018/03/04/install-powershell-and-vmware-powercli-on-macos/) and [here](/2018/03/04/install-powershell-and-vmware-powercli-on-centos/)), I covered how to install those on to a macOS 10.13.x "High Sierra" system and a CentOS 7 system.  In this post, I am going to show how to install both on to an Ubuntu 17.10 system as this is another common distro which I also use in my environments.  Let's get to it!

<aside class="info-block"><p>If you&#x27;re interested in installing this on other Linux distros, please consult the following link.</p></aside>

There is a prerequisite needed before PowerShell can be installed on Ubuntu and that is to install "*curl*" and then add the PowerShell Core repository (recommended) to your system.

To install curl, enter the following.

```bash
sudo apt-get install -y curl
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_15-08-20.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_15-08-41.png" alt="" loading="lazy">
</figure>

To add the PowerShell Core repository to Ubuntu, run the following command.  Enter your password if prompted

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_15-09-30.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_15-09-16.png" alt="" loading="lazy">
</figure>

To register the repository, enter the following command.  Again, enter your password if prompted.

```bash
curl https://packages.microsoft.com/config/ubuntu/17.04/prod.list | sudo tee /etc/apt/sources.list.d/microsoft.list
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_15-10-02-1024x409.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_15-10-16-1024x409.png" alt="" loading="lazy">
</figure>

Great!  With the prerequisites complete, it's time to install PowerShell Core 6.0.1.  Run the following command to do so and enter your password when prompted.

```bash
sudo apt-get install -y powershell
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_15-12-22-1024x409.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_15-13-37-1024x409.png" alt="" loading="lazy">
</figure>

Awesome!  Now, to launch a PowerShell session in CentOS, enter the following.

```bash
pwsh
```

![](/uploads/2018/03/2018-03-04_15-14-16-1024x409.png)

Within a PowerShell session, you can check the version of PowerShell by running the following.

```powershell
$PSVersionTable.PSVersion
```

![](/uploads/2018/03/2018-03-04_8-59-54-1024x428.png)

As new versions of PowerShell are released, simply update by running the following command.

```bash
sudo apt-get upgrade -y powershell
```

While leveraging the PowerShell Core repository is the recommended installation method, there are alternate methods as well.  For more information on that along with uninstallation commands, please see the following [link](https://github.com/PowerShell/PowerShell/blob/master/docs/installation/linux.md#ubuntu-1704).

Congratulations!  You've successfully installed PowerShell Core 6.0.1 onto Ubuntu!  Next comes the fun stuff for us VMware enthusiasts, installing VMware PowerCLI from the "PSGallery".  Let's continue!

Since VMware PowerCLI has moved from being its own native installer to the PSGallery, the PSGallery needs to be "Trusted" before anything from it can be installed.  To trust the PSGallery, entering the following command in the PowerShell session.

<aside class="info-block"><p>This is optional and if it is skipped, you will be prompted to trust the gallery when entering the PowerCLI module install command</p></aside>
```powershell
Set-PSRepository -Name "PSGallery" -InstallationPolicy "Trusted"
```
![](/uploads/2018/03/2018-03-04_9-00-48-1024x428.png)

Next, run the following command to install the VMware.PowerCLI module.  This will find and install the latest version of the module available in the PSGallery

```powershell
Find-Module "VMware.PowerCLI" | Install-Module -Scope "CurrentUser" -AllowClobber
```

<aside class="info-block"><p>Alternatively, you could set the &quot;-Scope&quot; parameter to &quot;AllUsers&quot; and if you wanted to install a different version you could use the &quot;-RequiredVersion&quot; parameter and specify the version number.</p></aside>
<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-04_9-01-48-1024x428.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-04_9-02-13-1024x428.png" alt="" loading="lazy">
</figure>

Once this finishes, we can check to make sure the module is installed by running the following command.

```powershell
Get-Module "VMware.PowerCLI" -ListAvailable | FT -Autosize
```

![](/uploads/2018/03/2018-03-04_9-03-36-1024x428.png)

And if you'd like to see all of the VMware installed modules, run the following.

```powershell
Get-Module "VMware.*" -ListAvailable | FT -Autosize
```

![](/uploads/2018/03/2018-03-04_9-05-16-1024x539.png)

As new versions of VMware.PowerCLI are released, you can run the following command to update it.

```powershell
Update-Module "VMware.PowerCLI"
```

With VMware.PowerCLI now installed, you can connect to your vCenter Server or ESXi host and begin using its cmdlets to obtain information or automate tasks!

I went ahead and ran the following to ensure the module was imported.

```powershell
Import-Module "VMware.PowerCLI"
```

![](/uploads/2018/03/2018-03-04_9-06-28-1024x428.png)

I noticed one caveat, the SRM module does not seem to be supported in PowerShell Core, so I hope that gets resolved soon.

![](/uploads/2018/03/2018-03-04_9-06-46-1024x428.png)

Let's test connecting to vCenter server...

```powershell
Connect-VIServer -Server "<Server_Name>"
```

I also noticed an error when running the above command stating that the "InvalidCertificateAction" setting was "Unset" and not supported.

![](/uploads/2018/03/2018-03-04_9-09-21-1024x428.png)

To bypass this, enter the following command and then enter "Y" when prompted.  This will set the parameter for the current user.

```powershell
Set-PowerCLIConfiguration -InvalidCertificateAction "Ignore"
```

![](/uploads/2018/03/2018-03-04_9-11-30-1024x428.png)
<aside class="info-block"><p>Alternatively, you can also use the &quot;-Scope&quot; parameter and enter &quot;Session&quot;, &quot;User&quot;, or &quot;AllUsers&quot; to apply the setting to those options respectively.</p></aside>

Now, if we try to connect to vCenter again, we should be successful.

![](/uploads/2018/03/2018-03-04_12-00-46-1024x428.png)

Well, that about does it!  I hope that you have found this post useful and I thank you for stopping by and reading my content.  Until next time!

-virtualex-

- [Install PowerShell and VMware PowerCLI on macOS](/2018/03/04/install-powershell-and-vmware-powercli-on-macos/)
- [Install PowerShell and VMware PowerCLI on CentOS](/2018/03/04/install-powershell-and-vmware-powercli-on-centos/)
