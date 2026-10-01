/* Legal lens walkthrough — the animated visualization on legal.html.
   Permitted by docs/DESIGN.md §7.1, which scopes its exceptions to this figure.
   Without JavaScript the page is complete: Figure 1 shows the parties and each
   step section carries its messages, protocol notes and legal lens. This script
   reads those sections (data-question / data-hitl / data-exposure, and the flow
   tables' data-from / data-to / data-human / data-none) and builds the
   walkthrough from them, so the step data exists in one place only. */
(function () {
  "use strict";

  var SVG_NS = "http://www.w3.org/2000/svg";
  var figure = document.getElementById("process-figure");
  var svg = document.getElementById("process-diagram");
  if (!figure || !svg) return;
  var flowLayer = svg.querySelector("#wt-flows");
  var labelLayer = svg.querySelector("#wt-labels");

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NW = 156, NH = 58, VW = 1000, VH = 540;
  var STEP_MS = 1250;
  var DRAW_MS = 750;
  var EXPOSURE = { high: "High legal exposure", medium: "Medium legal exposure", lower: "Lower legal exposure" };

  /* ---------- Data, read from the page ---------- */
  var nodes = {};
  Array.prototype.forEach.call(svg.querySelectorAll(".wt-node"), function (g) {
    nodes[g.getAttribute("data-node")] = {
      el: g,
      kind: g.classList.contains("kind-human") ? "human" : g.classList.contains("kind-infra") ? "infra" : "agent",
      x: +g.getAttribute("data-cx"),
      y: +g.getAttribute("data-cy"),
      label: g.querySelector(".wt-node-title").textContent,
      info: g.getAttribute("data-info")
    };
  });

  var steps = Array.prototype.map.call(document.querySelectorAll(".legal-step"), function (sec) {
    return {
      sec: sec,
      id: sec.id,
      title: sec.querySelector("h2").textContent.replace(/^Step \d+\s+—\s+/, ""),
      question: sec.getAttribute("data-question"),
      hitl: sec.getAttribute("data-hitl"),
      exposure: sec.getAttribute("data-exposure"),
      flows: Array.prototype.map.call(sec.querySelectorAll(".flow-table tbody tr"), function (tr) {
        var adcp = tr.querySelector('[data-label="AdCP"]');
        var aamp = tr.querySelector('[data-label="AAMP"]');
        return {
          from: tr.getAttribute("data-from"),
          to: tr.getAttribute("data-to"),
          human: tr.hasAttribute("data-human"),
          adcp: adcp.hasAttribute("data-none") ? null : adcp.textContent.trim(),
          aamp: aamp.hasAttribute("data-none") ? null : aamp.textContent.trim()
        };
      })
    };
  });
  if (!steps.length) return;

  var state = { cur: 0, proto: "both", tab: "what", playing: false, runId: 0, timers: [], obstacles: [] };

  /* ---------- DOM helpers ---------- */
  function make(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }
  function svgEl(tag, attrs, parent) {
    var e = document.createElementNS(SVG_NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function empty(e) { while (e.firstChild) e.removeChild(e.firstChild); }

  /* ---------- Build the stage ---------- */
  var stepper = make("ol", { "class": "wt-stepper", "aria-label": "Process steps" });
  var stepButtons = steps.map(function (s, i) {
    var li = make("li");
    var b = make("button", { type: "button", "class": "wt-step" });
    b.appendChild(make("span", { "class": "wt-step-num", "aria-hidden": "true" }, String(i + 1)));
    b.appendChild(make("span", { "class": "wt-step-label" }, s.title));
    b.setAttribute("aria-label", "Step " + (i + 1) + ": " + s.title);
    b.addEventListener("click", function () { setPlaying(false); go(i); });
    li.appendChild(b);
    stepper.appendChild(li);
    return b;
  });
  var progress = make("div", { "class": "wt-progress", "aria-hidden": "true" });
  var progressBar = make("i");
  progress.appendChild(progressBar);

  var stage = make("div", { "class": "wt-stage" });

  /* Diagram card */
  var card = make("div", { "class": "wt-card wt-diagram" });
  var head = make("div", { "class": "wt-head" });
  var headText = make("div");
  var stageTitle = make("p", { "class": "wt-title" });
  var stageKicker = make("p", { "class": "wt-kicker" });
  headText.appendChild(stageTitle);
  headText.appendChild(stageKicker);
  var seg = make("div", { "class": "wt-seg", role: "group", "aria-label": "Message names from" });
  var segButtons = [["both", "Both"], ["adcp", "AdCP"], ["aamp", "AAMP"]].map(function (p) {
    var b = make("button", { type: "button", "aria-pressed": p[0] === state.proto ? "true" : "false" }, p[1]);
    b.addEventListener("click", function () {
      state.proto = p[0];
      segButtons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      animateStep();
    });
    seg.appendChild(b);
    return b;
  });
  head.appendChild(headText);
  head.appendChild(seg);
  card.appendChild(head);
  var wrap = figure.querySelector(".figure-wrap");
  card.appendChild(wrap);

  var legend = make("ul", { "class": "wt-legend" });
  [["wt-key-agent", "Machine-to-machine message"], ["wt-key-human", "Human decision or approval"],
   ["wt-key-none", "Not covered by the selected protocol family"]].forEach(function (k) {
    var li = make("li");
    li.appendChild(make("i", { "class": k[0], "aria-hidden": "true" }));
    li.appendChild(document.createTextNode(k[1]));
    legend.appendChild(li);
  });
  legend.appendChild(make("li", {}, "Select any box for its role"));
  card.appendChild(legend);

  var controls = make("div", { "class": "wt-controls" });
  var btnRow = make("div", { "class": "wt-btn-row" });
  var prevBtn = make("button", { type: "button", "class": "wt-btn" }, "← Back");
  var playBtn = make("button", { type: "button", "class": "wt-btn wt-btn-primary" }, "▶ Play tour");
  var replayBtn = make("button", { type: "button", "class": "wt-btn" }, "↻ Replay");
  var nextBtn = make("button", { type: "button", "class": "wt-btn" }, "Next →");
  [prevBtn, playBtn, replayBtn, nextBtn].forEach(function (b) { btnRow.appendChild(b); });
  controls.appendChild(btnRow);
  controls.appendChild(make("p", { "class": "wt-hint" }, "Keyboard: ← → move between steps while the walkthrough has focus"));
  card.appendChild(controls);

  /* Side panel */
  var panel = make("aside", { "class": "wt-card wt-panel", "aria-label": "Step details" });
  var panelHead = make("div", { "class": "wt-panel-head" });
  var panelTitle = make("p", { "class": "wt-panel-title", "aria-live": "polite" });
  var panelBadges = make("p", { "class": "wt-chips" });
  panelHead.appendChild(panelTitle);
  panelHead.appendChild(panelBadges);
  var tabs = make("div", { "class": "wt-tabs", role: "tablist", "aria-label": "Step detail views" });
  var tabBody = make("div", { "class": "wt-tab-body", role: "tabpanel", id: "wt-tabpanel", tabindex: "0" });
  var tabButtons = [["what", "What happens"], ["adcp", "AdCP"], ["aamp", "AAMP"], ["legal", "Legal lens"]].map(function (t) {
    var b = make("button", { type: "button", role: "tab", "aria-controls": "wt-tabpanel", "data-tab": t[0] }, t[1]);
    b.addEventListener("click", function () { state.tab = t[0]; renderPanel(); });
    tabs.appendChild(b);
    return b;
  });
  panel.appendChild(panelHead);
  panel.appendChild(tabs);
  panel.appendChild(tabBody);

  stage.appendChild(card);
  stage.appendChild(panel);
  figure.insertBefore(stepper, figure.firstChild);
  figure.insertBefore(progress, stepper.nextSibling);
  figure.insertBefore(stage, progress.nextSibling);

  /* The figure is now interactive: its boxes are buttons, so it is a group,
     not a single image. */
  svg.setAttribute("role", "group");
  svg.setAttribute("aria-label", "Animated diagram of the messages exchanged in the selected step");
  Object.keys(nodes).forEach(function (k) {
    var n = nodes[k];
    n.el.setAttribute("tabindex", "0");
    n.el.setAttribute("role", "button");
    n.el.setAttribute("aria-label", n.label + ": " + n.info);
    n.el.addEventListener("click", function () { showNodeInfo(k); });
    n.el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); showNodeInfo(k); }
    });
  });
  figure.classList.add("is-interactive");

  /* ---------- Panel content, cloned from the step section ---------- */
  function sectionPart(sec, part) {
    var frag = document.createDocumentFragment();
    var kids = Array.prototype.slice.call(sec.children);
    function after(match) {
      var i = kids.findIndex(match);
      return i < 0 ? [] : kids.slice(i + 1);
    }
    function isH3(text) { return function (el) { return el.tagName === "H3" && el.textContent.trim() === text; }; }
    var list = [];
    if (part === "what") {
      var t = kids.findIndex(function (el) { return el.classList.contains("table-wrap"); });
      list = kids.slice(2, t < 0 ? kids.length : t); /* skip the h2 and the question line */
    } else if (part === "adcp") {
      list = after(isH3("AdCP")).slice(0, 1);
    } else if (part === "aamp") {
      var rest = after(isH3("AAMP"));
      list = rest.slice(0, 1);
      if (rest[1] && rest[1].classList.contains("source")) list.push(rest[1]);
    } else {
      list = after(isH3("Legal lens"));
    }
    list.forEach(function (el) {
      var c = el.cloneNode(true);
      c.removeAttribute("id");
      frag.appendChild(c);
    });
    return frag;
  }

  function renderPanel() {
    var s = steps[state.cur];
    panelTitle.textContent = "Step " + (state.cur + 1) + " of " + steps.length + ": " + s.title;
    empty(panelBadges);
    panelBadges.appendChild(make("span", { "class": "wt-chip" }, EXPOSURE[s.exposure] || s.exposure));
    panelBadges.appendChild(make("span", { "class": "wt-chip wt-chip-human" }, "Human in the loop: " + s.hitl));
    tabButtons.forEach(function (b) { b.setAttribute("aria-selected", b.getAttribute("data-tab") === state.tab ? "true" : "false"); });
    empty(tabBody);
    if (state.tab === "adcp" || state.tab === "aamp") {
      tabBody.appendChild(make("p", { "class": "wt-std-head" }, state.tab === "adcp" ? "AdCP — Ad Context Protocol" : "AAMP — IAB Tech Lab"));
    }
    tabBody.appendChild(sectionPart(s.sec, state.tab));
    var more = make("p", { "class": "source" });
    more.appendChild(make("a", { href: "#" + s.id }, "Read step " + (state.cur + 1) + " in full"));
    tabBody.appendChild(more);
  }

  function showNodeInfo(k) {
    var n = nodes[k];
    tabButtons.forEach(function (b) { b.setAttribute("aria-selected", "false"); });
    empty(tabBody);
    var h = make("p", { "class": "wt-std-head" });
    h.appendChild(make("span", { "class": "wt-kindtag kind-" + n.kind }, n.kind === "agent" ? "AI AGENT" : n.kind === "human" ? "PEOPLE" : "INFRA"));
    h.appendChild(document.createTextNode(" " + n.label));
    tabBody.appendChild(h);
    tabBody.appendChild(make("p", {}, n.info));
    var inv = make("p", { "class": "source" }, "Involved in steps: ");
    steps.forEach(function (s, i) {
      if (!s.flows.some(function (f) { return f.from === k || f.to === k; })) return;
      var b = make("button", { type: "button", "class": "wt-link" }, (i + 1) + ". " + s.title);
      b.addEventListener("click", function () { setPlaying(false); state.tab = "what"; go(i); });
      inv.appendChild(b);
    });
    tabBody.appendChild(inv);
    tabBody.appendChild(make("p", { "class": "source" }, "Select a tab above to return to the step details."));
  }

  /* ---------- Animation ---------- */
  function clearTimers() { state.timers.forEach(clearTimeout); state.timers = []; }
  function later(fn, ms) {
    var id = state.runId;
    state.timers.push(setTimeout(function () { if (id === state.runId) fn(); }, ms));
  }

  /* Point on node c's border, toward point o. */
  function clip(c, o) {
    var dx = o.x - c.x, dy = o.y - c.y;
    var t = Math.min((NW / 2 + 4) / (Math.abs(dx) || 1e-6), (NH / 2 + 4) / (Math.abs(dy) || 1e-6));
    return { x: c.x + dx * t, y: c.y + dy * t };
  }

  function labelLines(f) {
    if (state.proto === "adcp") return [f.adcp || "not specified in AdCP"];
    if (state.proto === "aamp") return [f.aamp || "not specified in AAMP"];
    if (f.adcp === f.aamp) return [f.adcp];
    return ["AdCP: " + (f.adcp || "not specified"), "AAMP: " + (f.aamp || "not specified")];
  }

  function isMissing(f) {
    return (state.proto === "adcp" && !f.adcp) || (state.proto === "aamp" && !f.aamp) ||
      (state.proto === "both" && !f.adcp && !f.aamp);
  }

  function pulse(k, on) { nodes[k].el.classList.toggle("is-pulse", on && !reduceMotion); }

  function drawFlow(f, i, repeat) {
    var A = nodes[f.from], B = nodes[f.to];
    var missing = isMissing(f);
    var type = missing ? "none" : f.human ? "human" : "agent";
    var p0 = clip(A, B), p2 = clip(B, A);
    var mx = (p0.x + p2.x) / 2, my = (p0.y + p2.y) / 2;
    var dx = p2.x - p0.x, dy = p2.y - p0.y, len = Math.hypot(dx, dy) || 1;
    var off = Math.min(46, len * 0.22) * (1 + repeat * 0.9);
    var c = { x: mx + (-dy / len) * off, y: my + (dx / len) * off };

    var path = svgEl("path", {
      "class": "wt-flow wt-flow-" + type,
      d: "M" + p0.x + "," + p0.y + " Q" + c.x + "," + c.y + " " + p2.x + "," + p2.y
    }, flowLayer);

    function finish() {
      path.style.strokeDasharray = "";
      path.style.strokeDashoffset = "";
      path.style.transition = "";
      path.classList.add("is-done");
      path.setAttribute("marker-end", "url(#wt-arr-" + type + ")");
    }

    if (reduceMotion) {
      finish();
    } else {
      var L = path.getTotalLength();
      path.style.strokeDasharray = L;
      path.style.strokeDashoffset = L;
      path.getBoundingClientRect();
      path.style.transition = "stroke-dashoffset " + DRAW_MS + "ms ease";
      path.style.strokeDashoffset = "0";
      pulse(f.from, true);
      /* The packet travels the path, then hands the pulse to the receiver. */
      var dot = svgEl("circle", { "class": "wt-packet wt-packet-" + type, r: 6.5 }, flowLayer);
      var t0 = performance.now(), id = state.runId;
      (function move(t) {
        if (id !== state.runId) return;
        var k = Math.min(1, Math.max(0, (t - t0) / DRAW_MS));
        var e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        var pt = path.getPointAtLength(L * e);
        dot.setAttribute("cx", pt.x);
        dot.setAttribute("cy", pt.y);
        if (k < 1) { requestAnimationFrame(move); return; }
        pulse(f.from, false);
        pulse(f.to, true);
        later(function () { pulse(f.to, false); }, 900);
        if (dot.animate) {
          dot.animate([{ r: 6.5, opacity: 1 }, { r: 14, opacity: 0 }], { duration: 500, fill: "forwards" });
        } else {
          dot.remove();
        }
        finish();
      })(t0);
    }

    /* Label: numbered, at the curve's midpoint, clamped inside the canvas. */
    var mid = { x: 0.25 * p0.x + 0.5 * c.x + 0.25 * p2.x, y: 0.25 * p0.y + 0.5 * c.y + 0.25 * p2.y };
    var lg = svgEl("g", { "class": "wt-label wt-label-" + type }, labelLayer);
    var bg = svgEl("rect", { rx: 7 }, lg);
    var num = svgEl("text", { "class": "wt-label-num" }, lg);
    num.textContent = String(i + 1);
    var lines = labelLines(f).map(function (l) {
      var t = svgEl("text", { "class": "wt-label-text" }, lg);
      t.textContent = l;
      return t;
    });
    var w = Math.max.apply(null, lines.map(function (t) { return t.getComputedTextLength(); })) + 32;
    var h = lines.length * 16 + 10;
    /* Slide the label along the arrow's normal until it clears the boxes and
       the labels already placed in this step; keep the start spot if none is free. */
    var nx = -dy / len, ny = dx / len, top = f.human && !missing ? 14 : 0;
    function at(d) {
      return {
        x: Math.max(6, Math.min(VW - 6 - w, mid.x + nx * d - w / 2)),
        y: Math.max(6 + top, Math.min(VH - 6 - h, mid.y + ny * d - h / 2))
      };
    }
    function hits(p) {
      return state.obstacles.some(function (o) {
        return p.x < o.x + o.w + 3 && p.x + w + 3 > o.x && p.y - top < o.y + o.h + 3 && p.y + h + 3 > o.y;
      });
    }
    var pos = at(0);
    for (var d = 8; hits(pos) && d <= 160; d += 8) {
      var a = at(d), b = at(-d);
      if (!hits(a)) { pos = a; break; }
      if (!hits(b)) { pos = b; break; }
      if (d === 160) pos = at(0);
    }
    state.obstacles.push({ x: pos.x, y: pos.y - top, w: w, h: h + top });
    var x = pos.x, y = pos.y;
    bg.setAttribute("x", x); bg.setAttribute("y", y);
    bg.setAttribute("width", w); bg.setAttribute("height", h);
    num.setAttribute("x", x + 9); num.setAttribute("y", y + 18);
    lines.forEach(function (t, j) { t.setAttribute("x", x + 24); t.setAttribute("y", y + 18 + j * 16); });
    if (f.human && !missing) {
      var tag = svgEl("text", { "class": "wt-label-human", x: x + w - 4, y: y - 4, "text-anchor": "end" }, lg);
      tag.textContent = "HUMAN";
    }
    if (reduceMotion) lg.classList.add("is-shown");
    else later(function () { lg.classList.add("is-shown"); }, 350);
  }

  function animateStep() {
    state.runId++;
    clearTimers();
    var s = steps[state.cur];
    empty(flowLayer);
    empty(labelLayer);
    var involved = {};
    s.flows.forEach(function (f) { involved[f.from] = involved[f.to] = true; });
    state.obstacles = Object.keys(involved).map(function (k) {
      return { x: nodes[k].x - NW / 2, y: nodes[k].y - NH / 2 - 9, w: NW, h: NH + 9 };
    });
    Object.keys(nodes).forEach(function (k) {
      nodes[k].el.classList.toggle("is-dim", !involved[k]);
      nodes[k].el.classList.remove("is-pulse");
    });
    var seen = {};
    s.flows.forEach(function (f, i) {
      var key = f.from + ">" + f.to;
      var repeat = seen[key] || 0;
      seen[key] = repeat + 1;
      if (reduceMotion) drawFlow(f, i, repeat);
      else later(function () { drawFlow(f, i, repeat); }, 250 + i * STEP_MS);
    });
    if (state.playing) {
      later(function () {
        if (state.cur < steps.length - 1) go(state.cur + 1);
        else setPlaying(false);
      }, 250 + s.flows.length * STEP_MS + 2600);
    }
  }

  function renderStepper() {
    stepButtons.forEach(function (b, i) {
      b.classList.toggle("is-current", i === state.cur);
      b.classList.toggle("is-done", i < state.cur);
      if (i === state.cur) b.setAttribute("aria-current", "step");
      else b.removeAttribute("aria-current");
    });
    var cur = stepButtons[state.cur];
    stepper.scrollTo({ left: cur.parentNode.offsetLeft - stepper.clientWidth / 2 + cur.clientWidth / 2, behavior: reduceMotion ? "auto" : "smooth" });
    progressBar.style.width = ((state.cur + 1) / steps.length * 100) + "%";
    prevBtn.disabled = state.cur === 0;
    nextBtn.disabled = state.cur === steps.length - 1;
    var s = steps[state.cur];
    stageTitle.textContent = (state.cur + 1) + ". " + s.title;
    stageKicker.textContent = s.question;
  }

  function go(i) {
    state.cur = Math.max(0, Math.min(steps.length - 1, i));
    renderStepper();
    renderPanel();
    animateStep();
  }

  function setPlaying(p) {
    state.playing = p;
    playBtn.textContent = p ? "❚❚ Pause tour" : "▶ Play tour";
    if (p) { state.tab = "what"; renderPanel(); animateStep(); }
  }

  prevBtn.addEventListener("click", function () { setPlaying(false); go(state.cur - 1); });
  nextBtn.addEventListener("click", function () { setPlaying(false); go(state.cur + 1); });
  replayBtn.addEventListener("click", function () { animateStep(); });
  playBtn.addEventListener("click", function () {
    if (!state.playing && state.cur === steps.length - 1) { state.cur = 0; renderStepper(); renderPanel(); }
    setPlaying(!state.playing);
  });
  figure.addEventListener("keydown", function (e) {
    if (e.target.closest("input, summary, a")) return;
    if (e.key === "ArrowRight") { setPlaying(false); go(state.cur + 1); }
    if (e.key === "ArrowLeft") { setPlaying(false); go(state.cur - 1); }
  });

  go(0);
})();
