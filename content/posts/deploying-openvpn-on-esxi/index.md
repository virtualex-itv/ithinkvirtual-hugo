{
  "title": "Deploying OpenVPN on ESXi",
  "date": "2017-02-13T02:35:24",
  "lastmod": "2018-02-10T14:19:59",
  "slug": "deploying-openvpn-on-esxi",
  "url": "/posts/deploying-openvpn-on-esxi/",
  "draft": false,
  "description": "Have you ever wondered to yourself, “What is OpenVPN and what is it used for?”  I know I have!  I currently leverage OpenDNS’s servers in my network, and when I saw that they offer an Open-Source VPN solution, I figured I had to give it a whirl!  While I have used VPN’s before for connecting…",
  "wordpress_id": 835,
  "wordpress_url": "https://ithinkvirtual.com/2017/02/12/deploying-openvpn-on-esxi/",
  "featured_image": "/uploads/2017/02/openvpn-as-banner.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "OpenVPN"
  ],
  "years": [
    "2017"
  ],
  "aliases": [
    "/2017/02/12/deploying-openvpn-on-esxi/"
  ],
  "comments": [
    {
      "author": "VirtuAlex",
      "date": "2017-04-26T21:41:00",
      "content": "<p>@disqus_xMOzGbcd6U:disqus &#8211; Thx for commenting, glad to hear it&#8217;s working for you without issues!</p>\n"
    },
    {
      "author": "Michael Garrison",
      "date": "2017-04-15T16:47:00",
      "content": "<p>Great tutorial!  I got it up and running without any issues!</p>\n"
    }
  ]
}

Have you ever wondered to yourself, “What is OpenVPN and what is it used for?”  I know I have!  I currently leverage OpenDNS’s servers in my network, and when I saw that they offer an Open-Source VPN solution, I figured I had to give it a whirl!  While I have used VPN’s before for connecting to a company network from a remote location, or using a VPN service while travelling and connecting to numerous public hot-spots for the added security, I never thought to implement my own for personal use where I can connect to my home network and browse my devices or surf the net securely as if I was sitting at home in front of my computer from anywhere in the world.  Well…welcome OpenVPN!

As stated on their website… *“OpenVPN Access Server is a full-featured secure network tunneling VPN software solution that integrates OpenVPN server capabilities, enterprise management capabilities, simplified OpenVPN Connect UI, and OpenVPN Client software packages that accommodate Windows, MAC, Linux, Android, and iOS environments. OpenVPN Access Server supports a wide range of configurations, including secure and granular remote access to internal network and/ or private cloud network resources and applications with fine-grained access control.”*

OpenVPN offers a variety of different software installation packages and virtual appliance to suit your needs.  I opted for the VMware virtual appliance to deploy in my home network.  In this tutorial, I will show you just how to deploy an OpenVPN Access Server on ESXi 6.5.  For the purposes of this demonstration, I will be deploying said appliance on a virtual ESXi host running in my lab so without any further hesitation, let’s get started!

- Head on over to the OpenVPN website and download the [virtual appliance](https://swupdate.openvpn.org/appliances/AS.ova) for VMware.
  - At the time of this writing, the current version is 2.1.3 released back on 9/16/2016.  Installation [instructions](https://openvpn.net/index.php/access-server/download-openvpn-as-vm/469-deploying-openvpn-access-server-from-an-ovf-template-in-vmware-esxi-environment.html) are also provided on this site.  Once you have obtained the virtual appliance, connect to your ESXi host via the ESXi Host UI or the vCenter Web Client.
- As I am just working on a single host without a vCenter, I will leverage the ESXi Host UI.  Follow along to deploy the appliance…

![](/uploads/2017/02/2017-02-12_15-42-50-150x150.png) ![](/uploads/2017/02/2017-02-12_15-43-06-150x150.png) ![](/uploads/2017/02/2017-02-12_15-43-56-150x150.png) ![](/uploads/2017/02/2017-02-12_15-44-27-150x150.png) ![](/uploads/2017/02/2017-02-12_15-44-50-150x150.png) ![](/uploads/2017/02/2017-02-12_15-45-22-150x150.png) ![](/uploads/2017/02/2017-02-12_15-45-45-150x150.png) ![](/uploads/2017/02/2017-02-12_15-49-49-150x150.png)

- Now that the appliance has been deployed, go ahead and power it on then open a Remote Console session to the appliance.  I will be leveraging the VMware VMRC version 9.0.  Once the appliance has booted, you will be presented with the following screen.

![](/uploads/2017/02/2017-02-12_15-50-11-300x151.png) ![](/uploads/2017/02/2017-02-12_15-51-58-300x150.png) ![](/uploads/2017/02/2017-02-12_15-59-03-300x169.png)

- Now, login to the appliance using the following default credentials.
  - Username – root
  - Password – openvpnas

- We are now entering the configuration wizard.  Type “yes” to accept the license agreement and begin the wizard

![](/uploads/2017/02/2017-02-12_16-00-31-300x169.png)

- From this point, a series of questions will be presented.  For the most part, we will be accepting the defaults so follow along to configure the appliance.
  - Will this be the primary Access Server node?
    - **Explanation:** If this is your initial Access Server node, press **Enter** to accept the default setting. Otherwise, if you are setting up your failover node, change this to say **no**.
  - Please specify the network interface and IP address to be used by the Admin Web UI:
    - **Explanation:** This will be the interface where OpenVPN Access Server will listen to Admin Web UI requests. Make sure you have access to the interface listed otherwise you will be unable to login to your server. If you are uncertain on what interface to use, select option **1** for all interfaces. Do note that if your network did not assign your appliance a DHCP lease or if you are planning to use a static IP for your server, you will need to specify all interfaces here and follow the instructions for assigning a Static IP in the later section of this article. This option may be changed any time after the completion of the wizard in the Web Admin UI.
  - Please specify the port number for the Admin Web UI.
    - **Explanation:** This is the port you will use to access the web-based administration area. It is usually safe to leave this at the default port unless customization is desired.
  - Please specify the TCP port number for the OpenVPN Daemon
    - **Explanation:** This is the port clients will use to connect to your VPN server. This port will have to be forwarded to the Internet if your server is behind a NAT-based router. By default, the web-based administration area also runs on this port for your convenience, although this setting can be disabled in the Admin Web UI interface.
  - Should client traffic be routed by default through the VPN?
    - **Explanation:** If you only have a small network you would like your remote users to connect over the VPN, select **no**. Otherwise, if you would like everything to go through the VPN while the user is connected (especially useful if you want to secure data communications over an insecure link), select **yes** for this option.
  - Should client DNS traffic be routed by default through the VPN?
    - **Explanation:** If you would like your VPN clients to able to resolve local domain names using an on-site DNS server, select **yes**for this option. Otherwise, select **no**. Do note that if you selected **yes** for the previous option, all traffic will be routed over the VPN regardless what you set for this setting here.
  - Use local authentication via internal DB?
    - **Explanation:** If you would like OpenVPN Access Server to keep an internal authentication database for authenticating your users, select **yes** for this option. When this option is turned on, you will be able to define and/or change username and passwords within the Admin Web UI. If you select **no** for this option, Linux PAM authentication will be used and you will need to add/change/delete users within the Linux operating system itself. If you would like to use LDAP or RADIUS as your authentication method, you will need to change this after you login to the Web Admin UI.
  - Should private subnets be accessible to clients by default?
    - **Explanation:** This option defines the default security setting of your OpenVPN Access Server. When **Should client traffic be routed by default through the VPN?** is set to **no**, it defines the list of subnets that your VPN clients is able to access. You are able to add more entries to this list once you log in to the Admin Web UI area. This option will have no effect if **Should client traffic be routed by default through the VPN?** is set to **yes**.
  - Do you wish to login to the Admin UI as “openvpn”?
    - **Explanation:** This defines the initial username in which you would use to login to the Access Server Admin UI area. This username will also serve as your **“lock out”** administrator username shall you ever lock yourself out of your own server. If you would like to specify your own username, select **no**. Otherwise, accept **yes** for the default.
  - Specify the username for an existing user or for the new user account:
    - **Explanation:** Enter the initial username you would like to use instead of the default ‘**openvpn**‘.
  - Type the password for the ‘user’ account: > Confirm the password for the ‘user’ account:
    - **Explanation:** Specify the password you would like to use for the account.
  - Please specify your OpenVPN-AS license key (or leave blank to specify later):
    - **Explanation:** If you have purchased a license key for your OpenVPN Access Server software, enter it here. Otherwise, leave it blank. OpenVPN Access Server includes two free licenses for testing purposes. After you complete the setup wizard, you can access the Admin Web UI area to configure other aspects of your VPN. The URL for the Admin Web UI area is displayed upon the completion of the setup wizard. As mentioned previously, you will be able to access the Admin Web UI on both the VPN port and the Admin port unless you disable this behavior in the Admin Web UI. Note: If you selected **yes** to the **Do you wish to login to the Admin UI as “openvpn”?** option in the setup wizard, you will need to define the password for this account by running: **passwd openvpn** and press **Enter**.
- The only options I changed from the defaults are as follows…
  - Port used by the OpenVPN Daemon
    - I used “9443”
  - Use local authentication via internal DB
    - I said “yes”
  - Do you wish to login to the Admin UI as “openvpn”?
    - I said “no” and then specified a username and password.

![](/uploads/2017/02/2017-02-12_17-01-46-300x169.png)

- There are also a few optional settings you can configure which are detailed on the instructions web page but I will not cover them here.
- If an at point you mess up during the initial configuration, first complete it and then from the command prompt type

```bash
ovpn-init
```

- This will prompt you to type “**DELETE**” to wipe the current config so you can start over.

![](/uploads/2017/02/2017-02-12_17-00-08-300x169.png)

- Now that the appliance is deployed and configured, a port-forwarding rule is required to pass traffic to the appliance so it can be connected to from outside your network.  Head over to your router and configure the TCP port you defined during the initial configuration for the OpenVPN Daemon to forward to the IP of the appliance.  An additional UDP port-forward is needed for port 1194 to the appliance’s IP address.

```text
TCP Port 9443 #this is the port that I defined in the configuration

UDP Port 1194
```

![](/uploads/2017/02/2017-02-12_20-20-18-300x241.png)

- Once the port forwarding rules are in place, you can connect to the appliance via a web browser on your network as well as from an external network.  Let’s start by testing connectivity from within our network.  Open a web browser and navigate to the appliance admin login page

```text
https://<appliance-IP>:<port>/admin
```

- If successful, you should see the login page and can log in with the credentials set during configuration.  From here you can configure the appliance to your liking then download the OpenVPN Client for use on Windows, Mac, etc.  I will not cover the settings in this tutorial but feel free to poke around here and configure your appliance before logging out.

![](/uploads/2017/02/2017-02-12_17-02-45-300x161.png) ![](/uploads/2017/02/2017-02-12_17-03-09-300x151.png) ![](/uploads/2017/02/2017-02-12_17-03-31-300x151.png)

- You can also connect to the appliance without the “/admin” in the URL so that you can download your client.  You can use either option from the drop-down menu.

```text
https://<appliance-IP>:<port>
```

![](/uploads/2017/02/2017-02-12_20-26-49-300x161.png)

- If you choose the “Connect” option, you will see this screen which will prompt you to download the OpenVPN Client for your computer.

![](/uploads/2017/02/2017-02-12_20-27-35-300x151.png)

- If you choose “Login” option, you will see this screen which provides various download links for other devices, as well as the option to download your custom profile to be used in the client so that you connect to your personal VPN environment.

![](/uploads/2017/02/2017-02-12_20-33-21-300x151.png)

- To connect to your VPN network from an external network, you will need to obtain your external IP address by using “What’s My IP” or “IP Chicken” websites.  Then enter that IP address in your web browser with the TCP port you defined in your port-forward rule.

```text
https://<external-WAN-IP>:<port>
```

- I tested this from my phone and was successful.  Then you can download the profile and use a VPN client on your phone or computer to access your network via your OpenVPN appliance.

![](/uploads/2017/02/2017-02-12_21-00-37-144x300.png)

Well, I hope this helps shed some more light on the awesomeness of OpenVPN and that you’ve found this useful.  Thanks for reading and please comment and subscribe!

-virtualex-
