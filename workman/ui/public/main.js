var __defProp = Object.defineProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => {
  __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
  return value;
};
function noop() {
}
function run(fn) {
  return fn();
}
function blank_object() {
  return /* @__PURE__ */ Object.create(null);
}
function run_all(fns) {
  fns.forEach(run);
}
function is_function(thing) {
  return typeof thing === "function";
}
function safe_not_equal(a, b) {
  return a != a ? b == b : a !== b || a && typeof a === "object" || typeof a === "function";
}
function is_empty(obj) {
  return Object.keys(obj).length === 0;
}
function subscribe(store, ...callbacks) {
  if (store == null) {
    for (const callback of callbacks) {
      callback(void 0);
    }
    return noop;
  }
  const unsub = store.subscribe(...callbacks);
  return unsub.unsubscribe ? () => unsub.unsubscribe() : unsub;
}
function component_subscribe(component, store, callback) {
  component.$$.on_destroy.push(subscribe(store, callback));
}
function append(target, node) {
  target.appendChild(node);
}
function insert(target, node, anchor) {
  target.insertBefore(node, anchor || null);
}
function detach(node) {
  if (node.parentNode) {
    node.parentNode.removeChild(node);
  }
}
function destroy_each(iterations, detaching) {
  for (let i = 0; i < iterations.length; i += 1) {
    if (iterations[i])
      iterations[i].d(detaching);
  }
}
function element(name) {
  return document.createElement(name);
}
function text(data) {
  return document.createTextNode(data);
}
function space() {
  return text(" ");
}
function empty() {
  return text("");
}
function listen(node, event, handler, options) {
  node.addEventListener(event, handler, options);
  return () => node.removeEventListener(event, handler, options);
}
function prevent_default(fn) {
  return function(event) {
    event.preventDefault();
    return fn.call(this, event);
  };
}
function attr(node, attribute, value) {
  if (value == null)
    node.removeAttribute(attribute);
  else if (node.getAttribute(attribute) !== value)
    node.setAttribute(attribute, value);
}
function children(element2) {
  return Array.from(element2.childNodes);
}
function set_data(text2, data) {
  data = "" + data;
  if (text2.data === data)
    return;
  text2.data = /** @type {string} */
  data;
}
function set_input_value(input, value) {
  input.value = value == null ? "" : value;
}
function select_option(select, value, mounting) {
  for (let i = 0; i < select.options.length; i += 1) {
    const option = select.options[i];
    if (option.__value === value) {
      option.selected = true;
      return;
    }
  }
  if (!mounting || value !== void 0) {
    select.selectedIndex = -1;
  }
}
function select_value(select) {
  const selected_option = select.querySelector(":checked");
  return selected_option && selected_option.__value;
}
let current_component;
function set_current_component(component) {
  current_component = component;
}
function get_current_component() {
  if (!current_component)
    throw new Error("Function called outside component initialization");
  return current_component;
}
function onMount(fn) {
  get_current_component().$$.on_mount.push(fn);
}
const dirty_components = [];
const binding_callbacks = [];
let render_callbacks = [];
const flush_callbacks = [];
const resolved_promise = /* @__PURE__ */ Promise.resolve();
let update_scheduled = false;
function schedule_update() {
  if (!update_scheduled) {
    update_scheduled = true;
    resolved_promise.then(flush);
  }
}
function add_render_callback(fn) {
  render_callbacks.push(fn);
}
const seen_callbacks = /* @__PURE__ */ new Set();
let flushidx = 0;
function flush() {
  if (flushidx !== 0) {
    return;
  }
  const saved_component = current_component;
  do {
    try {
      while (flushidx < dirty_components.length) {
        const component = dirty_components[flushidx];
        flushidx++;
        set_current_component(component);
        update(component.$$);
      }
    } catch (e) {
      dirty_components.length = 0;
      flushidx = 0;
      throw e;
    }
    set_current_component(null);
    dirty_components.length = 0;
    flushidx = 0;
    while (binding_callbacks.length)
      binding_callbacks.pop()();
    for (let i = 0; i < render_callbacks.length; i += 1) {
      const callback = render_callbacks[i];
      if (!seen_callbacks.has(callback)) {
        seen_callbacks.add(callback);
        callback();
      }
    }
    render_callbacks.length = 0;
  } while (dirty_components.length);
  while (flush_callbacks.length) {
    flush_callbacks.pop()();
  }
  update_scheduled = false;
  seen_callbacks.clear();
  set_current_component(saved_component);
}
function update($$) {
  if ($$.fragment !== null) {
    $$.update();
    run_all($$.before_update);
    const dirty = $$.dirty;
    $$.dirty = [-1];
    $$.fragment && $$.fragment.p($$.ctx, dirty);
    $$.after_update.forEach(add_render_callback);
  }
}
function flush_render_callbacks(fns) {
  const filtered = [];
  const targets = [];
  render_callbacks.forEach((c) => fns.indexOf(c) === -1 ? filtered.push(c) : targets.push(c));
  targets.forEach((c) => c());
  render_callbacks = filtered;
}
const outroing = /* @__PURE__ */ new Set();
let outros;
function group_outros() {
  outros = {
    r: 0,
    c: [],
    p: outros
    // parent group
  };
}
function check_outros() {
  if (!outros.r) {
    run_all(outros.c);
  }
  outros = outros.p;
}
function transition_in(block, local) {
  if (block && block.i) {
    outroing.delete(block);
    block.i(local);
  }
}
function transition_out(block, local, detach2, callback) {
  if (block && block.o) {
    if (outroing.has(block))
      return;
    outroing.add(block);
    outros.c.push(() => {
      outroing.delete(block);
      if (callback) {
        if (detach2)
          block.d(1);
        callback();
      }
    });
    block.o(local);
  } else if (callback) {
    callback();
  }
}
function ensure_array_like(array_like_or_iterator) {
  return (array_like_or_iterator == null ? void 0 : array_like_or_iterator.length) !== void 0 ? array_like_or_iterator : Array.from(array_like_or_iterator);
}
function create_component(block) {
  block && block.c();
}
function mount_component(component, target, anchor) {
  const { fragment, after_update } = component.$$;
  fragment && fragment.m(target, anchor);
  add_render_callback(() => {
    const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
    if (component.$$.on_destroy) {
      component.$$.on_destroy.push(...new_on_destroy);
    } else {
      run_all(new_on_destroy);
    }
    component.$$.on_mount = [];
  });
  after_update.forEach(add_render_callback);
}
function destroy_component(component, detaching) {
  const $$ = component.$$;
  if ($$.fragment !== null) {
    flush_render_callbacks($$.after_update);
    run_all($$.on_destroy);
    $$.fragment && $$.fragment.d(detaching);
    $$.on_destroy = $$.fragment = null;
    $$.ctx = [];
  }
}
function make_dirty(component, i) {
  if (component.$$.dirty[0] === -1) {
    dirty_components.push(component);
    schedule_update();
    component.$$.dirty.fill(0);
  }
  component.$$.dirty[i / 31 | 0] |= 1 << i % 31;
}
function init(component, options, instance2, create_fragment2, not_equal, props, append_styles = null, dirty = [-1]) {
  const parent_component = current_component;
  set_current_component(component);
  const $$ = component.$$ = {
    fragment: null,
    ctx: [],
    // state
    props,
    update: noop,
    not_equal,
    bound: blank_object(),
    // lifecycle
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
    // everything else
    callbacks: blank_object(),
    dirty,
    skip_bound: false,
    root: options.target || parent_component.$$.root
  };
  append_styles && append_styles($$.root);
  let ready = false;
  $$.ctx = instance2 ? instance2(component, options.props || {}, (i, ret, ...rest) => {
    const value = rest.length ? rest[0] : ret;
    if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
      if (!$$.skip_bound && $$.bound[i])
        $$.bound[i](value);
      if (ready)
        make_dirty(component, i);
    }
    return ret;
  }) : [];
  $$.update();
  ready = true;
  run_all($$.before_update);
  $$.fragment = create_fragment2 ? create_fragment2($$.ctx) : false;
  if (options.target) {
    if (options.hydrate) {
      const nodes = children(options.target);
      $$.fragment && $$.fragment.l(nodes);
      nodes.forEach(detach);
    } else {
      $$.fragment && $$.fragment.c();
    }
    if (options.intro)
      transition_in(component.$$.fragment);
    mount_component(component, options.target, options.anchor);
    flush();
  }
  set_current_component(parent_component);
}
class SvelteComponent {
  constructor() {
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    __publicField(this, "$$");
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    __publicField(this, "$$set");
  }
  /** @returns {void} */
  $destroy() {
    destroy_component(this, 1);
    this.$destroy = noop;
  }
  /**
   * @template {Extract<keyof Events, string>} K
   * @param {K} type
   * @param {((e: Events[K]) => void) | null | undefined} callback
   * @returns {() => void}
   */
  $on(type, callback) {
    if (!is_function(callback)) {
      return noop;
    }
    const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
    callbacks.push(callback);
    return () => {
      const index = callbacks.indexOf(callback);
      if (index !== -1)
        callbacks.splice(index, 1);
    };
  }
  /**
   * @param {Partial<Props>} props
   * @returns {void}
   */
  $set(props) {
    if (this.$$set && !is_empty(props)) {
      this.$$.skip_bound = true;
      this.$$set(props);
      this.$$.skip_bound = false;
    }
  }
}
const PUBLIC_VERSION = "4";
if (typeof window !== "undefined")
  (window.__svelte || (window.__svelte = { v: /* @__PURE__ */ new Set() })).v.add(PUBLIC_VERSION);
const subscriber_queue = [];
function writable(value, start = noop) {
  let stop;
  const subscribers = /* @__PURE__ */ new Set();
  function set(new_value) {
    if (safe_not_equal(value, new_value)) {
      value = new_value;
      if (stop) {
        const run_queue = !subscriber_queue.length;
        for (const subscriber of subscribers) {
          subscriber[1]();
          subscriber_queue.push(subscriber, value);
        }
        if (run_queue) {
          for (let i = 0; i < subscriber_queue.length; i += 2) {
            subscriber_queue[i][0](subscriber_queue[i + 1]);
          }
          subscriber_queue.length = 0;
        }
      }
    }
  }
  function update2(fn) {
    set(fn(value));
  }
  function subscribe2(run2, invalidate = noop) {
    const subscriber = [run2, invalidate];
    subscribers.add(subscriber);
    if (subscribers.size === 1) {
      stop = start(set, update2) || noop;
    }
    run2(value);
    return () => {
      subscribers.delete(subscriber);
      if (subscribers.size === 0 && stop) {
        stop();
        stop = null;
      }
    };
  }
  return { set, update: update2, subscribe: subscribe2 };
}
const alert = writable("");
const selected_service = writable("");
const selected_job = writable("");
const service_list = writable(null);
const job_status = writable(null);
const job_list = writable(null);
const service_details = writable(null);
const last_response = writable(null);
const job_definition = writable(null);
const job_fields = writable({});
function clear() {
  alert.set("");
  job_status.set(null);
  job_list.set(null);
  service_details.set(null);
  service_list.set(null);
  job_definition.set(null);
}
async function postData(url = "", data = {}) {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const response = await fetch(url, {
    method: "POST",
    cache: "no-cache",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    mode: "same-origin"
  });
  return response.json();
}
function handle_response(action, response) {
  last_response.set(response);
  if (response["error"]) {
    alert.set(response["error"]);
    return;
  } else {
    alert.set("");
  }
  if (action == "submit") {
    job_status.set(response);
  } else if (action == "status") {
    job_status.set(response);
  } else if (action == "listall") {
    service_list.set(Object.keys(response));
  } else if (action == "listsvc") {
    service_details.set(response);
    let jobitems = [];
    for (var type in response["jobs"]) {
      jobitems = jobitems.concat(response["jobs"][type]);
    }
    job_list.set(jobitems);
    if (response["definition"]) {
      job_definition.set(response["definition"]);
    }
  } else {
    console.log("Response for unknown action:", action);
  }
}
function send(action, service, job, message) {
  let payload = {
    service,
    job,
    message,
    action
  };
  selected_service.set(service);
  postData("/main/", payload).then((data) => {
    handle_response(action, data);
  });
}
function create_if_block_1$2(ctx) {
  let input;
  let input_value_value;
  return {
    c() {
      input = element("input");
      attr(input, "class", "hover:underline px-2 cursor-pointer uppercase");
      attr(input, "type", "submit");
      attr(input, "name", "status");
      input.value = input_value_value = "Refresh " + /*$selected_job*/
      ctx[0];
    },
    m(target, anchor) {
      insert(target, input, anchor);
    },
    p(ctx2, dirty) {
      if (dirty & /*$selected_job*/
      1 && input_value_value !== (input_value_value = "Refresh " + /*$selected_job*/
      ctx2[0])) {
        input.value = input_value_value;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(input);
      }
    }
  };
}
function create_if_block$5(ctx) {
  let input;
  return {
    c() {
      input = element("input");
      attr(input, "class", "hover:underline px-2 cursor-pointer uppercase");
      attr(input, "type", "submit");
      attr(input, "name", "listsvc");
      input.value = /*$selected_service*/
      ctx[1];
    },
    m(target, anchor) {
      insert(target, input, anchor);
    },
    p(ctx2, dirty) {
      if (dirty & /*$selected_service*/
      2) {
        input.value = /*$selected_service*/
        ctx2[1];
      }
    },
    d(detaching) {
      if (detaching) {
        detach(input);
      }
    }
  };
}
function create_fragment$5(ctx) {
  let form;
  let div;
  let t0;
  let t1;
  let input;
  let mounted;
  let dispose;
  let if_block0 = (
    /*$selected_job*/
    ctx[0] && create_if_block_1$2(ctx)
  );
  let if_block1 = (
    /*$selected_service*/
    ctx[1] && create_if_block$5(ctx)
  );
  return {
    c() {
      form = element("form");
      div = element("div");
      if (if_block0)
        if_block0.c();
      t0 = space();
      if (if_block1)
        if_block1.c();
      t1 = space();
      input = element("input");
      attr(input, "class", "hover:underline px-2 cursor-pointer uppercase");
      attr(input, "type", "submit");
      attr(input, "name", "listall");
      input.value = "List All";
      attr(div, "class", "col-span-5 mx-auto");
      attr(form, "class", "topbar svelte-1usbfhw");
    },
    m(target, anchor) {
      insert(target, form, anchor);
      append(form, div);
      if (if_block0)
        if_block0.m(div, null);
      append(div, t0);
      if (if_block1)
        if_block1.m(div, null);
      append(div, t1);
      append(div, input);
      if (!mounted) {
        dispose = listen(form, "submit", prevent_default(
          /*handleRequest*/
          ctx[2]
        ));
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      if (
        /*$selected_job*/
        ctx2[0]
      ) {
        if (if_block0) {
          if_block0.p(ctx2, dirty);
        } else {
          if_block0 = create_if_block_1$2(ctx2);
          if_block0.c();
          if_block0.m(div, t0);
        }
      } else if (if_block0) {
        if_block0.d(1);
        if_block0 = null;
      }
      if (
        /*$selected_service*/
        ctx2[1]
      ) {
        if (if_block1) {
          if_block1.p(ctx2, dirty);
        } else {
          if_block1 = create_if_block$5(ctx2);
          if_block1.c();
          if_block1.m(div, t1);
        }
      } else if (if_block1) {
        if_block1.d(1);
        if_block1 = null;
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(form);
      }
      if (if_block0)
        if_block0.d();
      if (if_block1)
        if_block1.d();
      mounted = false;
      dispose();
    }
  };
}
function instance$5($$self, $$props, $$invalidate) {
  let $selected_job;
  let $selected_service;
  component_subscribe($$self, selected_job, ($$value) => $$invalidate(0, $selected_job = $$value));
  component_subscribe($$self, selected_service, ($$value) => $$invalidate(1, $selected_service = $$value));
  function handleRequest(event) {
    clear();
    const { submitter: submitButton } = event;
    if (submitButton.name == "listsvc" && $selected_service == "") {
      alert.set("Select a service from the list");
      return;
    }
    send(submitButton.name, $selected_service, $selected_job, "");
  }
  return [$selected_job, $selected_service, handleRequest];
}
class TopBar extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$5, create_fragment$5, safe_not_equal, {});
  }
}
function get_each_context$3(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[4] = list[i][0];
  child_ctx[5] = list[i][1];
  return child_ctx;
}
function get_each_context_1$1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[8] = list[i][0];
  child_ctx[9] = list[i][1];
  return child_ctx;
}
function get_each_context_2(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[12] = list[i];
  return child_ctx;
}
function create_if_block$4(ctx) {
  let div;
  let each_value = ensure_array_like(Object.entries(
    /*$service_details*/
    ctx[0]
  ));
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$3(get_each_context$3(ctx, each_value, i));
  }
  return {
    c() {
      div = element("div");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      attr(div, "class", "grid grid-cols-10 mx-auto w-11/12 my-3");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(div, null);
        }
      }
    },
    p(ctx2, dirty) {
      if (dirty & /*Object, $service_details, onclick*/
      3) {
        each_value = ensure_array_like(Object.entries(
          /*$service_details*/
          ctx2[0]
        ));
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$3(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block$3(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(div, null);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(div);
      }
      destroy_each(each_blocks, detaching);
    }
  };
}
function create_if_block_1$1(ctx) {
  let p;
  let t0_value = (
    /*key*/
    ctx[4] + ""
  );
  let t0;
  let t1;
  let each_1_anchor;
  let each_value_1 = ensure_array_like(Object.entries(
    /*value*/
    ctx[5]
  ));
  let each_blocks = [];
  for (let i = 0; i < each_value_1.length; i += 1) {
    each_blocks[i] = create_each_block_1$1(get_each_context_1$1(ctx, each_value_1, i));
  }
  return {
    c() {
      p = element("p");
      t0 = text(t0_value);
      t1 = space();
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      each_1_anchor = empty();
      attr(p, "class", "col-start-1 col-span-9 font-bold border-b pt-2 pb-1 mt-1");
    },
    m(target, anchor) {
      insert(target, p, anchor);
      append(p, t0);
      insert(target, t1, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(target, anchor);
        }
      }
      insert(target, each_1_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (dirty & /*$service_details*/
      1 && t0_value !== (t0_value = /*key*/
      ctx2[4] + ""))
        set_data(t0, t0_value);
      if (dirty & /*Object, $service_details, onclick*/
      3) {
        each_value_1 = ensure_array_like(Object.entries(
          /*value*/
          ctx2[5]
        ));
        let i;
        for (i = 0; i < each_value_1.length; i += 1) {
          const child_ctx = get_each_context_1$1(ctx2, each_value_1, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block_1$1(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(each_1_anchor.parentNode, each_1_anchor);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value_1.length;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(p);
        detach(t1);
        detach(each_1_anchor);
      }
      destroy_each(each_blocks, detaching);
    }
  };
}
function create_else_block$2(ctx) {
  let p;
  let t0_value = (
    /*jobname*/
    ctx[12] + ""
  );
  let t0;
  let t1;
  return {
    c() {
      p = element("p");
      t0 = text(t0_value);
      t1 = space();
      attr(p, "class", "col-start-4 col-span-5 pb-1");
    },
    m(target, anchor) {
      insert(target, p, anchor);
      append(p, t0);
      append(p, t1);
    },
    p(ctx2, dirty) {
      if (dirty & /*$service_details*/
      1 && t0_value !== (t0_value = /*jobname*/
      ctx2[12] + ""))
        set_data(t0, t0_value);
    },
    d(detaching) {
      if (detaching) {
        detach(p);
      }
    }
  };
}
function create_if_block_2$1(ctx) {
  let p;
  let t0_value = (
    /*jobname*/
    ctx[12] + ""
  );
  let t0;
  let t1;
  let mounted;
  let dispose;
  return {
    c() {
      p = element("p");
      t0 = text(t0_value);
      t1 = space();
      attr(p, "class", "col-start-4 col-span-5 pb-1 cursor-pointer hover:underline");
    },
    m(target, anchor) {
      insert(target, p, anchor);
      append(p, t0);
      append(p, t1);
      if (!mounted) {
        dispose = listen(
          p,
          "click",
          /*onclick*/
          ctx[1]
        );
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (dirty & /*$service_details*/
      1 && t0_value !== (t0_value = /*jobname*/
      ctx2[12] + ""))
        set_data(t0, t0_value);
    },
    d(detaching) {
      if (detaching) {
        detach(p);
      }
      mounted = false;
      dispose();
    }
  };
}
function create_each_block_2(ctx) {
  let if_block_anchor;
  function select_block_type(ctx2, dirty) {
    if (
      /*key*/
      ctx2[4] == "jobs"
    )
      return create_if_block_2$1;
    return create_else_block$2;
  }
  let current_block_type = select_block_type(ctx);
  let if_block = current_block_type(ctx);
  return {
    c() {
      if_block.c();
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if_block.m(target, anchor);
      insert(target, if_block_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (current_block_type === (current_block_type = select_block_type(ctx2)) && if_block) {
        if_block.p(ctx2, dirty);
      } else {
        if_block.d(1);
        if_block = current_block_type(ctx2);
        if (if_block) {
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      }
    },
    d(detaching) {
      if (detaching) {
        detach(if_block_anchor);
      }
      if_block.d(detaching);
    }
  };
}
function create_each_block_1$1(ctx) {
  let p;
  let t0_value = (
    /*type*/
    ctx[8] + ""
  );
  let t0;
  let t1;
  let each_1_anchor;
  let each_value_2 = ensure_array_like(
    /*job*/
    ctx[9]
  );
  let each_blocks = [];
  for (let i = 0; i < each_value_2.length; i += 1) {
    each_blocks[i] = create_each_block_2(get_each_context_2(ctx, each_value_2, i));
  }
  return {
    c() {
      p = element("p");
      t0 = text(t0_value);
      t1 = space();
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      each_1_anchor = empty();
      attr(p, "class", "col-start-2 col-span-8 pb-2");
    },
    m(target, anchor) {
      insert(target, p, anchor);
      append(p, t0);
      insert(target, t1, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(target, anchor);
        }
      }
      insert(target, each_1_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (dirty & /*$service_details*/
      1 && t0_value !== (t0_value = /*type*/
      ctx2[8] + ""))
        set_data(t0, t0_value);
      if (dirty & /*onclick, Object, $service_details*/
      3) {
        each_value_2 = ensure_array_like(
          /*job*/
          ctx2[9]
        );
        let i;
        for (i = 0; i < each_value_2.length; i += 1) {
          const child_ctx = get_each_context_2(ctx2, each_value_2, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block_2(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(each_1_anchor.parentNode, each_1_anchor);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value_2.length;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(p);
        detach(t1);
        detach(each_1_anchor);
      }
      destroy_each(each_blocks, detaching);
    }
  };
}
function create_each_block$3(ctx) {
  let if_block_anchor;
  let if_block = (
    /*key*/
    ctx[4] != "definition" && create_if_block_1$1(ctx)
  );
  return {
    c() {
      if (if_block)
        if_block.c();
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if (if_block)
        if_block.m(target, anchor);
      insert(target, if_block_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (
        /*key*/
        ctx2[4] != "definition"
      ) {
        if (if_block) {
          if_block.p(ctx2, dirty);
        } else {
          if_block = create_if_block_1$1(ctx2);
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(if_block_anchor);
      }
      if (if_block)
        if_block.d(detaching);
    }
  };
}
function create_fragment$4(ctx) {
  let if_block_anchor;
  let if_block = (
    /*$service_details*/
    ctx[0] && create_if_block$4(ctx)
  );
  return {
    c() {
      if (if_block)
        if_block.c();
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if (if_block)
        if_block.m(target, anchor);
      insert(target, if_block_anchor, anchor);
    },
    p(ctx2, [dirty]) {
      if (
        /*$service_details*/
        ctx2[0]
      ) {
        if (if_block) {
          if_block.p(ctx2, dirty);
        } else {
          if_block = create_if_block$4(ctx2);
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(if_block_anchor);
      }
      if (if_block)
        if_block.d(detaching);
    }
  };
}
function instance$4($$self, $$props, $$invalidate) {
  let $selected_job;
  let $selected_service;
  let $service_details;
  component_subscribe($$self, selected_job, ($$value) => $$invalidate(2, $selected_job = $$value));
  component_subscribe($$self, selected_service, ($$value) => $$invalidate(3, $selected_service = $$value));
  component_subscribe($$self, service_details, ($$value) => $$invalidate(0, $service_details = $$value));
  function onclick(ev) {
    selected_job.set(ev.target.innerText);
    clear();
    send("status", $selected_service, $selected_job, null);
  }
  return [$service_details, onclick];
}
class ServiceDetails extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$4, create_fragment$4, safe_not_equal, {});
  }
}
function get_each_context$2(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[2] = list[i];
  child_ctx[4] = i;
  return child_ctx;
}
function create_each_block$2(ctx) {
  let li;
  let pre;
  let t_value = (
    /*item*/
    ctx[2] + ""
  );
  let t;
  return {
    c() {
      li = element("li");
      pre = element("pre");
      t = text(t_value);
      attr(pre, "class", "wrap");
    },
    m(target, anchor) {
      insert(target, li, anchor);
      append(li, pre);
      append(pre, t);
    },
    p(ctx2, dirty) {
      if (dirty & /*status*/
      1 && t_value !== (t_value = /*item*/
      ctx2[2] + ""))
        set_data(t, t_value);
    },
    d(detaching) {
      if (detaching) {
        detach(li);
      }
    }
  };
}
function create_if_block$3(ctx) {
  let span0;
  let t1;
  let span1;
  let t2_value = (
    /*status*/
    ctx[0]["error"] + ""
  );
  let t2;
  return {
    c() {
      span0 = element("span");
      span0.textContent = "Error:";
      t1 = space();
      span1 = element("span");
      t2 = text(t2_value);
      attr(span0, "class", "font-bold");
      attr(span1, "class", "col-span-4 text-red-500");
    },
    m(target, anchor) {
      insert(target, span0, anchor);
      insert(target, t1, anchor);
      insert(target, span1, anchor);
      append(span1, t2);
    },
    p(ctx2, dirty) {
      if (dirty & /*status*/
      1 && t2_value !== (t2_value = /*status*/
      ctx2[0]["error"] + ""))
        set_data(t2, t2_value);
    },
    d(detaching) {
      if (detaching) {
        detach(span0);
        detach(t1);
        detach(span1);
      }
    }
  };
}
function create_fragment$3(ctx) {
  let div;
  let span0;
  let t1;
  let span1;
  let t2_value = (
    /*status*/
    ctx[0]["id"] + ""
  );
  let t2;
  let t3;
  let span2;
  let t5;
  let span3;
  let t6_value = (
    /*status*/
    ctx[0]["service"] + ""
  );
  let t6;
  let t7;
  let span4;
  let t9;
  let span5;
  let t10;
  let t11;
  let span6;
  let t13;
  let span7;
  let t14_value = (
    /*status*/
    ctx[0]["workerid"] + ""
  );
  let t14;
  let t15;
  let span8;
  let t17;
  let span9;
  let t18_value = (
    /*status*/
    ctx[0]["task"] + ""
  );
  let t18;
  let t19;
  let span10;
  let t21;
  let span11;
  let ul;
  let t22;
  let span12;
  let t24;
  let span13;
  let t25_value = (
    /*status*/
    ctx[0]["result"] + ""
  );
  let t25;
  let t26;
  let each_value = ensure_array_like(
    /*status*/
    ctx[0]["updates"]
  );
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$2(get_each_context$2(ctx, each_value, i));
  }
  let if_block = (
    /*status*/
    ctx[0]["error"] && create_if_block$3(ctx)
  );
  return {
    c() {
      div = element("div");
      span0 = element("span");
      span0.textContent = "ID:";
      t1 = space();
      span1 = element("span");
      t2 = text(t2_value);
      t3 = space();
      span2 = element("span");
      span2.textContent = "Service:";
      t5 = space();
      span3 = element("span");
      t6 = text(t6_value);
      t7 = space();
      span4 = element("span");
      span4.textContent = "Status:";
      t9 = space();
      span5 = element("span");
      t10 = text(
        /*state*/
        ctx[1]
      );
      t11 = space();
      span6 = element("span");
      span6.textContent = "Worker:";
      t13 = space();
      span7 = element("span");
      t14 = text(t14_value);
      t15 = space();
      span8 = element("span");
      span8.textContent = "Input:";
      t17 = space();
      span9 = element("span");
      t18 = text(t18_value);
      t19 = space();
      span10 = element("span");
      span10.textContent = "Logs:";
      t21 = space();
      span11 = element("span");
      ul = element("ul");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      t22 = space();
      span12 = element("span");
      span12.textContent = "Output:";
      t24 = space();
      span13 = element("span");
      t25 = text(t25_value);
      t26 = space();
      if (if_block)
        if_block.c();
      attr(span0, "class", "font-bold");
      attr(span1, "class", "col-span-4");
      attr(span2, "class", "font-bold");
      attr(span3, "class", "col-span-4");
      attr(span4, "class", "font-bold");
      attr(span5, "class", "col-span-4");
      attr(span6, "class", "font-bold");
      attr(span7, "class", "col-span-4");
      attr(span8, "class", "font-bold");
      attr(span9, "class", "col-span-4");
      attr(span10, "class", "font-bold");
      attr(ul, "class", "my-8 text-sm flex flex-col justify-start");
      attr(span11, "class", "col-span-4");
      attr(span12, "class", "font-bold");
      attr(span13, "class", "col-span-4");
      attr(div, "class", "status svelte-1sy2uwb");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      append(div, span0);
      append(div, t1);
      append(div, span1);
      append(span1, t2);
      append(div, t3);
      append(div, span2);
      append(div, t5);
      append(div, span3);
      append(span3, t6);
      append(div, t7);
      append(div, span4);
      append(div, t9);
      append(div, span5);
      append(span5, t10);
      append(div, t11);
      append(div, span6);
      append(div, t13);
      append(div, span7);
      append(span7, t14);
      append(div, t15);
      append(div, span8);
      append(div, t17);
      append(div, span9);
      append(span9, t18);
      append(div, t19);
      append(div, span10);
      append(div, t21);
      append(div, span11);
      append(span11, ul);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(ul, null);
        }
      }
      append(div, t22);
      append(div, span12);
      append(div, t24);
      append(div, span13);
      append(span13, t25);
      append(div, t26);
      if (if_block)
        if_block.m(div, null);
    },
    p(ctx2, [dirty]) {
      if (dirty & /*status*/
      1 && t2_value !== (t2_value = /*status*/
      ctx2[0]["id"] + ""))
        set_data(t2, t2_value);
      if (dirty & /*status*/
      1 && t6_value !== (t6_value = /*status*/
      ctx2[0]["service"] + ""))
        set_data(t6, t6_value);
      if (dirty & /*state*/
      2)
        set_data(
          t10,
          /*state*/
          ctx2[1]
        );
      if (dirty & /*status*/
      1 && t14_value !== (t14_value = /*status*/
      ctx2[0]["workerid"] + ""))
        set_data(t14, t14_value);
      if (dirty & /*status*/
      1 && t18_value !== (t18_value = /*status*/
      ctx2[0]["task"] + ""))
        set_data(t18, t18_value);
      if (dirty & /*status*/
      1) {
        each_value = ensure_array_like(
          /*status*/
          ctx2[0]["updates"]
        );
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$2(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block$2(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(ul, null);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
      if (dirty & /*status*/
      1 && t25_value !== (t25_value = /*status*/
      ctx2[0]["result"] + ""))
        set_data(t25, t25_value);
      if (
        /*status*/
        ctx2[0]["error"]
      ) {
        if (if_block) {
          if_block.p(ctx2, dirty);
        } else {
          if_block = create_if_block$3(ctx2);
          if_block.c();
          if_block.m(div, null);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(div);
      }
      destroy_each(each_blocks, detaching);
      if (if_block)
        if_block.d();
    }
  };
}
function instance$3($$self, $$props, $$invalidate) {
  let { status = {
    id: "job1",
    service: "echo",
    task: "hello",
    queued: false,
    running: false,
    complete: true,
    cancelled: false,
    abandoned: false,
    workerid: "echo-worker",
    updates: ["Preparing response.", "Almost done.", "95% complete."],
    result: "hello"
  } } = $$props;
  let state = "queue";
  if (status["running"]) {
    state = "running";
  } else if (status["complete"]) {
    state = "finished";
  } else if (status["cancelled"]) {
    state = "cancelled";
  } else if (status["abandoned"]) {
    state = "abandoned";
  }
  $$self.$$set = ($$props2) => {
    if ("status" in $$props2)
      $$invalidate(0, status = $$props2.status);
  };
  return [status, state];
}
class JobStatus extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$3, create_fragment$3, safe_not_equal, { status: 0 });
  }
}
function get_each_context$1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[2] = list[i];
  child_ctx[4] = i;
  return child_ctx;
}
function create_if_block$2(ctx) {
  let ul;
  let each_value = ensure_array_like(
    /*$service_list*/
    ctx[0]
  );
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block$1(get_each_context$1(ctx, each_value, i));
  }
  return {
    c() {
      ul = element("ul");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      attr(ul, "class", "svelte-1vfek8v");
    },
    m(target, anchor) {
      insert(target, ul, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(ul, null);
        }
      }
    },
    p(ctx2, dirty) {
      if (dirty & /*onclick, $service_list*/
      3) {
        each_value = ensure_array_like(
          /*$service_list*/
          ctx2[0]
        );
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context$1(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block$1(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(ul, null);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(ul);
      }
      destroy_each(each_blocks, detaching);
    }
  };
}
function create_each_block$1(ctx) {
  let li;
  let t_value = (
    /*item*/
    ctx[2] + ""
  );
  let t;
  let mounted;
  let dispose;
  return {
    c() {
      li = element("li");
      t = text(t_value);
      attr(li, "class", "hover:underline svelte-1vfek8v");
    },
    m(target, anchor) {
      insert(target, li, anchor);
      append(li, t);
      if (!mounted) {
        dispose = listen(
          li,
          "click",
          /*onclick*/
          ctx[1]
        );
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (dirty & /*$service_list*/
      1 && t_value !== (t_value = /*item*/
      ctx2[2] + ""))
        set_data(t, t_value);
    },
    d(detaching) {
      if (detaching) {
        detach(li);
      }
      mounted = false;
      dispose();
    }
  };
}
function create_fragment$2(ctx) {
  let if_block_anchor;
  let if_block = (
    /*$service_list*/
    ctx[0] && create_if_block$2(ctx)
  );
  return {
    c() {
      if (if_block)
        if_block.c();
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if (if_block)
        if_block.m(target, anchor);
      insert(target, if_block_anchor, anchor);
    },
    p(ctx2, [dirty]) {
      if (
        /*$service_list*/
        ctx2[0]
      ) {
        if (if_block) {
          if_block.p(ctx2, dirty);
        } else {
          if_block = create_if_block$2(ctx2);
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(if_block_anchor);
      }
      if (if_block)
        if_block.d(detaching);
    }
  };
}
function instance$2($$self, $$props, $$invalidate) {
  let $service_list;
  component_subscribe($$self, service_list, ($$value) => $$invalidate(0, $service_list = $$value));
  function onclick(ev) {
    let service = ev.target.innerText;
    send("listsvc", service, null, null);
  }
  return [$service_list, onclick];
}
class ServiceList extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$2, create_fragment$2, safe_not_equal, {});
  }
}
function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[13] = list[i];
  child_ctx[14] = list;
  child_ctx[15] = i;
  return child_ctx;
}
function get_each_context_1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[16] = list[i];
  return child_ctx;
}
function create_else_block$1(ctx) {
  let input;
  let input_name_value;
  let input_placeholder_value;
  let input_required_value;
  let mounted;
  let dispose;
  function input_input_handler() {
    ctx[7].call(
      input,
      /*field*/
      ctx[13]
    );
  }
  return {
    c() {
      input = element("input");
      attr(input, "type", "text");
      attr(input, "name", input_name_value = /*field*/
      ctx[13]);
      attr(input, "placeholder", input_placeholder_value = /*props*/
      ctx[1][
        /*field*/
        ctx[13]
      ].required);
      input.required = input_required_value = /*props*/
      ctx[1][
        /*field*/
        ctx[13]
      ].required == "Required";
      attr(input, "class", "svelte-1pnm85l");
    },
    m(target, anchor) {
      insert(target, input, anchor);
      set_input_value(
        input,
        /*fields*/
        ctx[0][
          /*field*/
          ctx[13]
        ]
      );
      if (!mounted) {
        dispose = listen(input, "input", input_input_handler);
        mounted = true;
      }
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty & /*props, String, Object*/
      2 && input_name_value !== (input_name_value = /*field*/
      ctx[13])) {
        attr(input, "name", input_name_value);
      }
      if (dirty & /*props, String, Object*/
      2 && input_placeholder_value !== (input_placeholder_value = /*props*/
      ctx[1][
        /*field*/
        ctx[13]
      ].required)) {
        attr(input, "placeholder", input_placeholder_value);
      }
      if (dirty & /*props, String, Object*/
      2 && input_required_value !== (input_required_value = /*props*/
      ctx[1][
        /*field*/
        ctx[13]
      ].required == "Required")) {
        input.required = input_required_value;
      }
      if (dirty & /*fields, Object, props, String*/
      3 && input.value !== /*fields*/
      ctx[0][
        /*field*/
        ctx[13]
      ]) {
        set_input_value(
          input,
          /*fields*/
          ctx[0][
            /*field*/
            ctx[13]
          ]
        );
      }
    },
    d(detaching) {
      if (detaching) {
        detach(input);
      }
      mounted = false;
      dispose();
    }
  };
}
function create_if_block$1(ctx) {
  let select;
  let mounted;
  let dispose;
  let each_value_1 = ensure_array_like(
    /*props*/
    ctx[1][
      /*field*/
      ctx[13]
    ].choices
  );
  let each_blocks = [];
  for (let i = 0; i < each_value_1.length; i += 1) {
    each_blocks[i] = create_each_block_1(get_each_context_1(ctx, each_value_1, i));
  }
  function select_change_handler() {
    ctx[6].call(
      select,
      /*field*/
      ctx[13]
    );
  }
  return {
    c() {
      select = element("select");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      attr(select, "class", "svelte-1pnm85l");
      if (
        /*fields*/
        ctx[0][
          /*field*/
          ctx[13]
        ] === void 0
      )
        add_render_callback(select_change_handler);
    },
    m(target, anchor) {
      insert(target, select, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(select, null);
        }
      }
      select_option(
        select,
        /*fields*/
        ctx[0][
          /*field*/
          ctx[13]
        ],
        true
      );
      if (!mounted) {
        dispose = listen(select, "change", select_change_handler);
        mounted = true;
      }
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty & /*String, props, Object*/
      2) {
        each_value_1 = ensure_array_like(
          /*props*/
          ctx[1][
            /*field*/
            ctx[13]
          ].choices
        );
        let i;
        for (i = 0; i < each_value_1.length; i += 1) {
          const child_ctx = get_each_context_1(ctx, each_value_1, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block_1(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(select, null);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value_1.length;
      }
      if (dirty & /*fields, Object, props, String*/
      3) {
        select_option(
          select,
          /*fields*/
          ctx[0][
            /*field*/
            ctx[13]
          ]
        );
      }
    },
    d(detaching) {
      if (detaching) {
        detach(select);
      }
      destroy_each(each_blocks, detaching);
      mounted = false;
      dispose();
    }
  };
}
function create_each_block_1(ctx) {
  let option;
  let t_value = String(
    /*choice*/
    ctx[16]
  ) + "";
  let t;
  let option_value_value;
  return {
    c() {
      option = element("option");
      t = text(t_value);
      option.__value = option_value_value = String(
        /*choice*/
        ctx[16]
      );
      set_input_value(option, option.__value);
    },
    m(target, anchor) {
      insert(target, option, anchor);
      append(option, t);
    },
    p(ctx2, dirty) {
      if (dirty & /*props*/
      2 && t_value !== (t_value = String(
        /*choice*/
        ctx2[16]
      ) + ""))
        set_data(t, t_value);
      if (dirty & /*props, String, Object*/
      2 && option_value_value !== (option_value_value = String(
        /*choice*/
        ctx2[16]
      ))) {
        option.__value = option_value_value;
        set_input_value(option, option.__value);
      }
    },
    d(detaching) {
      if (detaching) {
        detach(option);
      }
    }
  };
}
function create_each_block(ctx) {
  let div;
  let b;
  let t0_value = (
    /*field*/
    ctx[13] + ""
  );
  let t0;
  let t1;
  let t2_value = (
    /*props*/
    ctx[1][
      /*field*/
      ctx[13]
    ].type + ""
  );
  let t2;
  let t3;
  let t4;
  let t5;
  let p;
  let t6_value = (
    /*props*/
    ctx[1][
      /*field*/
      ctx[13]
    ].help + ""
  );
  let t6;
  function select_block_type(ctx2, dirty) {
    if (
      /*props*/
      ctx2[1][
        /*field*/
        ctx2[13]
      ].choices
    )
      return create_if_block$1;
    return create_else_block$1;
  }
  let current_block_type = select_block_type(ctx);
  let if_block = current_block_type(ctx);
  return {
    c() {
      div = element("div");
      b = element("b");
      t0 = text(t0_value);
      t1 = text(" [");
      t2 = text(t2_value);
      t3 = text("]:");
      t4 = space();
      if_block.c();
      t5 = space();
      p = element("p");
      t6 = text(t6_value);
      attr(div, "class", "col-start-1 my-auto mr-auto");
      attr(p, "class", "col-start-2 col-span-3 mb-2 text-sm");
    },
    m(target, anchor) {
      insert(target, div, anchor);
      append(div, b);
      append(b, t0);
      append(div, t1);
      append(div, t2);
      append(div, t3);
      insert(target, t4, anchor);
      if_block.m(target, anchor);
      insert(target, t5, anchor);
      insert(target, p, anchor);
      append(p, t6);
    },
    p(ctx2, dirty) {
      if (dirty & /*props*/
      2 && t0_value !== (t0_value = /*field*/
      ctx2[13] + ""))
        set_data(t0, t0_value);
      if (dirty & /*props*/
      2 && t2_value !== (t2_value = /*props*/
      ctx2[1][
        /*field*/
        ctx2[13]
      ].type + ""))
        set_data(t2, t2_value);
      if (current_block_type === (current_block_type = select_block_type(ctx2)) && if_block) {
        if_block.p(ctx2, dirty);
      } else {
        if_block.d(1);
        if_block = current_block_type(ctx2);
        if (if_block) {
          if_block.c();
          if_block.m(t5.parentNode, t5);
        }
      }
      if (dirty & /*props*/
      2 && t6_value !== (t6_value = /*props*/
      ctx2[1][
        /*field*/
        ctx2[13]
      ].help + ""))
        set_data(t6, t6_value);
    },
    d(detaching) {
      if (detaching) {
        detach(div);
        detach(t4);
        detach(t5);
        detach(p);
      }
      if_block.d(detaching);
    }
  };
}
function create_fragment$1(ctx) {
  let form;
  let div0;
  let pre;
  let t0_value = (
    /*service*/
    ctx[2].desc + ""
  );
  let t0;
  let t1;
  let h20;
  let t3;
  let div1;
  let input0;
  let t4;
  let h21;
  let t6;
  let t7;
  let div2;
  let mounted;
  let dispose;
  let each_value = ensure_array_like(Object.keys(
    /*props*/
    ctx[1]
  ));
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
  }
  return {
    c() {
      form = element("form");
      div0 = element("div");
      pre = element("pre");
      t0 = text(t0_value);
      t1 = space();
      h20 = element("h2");
      h20.textContent = "Job ID";
      t3 = space();
      div1 = element("div");
      input0 = element("input");
      t4 = space();
      h21 = element("h2");
      h21.textContent = "Payload";
      t6 = space();
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      t7 = space();
      div2 = element("div");
      div2.innerHTML = `<input class="btn" type="submit" name="submit" value="Submit Job"/> <input class="btn" type="submit" name="status" value="Check Status"/> <input class="btn" type="submit" name="cancel" value="Cancel Job"/>`;
      attr(pre, "class", "wrap");
      attr(div0, "class", "col-span-5 py-2 text-slate-500 text-sm");
      attr(h20, "class", "col-span-5 my-2 border-b");
      attr(input0, "class", "col-start-2 col-span-3 mt-2 text-sm svelte-1pnm85l");
      attr(input0, "type", "text");
      attr(input0, "placeholder", "Unique job ID");
      input0.required = true;
      attr(div1, "class", "col-start-2 col-span-2");
      attr(h21, "class", "col-span-5 mb-2 mt-4 border-b");
      attr(div2, "class", "col-start-2 col-span-4 mt-2");
      attr(form, "class", "jobform svelte-1pnm85l");
    },
    m(target, anchor) {
      insert(target, form, anchor);
      append(form, div0);
      append(div0, pre);
      append(pre, t0);
      append(form, t1);
      append(form, h20);
      append(form, t3);
      append(form, div1);
      append(div1, input0);
      set_input_value(
        input0,
        /*$selected_job*/
        ctx[3]
      );
      append(form, t4);
      append(form, h21);
      append(form, t6);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(form, null);
        }
      }
      append(form, t7);
      append(form, div2);
      if (!mounted) {
        dispose = [
          listen(
            input0,
            "input",
            /*input0_input_handler*/
            ctx[5]
          ),
          listen(form, "submit", prevent_default(
            /*handleRequest*/
            ctx[4]
          ))
        ];
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      if (dirty & /*service*/
      4 && t0_value !== (t0_value = /*service*/
      ctx2[2].desc + ""))
        set_data(t0, t0_value);
      if (dirty & /*$selected_job*/
      8 && input0.value !== /*$selected_job*/
      ctx2[3]) {
        set_input_value(
          input0,
          /*$selected_job*/
          ctx2[3]
        );
      }
      if (dirty & /*props, Object, fields, String*/
      3) {
        each_value = ensure_array_like(Object.keys(
          /*props*/
          ctx2[1]
        ));
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(form, t7);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(form);
      }
      destroy_each(each_blocks, detaching);
      mounted = false;
      run_all(dispose);
    }
  };
}
function instance$1($$self, $$props, $$invalidate) {
  let $selected_job;
  let $selected_service;
  let $job_list;
  let $job_fields;
  let $job_definition;
  component_subscribe($$self, selected_job, ($$value) => $$invalidate(3, $selected_job = $$value));
  component_subscribe($$self, selected_service, ($$value) => $$invalidate(8, $selected_service = $$value));
  component_subscribe($$self, job_list, ($$value) => $$invalidate(9, $job_list = $$value));
  component_subscribe($$self, job_fields, ($$value) => $$invalidate(10, $job_fields = $$value));
  component_subscribe($$self, job_definition, ($$value) => $$invalidate(11, $job_definition = $$value));
  let fields = {};
  let defn = JSON.parse($job_definition);
  let props = {};
  let service = {};
  onMount(() => {
    $$invalidate(2, service.message = "", service);
    $$invalidate(2, service.name = defn["name"], service);
    $$invalidate(2, service.desc = defn["desc"], service);
    $$invalidate(0, fields = $job_fields);
    let items = defn["fields"];
    Object.entries(items).map((list, i) => {
      let field = list[0];
      let defn2 = list[1];
      if (field in fields == false) {
        $$invalidate(0, fields[field] = "default" in defn2 ? String(defn2["default"]) : "", fields);
      }
      $$invalidate(
        1,
        props[field] = {
          type: defn2["type"],
          help: defn2["help"],
          required: defn2["required"] ? "Required" : "Optional",
          choices: defn2["choices"] ? defn2["choices"] : null
        },
        props
      );
    });
    job_fields.set(fields);
  });
  function handleRequest(event) {
    clear();
    const { submitter: submitButton } = event;
    if (submitButton.name == "submit") {
      if ($job_list && $job_list.includes($selected_job)) {
        alert.set("Please choose a new job ID.");
        return;
      }
      $$invalidate(2, service.message = JSON.stringify(fields), service);
    }
    job_fields.set(fields);
    send(submitButton.name, $selected_service, $selected_job, service.message);
  }
  function input0_input_handler() {
    $selected_job = this.value;
    selected_job.set($selected_job);
  }
  function select_change_handler(field) {
    fields[field] = select_value(this);
    $$invalidate(0, fields);
    $$invalidate(1, props);
  }
  function input_input_handler(field) {
    fields[field] = this.value;
    $$invalidate(0, fields);
    $$invalidate(1, props);
  }
  return [
    fields,
    props,
    service,
    $selected_job,
    handleRequest,
    input0_input_handler,
    select_change_handler,
    input_input_handler
  ];
}
class JobInput extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$1, create_fragment$1, safe_not_equal, {});
  }
}
function create_if_block_3(ctx) {
  let h3;
  let t;
  return {
    c() {
      h3 = element("h3");
      t = text(
        /*$alert*/
        ctx[0]
      );
      attr(h3, "class", "mx-auto text-red-500 w-full text-left px-10");
    },
    m(target, anchor) {
      insert(target, h3, anchor);
      append(h3, t);
    },
    p(ctx2, dirty) {
      if (dirty & /*$alert*/
      1)
        set_data(
          t,
          /*$alert*/
          ctx2[0]
        );
    },
    d(detaching) {
      if (detaching) {
        detach(h3);
      }
    }
  };
}
function create_else_block(ctx) {
  let servicelist;
  let current;
  servicelist = new ServiceList({});
  return {
    c() {
      create_component(servicelist.$$.fragment);
    },
    m(target, anchor) {
      mount_component(servicelist, target, anchor);
      current = true;
    },
    p: noop,
    i(local) {
      if (current)
        return;
      transition_in(servicelist.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(servicelist.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(servicelist, detaching);
    }
  };
}
function create_if_block_1(ctx) {
  let t;
  let servicedetails;
  let current;
  let if_block = (
    /*$job_definition*/
    ctx[3] && create_if_block_2()
  );
  servicedetails = new ServiceDetails({});
  return {
    c() {
      if (if_block)
        if_block.c();
      t = space();
      create_component(servicedetails.$$.fragment);
    },
    m(target, anchor) {
      if (if_block)
        if_block.m(target, anchor);
      insert(target, t, anchor);
      mount_component(servicedetails, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      if (
        /*$job_definition*/
        ctx2[3]
      ) {
        if (if_block) {
          if (dirty & /*$job_definition*/
          8) {
            transition_in(if_block, 1);
          }
        } else {
          if_block = create_if_block_2();
          if_block.c();
          transition_in(if_block, 1);
          if_block.m(t.parentNode, t);
        }
      } else if (if_block) {
        group_outros();
        transition_out(if_block, 1, 1, () => {
          if_block = null;
        });
        check_outros();
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(if_block);
      transition_in(servicedetails.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(if_block);
      transition_out(servicedetails.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(t);
      }
      if (if_block)
        if_block.d(detaching);
      destroy_component(servicedetails, detaching);
    }
  };
}
function create_if_block(ctx) {
  let jobstatus;
  let current;
  jobstatus = new JobStatus({
    props: { status: (
      /*$job_status*/
      ctx[1]
    ) }
  });
  return {
    c() {
      create_component(jobstatus.$$.fragment);
    },
    m(target, anchor) {
      mount_component(jobstatus, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      const jobstatus_changes = {};
      if (dirty & /*$job_status*/
      2)
        jobstatus_changes.status = /*$job_status*/
        ctx2[1];
      jobstatus.$set(jobstatus_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(jobstatus.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(jobstatus.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(jobstatus, detaching);
    }
  };
}
function create_if_block_2(ctx) {
  let jobinput;
  let current;
  jobinput = new JobInput({});
  return {
    c() {
      create_component(jobinput.$$.fragment);
    },
    m(target, anchor) {
      mount_component(jobinput, target, anchor);
      current = true;
    },
    i(local) {
      if (current)
        return;
      transition_in(jobinput.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(jobinput.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(jobinput, detaching);
    }
  };
}
function create_fragment(ctx) {
  let topbar;
  let t0;
  let t1;
  let current_block_type_index;
  let if_block1;
  let if_block1_anchor;
  let current;
  topbar = new TopBar({});
  let if_block0 = (
    /*$alert*/
    ctx[0] && create_if_block_3(ctx)
  );
  const if_block_creators = [create_if_block, create_if_block_1, create_else_block];
  const if_blocks = [];
  function select_block_type(ctx2, dirty) {
    if (
      /*$job_status*/
      ctx2[1]
    )
      return 0;
    if (
      /*$job_list*/
      ctx2[2]
    )
      return 1;
    return 2;
  }
  current_block_type_index = select_block_type(ctx);
  if_block1 = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  return {
    c() {
      create_component(topbar.$$.fragment);
      t0 = space();
      if (if_block0)
        if_block0.c();
      t1 = space();
      if_block1.c();
      if_block1_anchor = empty();
    },
    m(target, anchor) {
      mount_component(topbar, target, anchor);
      insert(target, t0, anchor);
      if (if_block0)
        if_block0.m(target, anchor);
      insert(target, t1, anchor);
      if_blocks[current_block_type_index].m(target, anchor);
      insert(target, if_block1_anchor, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      if (
        /*$alert*/
        ctx2[0]
      ) {
        if (if_block0) {
          if_block0.p(ctx2, dirty);
        } else {
          if_block0 = create_if_block_3(ctx2);
          if_block0.c();
          if_block0.m(t1.parentNode, t1);
        }
      } else if (if_block0) {
        if_block0.d(1);
        if_block0 = null;
      }
      let previous_block_index = current_block_type_index;
      current_block_type_index = select_block_type(ctx2);
      if (current_block_type_index === previous_block_index) {
        if_blocks[current_block_type_index].p(ctx2, dirty);
      } else {
        group_outros();
        transition_out(if_blocks[previous_block_index], 1, 1, () => {
          if_blocks[previous_block_index] = null;
        });
        check_outros();
        if_block1 = if_blocks[current_block_type_index];
        if (!if_block1) {
          if_block1 = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx2);
          if_block1.c();
        } else {
          if_block1.p(ctx2, dirty);
        }
        transition_in(if_block1, 1);
        if_block1.m(if_block1_anchor.parentNode, if_block1_anchor);
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(topbar.$$.fragment, local);
      transition_in(if_block1);
      current = true;
    },
    o(local) {
      transition_out(topbar.$$.fragment, local);
      transition_out(if_block1);
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(t0);
        detach(t1);
        detach(if_block1_anchor);
      }
      destroy_component(topbar, detaching);
      if (if_block0)
        if_block0.d(detaching);
      if_blocks[current_block_type_index].d(detaching);
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  let $alert;
  let $job_status;
  let $job_list;
  let $job_definition;
  component_subscribe($$self, alert, ($$value) => $$invalidate(0, $alert = $$value));
  component_subscribe($$self, job_status, ($$value) => $$invalidate(1, $job_status = $$value));
  component_subscribe($$self, job_list, ($$value) => $$invalidate(2, $job_list = $$value));
  component_subscribe($$self, job_definition, ($$value) => $$invalidate(3, $job_definition = $$value));
  onMount(() => {
    send("listall", null, null, null);
  });
  return [$alert, $job_status, $job_list, $job_definition];
}
class Main extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, {});
  }
}
const app = new Main({
  target: document.getElementById("app")
});
export {
  app as default
};
//# sourceMappingURL=main.js.map
