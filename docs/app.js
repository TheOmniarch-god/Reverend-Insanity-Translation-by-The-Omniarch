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

  // mobile menu
  var burger = document.querySelector(".nav-burger");
  var links = document.querySelector(".nav-links");
  if (burger && links) {
    burger.addEventListener("click", function () {
      links.classList.toggle("open");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { links.classList.remove("open"); });
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
  
  function applyFontSize(size) {
    if (proseEl) {
      proseEl.style.fontSize = size + "px";
      proseEl.style.lineHeight = (size >= 19 ? "1.9" : "1.95");
      localStorage.setItem("readerFontSize", size);
    }
  }

  if (proseEl) {
    var savedSize = parseInt(localStorage.getItem("readerFontSize") || "17", 10);
    if (savedSize !== 17) applyFontSize(savedSize);
    
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


  // ============================================================
  // FROST POWERS ENGINE — Procedural Crystalline Ice Growth (3.8s)
  // Creeps inward like ice magic / Northern Dark Ice Soul frost
  // ============================================================
  var frostCanvas = document.getElementById("frostCanvas");
  var companionSection = document.getElementById("companionSection") || document.querySelector(".companion-section");

  if (frostCanvas && companionSection) {
    var ctx = frostCanvas.getContext("2d");
    var branches = [];
    var isFrozen = false;
    var animStart = null;
    var duration = 3800; // 3.8 seconds freeze animation
    var dpr = window.devicePixelRatio || 1;
    var width = 0;
    var height = 0;

    function resizeFrost() {
      var rect = companionSection.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      frostCanvas.width = width * dpr;
      frostCanvas.height = height * dpr;
      frostCanvas.style.width = width + "px";
      frostCanvas.style.height = height + "px";
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
      generateIceSeeds();
      if (isFrozen) {
        renderFrame(1);
      }
    }

    function generateIceSeeds() {
      branches = [];
      if (!width || !height) return;

      var maxCornerReach = Math.min(220, Math.min(width, height) * 0.38);
      var maxEdgeReach = Math.min(115, Math.min(width, height) * 0.22);

      // Helper to add branch
      function addBranch(ox, oy, targetAngle, targetLen, isCorner) {
        var subBranches = [];
        var numSubs = isCorner ? 4 : 3;
        var step = targetLen / (numSubs + 1);

        for (var i = 1; i <= numSubs; i++) {
          var dist = step * i;
          var subLen = (targetLen - dist) * 0.55;
          // 60-degree hexagonal ice symmetry
          subBranches.push({
            dist: dist,
            len: subLen,
            angleOffset: 1.05 // ~60 deg
          });
          subBranches.push({
            dist: dist,
            len: subLen * 0.9,
            angleOffset: -1.05 // ~ -60 deg
          });
        }

        branches.push({
          ox: ox,
          oy: oy,
          angle: targetAngle,
          len: targetLen,
          isCorner: isCorner,
          subs: subBranches,
          glintPhase: Math.random() * Math.PI * 2
        });
      }

      // 1. Four Corners (Denser & Deeper Reach)
      var cornerPoints = [
        { x: 0, y: 0, baseAngle: Math.PI / 4 }, // Top-Left
        { x: width, y: 0, baseAngle: (3 * Math.PI) / 4 }, // Top-Right
        { x: 0, y: height, baseAngle: -Math.PI / 4 }, // Bottom-Left
        { x: width, y: height, baseAngle: -(3 * Math.PI) / 4 } // Bottom-Right
      ];

      cornerPoints.forEach(function (c) {
        for (var i = 0; i < 9; i++) {
          var spread = (Math.random() - 0.5) * 0.85;
          var len = maxCornerReach * (0.65 + Math.random() * 0.45);
          addBranch(c.x, c.y, c.baseAngle + spread, len, true);
        }
      });

      // 2. Top Edge
      var numX = Math.max(16, Math.floor(width / 50));
      for (var i = 1; i < numX; i++) {
        var x = (width / numX) * i;
        var len = maxEdgeReach * (0.55 + Math.random() * 0.55);
        var angle = Math.PI / 2 + (Math.random() - 0.5) * 0.6;
        addBranch(x, 0, angle, len, false);
      }

      // 3. Bottom Edge
      for (var i = 1; i < numX; i++) {
        var x = (width / numX) * i;
        var len = maxEdgeReach * (0.55 + Math.random() * 0.55);
        var angle = -Math.PI / 2 + (Math.random() - 0.5) * 0.6;
        addBranch(x, height, angle, len, false);
      }

      // 4. Left & Right Edges
      var numY = Math.max(10, Math.floor(height / 55));
      for (var i = 1; i < numY; i++) {
        var y = (height / numY) * i;
        var len = maxEdgeReach * (0.55 + Math.random() * 0.55);
        addBranch(0, y, (Math.random() - 0.5) * 0.6, len, false);
        addBranch(width, y, Math.PI + (Math.random() - 0.5) * 0.6, len, false);
      }
    }

    function easeOutQuart(x) {
      return 1 - Math.pow(1 - x, 4);
    }

    function renderFrame(progress, timeMs) {
      ctx.clearRect(0, 0, width, height);
      if (!branches.length) return;

      var isDark = document.documentElement.getAttribute("data-theme") === "obsidian";

      // Color Palette
      var spineColor = isDark ? "rgba(255, 255, 255, 0.98)" : "rgba(255, 255, 255, 0.96)";
      var crystalColor = isDark ? "rgba(100, 205, 255, 0.85)" : "rgba(185, 225, 255, 0.9)";
      var facetColor = isDark ? "rgba(30, 95, 175, 0.22)" : "rgba(205, 235, 255, 0.35)";
      var glowColor = isDark ? "rgba(65, 170, 255, 0.65)" : "rgba(165, 220, 255, 0.75)";

      ctx.save();
      ctx.shadowColor = glowColor;
      ctx.shadowBlur = isDark ? 9 : 6;

      // Draw all growing branches
      for (var b = 0; b < branches.length; b++) {
        var br = branches[b];
        var curLen = br.len * progress;
        if (curLen <= 1) continue;

        var cosA = Math.cos(br.angle);
        var sinA = Math.sin(br.angle);
        var tipX = br.ox + cosA * curLen;
        var tipY = br.oy + sinA * curLen;

        // Draw Sub-branches (needles)
        for (var s = 0; s < br.subs.length; s++) {
          var sub = br.subs[s];
          if (curLen > sub.dist) {
            var subProgress = Math.min(1, (curLen - sub.dist) / (br.len * 0.4));
            var subCurLen = sub.len * subProgress;

            var subOx = br.ox + cosA * sub.dist;
            var subOy = br.oy + sinA * sub.dist;
            var subAngle = br.angle + sub.angleOffset;
            var subTipX = subOx + Math.cos(subAngle) * subCurLen;
            var subTipY = subOy + Math.sin(subAngle) * subCurLen;

            // Draw facet triangle
            if (subProgress > 0.4) {
              ctx.beginPath();
              ctx.moveTo(subOx, subOy);
              ctx.lineTo(subTipX, subTipY);
              ctx.lineTo(br.ox + cosA * Math.min(curLen, sub.dist + subCurLen * 0.7), br.oy + sinA * Math.min(curLen, sub.dist + subCurLen * 0.7));
              ctx.closePath();
              ctx.fillStyle = facetColor;
              ctx.fill();
            }

            // Draw needle line
            ctx.beginPath();
            ctx.moveTo(subOx, subOy);
            ctx.lineTo(subTipX, subTipY);
            ctx.strokeStyle = crystalColor;
            ctx.lineWidth = 1.3;
            ctx.stroke();
          }
        }

        // Draw Main Spine
        ctx.beginPath();
        ctx.moveTo(br.ox, br.oy);
        ctx.lineTo(tipX, tipY);
        ctx.strokeStyle = spineColor;
        ctx.lineWidth = br.isCorner ? 2.2 : 1.6;
        ctx.stroke();

        // Draw diamond glint at tip
        if (progress > 0.85 && (b % 4 === 0)) {
          var glintAlpha = 0.5 + 0.5 * Math.sin((timeMs ? timeMs * 0.003 : 1) + br.glintPhase);
          drawGlint(tipX, tipY, 4.5 * glintAlpha, isDark);
        }
      }

      ctx.restore();
    }

    function drawGlint(gx, gy, r, isDark) {
      if (r < 0.5) return;
      ctx.save();
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.moveTo(gx, gy - r * 1.6);
      ctx.lineTo(gx + r * 0.3, gy - r * 0.3);
      ctx.lineTo(gx + r * 1.6, gy);
      ctx.lineTo(gx + r * 0.3, gy + r * 0.3);
      ctx.lineTo(gx, gy + r * 1.6);
      ctx.lineTo(gx - r * 0.3, gy + r * 0.3);
      ctx.lineTo(gx - r * 1.6, gy);
      ctx.lineTo(gx - r * 0.3, gy - r * 0.3);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }

    function animateFreeze(timestamp) {
      if (!animStart) animStart = timestamp;
      var elapsed = timestamp - animStart;
      var rawP = Math.min(1, elapsed / duration);
      var easedP = easeOutQuart(rawP);

      renderFrame(easedP, timestamp);

      if (rawP < 1) {
        requestAnimationFrame(animateFreeze);
      } else {
        isFrozen = true;
        // Keep a subtle ambient sparkle loop
        startSparkleLoop();
      }
    }

    function startSparkleLoop() {
      var lastSparkle = 0;
      function loop(t) {
        if (!isFrozen) return;
        // Only re-render every 60ms to save CPU/battery
        if (t - lastSparkle > 60) {
          lastSparkle = t;
          renderFrame(1, t);
        }
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);
    }

    function triggerFreeze() {
      if (animStart !== null) return;
      companionSection.classList.add("frost-active");
      requestAnimationFrame(animateFreeze);
    }

    // Initialize layout
    resizeFrost();
    window.addEventListener("resize", resizeFrost, { passive: true });

    // Scroll trigger: triggers reliably when user approaches the companion section
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting || entry.intersectionRatio > 0) {
            triggerFreeze();
            observer.disconnect();
          }
        });
      }, { threshold: [0, 0.05, 0.15], rootMargin: "0px 0px 100px 0px" });
      observer.observe(companionSection);
    } else {
      triggerFreeze();
    }

    // Also support manual window scroll fallback
    window.addEventListener("scroll", function onScrollCheck() {
      var rect = companionSection.getBoundingClientRect();
      if (rect.top <= window.innerHeight * 0.88) {
        triggerFreeze();
        window.removeEventListener("scroll", onScrollCheck);
      }
    }, { passive: true });
  }

  // footer year
  var y = document.querySelector(".year");
  if (y) y.textContent = new Date().getFullYear();
});
