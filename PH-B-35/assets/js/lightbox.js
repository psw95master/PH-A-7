/* =========================================================
   사진 크게 보기 (라이트박스)

   `data-lightbox` 가 붙은 버튼을 누르면 검은 막이 덮이고 사진이 크게 열린다.
   제목·설명은 각 사진이 속한 <figure> 의 figcaption / .tile__meta 에서 읽는다.
   따로 적어 두지 않으므로 목록과 팝업의 문구가 어긋날 일이 없다.

   조작
     - 좌우 화살표 버튼 / 키보드 ← → : 앞뒤 사진
     - 닫기 버튼 / ESC / 검은 배경 클릭 : 닫기
     - 열기 전에 누른 버튼을 기억했다가 닫을 때 그 자리로 포커스를 돌려준다

   좁은 화면에서 좌측 메뉴로 페이지를 갈아끼우면 사진 목록이 통째로 바뀐다.
   그래서 window.NH_lightbox() 로 다시 훑을 수 있게 열어 둔다. (260821)
   ========================================================= */
(function () {
  "use strict";

  var items = [];
  var current = 0;
  var opener = null;
  var box = null;
  var elImg, elTitle, elDesc, elCount, btnPrev, btnNext;

  function render() {
    var it = items[current];
    elImg.setAttribute("src", it.src);
    elImg.setAttribute("alt", it.alt);
    elTitle.textContent = it.title;
    elDesc.textContent = it.desc;
    elDesc.hidden = !it.desc;
    elCount.textContent = (current + 1) + " / " + items.length;

    var only = items.length < 2;
    btnPrev.hidden = only;
    btnNext.hidden = only;
  }

  function move(step) {
    current = (current + step + items.length) % items.length;
    render();
  }

  function onKey(ev) {
    if (ev.key === "Escape") close();
    else if (ev.key === "ArrowLeft") move(-1);
    else if (ev.key === "ArrowRight") move(1);
  }

  function build() {
    box = document.createElement("div");
    box.className = "lb";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "사진 크게 보기");
    box.hidden = true;

    // 아이콘은 글자(× ‹ ›) 대신 SVG 로 그린다.
    // 글자는 폰트마다 위아래 여백이 달라 동그라미 안에서 미세하게 어긋난다.
    var icon = function (d) {
      return '<svg class="lb__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
             '<path d="' + d + '"/></svg>';
    };

    box.innerHTML =
      '<button class="lb__close" type="button" aria-label="닫기">' +
        icon("M6 6l12 12M18 6L6 18") + '</button>' +
      '<figure class="lb__figure">' +
        // 사진과 좌우 버튼자리를 한 줄로 놓는다. 버튼자리가 남는 여백을 반씩 나눠 갖고
        // 그 한가운데에 버튼이 놓이므로, 사진과 절대 겹치지 않는다.
        // 사진칸(.lb__frame)은 폭이 고정이다. 사진마다 버튼이 움직이지 않게 하려는 것.
        '<div class="lb__stage">' +
          '<div class="lb__side">' +
            '<button class="lb__nav lb__nav--prev" type="button" aria-label="이전 사진">' +
              icon("M15 5l-7 7 7 7") + '</button>' +
          '</div>' +
          '<div class="lb__frame"><img class="lb__img" alt=""></div>' +
          '<div class="lb__side">' +
            '<button class="lb__nav lb__nav--next" type="button" aria-label="다음 사진">' +
              icon("M9 5l7 7-7 7") + '</button>' +
          '</div>' +
        '</div>' +
        '<figcaption class="lb__cap">' +
          '<p class="lb__count"></p>' +
          '<h2 class="lb__title"></h2>' +
          '<p class="lb__desc"></p>' +
        '</figcaption>' +
      '</figure>';

    document.body.appendChild(box);

    elImg = box.querySelector(".lb__img");
    elTitle = box.querySelector(".lb__title");
    elDesc = box.querySelector(".lb__desc");
    elCount = box.querySelector(".lb__count");
    btnPrev = box.querySelector(".lb__nav--prev");
    btnNext = box.querySelector(".lb__nav--next");

    box.querySelector(".lb__close").addEventListener("click", close);
    btnPrev.addEventListener("click", function () { move(-1); });
    btnNext.addEventListener("click", function () { move(1); });

    // 사진이나 설명이 아닌 빈 곳(검은 막)을 누르면 닫는다.
    box.addEventListener("click", function (ev) {
      if (ev.target === box) close();
    });
  }

  function open(index) {
    if (!box) build();
    opener = document.activeElement;
    current = index;
    render();
    box.hidden = false;
    document.documentElement.classList.add("lb-open");   // 뒤 화면 스크롤 잠금
    document.addEventListener("keydown", onKey);
    box.querySelector(".lb__close").focus();
  }

  function close() {
    if (!box || box.hidden) return;
    box.hidden = true;
    document.documentElement.classList.remove("lb-open");
    document.removeEventListener("keydown", onKey);
    if (opener && document.contains(opener)) opener.focus();
    opener = null;
  }

  /* 사진 목록을 훑어 버튼에 동작을 건다.
     페이지를 갈아끼운 뒤 다시 부르면 새 목록으로 갱신된다. */
  function scan() {
    close();
    var triggers = [].slice.call(document.querySelectorAll("[data-lightbox]"));
    items = triggers.map(function (btn) {
      var fig = btn.closest("figure");
      var cap = fig ? fig.querySelector(".tile__cap") : null;
      var meta = fig ? fig.querySelector(".tile__meta") : null;
      var img = btn.querySelector("img");
      return {
        src: img.getAttribute("src"),
        alt: img.getAttribute("alt") || "",
        title: cap ? cap.textContent.trim() : "",
        desc: meta ? meta.textContent.trim() : ""
      };
    });

    triggers.forEach(function (btn, i) {
      if (btn.dataset.lbBound === "1") return;   // 같은 버튼에 두 번 걸지 않는다
      btn.dataset.lbBound = "1";
      btn.addEventListener("click", function () {
        // 목록이 바뀌었을 수 있으므로 누른 시점의 자리를 다시 센다.
        var all = [].slice.call(document.querySelectorAll("[data-lightbox]"));
        open(all.indexOf(btn));
      });
    });
  }

  window.NH_lightbox = scan;
  scan();
})();
