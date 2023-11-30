var jt = Object.defineProperty;
var wt = (t, e, n) => e in t ? jt(t, e, { enumerable: !0, configurable: !0, writable: !0, value: n }) : t[e] = n;
var Ce = (t, e, n) => (wt(t, typeof e != "symbol" ? e + "" : e, n), n);
function E() {
}
function mt(t) {
  return t();
}
function Ue() {
  return /* @__PURE__ */ Object.create(null);
}
function te(t) {
  t.forEach(mt);
}
function ht(t) {
  return typeof t == "function";
}
function H(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function yt(t) {
  return Object.keys(t).length === 0;
}
function St(t, ...e) {
  if (t == null) {
    for (const l of e)
      l(void 0);
    return E;
  }
  const n = t.subscribe(...e);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function J(t, e, n) {
  t.$$.on_destroy.push(St(e, n));
}
function a(t, e) {
  t.appendChild(e);
}
function g(t, e, n) {
  t.insertBefore(e, n || null);
}
function b(t) {
  t.parentNode && t.parentNode.removeChild(t);
}
function V(t, e) {
  for (let n = 0; n < t.length; n += 1)
    t[n] && t[n].d(e);
}
function d(t) {
  return document.createElement(t);
}
function q(t) {
  return document.createTextNode(t);
}
function k() {
  return q(" ");
}
function W() {
  return q("");
}
function U(t, e, n, l) {
  return t.addEventListener(e, n, l), () => t.removeEventListener(e, n, l);
}
function bt(t) {
  return function(e) {
    return e.preventDefault(), t.call(this, e);
  };
}
function p(t, e, n) {
  n == null ? t.removeAttribute(e) : t.getAttribute(e) !== n && t.setAttribute(e, n);
}
function qt(t) {
  return Array.from(t.childNodes);
}
function N(t, e) {
  e = "" + e, t.data !== e && (t.data = /** @type {string} */
  e);
}
function x(t, e) {
  t.value = e ?? "";
}
function He(t, e, n) {
  for (let l = 0; l < t.options.length; l += 1) {
    const s = t.options[l];
    if (s.__value === e) {
      s.selected = !0;
      return;
    }
  }
  (!n || e !== void 0) && (t.selectedIndex = -1);
}
function Ot(t) {
  const e = t.querySelector(":checked");
  return e && e.__value;
}
let ue;
function re(t) {
  ue = t;
}
function Ct() {
  if (!ue)
    throw new Error("Function called outside component initialization");
  return ue;
}
function gt(t) {
  Ct().$$.on_mount.push(t);
}
const Y = [], Ve = [];
let Z = [];
const We = [], Nt = /* @__PURE__ */ Promise.resolve();
let Ie = !1;
function Et() {
  Ie || (Ie = !0, Nt.then(vt));
}
function $e(t) {
  Z.push(t);
}
const Ne = /* @__PURE__ */ new Set();
let K = 0;
function vt() {
  if (K !== 0)
    return;
  const t = ue;
  do {
    try {
      for (; K < Y.length; ) {
        const e = Y[K];
        K++, re(e), It(e.$$);
      }
    } catch (e) {
      throw Y.length = 0, K = 0, e;
    }
    for (re(null), Y.length = 0, K = 0; Ve.length; )
      Ve.pop()();
    for (let e = 0; e < Z.length; e += 1) {
      const n = Z[e];
      Ne.has(n) || (Ne.add(n), n());
    }
    Z.length = 0;
  } while (Y.length);
  for (; We.length; )
    We.pop()();
  Ie = !1, Ne.clear(), re(t);
}
function It(t) {
  if (t.fragment !== null) {
    t.update(), te(t.before_update);
    const e = t.dirty;
    t.dirty = [-1], t.fragment && t.fragment.p(t.ctx, e), t.after_update.forEach($e);
  }
}
function Rt(t) {
  const e = [], n = [];
  Z.forEach((l) => t.indexOf(l) === -1 ? e.push(l) : n.push(l)), n.forEach((l) => l()), Z = e;
}
const ke = /* @__PURE__ */ new Set();
let F;
function kt() {
  F = {
    r: 0,
    c: [],
    p: F
    // parent group
  };
}
function $t() {
  F.r || te(F.c), F = F.p;
}
function P(t, e) {
  t && t.i && (ke.delete(t), t.i(e));
}
function z(t, e, n, l) {
  if (t && t.o) {
    if (ke.has(t))
      return;
    ke.add(t), F.c.push(() => {
      ke.delete(t), l && (n && t.d(1), l());
    }), t.o(e);
  } else
    l && l();
}
function D(t) {
  return (t == null ? void 0 : t.length) !== void 0 ? t : Array.from(t);
}
function fe(t) {
  t && t.c();
}
function ne(t, e, n) {
  const { fragment: l, after_update: s } = t.$$;
  l && l.m(e, n), $e(() => {
    const i = t.$$.on_mount.map(mt).filter(ht);
    t.$$.on_destroy ? t.$$.on_destroy.push(...i) : te(i), t.$$.on_mount = [];
  }), s.forEach($e);
}
function le(t, e) {
  const n = t.$$;
  n.fragment !== null && (Rt(n.after_update), te(n.on_destroy), n.fragment && n.fragment.d(e), n.on_destroy = n.fragment = null, n.ctx = []);
}
function Jt(t, e) {
  t.$$.dirty[0] === -1 && (Y.push(t), Et(), t.$$.dirty.fill(0)), t.$$.dirty[e / 31 | 0] |= 1 << e % 31;
}
function se(t, e, n, l, s, i, o = null, r = [-1]) {
  const u = ue;
  re(t);
  const c = t.$$ = {
    fragment: null,
    ctx: [],
    // state
    props: i,
    update: E,
    not_equal: s,
    bound: Ue(),
    // lifecycle
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(e.context || (u ? u.$$.context : [])),
    // everything else
    callbacks: Ue(),
    dirty: r,
    skip_bound: !1,
    root: e.target || u.$$.root
  };
  o && o(c.root);
  let f = !1;
  if (c.ctx = n ? n(t, e.props || {}, (_, m, ...w) => {
    const C = w.length ? w[0] : m;
    return c.ctx && s(c.ctx[_], c.ctx[_] = C) && (!c.skip_bound && c.bound[_] && c.bound[_](C), f && Jt(t, _)), m;
  }) : [], c.update(), f = !0, te(c.before_update), c.fragment = l ? l(c.ctx) : !1, e.target) {
    if (e.hydrate) {
      const _ = qt(e.target);
      c.fragment && c.fragment.l(_), _.forEach(b);
    } else
      c.fragment && c.fragment.c();
    e.intro && P(t.$$.fragment), ne(t, e.target, e.anchor), vt();
  }
  re(u);
}
class ie {
  constructor() {
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    Ce(this, "$$");
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    Ce(this, "$$set");
  }
  /** @returns {void} */
  $destroy() {
    le(this, 1), this.$destroy = E;
  }
  /**
   * @template {Extract<keyof Events, string>} K
   * @param {K} type
   * @param {((e: Events[K]) => void) | null | undefined} callback
   * @returns {() => void}
   */
  $on(e, n) {
    if (!ht(n))
      return E;
    const l = this.$$.callbacks[e] || (this.$$.callbacks[e] = []);
    return l.push(n), () => {
      const s = l.indexOf(n);
      s !== -1 && l.splice(s, 1);
    };
  }
  /**
   * @param {Partial<Props>} props
   * @returns {void}
   */
  $set(e) {
    this.$$set && !yt(e) && (this.$$.skip_bound = !0, this.$$set(e), this.$$.skip_bound = !1);
  }
}
const Tt = "4";
typeof window < "u" && (window.__svelte || (window.__svelte = { v: /* @__PURE__ */ new Set() })).v.add(Tt);
const Q = [];
function M(t, e = E) {
  let n;
  const l = /* @__PURE__ */ new Set();
  function s(r) {
    if (H(t, r) && (t = r, n)) {
      const u = !Q.length;
      for (const c of l)
        c[1](), Q.push(c, t);
      if (u) {
        for (let c = 0; c < Q.length; c += 2)
          Q[c][0](Q[c + 1]);
        Q.length = 0;
      }
    }
  }
  function i(r) {
    s(r(t));
  }
  function o(r, u = E) {
    const c = [r, u];
    return l.add(c), l.size === 1 && (n = e(s, i) || E), r(t), () => {
      l.delete(c), l.size === 0 && n && (n(), n = null);
    };
  }
  return { set: s, update: i, subscribe: o };
}
const ee = M(""), we = M(""), ce = M(""), Re = M(null), je = M(null), ye = M(null), Je = M(null), At = M(null), Se = M(null), Ee = M({});
function Te() {
  ee.set(""), je.set(null), ye.set(null), Je.set(null), Re.set(null), Se.set(null);
}
async function Dt(t = "", e = {}) {
  const n = document.querySelector("[name=csrfmiddlewaretoken]").value;
  return (await fetch(t, {
    method: "POST",
    cache: "no-cache",
    body: JSON.stringify(e),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": n
    },
    mode: "same-origin"
  })).json();
}
function Lt(t, e) {
  if (At.set(e), e.error) {
    ee.set(e.error);
    return;
  } else
    ee.set("");
  if (t == "submit")
    je.set(e);
  else if (t == "status")
    je.set(e);
  else if (t == "listall")
    Re.set(Object.keys(e));
  else if (t == "listsvc") {
    Je.set(e);
    let l = [];
    for (var n in e.jobs)
      l = l.concat(e.jobs[n]);
    ye.set(l), e.definition && Se.set(e.definition);
  } else
    console.log("Response for unknown action:", t);
}
function ae(t, e, n, l) {
  let s = {
    service: e,
    job: n,
    message: l,
    action: t
  };
  we.set(e), Dt("/main/", s).then((i) => {
    Lt(t, i);
  });
}
function Xe(t) {
  let e, n;
  return {
    c() {
      e = d("input"), p(e, "class", "hover:underline px-2 cursor-pointer uppercase"), p(e, "type", "submit"), p(e, "name", "status"), e.value = n = "Refresh " + /*$selected_job*/
      t[0];
    },
    m(l, s) {
      g(l, e, s);
    },
    p(l, s) {
      s & /*$selected_job*/
      1 && n !== (n = "Refresh " + /*$selected_job*/
      l[0]) && (e.value = n);
    },
    d(l) {
      l && b(e);
    }
  };
}
function Ge(t) {
  let e;
  return {
    c() {
      e = d("input"), p(e, "class", "hover:underline px-2 cursor-pointer uppercase"), p(e, "type", "submit"), p(e, "name", "listsvc"), e.value = /*$selected_service*/
      t[1];
    },
    m(n, l) {
      g(n, e, l);
    },
    p(n, l) {
      l & /*$selected_service*/
      2 && (e.value = /*$selected_service*/
      n[1]);
    },
    d(n) {
      n && b(e);
    }
  };
}
function Bt(t) {
  let e, n, l, s, i, o, r, u = (
    /*$selected_job*/
    t[0] && Xe(t)
  ), c = (
    /*$selected_service*/
    t[1] && Ge(t)
  );
  return {
    c() {
      e = d("form"), n = d("div"), u && u.c(), l = k(), c && c.c(), s = k(), i = d("input"), p(i, "class", "hover:underline px-2 cursor-pointer uppercase"), p(i, "type", "submit"), p(i, "name", "listall"), i.value = "List All", p(n, "class", "col-span-5 mx-auto"), p(e, "class", "topbar svelte-1usbfhw");
    },
    m(f, _) {
      g(f, e, _), a(e, n), u && u.m(n, null), a(n, l), c && c.m(n, null), a(n, s), a(n, i), o || (r = U(e, "submit", bt(
        /*handleRequest*/
        t[2]
      )), o = !0);
    },
    p(f, [_]) {
      /*$selected_job*/
      f[0] ? u ? u.p(f, _) : (u = Xe(f), u.c(), u.m(n, l)) : u && (u.d(1), u = null), /*$selected_service*/
      f[1] ? c ? c.p(f, _) : (c = Ge(f), c.c(), c.m(n, s)) : c && (c.d(1), c = null);
    },
    i: E,
    o: E,
    d(f) {
      f && b(e), u && u.d(), c && c.d(), o = !1, r();
    }
  };
}
function Pt(t, e, n) {
  let l, s;
  J(t, ce, (o) => n(0, l = o)), J(t, we, (o) => n(1, s = o));
  function i(o) {
    Te();
    const { submitter: r } = o;
    if (r.name == "listsvc" && s == "") {
      ee.set("Select a service from the list");
      return;
    }
    ae(r.name, s, l, "");
  }
  return [l, s, i];
}
class Mt extends ie {
  constructor(e) {
    super(), se(this, e, Pt, Bt, H, {});
  }
}
function Ke(t, e, n) {
  const l = t.slice();
  return l[4] = e[n][0], l[5] = e[n][1], l;
}
function Qe(t, e, n) {
  const l = t.slice();
  return l[8] = e[n][0], l[9] = e[n][1], l;
}
function Ye(t, e, n) {
  const l = t.slice();
  return l[12] = e[n], l;
}
function Ze(t) {
  let e, n = D(Object.entries(
    /*$service_details*/
    t[0]
  )), l = [];
  for (let s = 0; s < n.length; s += 1)
    l[s] = nt(Ke(t, n, s));
  return {
    c() {
      e = d("div");
      for (let s = 0; s < l.length; s += 1)
        l[s].c();
      p(e, "class", "grid grid-cols-10 mx-auto w-11/12 my-3");
    },
    m(s, i) {
      g(s, e, i);
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(e, null);
    },
    p(s, i) {
      if (i & /*Object, $service_details, onclick*/
      3) {
        n = D(Object.entries(
          /*$service_details*/
          s[0]
        ));
        let o;
        for (o = 0; o < n.length; o += 1) {
          const r = Ke(s, n, o);
          l[o] ? l[o].p(r, i) : (l[o] = nt(r), l[o].c(), l[o].m(e, null));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = n.length;
      }
    },
    d(s) {
      s && b(e), V(l, s);
    }
  };
}
function xe(t) {
  let e, n = (
    /*key*/
    t[4] + ""
  ), l, s, i, o = D(Object.entries(
    /*value*/
    t[5]
  )), r = [];
  for (let u = 0; u < o.length; u += 1)
    r[u] = tt(Qe(t, o, u));
  return {
    c() {
      e = d("p"), l = q(n), s = k();
      for (let u = 0; u < r.length; u += 1)
        r[u].c();
      i = W(), p(e, "class", "col-start-1 col-span-9 font-bold border-b pt-2 pb-1 mt-1");
    },
    m(u, c) {
      g(u, e, c), a(e, l), g(u, s, c);
      for (let f = 0; f < r.length; f += 1)
        r[f] && r[f].m(u, c);
      g(u, i, c);
    },
    p(u, c) {
      if (c & /*$service_details*/
      1 && n !== (n = /*key*/
      u[4] + "") && N(l, n), c & /*Object, $service_details, onclick*/
      3) {
        o = D(Object.entries(
          /*value*/
          u[5]
        ));
        let f;
        for (f = 0; f < o.length; f += 1) {
          const _ = Qe(u, o, f);
          r[f] ? r[f].p(_, c) : (r[f] = tt(_), r[f].c(), r[f].m(i.parentNode, i));
        }
        for (; f < r.length; f += 1)
          r[f].d(1);
        r.length = o.length;
      }
    },
    d(u) {
      u && (b(e), b(s), b(i)), V(r, u);
    }
  };
}
function zt(t) {
  let e, n = (
    /*jobname*/
    t[12] + ""
  ), l, s;
  return {
    c() {
      e = d("p"), l = q(n), s = k(), p(e, "class", "col-start-4 col-span-5 pb-1");
    },
    m(i, o) {
      g(i, e, o), a(e, l), a(e, s);
    },
    p(i, o) {
      o & /*$service_details*/
      1 && n !== (n = /*jobname*/
      i[12] + "") && N(l, n);
    },
    d(i) {
      i && b(e);
    }
  };
}
function Ft(t) {
  let e, n = (
    /*jobname*/
    t[12] + ""
  ), l, s, i, o;
  return {
    c() {
      e = d("p"), l = q(n), s = k(), p(e, "class", "col-start-4 col-span-5 pb-1 cursor-pointer hover:underline");
    },
    m(r, u) {
      g(r, e, u), a(e, l), a(e, s), i || (o = U(
        e,
        "click",
        /*onclick*/
        t[1]
      ), i = !0);
    },
    p(r, u) {
      u & /*$service_details*/
      1 && n !== (n = /*jobname*/
      r[12] + "") && N(l, n);
    },
    d(r) {
      r && b(e), i = !1, o();
    }
  };
}
function et(t) {
  let e;
  function n(i, o) {
    return (
      /*key*/
      i[4] == "jobs" ? Ft : zt
    );
  }
  let l = n(t), s = l(t);
  return {
    c() {
      s.c(), e = W();
    },
    m(i, o) {
      s.m(i, o), g(i, e, o);
    },
    p(i, o) {
      l === (l = n(i)) && s ? s.p(i, o) : (s.d(1), s = l(i), s && (s.c(), s.m(e.parentNode, e)));
    },
    d(i) {
      i && b(e), s.d(i);
    }
  };
}
function tt(t) {
  let e, n = (
    /*type*/
    t[8] + ""
  ), l, s, i, o = D(
    /*job*/
    t[9]
  ), r = [];
  for (let u = 0; u < o.length; u += 1)
    r[u] = et(Ye(t, o, u));
  return {
    c() {
      e = d("p"), l = q(n), s = k();
      for (let u = 0; u < r.length; u += 1)
        r[u].c();
      i = W(), p(e, "class", "col-start-2 col-span-8 pb-2");
    },
    m(u, c) {
      g(u, e, c), a(e, l), g(u, s, c);
      for (let f = 0; f < r.length; f += 1)
        r[f] && r[f].m(u, c);
      g(u, i, c);
    },
    p(u, c) {
      if (c & /*$service_details*/
      1 && n !== (n = /*type*/
      u[8] + "") && N(l, n), c & /*onclick, Object, $service_details*/
      3) {
        o = D(
          /*job*/
          u[9]
        );
        let f;
        for (f = 0; f < o.length; f += 1) {
          const _ = Ye(u, o, f);
          r[f] ? r[f].p(_, c) : (r[f] = et(_), r[f].c(), r[f].m(i.parentNode, i));
        }
        for (; f < r.length; f += 1)
          r[f].d(1);
        r.length = o.length;
      }
    },
    d(u) {
      u && (b(e), b(s), b(i)), V(r, u);
    }
  };
}
function nt(t) {
  let e, n = (
    /*key*/
    t[4] != "definition" && xe(t)
  );
  return {
    c() {
      n && n.c(), e = W();
    },
    m(l, s) {
      n && n.m(l, s), g(l, e, s);
    },
    p(l, s) {
      /*key*/
      l[4] != "definition" ? n ? n.p(l, s) : (n = xe(l), n.c(), n.m(e.parentNode, e)) : n && (n.d(1), n = null);
    },
    d(l) {
      l && b(e), n && n.d(l);
    }
  };
}
function Ut(t) {
  let e, n = (
    /*$service_details*/
    t[0] && Ze(t)
  );
  return {
    c() {
      n && n.c(), e = W();
    },
    m(l, s) {
      n && n.m(l, s), g(l, e, s);
    },
    p(l, [s]) {
      /*$service_details*/
      l[0] ? n ? n.p(l, s) : (n = Ze(l), n.c(), n.m(e.parentNode, e)) : n && (n.d(1), n = null);
    },
    i: E,
    o: E,
    d(l) {
      l && b(e), n && n.d(l);
    }
  };
}
function Ht(t, e, n) {
  let l, s, i;
  J(t, ce, (r) => n(2, l = r)), J(t, we, (r) => n(3, s = r)), J(t, Je, (r) => n(0, i = r));
  function o(r) {
    ce.set(r.target.innerText), Te(), ae("status", s, l, null);
  }
  return [i, o];
}
class Vt extends ie {
  constructor(e) {
    super(), se(this, e, Ht, Ut, H, {});
  }
}
function lt(t, e, n) {
  const l = t.slice();
  return l[2] = e[n], l[4] = n, l;
}
function st(t) {
  let e, n, l = (
    /*item*/
    t[2] + ""
  ), s;
  return {
    c() {
      e = d("li"), n = d("pre"), s = q(l), p(n, "class", "wrap");
    },
    m(i, o) {
      g(i, e, o), a(e, n), a(n, s);
    },
    p(i, o) {
      o & /*status*/
      1 && l !== (l = /*item*/
      i[2] + "") && N(s, l);
    },
    d(i) {
      i && b(e);
    }
  };
}
function it(t) {
  let e, n, l, s = (
    /*status*/
    t[0].error + ""
  ), i;
  return {
    c() {
      e = d("span"), e.textContent = "Error:", n = k(), l = d("span"), i = q(s), p(e, "class", "font-bold"), p(l, "class", "col-span-4 text-red-500");
    },
    m(o, r) {
      g(o, e, r), g(o, n, r), g(o, l, r), a(l, i);
    },
    p(o, r) {
      r & /*status*/
      1 && s !== (s = /*status*/
      o[0].error + "") && N(i, s);
    },
    d(o) {
      o && (b(e), b(n), b(l));
    }
  };
}
function Wt(t) {
  let e, n, l, s, i = (
    /*status*/
    t[0].id + ""
  ), o, r, u, c, f, _ = (
    /*status*/
    t[0].service + ""
  ), m, w, C, T, h, v, y, j, $, L, O = (
    /*status*/
    t[0].workerid + ""
  ), X, Ae, pe, De, _e, de = (
    /*status*/
    t[0].task + ""
  ), qe, Le, me, Be, he, oe, Pe, be, Me, ge, ve = (
    /*status*/
    t[0].result + ""
  ), Oe, ze, G = D(
    /*status*/
    t[0].updates
  ), R = [];
  for (let S = 0; S < G.length; S += 1)
    R[S] = st(lt(t, G, S));
  let A = (
    /*status*/
    t[0].error && it(t)
  );
  return {
    c() {
      e = d("div"), n = d("span"), n.textContent = "ID:", l = k(), s = d("span"), o = q(i), r = k(), u = d("span"), u.textContent = "Service:", c = k(), f = d("span"), m = q(_), w = k(), C = d("span"), C.textContent = "Status:", T = k(), h = d("span"), v = q(
        /*state*/
        t[1]
      ), y = k(), j = d("span"), j.textContent = "Worker:", $ = k(), L = d("span"), X = q(O), Ae = k(), pe = d("span"), pe.textContent = "Input:", De = k(), _e = d("span"), qe = q(de), Le = k(), me = d("span"), me.textContent = "Logs:", Be = k(), he = d("span"), oe = d("ul");
      for (let S = 0; S < R.length; S += 1)
        R[S].c();
      Pe = k(), be = d("span"), be.textContent = "Output:", Me = k(), ge = d("span"), Oe = q(ve), ze = k(), A && A.c(), p(n, "class", "font-bold"), p(s, "class", "col-span-4"), p(u, "class", "font-bold"), p(f, "class", "col-span-4"), p(C, "class", "font-bold"), p(h, "class", "col-span-4"), p(j, "class", "font-bold"), p(L, "class", "col-span-4"), p(pe, "class", "font-bold"), p(_e, "class", "col-span-4"), p(me, "class", "font-bold"), p(oe, "class", "my-8 text-sm flex flex-col justify-start"), p(he, "class", "col-span-4"), p(be, "class", "font-bold"), p(ge, "class", "col-span-4"), p(e, "class", "status svelte-1sy2uwb");
    },
    m(S, B) {
      g(S, e, B), a(e, n), a(e, l), a(e, s), a(s, o), a(e, r), a(e, u), a(e, c), a(e, f), a(f, m), a(e, w), a(e, C), a(e, T), a(e, h), a(h, v), a(e, y), a(e, j), a(e, $), a(e, L), a(L, X), a(e, Ae), a(e, pe), a(e, De), a(e, _e), a(_e, qe), a(e, Le), a(e, me), a(e, Be), a(e, he), a(he, oe);
      for (let I = 0; I < R.length; I += 1)
        R[I] && R[I].m(oe, null);
      a(e, Pe), a(e, be), a(e, Me), a(e, ge), a(ge, Oe), a(e, ze), A && A.m(e, null);
    },
    p(S, [B]) {
      if (B & /*status*/
      1 && i !== (i = /*status*/
      S[0].id + "") && N(o, i), B & /*status*/
      1 && _ !== (_ = /*status*/
      S[0].service + "") && N(m, _), B & /*state*/
      2 && N(
        v,
        /*state*/
        S[1]
      ), B & /*status*/
      1 && O !== (O = /*status*/
      S[0].workerid + "") && N(X, O), B & /*status*/
      1 && de !== (de = /*status*/
      S[0].task + "") && N(qe, de), B & /*status*/
      1) {
        G = D(
          /*status*/
          S[0].updates
        );
        let I;
        for (I = 0; I < G.length; I += 1) {
          const Fe = lt(S, G, I);
          R[I] ? R[I].p(Fe, B) : (R[I] = st(Fe), R[I].c(), R[I].m(oe, null));
        }
        for (; I < R.length; I += 1)
          R[I].d(1);
        R.length = G.length;
      }
      B & /*status*/
      1 && ve !== (ve = /*status*/
      S[0].result + "") && N(Oe, ve), /*status*/
      S[0].error ? A ? A.p(S, B) : (A = it(S), A.c(), A.m(e, null)) : A && (A.d(1), A = null);
    },
    i: E,
    o: E,
    d(S) {
      S && b(e), V(R, S), A && A.d();
    }
  };
}
function Xt(t, e, n) {
  let { status: l = {
    id: "job1",
    service: "echo",
    task: "hello",
    queued: !1,
    running: !1,
    complete: !0,
    cancelled: !1,
    abandoned: !1,
    workerid: "echo-worker",
    updates: ["Preparing response.", "Almost done.", "95% complete."],
    result: "hello"
  } } = e, s = "queue";
  return l.running ? s = "running" : l.complete ? s = "finished" : l.cancelled ? s = "cancelled" : l.abandoned && (s = "abandoned"), t.$$set = (i) => {
    "status" in i && n(0, l = i.status);
  }, [l, s];
}
class Gt extends ie {
  constructor(e) {
    super(), se(this, e, Xt, Wt, H, { status: 0 });
  }
}
function ot(t, e, n) {
  const l = t.slice();
  return l[2] = e[n], l[4] = n, l;
}
function rt(t) {
  let e, n = D(
    /*$service_list*/
    t[0]
  ), l = [];
  for (let s = 0; s < n.length; s += 1)
    l[s] = ut(ot(t, n, s));
  return {
    c() {
      e = d("ul");
      for (let s = 0; s < l.length; s += 1)
        l[s].c();
      p(e, "class", "svelte-1vfek8v");
    },
    m(s, i) {
      g(s, e, i);
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(e, null);
    },
    p(s, i) {
      if (i & /*onclick, $service_list*/
      3) {
        n = D(
          /*$service_list*/
          s[0]
        );
        let o;
        for (o = 0; o < n.length; o += 1) {
          const r = ot(s, n, o);
          l[o] ? l[o].p(r, i) : (l[o] = ut(r), l[o].c(), l[o].m(e, null));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = n.length;
      }
    },
    d(s) {
      s && b(e), V(l, s);
    }
  };
}
function ut(t) {
  let e, n = (
    /*item*/
    t[2] + ""
  ), l, s, i;
  return {
    c() {
      e = d("li"), l = q(n), p(e, "class", "hover:underline svelte-1vfek8v");
    },
    m(o, r) {
      g(o, e, r), a(e, l), s || (i = U(
        e,
        "click",
        /*onclick*/
        t[1]
      ), s = !0);
    },
    p(o, r) {
      r & /*$service_list*/
      1 && n !== (n = /*item*/
      o[2] + "") && N(l, n);
    },
    d(o) {
      o && b(e), s = !1, i();
    }
  };
}
function Kt(t) {
  let e, n = (
    /*$service_list*/
    t[0] && rt(t)
  );
  return {
    c() {
      n && n.c(), e = W();
    },
    m(l, s) {
      n && n.m(l, s), g(l, e, s);
    },
    p(l, [s]) {
      /*$service_list*/
      l[0] ? n ? n.p(l, s) : (n = rt(l), n.c(), n.m(e.parentNode, e)) : n && (n.d(1), n = null);
    },
    i: E,
    o: E,
    d(l) {
      l && b(e), n && n.d(l);
    }
  };
}
function Qt(t, e, n) {
  let l;
  J(t, Re, (i) => n(0, l = i));
  function s(i) {
    let o = i.target.innerText;
    ae("listsvc", o, null, null);
  }
  return [l, s];
}
class Yt extends ie {
  constructor(e) {
    super(), se(this, e, Qt, Kt, H, {});
  }
}
function ct(t, e, n) {
  const l = t.slice();
  return l[13] = e[n], l[14] = e, l[15] = n, l;
}
function ft(t, e, n) {
  const l = t.slice();
  return l[16] = e[n], l;
}
function Zt(t) {
  let e, n, l, s, i, o;
  function r() {
    t[7].call(
      e,
      /*field*/
      t[13]
    );
  }
  return {
    c() {
      e = d("input"), p(e, "type", "text"), p(e, "name", n = /*field*/
      t[13]), p(e, "placeholder", l = /*props*/
      t[1][
        /*field*/
        t[13]
      ].required), e.required = s = /*props*/
      t[1][
        /*field*/
        t[13]
      ].required == "Required", p(e, "class", "svelte-t7trdn");
    },
    m(u, c) {
      g(u, e, c), x(
        e,
        /*fields*/
        t[0][
          /*field*/
          t[13]
        ]
      ), i || (o = U(e, "input", r), i = !0);
    },
    p(u, c) {
      t = u, c & /*props, String, Object*/
      2 && n !== (n = /*field*/
      t[13]) && p(e, "name", n), c & /*props, String, Object*/
      2 && l !== (l = /*props*/
      t[1][
        /*field*/
        t[13]
      ].required) && p(e, "placeholder", l), c & /*props, String, Object*/
      2 && s !== (s = /*props*/
      t[1][
        /*field*/
        t[13]
      ].required == "Required") && (e.required = s), c & /*fields, Object, props, String*/
      3 && e.value !== /*fields*/
      t[0][
        /*field*/
        t[13]
      ] && x(
        e,
        /*fields*/
        t[0][
          /*field*/
          t[13]
        ]
      );
    },
    d(u) {
      u && b(e), i = !1, o();
    }
  };
}
function xt(t) {
  let e, n, l, s = D(
    /*props*/
    t[1][
      /*field*/
      t[13]
    ].choices
  ), i = [];
  for (let r = 0; r < s.length; r += 1)
    i[r] = at(ft(t, s, r));
  function o() {
    t[6].call(
      e,
      /*field*/
      t[13]
    );
  }
  return {
    c() {
      e = d("select");
      for (let r = 0; r < i.length; r += 1)
        i[r].c();
      p(e, "class", "svelte-t7trdn"), /*fields*/
      t[0][
        /*field*/
        t[13]
      ] === void 0 && $e(o);
    },
    m(r, u) {
      g(r, e, u);
      for (let c = 0; c < i.length; c += 1)
        i[c] && i[c].m(e, null);
      He(
        e,
        /*fields*/
        t[0][
          /*field*/
          t[13]
        ],
        !0
      ), n || (l = U(e, "change", o), n = !0);
    },
    p(r, u) {
      if (t = r, u & /*String, props, Object*/
      2) {
        s = D(
          /*props*/
          t[1][
            /*field*/
            t[13]
          ].choices
        );
        let c;
        for (c = 0; c < s.length; c += 1) {
          const f = ft(t, s, c);
          i[c] ? i[c].p(f, u) : (i[c] = at(f), i[c].c(), i[c].m(e, null));
        }
        for (; c < i.length; c += 1)
          i[c].d(1);
        i.length = s.length;
      }
      u & /*fields, Object, props, String*/
      3 && He(
        e,
        /*fields*/
        t[0][
          /*field*/
          t[13]
        ]
      );
    },
    d(r) {
      r && b(e), V(i, r), n = !1, l();
    }
  };
}
function at(t) {
  let e, n = String(
    /*choice*/
    t[16]
  ) + "", l, s;
  return {
    c() {
      e = d("option"), l = q(n), e.__value = s = String(
        /*choice*/
        t[16]
      ), x(e, e.__value);
    },
    m(i, o) {
      g(i, e, o), a(e, l);
    },
    p(i, o) {
      o & /*props*/
      2 && n !== (n = String(
        /*choice*/
        i[16]
      ) + "") && N(l, n), o & /*props, String, Object*/
      2 && s !== (s = String(
        /*choice*/
        i[16]
      )) && (e.__value = s, x(e, e.__value));
    },
    d(i) {
      i && b(e);
    }
  };
}
function pt(t) {
  let e, n, l = (
    /*field*/
    t[13] + ""
  ), s, i, o = (
    /*props*/
    t[1][
      /*field*/
      t[13]
    ].type + ""
  ), r, u, c, f, _, m = (
    /*props*/
    t[1][
      /*field*/
      t[13]
    ].help + ""
  ), w;
  function C(v, y) {
    return (
      /*props*/
      v[1][
        /*field*/
        v[13]
      ].choices ? xt : Zt
    );
  }
  let T = C(t), h = T(t);
  return {
    c() {
      e = d("div"), n = d("b"), s = q(l), i = q(" ["), r = q(o), u = q("]:"), c = k(), h.c(), f = k(), _ = d("p"), w = q(m), p(e, "class", "col-start-1 my-auto mr-auto"), p(_, "class", "col-start-2 col-span-3 mb-2 text-sm");
    },
    m(v, y) {
      g(v, e, y), a(e, n), a(n, s), a(e, i), a(e, r), a(e, u), g(v, c, y), h.m(v, y), g(v, f, y), g(v, _, y), a(_, w);
    },
    p(v, y) {
      y & /*props*/
      2 && l !== (l = /*field*/
      v[13] + "") && N(s, l), y & /*props*/
      2 && o !== (o = /*props*/
      v[1][
        /*field*/
        v[13]
      ].type + "") && N(r, o), T === (T = C(v)) && h ? h.p(v, y) : (h.d(1), h = T(v), h && (h.c(), h.m(f.parentNode, f))), y & /*props*/
      2 && m !== (m = /*props*/
      v[1][
        /*field*/
        v[13]
      ].help + "") && N(w, m);
    },
    d(v) {
      v && (b(e), b(c), b(f), b(_)), h.d(v);
    }
  };
}
function en(t) {
  let e, n, l, s = (
    /*service*/
    t[2].desc + ""
  ), i, o, r, u, c, f, _, m, w, C, T, h, v, y = D(Object.keys(
    /*props*/
    t[1]
  )), j = [];
  for (let $ = 0; $ < y.length; $ += 1)
    j[$] = pt(ct(t, y, $));
  return {
    c() {
      e = d("form"), n = d("div"), l = d("pre"), i = q(s), o = k(), r = d("h2"), r.textContent = "Job ID", u = k(), c = d("div"), f = d("input"), _ = k(), m = d("h2"), m.textContent = "Payload", w = k();
      for (let $ = 0; $ < j.length; $ += 1)
        j[$].c();
      C = k(), T = d("div"), T.innerHTML = '<input class="btn" type="submit" name="submit" value="Submit Job"/> <input class="btn" type="submit" name="status" value="Check Status"/> <input class="btn" type="submit" name="cancel" value="Cancel Job"/>', p(l, "class", "wrap"), p(n, "class", "col-span-5 py-2 text-slate-500 text-sm"), p(r, "class", "col-span-5 my-2 border-b"), p(f, "class", "col-start-2 col-span-3 mt-2 text-sm svelte-t7trdn"), p(f, "type", "text"), p(f, "placeholder", "Unique job ID"), f.required = !0, p(c, "class", "col-start-2 col-span-2"), p(m, "class", "col-span-5 mb-2 mt-4 border-b"), p(T, "class", "col-start-2 col-span-4 mt-2"), p(e, "class", "jobform svelte-t7trdn");
    },
    m($, L) {
      g($, e, L), a(e, n), a(n, l), a(l, i), a(e, o), a(e, r), a(e, u), a(e, c), a(c, f), x(
        f,
        /*$selected_job*/
        t[3]
      ), a(e, _), a(e, m), a(e, w);
      for (let O = 0; O < j.length; O += 1)
        j[O] && j[O].m(e, null);
      a(e, C), a(e, T), h || (v = [
        U(
          f,
          "input",
          /*input0_input_handler*/
          t[5]
        ),
        U(e, "submit", bt(
          /*handleRequest*/
          t[4]
        ))
      ], h = !0);
    },
    p($, [L]) {
      if (L & /*service*/
      4 && s !== (s = /*service*/
      $[2].desc + "") && N(i, s), L & /*$selected_job*/
      8 && f.value !== /*$selected_job*/
      $[3] && x(
        f,
        /*$selected_job*/
        $[3]
      ), L & /*props, Object, fields, String*/
      3) {
        y = D(Object.keys(
          /*props*/
          $[1]
        ));
        let O;
        for (O = 0; O < y.length; O += 1) {
          const X = ct($, y, O);
          j[O] ? j[O].p(X, L) : (j[O] = pt(X), j[O].c(), j[O].m(e, C));
        }
        for (; O < j.length; O += 1)
          j[O].d(1);
        j.length = y.length;
      }
    },
    i: E,
    o: E,
    d($) {
      $ && b(e), V(j, $), h = !1, te(v);
    }
  };
}
function tn(t, e, n) {
  let l, s, i, o, r;
  J(t, ce, (h) => n(3, l = h)), J(t, we, (h) => n(8, s = h)), J(t, ye, (h) => n(9, i = h)), J(t, Ee, (h) => n(10, o = h)), J(t, Se, (h) => n(11, r = h));
  let u = {}, c = JSON.parse(r), f = {}, _ = {};
  gt(() => {
    n(2, _.message = "", _), n(2, _.name = c.name, _), n(2, _.desc = c.desc, _), n(0, u = o);
    let h = c.fields;
    Object.entries(h).map((v, y) => {
      let j = v[0], $ = v[1];
      j in u || n(0, u[j] = "default" in $ ? String($.default) : "", u), n(
        1,
        f[j] = {
          type: $.type,
          help: $.help,
          required: $.required ? "Required" : "Optional",
          choices: $.choices ? $.choices : null
        },
        f
      );
    }), Ee.set(u);
  });
  function m(h) {
    Te();
    const { submitter: v } = h;
    if (v.name == "submit") {
      if (i && i.includes(l)) {
        ee.set("Please choose a new job ID.");
        return;
      }
      let y = {};
      Object.keys(f).forEach((j) => {
        y[j] = u[j];
      }), n(2, _.message = JSON.stringify(y), _);
    }
    Ee.set(u), ae(v.name, s, l, _.message);
  }
  function w() {
    l = this.value, ce.set(l);
  }
  function C(h) {
    u[h] = Ot(this), n(0, u), n(1, f);
  }
  function T(h) {
    u[h] = this.value, n(0, u), n(1, f);
  }
  return [
    u,
    f,
    _,
    l,
    m,
    w,
    C,
    T
  ];
}
class nn extends ie {
  constructor(e) {
    super(), se(this, e, tn, en, H, {});
  }
}
function _t(t) {
  let e, n;
  return {
    c() {
      e = d("h3"), n = q(
        /*$alert*/
        t[0]
      ), p(e, "class", "mx-auto text-red-500 w-full text-left px-10");
    },
    m(l, s) {
      g(l, e, s), a(e, n);
    },
    p(l, s) {
      s & /*$alert*/
      1 && N(
        n,
        /*$alert*/
        l[0]
      );
    },
    d(l) {
      l && b(e);
    }
  };
}
function ln(t) {
  let e, n;
  return e = new Yt({}), {
    c() {
      fe(e.$$.fragment);
    },
    m(l, s) {
      ne(e, l, s), n = !0;
    },
    p: E,
    i(l) {
      n || (P(e.$$.fragment, l), n = !0);
    },
    o(l) {
      z(e.$$.fragment, l), n = !1;
    },
    d(l) {
      le(e, l);
    }
  };
}
function sn(t) {
  let e, n, l, s = (
    /*$job_definition*/
    t[3] && dt()
  );
  return n = new Vt({}), {
    c() {
      s && s.c(), e = k(), fe(n.$$.fragment);
    },
    m(i, o) {
      s && s.m(i, o), g(i, e, o), ne(n, i, o), l = !0;
    },
    p(i, o) {
      /*$job_definition*/
      i[3] ? s ? o & /*$job_definition*/
      8 && P(s, 1) : (s = dt(), s.c(), P(s, 1), s.m(e.parentNode, e)) : s && (kt(), z(s, 1, 1, () => {
        s = null;
      }), $t());
    },
    i(i) {
      l || (P(s), P(n.$$.fragment, i), l = !0);
    },
    o(i) {
      z(s), z(n.$$.fragment, i), l = !1;
    },
    d(i) {
      i && b(e), s && s.d(i), le(n, i);
    }
  };
}
function on(t) {
  let e, n;
  return e = new Gt({
    props: { status: (
      /*$job_status*/
      t[1]
    ) }
  }), {
    c() {
      fe(e.$$.fragment);
    },
    m(l, s) {
      ne(e, l, s), n = !0;
    },
    p(l, s) {
      const i = {};
      s & /*$job_status*/
      2 && (i.status = /*$job_status*/
      l[1]), e.$set(i);
    },
    i(l) {
      n || (P(e.$$.fragment, l), n = !0);
    },
    o(l) {
      z(e.$$.fragment, l), n = !1;
    },
    d(l) {
      le(e, l);
    }
  };
}
function dt(t) {
  let e, n;
  return e = new nn({}), {
    c() {
      fe(e.$$.fragment);
    },
    m(l, s) {
      ne(e, l, s), n = !0;
    },
    i(l) {
      n || (P(e.$$.fragment, l), n = !0);
    },
    o(l) {
      z(e.$$.fragment, l), n = !1;
    },
    d(l) {
      le(e, l);
    }
  };
}
function rn(t) {
  let e, n, l, s, i, o, r;
  e = new Mt({});
  let u = (
    /*$alert*/
    t[0] && _t(t)
  );
  const c = [on, sn, ln], f = [];
  function _(m, w) {
    return (
      /*$job_status*/
      m[1] ? 0 : (
        /*$job_list*/
        m[2] ? 1 : 2
      )
    );
  }
  return s = _(t), i = f[s] = c[s](t), {
    c() {
      fe(e.$$.fragment), n = k(), u && u.c(), l = k(), i.c(), o = W();
    },
    m(m, w) {
      ne(e, m, w), g(m, n, w), u && u.m(m, w), g(m, l, w), f[s].m(m, w), g(m, o, w), r = !0;
    },
    p(m, [w]) {
      /*$alert*/
      m[0] ? u ? u.p(m, w) : (u = _t(m), u.c(), u.m(l.parentNode, l)) : u && (u.d(1), u = null);
      let C = s;
      s = _(m), s === C ? f[s].p(m, w) : (kt(), z(f[C], 1, 1, () => {
        f[C] = null;
      }), $t(), i = f[s], i ? i.p(m, w) : (i = f[s] = c[s](m), i.c()), P(i, 1), i.m(o.parentNode, o));
    },
    i(m) {
      r || (P(e.$$.fragment, m), P(i), r = !0);
    },
    o(m) {
      z(e.$$.fragment, m), z(i), r = !1;
    },
    d(m) {
      m && (b(n), b(l), b(o)), le(e, m), u && u.d(m), f[s].d(m);
    }
  };
}
function un(t, e, n) {
  let l, s, i, o;
  return J(t, ee, (r) => n(0, l = r)), J(t, je, (r) => n(1, s = r)), J(t, ye, (r) => n(2, i = r)), J(t, Se, (r) => n(3, o = r)), gt(() => {
    ae("listall", null, null, null);
  }), [l, s, i, o];
}
class cn extends ie {
  constructor(e) {
    super(), se(this, e, un, rn, H, {});
  }
}
const an = new cn({
  target: document.getElementById("app")
});
export {
  an as default
};
//# sourceMappingURL=main.js.map
