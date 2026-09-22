/* 사진 목록 옆에 붙는 목차 리모컨.

   data-toc 가 붙은 목록을 훑어 타이틀별로 묶고, 화면 오른쪽에 목차를 세운다.
   누르면 그 자리로 내려가고, 스크롤하면 지금 보고 있는 줄에 표시가 붙는다.
   (260922 페리 지시 — 하단 번호 리모컨을 떼고 노션 목차처럼 바꿨다)

   같은 타이틀이 여럿이면 뒤의 (1) (2) … 를 떼고 한 줄로 묶는다.
   화면이 좁으면 목차가 본문을 가리므로 CSS 에서 숨긴다. */
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
  var head = document.createElement("p");
  head.className = "toc__head";
  head.textContent = "사진 목록";
  nav.appendChild(head);

  var list = document.createElement("ul");
  var links = groups.map(function (g, i) {
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
  nav.appendChild(list);
  document.body.appendChild(nav);

  // 지금 보고 있는 줄에 표시를 옮긴다. 화면 위쪽에 가장 가까운 묶음을 고른다.
  var at = -1;
  function mark() {
    var best = 0;
    for (var i = 0; i < groups.length; i++) {
      if (groups[i].first.getBoundingClientRect().top - 120 <= 0) best = i;
    }
    if (best === at) return;
    if (at >= 0) links[at].removeAttribute("aria-current");
    links[best].setAttribute("aria-current", "true");
    at = best;
    // 목차가 길어 잘릴 때 현재 줄을 목차 안에서 보이게 한다
    var box = nav.getBoundingClientRect(), row = links[best].getBoundingClientRect();
    if (row.top < box.top + 8 || row.bottom > box.bottom - 8) {
      nav.scrollTop += row.top - box.top - box.height / 2 + row.height / 2;
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
