// 인퍼런스 공장 — 건물 전체(building) / 한 층(floor) 3D와 안내판. three.js(CDN) 없이도 안내판은 동작한다.
const D = JSON.parse(document.getElementById('gf-data').textContent);
const F = D.floors, N = F.length, MODE = D.mode, PAGE = D.page;
const $ = id => document.getElementById(id);
const SC = { done: '#5ee39c', kept: '#82b8ff', wip: '#f1b646', plan: '#4a4e6a' };
const KO = D.statusKo, KIND = { textbook: '교재', article: '논문', special: '부록' };
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
const open = st => st !== 'plan';

// 역 번호: 층 모드에서는 이 페이지 기계가 1번부터, 나머지는 그 뒤
const NUM = F.map(f => {
  const ord = MODE === 'floor' && f.i === D.focus ? [...f.stations.keys()].sort((a, b) => (f.stations[b].page === PAGE) - (f.stations[a].page === PAGE) || a - b) : [...f.stations.keys()];
  const n = []; ord.forEach((k, j) => n[k] = j + 1); return n;
});
function href(s) {
  if (!open(s.st)) return null;
  if (MODE === 'floor' && s.page === PAGE) return '#' + (s.sec || 'top');
  return D.base + s.page + '/' + (s.sec ? '#' + s.sec : '');
}

// ---------------- 안내판 ----------------
let sel = MODE === 'floor' ? D.focus : -1;
const m0 = /^#f(\d+)$/.exec(location.hash); if (MODE === 'building' && m0 && +m0[1] < N) sel = +m0[1];
let three = null;

function stationItems(f, onlyNums) {
  const ks = [...f.stations.keys()].sort((a, b) => NUM[f.i][a] - NUM[f.i][b]);
  let out = '', sep = false;
  ks.forEach(k => {
    const s = f.stations[k], h = href(s), mine = MODE !== 'floor' || s.page === PAGE;
    if (MODE === 'floor' && !mine && !sep) { out += '<li class="sep">같은 층의 다른 해설</li>'; sep = true; }
    const pg = (F[f.i].pages.find(p => p.folder === s.page) || {});
    const inner = '<span class="no">' + NUM[f.i][k] + '</span><span><b>' + esc(s.name) + '</b><span class="d">' + esc(s.desc) + '</span>' +
      (MODE === 'floor' && mine ? '' : '<small>' + esc((KIND[pg.kind] || '') + ' · ' + (pg.label || '') + ' · ' + (KO[s.st] || '')) + '</small>') + '</span>';
    out += '<li data-k="' + k + '" class="' + (mine ? '' : 'other') + '" style="--c:' + f.col + '">' + (h ? '<a href="' + esc(h) + '">' + inner + '</a>' : '<button type="button" aria-disabled="true">' + inner + '</button>') + '</li>';
  });
  return out;
}
function bindHot(root) {
  root.querySelectorAll('li[data-k]').forEach(li => {
    li.addEventListener('mouseenter', () => three && three.hot(+li.dataset.k));
    li.addEventListener('mouseleave', () => three && three.hot(-1));
    li.addEventListener('focusin', () => three && three.hot(+li.dataset.k));
  });
}
function say(t) { const e = $('gf-say'); if (e) e.innerHTML = t; }

function renderLift() {
  const L = $('gf-lift'); if (!L) return;
  L.innerHTML = F.slice().reverse().map(f => '<button type="button" data-i="' + f.i + '" aria-pressed="' + (f.i === sel) + '" style="--c:' + f.col + '"><span class="n">' + f.fl +
    '</span><span>' + esc(f.name) + '<br><span class="w">' + (f.week ? f.week + '주차 · ' : '') + esc(f.chap) + '</span></span><span class="gf-dot" style="background:' + SC[f.st] + '" title="' + esc(KO[f.st]) + '"></span></button>').join('');
  L.querySelectorAll('button').forEach(b => b.addEventListener('click', () => select(+b.dataset.i === sel ? -1 : +b.dataset.i)));
}
function renderInfo() {
  const I = $('gf-info'); if (!I) return;
  if (sel < 0) {
    const openN = F.filter(f => open(f.st)).length, pages = F.reduce((a, f) => a + f.pages.filter(p => open(p.st)).length, 0);
    I.innerHTML = '<h3>건물 안내</h3><p>' + N + '개 층(본편 10층 + 옥상) 중 <b>' + openN + '개 층</b>에 불이 켜졌고, 지금 열 수 있는 해설은 <b>' + pages + '편</b>입니다.</p>' +
      '<p>층 = 주차 · 오른쪽 색 띠 = 책의 장. 같은 장을 두 주에 나눠 읽는 2장 · 5장 · 7장은 두 층에 걸쳐 있어요. 토큰(빛 알갱이)은 1층 정문에서 들어와 층을 하나씩 지나 위로 올라갑니다.</p>';
    say('어서 오세요. 엘리베이터 버튼이나 건물의 층을 누르면 그 층의 공정과 해설을 안내해 드려요. 불이 켜진 층은 지금 읽을 수 있고, 회색 층은 공사 중이에요.');
    return;
  }
  const f = F[sel];
  I.innerHTML = '<h3>' + f.fl + ' ' + esc(f.name) + '</h3><span class="chip">' + (f.week ? f.week + '주차' : '부록') + '</span><span class="chip" style="border-color:' + f.col + '">' + esc(f.chap) +
    '</span><span class="chip"><span class="gf-dot" style="background:' + SC[f.st] + '"></span>' + esc(KO[f.st]) + '</span>' +
    '<p style="color:#f1b646">' + esc(f.process) + '</p><p>' + esc(f.desc) + '</p><div class="gf-pages">' +
    f.pages.map(p => (open(p.st) ? '<a class="gf-pg" href="' + esc(D.base + p.folder + '/') + '">' : '<div class="gf-pg plan">') + '<b>' + (KIND[p.kind] || '') + ' · ' + esc(p.label) + '</b> ' + esc(p.title) +
      '<small>' + esc(p.range) + (p.range ? ' · ' : '') + esc(KO[p.st]) + (open(p.st) ? ' · 해설 열기 →' : '') + '</small>' + (open(p.st) ? '</a>' : '</div>')).join('') +
    '</div><p style="margin-bottom:0"><b>이 층의 기계</b> <span style="color:#9d9bb8;font-size:12px">번호 = 3D 위 번호</span></p><ol class="gf-st">' + stationItems(f) + '</ol>';
  bindHot(I);
  say(f.fl + ' <b>' + esc(f.name) + '</b>입니다. ' + esc(f.process) + '. ' + (open(f.st) ? '불이 켜진 해설 ' + f.pages.filter(p => open(p.st)).length + '편을 지금 열 수 있어요. 기계를 누르면 그 칸으로 바로 갑니다.' : '아직 공사 중인 층이에요. 해설이 완성되면 불이 켜집니다.'));
}
function select(i) {
  sel = i;
  if (MODE === 'building') {
    renderLift(); renderInfo();
    try { history.replaceState(null, '', i < 0 ? location.pathname + location.search : '#f' + i); } catch (e) {}
  }
  three && three.select(i);
}
function renderFloorPanel() {
  const f = F[D.focus], S = $('gf-st');
  if (S) { S.innerHTML = stationItems(f); bindHot(S); }
  const M = $('gf-mini');
  if (M) M.innerHTML = '<span class="t">건물 속 위치</span><span class="bar">' + F.map(g => '<i class="' + (g.i === f.i ? 'on' : '') + '" style="--c:' + g.col + '" title="' + g.fl + ' ' + esc(g.name) + '">' + g.fl + '</i>').join('') + '</span><small>' + f.fl + ' ' + esc(f.name) + ' · 같은 색 = ' + esc(f.chap) + '</small>';
}
if (MODE === 'building') { renderLift(); renderInfo(); $('gf-all') && $('gf-all').addEventListener('click', () => select(-1)); window.addEventListener('hashchange', () => { const m = /^#f(\d+)$/.exec(location.hash); if (m && +m[1] < N && +m[1] !== sel) select(+m[1]); }); }
else renderFloorPanel();

// ---------------- 3D ----------------
try { three = await initThree(); } catch (e) { console.error(e); $('gf-err').style.display = 'flex'; const h = $('gf-hint'); if (h) h.style.display = 'none'; }

async function initThree() {
  const THREE = await import('three');
  const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
  const host = $('gf-cv'), LBL = $('gf-labels');
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#101119');
  const FW = 20, FD = 8, H = 3.4, GAP = MODE === 'floor' ? 2.4 : 3.2, WALL = 2.6;
  const cam = new THREE.OrthographicCamera(-10, 10, 10, -10, 0.1, 600);
  const DIR = new THREE.Vector3(1, .78, 1.3).normalize();
  const controls = new OrbitControls(cam, renderer.domElement);
  const AZ = Math.atan2(DIR.x, DIR.z);
  Object.assign(controls, { enableDamping: true, enablePan: false, minAzimuthAngle: AZ - .75, maxAzimuthAngle: AZ + .75, minPolarAngle: .45, maxPolarAngle: 1.32, minZoom: .6, maxZoom: 4 });
  cam.position.copy(DIR).multiplyScalar(120); controls.target.set(0, 0, 0); controls.update();

  scene.add(new THREE.HemisphereLight('#dfe2ff', '#22253a', 1.35));
  scene.add(new THREE.AmbientLight('#ffffff', .18));
  const sun = new THREE.DirectionalLight('#fff1dc', 1.75); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -26, right: 26, top: 26, bottom: -26, near: 1, far: 160 }); sun.shadow.bias = -.0006;
  scene.add(sun, sun.target);

  // 땅
  const ground = new THREE.Mesh(new THREE.BoxGeometry(64, .4, 44), new THREE.MeshStandardMaterial({ color: '#171927', roughness: .95 }));
  ground.position.set(2, -.5, 2); ground.receiveShadow = true; scene.add(ground);
  const grid = new THREE.GridHelper(64, 32, '#262a40', '#1f2234'); grid.position.set(2, -.29, 2); scene.add(grid);
  const road = new THREE.Mesh(new THREE.BoxGeometry(5, .05, 14), new THREE.MeshStandardMaterial({ color: '#23263a' })); road.position.set(-7, -.27, 11); scene.add(road);

  const grey = new THREE.Color('#3b3f5a');
  const pick = [], spin = [], blink = [], floors = [];
  let fadeOn = false;

  function buildFloor(f) {
    const g = new THREE.Group(); scene.add(g);
    const ghost = !open(f.st) && f.fl !== 'RF' ? true : f.fl === 'RF';
    const fade = MODE === 'floor' && f.i !== D.focus;
    const mats = [];
    const M = (c, o = {}) => { const col = new THREE.Color(c); if (ghost) col.lerp(grey, .55); const m = new THREE.MeshStandardMaterial({ color: col, roughness: .7, metalness: .08, ...o }); mats.push(m); return m; };
    const G = (c, k = .8, op) => { if (ghost) return M(c); const m = new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: k, roughness: .4, ...(op ? { transparent: true, opacity: op } : {}) }); mats.push(m); return m; };
    const add = (geo, mat, x, y, z, p) => { const m = new THREE.Mesh(geo, typeof mat === 'string' ? M(mat) : mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; p.add(m); return m; };
    const kit = p => ({
      box: (w, h, d, c, x, y, z) => add(new THREE.BoxGeometry(w, h, d), c, x, y, z, p),
      cyl: (rt, rb, h, c, x, y, z, s = 18) => add(new THREE.CylinderGeometry(rt, rb, h, s), c, x, y, z, p),
      sph: (r, c, x, y, z) => add(new THREE.SphereGeometry(r, 18, 14), c, x, y, z, p),
      hemi: (r, c, x, y, z) => add(new THREE.SphereGeometry(r, 22, 12, 0, Math.PI * 2, 0, Math.PI / 2), c, x, y, z, p),
      tor: (r, t, c, x, y, z) => add(new THREE.TorusGeometry(r, t, 8, 24), c, x, y, z, p), M, G
    });
    const B = kit(g);
    const roof = f.fl === 'RF';
    // 바닥판 · 벽 · 기둥
    const slab = B.box(FW, .3, FD, '#2a2d42', 0, -.15, 0); slab.userData.fl = f.i; pick.push(slab);
    const wallH = roof ? .7 : WALL;
    const wm = M('#23263a', { transparent: true, opacity: .92 });
    B.box(FW, wallH, .14, wm, 0, wallH / 2, -FD / 2 + .07).userData.fl = f.i;
    B.box(.14, wallH, FD, wm, -FW / 2 + .07, wallH / 2, 0).userData.fl = f.i;
    if (roof) { B.box(FW, .7, .14, wm, 0, .35, FD / 2 - .07); B.box(.14, .7, FD, wm, FW / 2 - .07, .35, 0); }
    else {
      // 창 띠 (불 켜진 층)
      const lit = open(f.st);
      B.box(FW - .6, .34, .04, lit ? G(SC[f.st], .55) : M('#30344c'), 0, WALL - .45, -FD / 2 + .16);
      B.box(.04, .34, FD - .6, lit ? G(SC[f.st], .55) : M('#30344c'), -FW / 2 + .16, WALL - .45, 0);
      [[FW / 2 - .15, FD / 2 - .15], [-FW / 2 + .15, FD / 2 - .15], [FW / 2 - .15, -FD / 2 + .15]].forEach(([x, z]) => B.box(.3, H - .3, .3, '#4a4f6e', x, (H - .3) / 2, z));
      // 장 색 띠 (오른쪽 뒤 기둥)
      const band = B.box(.34, H - .3, .34, new THREE.MeshStandardMaterial({ color: f.col, emissive: f.col, emissiveIntensity: lit ? .55 : .12 }), FW / 2 - .15, (H - .3) / 2, -FD / 2 + .15); mats.push(band.material);
    }
    // 앞 난간 불빛
    const rail = B.box(FW, .08, .08, open(f.st) ? G(SC[f.st], 1) : M('#555a74'), 0, .05, FD / 2 - .04);
    // 컨베이어 (토큰 길)
    if (!roof) { B.box(FW - 1.2, .1, .9, '#1b1d2b', 0, .05, 2.4); }
    // 공사 중 표시
    if (!open(f.st) && !roof) {
      for (let k = 0; k < 9; k++) { const bar = B.box(1.6, .12, .08, k % 2 ? '#1b1d2b' : new THREE.MeshStandardMaterial({ color: '#f1b646', emissive: '#f1b646', emissiveIntensity: .25 }), -8 + k * 2, .75, FD / 2 - .25); if (bar.material.emissive) mats.push(bar.material); }
      [-8.8, 8.8].forEach(x => B.box(.12, 1.6, .12, '#6c7192', x, .8, FD / 2 - .25));
    }
    // 기계
    const n = f.stations.length, sp = (FW - 3) / n, sc = Math.min(1, (sp - .25) / 2.4);
    const sts = f.stations.map((s, k) => {
      const sg = new THREE.Group(); sg.position.set(-FW / 2 + 1.6 + sp * (k + .5), 0, -.9); sg.scale.setScalar(sc); g.add(sg);
      (MK[s.type] || MK.box)(kit(sg), s);
      sg.traverse(o => { if (o.isMesh) { o.userData.fl = f.i; o.userData.st = k; pick.push(o); } });
      return { g: sg, top: 2.5 * sc, s };
    });
    if (fade) mats.forEach(m => { m.transparent = true; m.opacity = (m.opacity ?? 1) * .14; m.depthWrite = false; });
    if (fade) g.traverse(o => { if (o.isMesh) { o.castShadow = false; if (o.material && !mats.includes(o.material)) { o.material.transparent = true; o.material.opacity = .14; o.material.depthWrite = false; } } });
    const outline = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(FW + .3, .5, FD + .3)), new THREE.LineBasicMaterial({ color: f.col, transparent: true, opacity: 0 }));
    outline.position.y = -.1; g.add(outline);
    return { g, f, sts, y: 0, outline, delay: f.i * .09 };
  }

  // ---- 기계 모양 ----
  const PI = Math.PI;
  const legs = (b, w, d, h, c = '#4a4f6e') => [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([a, e]) => b.box(.08, h, .08, c, a * (w / 2 - .08), h / 2, e * (d / 2 - .08)));
  const MK = {
    box: b => b.box(1.4, 1.2, 1.2, '#5d6386', 0, .6, 0),
    door: b => { b.box(.3, 2.2, .3, '#8a8fa8', -1, 1.1, 0); b.box(.3, 2.2, .3, '#8a8fa8', 1, 1.1, 0); b.box(2.4, .35, .4, '#b07cff', 0, 2.3, 0); b.box(1.7, 1.9, .06, b.G('#82b8ff', .5, .55), 0, .98, 0); ['#ff86b8', '#5ee39c', '#f1b646'].forEach((c, i) => b.box(.32, .32, .32, c, -.6 + i * .6, .16, 1.0)); },
    scale: b => { b.cyl(.35, .45, .2, '#555a74', 0, .1, 0); b.cyl(.07, .07, 1.9, '#a7abc4', 0, 1.05, 0); b.box(2.2, .08, .08, '#d6d9ea', 0, 2.0, 0); b.box(.08, .08, .7, '#d6d9ea', 0, 2.0, .35);
      [[-1, 0, '#82b8ff'], [1, 0, '#5ee39c'], [0, .7, '#f1b646']].forEach(([x, z, c]) => { b.cyl(.015, .015, .55, '#a7abc4', x, 1.72, z); b.cyl(.34, .24, .08, c, x, 1.42, z); }); },
    twin: b => { b.box(.95, 1.7, 1.3, '#4a4f6e', -.65, .85, 0); b.box(.95, 1.05, 1.3, '#d6d9ea', .65, .52, 0); b.box(.6, .16, .02, b.G('#5ee39c', .8), .65, .75, .66); b.box(.6, .16, .02, b.G('#b07cff', .5), -.65, 1.3, .66); b.box(.5, .08, .12, b.G('#f1b646', .9), 0, 1.15, 0); },
    board: b => { b.cyl(.05, .05, 1.2, '#8a8fa8', -.8, .6, 0); b.cyl(.05, .05, 1.2, '#8a8fa8', .8, .6, 0); b.box(1.9, 1.25, .08, '#2a2e45', 0, 1.65, 0); ['#b07cff', '#82b8ff', '#5ee39c'].forEach((c, k) => b.box(1.65, .28, .02, b.G(c, .55), 0, 1.25 + k * .38, .05)); },
    desk: b => { b.box(2, .1, 1.1, '#8a6f55', 0, .8, 0); legs(b, 2, 1.1, .78); b.box(1.2, .02, .8, b.G('#82b8ff', .35), -.2, .86, 0); b.cyl(.03, .03, .6, '#ccc', .75, 1.15, -.35); b.sph(.1, b.G('#f1b646', 1), .75, 1.47, -.3); },
    gauge: b => { b.box(1.6, 1.3, .6, '#3d425e', 0, .65, 0); [-.4, .4].forEach((x, i) => { const d = b.cyl(.36, .36, .06, '#eceaf3', x, .85, .31); d.rotation.x = PI / 2; const nd = b.box(.04, .3, .02, '#ef5b5b', x, .92, .36); nd.rotation.z = i ? -.7 : .5; }); b.box(1.2, .16, .02, b.G('#5ee39c', .7), 0, .3, .31); },
    screen: b => { b.box(.8, .08, .5, '#555a74', 0, .04, 0); b.cyl(.08, .08, 1.1, '#777c96', 0, .6, 0); b.box(2.1, 1.25, .12, '#1b1d2b', 0, 1.65, 0); [.3, .55, .4, .75, .6].forEach((h, k) => b.box(.24, h, .02, b.G(['#5ee39c', '#82b8ff', '#ff86b8', '#f1b646', '#b07cff'][k], .7), -.7 + k * .35, 1.15 + h / 2, .07)); },
    conveyor: b => { b.box(2.3, .12, .8, '#2a2d3f', 0, .6, 0); legs(b, 2.2, .7, .55); b.box(.6, .7, .7, '#5d6386', -.85, 1.0, 0); ['#ff86b8', '#82b8ff', '#f1b646'].forEach((c, k) => b.box(.25, .25, .25, c, -.2 + k * .4, .8, 0)); b.box(.3, .3, .3, b.G('#5ee39c', .9), .95, .82, 0); },
    press: b => { b.box(1.8, .3, .9, '#3d425e', 0, .15, 0); [-.8, .8].forEach(x => b.box(.2, 2, .2, '#6c7192', x, 1, 0)); b.box(1.9, .3, .6, '#6c7192', 0, 2.05, 0); b.box(1.0, .35, .5, '#a7abc4', 0, 1.45, 0); b.cyl(.08, .08, .5, '#a7abc4', 0, 1.8, 0);
      for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) b.box(.2, .12, .2, b.G((i + j) % 2 ? '#5ee39c' : '#82b8ff', .5), -.3 + i * .3, .36, -.3 + j * .3); },
    layers: b => { [-.6, .0].forEach(x => b.cyl(.04, .04, 1.9, '#8a8fa8', x - .5, .95, -.45)); for (let k = 0; k < 4; k++) b.box(1.5, .08, 1.0, b.G('#5ee39c', .25, .7), -.4, .45 + k * .42, 0); b.box(.6, 1.8, .6, '#3d425e', .85, .9, 0); for (let k = 0; k < 4; k++) b.box(.4, .26, .4, b.G('#f1b646', .6), .85, .35 + k * .38, .32); },
    split: b => { b.box(.6, .6, .6, '#b07cff', 0, .3, .55); [-.9, -.3, .3, .9].forEach((x, i) => { b.box(.45, .75, .45, i === 1 || i === 2 ? b.G('#5ee39c', .45) : '#4a4f6e', x, .38, -.45); b.box(.06, .06, .7, '#8a8fa8', x * .5, .55, .05).rotation.y = -x * .6; }); },
    lamp: b => { b.box(2, .08, 1, '#3d425e', 0, .7, 0); legs(b, 2, 1, .68); b.box(1.4, .02, .7, '#eceaf3', 0, .75, 0); b.box(1.0, .022, .12, b.G('#f1b646', .7), -.1, .765, -.12); b.box(.7, .022, .12, b.G('#f1b646', .7), .05, .765, .15); const p = b.box(.12, .6, .12, '#f1b646', .7, 1.0, .25); p.rotation.z = .6; },
    heads: b => { b.box(1.9, .12, .55, '#3d425e', 0, .06, 0); ['#f1b646', '#ff86b8', '#5ee39c', '#82b8ff'].forEach((c, k) => { b.cyl(.13, .13, 1.3, c, -.66 + k * .44, .78, 0); b.cyl(.14, .14, .26, '#eceaf3', -.66 + k * .44, 1.5, 0); }); },
    kitchen: b => { b.box(.9, .9, .8, '#5d6386', -.55, .45, -.1); b.cyl(.18, .18, .03, b.G('#ef5b5b', .9), -.55, .92, -.1); b.cyl(.17, .21, .6, '#eceaf3', -.55, .3, .62); b.sph(.16, '#f1d9c2', -.55, .76, .62); b.cyl(.13, .13, .2, '#ffffff', -.55, .96, .62); b.box(.7, 1.7, .7, '#a7abc4', .75, .85, -.1); b.box(.62, .09, .09, b.G('#82b8ff', .7), .12, .72, -.1); },
    denoise: b => { b.box(2.2, .1, .35, '#3d425e', 0, .5, 0); legs(b, 2.1, .3, .48); ['#6b6f87', '#8a7a96', '#b07cb0', '#e08cc4', '#ff86b8'].forEach((c, k) => b.box(.36, .55, .05, k > 2 ? b.G(c, .35) : c, -.84 + k * .42, .85, 0)); },
    roofline: b => { b.cyl(.05, .05, 1, '#8a8fa8', -.85, .5, 0); b.cyl(.05, .05, 1, '#8a8fa8', .85, .5, 0); b.box(2, 1.3, .08, '#1b1d2b', 0, 1.5, 0); b.box(1.8, .03, .02, '#6c7192', 0, .95, .05); b.box(.03, 1.1, .02, '#6c7192', -.9, 1.45, .05);
      const s = b.box(1.03, .06, .03, b.G('#5ee39c', 1), -.45, 1.25, .06); s.rotation.z = .507; b.box(.9, .06, .03, b.G('#ef5b5b', 1), .45, 1.5, .06); b.sph(.08, b.G('#f1b646', 1), .15, 1.3, .08); },
    pipe: b => { b.cyl(.45, .45, 1.3, '#a7abc4', -.75, .65, 0); b.cyl(.45, .45, 1.3, '#a7abc4', .75, .65, 0); const p = b.cyl(.15, .15, .7, b.G('#5ee39c', .5), 0, .95, 0); p.rotation.z = PI / 2; const q = b.cyl(.06, .06, 1.6, '#555a74', 0, 1.55, 0); q.rotation.z = PI / 2; },
    warehouse: b => { b.box(1.1, 1.9, 1.1, '#5d6386', -.55, .95, -.15); b.box(.7, .02, 1.12, '#82b8ff', -.55, 1.5, -.15); b.box(.65, .65, .65, b.G('#5ee39c', .5), .72, .33, .3); b.box(.7, .06, .25, '#2a2d3f', .15, .2, .3); [0, .2].forEach(x => b.box(.14, .14, .14, '#f1b646', x + .05, .3, .3)); },
    tiles: b => { b.box(1.9, .1, 1.2, '#3d425e', 0, .7, 0); legs(b, 1.9, 1.2, .68); for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) b.box(.5, .05, .32, b.G(i === 1 && j === 1 ? '#f1b646' : (i + j) % 2 ? '#5ee39c' : '#82b8ff', .45), -.6 + i * .6, .78, -.38 + j * .38); },
    rack: b => { [-.5, .5].forEach(x => { b.box(.8, 2.1, .8, '#2b2f45', x, 1.05, 0); for (let k = 0; k < 6; k++) b.box(.6, .06, .02, b.G('#5ee39c', .9), x, .35 + k * .3, .41); }); },
    tower: b => { b.box(1.6, .12, 1.2, '#3d425e', 0, .06, 0); [[-.4, -.3], [.4, -.3], [-.4, .3], [.4, .3]].forEach(([x, z]) => { b.cyl(.22, .22, 1.5, '#82b8ff', x, .87, z); for (let k = 0; k < 3; k++) b.tor(.23, .03, b.G('#57d0dc', .6), x, .5 + k * .4, z).rotation.x = PI / 2; }); },
    shelf: b => { [-.95, .95].forEach(x => b.box(.06, 2, .6, '#6c7192', x, 1, 0)); [.5, 1.1, 1.7].forEach((y, k) => { b.box(1.9, .06, .6, '#6c7192', 0, y, 0); [.3, .4, .5].forEach((s, j) => b.box(s - k * .06, .1, s - k * .06, b.G(['#82b8ff', '#57d0dc', '#5ee39c'][k], .4), -.55 + j * .55, y + .08, 0)); }); },
    cells: b => { b.box(2.1, .08, 1.1, '#3d425e', 0, .04, 0); [-1, -.33, .33, 1].forEach(x => b.box(.05, 1.2, 1.1, b.M('#8a8fa8', { transparent: true, opacity: .55 }), x, .64, 0)); [-.66, 0, .66].forEach(x => { b.box(.4, .95, .4, '#2b2f45', x, .55, 0); b.box(.3, .05, .02, b.G('#5ee39c', .9), x, .8, .21); }); },
    chip: b => { b.box(1.6, .3, 1.4, '#3d425e', 0, .15, 0); b.box(1.2, .14, 1.0, '#2b2f45', -.1, .37, 0); b.box(.55, .06, .55, b.G('#57d0dc', .7), -.1, .47, 0); b.box(.35, .35, .35, '#ef5b5b', .75, .48, .45); b.box(.3, .3, .3, '#f1b646', .75, .46, -.4); },
    laptop: b => { b.box(1.4, .08, .8, '#8a6f55', 0, .75, 0); legs(b, 1.4, .8, .72); b.box(.75, .04, .45, '#a7abc4', 0, .81, .05); const s = b.box(.75, .46, .03, b.G('#82b8ff', .5), 0, 1.05, -.18); s.rotation.x = -.2; },
    panel: b => { b.box(1.7, 1.9, .4, '#3d425e', 0, .95, -.1); [-.5, -.17, .17, .5].forEach(x => b.box(.05, 1.4, .02, b.G('#57d0dc', .9), x, 1.0, .11)); [.5, 1.0, 1.5].forEach(y => b.box(1.2, .04, .02, b.G('#57d0dc', .6), 0, y, .11)); },
    wall: b => { b.box(2, 1.6, .08, '#5d6386', 0, 1.2, -.3); b.cyl(.05, .05, 1.2, '#8a8fa8', -.9, .6, -.3); b.cyl(.05, .05, 1.2, '#8a8fa8', .9, .6, -.3); ['#ef5b5b', '#f1b646', '#5ee39c', '#82b8ff', '#b07cff', '#ff86b8'].forEach((c, k) => b.box(.22, .45 + (k % 3) * .12, .1, c, -.7 + k * .28, 1.25, -.22)); },
    turbine: b => { b.box(1.9, .3, .9, '#3d425e', 0, .15, 0); const c = b.cyl(.5, .5, 1.6, '#a7abc4', 0, .85, 0); c.rotation.z = PI / 2; [-.5, 0, .5].forEach(x => b.tor(.52, .05, '#5d6386', x, .85, 0).rotation.y = PI / 2); const fan = b.cyl(.44, .44, .06, b.G('#57d0dc', .7), .82, .85, 0); fan.rotation.z = PI / 2; const bl = b.box(.04, .8, .14, '#eceaf3', .86, .85, 0); spin.push([bl, 'x', 3]); },
    hub: b => { b.cyl(.08, .08, 1, '#8a8fa8', 0, .5, 0); b.sph(.35, b.G('#57d0dc', .6), 0, 1.1, 0); [[-.8, -.4], [.8, -.4], [-.8, .4], [.8, .4]].forEach(([x, z]) => { b.box(.36, .36, .36, '#5d6386', x, .18, z); const a = b.box(Math.hypot(x, z), .05, .05, '#8a8fa8', x / 2, .65, z / 2); a.rotation.y = -Math.atan2(z, x); a.rotation.z = .5 * Math.sign(x); }); },
    load: b => { b.box(1.9, .2, 1.1, '#3d425e', 0, .1, 0); [[-.6, 3], [-.15, 5], [.3, 2], [.75, 4]].forEach(([x, n]) => { for (let k = 0; k < n; k++) b.box(.32, .2, .32, k === n - 1 ? b.G('#f1b646', .5) : '#82b8ff', x, .3 + k * .22, 0); }); },
    drawers: b => { b.box(1.7, 1.7, .7, '#5d6386', 0, .85, 0); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) b.box(.34, .32, .03, (i * 3 + j) % 5 < 2 ? b.G('#f1b646', .6) : '#3d425e', -.6 + i * .4, .3 + j * .4, .36); },
    cache: b => { [-.95, .95].forEach(x => b.box(.06, 2, .7, '#6c7192', x, 1, 0)); [.4, 1.0, 1.6].forEach(y => { b.box(1.9, .06, .7, '#6c7192', 0, y, 0); for (let j = 0; j < 4; j++) b.box(.3, .3, .3, j % 3 ? b.G('#5ee39c', .55) : '#4a4f6e', -.6 + j * .4, y + .18, 0); }); },
    parallel: b => { [-.5, 0, .5].forEach((z, k) => { b.box(2.1, .08, .3, '#2a2d3f', 0, .55, z); b.box(.5, .3, .25, b.G(['#f1b646', '#5ee39c', '#82b8ff'][k], .45), -.3 + k * .35, .74, z); }); legs(b, 2, 1.2, .52); b.box(.5, .9, 1.4, '#5d6386', -1.0, .45, 0); },
    rooms: b => { b.box(.9, 1.3, 1.2, '#5d6386', -.6, .65, 0); b.box(.9, 1.3, 1.2, '#4a4f6e', .6, .65, 0); b.box(.5, .3, .02, b.G('#f1b646', .8), -.6, .9, .61); b.box(.5, .3, .02, b.G('#5ee39c', .8), .6, .9, .61); const p = b.cyl(.08, .08, .4, '#a7abc4', 0, 1.15, 0); p.rotation.z = PI / 2; },
    router: b => { b.box(.6, .6, .6, b.G('#f1b646', .3), -.6, .5, 0); [[.7, -.5], [.7, 0], [.7, .5]].forEach(([x, z], k) => { b.box(.36, .36, .36, ['#5ee39c', '#82b8ff', '#ff86b8'][k], x, .3, z); const t = b.box(Math.hypot(1.3, z), .06, .06, '#8a8fa8', .05, .45, z / 2); t.rotation.y = -Math.atan2(z, 1.3); }); },
    eye: b => { b.box(1.0, 1.0, .9, '#5d6386', .2, .5, 0); b.sph(.3, b.G('#82b8ff', .7), .2, .6, .45); b.box(.75, .55, .04, '#ff86b8', -.75, .9, .2).rotation.y = .4; b.cyl(.03, .03, .6, '#8a8fa8', -.75, .3, .2); },
    sorter: b => { [-.65, 0, .65].forEach((x, k) => { b.box(.5, .5, .6, '#3d425e', x, .25, 0); for (let j = 0; j < 3; j++) b.sph(.1, b.G(['#5ee39c', '#82b8ff', '#ff86b8'][k], .5), x - .12 + j * .12, .58, 0); }); },
    booth: b => { [-.5, .5].forEach((x, k) => { b.box(.85, 1.7, .85, b.G('#82b8ff', .1, .35), x, .85, 0); k ? b.cyl(.15, .2, .35, '#eceaf3', x, 1.0, 0) : b.sph(.15, b.G('#ff86b8', .6), x, 1.1, 0); b.cyl(.03, .03, .9, '#8a8fa8', x, .45, 0); }); },
    canvas: b => { [-.4, .4].forEach(x => { const l = b.box(.06, 1.6, .06, '#8a6f55', x, .8, 0); l.rotation.z = x > 0 ? -.12 : .12; }); const p = b.box(1.0, .75, .04, b.G('#ff86b8', .35), 0, 1.25, .05); p.rotation.x = -.12; b.box(1.0, .25, .03, '#2a2d3f', .2, .3, .5); for (let k = 0; k < 4; k++) b.box(.18, .16, .02, b.G('#f1b646', .4), -.12 + k * .22, .3, .52); },
    container: b => { [[-.55, .25, 0, '#ef5b5b'], [.55, .25, 0, '#82b8ff'], [0, .75, 0, '#f1b646']].forEach(([x, y, z, c]) => { b.box(1.05, .48, .55, c, x, y, z); for (let k = 0; k < 5; k++) b.box(.02, .4, .57, '#1b1d2b', x - .4 + k * .2, y, z); }); },
    servers: b => { [.6, .9, 1.2, 1.5].forEach((h, k) => { b.box(.38, h, .55, k < 2 ? '#2b2f45' : b.M('#2b2f45', { transparent: true, opacity: .7 }), -.66 + k * .44, h / 2, 0); b.box(.26, .05, .02, b.G('#5ee39c', k < 3 ? .9 : .2), -.66 + k * .44, h - .15, .28); }); },
    dispatcher: b => { b.cyl(.1, .1, .6, '#8a8fa8', 0, .3, 0); const d = b.cyl(.85, .85, .15, '#5d6386', 0, .65, 0); for (let k = 0; k < 6; k++) { const a = k / 6 * PI * 2; const c = new THREE.Mesh(new THREE.BoxGeometry(.22, .22, .22), b.G(['#5ee39c', '#82b8ff', '#f1b646'][k % 3], .5)); c.position.set(Math.cos(a) * .6, .18, Math.sin(a) * .6); d.add(c); } spin.push([d, 'y', .8]); },
    crane: b => { b.box(.16, 2.3, .16, '#f1b646', -.7, 1.15, 0); b.box(1.9, .1, .1, '#f1b646', .15, 2.3, 0); b.cyl(.015, .015, .8, '#cccccc', .75, 1.9, 0); b.box(.42, .3, .42, '#82b8ff', .75, 1.35, 0); [[.4, .45], [.75, .55], [1.0, .42]].forEach(([x, r]) => b.sph(r * .6, '#e8eaf6', x - .2, .35, .4)); },
    gate: b => { [-.9, .9].forEach(x => b.box(.2, 1.8, .2, '#6c7192', x, .9, 0)); b.box(2.0, .25, .25, '#5d6386', 0, 1.9, 0); b.sph(.12, b.G('#5ee39c', 1), -.3, 1.9, .15); b.sph(.12, b.G('#ef5b5b', .5), .3, 1.9, .15); const a = b.box(1.5, .08, .08, '#f1b646', .05, .7, .2); a.rotation.z = .15; },
    window: b => { b.box(1.7, 1.5, .8, '#5d6386', 0, .75, -.15); b.box(1.1, .55, .02, b.G('#82b8ff', .45), 0, 1.0, .26); b.box(1.7, .08, .35, '#8a6f55', 0, .7, .4); },
    shield: b => { b.cyl(.05, .05, 1.1, '#8a8fa8', 0, .55, 0); const s = b.cyl(.72, .72, .12, '#82b8ff', 0, 1.3, 0); s.rotation.x = PI / 2; const i = b.cyl(.4, .4, .14, b.G('#5ee39c', .5), 0, 1.3, .01); i.rotation.x = PI / 2; [-.9, .9].forEach(x => b.box(.08, .6, .08, '#ef5b5b', x, .3, .3)); b.box(1.9, .06, .06, '#ef5b5b', 0, .5, .3); },
    draft: b => { b.box(2.2, .1, .5, '#2a2d3f', 0, .5, .45); legs(b, 2.1, .4, .48); b.box(.5, .55, .5, '#82b8ff', -.75, .28, -.35); b.box(.9, 1.3, .9, '#b07cff', .5, .65, -.35); for (let k = 0; k < 4; k++) b.box(.18, .18, .18, b.G(k < 3 ? '#5ee39c' : '#ef5b5b', .6), -.7 + k * .45, .65, .45); },
    dome: b => { b.cyl(.9, .9, .7, '#a7abc4', 0, .35, 0); b.hemi(.9, '#d6d9ea', 0, .7, 0); const t = b.cyl(.13, .13, 1.0, '#5d6386', .35, 1.35, .35); t.rotation.z = -.7; t.rotation.x = .5; },
    antenna: b => { b.cyl(.06, .06, 2.4, '#a7abc4', 0, 1.2, 0); const d = b.cyl(.55, .1, .15, '#d6d9ea', 0, 1.8, .2); d.rotation.x = .7; const l = b.sph(.09, b.G('#ef5b5b', 1), 0, 2.45, 0); blink.push(l); },
  };

  floors.push(...F.map(buildFloor));

  // 엘리베이터 (오른쪽 뒤)
  const top = (N - 1) * H + GAP + 1;
  const shaft = new THREE.Mesh(new THREE.BoxGeometry(1.6, top, 1.6), new THREE.MeshStandardMaterial({ color: '#82b8ff', transparent: true, opacity: .1, depthWrite: false }));
  shaft.position.set(FW / 2 + 1.1, top / 2, -FD / 2 + 1); scene.add(shaft);
  const car = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.6, 1.3), new THREE.MeshStandardMaterial({ color: '#f1b646', emissive: '#f1b646', emissiveIntensity: .35 }));
  car.position.set(FW / 2 + 1.1, .9, -FD / 2 + 1); scene.add(car);
  if (MODE === 'floor') { shaft.material.opacity = .05; }

  // 강조 고리
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.25, .07, 8, 40), new THREE.MeshBasicMaterial({ color: '#f1b646' }));
  ring.rotation.x = PI / 2; ring.visible = false; scene.add(ring);
  let hotK = -1;

  // 토큰 알갱이 (1층 정문 → 층마다 컨베이어 → 위층)
  const PN = RM ? 0 : 120;
  const parts = new THREE.InstancedMesh(new THREE.SphereGeometry(.15, 10, 8), new THREE.MeshBasicMaterial({ color: '#ffffff' }), Math.max(PN, 1));
  parts.instanceMatrix.setUsage(THREE.DynamicDrawUsage); parts.count = PN; scene.add(parts);
  const tmp = new THREE.Matrix4(), col = new THREE.Color(), NL = N - 1;
  const SEG = NL * 2 - 1; // 가로 NL개 + 세로 NL-1개
  function partAt(u) { // u in [0, SEG)
    const j = Math.floor(u), f = u - j, i = j >> 1;
    const y0 = floors[i].y + .45;
    const L = -FW / 2 + 1, R = FW / 2 - 1, z = 2.4;
    if (j % 2 === 0) { const a = i % 2 ? R : L, b = i % 2 ? L : R; return [a + (b - a) * f, y0, z, i]; }
    const x = i % 2 ? L : R, y1 = floors[i + 1].y + .45; return [x, y0 + (y1 - y0) * f, z, i + (f > .5 ? 1 : 0)];
  }

  // 라벨
  const flLbl = floors.map(o => {
    const e = document.createElement('div'); e.className = 'gf-lb fl'; e.style.setProperty('--c', o.f.col);
    e.innerHTML = '<b>' + o.f.fl + '</b><span class="nm"> ' + esc(o.f.name) + '<small>' + (o.f.week ? o.f.week + '주차' : '부록') + '</small></span>';
    e.addEventListener('click', () => { if (MODE === 'building') select(o.f.i === sel ? -1 : o.f.i); else location.href = '../index.html#f' + o.f.i; });
    LBL.appendChild(e); return e;
  });
  const stLbl = floors.map(o => o.sts.map((s, k) => {
    const e = document.createElement('div'), mine = MODE !== 'floor' || s.s.page === PAGE;
    e.className = 'gf-lb st' + (mine ? '' : ' other'); e.style.setProperty('--c', o.f.col);
    e.innerHTML = '<b>' + NUM[o.f.i][k] + '</b><span class="nm">' + esc(s.s.name) + '</span>';
    e.title = s.s.name; e.style.display = 'none';
    e.addEventListener('click', () => goStation(o.f.i, k)); e.addEventListener('mouseenter', () => setHot(k)); e.addEventListener('mouseleave', () => setHot(-1));
    LBL.appendChild(e); return e;
  }));

  function goStation(i, k) {
    const s = F[i].stations[k], h = href(s);
    if (MODE === 'building' && i !== sel) { select(i); return; }
    if (MODE === 'building') {
      setHot(k);
      say(F[i].fl + ' ' + NUM[i][k] + '번 <b>' + esc(s.name) + '</b> — ' + esc(s.desc) + (h ? ' <a href="' + esc(h) + '">그 칸 열기 →</a>' : ' <span style="color:#9d9bb8">(공사 중)</span>'));
      const li = document.querySelector('#gf-info li[data-k="' + k + '"]'); if (li) li.scrollIntoView({ block: 'nearest', behavior: RM ? 'auto' : 'smooth' });
      return;
    }
    if (h) location.href = h;
  }
  function setHot(k) {
    hotK = k;
    const fi = MODE === 'floor' ? D.focus : sel;
    stLbl.forEach((arr, i) => arr.forEach((e, j) => e.classList.toggle('hot', i === fi && j === k)));
    document.querySelectorAll('.gf-st li[data-k]').forEach(li => { const a = li.firstElementChild; a && a.classList.toggle('hot', +li.dataset.k === k); });
  }

  // 카메라 맞추기
  const view = { t: new THREE.Vector3(), half: 20, zoom: 1 }, want = { t: new THREE.Vector3(), half: 20 };
  const bY = i => i * H + ((sel >= 0 && i > sel) ? GAP : 0);
  function fit() {
    let y0, y1, xr = MODE === 'floor' ? 1.4 : 3.0, extra = MODE === 'floor' ? 0 : .3;
    if (sel < 0) { y0 = -.6; y1 = (N - 1) * H + 2.6; }
    else { y0 = bY(sel) - (MODE === 'floor' ? .9 : 1.2); y1 = bY(sel) + H + (MODE === 'floor' ? .9 : 1.6); }
    cam.updateMatrixWorld();
    const R = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 0), U = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 1);
    let a = Infinity, b = -Infinity, c = Infinity, d = -Infinity;
    for (const x of [-FW / 2 - .4, FW / 2 + xr]) for (const y of [y0, y1]) for (const z of [-FD / 2, FD / 2 + .4]) {
      const p = new THREE.Vector3(x, y, z); const dx = p.dot(R), dy = p.dot(U); a = Math.min(a, dx); b = Math.max(b, dx); c = Math.min(c, dy); d = Math.max(d, dy);
    }
    b += (b - a) * extra;
    const w = host.clientWidth || 1, h = host.clientHeight || 1, asp = w / h;
    const cx = (a + b) / 2, cy = (c + d) / 2;
    want.half = Math.max((d - c) / 2, (b - a) / 2 / asp) * 1.06;
    // 카메라 평면 위의 (cx, cy) 를 지나는 시선 위 한 점 = 목표
    const fwd = new THREE.Vector3(); cam.getWorldDirection(fwd);
    want.t.copy(R).multiplyScalar(cx).addScaledVector(U, cy);
    const yy = (y0 + y1) / 2; const k = (yy - want.t.y) / (fwd.y || -1); want.t.addScaledVector(fwd, k);
  }
  function applyView() {
    const w = host.clientWidth || 1, h = host.clientHeight || 1, asp = w / h;
    cam.left = -view.half * asp; cam.right = view.half * asp; cam.top = view.half; cam.bottom = -view.half; cam.updateProjectionMatrix();
  }
  function resize() { const w = host.clientWidth, h = host.clientHeight; renderer.setSize(w, h, false); fit(); applyView(); }
  new ResizeObserver(resize).observe(host);

  // 처음 위치
  floors.forEach(o => { o.y = (MODE === 'building' && !RM) ? bY(o.f.i) + 20 + o.f.i * 1.6 : bY(o.f.i); o.g.position.y = o.y; });
  resize(); fit(); view.half = want.half; view.t.copy(want.t);
  { const off = cam.position.clone().sub(controls.target); controls.target.copy(view.t); cam.position.copy(view.t).add(off); }
  applyView();

  // 고르기 · 누르기
  const ray = new THREE.Raycaster(), pv = new THREE.Vector2(); let down = null;
  function hit(ev) {
    const r = renderer.domElement.getBoundingClientRect();
    pv.set((ev.clientX - r.left) / r.width * 2 - 1, -(ev.clientY - r.top) / r.height * 2 + 1); ray.setFromCamera(pv, cam);
    const hs = ray.intersectObjects(pick, false);
    for (const h of hs) { const u = h.object.userData; if (MODE === 'floor' && u.fl !== D.focus) continue; return u; }
    return null;
  }
  renderer.domElement.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
  renderer.domElement.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 6) return; down = null;
    const u = hit(e); if (!u) { if (MODE === 'building' && sel >= 0) select(-1); return; }
    if (MODE === 'building' && u.fl !== sel) { select(u.fl); return; }
    if (u.st != null) goStation(u.fl, u.st);
  });
  renderer.domElement.addEventListener('pointermove', e => {
    if (e.buttons) return; const u = hit(e);
    const fi = MODE === 'floor' ? D.focus : sel;
    renderer.domElement.style.cursor = u ? 'pointer' : 'grab';
    const k = u && u.fl === fi && u.st != null ? u.st : -1; if (k !== hotK) setHot(k);
  });
  renderer.domElement.addEventListener('pointerleave', () => setHot(-1));

  // 보일 때만 그리기
  let vis = true; new IntersectionObserver(es => es.forEach(x => vis = x.isIntersecting), { threshold: .01 }).observe(host);

  const clock = new THREE.Clock(); let T = 0;
  const v3 = new THREE.Vector3();
  function frame() {
    requestAnimationFrame(frame);
    if (!vis || document.hidden) { clock.getDelta(); return; }
    const dt = Math.min(clock.getDelta(), .05); T += dt;
    const k = 1 - Math.exp(-dt * 6);
    floors.forEach(o => {
      if (T < o.delay) return;
      o.y += (bY(o.f.i) - o.y) * (MODE === 'building' && T < 3 ? 1 - Math.exp(-dt * 4) : k); o.g.position.y = o.y;
      const on = o.f.i === sel; o.outline.material.opacity += ((on ? .95 : 0) - o.outline.material.opacity) * k;
    });
    // 카메라
    view.half += (want.half - view.half) * k;
    v3.copy(want.t).sub(view.t).multiplyScalar(k); view.t.add(v3); controls.target.add(v3); cam.position.add(v3);
    if (Math.abs(cam.zoom - view.zoom) > .001 && !dragging) { cam.zoom += (view.zoom - cam.zoom) * k; }
    applyView(); controls.update();
    sun.position.copy(controls.target).add(new THREE.Vector3(14, 26, 10)); sun.target.position.copy(controls.target);
    // 엘리베이터
    const cy = sel >= 0 ? floors[sel].y + .85 : floors[0].y + .85 + (Math.sin(T * .35) * .5 + .5) * (N - 1) * H;
    car.position.y += (cy - car.position.y) * (sel >= 0 ? k : 1);
    // 토큰
    for (let p = 0; p < PN; p++) {
      const u = ((T * .055 + p / PN) * SEG) % SEG, [x, y, z, fi] = partAt(u);
      tmp.makeTranslation(x, y, z); parts.setMatrixAt(p, tmp);
      const fo = F[Math.min(fi, N - 1)], dim = MODE === 'floor' && fo.i !== D.focus;
      col.set(open(fo.st) ? SC[fo.st] : '#4a4e6a'); if (dim) col.multiplyScalar(.25); parts.setColorAt(p, col);
    }
    if (PN) { parts.instanceMatrix.needsUpdate = true; parts.instanceColor && (parts.instanceColor.needsUpdate = true); }
    spin.forEach(([m, ax, s]) => m.rotation[ax] += dt * s);
    blink.forEach(m => m.visible = (T % 1.4) < .9);
    // 고리
    const fi = MODE === 'floor' ? D.focus : sel;
    if (fi >= 0 && hotK >= 0 && floors[fi].sts[hotK]) { const s = floors[fi].sts[hotK].g; ring.visible = true; ring.position.set(s.position.x, floors[fi].y + .06, s.position.z); ring.scale.setScalar(s.scale.x * (1 + Math.sin(T * 6) * .05)); }
    else ring.visible = false;
    renderer.render(scene, cam);
    // 라벨 위치
    const w = host.clientWidth, h = host.clientHeight;
    const place = (e, x, y, z) => { v3.set(x, y, z).project(cam); const sx = (v3.x + 1) / 2 * w, sy = (1 - v3.y) / 2 * h; const ok = v3.z < 1 && sx > -40 && sx < w + 40 && sy > -10 && sy < h + 20; e.style.display = ok ? '' : 'none'; if (ok) { e.style.left = sx + 'px'; e.style.top = sy + 'px'; } };
    floors.forEach((o, i) => {
      const e = flLbl[i];
      place(e, FW / 2 + 1.9, o.y + 1.3, -FD / 2 + .9);
      e.classList.toggle('on', i === fi); e.classList.toggle('dim', fi >= 0 && i !== fi);
      if (MODE === 'floor') e.style.display = 'none';
      stLbl[i].forEach((le, j) => { if (i !== fi) { le.style.display = 'none'; return; } const s = o.sts[j]; place(le, s.g.position.x, o.y + s.top + .35, s.g.position.z); });
    });
  }
  let dragging = false;
  controls.addEventListener('start', () => { dragging = true; }); controls.addEventListener('end', () => { dragging = false; view.zoom = cam.zoom; });
  frame();

  return {
    select(i) { view.zoom = 1; fit(); },
    hot(k) { setHot(k); }
  };
}
