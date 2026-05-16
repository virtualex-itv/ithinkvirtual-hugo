{
  "title": "vRealize Suite 2019 - Part 3: Installing vRealize Automation",
  "date": "2020-01-17T21:56:02",
  "lastmod": "2020-01-17T22:03:40",
  "slug": "vrealize-suite-2019-part-3-installing-vrealize-automation",
  "url": "/posts/vrealize-suite-2019-part-3-installing-vrealize-automation/",
  "draft": false,
  "description": "",
  "wordpress_id": 1714,
  "wordpress_url": "https://ithinkvirtual.com/2020/01/17/vrealize-suite-2019-part-3-installing-vrealize-automation/",
  "featured_image": "/uploads/2020/01/2020-01-10_21-03-14.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "Nested Virtualization",
    "vExpert",
    "VMware",
    "vRealize Suite",
    "vSphere"
  ],
  "years": [
    "2020"
  ],
  "aliases": [
    "/2020/01/17/vrealize-suite-2019-part-3-installing-vrealize-automation/"
  ],
  "comments": []
}

## Intro

In my [previous post](/2020/01/05/vrealize-suite-2019-part-2-configuring-vmware-identity-manager/), I covered the configuration of VMware Identity Manager in preparation for what I will cover in this post, the installation of vRealize Automation 8.0!  This new release is a complete redesign of the product and now uses a similar codebase to vRealize Automation Cloud (formerly known as Cloud Automation Services), bringing those capabilities to the on-premises form factor and making it easier to transform IT delivery.  I look forward to tinkering with this more after the deployment!  Let's jump right in!

### Procedure

- Begin by logging into vRealize Lifecycle Manager and from the home page, click **Create Environment**.
- Fill out the details and click **Next**.
  - <aside class="info-block"><p>There is a known bug in vRA 8.0 which will fail the deployment if CEIP is enabled, so I unchecked the option to disable it during deployment. It can be re-enabled via CLI post-deployment. This bug has also been resolved in v8.0.1.</p></aside>

![](/uploads/2020/01/2020-01-11_10-07-14-1024x579.png)

- Select the **vRealize Automation** product and the preferred **Deployment Type**, then click **Next**.
  - I am doing a Standard single-node deployment.

![](/uploads/2020/01/2020-01-11_10-22-37-1024x579.png)

- Accept the EULA and click **Next**.

![](/uploads/2020/01/2020-01-11_10-22-52-1024x579.png)

- Add a vRA License by clicking **Add** or **Select**.
  - Add will guide through entering and saving a license into LCM's Locker.
  - Select will let you choose from your list of saved licenses.
- After adding the license click **Validate Association** then click **Next**.

![](/uploads/2020/01/2020-01-11_10-23-06-1024x579.png)

- Select your generated Certificate and click **Next**.
  - Certificates are also stored in LCM's Locker.  If you need to create a certificate, click the + sign on the far right to walk through the process of generating and saving a new cert.
  - <aside class="info-block"><p>There is another known bug that will cause the deployment to fail. vRA supports using a wildcard domain name in place of FQDNs when configuring the Subject Alternative Names during certificate generation. The caveat is that it must be on the registered Public Domain Suffix list(ex: .com, .org, .edu, etc.). If your lab environment is not using a public domain suffix, be sure to enter in the FQDNs for each product you plan on deploying with this certificate.</p></aside>

![](/uploads/2020/01/2020-01-11_10-23-19-1024x579.png)

- Configure the appropriate information and click **Next**.

![](/uploads/2020/01/2020-01-11_10-23-31-1024x579.png)

- Enter in the required network information and click **Next**.

![](/uploads/2020/01/2020-01-11_10-23-52-1024x579.png)

- Enter in the **VM Name**, **Hostname**, and **IP Address** for the vRealize Automation appliance and click **Next**.

![](/uploads/2020/01/2020-01-11_10-24-07-1024x579.png)

- Click **Run Precheck** and if everything comes back successful, click **Next**.

![](/uploads/2020/01/2020-01-11_10-25-37-1024x579.png)

- When ready, click **Submit**.
  - This is a good time to export the configuration to save as a backup or to use again for another deployment of vRA.

![](/uploads/2020/01/2020-01-11_10-25-50-1024x579.png)

If all goes well, in about an hour's time you'll have a successful installation of the new vRealize Automation 8.0

![](/uploads/2020/01/2020-01-11_10-26-04-1024x579.png)

- <aside class="info-block"><p>There&#x27;s another known bug, that will cause the deployment to fail and will throw the same error message as the other two previously mentioned bugs. This is due to the root account password used to install the RPMs during the in the vRealize Orchestrator pod installation (since both vRA and vRO run in K8s pods!) being expired, causing a timeout and an eventual failure. To work around this you must SSH into the vRA appliance and navigate to `/opt/charts/vco/templates` directory and editing the deployment.yaml file.</p></aside>
- Look for the following lines of code around line 210.

```yaml
command:
        - "/bin/bash"
        - "-c"
        - "/init_run.sh"
```

- - - Edit the lines to look like the following:

```yaml
command:
        - "/bin/bash"
        - "-c"
        - "sed -i 's/root:.*/root:x:18135:0:99999:7:::/g' /etc/shadow && sed -i 's/vco:.*/vco:x:18135:0:99999:7:::/g'
          /etc/shadow && /init_run.sh"
```

![](/uploads/2020/01/2020-01-17_16-51-31-1024x431.png)

- - After editing the file, return to the failed request in the vRealize Lifecycle Manager GUI and click **Retry**, and the installation should complete successfully.

![](/uploads/2020/01/2020-01-10_21-02-51-1024x579.png)

- Navigate to the vRealize Automation URL and click Go To Login Page.
  - Log in with the **configadmin** account from VMware Identity Manager.
    - We can then grant access to different users so they can access and work with vRealize Automation.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-10_21-03-14-1024x579.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-15_9-32-37-1024x579.png" alt="" loading="lazy">
</figure>

- Click on Identity & Access Management.
  - You may already see the users configured previously in vIDM.
  - Configadmin has all the roles so feel free to mirror the roles to your users, which I did here, or select the appropriate roles for your production users.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-15_9-38-05-1024x579.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-15_9-40-17-1024x579.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-15_9-41-33-1024x579.png" alt="" loading="lazy">
</figure>

Now, we can log out of vRealize Automation and head over to the Admin Console of VMware Identity Manager so we can configure a new Web Application for our users.  This way, once they log into Workspace One Access, they can launch the application and authenticate automatically!

- From the **vIDM Administrator Console**, click **Catalog > New**.

![](/uploads/2020/01/2020-01-15_9-42-14-1024x579.png)

- Provide a **Name** for the application and select an **Icon** file if you have one, then click **Next**.

![](/uploads/2020/01/2020-01-15_9-44-00-1024x579.png)

- Select **Web Application Link** for the Authentication Type and enter the **Target URL**, then click **Next**.

![](/uploads/2020/01/2020-01-15_9-44-39-1024x579.png)

- Click **Save & Assign**

![](/uploads/2020/01/2020-01-15_9-44-51-1024x579.png)

- Add the desired users and set the **Deployment Type** to **Automatic**, then click **Save**.
  - When the application is launched, it will automatically attempt to authenticate the user.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-15_9-46-52-1024x579.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-15_9-45-58-1024x579.png" alt="" loading="lazy">
</figure>

- Navigate back to the User Portal and the application should now be available in the Catalog.

![](/uploads/2020/01/2020-01-15_9-48-07-1024x579.png)

Well, that about wraps up this installation and I can't wait to start getting my feet wet with this new version.  I'm familiar with the previous versions, but as mentioned earlier, this is a complete redesign of the product so time for me to learn it...can't wait!

I hope that you've found this information useful, and I thank you all for stopping by and reading!
