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
