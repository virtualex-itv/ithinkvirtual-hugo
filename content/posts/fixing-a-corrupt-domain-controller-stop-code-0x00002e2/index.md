{
  "title": "Fixing A Corrupt Domain Controller – Stop Code 0x00002e2",
  "date": "2017-11-13T02:22:23",
  "lastmod": "2018-02-10T14:11:59",
  "slug": "fixing-a-corrupt-domain-controller-stop-code-0x00002e2",
  "url": "/posts/fixing-a-corrupt-domain-controller-stop-code-0x00002e2/",
  "draft": false,
  "description": "Yesterday morning I discovered that my Synology NAS had an unexpected shutdown in the middle of the night while my homelab VMs/workloads were still running.  This caused both of my Domain Controllers databases to become corrupt resulting in being unable to boot those machines.  When attempting to boot them, they would get stuck in a BSOD…",
  "wordpress_id": 905,
  "wordpress_url": "https://ithinkvirtual.com/2017/11/12/fixing-a-corrupt-domain-controller-stop-code-0x00002e2/",
  "featured_image": "/uploads/2017/11/2017-11-12_19-12-46.png",
  "categories": [
    "How-To's"
  ],
  "tags": [
    "homelab",
    "How-To's",
    "Troubleshooting",
    "Windows Server"
  ],
  "years": [
    "2017"
  ],
  "aliases": [
    "/2017/11/12/fixing-a-corrupt-domain-controller-stop-code-0x00002e2/"
  ],
  "comments": []
}

Yesterday morning I discovered that my Synology NAS had an unexpected shutdown in the middle of the night while my homelab VMs/workloads were still running.  This caused both of my Domain Controllers databases to become corrupt resulting in being unable to boot those machines.  When attempting to boot them, they would get stuck in a BSOD boot-loop and would display a Stop Error Code of 0x00002e2.

.

After some research I was able to figure out how to recover my VMs and get them to boot up again.  This had happened to me once before sometime earlier this year and luckily I remembered that I had taken some notes on how to fix it so I figured this time I would put together a formal “How To:” guide to have it documented for myself and hopefully to help others facing this issue as well.  So without further adieu…let’s get to it!

.

To start, you will need to power-on the machine and then keep pressing the **F8** key to bring up the “**Advanced Boot Options**” boot menu.  Navigate down to **Directory Services Repair Mode** enter press **Enter** to boot you into Safe Mode.

![](/uploads/2017/11/2017-11-12_15-57-52-300x226.png)

When you reach the login screen, log in with the **Local Administrator** account since Active Directory Domain Services are obviously unavailable.

![](/uploads/2017/11/2017-11-12_16-00-53-300x226.png)

Once at the Desktop, open an elevated **Command Prompt** window.

![](/uploads/2017/11/2017-11-12_16-03-09-300x226.png)

As a best practice, I feel it is always wise and important to make a backup of the files before doing any modifications.  Since we will be backing up the NTDS directory, create a directory at your preferred location to store the backup files.  I chose to make a backup folder on the root of “**C:\**” and a sub-directory with the name/date of the directory I am backing up.

```batch
md C:\Backup\NTDS_11122017
```

Then copy everything from the “C:\Windows\NTDS” directory to this new location using xcopy.

```batch
xcopy C:\Windows\NTDS\* C:\Backup\NTDS_11122017 /E /Y /V /C /I
```

![](/uploads/2017/11/2017-11-12_16-11-23-300x159.png)

Once done, let’s rename any .log file extensions in the NTDS directory to .log.old

```bash
cd C:\Windows\NTDS

ren *.log *.log.old
```

![](/uploads/2017/11/2017-11-12_16-28-55-300x159.png)

Now, this is where we get to the good stuff!

First, run the following command to repair the database.

```batch
esentutl /p "C:\Windows\NTDS\ntds.dit"
```

![](/uploads/2017/11/2017-11-12_16-31-06-300x159.png)

This will display the following warning message, click “**OK**“

![](/uploads/2017/11/2017-11-12_16-31-41-300x116.png)

Let it do its thing and you will see the following once complete.

![](/uploads/2017/11/2017-11-12_16-35-59-259x300.png)

Now we need to use the NTDS Utility (ntdsutil.exe) to activate the NTDS instance and compact the DB to a new file which will then be used to overwrite the original.  I will be compacting it to a new TEMP directory within the NTDS directory.  The command will automatically create the new directory if it’s not already present.  Enter the following commands.

```batch
ntdsutil

activate instance ntds

files

compact to C:\Windows\NTDS\TEMP
```

If successful, you will be presented with instructions to copy the newly compacted file to the NTDS directory, overwriting the original, and also to delete any .log files in the NTDS directory.  Before we can do that we need to exit out of the ntdsutil.  Type ***quit*** twice to exit.

```batch
quit

quit
```

![](/uploads/2017/11/2017-11-12_16-48-11-300x159.png)

Let’s follow those instructions and also delete the *.log.old files we renamed earlier.

```batch
copy "C:\Windows\NTDS\TEMP\ntds.dit" "C:\Windows\NTDS\ntds.dit"

Yes
```

Ensure you are still in the NTDS directory before entering the following delete commands.

```batch
del *.log

del *.log.old
```

![](/uploads/2017/11/2017-11-12_16-51-21-300x159.png)

The hard part is now over!  Let’s go ahead and reboot the machine normally.

![](/uploads/2017/11/2017-11-12_16-52-06-300x226.png)

If all goes well and as expected, your machine will boot successfully and you can log in again with an Active Directory Domain Admin account.

![](/uploads/2017/11/2017-11-12_16-55-24-300x226.png) ![](/uploads/2017/11/2017-11-12_16-58-10-300x226.png)

Awesome!  Well, I hope you’ve found this guide useful.  Please feel free to share this and provide me some feedback/comments below.  Thanks for reading!

-virtualex-
