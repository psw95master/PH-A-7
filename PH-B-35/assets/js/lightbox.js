/* =========================================================
   사진 크게 보기 (라이트박스)

   `data-lightbox` 가 붙은 버튼을 누르면 검은 막이 덮이고 사진이 크게 열린다.
   제목·설명은 각 사진이 속한 <figure> 의 figcaption / .tile__meta 에서 읽는다.
   따로 적어 두지 않으므로 목록과 팝업의 문구가 어긋날 일이 없다.

   조작
     - 좌우 화살표 버튼 / 키보드 ← → : 앞뒤 사진
     - 닫기 버튼 / ESC / 검은 배경 클릭 : 닫기
     - 열기 전에 누른 버튼을 기억했다가 닫을 때 그 자리로 포커스를 돌려준다
   ========================================================= */
(function () {
  "use strict";

  var triggers = [].slice.call(document.querySelectorAll("[data-lightbox]"));
  if (!triggers.length) return;

  // 목록에서 사진 정보를 미리 뽑아 둔다.
  var items = triggers.map(function (btn) {
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
    // 글자는 폰트마다 위아래 여백이 달라 동그라미 안에서 미세하게 어긋난다. (260821 수정)
    var icon = function (d) {
      return '<svg class="lb__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
             '<path d="' + d + '"/></svg>';
    };

    box.innerHTML =
      '<button class="lb__close" type="button" aria-label="닫기">' +
        icon("M6 6l12 12M18 6L6 18") + '</button>' +
      '<figure class="lb__figure">' +
        // 사진과 좌우 버튼자리를 한 줄로 놓는다. 버튼자리가 남는 여백을 반씩 나눠 갖고
        // 그 한가운데에 버튼이 놓이므로, 사진과 절대 겹치지 않는다. (260821 페리 지시)
        '<div class="lb__stage">' +
          '<div class="lb__side">' +
            '<button class="lb__nav lb__nav--prev" type="button" aria-label="이전 사진">' +
              icon("M15 5l-7 7 7 7") + '</button>' +
          '</div>' +
          '<img class="lb__img" alt="">' +
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

  triggers.forEach(function (btn, i) {
    btn.addEventListener("click", function () { open(i); });
  });
})();
