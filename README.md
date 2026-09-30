# PH-A-7. 나우하이텍 웹사이트 리뉴얼

나우하이텍(`nawoohitech.co.kr`) 웹사이트 리뉴얼 프로젝트의 작업 저장소입니다.

옛 사이트는 2006년식 frameset + 테이블 구조로, 본문 대부분이 이미지 안의 글자였습니다.
2010년 이후 콘텐츠 갱신이 없었습니다. `261001` 부터 이 저장소의 전환본이 실주소에 올라가 있습니다.

---

## 구성

| 위치 | 내용 |
| --- | --- |
| [`PH-B-35/`](PH-B-35/) | **이미지 텍스트 HTML 전환본** — 현행 사이트의 이미지 속 글자를 전부 실제 HTML 텍스트로 옮긴 정적 사이트 14개 페이지 |
| [`@log/`](@log/) | 세션 작업 로그 (최신순). 무엇을 했고 **왜 그렇게 정했는지**를 남깁니다 |

---

## PH-B-35 보는 방법

### 브라우저로 바로

**라이브 — https://nawoohitech.co.kr**

> `261001` 확인: `https` 정상, 인증서 유효, `http` 와 `www` 모두 여기로 넘어옵니다.
> 가비아 소유자 인증이 풀려 네임서버가 Cloudflare(`garret` · `celine.ns.cloudflare.com`)로 넘어갔습니다.
> 경위는 [`@log/PH-A-7_@log_260918.md`](@log/PH-A-7_@log_260918.md).
>
> GitHub Pages(`psw95master.github.io/...`)는 상거래 목적 사이트의 무료 호스팅을 제한하는
> 약관 조항 때문에 `260817` 에 기각됐습니다. 경위는 [`@log/PH-A-7_@log_260817.md`](@log/PH-A-7_@log_260817.md).

### 배포 — 어느 브랜치가 어디로 가는가

| 브랜치 | 주소 | 무엇 |
| --- | --- | --- |
| `main` | **https://nawoohitech.co.kr** | **라이브 서버.** 고객이 보는 화면. 푸시하면 즉시 반영됩니다 |
| `staging` | https://staging.nawoohitech.pages.dev | **테스트 서버.** 검수용. 검색에서 빠져 있습니다 |

둘 다 Cloudflare Pages 프로젝트 `nawoohitech` 입니다. 출력 폴더는 `PH-B-35`, 빌드 명령은 없습니다(정적 HTML).

**고칠 때는 `staging` 에 먼저 올리고, 눌러본 뒤 `main` 에 합칩니다.** `main` 에 바로 푸시하면
검수 없이 고객이 보는 화면이 바뀝니다.

```bash
git switch staging
# ... 고치고 커밋 ...
git push origin staging          # 검수 주소에서 확인
git switch main && git merge staging && git push origin main   # 라이브 반영
```

> ⚠️ `261001` 기준 `staging.nawoohitech.pages.dev` 는 **404 입니다.**
> Cloudflare 대시보드 → `nawoohitech` → Settings → Builds 의
> **Preview deployments 가 꺼져 있는 것으로 봅니다.** 켜야 검수 주소가 뜹니다.
> 브랜치와 `_headers` 는 이미 올라가 있어서, 켜는 순간 동작합니다.

### 내려받아서

```bash
git clone git@github.com:psw95master/PH-A-7.git
cd PH-A-7/PH-B-35
open index.html
```

### 수정할 때

머리말·꼬리말·좌측 메뉴가 14개 페이지에 반복되므로 생성 스크립트로 만듭니다.
**`.html` 을 직접 고치지 말고** `PH-B-35/build.py` 를 고친 뒤 다시 생성하십시오.

```bash
cd PH-B-35 && python3 build.py
```

`robots.txt` · `sitemap.xml` · `_redirects` · `_headers` 도 `build.py` 가 만듭니다. 직접 고치지 마십시오.

자세한 내용은 [`PH-B-35/README.md`](PH-B-35/README.md) — 무엇을 텍스트로 바꿨고 무엇을 이미지로 남겼는지,
원본과 달라진 점, 확인 필요 항목 8건이 정리돼 있습니다.

---

## 관련 문서

| 문서 | 위치 |
| --- | --- |
| 리뉴얼 플랜 제안서 v2.0 (현행) | [구글 슬라이드](https://docs.google.com/presentation/d/1sYM8vyvfJ6QdAr6vxMbj3mE3-Q0JaU5asGwnyB5Mmfk/edit) |
| 제안서 v1.0 (규격·일정 기준 원본) | [구글 슬라이드](https://docs.google.com/presentation/d/1vAZXOs4I7r0IYVBcv1o4lqu-ZEedjQoisX5e5SPnC-8/edit) |
| 메일 이력 | Gmail 라벨 `PH-A-7. 나우하이텍 웹사이트 리뉴얼` |
| 작업 로그 목차 | [`@log/README.md`](@log/README.md) |

---

## 실제 제작 전 확인할 것

| 항목 | 내용 |
| --- | --- |
| 사진 해상도 | 현행 사이트 원본이 작아 확대 시 흐림. **재촬영 필요** |
| 설비명 | 사진 13장의 장비명은 육안 판단 + 현황표 대조. 회사 확인 필요 |
| 설비 규격 | 미확인 |
| 선급 승인 | 유효 증서 확인 후 게재 여부 결정 |
| ~~주소 표기~~ | ✅ `260917` 해결. 정본은 **부산 강서구 화전산단 3로 102** (페리 확인). `261001` 재확인 — 남은 `송정동` 표기는 연혁의 2003년 소재지뿐이라 그대로 둡니다 |
| ~~전화번호~~ | ✅ `261001` 해결. **051-831-9161** (페리 확인). `~2` 를 뗐으므로 9162번 안내는 사라졌습니다 |
| 팩스 표기 | 전화만 국내 표기로 바뀌어 `+82-51-831-9163` 과 형식이 어긋납니다. 맞출지 미정 |
| 클릭 다이얼 | 화면 글자는 `051-831-9161`, `tel:` 링크는 `+82518319161` 로 다릅니다. 국내·해외 모두 걸리지만 통일할지 미정 |

나머지 확인 항목은 [`PH-B-35/README.md`](PH-B-35/README.md) 6절에 있습니다.

---

## 변경 이력

- **261001** — 실주소 `nawoohitech.co.kr` 반영 확인. `staging` 브랜치를 검수용으로 분리하고,
  검수 주소를 검색에서 빼는 `_headers` 를 `build.py` 에 추가했습니다.
  전화번호를 `051-831-9161` 로 일괄 교체했습니다.
- **260817** — 메인 화면 시안 `1an.html` · `2an.html` 과 `img/` · `shots/` 삭제.
  두 시안은 제안서 S13 삽입용으로 제작됐고 역할을 마쳤습니다. 내용은 제안서 슬라이드와
  [`@log/PH-A-7_@log_260806.md`](@log/PH-A-7_@log_260806.md) 에 남아 있습니다.
- **260806** — 저장소 개설. 당시 ID 는 `ESL-A-11 / ESL-B-24 / ESL-C-12` 였고 이후 `PH-A-7` 로 개편됐습니다.
