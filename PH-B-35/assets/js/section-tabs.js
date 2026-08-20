/* =========================================================
   좁은 화면 — 좌측 메뉴(LNB)를 화면 전환 없이 넘긴다

   원래는 탭을 누르면 페이지가 통째로 다시 열렸다. 눌렀을 때 화면이 하얗게 깜빡이고
   스크롤이 맨 위로 튄다. 대신 누른 페이지의 본문만 가져와 지금 화면에 끼워 넣는다.
   (260821 페리 지시 — A안)

   주소는 그대로 바꾼다(history.pushState). 그래서
     - 공유·북마크가 살아 있고
     - 뒤로가기가 정상 동작하며
     - 검색엔진은 여전히 페이지마다 따로 본다
   한 페이지에 다 담는 방식(B안)은 이 세 가지를 잃어서 버렸다.

   넓은 화면에서는 아무 일도 하지 않는다. 거기서 LNB 는 세로 목록이고
   깜빡임이 문제 되지 않는다.

   좌우로 밀어 넘기는 동작도 넣었다가 걷어냈다 — 써 보니 오히려 헷갈린다는 판단.
   (260821 페리 지시)
   ========================================================= */
(function () {
  "use strict";

  var MOBILE = "(max-width: 860px)";
  var mq = window.matchMedia(MOBILE);
  var layout = document.querySelector(".layout");
  var lnb = document.querySelector(".lnb__list");
  var content = document.querySelector(".content");
  if (!layout || !lnb || !content) return;

  var links = [].slice.call(lnb.querySelectorAll("a"));
  if (links.length < 2) return;              // 갈아끼울 상대가 없으면 그만둔다

  var busy = false;

  function urlOf(a) {
    return a.getAttribute("href");
  }

  function indexOfCurrent() {
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute("aria-current") === "page") return i;
    }
    return 0;
  }

  /* 가져온 문서에서 필요한 조각만 뽑아 지금 화면에 반영한다. */
  function apply(doc, url, push) {
    var newContent = doc.querySelector(".content");
    if (!newContent) return false;           // 짜임이 다른 페이지면 그냥 넘어간다

    // 본문에 딸린 <script> 는 떼고 넣는다. 두 가지 이유다.
    //   1) innerHTML 로 넣은 script 는 어차피 실행되지 않는다
    //   2) 그대로 두면 아래 loadScripts 가 "이미 있다"고 오판해 진짜 로드를 건너뛴다
    var body = newContent.cloneNode(true);
    [].slice.call(body.querySelectorAll("script")).forEach(function (s) {
      s.parentNode.removeChild(s);
    });
    content.innerHTML = body.innerHTML;

    var newTitle = doc.querySelector(".page-head__title");
    var oldTitle = document.querySelector(".page-head__title");
    if (newTitle && oldTitle) oldTitle.textContent = newTitle.textContent;

    var newCrumb = doc.querySelector(".breadcrumb ol");
    var oldCrumb = document.querySelector(".breadcrumb ol");
    if (newCrumb && oldCrumb) oldCrumb.innerHTML = newCrumb.innerHTML;

    document.title = doc.title;

    var desc = doc.querySelector('meta[name="description"]');
    var myDesc = document.querySelector('meta[name="description"]');
    if (desc && myDesc) myDesc.setAttribute("content", desc.getAttribute("content"));

    // 지금 어디인지 표시를 옮긴다.
    var target = url.split("?")[0].split("#")[0];
    links.forEach(function (a) {
      var mine = urlOf(a).split("?")[0].split("#")[0] === target;
      if (mine) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });

    if (push) history.pushState({ nhTab: url }, "", url);

    loadScripts(doc);

    // 본문이 통째로 바뀌었으니 읽는 사람에게도 알린다.
    content.setAttribute("tabindex", "-1");
    content.focus({ preventScroll: true });

    // 페이지 제목이 보이는 자리로 올린다.
    // 머리말이 화면에 붙어 있으므로 그 높이만큼 빼지 않으면 제목이 가려진다.
    var head = document.querySelector(".page-head");
    var bar = document.querySelector(".site-header");
    if (head) {
      var top = head.offsetTop - (bar ? bar.offsetHeight : 0);
      window.scrollTo({ top: Math.max(top, 0), behavior: "instant" });
    }
    return true;
  }

  /* 새 본문이 필요로 하는 스크립트를 챙긴다.
     이미 있으면 다시 훑게만 하고, 없으면 그때 불러온다. */
  function loadScripts(doc) {
    var have = [].slice.call(document.querySelectorAll("script[src]")).map(function (s) {
      return s.getAttribute("src").split("?")[0];
    });

    [].slice.call(doc.querySelectorAll("script[src]")).forEach(function (s) {
      var src = s.getAttribute("src");
      if (have.indexOf(src.split("?")[0]) !== -1) return;
      var el = document.createElement("script");
      el.src = src;
      document.body.appendChild(el);
    });

    if (window.NH_lightbox) window.NH_lightbox();
  }

  function go(url, push) {
    if (busy) return;
    busy = true;
    layout.classList.add("is-loading");

    fetch(url, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");
        if (!apply(doc, url, push)) location.href = url;
      })
      .catch(function () {
        location.href = url;               // 실패하면 그냥 페이지를 연다
      })
      .then(function () {
        busy = false;
        layout.classList.remove("is-loading");
      });
  }

  links.forEach(function (a) {
    a.addEventListener("click", function (ev) {
      if (!mq.matches) return;                // 넓은 화면에서는 그냥 링크
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return;
      if (a.getAttribute("aria-current") === "page") { ev.preventDefault(); return; }
      ev.preventDefault();
      go(urlOf(a), true);
    });
  });

  window.addEventListener("popstate", function (ev) {
    if (!mq.matches) return;
    if (ev.state && ev.state.nhTab) go(ev.state.nhTab, false);
  });

  // 처음 들어온 자리도 기록해 둬야 뒤로가기가 이 페이지로 돌아온다.
  history.replaceState({ nhTab: location.pathname + location.search }, "", location.href);
})();
