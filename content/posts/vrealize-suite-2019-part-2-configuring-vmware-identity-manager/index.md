{
  "title": "vRealize Suite 2019 – Part 2: Configuring VMware Identity Manager",
  "date": "2020-01-06T04:42:40",
  "lastmod": "2020-01-06T16:09:03",
  "slug": "vrealize-suite-2019-part-2-configuring-vmware-identity-manager",
  "url": "/posts/vrealize-suite-2019-part-2-configuring-vmware-identity-manager/",
  "draft": false,
  "description": "",
  "wordpress_id": 1671,
  "wordpress_url": "https://ithinkvirtual.com/2020/01/05/vrealize-suite-2019-part-2-configuring-vmware-identity-manager/",
  "featured_image": "/uploads/2020/01/2020-01-05_23-23-26.png",
  "categories": [
    "Home Lab",
    "How-To's"
  ],
  "tags": [
    "How-To's",
    "Nested Virtualization",
    "VMware",
    "vRealize Suite",
    "vSphere"
  ],
  "years": [
    "2020"
  ],
  "aliases": [
    "/2020/01/05/vrealize-suite-2019-part-2-configuring-vmware-identity-manager/"
  ],
  "comments": []
}

## Intro

In my [previous post](/2020/01/04/vrealize-suite-2019-part-1-installing-vrealize-lifecycle-manager/), I covered how to install vRealize Suite Lifecycle Manager 8.0 and in the process it also deployed an instance of VMware Identity Manager aka Workspace One Access, which is a requirement for installing vRealize Automation 8.0.  I opted to skip the deployment of the latter as to keep focus on the deployment of LCM only.

In this post, I'll cover how to configure VMware Identity Manager to support Active Directory Authentication for the vRealize Suite solutions

### Procedure

- Log in to **VMware Identity Manager** and then access the **Administration Console**.

![](/uploads/2020/01/2020-01-05_20-46-46-1024x585.png)

- Click **Identity & Access Management**, then click **Setup > User Attributes**.
  - I elected to only require the AD account to have a *Username* and a *First Name*, so I unchecked all other options.  This is optional and shouldn't be done in Production environments.  The more security the better!

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_20-47-26-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_20-48-22-1024x585.png" alt="" loading="lazy">
</figure>

- Click **Manage**, then click **Add Directory > Add Active Directory over LDAP/IWA**

![](/uploads/2020/01/2020-01-05_20-52-21-1024x585.png)

- Provide a **Directory Name, Base DN, Bind DN,** and **Bind User Password** then click **Test Connection**.  If it is Successful, click **Save & Next**.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_20-52-48-1024x581.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_20-53-22-1024x585.png" alt="" loading="lazy">
</figure>

- Select any domains that you'd like to add then click **Next > Next**.
  - This was already selected and is unable to be unchecked.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_20-54-18-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_20-55-03-1024x585.png" alt="" loading="lazy">
</figure>

- Add the **group DNs** and either check **Select All** box or click the **Select** button to add any Groups that are to be synchronized with VMware Identity Manager, then click **Next**.

![](/uploads/2020/01/2020-01-05_20-56-31-1024x585.png)

- Add any **user DNs** that are to be synced as well and click **Next**.

![](/uploads/2020/01/2020-01-05_20-57-09-1024x585.png)

- Review and make any changes if necessary then click **Sync Directory**.
  - The sync will begin, after a bit click the ***Refresh*** button to see the sync has finished

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_20-58-06-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_20-58-32-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_20-58-55-1024x585.png" alt="" loading="lazy">
</figure>

- To confirm that the users and groups synced, click **Users & Groups > Users/Groups**.

![](/uploads/2020/01/2020-01-05_21-03-49-1024x585.png)

Now that the users I want are synced, I'd like to also give these users ***Super Admin*** rights to VMware Identity Manager.

- Click **Roles**, then select the **checkbox** next to **Super Admin** and click **Assign**.  Search for the users to add and when finished, click **Save**.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_21-00-23-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_21-01-12-1024x585.png" alt="" loading="lazy">
</figure>

Now, I can successfully log in to VMware Identity Manager using the newly synced Active Directory accounts.  But, before I can actually use these r accounts for *other* products, the users need to be given access to login to the respective solution.  In my case, I've only deployed vRealize Suite Lifecycle Manager so far.

- Log in to **vRealize Lifecycle Manager** with the **local admin account** then select **User Management > User Management > Add User / Group**.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_21-05-03-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_21-05-36-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_21-06-06-1024x585.png" alt="" loading="lazy">
</figure>

- Search for the users to add and click **Next**.

![](/uploads/2020/01/2020-01-05_22-27-53-1024x585.png)

- Select the **LCM Cloud Admin** role and click **Next**.

![](/uploads/2020/01/2020-01-05_21-07-18-1024x585.png)

- Review the Summary and click **Submit**.

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_21-07-44-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_21-08-07-1024x585.png" alt="" loading="lazy">
</figure>

One final step to go! Now that I've granted rights in vRealize Suite Lifecycle Manager, I'm able to entitle users in VMware Identity Manager to allow access to vRealize Suite Lifecycle Manager using VMware Identity Manger authentication.  How sweet it that, right?!

- Log in to **VMware Identity Manager** and access the **Administration Console** then **Catalog**.  Select the **checkbox** next to the **Application** that is to be Entitled and click **Assign**.

![](/uploads/2020/01/2020-01-05_21-10-29-1024x585.png)

- Search for the Users and/or Groups to be Entitled then ( *Optional: also Change the Deployment Type to Automatic* ) click **Save**.

![](/uploads/2020/01/2020-01-05_21-11-34-1024x581.png)

- Navigate to **vRealize Suite Lifecycle Manager** and select **Identity Manager User** from the **drop-down** selection, then click **Login with Identity Manager**.  Success!!

<figure class="image-gallery">
<img src="/uploads/2020/01/2020-01-05_21-11-59-1024x585.png" alt="" loading="lazy">
<img src="/uploads/2020/01/2020-01-05_21-14-57-1024x585.png" alt="" loading="lazy">
</figure>

Additionally, a user can also automatically authenticate into an Application from their Workspace One Access (VMware Identity Manager) User Portal.

- Click the **Open** link on the **Application** watch it launch the URL and authenticate the user *Automagically*!

![](/uploads/2020/01/2020-01-05_23-13-35.gif)

Well, that about wraps up this post.  In the next post, I'll go over the deployment of vRealize Automation 8.0.

I hope that you've found this useful and I thank each and every one of you for reading.
