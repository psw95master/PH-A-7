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

/* 모바일 GNB 아코디언 — 대분류를 누르면 하위 메뉴가 펼쳐진다. (260821 페리 지시)
   이전에는 하위가 전부 펼쳐진 채라 메뉴가 길게 늘어졌다.

   상태는 둘 — default(접힘) / is-expanded(펼침)
   넓은 화면에서는 아무 일도 하지 않는다. 거기서는 마우스를 올리면 펼쳐지는 방식이다.

   대분류는 원래 첫 하위 페이지로 가는 링크다. 좁은 화면에서만 이동을 막고
   펼치는 역할로 바꾼다. 스크립트가 죽어도 링크로서는 그대로 동작한다. */
(function () {
  'use strict';

  var MOBILE = '(max-width: 960px)';
  var items = [].slice.call(document.querySelectorAll('.gnb > ul > li'));
  if (!items.length) return;

  var mq = window.matchMedia(MOBILE);

  function collapseAll(except) {
    items.forEach(function (li) {
      if (li !== except) li.classList.remove('is-expanded');
    });
  }

  items.forEach(function (li) {
    var link = li.querySelector('.gnb__link');
    var sub = li.querySelector('.gnb__sub');
    if (!link || !sub) return;

    link.setAttribute('aria-expanded', 'false');

    link.addEventListener('click', function (ev) {
      if (!mq.matches) return;              // 넓은 화면에서는 그냥 링크로 둔다
      ev.preventDefault();
      var willOpen = !li.classList.contains('is-expanded');
      collapseAll(li);                      // 한 번에 하나만 펼친다
      li.classList.toggle('is-expanded', willOpen);
      link.setAttribute('aria-expanded', String(willOpen));
    });
  });

  // 현재 보고 있는 페이지가 속한 갈래는 처음부터 펼쳐 둔다.
  var current = document.querySelector('.gnb > ul > li.is-current');
  if (current) {
    current.classList.add('is-expanded');
    var curLink = current.querySelector('.gnb__link');
    if (curLink) curLink.setAttribute('aria-expanded', 'true');
  }

  // 넓은 화면으로 넘어가면 펼침 상태를 지운다. 남아 있으면 드롭다운과 겹친다.
  function onChange() {
    if (!mq.matches) {
      collapseAll(null);
      items.forEach(function (li) {
        var l = li.querySelector('.gnb__link');
        if (l) l.setAttribute('aria-expanded', 'false');
      });
    }
  }
  if (mq.addEventListener) mq.addEventListener('change', onChange);
  else if (mq.addListener) mq.addListener(onChange);
})();
