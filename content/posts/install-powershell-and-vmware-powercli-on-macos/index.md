{
  "title": "Install PowerShell and VMware PowerCLI on macOS",
  "date": "2018-03-04T05:57:43",
  "lastmod": "2018-03-31T11:26:19",
  "slug": "install-powershell-and-vmware-powercli-on-macos",
  "url": "/posts/install-powershell-and-vmware-powercli-on-macos/",
  "draft": false,
  "description": "Just a few days ago, PowerShell Core v6.0 was released for Windows, Linux, and macOS systems.  Alongside this release came the release of VMware PowerCLI 10.0.0.78953 which is VMware’s own “PowerShell-like” utility.  In this post, I am going to show how to install both on to a macOS system.  Let’s get to it! There are…",
  "wordpress_id": 1140,
  "wordpress_url": "https://ithinkvirtual.com/2018/03/04/install-powershell-and-vmware-powercli-on-macos/",
  "featured_image": "/uploads/2018/03/macOS_PCLI_BG.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "macOS",
    "PowerCLI",
    "VMware",
    "vSphere"
  ],
  "years": [
    "2018"
  ],
  "aliases": [
    "/2018/03/04/install-powershell-and-vmware-powercli-on-macos/"
  ],
  "comments": []
}

Just a few days ago, [PowerShell Core v6.0](https://docs.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-core-60?view=powershell-6) was released for Windows, Linux, and macOS systems.  Alongside this release came the release of [VMware PowerCLI 10.0.0.78953](https://www.powershellgallery.com/packages/VMware.PowerCLI/10.0.0.7895300) which is VMware’s own “PowerShell-like” utility.  In this post, I am going to show how to install both on to a macOS system.  Let’s get to it!

There are a few prerequisites needed before PowerShell can be installed on macOS which I will cover, and they are as follows:

- [Homebrew](https://brew.sh) – Homebrew installs the stuff you need that Apple didn’t.
- [Homebrew-Cask](https://github.com/Homebrew/homebrew-cask) – extends Homebrew and brings its elegance, simplicity, and speed to macOS applications and large binaries alike.
- Xcode Command Line Tools

Per the instructions on the Homebrew site, copy and paste the following command into a terminal window to install Homebrew.

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

![](/uploads/2018/03/2018-03-02_10-57-42.png)

This will prompt you to press ***Enter*** to continue and the prompt you to enter your password.  It will also check if Xcode command line tools are installed, and if not, it will download and install it for you before completing the installation of Homebrew. Nice!

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-02_10-58-05.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_10-58-33.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_10-59-41.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_11-01-16.png" alt="" loading="lazy">
</figure>

Now, the next step is to install Homebrew-Cask and per its sites installation notes, copy and paste the following command into a terminal window.

```bash
brew tap caskroom/cask
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-02_11-06-10.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_11-06-38.png" alt="" loading="lazy">
</figure>

Great!  With the prerequisites complete, it’s time to install PowerShell Core 6.0.1.  Run the following command to do so and enter your password when prompted.

```bash
brew cask install powershell
```

<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-02_11-07-18.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_11-08-23.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_11-09-22.png" alt="" loading="lazy">
</figure>

Awesome!  Now, to launch a PowerShell session in macOS, enter the following in terminal.

```bash
pwsh
```

![](/uploads/2018/03/2018-03-02_11-10-11.png)

Within a PowerShell session, you can check the version of PowerShell by running the following.

```powershell
$PSVersionTable.PSVersion
```

![](/uploads/2018/03/2018-03-02_12-01-44.png)

As new versions of PowerShell are released, simply update the Homebrew formulae and update PowerShell by running the following commands in terminal.

```bash
brew update
brew cask upgrade powershell
```

While leveraging Homebrew is the recommended installation method, there are alternate methods as well.  For more information on that along with uninstallation commands, please see the following [link](https://github.com/PowerShell/PowerShell/blob/master/docs/installation/macos.md).

Congratulations!  You’ve successfully installed PowerShell Core 6.0.1 onto macOS!  Next comes the fun stuff for us VMware enthusiasts, installing VMware PowerCLI from the “PSGallery”.  Let’s continue!

Since VMware PowerCLI has moved from being its own native installer to the PSGallery, the PSGallery needs to be “Trusted” before anything from it can be installed.  To trust the PSGallery, entering the following command in the PowerShell session.

<aside class="info-block"><p>This is optional and if it is skipped, you will be prompted to trust the gallery when entering the PowerCLI module install command</p></aside>
```powershell
Set-PSRepository -Name "PSGallery" -InstallationPolicy "Trusted"
```
![](/uploads/2018/03/2018-03-02_11-18-54.png)

Next, run the following command to install the VMware.PowerCLI module.  This will find and install the latest version of the module available in the PSGallery

```powershell
Find-Module "VMware.PowerCLI" | Install-Module -Scope "CurrentUser" -AllowClobber
```

<aside class="info-block"><p>Alternatively, you could set the “-Scope” parameter to “AllUsers” and if you wanted to install a different version you could use the “-RequiredVersion” parameter and specify the version number.</p></aside>
<figure class="image-gallery">
<img src="/uploads/2018/03/2018-03-02_11-22-53.png" alt="" loading="lazy">
<img src="/uploads/2018/03/2018-03-02_11-24-02.png" alt="" loading="lazy">
</figure>

Once this finishes, we can check to make sure the module is installed by running the following command.

```powershell
Get-Module "VMware.PowerCLI" -ListAvailable | FT -Autosize
```

![](/uploads/2018/03/2018-03-02_11-26-18.png)

And if you’d like to see all of the VMware installed modules, run the following.

```powershell
Get-Module "VMware.*" -ListAvailable | FT -Autosize
```

![](/uploads/2018/03/2018-03-02_11-27-51.png)

As new versions of VMware.PowerCLI are released, you can run the following command to update it.

```powershell
Update-Module "VMware.PowerCLI"
```

With VMware.PowerCLI now installed, you can connect to your vCenter Server or ESXi host and begin using its cmdlets to obtain information or automate tasks!

I went ahead and ran the following to ensure the module was imported.

```powershell
Import-Module "VMware.PowerCLI"
```

![](/uploads/2018/03/2018-03-02_11-29-56.png)

I noticed one caveat, the SRM module does not seem to be supported in PowerShell Core, so I hope that gets resolved soon.

![](/uploads/2018/03/2018-03-02_11-31-44.png)

Let’s test connecting to vCenter server…

```powershell
Connect-VIServer -Server "<Server_Name>"
```

I also noticed an error when running the above command stating that the “InvalidCertificateAction” setting was “Unset” and not supported.

![](/uploads/2018/03/2018-03-02_11-33-04.png)

To bypass this, enter the following command and then enter “Y” when prompted.  This will set the parameter for the current user.

```powershell
Set-PowerCLIConfiguration -InvalidCertificateAction "Ignore"
```

![](/uploads/2018/03/2018-03-02_11-35-54.png)
<aside class="info-block"><p>Alternatively, you can also use the “-Scope” parameter and enter “Session”, “User”, or “AllUsers” to apply the setting to those options respectively.</p></aside>

Now, if we try to connect to vCenter again, we should be successful.

![](/uploads/2018/03/2018-03-02_11-38-34.png)

Well, that about does it!  I hope that you have found this post useful and I thank you for stopping by and reading my content.  I’d like to give a shoutout to [Mike White](https://twitter.com/mwVme) for his post on the same topic.  Until next time!

-virtualex-

## Pingbacks

- [Installing PowerShell/PowerCLI on a Mac](https://notesfrommwhite.net/2018/02/28/installing-powershell-powercli-on-a-mac/)
