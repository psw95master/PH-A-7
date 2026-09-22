/* 사진 목록 페이지 나누기.

   data-pager="10" 이 붙은 목록을 10칸씩 끊어 보여주고, 아래에 번호 리모컨을 단다.
   (260922 페리 지시 — 사업분야 사진이 늘면서 한 화면이 너무 길어졌다)

   숨긴 칸은 data-lightbox 를 떼어 둔다. 그래야 팝업에서 좌우로 넘길 때
   지금 화면에 없는 사진이 끼어들지 않는다. 뗐다 붙인 뒤에는 NH_lightbox() 로
   목록을 다시 훑게 한다. */
(function () {
  "use strict";

  function setup(gal) {
    var size = parseInt(gal.getAttribute("data-pager"), 10) || 10;
    var tiles = [].slice.call(gal.children);
    if (tiles.length <= size) return;

    var pages = Math.ceil(tiles.length / size);
    var nav = document.createElement("nav");
    nav.className = "pager";
    nav.setAttribute("aria-label", "사진 목록 페이지");

    var prev = button("‹", "이전 페이지");
    var next = button("›", "다음 페이지");
    var nums = [];
    nav.appendChild(prev);
    for (var n = 1; n <= pages; n++) nav.appendChild(nums[nums.length] = button(String(n), n + "페이지"));
    nav.appendChild(next);
    gal.parentNode.insertBefore(nav, gal.nextSibling);

    var at = 0;
    show(0);

    prev.addEventListener("click", function () { show(at - 1, true); });
    next.addEventListener("click", function () { show(at + 1, true); });
    nums.forEach(function (b, i) {
      b.addEventListener("click", function () { show(i, true); });
    });

    function show(i, moveView) {
      at = Math.max(0, Math.min(pages - 1, i));
      tiles.forEach(function (tile, k) {
        var on = Math.floor(k / size) === at;
        tile.hidden = !on;
        var btn = tile.querySelector("[data-lightbox], [data-lightbox-off]");
        if (btn) {
          btn.removeAttribute(on ? "data-lightbox-off" : "data-lightbox");
          btn.setAttribute(on ? "data-lightbox" : "data-lightbox-off", "");
        }
      });
      nums.forEach(function (b, k) {
        if (k === at) b.setAttribute("aria-current", "page");
        else b.removeAttribute("aria-current");
      });
      prev.disabled = at === 0;
      next.disabled = at === pages - 1;
      if (window.NH_lightbox) window.NH_lightbox();
      if (moveView) gal.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function button(label, aria) {
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = label;
    b.setAttribute("aria-label", aria);
    return b;
  }

  [].slice.call(document.querySelectorAll("[data-pager]")).forEach(setup);
})();
