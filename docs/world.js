/* ============================================================
   The World Plate — a live 3D scene of Qing Mao Mountain and
   Gu Yue Village, drawn from the published chapters.

   Engineered with pure Canvas 2D: perspective projection,
   multi-octave ridged crag geology, Lambertian sun diffuse
   shading, and 3D architectural geometry for Gu Yue Village.
   ============================================================ */
(function () {
  'use strict';

  var GRID = 56;                 // heightfield resolution
  var SPAN = 26;                 // world units across
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

  var VILLAGE = { x: 0.25, z: 1.35 };

  function heightAt(x, z) {
    // 1. Natural mountain foundation with sharp crags
    var base = fbm(x * 0.082 + 11.3, z * 0.082 + 7.7) * 1.5;
    var crags = ridged(x * 0.11 + 4.3, z * 0.11 + 2.7) * 2.2;
    var h = 0.35 + base + crags * 0.58;

    // 2. Main Qing Mao Mountain Peak (青茅主峰): towering crest behind the village
    var dq = Math.hypot(x - 5.5, z + 2.8);
    h += 5.6 * Math.exp(-(dq * dq) / 26);

    // 3. North-western crag precipice & gorge
    var dn = Math.hypot(x + 5.2, z - 2.5);
    h += 3.6 * Math.exp(-(dn * dn) / 18);

    // 4. Distant eastern horizon ridge
    var de = Math.hypot(x + 8.8, z + 7.8);
    h += 2.6 * Math.exp(-(de * de) / 46);

    // 5. Gu Yue Village Shelf: natural mountain terrace where the clan built their settlement
    var dx = (x - VILLAGE.x) / 1.85;
    var dz = (z - VILLAGE.z) / 1.35;
    var shelf = Math.exp(-(dx * dx + dz * dz) / 1.6);
    // Smooth terraced living shelf, gently stepped from height 0.95 at gate to 1.55 at Grand Council Hall
    var terraceH = 0.95 + (z - 0.2) * 0.24;
    h = h * (1 - 0.88 * shelf) + terraceH * (0.88 * shelf);
    return h;
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
  var cam = { az: 0.62, pitch: 0.30, dist: 40, f: 900, cx: 0, cy: 0, ty: 1.1, tx: 0, tz: 0 };
  var target = { dist: 40, ty: 1.1, tx: 0, tz: 0 };
  var drag = { on: false, x: 0, y: 0, az0: 0, pitch0: 0, moved: 0 };
  var pitchBase = 0.30;
  var parallax = { x: 0, y: 0, tx: 0, ty: 0 };

  function project(x, y, z) {
    var dx = x - (cam.tx || 0), dz = z - (cam.tz || 0);
    var ca = Math.cos(cam.az), sa = Math.sin(cam.az);
    var rx = dx * ca - dz * sa;
    var rz = dx * sa + dz * ca;
    var ry = y - cam.ty;
    var cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
    var y2 = ry * cp - rz * sp;
    var z2 = ry * sp + rz * cp + cam.dist;
    if (z2 < 0.6) z2 = 0.6;
    var f = cam.f / z2;
    return { x: cam.cx + rx * f, y: cam.cy - y2 * f, z: z2, f: f };
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
    this.build();
  }

  function chapterOf(f) { return f.chapter !== undefined ? f.chapter : (f.c || 1); }

  World.prototype.reachNow = function () {
    if (this.reach >= 4) return 8.4;
    return REACH_AT[this.reach] || 8.4;
  };

  World.prototype.build = function () {
    var step = SPAN / GRID;
    for (var j = 0; j <= GRID; j++) {
      for (var i = 0; i <= GRID; i++) {
        var x = -SPAN / 2 + i * step;
        var z = -SPAN / 2 + j * step;
        var h = heightAt(x, z);
        this.heights[j * (GRID + 1) + i] = h;

        // 3D Lambertian normal calculation: sunlight from northwest (-0.52, 0.72, -0.45)
        var hx = heightAt(x + step * 0.5, z) - heightAt(x - step * 0.5, z);
        var hz = heightAt(x, z + step * 0.5) - heightAt(x, z - step * 0.5);
        var len = Math.hypot(hx, step, hz);
        var nx = -hx / len, ny = step / len, nz = -hz / len;
        var sunDot = nx * (-0.48) + ny * 0.76 + nz * (-0.42);
        this.shade[j * (GRID + 1) + i] = Math.max(0.15, Math.min(1.0, (sunDot + 0.35) / 1.35));
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
    cam.cy = this.h * 0.60;
    cam.f = this.w * 0.95;
  };

  World.prototype.draw = function (pal, clock) {
    var ctx = this.ctx, i, j;
    ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    ctx.clearRect(0, 0, this.w, this.h);

    // 1. Sky & horizon atmosphere
    var sky = ctx.createLinearGradient(0, 0, 0, this.h);
    sky.addColorStop(0, pal.dark ? mix(pal.paper, '#000000', 0.45) : mix(pal.paper, '#ffffff', 0.5));
    sky.addColorStop(0.55, pal.paper);
    sky.addColorStop(1, pal.dark ? mix(pal.paper, '#000000', 0.25) : mix(pal.paper, '#ffffff', 0.85));
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, this.w, this.h);

    // 2. The morning sun illuminating Qing Mao Mountain
    var sun = project(-16, 6.5, 0);
    if (sun.z > 1) {
      var sr = Math.max(26, sun.f * 1.1);
      var g = ctx.createRadialGradient(sun.x, sun.y, 0, sun.x, sun.y, sr);
      g.addColorStop(0, pal.dark ? 'rgba(201,162,39,0.30)' : 'rgba(201,162,39,0.22)');
      g.addColorStop(1, 'rgba(201,162,39,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(sun.x, sun.y, sr, 0, 6.2832); ctx.fill();
    }

    // 3. Distant mountain mist layers
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

    // 4. Solid, photorealistic terrain with natural biome stratification
    var n = GRID + 1, step = SPAN / GRID;
    var reach = this.reachNow();
    var ca = Math.cos(cam.az), sa = Math.sin(cam.az);

    var ip = [], jp = [];
    for (i = 0; i < GRID; i++) ip.push(i);
    for (j = 0; j < GRID; j++) jp.push(j);
    if (ca * sa > 0) { ip.reverse(); } else { jp.reverse(); }
    if (ca < 0) { ip.reverse(); jp.reverse(); }

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

    var ink = pal.ink, paper = pal.paper;
    for (var a = 0; a < jp.length; a++) {
      for (var b = 0; b < ip.length; b++) {
        i = ip[b]; j = jp[a];
        var k0 = j * n + i, k1 = k0 + 1, k2 = k0 + n, k3 = k2 + 1;
        var z0 = pts[k0 * 4 + 2], z1 = pts[k1 * 4 + 2], z2 = pts[k2 * 4 + 2], z3 = pts[k3 * 4 + 2];
        var depth = (z0 + z1 + z2 + z3) / 4;
        if (depth > cam.dist * 2.35) continue;

        var hgt = (this.heights[k0] + this.heights[k1] + this.heights[k2] + this.heights[k3]) / 4;
        var light = this.shade[k0];

        // Biome Color Palette with 3D Sun Lighting
        var col;
        if (pal.dark) {
          // Obsidian Mode:
          if (hgt > 5.2) {
            // Summit snow / frost on high crag
            col = mix('#3b404d', '#c2c9d6', Math.min(1, (hgt - 5.2) / 1.5) * light);
          } else if (hgt > 3.4) {
            // High rocky granite crags
            col = mix('#181b22', '#4b5263', (hgt - 3.4) / 1.8 * 0.7 + light * 0.3);
          } else if (hgt > 1.3) {
            // Dense alpine pine forest slope
            col = mix('#111c16', '#253d2f', light * 0.85);
          } else if (hgt > 0.85) {
            // Living village terrace stone and compacted earth
            col = mix('#1c1a17', '#38332c', light * 0.9);
          } else {
            // Deep mist-veiled valley basin
            col = mix('#0c0d12', '#1a1b24', light * 0.6);
          }
        } else {
          // Light Mode (Classical Chinese Shanshui Landscape):
          if (hgt > 5.2) {
            // High snow cap and pale granite
            col = mix('#e0dad0', '#ffffff', Math.min(1, (hgt - 5.2) / 1.5) * light);
          } else if (hgt > 3.4) {
            // Weathered granite crags with warm sun highlights
            col = mix('#635e54', '#b8b0a2', light);
          } else if (hgt > 1.3) {
            // Alpine pine green slope wash
            col = mix('#526955', '#9bb09e', light);
          } else if (hgt > 0.85) {
            // Village terrace cobblestone and warm earth
            col = mix('#b8b0a0', '#dfd9cc', light);
          } else {
            // Soft valley mist and riverbed
            col = mix('#cdc7ba', '#e8e4dc', light * 0.8);
          }
        }

        // Atmosphere fog distance fade
        var d = (off[k0] + off[k3]) / 2;
        var fog = d < reach ? 0 : Math.min(1, (d - reach) / 5.0);
        var mist = 1 - Math.max(0, Math.min(0.94, fog));
        col = mix(col, paper, 1 - mist * mist);

        var alpha = 0.98 * (1 - fog * 0.96);
        ctx.globalAlpha = alpha < 0.05 ? 0.05 : alpha;
        ctx.fillStyle = col;
        ctx.beginPath();
        ctx.moveTo(pts[k0 * 4], pts[k0 * 4 + 1]);
        ctx.lineTo(pts[k1 * 4], pts[k1 * 4 + 1]);
        ctx.lineTo(pts[k3 * 4], pts[k3 * 4 + 1]);
        ctx.lineTo(pts[k2 * 4], pts[k2 * 4 + 1]);
        ctx.closePath();
        ctx.fill();

        // Forest: organic pine clusters on middle slopes without grid lines
        if (hgt > 1.4 && hgt < 4.2 && fog < 0.50) {
          var seed = hash(i * 3.1 + 0.7, j * 2.7 + 1.3);
          if (seed > 0.82) {
            var cx = (pts[k0 * 4] + pts[k3 * 4]) / 2;
            var cy = (pts[k0 * 4 + 1] + pts[k3 * 4 + 1]) / 2;
            var sc = Math.max(1.2, pts[k0 * 4 + 3] * 0.06);
            ctx.globalAlpha = alpha * 0.65;
            ctx.fillStyle = pal.dark ? '#0c150e' : '#2d3d2e';
            // triangular pine silhouette
            ctx.beginPath();
            ctx.moveTo(cx, cy - sc * 3.0);
            ctx.lineTo(cx - sc * 1.1, cy);
            ctx.lineTo(cx + sc * 1.1, cy);
            ctx.closePath();
            ctx.fill();
          }
        }
      }
    }
    ctx.globalAlpha = 1;

    // 5. Tangible 3D Village Architecture & Landmarks
    this.drawVillageBuildings(pal, clock || 0);
    this.drawSubterraneanCavern(pal, clock || 0);

    // 6. Cultivators standing in the world
    this.drawPeople(pal, clock || 0);

    // 7. Translation frontier & atmosphere
    this.drawFrontier(pal);
    this.drawAir(pal, clock || 0);
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
      if (p.z > 1) {
        list.push({ s: s, y: y, p: p });
      }
    }
    // Depth sort: back to front painter's algorithm
    list.sort(function (a, b) { return b.p.z - a.p.z; });

    for (i = 0; i < list.length; i++) {
      var bldg = list[i].s, by = list[i].y, bp = list[i].p;
      var f = bp.f;
      var w = Math.max(8, bldg.w * f * 0.10);
      var h = Math.max(10, bldg.h * f * 0.12);
      var bx = bp.x, bbase = bp.y;

      ctx.save();

      if (bldg.type === 'pagoda2') {
        // ── Grand Clan Council Hall (2-tier Pagoda) ──
        // 1. Stone Foundation Platform
        ctx.fillStyle = pal.dark ? '#22232a' : '#544f47';
        ctx.fillRect(bx - w * 0.65, bbase - h * 0.22, w * 1.3, h * 0.22);
        ctx.fillStyle = pal.dark ? '#2e303a' : '#736d62';
        ctx.fillRect(bx - w * 0.58, bbase - h * 0.22, w * 1.16, h * 0.06);

        // 2. Lower Pavilion Walls & Timber Pillars
        ctx.fillStyle = pal.dark ? '#1a191f' : '#332e27';
        ctx.fillRect(bx - w * 0.50, bbase - h * 0.62, w * 1.0, h * 0.40);
        // glowing council windows
        ctx.fillStyle = 'rgba(235, 175, 55, 0.85)';
        ctx.fillRect(bx - w * 0.36, bbase - h * 0.54, w * 0.22, h * 0.24);
        ctx.fillRect(bx + w * 0.14, bbase - h * 0.54, w * 0.22, h * 0.24);

        // 3. Lower Tier Flared Eaves (feiyan)
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.75, bbase - h * 0.62);
        ctx.quadraticCurveTo(bx - w * 0.4, bbase - h * 0.74, bx, bbase - h * 0.78);
        ctx.quadraticCurveTo(bx + w * 0.4, bbase - h * 0.74, bx + w * 0.75, bbase - h * 0.62);
        ctx.lineTo(bx + w * 0.58, bbase - h * 0.60);
        ctx.lineTo(bx - w * 0.58, bbase - h * 0.60);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3b3a45' : '#453f36';
        ctx.fill();

        // 4. Upper Tier Pavilion
        ctx.fillStyle = pal.dark ? '#26252e' : '#3d3730';
        ctx.fillRect(bx - w * 0.32, bbase - h * 1.05, w * 0.64, h * 0.27);
        // upper window
        ctx.fillStyle = 'rgba(235, 175, 55, 0.9)';
        ctx.fillRect(bx - w * 0.12, bbase - h * 0.98, w * 0.24, h * 0.16);

        // 5. Grand Upper Roof with Upturned Flared Corners
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.60, bbase - h * 1.05);
        ctx.quadraticCurveTo(bx - w * 0.28, bbase - h * 1.25, bx, bbase - h * 1.32);
        ctx.quadraticCurveTo(bx + w * 0.28, bbase - h * 1.25, bx + w * 0.60, bbase - h * 1.05);
        ctx.lineTo(bx + w * 0.44, bbase - h * 1.03);
        ctx.lineTo(bx - w * 0.44, bbase - h * 1.03);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#4c4a57' : '#524b40';
        ctx.fill();

        // 6. Gu Yue Clan Golden Crescent Moon Finial (月牙顶针)
        ctx.strokeStyle = pal.gold;
        ctx.lineWidth = Math.max(1.5, f * 0.015);
        ctx.beginPath();
        ctx.arc(bx, bbase - h * 1.44, Math.max(3, w * 0.12), Math.PI * 0.2, Math.PI * 1.3);
        ctx.stroke();

        // 7. Glowing Clan Lanterns
        var lg1 = ctx.createRadialGradient(bx - w * 0.52, bbase - h * 0.58, 0, bx - w * 0.52, bbase - h * 0.58, w * 0.55);
        lg1.addColorStop(0, 'rgba(235, 175, 55, 0.65)');
        lg1.addColorStop(1, 'rgba(235, 175, 55, 0)');
        ctx.fillStyle = lg1;
        ctx.beginPath(); ctx.arc(bx - w * 0.52, bbase - h * 0.58, w * 0.55, 0, 6.2832); ctx.fill();

        var lg2 = ctx.createRadialGradient(bx + w * 0.52, bbase - h * 0.58, 0, bx + w * 0.52, bbase - h * 0.58, w * 0.55);
        lg2.addColorStop(0, 'rgba(235, 175, 55, 0.65)');
        lg2.addColorStop(1, 'rgba(235, 175, 55, 0)');
        ctx.fillStyle = lg2;
        ctx.beginPath(); ctx.arc(bx + w * 0.52, bbase - h * 0.58, w * 0.55, 0, 6.2832); ctx.fill();

      } else if (bldg.type === 'courtyard') {
        // ── Clan Academy & Martial Grounds ──
        // Courtyard perimeter wall
        ctx.fillStyle = pal.dark ? '#23232b' : '#6b6459';
        ctx.fillRect(bx - w * 0.60, bbase - h * 0.26, w * 1.20, h * 0.26);
        // Courtyard ground
        ctx.fillStyle = pal.dark ? '#1c1c24' : '#8c8477';
        ctx.fillRect(bx - w * 0.54, bbase - h * 0.22, w * 1.08, h * 0.22);
        // Main Lecture Pavilion
        ctx.fillStyle = pal.dark ? '#2b2a33' : '#453f36';
        ctx.fillRect(bx - w * 0.40, bbase - h * 0.72, w * 0.80, h * 0.50);
        // Tiled Roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.55, bbase - h * 0.72);
        ctx.lineTo(bx, bbase - h * 1.02);
        ctx.lineTo(bx + w * 0.55, bbase - h * 0.72);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3d3c47' : '#574f43';
        ctx.fill();
        // Academy entrance lantern
        ctx.fillStyle = pal.gold;
        ctx.beginPath(); ctx.arc(bx, bbase - h * 0.52, Math.max(1.5, w * 0.05), 0, 6.2832); ctx.fill();

      } else if (bldg.type === 'manor') {
        // ── Clan Faction Manors (Mo & Chi Compounds) ──
        // Enclosed Manor Wall
        ctx.fillStyle = pal.dark ? '#24242c' : '#5e574d';
        ctx.fillRect(bx - w * 0.55, bbase - h * 0.32, w * 1.10, h * 0.32);
        // Manor Central Residence
        ctx.fillStyle = pal.dark ? '#1e1d24' : '#423d35';
        ctx.fillRect(bx - w * 0.38, bbase - h * 0.78, w * 0.76, h * 0.46);
        // Dual-gabled Manor Roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.52, bbase - h * 0.78);
        ctx.quadraticCurveTo(bx - w * 0.25, bbase - h * 0.95, bx, bbase - h * 1.05);
        ctx.quadraticCurveTo(bx + w * 0.25, bbase - h * 0.95, bx + w * 0.52, bbase - h * 0.78);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3a3945' : '#524b41';
        ctx.fill();
        // Warm amber window
        ctx.fillStyle = 'rgba(235, 175, 55, 0.8)';
        ctx.fillRect(bx - w * 0.16, bbase - h * 0.62, w * 0.32, h * 0.22);

      } else if (bldg.type === 'gate') {
        // ── Gu Yue Fortified Mountain Gate ──
        // Twin Timber & Stone Gateposts
        ctx.fillStyle = pal.dark ? '#29272d' : '#3b362f';
        ctx.fillRect(bx - w * 0.45, bbase - h * 0.85, w * 0.18, h * 0.85);
        ctx.fillRect(bx + w * 0.27, bbase - h * 0.85, w * 0.18, h * 0.85);
        // Heavy Crossbeam Lintel
        ctx.fillRect(bx - w * 0.55, bbase - h * 0.92, w * 1.10, h * 0.14);
        // Tiled Gate Canopy Roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.65, bbase - h * 0.92);
        ctx.lineTo(bx, bbase - h * 1.18);
        ctx.lineTo(bx + w * 0.65, bbase - h * 0.92);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#423f4c' : '#4d463b';
        ctx.fill();
        // Gu Yue Red Clan Banner
        ctx.fillStyle = pal.red;
        ctx.fillRect(bx - w * 0.40, bbase - h * 0.74, w * 0.10, h * 0.35);

      } else if (bldg.type === 'tower') {
        // ── Perimeter Lookout Watchtower ──
        // 4 Timber Stilts
        ctx.fillStyle = pal.dark ? '#26242a' : '#3a352e';
        ctx.fillRect(bx - w * 0.35, bbase - h * 0.75, w * 0.12, h * 0.75);
        ctx.fillRect(bx + w * 0.23, bbase - h * 0.75, w * 0.12, h * 0.75);
        // Elevated Lookout Deck
        ctx.fillRect(bx - w * 0.45, bbase - h * 0.82, w * 0.90, h * 0.10);
        // Conical Thatched / Tiled Roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.52, bbase - h * 0.82);
        ctx.lineTo(bx, bbase - h * 1.15);
        ctx.lineTo(bx + w * 0.52, bbase - h * 0.82);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3c3945' : '#4e463a';
        ctx.fill();
        // Beacon Brazier / Fire
        var bg = ctx.createRadialGradient(bx, bbase - h * 0.78, 0, bx, bbase - h * 0.78, w * 0.6);
        bg.addColorStop(0, 'rgba(235, 130, 45, 0.75)');
        bg.addColorStop(1, 'rgba(235, 130, 45, 0)');
        ctx.fillStyle = bg;
        ctx.beginPath(); ctx.arc(bx, bbase - h * 0.78, w * 0.6, 0, 6.2832); ctx.fill();

      } else {
        // ── Terraced Village Cottages & Stilt Homes ──
        // Stone foundation footing
        ctx.fillStyle = pal.dark ? '#1e1f26' : '#575249';
        ctx.fillRect(bx - w * 0.45, bbase - h * 0.18, w * 0.90, h * 0.18);
        // Timber walls
        ctx.fillStyle = pal.dark ? '#272630' : '#423d34';
        ctx.fillRect(bx - w * 0.40, bbase - h * 0.65, w * 0.80, h * 0.47);
        // Flared roof
        ctx.beginPath();
        ctx.moveTo(bx - w * 0.56, bbase - h * 0.65);
        ctx.lineTo(bx, bbase - h * 1.05);
        ctx.lineTo(bx + w * 0.56, bbase - h * 0.65);
        ctx.closePath();
        ctx.fillStyle = pal.dark ? '#3b3a45' : '#544c41';
        ctx.fill();
        // Warm amber window
        ctx.fillStyle = 'rgba(235, 175, 55, 0.82)';
        ctx.fillRect(bx - w * 0.18, bbase - h * 0.52, w * 0.36, h * 0.22);
        // Porch lantern
        var plg = ctx.createRadialGradient(bx - w * 0.28, bbase - h * 0.42, 0, bx - w * 0.28, bbase - h * 0.42, w * 0.45);
        plg.addColorStop(0, 'rgba(235, 175, 55, 0.60)');
        plg.addColorStop(1, 'rgba(235, 175, 55, 0)');
        ctx.fillStyle = plg;
        ctx.beginPath(); ctx.arc(bx - w * 0.28, bbase - h * 0.42, w * 0.45, 0, 6.2832); ctx.fill();
      }

      ctx.restore();
    }
  };

  // ── Subterranean Spirit Spring & River of Light (地下灵泉与觉醒光河) ─────────
  World.prototype.drawSubterraneanCavern = function (pal, clock) {
    var ctx = this.ctx, i;
    // The river of light flows through the cavern beneath the village
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
      if (rp.z > 1) projectedRiver.push(rp);
    }
    if (projectedRiver.length >= 2) {
      ctx.save();
      // Flowing luminous river surface
      ctx.beginPath();
      ctx.moveTo(projectedRiver[0].x - projectedRiver[0].f * 0.05, projectedRiver[0].y);
      for (i = 1; i < projectedRiver.length; i++) {
        ctx.lineTo(projectedRiver[i].x - projectedRiver[i].f * 0.06, projectedRiver[i].y);
      }
      for (i = projectedRiver.length - 1; i >= 0; i--) {
        ctx.lineTo(projectedRiver[i].x + projectedRiver[i].f * 0.06, projectedRiver[i].y);
      }
      ctx.closePath();
      var rlg = ctx.createLinearGradient(projectedRiver[0].x, projectedRiver[0].y, projectedRiver[projectedRiver.length - 1].x, projectedRiver[projectedRiver.length - 1].y);
      rlg.addColorStop(0, 'rgba(80, 200, 240, 0.75)');
      rlg.addColorStop(0.5, 'rgba(120, 230, 200, 0.85)');
      rlg.addColorStop(1, 'rgba(235, 195, 75, 0.80)');
      ctx.fillStyle = rlg;
      ctx.fill();

      // River glow aura
      ctx.lineWidth = Math.max(3, projectedRiver[0].f * 0.08);
      ctx.strokeStyle = 'rgba(100, 220, 240, 0.35)';
      ctx.stroke();

      // Floating Hope Gu starlight motes (希望蛊光点) drifting along the current
      var t = (clock || 0) * 0.001;
      for (var gi = 0; gi < 12; gi++) {
        var frac = (t * 0.08 + gi * 0.083) % 1.0;
        var idx = Math.floor(frac * (riverPts.length - 1));
        var subFrac = (frac * (riverPts.length - 1)) - idx;
        var pA = riverPts[idx], pB = riverPts[idx + 1];
        var gx = pA[0] + (pB[0] - pA[0]) * subFrac + Math.sin(t * 1.5 + gi) * 0.04;
        var gy = pA[1] + (pB[1] - pA[1]) * subFrac + 0.12 + Math.abs(Math.sin(t * 2.0 + gi * 0.7)) * 0.18;
        var gz = pA[2] + (pB[2] - pA[2]) * subFrac;
        var gp = project(gx, gy, gz);
        if (gp.z > 1) {
          var gr = Math.max(1.8, gp.f * 0.022);
          var gg = ctx.createRadialGradient(gp.x, gp.y, 0, gp.x, gp.y, gr * 2.2);
          gg.addColorStop(0, '#ffffff');
          gg.addColorStop(0.35, 'rgba(100, 230, 255, 0.9)');
          gg.addColorStop(1, 'rgba(100, 230, 255, 0)');
          ctx.fillStyle = gg;
          ctx.beginPath(); ctx.arc(gp.x, gp.y, gr * 2.2, 0, 6.2832); ctx.fill();
        }
      }
      ctx.restore();
    }
  };

  World.prototype.drawFrontier = function (pal) {
    var ctx = this.ctx, i;
    var p = project(0, 0, 0);
    if (p.z < 1) return;
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
      if (bp.z < 1) continue;
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
      if (p.z < 1) continue;
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

    window.RIWorld = {
      setReach: function (n) { world.reach = n; },
      setPeople: function (list) { world.people = list || []; },
      zoom: function (d) { target.dist = Math.max(12, Math.min(70, target.dist + d)); },
      look: function (deg) { azBase = deg * Math.PI / 180; },
      vantage: function (name) {
        var presets = {
          'overview': { tx: 0, tz: 0, ty: 1.1, dist: 40, az: 0.62, pitch: 0.30 },
          'village':  { tx: 0.45, tz: 1.25, ty: 1.45, dist: 16, az: 0.85, pitch: 0.24 },
          'hall':     { tx: -0.35, tz: 2.30, ty: 2.15, dist: 11, az: 0.35, pitch: 0.18 },
          'bai':      { tx: 3.40, tz: -1.80, ty: 3.80, dist: 13, az: 2.15, pitch: 0.25 },
          'cavern':   { tx: 0.25, tz: 1.85, ty: 0.65, dist: 12, az: 1.15, pitch: 0.15 }
        };
        var p = presets[name] || presets['overview'];
        target.tx = p.tx; target.tz = p.tz; target.ty = p.ty; target.dist = p.dist;
        target.az = p.az; target.pitch = p.pitch;
      },
      focus: function (x, z) {
        target.tx = x; target.tz = z;
        target.ty = heightAt(x, z) + 0.35;
        target.dist = 14;
      },
      reset: function () {
        target.tx = 0; target.tz = 0;
        target.ty = 1.1;
        target.dist = 40;
        target.az = 0.62;
        target.pitch = 0.30;
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
          azBase += 0.0012;
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
        wk.el.style.opacity = wk.live && wk.z > 1 ? '1' : '0';
        wk.el.style.transform = 'translate(' + Math.round(wk.x) + 'px,' + Math.round(wk.y) + 'px)';
      }
      for (var k = 0; k < placed.length; k++) {
        var it = placed[k];
        var vis = it.z > 1 && it.x > -60 && it.x < world.w + 60 && it.y > -40 && it.y < world.h + 60;
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
      if (hint) hint.style.opacity = '0';
    });
    window.addEventListener('pointerup', function () { drag.on = false; });
    window.addEventListener('pointermove', function (e) {
      if (!drag.on) return;
      azBase = drag.az0 - (e.clientX - drag.x) * 0.006;
      pitchBase = Math.max(0.10, Math.min(0.60, drag.pitch0 + (e.clientY - drag.y) * 0.004));
    });
    canvas.addEventListener('wheel', function (e) {
      if (!canvas.getAttribute('data-zoom')) return;
      e.preventDefault();
      target.dist = Math.max(12, Math.min(70, target.dist + (e.deltaY > 0 ? 2.5 : -2.5)));
    }, { passive: false });
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
