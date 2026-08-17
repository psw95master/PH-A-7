/* =========================================================
   검수용 진입 게이트
   전달받은 4자리 번호를 입력해야 화면이 열린다.

   ⚠️ 실제 보안 장치가 아니다. 번호가 이 파일에 그대로 들어 있어
      소스를 열면 누구나 볼 수 있다. 검수 단계에서 링크가 우연히
      퍼지는 것을 막는 형식적 장치다. 실서버 이관 시 걷어낸다.
   ========================================================= */
(function () {
  "use strict";

  var CODE = "0000";
  var KEY = "nh-gate";           // sessionStorage — 탭을 닫으면 다시 묻는다
  var LOCKED = "nh-locked";

  // 이미 통과한 세션이면 아무것도 하지 않는다.
  try {
    if (window.sessionStorage && sessionStorage.getItem(KEY) === "ok") return;
  } catch (e) {
    return;                       // 스토리지가 막힌 환경에서는 게이트를 걸지 않는다
  }

  // body 가 파싱되기 전에 잠근다. 내용이 한 순간도 비치지 않게.
  var root = document.documentElement;
  root.classList.add(LOCKED);

  function unlock() {
    try { sessionStorage.setItem(KEY, "ok"); } catch (e) {}
    root.classList.remove(LOCKED);
    var gate = document.querySelector(".nh-gate");
    if (gate) gate.parentNode.removeChild(gate);
  }

  function build() {
    var gate = document.createElement("div");
    gate.className = "nh-gate";
    gate.setAttribute("role", "dialog");
    gate.setAttribute("aria-modal", "true");
    gate.setAttribute("aria-labelledby", "nh-gate-title");

    gate.innerHTML =
      '<form class="nh-gate__box" novalidate>' +
        '<img class="nh-gate__logo" src="assets/img/logo.png" alt="나우하이텍" width="192" height="48">' +
        '<h1 class="nh-gate__title" id="nh-gate-title">검수용 페이지입니다</h1>' +
        '<p class="nh-gate__desc">전달받은 4자리 번호를 입력해 주세요.</p>' +
        '<label class="nh-gate__label" for="nh-gate-input">확인 번호</label>' +
        '<input class="nh-gate__input" id="nh-gate-input" type="password" ' +
               'inputmode="numeric" autocomplete="off" maxlength="4" ' +
               'aria-describedby="nh-gate-error">' +
        '<p class="nh-gate__error" id="nh-gate-error" role="alert" hidden>' +
          '번호가 맞지 않습니다. 다시 입력해 주세요.</p>' +
        '<button class="nh-gate__submit" type="submit">확인</button>' +
      '</form>';

    document.body.insertBefore(gate, document.body.firstChild);

    var form = gate.querySelector("form");
    var input = gate.querySelector(".nh-gate__input");
    var error = gate.querySelector(".nh-gate__error");

    input.focus();

    // 입력을 고치기 시작하면 오류 표시를 거둔다.
    input.addEventListener("input", function () {
      error.hidden = true;
      gate.classList.remove("is-error");
    });

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (input.value === CODE) {
        unlock();
        return;
      }
      error.hidden = false;
      gate.classList.add("is-error");
      input.value = "";
      input.focus();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
