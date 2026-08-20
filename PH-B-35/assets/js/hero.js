/* =========================================================
   홈 상단 키배너 자동 롤링

   - 간격 1.5초 (260820 페리 지시. 최초 2.5초 → 슬라이드 5장이 되면서 단축)
   - 마우스를 올리거나 점에 포커스가 가면 멈추고, 벗어나면 다시 돈다
   - 다른 탭으로 가 있는 동안에는 돌리지 않는다
   - 사용자가 OS 에서 "동작 줄이기"를 켜 두었으면 자동 롤링을 하지 않는다
     (멀미·어지럼 유발 때문. 점을 눌러 직접 넘기는 것은 그대로 된다)
   ========================================================= */
(function () {
  "use strict";

  var INTERVAL = 1500;

  var root = document.querySelector("[data-hero]");
  if (!root) return;

  var slides = root.querySelectorAll(".hero__slide");
  var dots = root.querySelectorAll(".hero__dot");
  if (slides.length < 2) return;              // 한 장뿐이면 롤링할 것이 없다

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var current = 0;
  var timer = null;

  function show(next) {
    if (next === current) return;
    slides[current].classList.remove("is-active");
    slides[next].classList.add("is-active");
    if (dots.length) {
      dots[current].classList.remove("is-active");
      dots[current].removeAttribute("aria-current");
      dots[next].classList.add("is-active");
      dots[next].setAttribute("aria-current", "true");
    }
    current = next;
  }

  function start() {
    stop();
    if (reduce.matches) return;
    timer = setInterval(function () {
      show((current + 1) % slides.length);
    }, INTERVAL);
  }

  function stop() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  for (var i = 0; i < dots.length; i++) {
    dots[i].addEventListener("click", function () {
      show(Number(this.getAttribute("data-index")));
      start();                                 // 누른 장부터 다시 세기 시작한다
    });
  }

  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", start);

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop();
    else start();
  });

  // 설정을 도중에 바꾸는 경우까지 따라간다. addEventListener 가 없는 구형 사파리 대비.
  if (reduce.addEventListener) reduce.addEventListener("change", start);
  else if (reduce.addListener) reduce.addListener(start);

  start();
})();
