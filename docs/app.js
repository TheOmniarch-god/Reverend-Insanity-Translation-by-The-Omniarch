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
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
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
        localStorage.setItem("theme", "light");
        updateThemeUI("light");
      } else {
        document.documentElement.setAttribute("data-theme", "obsidian");
        localStorage.setItem("theme", "obsidian");
        updateThemeUI("obsidian");
      }
    });
  }


  // Chapter keyboard navigation (ArrowLeft = previous, ArrowRight = next)
  document.addEventListener("keydown", function (e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.isComposing) return;
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

  // Reader typefaces: Inter (default) + three premium serifs.
  // Each scale compensates for the face's natural x-height so every
  // typeface reads at a comparable visual size at the same setting.
  var READER_FONTS = {
    inter:      { scale: 1.00 },
    cormorant:  { scale: 1.12 },
    newsreader: { scale: 1.03 },
    spectral:   { scale: 1.05 }
  };

  function currentReaderFont() {
    var f = localStorage.getItem("readerFont");
    return (f && READER_FONTS[f]) ? f : "inter";
  }

  function applyFontSize(size) {
    if (proseEl) {
      var f = currentReaderFont();
      var scale = READER_FONTS[f].scale;
      proseEl.style.fontSize = (Math.round(size * scale * 10) / 10) + "px";
      proseEl.style.lineHeight = (f === "inter") ? (size >= 19 ? "1.9" : "1.95") : "";
      localStorage.setItem("readerFontSize", size);
    }
  }

  function applyReaderFont(key, persist) {
    if (!READER_FONTS[key]) key = "inter";
    document.documentElement.classList.remove("rf-cormorant", "rf-newsreader", "rf-spectral");
    if (key !== "inter") document.documentElement.classList.add("rf-" + key);
    if (persist !== false) localStorage.setItem("readerFont", key);
    applyFontSize(parseInt(localStorage.getItem("readerFontSize") || "17", 10));
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
          fpPanel.classList.remove("open");
        });
      }
    }

    if (fontDec && fontInc) {
      fontDec.addEventListener("click", function () {
        var current = parseInt(localStorage.getItem("readerFontSize") || "17", 10);
        var idx = fontSizes.indexOf(current);
        if (idx === -1) idx = 1;
        if (idx > 0) applyFontSize(fontSizes[idx - 1]);
      });
      fontInc.addEventListener("click", function () {
        var current = parseInt(localStorage.getItem("readerFontSize") || "17", 10);
        var idx = fontSizes.indexOf(current);
        if (idx === -1) idx = 1;
        if (idx < fontSizes.length - 1) applyFontSize(fontSizes[idx + 1]);
      });
    }
  }


  
  // Anti-theft & copy protection on chapter reader pages
  var readerBody = document.querySelector(".chapter-body");
  if (readerBody) {
    // 1. Disable context menu (right-click)
    document.addEventListener("contextmenu", function (e) {
      e.preventDefault();
      return false;
    });

    // 2. Disable text selection and dragging
    document.addEventListener("selectstart", function (e) {
      e.preventDefault();
      return false;
    });
    document.addEventListener("dragstart", function (e) {
      e.preventDefault();
      return false;
    });

    // 3. Clear and intercept copy / cut
    document.addEventListener("copy", function (e) {
      e.preventDefault();
      if (e.clipboardData) {
        e.clipboardData.setData("text/plain", "");
      }
      return false;
    });
    document.addEventListener("cut", function (e) {
      e.preventDefault();
      return false;
    });

    // 4. Block common copy & inspect shortcuts (Ctrl/Cmd + C, A, U, S, P, F12)
    document.addEventListener("keydown", function (e) {
      var isMac = navigator.platform.toUpperCase().indexOf("MAC") >= 0;
      var ctrl = isMac ? e.metaKey : e.ctrlKey;
      var key = e.key ? e.key.toLowerCase() : "";
      if (ctrl && (key === "c" || key === "a" || key === "u" || key === "s" || key === "p")) {
        e.preventDefault();
        return false;
      }
      if (e.key === "F12") {
        e.preventDefault();
        return false;
      }
    });
  }

    // footer year
  var y = document.querySelector(".year");
  if (y) y.textContent = new Date().getFullYear();
});
