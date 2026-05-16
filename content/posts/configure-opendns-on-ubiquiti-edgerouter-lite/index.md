{
  "title": "Configure OpenDNS on Ubiquiti EdgeRouter Lite",
  "date": "2016-03-27T15:46:36",
  "lastmod": "2016-03-30T03:38:16",
  "slug": "configure-opendns-on-ubiquiti-edgerouter-lite",
  "url": "/posts/configure-opendns-on-ubiquiti-edgerouter-lite/",
  "draft": false,
  "description": "I recently picked up a new router/firewall for my home, and chose the Ubiquiti EdgeRouter Lite (ERLite-3).  This device comes with a lot of bells and whistles and if you would like more information on it, please see here.I am a huge fan of speed and security, and for this purpose I always choose to…",
  "wordpress_id": 280,
  "wordpress_url": "https://ithinkvirtual.com/2016/03/27/configure-opendns-on-ubiquiti-edgerouter-lite/",
  "featured_image": "/uploads/2016/03/opendns.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "How-To's"
  ],
  "years": [
    "2016"
  ],
  "aliases": [
    "/2016/03/27/configure-opendns-on-ubiquiti-edgerouter-lite/"
  ],
  "comments": [
    {
      "author": "VirtuAlex",
      "date": "2017-08-20T11:15:00",
      "content": "<p>You welcome!  Thanks for stopping by!</p>\n"
    },
    {
      "author": "Stanley J Ziemba",
      "date": "2017-07-09T11:31:00",
      "content": "<p>Awesome thank!</p>\n"
    }
  ]
}

I recently picked up a new router/firewall for my home, and chose the Ubiquiti EdgeRouter Lite ([ERLite-3](https://www.ubnt.com/edgemax/edgerouter-lite/)).  This device comes with a lot of bells and whistles and if you would like more information on it, please see [here](https://dl.ubnt.com/datasheets/edgemax/EdgeRouter_Lite_DS.pdf).

I am a huge fan of speed and security, and for this purpose I always choose to configure my home network to use [OpenDNS](https://www.opendns.com/home-internet-security/) name servers rather than my ISP’s (Internet Service Provider) name servers.  OpenDNS has some great setup guides available for users to configure their devices and you can view the setup guides [here](https://www.opendns.com/setupguide/) and choose the solution that best suits your needs.  Now, I prefer to configure OpenDNS right on the router so that it applies to any and all devices on my network that use the internet.  Unfortunately though, I did not find a setup guide for Ubiquiti devices…but since I was already familiar with the process, I tinkered a bit around the EdgeOS and managed to figure it out.

In this post, I am going to cover how to set up your EdgeRouter to use OpenDNS name servers.  By default, the router is configured to forward DNS queries to the name server IP addresses obtained from your ISP via DHCP.  So let’s go ahead and change that!

First, let’s head over to the following [OpenDNS](https://www.opendns.com/setupguide) page to test our settings and ensure we are not already configured to use OpenDNS’s DNS name servers somehow (this is just for good measure).  On the right-hand site there is a link that reads:

> “click here to test your settings”

![2016-03-27_10-56-18](/uploads/2016/03/2016-03-27_10-56-18.png)

Go ahead and click it, and it should return the following message:

![2016-03-27_10-56-39](/uploads/2016/03/2016-03-27_10-56-39-157x300.png)

Next, login to your EdgeOS dashboard WebGUI (by default it’s configured as **192.168.1.1**) and login using the default user credentials (**ubnt**/**ubnt**).

![2016-03-27_11-18-00](/uploads/2016/03/2016-03-27_11-18-00-300x293.png)

On the bottom left corner, click the System tab to open it up.

![2016-03-27_11-19-21](/uploads/2016/03/2016-03-27_11-19-21-300x293.png)

In the **Name Server** area, add the following OpenDNS name server IP addresses then scroll to the bottom and click **Save** before closing this window:

> **208.67.222.222**
>
> **208.67.220.220**

![2016-03-27_11-20-23](/uploads/2016/03/2016-03-27_11-20-23-300x293.png)![2016-03-27_11-20-40](/uploads/2016/03/2016-03-27_11-20-40-300x293.png)

Great, Step 1 is done!  Now onto Step 2…this can be done via the **CLI** or the **Config Tree**.  (I chose the latter…)

Click on the **Config Tree** button and navigate to the following from the left-side **Configuration** pane:

> **service / dns / forwarding / system**

Click the **triangle-like** icon direct to the left of the word **system**, then click the “**+**” icon to the right of the word **system**. If done correctly you should see the following header on the top of the page and two buttons, Discard & Preview, on the bottom of the page.

![2016-03-27_11-21-41](/uploads/2016/03/2016-03-27_11-21-41-300x293.png)

Next, click the **Preview** button at the bottom of the page.  This will show you the command that would be used in the CLI to apply the name servers.  The great thing about this is that it also give you the option to “**Apply**” it now via the GUI!  I chose to hit Apply.

![2016-03-27_10-58-20](/uploads/2016/03/2016-03-27_10-58-20-300x200.png)

Once, completed, there should be some green text at the bottom reading:

> “The configuration has been applied successfully”

![2016-03-27_11-13-02](/uploads/2016/03/2016-03-27_11-13-02-300x43.png)

Now, the final step is to go back to the [OpenDNS](https://www.opendns.com/setupguide) page and test the settings again.  If everything is applied correctly, you will be presented with the following:

![2016-03-27_11-03-45](/uploads/2016/03/2016-03-27_11-03-45-147x300.png)

Now your router is fully configured to use OpenDNS!

I hope that you have found this to be informative so please be sure to comment below and share this post.
