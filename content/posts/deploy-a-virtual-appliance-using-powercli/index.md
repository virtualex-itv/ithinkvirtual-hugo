{
  "title": "Deploy A Virtual Appliance Using PowerCLI",
  "date": "2018-02-04T22:53:08",
  "lastmod": "2018-02-10T13:55:54",
  "slug": "deploy-a-virtual-appliance-using-powercli",
  "url": "/posts/deploy-a-virtual-appliance-using-powercli/",
  "draft": false,
  "description": "Hello all and thank you for visiting my blog!  In today’s post, I am going to cover how to deploy a VMware virtual appliance (.ova) using PowerCLI.  “Why?” you asked?  Well, because scripting and automation via PowerCLI is fun and awesome!  Sure, it’s simple enough to deploy an appliance natively within the vSphere Web Client…",
  "wordpress_id": 1090,
  "wordpress_url": "https://ithinkvirtual.com/2018/02/04/deploy-a-virtual-appliance-using-powercli/",
  "featured_image": "/uploads/2018/02/OVA_PCLI_BG.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "PowerCLI",
    "VMware",
    "vSphere"
  ],
  "years": [
    "2018"
  ],
  "aliases": [
    "/2018/02/04/deploy-a-virtual-appliance-using-powercli/"
  ],
  "comments": []
}

Hello all and thank you for visiting my blog!  In today’s post, I am going to cover how to deploy a VMware virtual appliance (.ova) using PowerCLI.  “Why?” you asked?  Well, because scripting and automation via PowerCLI is fun and awesome!  Sure, it’s simple enough to deploy an appliance natively within the vSphere Web Client by selecting the .ova that you’d like to import, press a few mouse clicks, enter some info, and off you go!  But who wants to do stuff the easy way?  It takes the fun away!

In my opinion, scripting this out is just as easy since you can pre-populate your information into variables, and then run a simple “one-liner” command to kick off the deployment.  Pretty neat right?

Now, I do understand that initially doing a deployment this way is a bit time-consuming.  But once you have the method and process down, you can create a simple PowerShell script with all of your information embedded, then simply tweak/adjust it as needed per appliance.  The only time-consuming part is identifying the proper variables for each appliance.  Please keep in mind that while most appliances have the same initial setup variables, some may have more and some may have less so it is always best to follow the initial steps I’ll cover below for each appliance to ensure you have all the correct information for your deployment and/or script.

Well, let’s get to it, shall we!

In this example, I will be using the latest version of PowerCLI which, at the time of this writing, is 6.5.4.7155375, to deploy the VMware Support Assistant appliance for vSphere 6.5.

![](/uploads/2018/02/2018-02-04_14-52-55-1024x397.png)

To kick things off, we will be using two important variables, ***$ovfPath***, and ***$ovfConfig***.  The latter will use the ***$ovfPath*** variable to discover the correct variable properties to build out our ***$ovfConfig***.  I’ll assume that you’re already connected to your vCenter server in the PowerCLI session but, if not, please go ahead and do so using the “***Connect-VIServer***” cmdlet.

![](/uploads/2018/02/2018-02-04_14-05-15-1024x396.png)

Let’s define our ***$ovfPath*** first:

```powershell
$ovfPath = "<path_to_ova_file>"
```

Next, let’s define ***$ovfConfig***

```powershell
$ovfConfig = Get-OvfConfiguration -Ovf $ovfPath
```

Great!  Now if we simply type ***$ovfConfig***, it will check our ***$ovfPath*** for the file and list the setup properties.

![](/uploads/2018/02/2018-02-04_14-10-51-1024x396.png)

We can see that it has identified “***Common***“, “***IpAssignment***“, “***NetworkMapping***“, and “***vami***” as the starting base properties.  Next, we will have to drill down into each of these properties to determine the full property “***Value***” to define our variable with.

So starting with “***Common***“, let’s drill down more by typing:

```powershell
$ovfConfig.Common
```

This now identifies the next “***Common***” property which is “***varoot_password***“.  Let’s drill into that to see what it finds.

```powershell
$ovfConfig.Common.varoot_password
```

This gives us more information about the property and the key one here is “***Value***“.

![](/uploads/2018/02/2018-02-04_14-12-37-1024x396.png)

This means that we have reached the last property entry needed to define our first config variable with.  Great! With this information, our first defined configuration variable will look like this:

```powershell
$ovfConfig.Common.varoot_password.Value = "<some_password>"
```

Let’s now move to the next property, “***IpAssignment***“.  Following the same logic as before and drilling into this property identifies “***IpProtocol***” which requires a “*string*” value of “***IPv4*** or ***IPv6***“.

![](/uploads/2018/02/2018-02-04_14-14-14-1024x396.png)

This means our next defined variable will look like this.

```powershell
$ovfConfig.IpAssignment.IpProtocol.Value = "IPv4"
```

Now for the next property, “***NetworkMapping***“.  Drilling down into this property identifies “***Network_1***” which again will be a “*string*” value for our variable.  This string is the VM PortGroup that you want to attach to the appliance, whether it be on a virtual Standard Switch (vSS) or Distributed Switch (vDS).

![](/uploads/2018/02/2018-02-04_14-14-55-1024x396.png)

This defined variable will look like this.

```powershell
$ovfConfig.NetworkMapping.Network_1.Value = "<some_vm_portgroup>"
```

Getting the gist of this yet?  Let’s move onto the final property, “***vami***“.  Again, following the same logic we’ve been doing and drilling into the “*vami*” property, we can see that it has identified the “a*ppliance*” as “***VMware_vCenter_Support_Assistant_Appliance***“.  Drilling down further, there are multiple properties discovered in this one and they are “***gateway***“, “***domain***“, “***searchpath***“, “***DNS***“, “***ip0***“, and “***netmask0***“.

![](/uploads/2018/02/2018-02-04_14-17-10-1024x396.png)

Whoa! Quite a few huh?  Yet again, drilling into each of these lets us know that “*string*” values are required for each property.

![](/uploads/2018/02/2018-02-04_14-19-00-1024x412.png)

These config variables will be defined like this.

```powershell
$ovfConfig.vami.VMware_vCenter_Support_Assistant_Appliance.gateway.Value = "<gateway_ip>"
$ovfConfig.vami.VMware_vCenter_Support_Assistant_Appliance.domain.Value = "<domain_name>"
$ovfConfig.vami.VMware_vCenter_Support_Assistant_Appliance.searchpath.Value = "<dns_searchpath>"
$ovfConfig.vami.VMware_vCenter_Support_Assistant_Appliance.DNS.Value = "<dns_ip(s)>"
$ovfConfig.vami.VMware_vCenter_Support_Assistant_Appliance.ip0.Value = "<appliance_ip>"
$ovfConfig.vami.VMware_vCenter_Support_Assistant_Appliance.netmask0.Value = "<netmask_ip>"
```

From what we’ve obtained so far, all of our defined variables look like this.

![](/uploads/2018/02/2018-02-04_14-26-41-1024x412.png)

Ready to deploy the appliance?  Not quite yet!  There are some additional variables we can create/define to make the syntax of our command shorter, neater, and nicer.  First, let’s see what the cmdlet requires.  The cmdlet used to deploy an appliance is “[Import-vApp](https://code.vmware.com/doc/preview?id=5060#https://vdc-repo.vmware.com/vmwb-repository/dcr-public/cd82421a-ee01-40a9-97c3-424ae49db692/972fed92-0e32-4993-9d35-0557c829bebd/doc/Import-VApp.html)“.  Clinking that link and reviewing the table show us what is required or not.

![](/uploads/2018/02/2018-02-04_14-27-31.png)

From this table, I am going to define some more variables for the following parameters.

- Source
- Name
- VMHost
- Datastore
- DiskStorageFormat
- Location
- OvfConfiguration

![](/uploads/2018/02/2018-02-04_14-35-12-1024x412.png)

Now, with all of the variables defined, we are ready to enter the “Import-VApp” command with the required parameters.

```powershell
Import-VApp -Source $ovfpath -OvfConfiguration $ovfConfig -Name $VMName -VMHost $VMHost -Location $Cluster -Datastore $Datastore -DiskStorageFormat $DiskFormat -Confirm:$false
```

A progress bar will load in your session showing that the deployment has kicked off, and a short while later it will end, meaning that the appliance has been successfully deployed.

![](/uploads/2018/02/2018-02-04_14-39-53-1024x302.png) ![](/uploads/2018/02/2018-02-04_14-42-20-1024x302.png)

A quick look at the vSphere Client, and we can see that the appliance is indeed there and configured as per the settings we defined earlier in our configuration.

![](/uploads/2018/02/2018-02-04_14-42-44-1024x750.png)

At this point, you can safely power-on the appliance and proceed with normal setup processes.  Also, as I noted earlier, you can take all of these variables and create a PowerShell script to deploy your appliances with and just add/remove/change variables as needed per appliance!  Automation at its finest!

Well, I’d like to thank you for stopping by and supporting my page.  I do hope that you have found this information useful, and hope you’ll return again.  Thanks much and I’ll catch you on the next one!

-virtualex-
