// Safe storage: if the browser blocks storage (privacy mode, locked-down
// settings) the reader still works — preferences simply stop persisting.
var store = (function () {
  try {
    var probe = "__ri_probe__";
    window.localStorage.setItem(probe, "1");
    window.localStorage.removeItem(probe);
    return window.localStorage;
  } catch (e) {
    var mem = {};
    return {
      getItem: function (k) { return Object.prototype.hasOwnProperty.call(mem, k) ? mem[k] : null; },
      setItem: function (k, v) { mem[k] = String(v); },
      removeItem: function (k) { delete mem[k]; }
    };
  }
})();

  // Silently remove .html from browser address bar
  if (window.location.pathname.endsWith(".html")) {
    var clean = window.location.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "");
    if (!clean) clean = "/";
    window.history.replaceState(null, "", clean + window.location.search + window.location.hash);
  }

// Reverend Insanity — The Omniarch Translation
document.addEventListener("DOMContentLoaded", function () {
  // nav shadow on scroll
  var nav = document.querySelector(".nav");
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // mobile menu (compact box: opens under the burger, closes on any outside tap)
  var burger = document.querySelector(".nav-burger");
  var links = document.querySelector(".nav-links");
  if (burger && links) {
    function closeMenu() {
      links.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
    burger.setAttribute("aria-expanded", "false");
    burger.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = links.classList.toggle("open");
      burger.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (links.classList.contains("open") && !links.contains(e.target)) closeMenu();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 860) closeMenu();
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
  }

  // reveal on scroll
  var reveals = document.querySelectorAll(".reveal");
  var animate = document.documentElement.classList.contains("js-anim");
  if (animate && "IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.05 });
    reveals.forEach(function (el) { io.observe(el); });
    setTimeout(function () {
      reveals.forEach(function (el) { el.classList.add("in"); });
    }, 250);
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // Gentle 3D proximity tilt on the homepage cover (desktop pointers only)
  var coverCard = document.querySelector(".cover-card");
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (coverCard && !reduceMotion && window.matchMedia && window.matchMedia("(pointer: fine)").matches) {
    var tiltZone = coverCard.closest(".hero") || document.body;
    var tiltAnchor = coverCard.parentElement || coverCard;
    var tX = 0, tY = 0, tiltRaf = null;
    var renderTilt = function () {
      tiltRaf = null;
      coverCard.style.transform =
        "perspective(1100px) rotateX(" + tX.toFixed(2) + "deg) rotateY(" + tY.toFixed(2) + "deg)";
    };
    var queueTilt = function () {
      if (!tiltRaf) tiltRaf = requestAnimationFrame(renderTilt);
    };
    tiltZone.addEventListener("mousemove", function (e) {
      var r = tiltAnchor.getBoundingClientRect();
      var cx = r.left + r.width / 2;
      var cy = r.top + r.height / 2;
      var px = e.clientX - cx;
      var py = e.clientY - cy;
      var dist = Math.sqrt(px * px + py * py);
      var influence = Math.max(0, 1 - dist / 720);
      var nx = Math.max(-1, Math.min(1, px / 240));
      var ny = Math.max(-1, Math.min(1, py / 240));
      tY = nx * 9 * influence;
      tX = -ny * 7 * influence;
      queueTilt();
    });
    tiltZone.addEventListener("mouseleave", function () {
      tX = 0;
      tY = 0;
      queueTilt();
    });
  }

  // reading progress bar (chapter pages)
  var bar = document.querySelector(".progress");
  if (bar) {
    var onRead = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    };
    window.addEventListener("scroll", onRead, { passive: true });
    onRead();
  }

  // Theme toggle: "Dark theme" and "Light theme"
  var themeToggle = document.getElementById("themeToggle");
  var themeToggleText = document.getElementById("themeToggleText");

  function updateThemeUI(theme) {
    if (themeToggleText) {
      themeToggleText.textContent = theme === "obsidian" ? "Light theme" : "Dark theme";
    }
    if (themeToggle) {
      var isDark = theme === "obsidian";
      themeToggle.setAttribute("title", isDark ? "Switch to Light theme" : "Switch to Dark theme");
      themeToggle.setAttribute("aria-label", isDark ? "Switch to Light theme" : "Switch to Dark theme");
    }
  }

  // Initial sync on load
  var currentTheme = document.documentElement.getAttribute("data-theme") || "light";
  updateThemeUI(currentTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var isDark = document.documentElement.getAttribute("data-theme") === "obsidian";
      if (isDark) {
        document.documentElement.removeAttribute("data-theme");
        store.setItem("theme", "light");
        updateThemeUI("light");
      } else {
        document.documentElement.setAttribute("data-theme", "obsidian");
        store.setItem("theme", "obsidian");
        updateThemeUI("obsidian");
      }
    });
  }


  // Chapter keyboard navigation (ArrowLeft = previous, ArrowRight = next)
  document.addEventListener("keydown", function (e) {
    if (e.isComposing || e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
    if (tag === "input" || tag === "textarea" || tag === "select" || tag === "button" ||
        tag === "a" || tag === "option" || tag === "summary" || e.target.isContentEditable) return;
    if (e.key === "ArrowLeft") {
      var prevBtn = document.querySelector(".chapter-nav .btn-ghost[href]");
      if (prevBtn && prevBtn.getAttribute("href") && prevBtn.getAttribute("href") !== "#") {
        window.location.href = prevBtn.href;
      }
    } else if (e.key === "ArrowRight") {
      var nextBtn = document.querySelector(".chapter-nav .btn-primary[href]");
      if (nextBtn && nextBtn.getAttribute("href") && nextBtn.getAttribute("href") !== "#" && !nextBtn.getAttribute("aria-disabled")) {
        window.location.href = nextBtn.href;
      }
    }
  });

  // Reader font-size adjustment with persistence
  var proseEl = document.querySelector(".chapter-body .prose");
  var fontDec = document.getElementById("fontDec");
  var fontInc = document.getElementById("fontInc");
  var fontSizes = [15, 17, 19, 21, 23];

  // Reader typefaces: Inter (default), San Francisco/system, OpenDyslexic, and three literary serifs.
  // Each scale compensates for the face's natural x-height so every
  // typeface reads at a comparable visual size at the same setting.
  var READER_FONTS = {
    inter:        { scale: 1.00 },
    sanfrancisco: { scale: 1.00 },
    opendyslexic: { scale: 1.00 },
    cormorant:    { scale: 1.12 },
    newsreader:   { scale: 1.03 },
    spectral:     { scale: 1.05 }
  };

  function currentReaderFont() {
    var f = store.getItem("readerFont");
    return (f && READER_FONTS[f]) ? f : "inter";
  }

  function applyFontSize(size) {
    if (proseEl) {
      var f = currentReaderFont();
      var scale = READER_FONTS[f].scale;
      proseEl.style.fontSize = (Math.round(size * scale * 10) / 10) + "px";
      proseEl.style.lineHeight = (f === "inter") ? (size >= 19 ? "1.9" : "1.95") : "";
      store.setItem("readerFontSize", size);
    }
  }

  function applyReaderFont(key, persist) {
    if (!READER_FONTS[key]) key = "inter";
    document.documentElement.classList.remove("rf-sanfrancisco", "rf-opendyslexic", "rf-cormorant", "rf-newsreader", "rf-spectral");
    if (key !== "inter") document.documentElement.classList.add("rf-" + key);
    if (persist !== false) store.setItem("readerFont", key);
    applyFontSize(parseInt(store.getItem("readerFontSize") || "17", 10));
    var opts = document.querySelectorAll(".font-panel .font-option");
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].getAttribute("data-font") === key) opts[i].classList.add("active");
      else opts[i].classList.remove("active");
    }
  }

  if (proseEl) {
    applyReaderFont(currentReaderFont(), false);

    // Typeface picker ("Aa" button)
    var fpBtn = document.getElementById("fontPickerBtn");
    var fpPanel = document.getElementById("fontPanel");
    if (fpPanel && !fpPanel.querySelector('[data-font="sanfrancisco"]')) {
      var sfOption = document.createElement("button");
      sfOption.className = "font-option";
      sfOption.setAttribute("data-font", "sanfrancisco");
      sfOption.setAttribute("role", "menuitem");
      sfOption.setAttribute("type", "button");
      sfOption.innerHTML = '<span class="fo-name fo-sanfrancisco">San Francisco</span><span class="fo-desc">SF on Apple devices · system sans elsewhere</span><span class="fo-sample fo-sanfrancisco">The Spring Autumn Cicada stirred.</span>';
      var interOption = fpPanel.querySelector('[data-font="inter"]');
      if (interOption && interOption.nextSibling) fpPanel.insertBefore(sfOption, interOption.nextSibling);
      else fpPanel.appendChild(sfOption);
    }
    if (fpBtn && fpPanel) {
      fpBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        var isOpen = fpPanel.classList.toggle("open");
        fpBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
      function closeFontPanel() {
        fpPanel.classList.remove("open");
        fpBtn.setAttribute("aria-expanded", "false");
      }
      document.addEventListener("click", function (e) {
        if (!fpPanel.contains(e.target) && e.target !== fpBtn) closeFontPanel();
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeFontPanel();
      });
      var fpOpts = fpPanel.querySelectorAll(".font-option");
      for (var i = 0; i < fpOpts.length; i++) {
        fpOpts[i].addEventListener("click", function () {
          applyReaderFont(this.getAttribute("data-font"));
          closeFontPanel();
        });
      }
    }

    if (fontDec && fontInc) {
      fontDec.addEventListener("click", function () {
        var current = parseInt(store.getItem("readerFontSize") || "17", 10);
        var idx = fontSizes.indexOf(current);
        if (idx === -1) idx = 1;
        if (idx > 0) applyFontSize(fontSizes[idx - 1]);
      });
      fontInc.addEventListener("click", function () {
        var current = parseInt(store.getItem("readerFontSize") || "17", 10);
        var idx = fontSizes.indexOf(current);
        if (idx === -1) idx = 1;
        if (idx < fontSizes.length - 1) applyFontSize(fontSizes[idx + 1]);
      });
    }

    // Alignment freedom — justify vs left, persisted as readerAlign
    var chapterBodyEl = document.querySelector(".chapter-body");
    var readerAlign = store.getItem("readerAlign");
    function applyAlignment(align, persist) {
      if (!chapterBodyEl) return;
      chapterBodyEl.classList.remove("align-justify", "align-left");
      var prose = chapterBodyEl.querySelector(".prose");
      if (prose) prose.classList.remove("align-justify", "align-left");
      if (align === "justify" || align === "left") {
        chapterBodyEl.classList.add("align-" + align);
        if (prose) prose.classList.add("align-" + align);
        if (persist !== false) store.setItem("readerAlign", align);
      } else {
        if (persist !== false) store.removeItem("readerAlign");
      }
      var alignBtn = document.getElementById("alignToggle");
      if (alignBtn) {
        if (chapterBodyEl.classList.contains("align-justify")) {
          alignBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/></svg>';
          alignBtn.title = "Switch to left-aligned text";
          alignBtn.setAttribute("aria-label", "Switch to left-aligned text");
        } else if (chapterBodyEl.classList.contains("align-left")) {
          alignBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
          alignBtn.title = "Switch to justified text";
          alignBtn.setAttribute("aria-label", "Switch to justified text");
        } else {
          var eff = window.getComputedStyle(chapterBodyEl).textAlign;
          if (eff === "justify") {
            alignBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/></svg>';
            alignBtn.title = "Switch to left-aligned text";
            alignBtn.setAttribute("aria-label", "Switch to left-aligned text");
          } else {
            alignBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
            alignBtn.title = "Switch to justified text";
            alignBtn.setAttribute("aria-label", "Switch to justified text");
          }
        }
      }
    }

    // Apply saved alignment on load
    if (chapterBodyEl && (readerAlign === "justify" || readerAlign === "left")) {
      applyAlignment(readerAlign, false);
    }

    // Create alignment toggle button
    var fontCtrls = document.querySelector(".font-ctrls");
    if (fontCtrls && chapterBodyEl) {
      var alignBtn = document.createElement("button");
      alignBtn.className = "font-btn";
      alignBtn.id = "alignToggle";
      alignBtn.type = "button";
      var effAlign = window.getComputedStyle(chapterBodyEl).textAlign;
      if (effAlign === "justify") {
        alignBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="15" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/></svg>';
        alignBtn.title = "Switch to left-aligned text";
        alignBtn.setAttribute("aria-label", "Switch to left-aligned text");
      } else {
        alignBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
        alignBtn.title = "Switch to justified text";
        alignBtn.setAttribute("aria-label", "Switch to justified text");
      }
      fontCtrls.appendChild(alignBtn);
      alignBtn.addEventListener("click", function () {
        var cur = store.getItem("readerAlign");
        if (!cur) {
          var comp = window.getComputedStyle(chapterBodyEl).textAlign;
          cur = comp === "justify" ? "justify" : "left";
        }
        var nxt = cur === "justify" ? "left" : "justify";
        applyAlignment(nxt, true);
      });

      // Indent toggle - two toggles design
      var readerIndent = store.getItem("readerIndent");
      function applyIndent(indent, persist) {
        if (!chapterBodyEl) return;
        chapterBodyEl.classList.remove("indent-on", "indent-off");
        var prose2 = chapterBodyEl.querySelector(".prose");
        if (prose2) prose2.classList.remove("indent-on", "indent-off");
        if (indent === "on" || indent === "off") {
          chapterBodyEl.classList.add("indent-" + indent);
          if (prose2) prose2.classList.add("indent-" + indent);
          if (persist !== false) store.setItem("readerIndent", indent);
        } else {
          if (persist !== false) store.removeItem("readerIndent");
        }
        var indentBtn = document.getElementById("indentToggle");
        if (indentBtn) {
          if (chapterBodyEl.classList.contains("indent-on")) {
            indentBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="4" x2="21" y2="4"/><line x1="3" y1="8" x2="21" y2="8"/><line x1="7" y1="12" x2="21" y2="12"/><line x1="7" y1="16" x2="21" y2="16"/><line x1="7" y1="20" x2="21" y2="20"/></svg>';
            indentBtn.title = "Switch to no indent";
            indentBtn.setAttribute("aria-label", "Switch to no indent");
          } else {
            indentBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="4" x2="21" y2="4"/><line x1="3" y1="8" x2="21" y2="8"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="16" x2="21" y2="16"/><line x1="3" y1="20" x2="21" y2="20"/></svg>';
            indentBtn.title = "Switch to indented paragraphs";
            indentBtn.setAttribute("aria-label", "Switch to indented paragraphs");
          }
        }
      }

      if (chapterBodyEl && (readerIndent === "on" || readerIndent === "off")) {
        applyIndent(readerIndent, false);
      } else {
        // Default: indent on for book style, but first paragraph no indent for drop cap
        applyIndent("on", false);
      }

      var indentBtn = document.createElement("button");
      indentBtn.className = "font-btn";
      indentBtn.id = "indentToggle";
      indentBtn.type = "button";
      if (chapterBodyEl.classList.contains("indent-on")) {
        indentBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="4" x2="21" y2="4"/><line x1="3" y1="8" x2="21" y2="8"/><line x1="7" y1="12" x2="21" y2="12"/><line x1="7" y1="16" x2="21" y2="16"/><line x1="7" y1="20" x2="21" y2="20"/></svg>';
        indentBtn.title = "Switch to no indent";
        indentBtn.setAttribute("aria-label", "Switch to no indent");
      } else {
        indentBtn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="4" x2="21" y2="4"/><line x1="3" y1="8" x2="21" y2="8"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="16" x2="21" y2="16"/><line x1="3" y1="20" x2="21" y2="20"/></svg>';
        indentBtn.title = "Switch to indented paragraphs";
        indentBtn.setAttribute("aria-label", "Switch to indented paragraphs");
      }
      fontCtrls.appendChild(indentBtn);
      indentBtn.addEventListener("click", function () {
        var cur = store.getItem("readerIndent") || "on";
        var nxt = cur === "on" ? "off" : "on";
        applyIndent(nxt, true);
      });
    }
  }


  
  // Custom copy & right-click for chapter pages — Ch1-9 now copyable with attribution
  var readerBody = document.querySelector(".chapter-body");
  if (readerBody) {
    function isField(el) {
      if (!el) return false;
      var tag = el.tagName ? el.tagName.toLowerCase() : "";
      return tag === "input" || tag === "textarea" || tag === "select" || el.isContentEditable;
    }
    function closestPara(el) {
      if (!el) return null;
      return el.closest ? el.closest(".prose p[id], .prose-poem[id], p[id]") : null;
    }
    function getSelectedText() {
      var sel = window.getSelection();
      return sel ? sel.toString() : "";
    }
    function getChapterInfo() {
      var ch = document.body.getAttribute("data-chapter") || "";
      var chNum = ch ? parseInt(ch, 10) : null;
      return { raw: ch, num: chNum };
    }
    function buildParaUrl(paraEl) {
      var info = getChapterInfo();
      var base = window.location.origin + (info.num ? "/chapter-" + info.num : window.location.pathname.replace(/\.html$/, "").replace(/\/$/, ""));
      var hash = paraEl && paraEl.id ? "#" + paraEl.id : "";
      // Use clean path: /chapter-X#pY
      if (info.num) {
        return window.location.origin + "/chapter-" + info.num + hash;
      }
      return window.location.href.split("#")[0] + hash;
    }
    function buildCitation(selectedOrPara, paraEl) {
      var info = getChapterInfo();
      var url = buildParaUrl(paraEl);
      var chLabel = info.num ? "Chapter " + info.num : "Reverend Insanity";
      var pLabel = paraEl && paraEl.id ? " ¶" + paraEl.id.replace(/^p/, "") : "";
      return selectedOrPara + "\n\n— " + chLabel + pLabel + ", The Omniarch Translation (" + url + ")";
    }

    // 1. Create custom context menu element
    var customMenu = document.createElement("div");
    customMenu.id = "riCustomMenu";
    customMenu.className = "ri-custom-menu";
    customMenu.hidden = true;
    customMenu.innerHTML = '<button type="button" data-act="copy">Copy</button>' +
      '<button type="button" data-act="copyCite">Copy with citation</button>' +
      '<button type="button" data-act="copyLink">Copy paragraph link</button>' +
      '<button type="button" data-act="search">Search selection</button>';
    document.body.appendChild(customMenu);

    var lastContextPara = null;
    var lastContextEvent = null;

    function hideMenu() {
      customMenu.hidden = true;
      customMenu.classList.remove("open");
    }
    function showMenu(x, y) {
      customMenu.style.left = x + "px";
      customMenu.style.top = y + "px";
      customMenu.hidden = false;
      // Adjust if off-screen
      requestAnimationFrame(function () {
        var rect = customMenu.getBoundingClientRect();
        var vw = window.innerWidth, vh = window.innerHeight;
        var nx = x, ny = y;
        if (rect.right > vw - 8) nx = Math.max(8, vw - rect.width - 8);
        if (rect.bottom > vh - 8) ny = Math.max(8, vh - rect.height - 8);
        customMenu.style.left = nx + "px";
        customMenu.style.top = ny + "px";
        customMenu.classList.add("open");
      });
    }

    // 2. Right-click inside prose → show custom menu
    document.addEventListener("contextmenu", function (e) {
      if (isField(e.target)) return; // allow native in inputs
      var inside = e.target.closest ? e.target.closest(".chapter-body, .prose") : null;
      if (!inside) { hideMenu(); return; }
      // Only custom menu for chapter reader
      e.preventDefault();
      lastContextPara = closestPara(e.target);
      lastContextEvent = e;
      var selText = getSelectedText().trim();
      // Update search label
      var searchBtn = customMenu.querySelector('[data-act="search"]');
      if (searchBtn) {
        if (selText) {
          var short = selText.length > 24 ? selText.slice(0, 24) + "…" : selText;
          searchBtn.textContent = 'Search "' + short + '"';
          searchBtn.disabled = false;
        } else {
          searchBtn.textContent = "Search…";
          searchBtn.disabled = true;
        }
      }
      showMenu(e.clientX, e.clientY);
      return false;
    });

    // 3. Menu actions
    customMenu.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-act]");
      if (!btn) return;
      var act = btn.getAttribute("data-act");
      var selText = getSelectedText().trim();
      var paraEl = lastContextPara || (function () {
        // If no para from right-click, try from selection anchor
        var sel = window.getSelection();
        if (sel && sel.anchorNode) {
          var el = sel.anchorNode.nodeType === 1 ? sel.anchorNode : sel.anchorNode.parentElement;
          return closestPara(el);
        }
        return null;
      })();
      var paraText = paraEl ? paraEl.textContent.trim() : "";

      if (act === "copy") {
        var toCopy = selText || paraText;
        if (toCopy && navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(toCopy).catch(function () {});
        } else if (toCopy) {
          // Fallback: execCommand
          var ta = document.createElement("textarea");
          ta.value = toCopy;
          ta.style.position = "fixed"; ta.style.opacity = "0";
          document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); } catch (err) {}
          document.body.removeChild(ta);
        }
      } else if (act === "copyCite") {
        var src = selText || paraText;
        if (!src) { hideMenu(); return; }
        var cited = buildCitation(src, paraEl);
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(cited).catch(function () {});
        } else {
          var ta2 = document.createElement("textarea");
          ta2.value = cited;
          ta2.style.position = "fixed"; ta2.style.opacity = "0";
          document.body.appendChild(ta2); ta2.select();
          try { document.execCommand("copy"); } catch (err) {}
          document.body.removeChild(ta2);
        }
      } else if (act === "copyLink") {
        var link = buildParaUrl(paraEl);
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(link).catch(function () {});
        } else {
          var ta3 = document.createElement("textarea");
          ta3.value = link;
          ta3.style.position = "fixed"; ta3.style.opacity = "0";
          document.body.appendChild(ta3); ta3.select();
          try { document.execCommand("copy"); } catch (err) {}
          document.body.removeChild(ta3);
        }
        // Update URL hash for sharing
        if (paraEl && paraEl.id) {
          try { history.replaceState(null, "", "#" + paraEl.id); } catch (err) {}
        }
      } else if (act === "search") {
        if (!selText) { hideMenu(); return; }
        window.location.href = "/search?q=" + encodeURIComponent(selText);
      }
      hideMenu();
    });

    // Hide on click outside, scroll, escape
    document.addEventListener("click", function (e) {
      if (!customMenu.hidden && !customMenu.contains(e.target)) hideMenu();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") hideMenu();
    });
    window.addEventListener("scroll", function () { if (!customMenu.hidden) hideMenu(); }, { passive: true });
    window.addEventListener("resize", function () { if (!customMenu.hidden) hideMenu(); });

    // 4. Ctrl+C adds attribution footer automatically (for selections inside chapter)
    document.addEventListener("copy", function (e) {
      if (isField(e.target)) return;
      var sel = window.getSelection();
      if (!sel || sel.isCollapsed) return;
      var range = sel.getRangeAt ? sel.getRangeAt(0) : null;
      if (!range) return;
      var container = range.commonAncestorContainer;
      var el = container.nodeType === 1 ? container : container.parentElement;
      if (!el || !el.closest || !el.closest(".chapter-body, .prose")) return;
      var selected = sel.toString();
      if (!selected || selected.length < 20) return; // don't clutter tiny copies
      var paraEl = closestPara(el) || (sel.anchorNode ? closestPara(sel.anchorNode.parentElement) : null);
      var cited = buildCitation(selected, paraEl);
      if (e.clipboardData) {
        e.preventDefault();
        e.clipboardData.setData("text/plain", cited);
      }
    });
  }

  // chapter finder (homepage): filters the list as you type; Enter opens the first match
  var finder = document.getElementById("chapterFilter");
  if (finder) {
    var countOut = document.getElementById("chapterFilterCount");
    var allRows = Array.prototype.slice.call(document.querySelectorAll(".ch-list .ch-row"));
    var queuedRows = allRows.filter(function (r) { return !r.getAttribute("href"); });
    var queuedNums = queuedRows.map(function (r) {
      var n = r.querySelector(".ch-num");
      return (n ? n.textContent : "").trim();
    });
    var shelves = allRows.filter(function (r) { return r.getAttribute("href"); })
      .map(function (r) {
        var n = r.querySelector(".ch-num"), t = r.querySelector(".ch-name");
        return {
          el: r,
          num: (n ? n.textContent : "").trim(),
          hay: ((n ? n.textContent : "") + " " + (t ? t.textContent : "")).toLowerCase()
        };
      });

    function applyFinder() {
      var q = finder.value.trim().toLowerCase();
      var digits = q.replace(/^(chapter|ch)\s*/, "");
      var numeric = /^[0-9]+$/.test(digits);
      var shown = 0, firstHit = null;
      shelves.forEach(function (it) {
        var hit = !q || (numeric ? it.num.indexOf(digits) === 0 : it.hay.indexOf(q) !== -1);
        it.el.hidden = !hit;
        if (hit) { shown++; if (!firstHit) firstHit = it.el; }
      });
      queuedRows.forEach(function (r) { r.hidden = !!q; });
      if (countOut) {
        countOut.textContent = "";
        if (!q) {
          // nothing to say yet
        } else if (shown) {
          countOut.textContent = shown + (shown === 1 ? " chapter" : " chapters") +
            " \u2014 press Enter to open";
        } else if (numeric && queuedNums.indexOf(digits) !== -1) {
          countOut.textContent = "Chapter " + digits +
            " is still at the bench \u2014 not published yet";
        } else {
          // no chapter by that name: offer the whole text
          var phrase = finder.value.trim();
          countOut.appendChild(document.createTextNode("No chapter matches \u201c" + phrase + "\u201d \u2014 "));
          var go = document.createElement("a");
          go.className = "ch-search-fallback";
          go.href = "search?q=" + encodeURIComponent(phrase);
          go.textContent = "search the text for \u201c" + phrase + "\u201d \u2192";
          countOut.appendChild(go);
        }
      }
      return firstHit;
    }

    var firstHit = null;
    finder.addEventListener("input", function () { firstHit = applyFinder(); });
    finder.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        var target = firstHit || applyFinder();
        e.preventDefault();
        if (target) {
          window.location.href = target.getAttribute("href");
        } else if (finder.value.trim()) {
          // nothing in the chapter list — send the phrase to the full-text search
          window.location.href = "search?q=" + encodeURIComponent(finder.value.trim());
        }
      } else if (e.key === "Escape") {
        finder.value = ""; firstHit = null; applyFinder();
      }
    });
    applyFinder();
  }

    // codex & resume: remember reading progress and current paragraph position
  var chAttr = document.body.getAttribute("data-chapter");
  if (chAttr) {
    var chNum = parseInt(chAttr, 10);
    var prevCh = parseInt(store.getItem("riProgress") || "0", 10);
    if (chNum > prevCh) store.setItem("riProgress", String(chNum));

    var activeHash = window.location.hash ? window.location.hash.substring(1) : "";
    var saveResumeState = function (paraId) {
      try {
        var state = {
          ch: chNum,
          p: paraId || "",
          t: Date.now()
        };
        store.setItem("ri_resume", JSON.stringify(state));
      } catch (e) {}
    };

    // If user arrived directly without a hash, check if there was a saved paragraph
    if (!activeHash) {
      try {
        var prevResume = JSON.parse(store.getItem("ri_resume") || "null");
        if (prevResume && prevResume.ch === chNum && prevResume.p && prevResume.p !== "p1") {
          var targetEl = document.getElementById(prevResume.p);
          if (targetEl) {
            var pill = document.createElement("a");
            pill.className = "resume-pill";
            pill.href = "#" + prevResume.p;
            pill.innerHTML = '<span class="rp-icon">\u21B4</span> Resume at \u00b6' + prevResume.p.replace(/^p/, '');
            pill.addEventListener("click", function (ev) {
              ev.preventDefault();
              targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
              try { history.replaceState(null, "", "#" + prevResume.p); } catch (e) {}
              pill.classList.add("fade-out");
              setTimeout(function () { if (pill.parentNode) pill.parentNode.removeChild(pill); }, 400);
            });
            document.body.appendChild(pill);

            var dismissTimer = setTimeout(function () {
              pill.classList.add("fade-out");
              setTimeout(function () { if (pill.parentNode) pill.parentNode.removeChild(pill); }, 400);
            }, 9000);

            var onDismissScroll = function () {
              if (window.scrollY > 400) {
                clearTimeout(dismissTimer);
                pill.classList.add("fade-out");
                setTimeout(function () { if (pill.parentNode) pill.parentNode.removeChild(pill); }, 400);
                window.removeEventListener("scroll", onDismissScroll);
              }
            };
            window.addEventListener("scroll", onDismissScroll, { passive: true });
          }
        }
      } catch (e) {}
    }

    // Observe paragraph visibility to record current reading paragraph
    var proseParas = document.querySelectorAll(".prose p[id]");
    if (proseParas.length && "IntersectionObserver" in window) {
      var pObs = new IntersectionObserver(function (entries) {
        for (var pi = 0; pi < entries.length; pi++) {
          var ent = entries[pi];
          if (ent.isIntersecting && ent.target.id) {
            saveResumeState(ent.target.id);
          }
        }
      }, { rootMargin: "0px 0px -70% 0px" });
      for (var pi = 0; pi < proseParas.length; pi++) {
        pObs.observe(proseParas[pi]);
      }
    } else {
      saveResumeState(activeHash || "p1");
    }
  }

  var revealed = document.body.getAttribute("data-revealed");
  if (revealed) {
    var reached = parseInt(store.getItem("riProgress") || "0", 10);
    var prog = document.getElementById("wikiProgress");
    if (prog) prog.textContent = reached ? "You have read to chapter " + reached : "Not started yet";
    if (reached < parseInt(revealed, 10)) {
      var gate = document.getElementById("wikiGate");
      var wbody = document.getElementById("wikiBody");
      var gm = document.getElementById("wikiGateMsg");
      if (gate && wbody) {
        wbody.hidden = true;
        gate.hidden = false;
        if (gm) gm.textContent = "This entry continues past chapter " + revealed +
          ". You have read to chapter " + (reached || 0) + ".";
      }
    }
  }

  // the trace obeys the reader's position as well: marks from chapters you have
  // not reached are not shown, and the count is recomputed from what is left.
  var trace = document.querySelector(".wiki-trace");
  if (trace && revealed) {
    var reachedT = parseInt(store.getItem("riProgress") || "0", 10);
    if (reachedT && reachedT < 2334) {
      var segs = trace.querySelectorAll(".trace-ch");
      var kept = 0, total = 0, firstA = null, lastA = null;
      for (var si = 0; si < segs.length; si++) {
        var seg = segs[si];
        var cnm = seg.getAttribute("data-ch");
        var cnum = cnm === "preface" ? 0 : parseInt(cnm, 10);
        var open = cnum === 0 || cnum <= reachedT;
        var cells = seg.querySelectorAll(".tc");
        for (var ci = 0; ci < cells.length; ci++) {
          var cell = cells[ci];
          if (!open) {
            cell.removeAttribute("title");
            if (cell.tagName === "A") { cell.removeAttribute("href"); }
            continue;
          }
          total++;
          if (cell.className.indexOf("on") !== -1) {
            kept++;
            if (!firstA) firstA = cell;
            lastA = cell;
          }
        }
        if (!open) seg.className += " trace-off";
      }
      var sum = trace.querySelector(".trace-sum");
      if (sum && firstA) {
        var nameOf = function (a) {
          var m = (a.getAttribute("title") || "").match(/^\s*(Chapter \d+|Preface)\s*\u00b6(\d+)/);
          return m ? [m[1], m[2]] : ["", ""];
        };
        var f = nameOf(firstA), l = nameOf(lastA);
        var pct = total ? Math.round(kept * 100 / total) : 0;
        sum.innerHTML = "Written into <strong>" + kept + "</strong> of <strong>" + total +
          "</strong> paragraphs up to chapter " + reachedT + " (" + pct + "%) \u2014 first at " +
          '<a href="' + firstA.getAttribute("href") + '">' + f[0] + ", \u00b6" + f[1] + "</a>, " +
          "most recently at " + '<a href="' + lastA.getAttribute("href") + '">' + l[0] +
          ", \u00b6" + l[1] + "</a>.";
      }
    }
  }

  // Resume reading banner / dynamic CTA on index page & chapter progress markers
  try {
    var resumeRaw = store.getItem("ri_resume");
    var maxRead = parseInt(store.getItem("riProgress") || "0", 10);
    if (resumeRaw || maxRead > 0) {
      var rData = resumeRaw ? JSON.parse(resumeRaw) : null;
      var targetCh = rData && rData.ch ? rData.ch : maxRead;
      var targetP = rData && rData.ch === targetCh && rData.p ? rData.p : "";

      var ctaRow = document.querySelector(".cta-row");
      var primaryBtn = ctaRow ? ctaRow.querySelector(".btn-primary") : null;
      if (primaryBtn && targetCh > 0) {
        var pHash = targetP && targetP !== "p1" ? "#" + targetP : "";
        var pLabel = targetP && targetP !== "p1" ? " \u00b7 \u00b6" + targetP.replace(/^p/, "") : "";
        primaryBtn.href = "/chapter-" + targetCh + pHash;
        primaryBtn.textContent = "Resume Chapter " + targetCh + pLabel + " \u2192";
        primaryBtn.classList.add("btn-resumed");

        var ctaNote = document.querySelector(".cta-note");
        if (ctaNote) {
          ctaNote.innerHTML = '<span>Picking up where you left off. Or <a href="/preface">read the Preface &rarr;</a></span>';
        }
      }

      // Mark chapters in chapter list
      if (targetCh > 0) {
        var chRows = document.querySelectorAll(".ch-row[href]");
        for (var cri = 0; cri < chRows.length; cri++) {
          var row = chRows[cri];
          var href = row.getAttribute("href") || "";
          var m = href.match(/chapter-(\d+)/);
          if (m) {
            var num = parseInt(m[1], 10);
            if (num === targetCh) {
              row.classList.add("ch-current");
              var pill = row.querySelector(".pill");
              if (pill) pill.textContent = "Current";
              var link = row.querySelector(".ch-link");
              if (link) link.textContent = "Resume \u2192";
            } else if (num < targetCh) {
              row.classList.add("ch-read");
              var pillR = row.querySelector(".pill");
              if (pillR) pillR.textContent = "\u2713 Read";
            }
          }
        }
      }
    }
  } catch (e) {}

  // ── TN — Fresh Rewrite: Blur TN note itself, NOT story ──
  // Logic: When details[data-spoiler] opens, blur .tn-note inside it. Click note/hint to reveal.
  (function initTNBlur() {
    function setupTN(details) {
      if (!details.classList.contains('tn-details')) return;
      if (!details.hasAttribute('data-spoiler')) return;

      details.addEventListener('toggle', function() {
        var note = details.querySelector('.tn-note');
        if (!note) return;

        if (details.open) {
          // On open: blur note, show hint
          note.classList.add('tn-blurred');
          note.classList.remove('is-revealed');

          // Remove old hint if exists
          var oldHint = note.querySelector('.tn-unblur-hint');
          if (oldHint) oldHint.remove();

          var hint = document.createElement('button');
          hint.type = 'button';
          hint.className = 'tn-unblur-hint';
          hint.textContent = 'Spoiler — tap to reveal';
          hint.addEventListener('click', function(ev) {
            ev.stopPropagation();
            note.classList.remove('tn-blurred');
            note.classList.add('is-revealed');
            hint.remove();
          });
          note.appendChild(hint);
        } else {
          // On close: reset
          note.classList.remove('tn-blurred');
          note.classList.remove('is-revealed');
          var h = note.querySelector('.tn-unblur-hint');
          if (h) h.remove();
        }
      });
    }

  // Style Rank Roman numerals to avoid i/l confusion — wrap I, II, III, IV, V, etc.
  (function styleRankRomans() {
    var prose = document.querySelectorAll(".prose, .chapter-body");
    if (!prose.length) return;
    var rankRe = /\bRank\s+([IVX]+)\b/g;
    prose.forEach(function(container) {
      // Avoid double-wrapping
      if (container.dataset.rankStyled) return;
      container.dataset.rankStyled = "1";
      container.innerHTML = container.innerHTML.replace(rankRe, function(match, roman) {
        return 'Rank <span class="rank-roman">' + roman + '</span>';
      });
    });
  })();

    // Setup existing TNs
    var allTN = document.querySelectorAll('.tn-details[data-spoiler]');
    for (var i = 0; i < allTN.length; i++) {
      setupTN(allTN[i]);
    }

    // Click on blurred note itself to reveal (not just hint)
    document.addEventListener('click', function(e) {
      var note = e.target.closest('.tn-details[data-spoiler][open] .tn-note.tn-blurred');
      if (!note) return;
      if (e.target.closest('.tn-unblur-hint')) return; // hint handles itself
      note.classList.remove('tn-blurred');
      note.classList.add('is-revealed');
      var hint = note.querySelector('.tn-unblur-hint');
      if (hint) hint.remove();
    });
  })();

  // footer year
  var y = document.querySelector(".year");
  if (y) y.textContent = new Date().getFullYear();
});

// Notes tabs — peak pro complex
document.addEventListener("DOMContentLoaded", function() {
  var notesSections = document.querySelectorAll(".notes-section");
  notesSections.forEach(function(section) {
    var tabs = section.querySelectorAll(".notes-tab");
    var panels = section.querySelectorAll(".notes-panel");
    
    tabs.forEach(function(tab) {
      tab.addEventListener("click", function() {
        var target = tab.getAttribute("data-tab");
        
        // Deactivate all
        tabs.forEach(function(t) { t.classList.remove("active"); });
        panels.forEach(function(p) { p.classList.remove("active"); });
        
        // Activate target
        tab.classList.add("active");
        var panel = section.querySelector('.notes-panel[data-panel="'+target+'"]');
        if (panel) panel.classList.add("active");
      });
    });
  });
  
  // Superscript refs — fixed: allow /notes#ch1-... to navigate, don't block
  var allRefs = document.querySelectorAll(".note-ref");
  allRefs.forEach(function(ref) {
    ref.addEventListener("click", function(e) {
      var href = ref.getAttribute("href") || "";
      // If it's a link to /notes#... — let it navigate (smart superscript system)
      if (href.indexOf("/notes#") !== -1 || href.indexOf("#ch") === 0) {
        // Don't prevent — allow navigation to notes page with hash
        // If same page anchor (world page world-ch1-...), handle smooth scroll
        if (href.charAt(0) === "#" || href.indexOf("#world-") !== -1) {
          var targetId = href.split("#")[1];
          var targetNote = document.getElementById(targetId);
          if (targetNote) {
            e.preventDefault();
            // Switch tab if needed
            var panel = targetNote.closest(".chapter-panel") || targetNote.closest(".notes-panel");
            if (panel) {
              var ch = panel.getAttribute("data-ch") || panel.getAttribute("data-panel");
              if (ch) {
                var tab = document.querySelector('.chapter-tab[data-ch="'+ch+'"]') || document.querySelector('.notes-tab[data-tab="'+ch+'"]');
                if (tab) tab.click();
              }
            }
            setTimeout(function() {
              targetNote.scrollIntoView({ behavior: "smooth", block: "center" });
              targetNote.style.animation = "noteFlash 1.8s ease";
              setTimeout(function() { targetNote.style.animation = ""; }, 1800);
            }, 120);
          }
        }
        return; // allow /notes# navigation
      }
      // Legacy: note-1, note-2 on same page
      e.preventDefault();
      var noteId = ref.getAttribute("data-note") || ref.textContent.trim();
      var targetNote = document.getElementById("note-" + noteId);
      if (targetNote) {
        var panel = targetNote.closest(".notes-panel");
        if (panel) {
          var panelName = panel.getAttribute("data-panel");
          var notesSection = document.querySelector(".notes-section");
          if (notesSection) {
            var tab = notesSection.querySelector('.notes-tab[data-tab="'+panelName+'"]');
            if (tab) tab.click();
          }
        }
        setTimeout(function() {
          targetNote.scrollIntoView({ behavior: "smooth", block: "center" });
          targetNote.style.animation = "noteFlash 1.8s ease";
          setTimeout(function() { targetNote.style.animation = ""; }, 1800);
        }, 100);
      }
    });
  });
});
