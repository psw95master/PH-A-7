/* 좁은 화면에서 좌측 메뉴는 가로 스크롤 줄이 된다.
   현재 페이지가 뒤쪽 항목이면 화면 밖에 있어 지금 어디인지 알 수 없으므로 가운데로 당겨 둔다. */
(function () {
  var list = document.querySelector('.lnb__list');
  if (!list) return;
  var cur = list.querySelector('[aria-current="page"]');
  if (!cur || list.scrollWidth <= list.clientWidth) return;
  var c = list.getBoundingClientRect(), r = cur.getBoundingClientRect();
  list.scrollLeft += (r.left - c.left) - (c.width - r.width) / 2;
})();

/* 모바일 GNB 토글 — default / is-open 두 상태만 가진다. */
(function () {
  var btn = document.querySelector('.nav-toggle');
  var gnb = document.getElementById('gnb');
  if (!btn || !gnb) return;

  function setOpen(open) {
    gnb.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  }

  btn.addEventListener('click', function () {
    setOpen(btn.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setOpen(false);
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 960) setOpen(false);
  });
})();
