{
  "title": "System Center Configuration Manager: Step-by-Step - SQL Server Installation",
  "date": "2018-03-31T16:02:06",
  "lastmod": "2018-03-31T20:02:06",
  "slug": "system-center-configuration-manager-step-by-step---sql-server-installation",
  "url": "/posts/system-center-configuration-manager-step-by-step---sql-server-installation/",
  "draft": true,
  "description": "",
  "wordpress_id": 1011,
  "wordpress_url": "https://ithinkvirtual.com/?p=1011",
  "featured_image": "/uploads/2017/11/2017-11-05_19-48-47-300x228.png",
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

In the previous section of this series, I covered the basic server preparation and prerequisite installation steps needed for installing System Center Configuration Manager.

This next section will cover the installation and configuration of Microsoft SQL Server 2017 which will be installed locally on the Primary Site Server.  Let's get to it!

## Microsoft SQL Server 2017 Installation

- Mount the SQL installation media to your Site Server and then log in to your machine
- Navigate to your installation media and double-click the **Setup.exe** file
- Select **Installation** then click **New SQL Server stand-alone installation...**

![](/uploads/2017/11/2017-11-05_19-48-47-300x228.png)

- Enter your **product key** and click **Next**

![](/uploads/2017/11/2017-11-05_19-49-21-300x228.png)

- Accept the **license terms** and click **Next**

![](/uploads/2017/11/2017-11-05_19-50-40-300x228.png)

- Select the **Use Microsoft Update to check for updates (recommended)** and click **Next**

![](/uploads/2017/11/2017-11-05_19-51-10-300x228.png)

- Click **Next** after the **Install Rules** completes

![](/uploads/2017/11/2017-11-05_19-51-56-300x228.png)

- Select the checkbox for **Database Engine Services**, then change the location of the **Instance root directory** and **Share feature directory (x86)** then click **Next**
  - I change the Instance root directory to my ***E:*** drive as this was previously configured for the **SQL DB**
  - I then kept the Shared feature directory on the ***C:*** drive

![](/uploads/2017/11/2017-11-05_20-02-43-272x300.png)

- Select **Default instance** and click **Next**
  - You may choose to give this a named instance if you'd like but for the sake of simplicity, I kept the default selection

![](/uploads/2017/11/2017-11-05_20-04-32-300x246.png)

- Select the **drop-down** arrow under **Account Name** for both **SQL Server Agent** and **SQL Server Database Engine**, then click **Browse**
- Enter the name of the SQL Service account that we created in the previous section then click **OK**
- Enter the Password for each account and change the Startup Type to **Automatic**, then click the **Collation** tab and ensure it's set to **SQL_Latin1_General_CI_AS** and click **Next**

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_20-05-59-300x246.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_20-06-42-300x169.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_20-08-52-300x246.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_20-09-12-300x246.png" alt="" loading="lazy">
</figure>

- Select **Windows authentication mode** and add the **Current User**, the **Local Administrator** account of the site server (if this is not the current user), the domain **SCCM Admins group**, and the domain **SCCM Admin account**, then click the **Data Directories** tab

![](/uploads/2017/11/2017-11-05_20-12-27-300x246.png)

- Set the **directory locations** (simply changing the drive letter) based on the disk layout configuration we set during the server setup, then click the **TempDB** tab

![](/uploads/2017/11/2017-11-05_20-13-46-300x246.png)

- We need to add the location directory for the TempDB which is not yet created.  Remove the current directory first
  - **Quick tip**: You can run the following command to create the TempDB directory in advance

```batch
MD "H:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\Data"
```

![](/uploads/2017/11/2017-11-05_20-16-59-300x159.png)

- Add the newly created directory and change the **Log directory** to the same location then click **Next**, then click **Install** and let it do its thing.

<figure class="image-gallery">
<img src="/uploads/2017/11/2017-11-05_20-18-16-290x300.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_20-19-16-300x246.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_20-19-47-300x246.png" alt="" loading="lazy">
<img src="/uploads/2017/11/2017-11-05_20-23-18-300x246.png" alt="" loading="lazy">
</figure>

That completes the installation of Microsoft SQL Server but we still need to do a few more things.

## SQL Server Management Studio Installation
