/* ============================================================
   The World Plate — a live 3D scene of Qing Mao Mountain and
   Gu Yue Village, drawn from the published chapters.

   Engineered with pure Canvas 2D: high-resolution geological
   heightfield with domain warping, slope-aware rock & biome
   stratification, Lambertian sun diffuse lighting, crevice
   ambient occlusion, drifting volumetric mist ribbons, close-up
   camera zoom, and 3D architectural geometry for Gu Yue Village.
   ============================================================ */
(function () {
  'use strict';

  var GRID = 72;                 // high-resolution terrain grid (73x73 vertices)
  var SPAN = 56;                 // grand world units across
  var REACH = 8.4;               // where the translation currently stops
  var REACH_AT = { 1: 7.4, 2: 7.7, 3: 8.0, 4: 8.4 };   // how far the mists had drawn back
  var FRONTIER = 4;              // chapter the reach stands for

  // ── terrain mathematics & geology ──────────────────────────────────────────
  function hash(x, z) {
    var n = Math.sin(x * 127.1 + z * 311.7) * 43758.5453123;
    return n - Math.floor(n);
  }
  function smooth(t) { return t * t * (3 - 2 * t); }
  function noise(x, z) {
    var xi = Math.floor(x), zi = Math.floor(z);
    var xf = x - xi, zf = z - zi;
    var a = hash(xi, zi), b = hash(xi + 1, zi), c = hash(xi, zi + 1), d = hash(xi + 1, zi + 1);
    var u = smooth(xf), v = smooth(zf);
    return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v;
  }
  function fbm(x, z) {
    var out = 0, amp = 1, freq = 1, norm = 0;
    for (var o = 0; o < 4; o++) {
      out += amp * noise(x * freq, z * freq);
      norm += amp;
      amp *= 0.5;
      freq *= 2.03;
    }
    return out / norm;
  }
  // ridged multifractal noise: produces sharp rocky mountain crags & ridgelines
  function ridged(x, z) {
    var out = 0, amp = 1, freq = 1, norm = 0;
    for (var o = 0; o < 3; o++) {
      var n = 1 - Math.abs(noise(x * freq, z * freq) * 2 - 1);
      out += amp * (n * n);
      norm += amp;
      amp *= 0.52;
      freq *= 2.08;
    }
    return out / norm;
  }
  // domain warping: produces natural tectonic folds and fluid rock strata
  function domainWarp(x, z) {
    var wx = fbm(x * 0.088 + 3.1, z * 0.088 + 1.7) * 2.2;
    var wz = fbm(x * 0.088 + 8.4, z * 0.088 + 5.9) * 2.2;
    return fbm((x + wx) * 0.082 + 11.3, (z + wz) * 0.082 + 7.7);
  }

  var VILLAGE = { x: 0.25, z: 1.35 };

  function heightAt(x, z) {
    // 1. Natural mountain folds with geological domain warping
    var base = domainWarp(x, z) * 2.2;
    var crags = ridged(x * 0.085 + 4.3, z * 0.085 + 2.7) * 2.8;
    var h = 0.35 + base + crags * 0.6;

    // 2. Subtle horizontal geological rock strata steps
    h += Math.sin(h * 4.8) * 0.08;

    // 3. Main Qing Mao Mountain Peak (青茅主峰): towering crest behind the village
    var dq = Math.hypot(x - 5.5, z + 2.8);
    h += 7.8 * Math.exp(-(dq * dq) / 38);
    // Qing Mao descending ridge arm towards village terrace
    var ridgeQ = Math.abs((x - 5.5) * 0.6 + (z + 2.8) * 0.8);
    h += 2.6 * Math.exp(-(dq * dq) / 90 - ridgeQ * 0.35);

    // 4. Bai Clan Mountain / White Bone Peak (白家山 / 白骨峰) to the northwest
    var db = Math.hypot(x + 16.5, z + 12.0);
    h += 7.4 * Math.exp(-(db * db) / 45);
    var ridgeB = Math.abs((x + 16.5) * 0.7 - (z + 12.0) * 0.7);
    h += 2.8 * Math.exp(-(db * db) / 100 - ridgeB * 0.4);

    // 5. Xiong Clan Mountain / Black Bear Peak (熊家山 / 黑熊峰) to the northeast
    var dxiong = Math.hypot(x - 17.0, z + 11.5);
    h += 7.6 * Math.exp(-(dxiong * dxiong) / 50);

    // 6. Southern Border Hundred Thousand Mountains (南疆十万大山): vast concentric mountain ridges
    var ds1 = Math.hypot(x + 5.0, z - 20.0);
    h += 5.8 * Math.exp(-(ds1 * ds1) / 70);

    var ds2 = Math.hypot(x - 19.0, z - 18.0);
    h += 6.2 * Math.exp(-(ds2 * ds2) / 80);

    var ds3 = Math.hypot(x + 21.0, z - 15.0);
    h += 6.0 * Math.exp(-(ds3 * ds3) / 85);

    var ds4 = Math.hypot(x, z + 23.0);
    h += 5.2 * Math.exp(-(ds4 * ds4) / 90);

    // 7. Winding Mountain River Gorges (幽谷清溪) cutting between the three mountain massifs
    var gorge1 = Math.abs(x * 0.55 + z * 0.83 + 2.4);
    if (gorge1 < 4.2 && Math.hypot(x, z) > 5.5) {
      h -= (4.2 - gorge1) * 0.5;
    }

    // 8. Gu Yue Village Shelf: natural mountain terrace where the clan built their settlement
    var dx = (x - VILLAGE.x) / 1.85;
    var dz = (z - VILLAGE.z) / 1.35;
    var shelf = Math.exp(-(dx * dx + dz * dz) / 1.6);
    // Smooth terraced living shelf, gently stepped from height 0.95 at gate to 1.55 at Grand Council Hall
    var terraceH = 0.95 + (z - 0.2) * 0.24;
    h = h * (1 - 0.88 * shelf) + terraceH * (0.88 * shelf);

    return Math.max(0.22, h);
  }

  // ── palette ────────────────────────────────────────────────────────────────
  function readVar(name, fallback) {
    try {
      var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      return v || fallback;
    } catch (e) { return fallback; }
  }
  function palette() {
    var dark = document.documentElement.getAttribute('data-theme') === 'obsidian';
    return {
      dark: dark,
      paper: readVar('--bg', dark ? '#0d0d10' : '#f7f6f2'),
      ink: dark ? '#dcd7cd' : '#17171a',
      deep: dark ? '#07070a' : '#fffdf8',
      red: readVar('--red', '#8f1d1d'),
      gold: '#c9a227'
    };
  }
  function mix(a, b, t) {
    function hex(h) {
      h = h.replace('#', '');
      if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    if (a.charAt(0) !== '#') a = '#17171a';
    if (b.charAt(0) !== '#') b = '#ffffff';
    var A = hex(a), B = hex(b);
    return 'rgb(' + Math.round(A[0] + (B[0] - A[0]) * t) + ','
                  + Math.round(A[1] + (B[1] - A[1]) * t) + ','
                  + Math.round(A[2] + (B[2] - A[2]) * t) + ')';
  }

  // ── camera & projection ───────────────────────────────────────────────────
  var cam = { az: 2.45, pitch: 0.32, dist: 36, f: 900, cx: 0, cy: 0, ty: 1.4, tx: 0.5, tz: 0.5 };
  var target = { dist: 36, ty: 1.4, tx: 0.5, tz: 0.5, az: 2.45, pitch: 0.32 };
  var drag = { on: false, x: 0, y: 0, az0: 0, pitch0: 0, moved: 0 };
  var pitchBase = 0.32;
  var parallax = { x: 0, y: 0, tx: 0, ty: 0 };

  var camEye = { x: 0, y: 0, z: 0 };
  var camF = { x: 0, y: 0, z: 1 };
  var camR = { x: 1, y: 0, z: 0 };
  var camU = { x: 0, y: 1, z: 0 };

  function updateCameraVectors() {
    var cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
    var ca = Math.cos(cam.az), sa = Math.sin(cam.az);

    var ex = (cam.tx || 0) - cam.dist * sa * cp;
    var ez = (cam.tz || 0) - cam.dist * ca * cp;
    var rawEy = (cam.ty || 1.4) + cam.dist * sp;

    // Ground clearance: ensure eye camera never penetrates beneath the mountain terrain
    var groundH = heightAt(ex, ez);
    var ey = Math.max(rawEy, groundH + 0.95);

    camEye.x = ex;
    camEye.y = ey;
    camEye.z = ez;

    var fx = (cam.tx || 0) - ex;
    var fy = (cam.ty || 1.4) - ey;
    var fz = (cam.tz || 0) - ez;
    var flen = Math.hypot(fx, Math.hypot(fy, fz)) || 1.0;
    camF.x = fx / flen;
    camF.y = fy / flen;
    camF.z = fz / flen;

    // Right = normalize(-Fz, 0, Fx)
    var rx = -camF.z, rz = camF.x;
    var rlen = Math.hypot(rx, rz) || 1.0;
    camR.x = rx / rlen;
    camR.y = 0;
    camR.z = rz / rlen;

    // Up = Right x Forward
    camU.x = camR.y * camF.z - camR.z * camF.y;
    camU.y = camR.z * camF.x - camR.x * camF.z;
    camU.z = camR.x * camF.y - camR.y * camF.x;
  }

  function project(x, y, z) {
    var vx = x - camEye.x;
    var vy = y - camEye.y;
    var vz = z - camEye.z;

    var xc = vx * camR.x + vy * camR.y + vz * camR.z;
    var yc = vx * camU.x + vy * camU.y + vz * camU.z;
    var zc = vx * camF.x + vy * camF.y + vz * camF.z;

    if (zc <= 0.25) {
      return { x: -9999, y: -9999, z: -1, f: 0 };
    }

    var f = cam.f / zc;
    return {
      x: cam.cx + xc * f,
      y: cam.cy - yc * f,
      z: zc,
      f: f
    };
  }

  // ── scene engine ──────────────────────────────────────────────────────────
  function World(canvas) {
    this.reach = FRONTIER;
    this.people = [];
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.w = 0; this.h = 0; this.dpr = 1;
    this.heights = new Float32Array((GRID + 1) * (GRID + 1));
    this.shade = new Float32Array((GRID + 1) * (GRID + 1));
    this.slope = new Float32Array((GRID + 1) * (GRID + 1));
    this.ao = new Float32Array((GRID + 1) * (GRID + 1));
    this.build();
  }

  function chapterOf(f) { return f.chapter !== undefined ? f.chapter : (f.c || 1); }

  World.prototype.reachNow = function () {
    if (this.reach >= 4) return 8.4;
    return REACH_AT[this.reach] || 8.4;
  };

  World.prototype.build = function () {
    var step = SPAN / GRID;
    var n = GRID + 1;
    for (var j = 0; j <= GRID; j++) {
      for (var i = 0; i <= GRID; i++) {
        var x = -SPAN / 2 + i * step;
        var z = -SPAN / 2 + j * step;
        var h = heightAt(x, z);
        var idx = j * n + i;
        this.heights[idx] = h;

        // 3D Lambertian normal calculation: sunlight from northwest (-0.52, 0.72, -0.45)
        var hx = heightAt(x + step * 0.5, z) - heightAt(x - step * 0.5, z);
        var hz = heightAt(x, z + step * 0.5) - heightAt(x, z - step * 0.5);
        var len = Math.hypot(hx, step, hz);
        var nx = -hx / len, ny = step / len, nz = -hz / len;
        var sunDot = nx * (-0.48) + ny * 0.76 + nz * (-0.42);

        this.shade[idx] = Math.max(0.12, Math.min(1.0, (sunDot + 0.35) / 1.35));
        this.slope[idx] = ny; // vertical normal: ny > 0.8 is flat plateau, ny < 0.68 is steep cliff

        // Crevice Ambient Occlusion (AO) from local terrain curvature
        var avgSurround = (heightAt(x + step, z) + heightAt(x - step, z) + heightAt(x, z + step) + heightAt(x, z - step)) * 0.25;
        this.ao[idx] = Math.max(0.65, Math.min(1.22, 1.0 + (h - avgSurround) * 1.6));
      }
    }
  };

  World.prototype.resize = function () {
    var r = this.canvas.getBoundingClientRect();
    this.dpr = Math.min(2, window.devicePixelRatio || 1);
    this.w = Math.max(320, Math.round(r.width));
    this.h = Math.max(240, Math.round(r.height));
    this.canvas.width = Math.round(this.w * this.dpr);
    this.canvas.height = Math.round(this.h * this.dpr);
    cam.cx = this.w * 0.5;
    cam.cy = this.h * 0.54;
    cam.f = this.w * 1.0;
  };

  World.prototype.draw = function (pal, clock) {
    var ctx = this.ctx, i, j;
    ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    ctx.clearRect(0, 0, this.w, this.h);

    // Refresh 3D LookAt camera vectors and ground clearance for the current frame
    updateCameraVectors();

    // 1. Sky & horizon atmosphere
    var sky = ctx.createLinearGradient(0, 0, 0, this.h);
    sky.addColorStop(0, pal.dark ? mix(pal.paper, '#000000', 0.45) : mix(pal.paper, '#ffffff', 0.5));
    sky.addColorStop(0.55, pal.paper);
    sky.addColorStop(1, pal.dark ? mix(pal.paper, '#000000', 0.25) : mix(pal.paper, '#ffffff', 0.85));
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, this.w, this.h);

    // 2. The morning sun illuminating Qing Mao Mountain
    var sun = project(-24, 11, -8);
    if (sun.z > 1) {
      var sr = Math.max(32, sun.f * 1.35);
      var g = ctx.createRadialGradient(sun.x, sun.y, 0, sun.x, sun.y, sr);
      g.addColorStop(0, pal.dark ? 'rgba(201,162,39,0.32)' : 'rgba(201,162,39,0.24)');
      g.addColorStop(1, 'rgba(201,162,39,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(sun.x, sun.y, sr, 0, 6.2832); ctx.fill();
    }

    // 3. Distant mountain mist layers & earth foundation
    for (var band = 0; band < 3; band++) {
      var by = this.h * (0.30 + band * 0.075);
      var bh = this.h * (0.055 + band * 0.02);
      var bg2 = ctx.createLinearGradient(0, by - bh, 0, by + bh);
      bg2.addColorStop(0, 'rgba(0,0,0,0)');
      bg2.addColorStop(0.5, pal.dark ? 'rgba(255,255,255,0.045)' : 'rgba(255,255,255,0.55)');
      bg2.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = bg2;
      ctx.fillRect(0, by - bh, this.w, bh * 2);
    }

    var earthBaseGrad = ctx.createLinearGradient(0, this.h * 0.45, 0, this.h);
    earthBaseGrad.addColorStop(0, 'rgba(0,0,0,0)');
    earthBaseGrad.addColorStop(0.4, pal.dark ? 'rgba(34, 25, 18, 0.40)' : 'rgba(115, 98, 78, 0.35)');
    earthBaseGrad.addColorStop(1, pal.dark ? 'rgba(20, 15, 11, 0.85)' : 'rgba(88, 74, 58, 0.75)');
    ctx.fillStyle = earthBaseGrad;
    ctx.fillRect(0, this.h * 0.45, this.w, this.h * 0.55);

    // 4. Solid, photorealistic terrain with slope-aware biome stratification & back-to-front depth sorting
    var n = GRID + 1, step = SPAN / GRID;
    var reach = this.reachNow();

    var pts = new Float32Array(n * n * 4);
    var off = new Float32Array(n * n);
    for (j = 0; j <= GRID; j++) {
      for (i = 0; i <= GRID; i++) {
        var k = j * n + i;
        var x = -SPAN / 2 + i * step, z = -SPAN / 2 + j * step;
        var p = project(x, this.heights[k], z);
        pts[k * 4] = p.x; pts[k * 4 + 1] = p.y; pts[k * 4 + 2] = p.z; pts[k * 4 + 3] = p.f;
        off[k] = Math.hypot(x - VILLAGE.x, z - VILLAGE.z);
      }
    }

    // Collect all valid quads in front of near plane
    var quads = [];
    for (j = 0; j < GRID; j++) {
      for (i = 0; i < GRID; i++) {
        var k0 = j * n + i, k1 = k0 + 1, k2 = k0 + n, k3 = k2 + 1;
        var z0 = pts[k0 * 4 + 2], z1 = pts[k1 * 4 + 2], z2 = pts[k2 * 4 + 2], z3 = pts[k3 * 4 + 2];
        if (z0 <= 0.25 || z1 <= 0.25 || z2 <= 0.25 || z3 <= 0.25) continue;
        var depth = (z0 + z1 + z2 + z3) * 0.25;
        if (depth > cam.dist * 3.5 + 50) continue;
        quads.push({ i: i, j: j, k0: k0, k1: k1, k2: k2, k3: k3, depth: depth });
      }
    }

    // Strict back-to-front depth sorting (Painter's algorithm)
    quads.sort(function (a, b) { return b.depth - a.depth; });

    var ink = pal.ink, paper = pal.paper;
    for (var qIdx = 0; qIdx < quads.length; qIdx++) {
      var q = quads[qIdx];
      i = q.i; j = q.j;
      var k0 = q.k0, k1 = q.k1, k2 = q.k2, k3 = q.k3;
      var depth = q.depth;

      var hgt = (this.heights[k0] + this.heights[k1] + this.heights[k2] + this.heights[k3]) / 4;
      var light = this.shade[k0];
      var ny = this.slope[k0];
      var ao = this.ao[k0];

      // Slope-Aware Biome Color Palette with 3D Sun Lighting & Ambient Occlusion
      var col;
      var soilVar = hash(i * 4.7 + 1.2, j * 5.3 + 2.8); // 0.0 to 1.0 soil organic variation
      var distV = off[k0];
      var nBorder = noise(x * 0.85, z * 0.85) * 0.8;
      // Smooth organic soil blending around village settlement and agricultural terraces
      var soilWeight = Math.max(0, Math.min(1, 1 - (distV - 1.8 + nBorder) / 2.4));
      var isVillage = soilWeight > 0.35;

      if (pal.dark) {
        // Obsidian Mode:
        var earthDark = '#342215';
        var earthWarm = '#5c402d';
        var villageSoil = mix(earthDark, earthWarm, soilVar * 0.45 + light * 0.55);
        if (ny > 0.80) villageSoil = mix(villageSoil, '#2d1e13', 0.20);

        var forestUnder = '#1e281c';
        var greenSlope = '#2a542e';
        var bambooGreen = mix(mix(forestUnder, greenSlope, light * ao), '#3d6e42', ny > 0.78 ? 0.45 : 0.15);

        var cliffDark = '#242b36';
        var cliffLight = '#48556b';
        var rockCol = mix(cliffDark, cliffLight, light * ao);

        var snowCol = mix('#444d5c', '#e2eaf5', Math.min(1, (hgt - 6.4) / 1.4) * light * ao);
        var cragCol = mix('#282f3c', '#545f73', ((hgt - 4.2) / 2.2 * 0.7 + light * 0.3) * ao);

        if (ny < 0.62) {
          col = rockCol;
        } else if (hgt > 6.4) {
          col = snowCol;
        } else if (hgt > 4.2) {
          col = cragCol;
        } else if (hgt > 1.35) {
          col = mix(bambooGreen, villageSoil, soilWeight);
        } else {
          var valleySoil = '#221c16';
          col = mix(mix(forestUnder, valleySoil, 0.5), villageSoil, soilWeight * 0.8 + 0.2);
        }
      } else {
        // Light Mode (Classical Chinese Shanshui Verdant Landscape):
        var earthDarkL = '#785e44';
        var earthWarmL = '#b59a7a';
        var villageSoilL = mix(earthDarkL, earthWarmL, soilVar * 0.35 + light * 0.65);
        if (ny > 0.80) villageSoilL = mix(villageSoilL, '#664d36', 0.20);

        var forestUnderL = '#5c6650';
        var greenSlopeL = '#4d7a52';
        var bambooGreenL = mix(mix(forestUnderL, greenSlopeL, light * ao), '#76a87c', ny > 0.78 ? 0.45 : 0.15);

        var rockColL = mix('#5a5347', '#91897b', light * ao);
        var snowColL = mix('#ded7cc', '#ffffff', Math.min(1, (hgt - 6.4) / 1.4) * light * ao);
        var cragColL = mix('#686256', '#bfb6a6', light * ao);

        if (ny < 0.62) {
          col = rockColL;
        } else if (hgt > 6.4) {
          col = snowColL;
        } else if (hgt > 4.2) {
          col = cragColL;
        } else if (hgt > 1.35) {
          col = mix(bambooGreenL, villageSoilL, soilWeight);
        } else {
          var valleySoilL = '#56645e';
          col = mix(mix(forestUnderL, valleySoilL, 0.5), villageSoilL, soilWeight * 0.8 + 0.2);
        }
      }

      // Natural aerial perspective: distant mountains soften into horizon atmosphere
      var horizonFog = Math.max(0, Math.min(0.85, (off[k0] - 22.0) / 14.0));
      var frontierFog = 0;
      if (this.reach < 4) {
        var fLim = 14.0 + this.reach * 4.0;
        if (off[k0] > fLim) frontierFog = Math.min(0.65, (off[k0] - fLim) / 8.0);
      }
      var totalFog = Math.max(horizonFog, frontierFog);
      var mist = 1 - totalFog;
      col = mix(col, paper, 1 - mist * mist);

      var alpha = 0.98 * (1 - totalFog * 0.80);
      ctx.globalAlpha = alpha < 0.08 ? 0.08 : alpha;
      ctx.fillStyle = col;
      ctx.strokeStyle = col;
      ctx.lineWidth = 1.3;
      ctx.beginPath();
      ctx.moveTo(pts[k0 * 4], pts[k0 * 4 + 1]);
      ctx.lineTo(pts[k1 * 4], pts[k1 * 4 + 1]);
      ctx.lineTo(pts[k3 * 4], pts[k3 * 4 + 1]);
      ctx.lineTo(pts[k2 * 4], pts[k2 * 4 + 1]);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

        var cx = (pts[k0 * 4] + pts[k3 * 4]) / 2;
        var cy = (pts[k0 * 4 + 1] + pts[k3 * 4 + 1]) / 2;
        var sc = Math.max(1.4, pts[k0 * 4 + 3] * 0.065);

        // 1. Village soil details: scattered earth pebbles and soil stones
        if (isVillage && soilVar > 0.78 && totalFog < 0.35) {
          ctx.globalAlpha = alpha * 0.55;
          ctx.fillStyle = pal.dark ? '#1c140d' : '#524332';
          ctx.beginPath();
          ctx.arc(cx, cy, sc * 0.28, 0, 6.28);
          ctx.fill();
        }

        // 2. Spear Bamboo & Mountain Pine Clusters on green slopes
        if (hgt > 1.35 && hgt < 4.8 && ny >= 0.72 && totalFog < 0.55 && !isVillage) {
          var seed = hash(i * 3.1 + 0.7, j * 2.7 + 1.3);
          if (seed > 0.82) {
            ctx.globalAlpha = alpha * 0.80;
            // dark timber trunk
            ctx.fillStyle = pal.dark ? '#0c120c' : '#222b20';
            ctx.fillRect(cx - sc * 0.18, cy - sc * 0.55, sc * 0.36, sc * 0.55);
            // tiered pine evergreen canopy
            ctx.fillStyle = pal.dark ? '#122416' : '#324734';
            ctx.beginPath();
            ctx.moveTo(cx, cy - sc * 3.0);
            ctx.lineTo(cx - sc * 0.85, cy - sc * 1.6);
            ctx.lineTo(cx + sc * 0.85, cy - sc * 1.6);
            ctx.closePath(); ctx.fill();

            ctx.beginPath();
            ctx.moveTo(cx, cy - sc * 1.9);
            ctx.lineTo(cx - sc * 1.15, cy - sc * 0.45);
            ctx.lineTo(cx + sc * 1.15, cy - sc * 0.45);
            ctx.closePath(); ctx.fill();
          } else if (seed > 0.70 && seed <= 0.82) {
            // Spear Bamboo cluster (青茅竹林丛) - slender bamboo stalks with blade leaves
            ctx.globalAlpha = alpha * 0.75;
            ctx.strokeStyle = pal.dark ? '#274b2a' : '#4f8052';
            ctx.lineWidth = Math.max(1, sc * 0.18);
            ctx.beginPath();
            ctx.moveTo(cx - sc * 0.3, cy); ctx.lineTo(cx - sc * 0.3, cy - sc * 2.2);
            ctx.moveTo(cx + sc * 0.2, cy); ctx.lineTo(cx + sc * 0.2, cy - sc * 2.5);
            ctx.stroke();
            // Bamboo blade foliage
            ctx.fillStyle = pal.dark ? '#336137' : '#609964';
            ctx.beginPath();
            ctx.ellipse(cx - sc * 0.3, cy - sc * 2.2, sc * 0.55, sc * 0.22, -0.4, 0, 6.28);
            ctx.ellipse(cx + sc * 0.2, cy - sc * 2.5, sc * 0.6, sc * 0.24, 0.35, 0, 6.28);
            ctx.fill();
          }
        }
      }
    ctx.globalAlpha = 1;

    // 5. Volumetric Sea of Clouds & mountain mist ribbons
    this.drawSeaOfClouds(pal, clock || 0);
    this.drawMistRibbons(pal, clock || 0);

    // 6. Tangible 3D Village Architecture & Landmarks
    this.drawVillageRoads(pal);
    this.drawVillageBuildings(pal, clock || 0);
    this.drawSubterraneanCavern(pal, clock || 0);

    // 7. Cultivators standing in the world
    this.drawPeople(pal, clock || 0);

    // 8. Translation frontier & atmosphere
    this.drawFrontier(pal);
    this.drawAir(pal, clock || 0);
  };

  // ── Volumetric Sea of Clouds (云海) in the deep gorges ───────────────
  World.prototype.drawSeaOfClouds = function (pal, clock) {
    var ctx = this.ctx;
    var t = (clock || 0) * 0.00035;
    var cloudBands = [
      { y: 0.70, r: 24, alpha: pal.dark ? 0.28 : 0.60, count: 8 },
      { y: 1.10, r: 18, alpha: pal.dark ? 0.22 : 0.48, count: 7 },
      { y: 1.55, r: 13, alpha: pal.dark ? 0.16 : 0.35, count: 6 }
    ];
    ctx.save();
    for (var bi = 0; bi < cloudBands.length; bi++) {
      var band = cloudBands[bi];
      for (var ci = 0; ci < band.count; ci++) {
        var angle = ci * (Math.PI * 2 / band.count) + t * (0.6 + bi * 0.25);
        var dist = band.r * (0.55 + 0.45 * Math.sin(ci * 1.6 + t * 0.8));
        var cx = Math.cos(angle) * dist;
        var cz = Math.sin(angle) * dist;
        // Don't obscure village core at higher cloud elevations
        if (Math.hypot(cx - VILLAGE.x, cz - VILLAGE.z) < 3.2 && band.y > 0.85) continue;
        var cp = project(cx, band.y, cz);
        if (cp.z > 0.3 && cp.x > -120 && cp.x < this.w + 120 && cp.y > -100 && cp.y < this.h + 100) {
          var cr = Math.max(30, cp.f * (1.9 + bi * 0.4));
          var cg = ctx.createRadialGradient(cp.x, cp.y, 0, cp.x, cp.y, cr);
          if (pal.dark) {
            cg.addColorStop(0, 'rgba(42, 48, 62, ' + band.alpha + ')');
            cg.addColorStop(0.5, 'rgba(28, 32, 42, ' + (band.alpha * 0.6) + ')');
            cg.addColorStop(1, 'rgba(20, 22, 28, 0)');
          } else {
            cg.addColorStop(0, 'rgba(255, 255, 255, ' + band.alpha + ')');
            cg.addColorStop(0.55, 'rgba(244, 240, 232, ' + (band.alpha * 0.65) + ')');
            cg.addColorStop(1, 'rgba(240, 235, 225, 0)');
          }
          ctx.fillStyle = cg;
          ctx.beginPath();
          ctx.arc(cp.x, cp.y, cr, 0, 6.2832);
          ctx.fill();
        }
      }
    }
    ctx.restore();
  };

  // ── Volumetric Mist Ribbons (云雾缭绕) ────────────────────────────────────
  World.prototype.drawMistRibbons = function (pal, clock) {
    var ctx = this.ctx, m;
    var t = (clock || 0) * 0.00018;
    var belts = [
      { y: 1.15, r: 12.0, speed: 0.8, alpha: 0.18 },
      { y: 2.25, r: 18.0, speed: -0.6, alpha: 0.14 },
      { y: 3.45, r: 24.5, speed: 0.4, alpha: 0.12 }
    ];
    for (m = 0; m < belts.length; m++) {
      var b = belts[m];
      ctx.save();
      ctx.beginPath();
      var first = true;
      for (var s = 0; s <= 28; s++) {
        var angle = (s / 28) * Math.PI * 1.6 + t * b.speed;
        var mx = Math.cos(angle) * b.r + Math.sin(angle * 2.5) * 1.2;
        var mz = Math.sin(angle) * b.r * 0.75 + Math.cos(angle * 1.8) * 1.0;
        var my = b.y + Math.sin(angle * 3.0 + t) * 0.25;
        var mp = project(mx, my, mz);
        if (mp.z > 1) {
          if (first) { ctx.moveTo(mp.x, mp.y); first = false; }
          else { ctx.lineTo(mp.x, mp.y); }
        }
      }
      var mg = ctx.createLinearGradient(0, this.h * 0.2, 0, this.h * 0.8);
      mg.addColorStop(0, pal.dark ? 'rgba(210, 220, 235, ' + b.alpha + ')' : 'rgba(255, 255, 255, ' + (b.alpha * 2.2) + ')');
      mg.addColorStop(1, 'rgba(255, 255, 255, 0)');
      ctx.strokeStyle = mg;
      ctx.lineWidth = Math.max(14, 130 / (cam.dist * 0.45));
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.stroke();
      ctx.restore();
    }
  };

  // ── Paved Flagstone Village Roads & Terraced Steps (青石古道与石阶) ───────
  World.prototype.drawVillageRoads = function (pal) {
    var ctx = this.ctx, i;
    var roads = [
      // 1. Village Main Avenue: Mountain Gate -> Central Square -> Grand Council Hall
      [
        [0.20, 0.15],
        [0.18, 0.45],
        [0.12, 0.85],
        [0.05, 1.25],
        [-0.08, 1.65],
        [-0.22, 1.95],
        [-0.35, 2.22]
      ],
      // 2. East Faction Lane: to Mo Manor & tavern
      [
        [0.12, 0.85],
        [0.45, 1.10],
        [0.85, 1.35],
        [1.25, 1.60],
        [1.50, 1.80]
      ],
      // 3. West Faction Lane: to Chi Manor
      [
        [-0.08, 1.65],
        [-0.45, 1.68],
        [-0.90, 1.72],
        [-1.30, 1.75]
      ],
      // 4. Fang Family Terrace Path: secluded lane to Fang stilt house
      [
        [0.45, 1.10],
        [0.68, 0.95]
      ],
      // 5. Academy Approach: connecting main street to martial courtyard
      [
        [-0.08, 1.65],
        [-0.15, 1.65]
      ]
    ];

    ctx.save();
    for (var r = 0; r < roads.length; r++) {
      var pts = roads[r];
      var proj = [];
      for (i = 0; i < pts.length; i++) {
        var rx = pts[i][0], rz = pts[i][1];
        var ry = heightAt(rx, rz) + 0.015;
        var p = project(rx, ry, rz);
        if (p.z > 0.25) proj.push(p);
      }
      if (proj.length >= 2) {
        // Road base: compacted earth and crushed gravel shoulder
        ctx.beginPath();
        ctx.moveTo(proj[0].x, proj[0].y);
        for (i = 1; i < proj.length; i++) {
          ctx.lineTo(proj[i].x, proj[i].y);
        }
        ctx.lineWidth = Math.max(3.8, proj[0].f * 0.056);
        ctx.strokeStyle = pal.dark ? '#221912' : '#6b5844';
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.stroke();

        // Flagstone center surface (青石板路面)
        ctx.lineWidth = Math.max(2.2, proj[0].f * 0.038);
        ctx.strokeStyle = pal.dark ? '#3a332a' : '#a39786';
        ctx.stroke();

        // Transverse flagstone slab joints (横向石板接缝与石阶纹路)
        for (i = 0; i < proj.length - 1; i++) {
          var p0 = proj[i], p1 = proj[i + 1];
          var mx = (p0.x + p1.x) * 0.5, my = (p0.y + p1.y) * 0.5;
          var dx = p1.x - p0.x, dy = p1.y - p0.y;
          var len = Math.hypot(dx, dy);
          if (len > 0.1) {
            var nx = -dy / len, ny = dx / len;
            var w = Math.max(2.4, p0.f * 0.026);
            ctx.beginPath();
            ctx.moveTo(mx - nx * w, my - ny * w);
            ctx.lineTo(mx + nx * w, my + ny * w);
            ctx.lineWidth = 0.95;
            ctx.strokeStyle = pal.dark ? '#16120e' : '#544636';
            ctx.stroke();
          }
        }
      }
    }
    ctx.restore();
  };

  // ── 3D village architecture: tangible pavilions, gates, manors & cottages ──
  var VILLAGE_STRUCTURES = [
    // 1. Grand Clan Council Hall (古月族长议事大厅) - 2-tier Pagoda Pavilion
    { id: 'hall', x: -0.35, z: 2.30, w: 1.45, d: 1.15, h: 1.05, type: 'pagoda2' },
    // 2. Clan Academy & Martial Grounds (古月学堂与演武场)
    { id: 'academy', x: -0.15, z: 1.65, w: 1.25, d: 0.90, h: 0.58, type: 'courtyard' },
    // 3. Mo Faction Compound (莫家府邸)
    { id: 'mo-manor', x: 1.55, z: 1.85, w: 1.15, d: 0.95, h: 0.65, type: 'manor' },
    // 4. Chi Faction Compound (赤家府邸)
    { id: 'chi-manor', x: -1.35, z: 1.75, w: 1.15, d: 0.95, h: 0.65, type: 'manor' },
    // 5. Fang Family Stilt Residence (方家旧居)
    { id: 'fang-residence', x: 0.70, z: 0.95, w: 0.80, d: 0.65, h: 0.62, type: 'stilt' },
    // 6. Gu Yue Fortified Mountain Gate (古月寨门)
    { id: 'gate', x: 0.20, z: 0.15, w: 0.95, d: 0.45, h: 0.82, type: 'gate' },
    // 7. North Lookout Watchtower (北哨楼)
    { id: 'north-tower', x: 1.85, z: 0.60, w: 0.45, d: 0.45, h: 1.18, type: 'tower' },
    // 8. South Gorge Watchtower (南哨楼)
    { id: 'south-tower', x: -0.85, z: 0.65, w: 0.45, d: 0.45, h: 1.12, type: 'tower' },
    // 9-16. Terraced Village Cottages & Clan Workshops
    { id: 'h1', x: 0.45, z: 1.35, w: 0.65, d: 0.52, h: 0.50, type: 'house' }, // Herbalist apothecary
    { id: 'h2', x: 1.10, z: 1.35, w: 0.70, d: 0.54, h: 0.52, type: 'house' }, // Wine tavern
    { id: 'h3', x: 0.10, z: 1.95, w: 0.62, d: 0.50, h: 0.48, type: 'house' }, // Elder residence
    { id: 'h4', x: -0.75, z: 1.30, w: 0.64, d: 0.52, h: 0.50, type: 'house' }, // Terrace home
    { id: 'h5', x: 0.95, z: 1.65, w: 0.66, d: 0.52, h: 0.50, type: 'house' }, // Gu master lodge
    { id: 'h6', x: -0.65, z: 2.05, w: 0.68, d: 0.55, h: 0.52, type: 'house' }, // Upper terrace home
    { id: 'h7', x: 1.15, z: 2.15, w: 0.64, d: 0.50, h: 0.50, type: 'house' }, // Clan archive
    { id: 'h8', x: -0.10, z: 1.05, w: 0.62, d: 0.50, h: 0.48, type: 'house' }  // Lower lane cottage
  ];

  World.prototype.drawVillageBuildings = function (pal, clock) {
    var ctx = this.ctx, i;
    var list = [];
    for (i = 0; i < VILLAGE_STRUCTURES.length; i++) {
      var s = VILLAGE_STRUCTURES[i];
      var y = heightAt(s.x, s.z);
      var p = project(s.x, y, s.z);
      if (p.z > 0.3) {
        list.push({ s: s, y: y, p: p });
      }
    }
    // Depth sort: back to front painter's algorithm
    list.sort(function (a, b) { return b.p.z - a.p.z; });

    var windSway = Math.sin((clock || 0) * 0.003) * 0.08;

    for (i = 0; i < list.length; i++) {
      var bldg = list[i].s, by = list[i].y, bp = list[i].p;
      var f = bp.f;
      var w = Math.max(8, bldg.w * f * 0.10);
      var h = Math.max(10, bldg.h * f * 0.12);
      var bx = bp.x, bbase = bp.y;

      ctx.save();

      if (bldg.type === 'pagoda2') {
        // ── Grand Clan Council Hall (古月族长议事大厅 - 2-tier Pagoda) ──
        // 1. Carved Stone Foundation Platform (白石台基)
        ctx.fillStyle = pal.dark ? '#22232a' : '#544f47';
        ctx.fillRect(bx - w * 0.68, bbase - h * 0.22, w * 1.36, h * 0.22);
        ctx.fillStyle = pal.dark ? '#2e303a' : '#736d62';
        ctx.fillRect(bx - w * 0.60, bbase - h * 0.22, w * 1.20, h * 0.06);

        // Center Stone Steps (殿前汉白玉石阶)
        ctx.fillStyle = pal.dark ? '#3a3c48' : '#8e8677';
        for (var stepI = 0; stepI < 3; stepI++) {
          var stepY = bbase - h * (0.07 * (stepI + 1));
          var stepW = w * (0.34 - stepI * 0.04);
          ctx.fillRect(bx - stepW * 0.5, stepY, stepW, h * 0.06);
        }

        // 2. Lower Pavilion Timber Pillars & Crimson Walls (朱红殿壁与立柱)
        ctx.fillStyle = pal.dark ? '#1a191f' : '#332e27';
        ctx.fillRect(bx - w * 0.50, bbase - h * 0.62, w * 1.0, h * 0.40);
        // Timber structural pillars
        ctx.fillStyle = pal.dark ? '#2a1a18' : '#6b201a';
        ctx.fillRect(bx - w * 0.48, bbase - h * 0.62, w * 0.06, h * 0.40);
        ctx.fillRect(bx + w * 0.42, bbase - h * 0.62, w * 0.06, h * 0.40);
        ctx.fillRect(bx - w * 0.18, bbase - h * 0.62, w * 0.05, h * 0.40);
        ctx.fillRect(bx + w * 0.13, bbase - h * 0.62, w * 0.05, h * 0.40);

        // Grand entrance double doors (中央红木殿门)
        ctx.fillStyle = pal.dark ? '#3d1614' : '#82241d';
        ctx.fillRect(bx - w * 0.12, bbase - h * 0.52, w * 0.24, h * 0.30);
        // Gold door studs & knockers
        ctx.fillStyle = pal.gold;
        ctx.fillRect(bx - w * 0.07, bbase - h * 0.40, w * 0.025, w * 0.025);
        ctx.fillRect(bx + w * 0.045, bbase - h * 0.40, w * 0.025, w * 0.025);

        // Glowing council lattice windows (雕花窗棂与暖光)
        ctx.fillStyle = 'rgba(235, 175, 55, 0.88)';
        ctx.fillRect(bx - w * 0.38, bbase - h * 0.54, w * 0.16, h * 0.24);
        ctx.fillRect(bx + w * 0.22, bbase - h * 0.54, w * 0.16, h * 0.24);

        // 3. Lower Tier Dougong Brackets (斗栱)
        ctx.fillStyle = pal.dark ? '#2f2c38' : '#574e42';
        for (var dg = -4; dg <= 4; dg++) {
          ctx.fillRect(bx + dg * (w * 0.11) - w * 0.03, bbase - h * 0.66, w * 0.06, h * 0.05);
        }

        // Lower Tier Flared Eaves with upturned corner wings (飞檐翼角)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.78, bbase - h * 0.64);
        ctx.quadraticCurveTo(bx - w * 0.4, bbase - h * 0.76, bx, bbase - h * 0.80);
        ctx.quadraticCurveTo(bx + w * 0.4, bbase - h * 0.76, bx + w * 0.78, bbase - h * 0.64);
        ctx.lineTo(bx + w * 0.60, bbase - h * 0.60);
        ctx.lineTo(bx - w * 0.60, bbase - h * 0.60);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3b3a45' : '#453f36';
        ctx.fill();

        // 4. Upper Tier Pavilion & Clan Inscription Plaque (二层阁楼与古月匾额)
        ctx.fillStyle = pal.dark ? '#26252e' : '#3d3730';
        ctx.fillRect(bx - w * 0.34, bbase - h * 1.05, w * 0.68, h * 0.28);
        // Clan Plaque: "古月"
        ctx.fillStyle = pal.red;
        ctx.fillRect(bx - w * 0.14, bbase - h * 1.02, w * 0.28, h * 0.09);
        ctx.fillStyle = pal.gold;
        ctx.fillRect(bx - w * 0.12, bbase - h * 1.00, w * 0.24, h * 0.05);

        // Upper Pavilion Windows
        ctx.fillStyle = 'rgba(235, 175, 55, 0.92)';
        ctx.fillRect(bx - w * 0.10, bbase - h * 0.90, w * 0.20, h * 0.14);

        // 5. Grand Upper Roof with Upturned Flared Corners (重檐歇山顶)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.64, bbase - h * 1.08);
        ctx.quadraticCurveTo(bx - w * 0.30, bbase - h * 1.28, bx, bbase - h * 1.34);
        ctx.quadraticCurveTo(bx + w * 0.30, bbase - h * 1.28, bx + w * 0.64, bbase - h * 1.08);
        ctx.lineTo(bx + w * 0.46, bbase - h * 1.04);
        ctx.lineTo(bx - w * 0.46, bbase - h * 1.04);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#4c4a57' : '#524b40';
        ctx.fill();

        // Animal ridge ornaments (吻兽) at roof ends
        ctx.fillStyle = pal.gold;
        ctx.fillRect(bx - w * 0.62, bbase - h * 1.12, w * 0.04, h * 0.06);
        ctx.fillRect(bx + w * 0.58, bbase - h * 1.12, w * 0.04, h * 0.06);

        // 6. Gu Yue Clan Golden Crescent Moon Finial (月牙顶针)
        ctx.strokeStyle = pal.gold;
        ctx.lineWidth = Math.max(1.8, f * 0.018);
        ctx.beginPath();
        ctx.arc(bx, bbase - h * 1.48, Math.max(3.2, w * 0.13), Math.PI * 0.2, Math.PI * 1.3);
        ctx.stroke();

        // 7. Swaying Red & Gold Clan Lanterns (随风轻摇的迎风灯笼)
        var lanternSway = Math.sin((clock || 0) * 0.0035) * (w * 0.04);
        var lx1 = bx - w * 0.54 + lanternSway, ly1 = bbase - h * 0.58;
        var lx2 = bx + w * 0.54 + lanternSway, ly2 = bbase - h * 0.58;

        // Lantern string & tassel
        ctx.strokeStyle = pal.dark ? '#802020' : '#a02820';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.54, bbase - h * 0.62); ctx.lineTo(lx1, ly1);
        ctx.moveTo(bx + w * 0.54, bbase - h * 0.62); ctx.lineTo(lx2, ly2);
        ctx.stroke();

        // Lantern glows
        var lg1 = ctx.createRadialGradient(lx1, ly1, 0, lx1, ly1, w * 0.6);
        lg1.addColorStop(0, 'rgba(235, 175, 55, 0.75)');
        lg1.addColorStop(0.4, 'rgba(215, 65, 45, 0.45)');
        lg1.addColorStop(1, 'rgba(235, 175, 55, 0)');
        ctx.fillStyle = lg1;
        ctx.beginPath(); ctx.arc(lx1, ly1, w * 0.6, 0, 6.2832); ctx.fill();

        var lg2 = ctx.createRadialGradient(lx2, ly2, 0, lx2, ly2, w * 0.6);
        lg2.addColorStop(0, 'rgba(235, 175, 55, 0.75)');
        lg2.addColorStop(0.4, 'rgba(215, 65, 45, 0.45)');
        lg2.addColorStop(1, 'rgba(235, 175, 55, 0)');
        ctx.fillStyle = lg2;
        ctx.beginPath(); ctx.arc(lx2, ly2, w * 0.6, 0, 6.2832); ctx.fill();

      } else if (bldg.type === 'courtyard') {
        // ── Clan Academy & Martial Grounds (古月学堂与演武场) ──
        // Perimeter enclosure wall
        ctx.fillStyle = pal.dark ? '#23232b' : '#6b6459';
        ctx.fillRect(bx - w * 0.62, bbase - h * 0.26, w * 1.24, h * 0.26);
        // Courtyard flagstone training ground
        ctx.fillStyle = pal.dark ? '#1c1c24' : '#8c8477';
        ctx.fillRect(bx - w * 0.56, bbase - h * 0.22, w * 1.12, h * 0.22);

        // Martial Arts Practice Circle (演武太极圈)
        ctx.strokeStyle = pal.dark ? '#383644' : '#a89f90';
        ctx.lineWidth = Math.max(1, f * 0.01);
        ctx.beginPath();
        ctx.arc(bx, bbase - h * 0.11, Math.max(4, w * 0.22), 0, 6.2832);
        ctx.stroke();

        // Weapon Racks on the perimeter (兵器架)
        ctx.fillStyle = pal.dark ? '#141418' : '#3a332a';
        ctx.fillRect(bx - w * 0.48, bbase - h * 0.28, w * 0.12, h * 0.14);
        ctx.fillRect(bx + w * 0.36, bbase - h * 0.28, w * 0.12, h * 0.14);

        // Main Lecture Pavilion (讲经堂)
        ctx.fillStyle = pal.dark ? '#2b2a33' : '#453f36';
        ctx.fillRect(bx - w * 0.40, bbase - h * 0.74, w * 0.80, h * 0.52);
        // Tiled Roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.58, bbase - h * 0.74);
        ctx.lineTo(bx, bbase - h * 1.05);
        ctx.lineTo(bx + w * 0.58, bbase - h * 0.74);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3d3c47' : '#574f43';
        ctx.fill();
        // Academy entrance lantern
        ctx.fillStyle = pal.gold;
        ctx.beginPath(); ctx.arc(bx, bbase - h * 0.54, Math.max(1.8, w * 0.05), 0, 6.2832); ctx.fill();

      } else if (bldg.type === 'manor') {
        // ── Clan Faction Manors (Mo & Chi Compounds 徽派世家府邸) ──
        // High Stepped Horse-Head Fire Wall (徽派马头墙)
        ctx.fillStyle = pal.dark ? '#24242c' : '#5e574d';
        ctx.fillRect(bx - w * 0.56, bbase - h * 0.36, w * 1.12, h * 0.36);
        // Stepped gables at side rims
        ctx.fillStyle = pal.dark ? '#353340' : '#453e35';
        ctx.fillRect(bx - w * 0.56, bbase - h * 0.50, w * 0.12, h * 0.14);
        ctx.fillRect(bx + w * 0.44, bbase - h * 0.50, w * 0.12, h * 0.14);

        // Manor Central Residence
        ctx.fillStyle = pal.dark ? '#1e1d24' : '#423d35';
        ctx.fillRect(bx - w * 0.38, bbase - h * 0.82, w * 0.76, h * 0.50);

        // Heavy Courtyard Gate with black timber & red trim (重木黑漆大门)
        ctx.fillStyle = pal.dark ? '#111114' : '#26221c';
        ctx.fillRect(bx - w * 0.14, bbase - h * 0.42, w * 0.28, h * 0.42);
        ctx.fillStyle = pal.red;
        ctx.fillRect(bx - w * 0.16, bbase - h * 0.44, w * 0.32, h * 0.04);

        // Dual-gabled Manor Roof (重檐黑瓦)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.54, bbase - h * 0.82);
        ctx.quadraticCurveTo(bx - w * 0.25, bbase - h * 1.00, bx, bbase - h * 1.10);
        ctx.quadraticCurveTo(bx + w * 0.25, bbase - h * 1.00, bx + w * 0.54, bbase - h * 0.82);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3a3945' : '#524b41';
        ctx.fill();

        // Warm amber window
        ctx.fillStyle = 'rgba(235, 175, 55, 0.82)';
        ctx.fillRect(bx - w * 0.16, bbase - h * 0.65, w * 0.32, h * 0.22);

      } else if (bldg.type === 'stilt') {
        // ── Fang Family Stilt Residence (方家旧居吊脚楼) ──
        // Elevated timber stilts resting on bedrock (穿斗式木柱)
        ctx.fillStyle = pal.dark ? '#1f1e24' : '#4a3f32';
        ctx.fillRect(bx - w * 0.36, bbase - h * 0.35, w * 0.08, h * 0.35);
        ctx.fillRect(bx + w * 0.28, bbase - h * 0.35, w * 0.08, h * 0.35);
        ctx.fillRect(bx - w * 0.04, bbase - h * 0.35, w * 0.08, h * 0.35);

        // Raised timber deck & veranda railing (临崖木栏杆)
        ctx.fillStyle = pal.dark ? '#2b2933' : '#5e5040';
        ctx.fillRect(bx - w * 0.48, bbase - h * 0.42, w * 0.96, h * 0.08);
        ctx.strokeStyle = pal.dark ? '#423f4f' : '#7d6b56';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.46, bbase - h * 0.50);
        ctx.lineTo(bx + w * 0.46, bbase - h * 0.50);
        ctx.stroke();

        // Main Timber Dwelling
        ctx.fillStyle = pal.dark ? '#23222a' : '#4d4235';
        ctx.fillRect(bx - w * 0.36, bbase - h * 0.78, w * 0.72, h * 0.40);

        // Slanted Shingle Roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.54, bbase - h * 0.78);
        ctx.lineTo(bx, bbase - h * 1.08);
        ctx.lineTo(bx + w * 0.54, bbase - h * 0.78);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3c3a47' : '#574c3e';
        ctx.fill();

        // Quiet amber window
        ctx.fillStyle = 'rgba(235, 175, 55, 0.85)';
        ctx.fillRect(bx - w * 0.14, bbase - h * 0.65, w * 0.28, h * 0.18);

      } else if (bldg.type === 'gate') {
        // ── Gu Yue Fortified Mountain Gate (古月坚固寨门) ──
        // Spiked Timber Palisades (外围拒马鹿角木桩)
        ctx.fillStyle = pal.dark ? '#1c1b20' : '#38322a';
        ctx.fillRect(bx - w * 0.68, bbase - h * 0.45, w * 0.18, h * 0.45);
        ctx.fillRect(bx + w * 0.50, bbase - h * 0.45, w * 0.18, h * 0.45);

        // Twin Heavy Gateposts (粗壮石木门柱)
        ctx.fillStyle = pal.dark ? '#29272d' : '#3b362f';
        ctx.fillRect(bx - w * 0.46, bbase - h * 0.88, w * 0.18, h * 0.88);
        ctx.fillRect(bx + w * 0.28, bbase - h * 0.88, w * 0.18, h * 0.88);

        // Heavy Timber Crossbeam Lintel (重横梁)
        ctx.fillRect(bx - w * 0.58, bbase - h * 0.94, w * 1.16, h * 0.15);

        // Tiled Gate Canopy Roof (歇山门楼顶)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.68, bbase - h * 0.94);
        ctx.lineTo(bx, bbase - h * 1.22);
        ctx.lineTo(bx + w * 0.68, bbase - h * 0.94);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#423f4c' : '#4d463b';
        ctx.fill();

        // Twin Gu Yue Red Clan Banners (左右迎风烈烈战旗)
        var flagSway = Math.sin((clock || 0) * 0.004) * (w * 0.08);
        ctx.fillStyle = pal.red;
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.44, bbase - h * 0.82);
        ctx.lineTo(bx - w * 0.44 - w * 0.22 + flagSway, bbase - h * 0.72);
        ctx.lineTo(bx - w * 0.44, bbase - h * 0.58);
        ctx.closePath();
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(bx + w * 0.44, bbase - h * 0.82);
        ctx.lineTo(bx + w * 0.44 + w * 0.22 + flagSway, bbase - h * 0.72);
        ctx.lineTo(bx + w * 0.44, bbase - h * 0.58);
        ctx.closePath();
        ctx.fill();

      } else if (bldg.type === 'tower') {
        // ── Perimeter Lookout Watchtower (高耸瞭望哨楼) ──
        // 4 Cross-braced Timber Stilts (四方交叉木桁柱)
        ctx.fillStyle = pal.dark ? '#26242a' : '#3a352e';
        ctx.fillRect(bx - w * 0.36, bbase - h * 0.78, w * 0.12, h * 0.78);
        ctx.fillRect(bx + w * 0.24, bbase - h * 0.78, w * 0.12, h * 0.78);
        // X-Braces
        ctx.strokeStyle = pal.dark ? '#333139' : '#4d463c';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.32, bbase - h * 0.20); ctx.lineTo(bx + w * 0.32, bbase - h * 0.65);
        ctx.moveTo(bx + w * 0.32, bbase - h * 0.20); ctx.lineTo(bx - w * 0.32, bbase - h * 0.65);
        ctx.stroke();

        // Elevated Guard Platform with Railing (护栏瞭望台)
        ctx.fillStyle = pal.dark ? '#1a191f' : '#2e2a24';
        ctx.fillRect(bx - w * 0.48, bbase - h * 0.84, w * 0.96, h * 0.10);
        ctx.strokeStyle = pal.dark ? '#454252' : '#6b6154';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.46, bbase - h * 0.92);
        ctx.lineTo(bx + w * 0.46, bbase - h * 0.92);
        ctx.stroke();

        // Conical Thatched Guard Roof (尖顶茅草顶棚)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.56, bbase - h * 0.92);
        ctx.lineTo(bx, bbase - h * 1.22);
        ctx.lineTo(bx + w * 0.56, bbase - h * 0.92);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3c3945' : '#4e463a';
        ctx.fill();

        // Animated Beacon Fire Brazier (夜巡烽火盆 - 火光闪烁)
        var firePulse = Math.sin((clock || 0) * 0.007) * 0.15;
        var bg = ctx.createRadialGradient(bx, bbase - h * 0.86, 0, bx, bbase - h * 0.86, w * (0.65 + firePulse));
        bg.addColorStop(0, 'rgba(255, 200, 80, 0.90)');
        bg.addColorStop(0.35, 'rgba(235, 110, 35, 0.70)');
        bg.addColorStop(1, 'rgba(235, 110, 35, 0)');
        ctx.fillStyle = bg;
        ctx.beginPath(); ctx.arc(bx, bbase - h * 0.86, w * (0.65 + firePulse), 0, 6.2832); ctx.fill();

      } else {
        // ── Terraced Village Cottages & Clan Workshops (青石石屋与农家瓦舍) ──
        // Stone foundation footing
        ctx.fillStyle = pal.dark ? '#1e1f26' : '#575249';
        ctx.fillRect(bx - w * 0.46, bbase - h * 0.18, w * 0.92, h * 0.18);
        // Timber walls
        ctx.fillStyle = pal.dark ? '#272630' : '#423d34';
        ctx.fillRect(bx - w * 0.40, bbase - h * 0.68, w * 0.80, h * 0.50);
        // Stone chimney
        ctx.fillStyle = pal.dark ? '#34333d' : '#696256';
        ctx.fillRect(bx + w * 0.22, bbase - h * 0.95, w * 0.10, h * 0.35);

        // Flared Slate Roof (青石板斜顶)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.58, bbase - h * 0.68);
        ctx.lineTo(bx, bbase - h * 1.08);
        ctx.lineTo(bx + w * 0.58, bbase - h * 0.68);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3b3a45' : '#544c41';
        ctx.fill();

        // Warm amber window
        ctx.fillStyle = 'rgba(235, 175, 55, 0.85)';
        ctx.fillRect(bx - w * 0.18, bbase - h * 0.54, w * 0.36, h * 0.22);
        // Porch lantern
        var plg = ctx.createRadialGradient(bx - w * 0.30, bbase - h * 0.44, 0, bx - w * 0.30, bbase - h * 0.44, w * 0.50);
        plg.addColorStop(0, 'rgba(235, 175, 55, 0.65)');
        plg.addColorStop(1, 'rgba(235, 175, 55, 0)');
        ctx.fillStyle = plg;
        ctx.beginPath(); ctx.arc(bx - w * 0.30, bbase - h * 0.44, w * 0.50, 0, 6.2832); ctx.fill();
      }

      ctx.restore();
    }
  };

  // ── Subterranean Spirit Spring & River of Light (地下灵泉与觉醒光河) ─────────
  World.prototype.drawSubterraneanCavern = function (pal, clock) {
    var ctx = this.ctx, i;
    var t = (clock || 0) * 0.001;

    // 1. Ancestral Cavern Archway (族长议事大厅后的灵泉溶洞岩穴入口)
    var caveArch = project(-0.25, heightAt(-0.25, 2.55) + 0.05, 2.55);
    if (caveArch.z > 0.25) {
      ctx.save();
      var cw = Math.max(16, caveArch.f * 0.14);
      var ch = Math.max(12, caveArch.f * 0.11);
      // Dark fissure cavity
      ctx.fillStyle = pal.dark ? '#050608' : '#121110';
      ctx.beginPath();
      ctx.ellipse(caveArch.x, caveArch.y, cw * 0.65, ch * 0.65, 0, Math.PI, 0);
      ctx.fill();
      // Stalactites hanging from cavern entrance
      ctx.fillStyle = pal.dark ? '#181b22' : '#3d3830';
      for (var st = -3; st <= 3; st++) {
        var sx = caveArch.x + st * (cw * 0.16);
        var slen = ch * (0.35 + Math.abs(Math.sin(st * 1.7)) * 0.35);
        ctx.beginPath();
        ctx.moveTo(sx - 2, caveArch.y - ch * 0.60);
        ctx.lineTo(sx, caveArch.y - ch * 0.60 + slen);
        ctx.lineTo(sx + 2, caveArch.y - ch * 0.60);
        ctx.closePath();
        ctx.fill();
      }
      // Glowing cavern interior glow from the underground spirit spring
      var caveGlow = ctx.createRadialGradient(caveArch.x, caveArch.y, 0, caveArch.x, caveArch.y, cw * 1.2);
      caveGlow.addColorStop(0, 'rgba(80, 220, 240, 0.45)');
      caveGlow.addColorStop(0.5, 'rgba(120, 230, 200, 0.18)');
      caveGlow.addColorStop(1, 'rgba(80, 220, 240, 0)');
      ctx.fillStyle = caveGlow;
      ctx.beginPath(); ctx.arc(caveArch.x, caveArch.y, cw * 1.2, 0, 6.2832); ctx.fill();
      ctx.restore();
    }

    // 2. Cascading Spirit Waterfall into the Cavern Pool (灵泉飞瀑)
    var falls = [
      [-0.20, 1.20, 2.50],
      [-0.12, 0.82, 2.38],
      [-0.04, 0.50, 2.25]
    ];
    var pFalls = [];
    for (i = 0; i < falls.length; i++) {
      var fp = project(falls[i][0], falls[i][1], falls[i][2]);
      if (fp.z > 0.25) pFalls.push(fp);
    }
    if (pFalls.length >= 2) {
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(pFalls[0].x, pFalls[0].y);
      for (i = 1; i < pFalls.length; i++) {
        ctx.lineTo(pFalls[i].x, pFalls[i].y);
      }
      ctx.lineWidth = Math.max(3, pFalls[0].f * 0.035);
      var wfg = ctx.createLinearGradient(pFalls[0].x, pFalls[0].y, pFalls[pFalls.length - 1].x, pFalls[pFalls.length - 1].y);
      wfg.addColorStop(0, 'rgba(200, 240, 255, 0.85)');
      wfg.addColorStop(0.5, 'rgba(120, 230, 240, 0.90)');
      wfg.addColorStop(1, 'rgba(235, 250, 255, 0.95)');
      ctx.strokeStyle = wfg;
      ctx.lineCap = 'round';
      ctx.stroke();
      ctx.restore();
    }

    // 3. The River of Light (觉醒光河) - Multi-layer Shimmering Current
    var riverPts = [
      [-0.15, 0.45, 1.40],
      [0.05, 0.35, 1.65],
      [0.25, 0.28, 1.90],
      [0.45, 0.22, 2.15],
      [0.65, 0.18, 2.40]
    ];
    var projectedRiver = [];
    for (i = 0; i < riverPts.length; i++) {
      var rp = project(riverPts[i][0], riverPts[i][1], riverPts[i][2]);
      if (rp.z > 0.25) projectedRiver.push(rp);
    }
    if (projectedRiver.length >= 2) {
      ctx.save();
      // Flowing luminous river surface
      ctx.beginPath();
      ctx.moveTo(projectedRiver[0].x - projectedRiver[0].f * 0.065, projectedRiver[0].y);
      for (i = 1; i < projectedRiver.length; i++) {
        ctx.lineTo(projectedRiver[i].x - projectedRiver[i].f * 0.075, projectedRiver[i].y);
      }
      for (i = projectedRiver.length - 1; i >= 0; i--) {
        ctx.lineTo(projectedRiver[i].x + projectedRiver[i].f * 0.075, projectedRiver[i].y);
      }
      ctx.closePath();
      var rlg = ctx.createLinearGradient(
        projectedRiver[0].x, projectedRiver[0].y,
        projectedRiver[projectedRiver.length - 1].x, projectedRiver[projectedRiver.length - 1].y
      );
      rlg.addColorStop(0, 'rgba(70, 190, 235, 0.80)');
      rlg.addColorStop(0.35, 'rgba(110, 235, 210, 0.90)');
      rlg.addColorStop(0.70, 'rgba(130, 220, 255, 0.85)');
      rlg.addColorStop(1, 'rgba(235, 205, 80, 0.82)');
      ctx.fillStyle = rlg;
      ctx.fill();

      // Flowing Light Ribbons (光河波纹)
      for (var rib = -1; rib <= 1; rib++) {
        ctx.beginPath();
        var waveOffset = Math.sin(t * 2.2 + rib * 1.5) * 0.02;
        for (i = 0; i < projectedRiver.length; i++) {
          var px = projectedRiver[i].x + rib * (projectedRiver[i].f * 0.03) + Math.sin(t * 3.0 + i) * 3.0;
          var py = projectedRiver[i].y + waveOffset * projectedRiver[i].f;
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.lineWidth = Math.max(1.2, projectedRiver[0].f * 0.018);
        ctx.strokeStyle = rib === 0 ? 'rgba(255, 255, 255, 0.75)' : 'rgba(120, 240, 255, 0.45)';
        ctx.stroke();
      }

      // Cavern River Ambient Luminescence
      ctx.lineWidth = Math.max(6, projectedRiver[0].f * 0.12);
      ctx.strokeStyle = 'rgba(80, 215, 245, 0.32)';
      ctx.stroke();

      // 4. Floating Hope Gu Starlight Motes (希望蛊光点 - 星光璀璨)
      // Chapter 4: Hope Gu are like floating stars, circling and entering the youth's apertures
      for (var gi = 0; gi < 22; gi++) {
        var frac = (t * 0.065 + gi * 0.045) % 1.0;
        var pIdx = Math.floor(frac * (riverPts.length - 1));
        var subFrac = (frac * (riverPts.length - 1)) - pIdx;
        var pA = riverPts[pIdx], pB = riverPts[pIdx + 1];
        var gx = pA[0] + (pB[0] - pA[0]) * subFrac + Math.sin(t * 1.8 + gi * 1.3) * 0.07;
        var gy = pA[1] + (pB[1] - pA[1]) * subFrac + 0.12 + Math.abs(Math.sin(t * 2.4 + gi * 0.9)) * 0.38;
        var gz = pA[2] + (pB[2] - pA[2]) * subFrac + Math.cos(t * 1.6 + gi) * 0.06;
        var gp = project(gx, gy, gz);
        if (gp.z > 0.25) {
          var pulse = 0.75 + Math.sin(t * 4.0 + gi * 2.0) * 0.25;
          var gr = Math.max(1.6, gp.f * 0.024) * pulse;
          var gg = ctx.createRadialGradient(gp.x, gp.y, 0, gp.x, gp.y, gr * 2.8);
          gg.addColorStop(0, '#ffffff');
          gg.addColorStop(0.3, 'rgba(140, 235, 255, 0.95)');
          gg.addColorStop(0.7, 'rgba(90, 200, 245, 0.45)');
          gg.addColorStop(1, 'rgba(90, 200, 245, 0)');
          ctx.fillStyle = gg;
          ctx.beginPath(); ctx.arc(gp.x, gp.y, gr * 2.8, 0, 6.2832); ctx.fill();

          // Tiny cross starburst on prominent Hope Gu motes
          if (gi % 3 === 0) {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.75)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(gp.x - gr * 1.8, gp.y); ctx.lineTo(gp.x + gr * 1.8, gp.y);
            ctx.moveTo(gp.x, gp.y - gr * 1.8); ctx.lineTo(gp.x + gr * 1.8, gp.y);
            ctx.stroke();
          }
        }
      }
      ctx.restore();
    }
  };

  World.prototype.drawFrontier = function (pal) {
    if (this.reach >= 4) return; // Full world view at current frontier
    var ctx = this.ctx, i;
    var p = project(0, 0, 0);
    if (p.z < 0.25) return;
    var reach = this.reachNow();
    ctx.save();
    ctx.strokeStyle = pal.red;
    ctx.globalAlpha = 0.30;
    ctx.setLineDash([7, 7]);
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    for (i = 0; i <= 72; i++) {
      var a = i / 72 * Math.PI * 2;
      var q = project(Math.cos(a) * reach,
                      heightAt(Math.cos(a) * reach, Math.sin(a) * reach) + 0.12,
                      Math.sin(a) * reach);
      if (i === 0) ctx.moveTo(q.x, q.y); else ctx.lineTo(q.x, q.y);
    }
    ctx.stroke();
    ctx.restore();
    ctx.globalAlpha = 1;
  };

  World.prototype.drawAir = function (pal, t) {
    var ctx = this.ctx, i;
    var sway = Math.sin(t * 0.00013) * 0.6;
    var gr = ctx.createLinearGradient(0, this.h * 0.66, 0, this.h);
    gr.addColorStop(0, 'rgba(0,0,0,0)');
    gr.addColorStop(0.55, pal.dark ? 'rgba(200,196,188,0.06)' : 'rgba(255,255,255,0.44)');
    gr.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = gr;
    ctx.fillRect(0, this.h * 0.66, this.w, this.h * 0.34);
    for (i = 0; i < 3; i++) {
      var bx = -13 + i * 3.0 + Math.sin(t * 0.00021 + i) * 1.0;
      var bz = -12 + i * 2.4 + sway;
      var byy = 5.3 + i * 0.5 + Math.cos(t * 0.00018 + i * 1.7) * 0.2;
      var bp = project(bx, byy, bz);
      if (bp.z < 0.25) continue;
      var bw = Math.max(2.2, bp.f * 0.085);
      ctx.globalAlpha = 0.4;
      ctx.strokeStyle = pal.ink;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(bp.x - bw, bp.y);
      ctx.quadraticCurveTo(bp.x - bw * 0.45, bp.y - bw * 0.5, bp.x, bp.y);
      ctx.quadraticCurveTo(bp.x + bw * 0.45, bp.y - bw * 0.5, bp.x + bw, bp.y);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  };

  World.prototype.drawPeople = function (pal, clock) {
    if (!this.people || !this.people.length) return;
    var ctx = this.ctx, i;
    var placed = [];
    for (i = 0; i < this.people.length; i++) {
      var f = this.people[i];
      if (chapterOf(f) > this.reach) continue;
      var y = heightAt(f.x, f.z);
      var p = project(f.x, y, f.z);
      if (p.z < 0.25) continue;
      placed.push({ p: p, f: f, y: y });
    }
    placed.sort(function (a, b) { return b.p.z - a.p.z; });
    var sway = Math.sin((clock || 0) * 0.0006) * 0.012;
    for (i = 0; i < placed.length; i++) {
      var o = placed[i], s2 = Math.max(2.6, o.p.f * 0.085), x = o.p.x, yy = o.p.y;
      var robe = pal.ink;
      if (o.f.kind === 'demonic') robe = pal.red;
      if (o.f.kind === 'elder') robe = pal.dark ? '#6f6a63' : '#4a463f';
      ctx.globalAlpha = 0.95;
      // legs
      ctx.strokeStyle = robe; ctx.lineWidth = Math.max(1, s2 * 0.16);
      ctx.beginPath();
      ctx.moveTo(x - s2 * 0.16, yy); ctx.lineTo(x - s2 * 0.2 + sway * s2, yy - s2 * 0.55);
      ctx.moveTo(x + s2 * 0.16, yy); ctx.lineTo(x + s2 * 0.2 + sway * s2, yy - s2 * 0.55);
      ctx.stroke();
      // robe
      ctx.fillStyle = robe;
      ctx.beginPath();
      ctx.moveTo(x - s2 * 0.42 + sway * s2, yy - s2 * 0.5);
      ctx.lineTo(x + s2 * 0.42 + sway * s2, yy - s2 * 0.5);
      ctx.lineTo(x + s2 * 0.26 + sway * s2, yy - s2 * 1.32);
      ctx.lineTo(x - s2 * 0.26 + sway * s2, yy - s2 * 1.32);
      ctx.closePath(); ctx.fill();
      // shoulders and head
      ctx.beginPath();
      ctx.arc(x + sway * s2, yy - s2 * 1.5, s2 * 0.3, 0, 6.2832);
      ctx.fill();
      // hair
      ctx.fillStyle = pal.dark ? '#0d0d10' : '#141416';
      ctx.beginPath();
      ctx.arc(x + sway * s2, yy - s2 * 1.56, s2 * 0.31, Math.PI * 1.02, Math.PI * 2.0);
      ctx.fill();
      // rank sigil
      if (o.f.rank) {
        var sy = yy - s2 * 2.05;
        ctx.fillStyle = pal.gold;
        for (var r = 0; r < o.f.rank; r++) {
          ctx.globalAlpha = 0.9;
          ctx.fillRect(x + sway * s2 - s2 * 0.22 + r * s2 * 0.16, sy, s2 * 0.07, s2 * 0.5);
        }
      }
      // aptitude halo
      if (o.f.grade) {
        ctx.globalAlpha = 0.35;
        ctx.strokeStyle = o.f.grade === 'A' ? pal.gold : pal.red;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.ellipse(x + sway * s2, yy - s2 * 0.62, s2 * 0.72, s2 * 0.22, 0, 0, 6.2832);
        ctx.stroke();
      }
      ctx.globalAlpha = 1;
    }
  };

  World.prototype.peoplePins = function (els, clock) {
    var out = [], i;
    for (i = 0; i < this.people.length; i++) {
      var f = this.people[i], el = els[i];
      if (!el) continue;
      var y = heightAt(f.x, f.z);
      var p = project(f.x, y + 1.5, f.z);
      out.push({ el: el, x: p.x, y: p.y, z: p.z, live: chapterOf(f) <= this.reach });
    }
    return out;
  };

  World.prototype.pins = function (list) {
    var out = [], i;
    for (i = 0; i < list.length; i++) {
      var pn = list[i];
      var p = project(pn.x, heightAt(pn.x, pn.z) + 0.35, pn.z);
      out.push({ el: pn.el, x: p.x, y: p.y, z: p.z, f: p.f });
    }
    return out;
  };

  // ── loop & interaction ────────────────────────────────────────────────────
  function boot() {
    var canvas = document.getElementById('worldCanvas');
    if (!canvas || !canvas.getContext) return;
    var pinsBox = document.getElementById('worldPins');
    var hint = document.getElementById('worldHint');
    var world = new World(canvas);
    var reduce = false;
    try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

    var peopleEls = [];
    function buildPeople() {
      if (!pinsBox) return;
      peopleEls = [];
      for (var pi = 0; pi < world.people.length; pi++) {
        var f = world.people[pi];
        var a = document.createElement('a');
        a.className = 'world-pin world-figure';
        var base = (typeof window !== 'undefined' && /\/world\/?$/.test(window.location.pathname)) ? '../' : '';
        a.href = base + f.s;
        a.setAttribute('data-slug', f.s);
        a.setAttribute('data-c', f.c);
        a.innerHTML = '<span class="world-pin-dot"></span><span class="world-pin-label">' +
          f.t + '<em>ch. ' + f.c + (f.rank ? ' \u00b7 rank ' + f.rank : '') +
          (f.grade ? ' \u00b7 grade ' + f.grade : '') + '</em></span>';
        pinsBox.appendChild(a);
        peopleEls.push(a);
      }
    }

    var pinEls = [];
    if (pinsBox) {
      var data = [];
      try { data = JSON.parse(pinsBox.getAttribute('data-pins') || '[]'); } catch (e) { data = []; }
      var base = (typeof window !== 'undefined' && /\/world\/?$/.test(window.location.pathname)) ? '../' : '';
      for (var i = 0; i < data.length; i++) {
        var a = document.createElement('a');
        a.className = 'world-pin' + (data[i].c ? ' is-live' : '');
        a.href = base + data[i].s;
        a.setAttribute('data-c', data[i].c);
        a.innerHTML = '<span class="world-pin-dot"></span><span class="world-pin-label">' +
          data[i].t + '<em>ch. ' + data[i].c + '</em></span>';
        pinsBox.appendChild(a);
        pinEls.push({ el: a, x: data[i].x, z: data[i].z, t: data[i].t });
      }
    }

    var pal = palette();
    world.resize();
    world.draw(pal);

    var azBase = cam.az;

    // Vantage points directory covering all canonical landmarks
    var VANTAGE_PRESETS = {
      'overview':         { tx: 0.50, tz: 0.50, ty: 1.40, dist: 36, az: 2.45, pitch: 0.32 },
      'village':          { tx: 0.25, tz: 1.35, ty: 1.25, dist: 11.0, az: 2.55, pitch: 0.30 },
      'hall':             { tx: -0.35, tz: 2.30, ty: 1.65, dist: 5.5, az: 2.65, pitch: 0.22 },
      'academy':          { tx: -0.15, tz: 1.65, ty: 1.45, dist: 5.5, az: 2.60, pitch: 0.22 },
      'cavern':           { tx: 0.25, tz: 1.95, ty: 0.95, dist: 5.5, az: 2.75, pitch: 0.18 },
      'mo-manor':         { tx: 1.55, tz: 1.85, ty: 1.55, dist: 5.5, az: 2.50, pitch: 0.22 },
      'chi-manor':        { tx: -1.35, tz: 1.75, ty: 1.50, dist: 5.5, az: 2.70, pitch: 0.22 },
      'fang-residence':   { tx: 0.70, tz: 0.95, ty: 1.30, dist: 5.0, az: 2.55, pitch: 0.20 },
      'mountain-gate':    { tx: 0.20, tz: 0.15, ty: 1.00, dist: 5.5, az: 2.80, pitch: 0.18 },
      'north-tower':      { tx: 1.85, tz: 0.60, ty: 1.55, dist: 5.5, az: 2.40, pitch: 0.22 },
      'south-tower':      { tx: -0.85, tz: 0.65, ty: 1.45, dist: 5.5, az: 2.85, pitch: 0.22 },
      'bai':              { tx: -16.5, tz: -12.0, ty: 4.5, dist: 24, az: 2.40, pitch: 0.24 },
      'xiong':            { tx: 17.0, tz: -11.5, ty: 4.6, dist: 25, az: 0.92, pitch: 0.24 },
      'southern-border':  { tx: 0, tz: 0, ty: 2.2, dist: 98, az: 2.45, pitch: 0.36 }
    };

    window.RIWorld = {
      setReach: function (n) { world.reach = n; },
      setPeople: function (list) { world.people = list || []; },
      zoom: function (d) { target.dist = Math.max(2.2, Math.min(130, target.dist + d)); },
      zoomIn: function () { target.dist = Math.max(2.2, target.dist - 5.5); },
      zoomOut: function () { target.dist = Math.min(130, target.dist + 5.5); },
      look: function (deg) { azBase = deg * Math.PI / 180; },
      vantage: function (name) {
        var p = VANTAGE_PRESETS[name] || VANTAGE_PRESETS['overview'];
        target.tx = p.tx; target.tz = p.tz; target.ty = p.ty; target.dist = p.dist;
        target.az = p.az; target.pitch = p.pitch;
      },
      focus: function (x, z) {
        target.tx = x; target.tz = z;
        target.ty = heightAt(x, z) + 0.35;
        target.dist = 5.2; // comfortable close zoom for character inspection
      },
      reset: function () {
        target.tx = 0.50; target.tz = 0.50;
        target.ty = 1.40;
        target.dist = 36;
        target.az = 2.45;
        target.pitch = 0.32;
      }
    };

    function frame(t) {
      if (!reduce) {
        if (target.az !== undefined) {
          var daz = target.az - azBase;
          while (daz > Math.PI) daz -= Math.PI * 2;
          while (daz < -Math.PI) daz += Math.PI * 2;
          if (Math.abs(daz) < 0.003) {
            delete target.az;
          } else {
            azBase += daz * 0.07;
          }
        } else {
          azBase += 0.0011;
        }
        if (target.pitch !== undefined) {
          var dp = target.pitch - pitchBase;
          if (Math.abs(dp) < 0.003) {
            delete target.pitch;
          } else {
            pitchBase += dp * 0.07;
          }
        }
        parallax.x += (parallax.tx - parallax.x) * 0.045;
        parallax.y += (parallax.ty - parallax.y) * 0.045;
        cam.tx += (target.tx - cam.tx) * 0.08;
        cam.tz += (target.tz - cam.tz) * 0.08;
        cam.dist += (target.dist - cam.dist) * 0.08;
        cam.ty += (target.ty - cam.ty) * 0.08;
      }
      cam.az = azBase + parallax.x;
      cam.pitch = pitchBase + parallax.y * 0.5;
      world.draw(pal, t);

      if (peopleEls.length !== world.people.length) buildPeople();
      var placed = world.pins(pinEls);
      var walkers = world.peoplePins(peopleEls, t);
      for (var wi = 0; wi < walkers.length; wi++) {
        var wk = walkers[wi];
        var charDistFade = cam.dist < 52 ? 1 : Math.max(0, 1 - (cam.dist - 52) / 16);
        wk.el.style.opacity = (wk.live && wk.z > 0.3 && charDistFade > 0.05) ? String(charDistFade) : '0';
        wk.el.style.transform = 'translate(' + Math.round(wk.x) + 'px,' + Math.round(wk.y) + 'px)';
      }
      for (var k = 0; k < placed.length; k++) {
        var it = placed[k];
        var vis = it.z > 0.3 && it.x > -60 && it.x < world.w + 60 && it.y > -40 && it.y < world.h + 60;
        it.el.style.opacity = vis ? '1' : '0';
        it.el.style.transform = 'translate(' + Math.round(it.x) + 'px,' + Math.round(it.y) + 'px)';
      }
      requestAnimationFrame(frame);
    }
    if (reduce) {
      cam.az = azBase;
      buildPeople();
      var held = world.pins(pinEls);
      for (var hk = 0; hk < held.length; hk++) {
        held[hk].el.style.opacity = '1';
        held[hk].el.style.transform = 'translate(' + Math.round(held[hk].x) + 'px,' + Math.round(held[hk].y) + 'px)';
      }
      return;
    }
    requestAnimationFrame(frame);

    window.addEventListener('resize', function () {
      world.resize();
      pal = palette();
      world.draw(pal);
    });
    document.addEventListener('mousemove', function (e) {
      var r = canvas.getBoundingClientRect();
      parallax.tx = ((e.clientX - r.left) / r.width - 0.5) * 0.22;
      parallax.ty = ((e.clientY - r.top) / r.height - 0.5) * -0.16;
    });
    canvas.addEventListener('pointerdown', function (e) {
      drag.on = true; drag.x = e.clientX; drag.y = e.clientY;
      drag.az0 = azBase; drag.pitch0 = pitchBase;
      delete target.az; delete target.pitch;
      if (hint) hint.style.opacity = '0';
    });
    window.addEventListener('pointerup', function () { drag.on = false; });
    window.addEventListener('pointermove', function (e) {
      if (!drag.on) return;
      azBase = drag.az0 - (e.clientX - drag.x) * 0.006;
      pitchBase = Math.max(0.10, Math.min(0.60, drag.pitch0 + (e.clientY - drag.y) * 0.004));
    });
    // Smooth grand zoom on wheel
    canvas.addEventListener('wheel', function (e) {
      if (!canvas.getAttribute('data-zoom')) return;
      e.preventDefault();
      target.dist = Math.max(2.2, Math.min(130, target.dist + (e.deltaY > 0 ? 3.5 : -3.5)));
    }, { passive: false });

    // Multi-touch pinch-to-zoom on mobile
    var touchDist0 = null;
    canvas.addEventListener('touchstart', function (e) {
      if (e.touches.length === 2) {
        touchDist0 = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      }
    }, { passive: true });
    canvas.addEventListener('touchmove', function (e) {
      if (e.touches.length === 2 && touchDist0) {
        var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
        var diff = touchDist0 - d;
        target.dist = Math.max(2.2, Math.min(130, target.dist + diff * 0.06));
        touchDist0 = d;
      }
    }, { passive: true });
    canvas.addEventListener('touchend', function () { touchDist0 = null; });

    document.documentElement.addEventListener('themechange', function () { pal = palette(); });

    var obs = new MutationObserver(function () { pal = palette(); });
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { heightAt: heightAt, project: project, World: World, cam: cam };
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
