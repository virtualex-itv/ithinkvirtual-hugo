{
  "title": "Goodbye WordPress, Hello Hugo!",
  "date": "2026-05-18T00:00:00-04:00",
  "lastmod": "2026-05-18T00:00:00-04:00",
  "slug": "goodbye-wordpress-hello-hugo",
  "url": "/posts/goodbye-wordpress-hello-hugo/",
  "draft": false,
  "description": "After 10 years running on WordPress, I migrated iThinkVirtual to Hugo. Here's why I made the change and what writing on the new stack feels like.",
  "featured_image": "blog-migration.png",
  "categories": [
    "Meta"
  ],
  "tags": [
    "Blogging",
    "Hugo",
    "WordPress",
    "Cloudflare Pages",
    "Migration"
  ],
  "years": [
    "2026"
  ],
  "aliases": [],
  "comments": []
}

Hello all, and thanks so much for stopping by!  First off, let me start by apologizing for being quiet for a bit...I took some time to focus on a brand new project here on the blog, and I'm excited to finally be back at it on a fresh new platform!

After running on [WordPress](https://wordpress.com/) for the better part of 10 years, I finally pulled the trigger and migrated this site over to [Hugo](https://gohugo.io/).  WordPress was a great place to start when I first launched iThinkVirtual back in the day...it got me online quickly, themes were plentiful, and there was a plugin for just about anything I wanted to do.  But over time, things started to wear on me...

## Why leave WordPress?

If I'm being completely honest, I started to dread the idea of writing new posts.  There wasn't really any one big thing, just a bunch of smaller things that piled up over time.

The admin console was a bit slow at times.  The plugin sprawl was very real!  SEO, comments, caching, image optimization, security...each one with its own update cadence and the occasional breaking change to deal with.  And then there was the newer block editor...it was fine in theory, but it just wasn't as intuitive as I'd hoped when all I really wanted to do was write some Markdown.  Even simple things like dropping an image in between two paragraphs felt way more involved than they should have been, and a lot of those little annoyances just added up over time!

Honestly, the platform and editor friction was what did me in.  Once I caught myself procrastinating on writing new posts simply because I dreaded firing up the editor, I knew it was time to make a change!

## Why Hugo?

I wanted something that was Markdown-native so I could just write files on disk...no database, no admin console.  Something fast, both to write and to publish.  Something I had real control of so I could version it in git and deploy it anywhere I wanted to.  And something that was plugin-free...just a static site generator and some templates that I could actually read and tweak as needed.

[Hugo](https://gohugo.io/) checked every single box!  Builds are incredibly fast (the entire site builds in under 2 seconds locally!), the content is just plain Markdown files in a sane folder structure, and I get to manage everything in git the same way I manage every other code project I work on.

## What got migrated?

Pretty much everything!

- All of my existing posts are now plain Markdown.
- All of the categories, tags, and old date-based permalinks (`/2017/05/15/post-name/`) still work...they just redirect to the new URLs so nothing breaks on the internet.
- Featured images and screenshots are all preserved as well.
- And yes...the original Disqus comments on every old post are also kept and rendered separately under a *"Historical Comments"* section so that nothing is lost to history!

For new comments going forward, I've switched from [Disqus](https://disqus.com/) to [Giscus](https://giscus.app/), which is backed by [GitHub](https://github.com/) Discussions.  It's lightweight, no ads, no tracking, and the threads live as long as the repo does!

## What writing is like now

Man, what a difference!  To write a new post now, all I have to do is run the following:

```bash
hugo new posts/my-new-post/index.md
```

That creates a folder with a Markdown file.  I open it up in my editor, write the content, drop any screenshots into the same folder, save the file, and then `git push`.  A few seconds later, [Cloudflare Pages](https://pages.cloudflare.com/) has rebuilt the site and the post is live!  No console to wait on, no plugins to update, no surprises...just writing!

The whole experience has been a massive quality-of-life upgrade for me, and I'm actually looking forward to writing again...which is kind of the whole point of having a blog in the first place!

## What's next?

More content, of course!  Going forward, most of my VMware focus has shifted over to [VMware Cloud Foundation (VCF)](https://www.vmware.com/products/cloud-infrastructure/vmware-cloud-foundation), which is essentially the whole stack wrapped up under one umbrella...vSphere, NSX, vSAN, and the VCF Suite (formerly Aria/vRealize Suite) all rolled into one platform.  So expect a lot of VCF-flavored content going forward, starting with some VCF 9.x upgrade stuff I've been working through in the lab.

Outside of VCF, I've also got my eye on writing about [Veeam Backup and Recovery](https://www.veeam.com/products/virtual/vmware-backup-recovery.html), plus some [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) [MCP (Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro) and other tooling I've been playing around with lately.  And of course, more home lab content as it continues to evolve!

Thanks as always for stopping by and for sticking around all these years.  Here's to the next 10!

-virtualex-
