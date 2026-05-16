(() => {
  // Theme toggle. Initial theme is applied by the inline bootstrap in baseof.html
  // to avoid flash; this handler just flips it on click and persists the choice.
  const themeToggle = document.querySelector("[data-theme-toggle]");
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const isLight = document.documentElement.getAttribute("data-theme") === "light";
      if (isLight) {
        document.documentElement.removeAttribute("data-theme");
        try { localStorage.removeItem("theme"); } catch (e) {}
      } else {
        document.documentElement.setAttribute("data-theme", "light");
        try { localStorage.setItem("theme", "light"); } catch (e) {}
      }
    });
  }

  document.querySelectorAll("[data-copy-feed]").forEach((btn) => {
    const label = btn.querySelector(".subscribe-copy-label");
    const original = label ? label.textContent : null;
    btn.addEventListener("click", async () => {
      const url = btn.getAttribute("data-copy-feed");
      try {
        await navigator.clipboard.writeText(url);
      } catch (e) {
        const ta = document.createElement("textarea");
        ta.value = url;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (err) {}
        document.body.removeChild(ta);
      }
      btn.classList.add("is-copied");
      if (label) label.textContent = "Copied!";
      setTimeout(() => {
        btn.classList.remove("is-copied");
        if (label && original !== null) label.textContent = original;
      }, 1800);
    });
  });

  const content = document.querySelector(".content");

  if (content) {
    const headings = Array.from(content.querySelectorAll("h2, h3, h4"));
    const toc = document.querySelector("[data-post-toc]");
    const tocNav = toc ? toc.querySelector("nav") : null;
    const usedIds = new Set(Array.from(document.querySelectorAll("[id]")).map((node) => node.id));

    function slugify(value) {
      const base = value
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, "")
        .trim()
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-");
      return base || "section";
    }

    function uniqueId(value) {
      const base = slugify(value);
      let id = base;
      let index = 2;
      while (usedIds.has(id)) {
        id = `${base}-${index}`;
        index += 1;
      }
      usedIds.add(id);
      return id;
    }

    headings.forEach((heading) => {
      const text = heading.textContent.trim();
      if (!text) return;
      if (!heading.id) heading.id = uniqueId(text);
      if (!heading.querySelector(".heading-anchor")) {
        const anchor = document.createElement("a");
        anchor.className = "heading-anchor";
        anchor.href = `#${heading.id}`;
        anchor.setAttribute("aria-label", `Link to ${text}`);
        anchor.textContent = "#";
        heading.appendChild(anchor);
      }
    });

    if (toc && tocNav && headings.length >= 3) {
      const list = document.createElement("ol");
      headings.forEach((heading) => {
        const item = document.createElement("li");
        item.className = `toc-level-${heading.tagName.slice(1)}`;
        const link = document.createElement("a");
        link.href = `#${heading.id}`;
        link.textContent = heading.textContent.replace("#", "").trim();
        item.appendChild(link);
        list.appendChild(item);
      });
      tocNav.appendChild(list);
      toc.hidden = false;
    }
  }

  const images = Array.from(document.querySelectorAll(".content img"));
  if (!images.length) return;

  const overlay = document.createElement("div");
  overlay.className = "image-lightbox";
  overlay.setAttribute("aria-hidden", "true");
  overlay.innerHTML = [
    '<button class="image-lightbox__close" type="button" aria-label="Close image">x</button>',
    '<img class="image-lightbox__image" alt="">',
  ].join("");
  document.body.appendChild(overlay);

  const lightboxImage = overlay.querySelector(".image-lightbox__image");
  const closeButton = overlay.querySelector(".image-lightbox__close");

  // WordPress thumbnails embed the displayed dimensions in the filename:
  //   /uploads/2016/03/foo-300x200.png  (thumbnail shown on the page)
  //   /uploads/2016/03/foo.png          (full-resolution original)
  // The lightbox wants the original so the zoomed image isn't a blurry upscale.
  function fullResUrl(src) {
    return src.replace(/-\d+x\d+(\.\w+)(\?.*)?$/, "$1$2");
  }

  function openLightbox(image) {
    const original = image.currentSrc || image.src;
    const fullRes = fullResUrl(original);
    // Try full-res first; fall back to the displayed thumbnail if the original is missing.
    lightboxImage.onerror = () => {
      if (lightboxImage.src !== original) {
        lightboxImage.onerror = null;
        lightboxImage.src = original;
      }
    };
    lightboxImage.src = fullRes;
    lightboxImage.alt = image.alt || "";
    overlay.classList.add("is-open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.classList.add("has-lightbox");
    closeButton.focus();
  }

  function closeLightbox() {
    overlay.classList.remove("is-open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.classList.remove("has-lightbox");
    lightboxImage.removeAttribute("src");
  }

  images.forEach((image) => {
    const link = image.closest("a");
    if (link) {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        openLightbox(image);
      });
      return;
    }

    image.tabIndex = 0;
    image.setAttribute("role", "button");
    image.setAttribute("aria-label", image.alt ? `Open image: ${image.alt}` : "Open image");
    image.addEventListener("click", () => openLightbox(image));
    image.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openLightbox(image);
      }
    });
  });

  closeButton.addEventListener("click", closeLightbox);
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) closeLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && overlay.classList.contains("is-open")) {
      closeLightbox();
    }
  });
})();
