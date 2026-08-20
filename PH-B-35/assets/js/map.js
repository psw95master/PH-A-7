/* =========================================================
   오시는길 — 카카오맵

   지도 자리(#map)에 회사 위치를 띄우고 이름표를 붙인다. (260821 페리 지시)

   좌표를 직접 적어 두지 않고 주소로 찾는다(services 라이브러리의 Geocoder).
   좌표를 손으로 넣으면 주소가 바뀌었을 때 두 값이 어긋나는데,
   주소는 이미 build.py 의 COMPANY 한 곳에서 관리하고 있기 때문이다.

   지도가 뜨지 않는 경우(키 미발급 · 도메인 미등록 · 주소 검색 실패 · 스크립트 차단)에는
   지도 자리를 숨기고 원래의 "카카오맵에서 위치 보기" 안내를 그대로 남긴다.
   지도는 거들 뿐이고, 주소와 연락처는 그 아래 표에 언제나 글자로 적혀 있다.
   ========================================================= */
(function () {
  "use strict";

  var box = document.getElementById("map");
  if (!box) return;

  var address = box.dataset.address;
  var label = box.dataset.label || "";
  var fallback = document.querySelector(".map-fallback");

  function giveUp() {
    box.hidden = true;
    if (fallback) fallback.hidden = false;
  }

  if (!window.kakao || !window.kakao.maps) return giveUp();

  kakao.maps.load(function () {
    if (!kakao.maps.services) return giveUp();

    var map = new kakao.maps.Map(box, {
      center: new kakao.maps.LatLng(35.0951, 128.8555),   // 검색 전 임시 중심(부산 강서구)
      level: 4
    });

    map.addControl(new kakao.maps.MapTypeControl(), kakao.maps.ControlPosition.TOPRIGHT);
    map.addControl(new kakao.maps.ZoomControl(), kakao.maps.ControlPosition.RIGHT);

    new kakao.maps.services.Geocoder().addressSearch(address, function (result, status) {
      if (status !== kakao.maps.services.Status.OK || !result.length) return giveUp();

      var pos = new kakao.maps.LatLng(result[0].y, result[0].x);
      map.setCenter(pos);

      var marker = new kakao.maps.Marker({ position: pos });
      marker.setMap(map);

      if (label) {
        new kakao.maps.InfoWindow({
          position: pos,
          content: '<div style="padding:6px 10px;font-size:13px;white-space:nowrap">' +
                   label + "</div>"
        }).open(map, marker);
      }

      // 창 크기가 바뀌면 지도가 한쪽으로 쏠린다. 중심을 다시 잡아 준다.
      window.addEventListener("resize", function () {
        map.relayout();
        map.setCenter(pos);
      });
    });
  });
})();
