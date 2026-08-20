/* =========================================================
   홈 상단 키배너 자동 롤링

   - 간격 1.8초 (260820 페리 지시. 2.5초 → 1.5초 → 1.8초. 급해 보이지 않게 조정)
   - 점에 키보드 포커스가 가 있는 동안만 멈춘다. 직접 넘겨 보는 중이니까.
     마우스를 올렸다고 멈추지는 않는다 — 배너에 누를 링크가 없어 멈출 이유가 없고,
     검수용 게이트의 확인 버튼이 배너 위에 겹쳐 있어서 게이트를 통과하는 순간
     마우스가 배너에 얹힌 것으로 잡혀 그대로 멈춰 버렸다 (260820 수정)
   - 다른 탭으로 가 있는 동안에는 돌리지 않는다
   - 사용자가 OS 에서 "동작 줄이기"를 켜 두었으면 자동 롤링을 하지 않는다
     (멀미·어지럼 유발 때문. 점을 눌러 직접 넘기는 것은 그대로 된다)
   ========================================================= */
(function () {
  "use strict";

  var INTERVAL = 1800;

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

  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", function () {
    // 포커스가 배너 밖으로 나갔을 때만 다시 돌린다.
    // 포커스를 쥐고 있던 요소가 사라지는 경우까지 감안해 다음 차례에 확인한다.
    setTimeout(function () {
      if (!root.contains(document.activeElement)) start();
    }, 0);
  });

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop();
    else start();
  });

  // 설정을 도중에 바꾸는 경우까지 따라간다. addEventListener 가 없는 구형 사파리 대비.
  if (reduce.addEventListener) reduce.addEventListener("change", start);
  else if (reduce.addListener) reduce.addListener(start);

  start();
})();
