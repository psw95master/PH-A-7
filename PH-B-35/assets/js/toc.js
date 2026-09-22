/* 사진 목록 옆에 붙는 목차.

   data-toc 가 붙은 목록을 훑어 타이틀별로 묶고, 화면 오른쪽에 목차를 세운다.
   평소에는 짧은 선만 보이고, 마우스를 올리면 목차가 펼쳐진다. (노션 방식)
   누르면 그 자리로 내려가고, 스크롤하면 지금 보고 있는 줄에 표시가 붙는다.
   (260922 페리 지시)

   같은 타이틀이 여럿이면 뒤의 (1) (2) … 를 떼고 한 줄로 묶는다.
   마우스가 없는 기기(휴대폰·태블릿)와 좁은 화면에서는 CSS 에서 감춘다. */
(function () {
  "use strict";

  var gal = document.querySelector("[data-toc]");
  if (!gal) return;

  var tiles = [].slice.call(gal.children);
  if (tiles.length < 4) return;

  // 타이틀별로 묶는다. 각 묶음의 첫 칸이 이동 목표가 된다.
  var groups = [], byName = {};
  tiles.forEach(function (tile) {
    var cap = tile.querySelector(".tile__cap");
    if (!cap) return;
    var name = cap.textContent.trim().replace(/\s*\(\d+\)$/, "");
    if (!byName[name]) {
      byName[name] = { name: name, first: tile, count: 0 };
      groups.push(byName[name]);
    }
    byName[name].count++;
  });
  if (groups.length < 2) return;

  var nav = document.createElement("nav");
  nav.className = "toc";
  nav.setAttribute("aria-label", "사진 목록 바로가기");

  // 접힌 상태에서 보이는 짧은 선들
  var mini = document.createElement("div");
  mini.className = "toc__mini";
  mini.setAttribute("aria-hidden", "true");
  var dashes = groups.map(function () {
    var d = document.createElement("span");
    mini.appendChild(d);
    return d;
  });
  nav.appendChild(mini);

  // 마우스를 올리면 펼쳐지는 목차
  var full = document.createElement("div");
  full.className = "toc__full";
  var head = document.createElement("p");
  head.className = "toc__head";
  head.textContent = gal.getAttribute("data-toc") || "사진 목록";
  full.appendChild(head);

  var list = document.createElement("ul");
  var links = groups.map(function (g) {
    var li = document.createElement("li");
    var a = document.createElement("button");
    a.type = "button";
    a.className = "toc__item";
    a.title = g.name + (g.count > 1 ? " — 사진 " + g.count + "장" : "");
    var label = document.createElement("span");
    label.className = "toc__name";
    label.textContent = g.name;
    a.appendChild(label);
    if (g.count > 1) {
      var n = document.createElement("span");
      n.className = "toc__n";
      n.textContent = g.count;
      a.appendChild(n);
    }
    a.addEventListener("click", function () {
      var y = g.first.getBoundingClientRect().top + window.scrollY - 90;
      window.scrollTo({ top: y, behavior: "smooth" });
    });
    li.appendChild(a);
    list.appendChild(li);
    return a;
  });
  full.appendChild(list);
  nav.appendChild(full);
  document.body.appendChild(nav);

  // 지금 보고 있는 줄에 표시를 옮긴다. 화면 위쪽에 가장 가까운 묶음을 고른다.
  var at = -1;
  function mark() {
    var best = 0;
    for (var i = 0; i < groups.length; i++) {
      if (groups[i].first.getBoundingClientRect().top - 120 <= 0) best = i;
    }
    if (best === at) return;
    if (at >= 0) {
      links[at].removeAttribute("aria-current");
      dashes[at].removeAttribute("data-on");
    }
    links[best].setAttribute("aria-current", "true");
    dashes[best].setAttribute("data-on", "");
    at = best;
    // 목차가 길어 잘릴 때 현재 줄을 목차 안에서 보이게 한다
    var box = list.getBoundingClientRect(), row = links[best].getBoundingClientRect();
    if (row.top < box.top + 8 || row.bottom > box.bottom - 8) {
      list.scrollTop += row.top - box.top - box.height / 2 + row.height / 2;
    }
  }

  var ticking = false;
  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { mark(); ticking = false; });
  }, { passive: true });
  mark();
})();
