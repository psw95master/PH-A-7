#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
나우하이텍 정적 사이트 빌더.

원본 nawoohitech.co.kr 은 2006년식 frameset + 테이블 레이아웃으로,
본문 대부분이 JPG/GIF 안에 구워진 글자였다. 이 스크립트는 그 글자를
전부 실제 HTML 텍스트로 옮겨 담은 정적 페이지를 생성한다.
사진·도면·인증서 스캔만 이미지로 남기고 캡션은 HTML 로 뽑았다.

실행:  python3 build.py
결과:  프로젝트 루트에 *.html 생성
"""

from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
TODAY = "260817"

# =========================================================
# 회사 정보 (원본 footer.gif / left_call.gif / contents6.jpg 에서 추출)
# =========================================================
COMPANY = {
    "name_ko": "나우하이텍",
    "name_en": "NAWOO HI-TECH",
    "ceo": "김재욱",
    "biz_no": "606-10-12773",
    "zip": "618-210",
    "addr": "부산광역시 강서구 녹산동 화전산단 3로 102",
    "tel": "+82-51-831-9161~2",
    "tel_href": "+82518319161",
    "fax": "+82-51-831-9163",
    "email": "nawoo11@naver.com",
    "copyright": "COPYRIGHT(C) 2006 NAWOO HI-TECH. ALL RIGHTS RESERVED.",
}

# =========================================================
# 내비게이션
# =========================================================
NAV = [
    ("회사소개", "COMPANY INFO", [
        ("인사말", "greeting.html"),
        ("조직도", "organization.html"),
        ("연혁", "history.html"),
        ("인증현황", "certification.html"),
        ("설비현황 (가공장비·계측기)", "facility.html"),
        ("오시는길", "location.html"),
    ]),
    ("사업분야", "BUSINESS INFO", [
        ("유압장치 및 부품", "products.html"),
        ("도면소개", "drawings.html"),
    ]),
    ("품질방침", "QUALITY PLAN", [
        ("품질방침", "quality.html"),
    ]),
    ("환경방침", "ENVIRONMENT PLAN", [
        ("환경방침", "environment.html"),
    ]),
    ("Q&A", "Q & A", [
        ("Q&A", "qna.html"),
    ]),
    ("공지사항", "NOTICE", [
        ("공지사항", "notice.html"),
    ]),
]


def find_section(page):
    for label, en, items in NAV:
        for name, href in items:
            if href == page:
                return label, en, items, name
    return None, None, None, None


# =========================================================
# 공통 셸
# =========================================================
def header(page):
    items = []
    for label, en, subs in NAV:
        first = subs[0][1]
        current = any(href == page for _, href in subs)
        subhtml = "".join(
            f'<li><a href="{href}">{escape(name)}</a></li>' for name, href in subs
        )
        cur_attr = ' aria-current="page"' if current else ""
        cur_cls = "is-current" if current else ""
        items.append(
            f'<li class="{cur_cls}">'
            f'<a class="gnb__link" href="{first}"{cur_attr}>{escape(label)}</a>'
            f'<ul class="gnb__sub">{subhtml}</ul></li>'
        )
    return f"""<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="utility">
    <div class="wrap">
      <ul class="u-links">
        <li><a href="location.html">오시는길</a></li>
        <li><a href="facility.html">설비현황</a></li>
        <li><a href="notice.html">공지사항</a></li>
      </ul>
      <p class="tel">고객센터 <a href="tel:{COMPANY['tel_href']}"><strong>{COMPANY['tel']}</strong></a></p>
    </div>
  </div>
  <div class="masthead">
    <div class="wrap">
      <a class="brand" href="index.html">
        <img src="assets/img/logo.png" alt="{COMPANY['name_ko']}" width="192" height="48">
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false"
              aria-controls="gnb" aria-label="전체 메뉴 열기"><span></span></button>
      <nav class="gnb" id="gnb" aria-label="주 메뉴">
        <ul>{''.join(items)}</ul>
      </nav>
    </div>
  </div>
</header>"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__links">
      <a href="greeting.html">회사소개</a>
      <a href="location.html">오시는길</a>
      <a href="facility.html">설비현황</a>
      <a href="notice.html">공지사항</a>
    </div>
    <div class="site-footer__grid">
      <div>
        <dl>
          <dt>상호</dt><dd>{COMPANY['name_ko']}</dd>
          <dt>대표자</dt><dd>{COMPANY['ceo']}</dd>
          <dt>주소</dt><dd>({COMPANY['zip']}) {COMPANY['addr']}</dd>
          <dt>사업자등록번호</dt><dd>{COMPANY['biz_no']}</dd>
          <dt>전화</dt><dd><a href="tel:{COMPANY['tel_href']}">{COMPANY['tel']}</a></dd>
          <dt>팩스</dt><dd>{COMPANY['fax']}</dd>
          <dt>이메일</dt><dd><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></dd>
        </dl>
        <p class="copy">{COMPANY['copyright']}</p>
      </div>
    </div>
  </div>
</footer>
<script src="assets/js/nav.js"></script>"""


def page(filename, title, body, description):
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | {COMPANY['name_ko']} {COMPANY['name_en']}</title>
<meta name="description" content="{escape(description)}">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header(filename)}
{body}
{footer()}
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")
    return filename


def sub_page(filename, title, description, content, intro=None):
    """서브 페이지 셸: 페이지 헤더 + 좌측 LNB + 본문."""
    section, section_en, items, name = find_section(filename)
    def lnb_item(label, href):
        attr = ' aria-current="page"' if href == filename else ""
        return f'<li><a href="{href}"{attr}>{escape(label)}</a></li>'

    lnb_items = "".join(lnb_item(label, href) for label, href in items)
    crumbs = (
        '<li><a href="index.html">홈</a></li>'
        f'<li>{escape(section)}</li>'
        f'<li aria-current="page">{escape(name)}</li>'
    )
    body = f"""<div class="page-head">
  <div class="wrap">
    <p class="page-head__section">{escape(section_en)}</p>
    <h1 class="page-head__title">{escape(title)}</h1>
    <nav class="breadcrumb" aria-label="현재 위치"><ol>{crumbs}</ol></nav>
  </div>
</div>
<div class="wrap">
  <div class="layout">
    <nav class="lnb" aria-label="{escape(section)} 하위 메뉴">
      <div class="lnb__title"><strong>{escape(section)}</strong><span>{escape(section_en)}</span></div>
      <ul class="lnb__list">{lnb_items}</ul>
      <div class="lnb__call">
        <h3>CUSTOMER CENTER</h3>
        <p class="num">{COMPANY['tel']}</p>
        <dl>
          <dt>Fax</dt><dd>{COMPANY['fax']}</dd>
          <dt>Mail</dt><dd><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></dd>
        </dl>
      </div>
    </nav>
    <main class="content" id="main">
{content}
    </main>
  </div>
</div>"""
    return page(filename, title, body, description)


# =========================================================
# index.html — 홈
# =========================================================
def build_index():
    body = f"""<main id="main">
  <section class="hero">
    <div class="wrap hero__inner">
      <p class="hero__eyebrow">믿을 수 있는 기업 나우하이텍입니다.</p>
      <h1 class="hero__title">NAWOO <em>HI-TECH</em></h1>
      <p class="hero__lead">
        선진기술 도입과 지속적인 연구개발을 통해 앞서가는 나우하이텍은
        고효율성과 친환경성의 녹색경영 실현에 앞장서고 있습니다.
      </p>
      <ul class="hero__tags">
        <li>선박설비</li>
        <li>유압 시스템</li>
        <li>산업기계</li>
        <li>특수유압 실린더 제작</li>
      </ul>
    </div>
    <div class="hero__photo" role="img" aria-label="나우하이텍 부산 화전산단 공장 전경"></div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="section__eyebrow">Nawoo Hi-Tech</p>
        <h2 class="section__title">2002년부터 유압 실린더 한 길</h2>
        <p class="section__desc">
          유압 액튜에이터와 철도 차량 부품 전문 제작·가공 업체로 출발해,
          선박설비·산업기계·유압 시스템의 주요 부품을 국산화하고 있습니다.
        </p>
      </div>
      <div class="cards cards--3">
        <a class="card" href="greeting.html">
          <p class="card__label">Company</p>
          <h3 class="card__title">나우하이텍 소개</h3>
          <p class="card__body">최상의 기술력과 전문인재를 바탕으로 고객으로부터 가장 신뢰받는 나우하이텍입니다.</p>
          <span class="card__more">인사말 보기</span>
        </a>
        <a class="card" href="certification.html">
          <p class="card__label">Certification</p>
          <h3 class="card__title">인증현황 안내</h3>
          <p class="card__body">나우하이텍만이 가지고 있는 최고의 기술력으로 최상의 서비스를 제공해 드리겠습니다.</p>
          <span class="card__more">인증서 보기</span>
        </a>
        <a class="card" href="facility.html">
          <p class="card__label">Equipment</p>
          <h3 class="card__title">설비현황 &lsquo;가공장비·계측기&rsquo;</h3>
          <p class="card__body">고품질, 고성능의 기능을 갖춘 나우하이텍의 장비들로 최고의 결과물을 약속드립니다.</p>
          <span class="card__more">장비 목록 보기</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="wrap">
      <div class="cards">
        <div class="card card--quote">
          <p class="card__label">Environment</p>
          <h3 class="card__title">나우하이텍 환경방침</h3>
          <blockquote>&ldquo;끊임없는 환경개선을 통하여 어떤 예외도 없이 고객을 만족, 감동 시키기 위해서 최선을 다한다.&rdquo;</blockquote>
          <p class="card__body">
            나우하이텍은 모든 활동, 제품 및 서비스 환경에 미치는 영향을 깊이 인식하고,
            환경오염방지 및 재난예방에 최선을 다하겠습니다.
          </p>
          <a class="card__more" href="environment.html" style="color:#94c34b">환경방침 전문</a>
        </div>
        <div class="card">
          <p class="card__label">Customer Center</p>
          <h3 class="card__title">고객센터</h3>
          <div class="contact-strip">
            <div>
              <p class="big"><a href="tel:{COMPANY['tel_href']}">{COMPANY['tel']}</a></p>
              <dl>
                <dt>Fax</dt><dd>{COMPANY['fax']}</dd>
                <dt>E-mail</dt><dd><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></dd>
              </dl>
            </div>
          </div>
          <a class="card__more" href="location.html">오시는길</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="section__eyebrow">Notice</p>
        <h2 class="section__title">공지사항</h2>
      </div>
      <ul class="notice-list">
        <li>
          <a href="notice.html#post-3">
            <span class="notice-list__badge">공지</span>
            <span class="notice-list__title">나우하이텍 확장이전 했습니다.</span>
            <time class="notice-list__date" datetime="2010-08-26">2010-08-26</time>
          </a>
        </li>
        <li>
          <a href="notice.html#post-1">
            <span class="notice-list__title">홈페이지가 오픈 되었습니다.</span>
            <time class="notice-list__date" datetime="2006-10-18">2006-10-18</time>
          </a>
        </li>
      </ul>
    </div>
  </section>
</main>"""
    return page("index.html", "홈", body,
                "부산 화전산단 소재 유압 실린더·유압 시스템 전문 제작 업체 나우하이텍(NAWOO HI-TECH). "
                "선박설비, 산업기계, 특수유압 실린더를 제작합니다.")


# =========================================================
# greeting.html — 인사말
# =========================================================
def build_greeting():
    content = """<div class="greeting">
  <figure class="greeting__photo">
    <img src="assets/img/ceo-photo.jpg" width="388" height="207"
         alt="집무실에서 촬영한 나우하이텍 대표 김재욱">
  </figure>
  <div>
    <h2 class="greeting__title" style="padding-left:0">나우하이텍을 찾아주셔서 감사합니다.</h2>
    <p class="greeting__sub">안녕하십니까? 대표 김재욱입니다.</p>
    <p>
      나우하이텍은 2002년 유압 액튜에이터, 철도 차량 부품 전문 제작 및 가공 업체(대표 김재욱)로
      설립하여 약 8년간 기계 제조업에 전념한 회사로서, 다양한 최신 산업 특수 유압 실린더 제작 및
      꾸준한 기술개발을 통하여 선박설비 및 산업기계, 유압 시스템 등의 주요 부품 및 설비를
      국산화하고 생산하는 기업으로 성장하고 있습니다.
    </p>
  </div>
</div>

<div class="callout">
  <p>
    <strong>고객의 관심과 격려 속에서 발전하고 있는 나우하이텍은</strong>
    고객만족 및 기술 개발의 일환으로 2005년 품질경영시스템 인증(KSA9001:2001 / ISO9001:2000) 및
    환경경영시스템 인증(KSA14001:2004 / ISO14001:2004)을 획득하여 끊임없는 기술개발에 노력해 왔습니다.
  </p>
</div>

<p>
  특히, 특수 ABS 유압실린더 및 시스템을 제조한 경험으로 선박 윈치용 브레이크 실린더 및
  DSP PRESS 100Ton, 200Ton, 300Ton용 유압실린더를 다년간의 노력 끝에 개발을 완료하고
  양산체제를 구축하여, 본격적인 생산판매로 롤스로이스 마린 코리아(주), 현대위아(주) 및 (주)로템,
  보쉬 렉스로스, 동양하이드텍, 한국철강, (주)협신, 한국기계연구원 등의 다국적 기업에 납품하여
  국내외 시장에서 많은 호평을 받고 있습니다.
</p>

<p>
  역동적인 대한민국의 산업사회에서, 기계 제조업에 종사한지 8년이라는 짧은 연력을 가진 저희
  나우하이텍의 전 임직원은 무한한 책임감과 자긍심을 가지고 항상 고객만족을 생각하며,
  격려와 질책을 감수하며 고객과 함께 발전하고 가치창조를 추구하여 나갈 것이며,
  인간의 미래를 생각하는 기업, 환경을 생각하는 기업, 우리의 제품과 품질에 책임지며 개선하는
  기업으로 끊임없이 노력하겠습니다.
</p>

<p class="greeting__sign">대표 김재욱 올림</p>"""
    return sub_page("greeting.html", "인사말",
                    "나우하이텍 대표 김재욱 인사말. 2002년 설립 이후 특수 유압 실린더와 유압 시스템 국산화에 매진해 왔습니다.",
                    content)


# =========================================================
# organization.html — 조직도
# =========================================================
ORG_UNITS = [
    ("기술영업부", "이사", False, []),
    ("관리부", "이사 / 총무 / 경리", False, []),
    ("품질보증부", "과장", False, []),
    ("기술개발", "차장", True,
     ["유압 프레스 및 유압 공급 장치", "표준 및 특수 유압 실린더", "특수 공기압 실린더"]),
    ("생산기술", "차장", True,
     ["유압 프레스 및 유압 공급 장치", "표준 및 특수 유압 실린더", "특수 공기압 실린더"]),
]


def build_organization():
    units = []
    for name, role, gray, tasks in ORG_UNITS:
        task_html = ""
        if tasks:
            lis = "".join(f"<li>{escape(t)}</li>" for t in tasks)
            task_html = f'<ul class="org__tasks">{lis}</ul>'
        units.append(
            f'<div class="org__unit">'
            f'<p class="org__name">{escape(name)}</p>'
            f'<p class="org__role{" org__role--gray" if gray else ""}">{escape(role)}</p>'
            f'{task_html}</div>'
        )
    content = f"""<h2>조직도</h2>
<div class="org">
  <div class="org__top"><p class="org__ceo">대표이사</p></div>
  <div class="org__grid">{''.join(units)}</div>
</div>
<p class="note">
  원본 조직도 이미지에서 기술개발·생산기술 부서의 세 번째 업무는
  &ldquo;특수 공기압 실린더 실린더&rdquo;로 표기돼 있었습니다. 중복 표기로 보아
  &ldquo;특수 공기압 실린더&rdquo;로 정리했습니다. ({TODAY} 판단)
</p>"""
    return sub_page("organization.html", "조직도",
                    "나우하이텍 조직도 — 대표이사 아래 기술영업부, 관리부, 품질보증부, 기술개발, 생산기술 5개 부서.",
                    content)


# =========================================================
# history.html — 연혁
# =========================================================
HISTORY = [
    ("2009", [
        ("12", "나우하이텍 신축 사옥 완공 및 확장이전", "부산시 강서구 녹산동",
         ["대지 500평 · 공장 300평 · 사무실 100평",
          "주요품목 : 유압실린더 제작",
          "각종 산업기계부품 가공"]),
    ]),
    ("2007", [
        ("08", "(주)한국철강 협력업체 등록", None, []),
    ]),
    ("2003", [
        ("01", "나우하이텍 사옥 확장 이전", "부산시 강서구 송정동",
         ["주요품목 : 유압실린더 제작, 각종 산업기계부품 가공"]),
        ("01", "(주)위아 협력업체 등록", None, []),
    ]),
    ("2002", [
        ("10", "나우하이텍 설립", "대표 김재욱 · 부산시 사상구",
         ["주요품목 : 유압실린더 제작"]),
        ("11", "롤스로이스 마린 코리아(주) 협력업체 등록", None, []),
        ("12", "보쉬렉스로스(주) 협력업체 등록", None, []),
    ]),
]


def build_history():
    blocks = []
    for year, entries in HISTORY:
        items = []
        for month, title, place, metas in entries:
            meta_html = ""
            lines = ([escape(place)] if place else []) + [escape(m) for m in metas]
            if lines:
                meta_html = '<div class="history__meta">' + \
                            "".join(f"<span>{l}</span>" for l in lines) + "</div>"
            items.append(
                f'<div class="history__item">'
                f'<p class="history__month">{month}.</p>'
                f'<div class="history__desc"><strong>{escape(title)}</strong>{meta_html}</div>'
                f'</div>'
            )
        blocks.append(
            f'<div class="history__year">'
            f'<p class="history__label">{year}</p>'
            f'<div class="history__items">{"".join(items)}</div></div>'
        )
    content = f"""<h2>연혁</h2>
<div class="history">{''.join(blocks)}</div>
<p class="note">
  원본 연혁 이미지는 2009년 12월까지만 기재돼 있습니다. 이후 이력은 원본에 없어 채우지 않았습니다.
  ※확인 필요
</p>"""
    return sub_page("history.html", "연혁",
                    "2002년 설립부터 2009년 화전산단 신축 사옥 확장이전까지 나우하이텍 연혁.",
                    content)


# =========================================================
# certification.html — 인증현황
# =========================================================
CERTS = [
    ("cert-iso9001-2008.jpg", "ISO 9001:2008 품질경영시스템 인증서",
     [("인증기관", "MSA Certification Co., Ltd."), ("인증번호", "KorQ-083580")],
     "MSA Certification 발행 ISO 9001:2008 품질경영시스템 인증서 스캔본"),
    ("cert-iso14001-2004.jpg", "ISO 14001:2004 환경경영시스템 인증서",
     [("인증기관", "MSA Certification Co., Ltd."), ("인증번호", "KorE-081806")],
     "MSA Certification 발행 ISO 14001:2004 환경경영시스템 인증서 스캔본"),
    ("cert-gl-welding.jpg", "Germanischer Lloyd 용접절차 승인서",
     [("인증기관", "Germanischer Lloyd"), ("문서번호", "WPS-No. NWH-FC-01-2008-04-08")],
     "Germanischer Lloyd 발행 용접절차(WPS) 승인 인증서 스캔본"),
    ("cert-gl-hydraulic.jpg", "Germanischer Lloyd 제조공정 승인서",
     [("인증기관", "Germanischer Lloyd"), ("승인범위", "Hydraulic Cylinders")],
     "Germanischer Lloyd 발행 유압 실린더 제조공정 승인 인증서 스캔본"),
    ("cert-iso9001-2015.jpg", "ISO 9001:2015 품질경영시스템 인증서",
     [("인증기관", "GERMAN CERT"), ("인증번호", "KorQ-083580"),
      ("인증범위", "유공압기계의 설계, 개발, 제조 및 부가서비스")],
     "GERMAN CERT 발행 ISO 9001:2015 품질경영시스템 인증서 스캔본"),
    ("cert-iso14001-2015.jpg", "ISO 14001:2015 환경경영시스템 인증서",
     [("인증기관", "GERMAN CERT"), ("인증번호", "KorE-081806"),
      ("인증범위", "유공압기계의 설계, 개발, 제조")],
     "GERMAN CERT 발행 ISO 14001:2015 환경경영시스템 인증서 스캔본"),
]


def cert_tiles(certs):
    tiles = []
    for src, title, metas, alt in certs:
        meta_html = ""
        if metas:
            meta_html = '<dl class="tile__meta">' + "".join(
                f"<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>" for k, v in metas
            ) + "</dl>"
        tiles.append(
            f'<figure class="tile">'
            f'<span class="tile__frame"><img src="assets/img/{src}" alt="{escape(alt)}" loading="lazy"></span>'
            f'<figcaption class="tile__cap">{escape(title)}</figcaption>{meta_html}</figure>'
        )
    return f'<div class="gallery">{"".join(tiles)}</div>'


def build_certification():
    content = f"""<h2>인증현황</h2>
<p>
  나우하이텍은 품질경영시스템(ISO 9001)과 환경경영시스템(ISO 14001) 인증을 유지하고 있으며,
  선급 인증기관 Germanischer Lloyd 로부터 용접절차와 유압 실린더 제조공정을 승인받았습니다.
</p>
{cert_tiles(CERTS)}
<p class="note">
  인증서 이미지는 원본을 그대로 유지했습니다. 스캔 해상도가 낮아 판독되지 않는 인증일자·유효기간은
  적지 않았습니다. ※확인 필요
</p>"""
    return sub_page("certification.html", "인증현황",
                    "나우하이텍 ISO 9001 / ISO 14001 및 Germanischer Lloyd 인증 현황.",
                    content)


# =========================================================
# facility.html — 설비현황
# =========================================================
MACHINES = [
    ("Lathe", "Φ850 × 4000(L)", "1", "Apr. 2007", "Danita"),
    ("Lathe", "Φ580 × 2000(L)", "1", "May. 2004", "화천기계"),
    ("Lathe", "Φ460 × 1000(L)", "1", "May. 2004", "화천기계"),
    ("CNC Lathe", "PUMA 300 (12”)", "1", "May. 2005", "두산인프라코어"),
    ("CNC Lathe", "PUMA CT 300 (10”)", "1", "Oct. 2007", "두산인프라코어"),
    ("Milling Machine", "DMB-45 (U5호)", "1", "May. 2004", "두산인프라코어"),
    ("Radial Drill M/C", "2,000(L)", "1", "Apr. 2004", "Nambuk"),
    ("Co2 Welding M/C", "TR-650", "2", "July. 2008", "Taesin"),
    ("TIG Welding M/C", "WS-ADT(500S)", "1", "July. 2008", "Taesin"),
    ("Co2/MAG Welding M/C", "MAX 800C", "1", "Apr. 2009", "Easywel"),
    ("Lathe", "Φ1500 × 10000(L)", "1", "Nov. 2009", "Dainichi"),
    ("Hoist Crane", "15 Ton", "1", "Dec. 2009", "신성"),
    ("Hoist Crane", "5 Ton", "1", "Dec. 2009", "신성"),
    ("Hydraulic test M/C", "pressure 700bar", "1", "Dec. 2009", "동양하이드텍"),
    ("Air compressor", "10HP", "2", "Nov. 2009", "대동"),
    ("Paint booth", "—", "1", "Nov. 2009", "태일산업"),
    ("CNC Lathe", "Φ850 × 3000(L)", "1", "May. 2005", "Danita"),
    ("정반", "500 × 2000", "1", "Jan. 2010", "나우하이텍"),
]

GAUGES = [
    ("도막 두께 측정기", "0~0.5mm", "1", "2005", "Mitutoyo(Japan)"),
    ("Micrometer", "0~25mm", "3", "2002", "Mitutoyo(Japan)"),
    ("Micrometer", "25~50mm", "3", "2002", "Mitutoyo(Japan)"),
    ("Micrometer", "50~75mm", "3", "2002", "Mitutoyo(Japan)"),
    ("Micrometer", "75~100mm", "3", "2002", "Mitutoyo(Japan)"),
    ("Micrometer", "100~125mm", "2", "2002", "Mitutoyo(Japan)"),
    ("Micrometer", "125~150mm", "3", "2008", "Mitutoyo(Japan)"),
    ("Micrometer", "150~175mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Micrometer", "150~300mm", "1", "2002", "Mitutoyo(Japan)"),
    ("Micrometer", "300~400mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Micrometer", "400~500mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Micrometer", "600~700mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Micrometer", "700~800mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Cylinder gauge", "18~35mm", "2", "2002", "Mitutoyo(Japan)"),
    ("Cylinder gauge", "35~60mm", "3", "2002", "Mitutoyo(Japan)"),
    ("Cylinder gauge", "50~100mm", "2", "2002", "Mitutoyo(Japan)"),
    ("Cylinder gauge", "160~250mm", "1", "2002", "Mitutoyo(Japan)"),
    ("Cylinder gauge", "250~400mm", "1", "2002", "Mitutoyo(Japan)"),
    ("Inside micrometer", "50~1000mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Vernier Height gauge", "0~300mm", "1", "2002", "Mitutoyo(Japan)"),
    ("Vernier Height gauge", "0~600mm", "1", "2002", "Mitutoyo(Japan)"),
    ("정반", "300 × 1000 × 2000", "1", "2002", "나우하이텍"),
    ("Inside micrometer", "0~150mm", "1", "2009", "Mitutoyo(Japan)"),
    ("Vernier Calipers", "0~300mm", "6", "2009", "Mitutoyo(Japan)"),
    ("Vernier Calipers", "0~600mm", "2", "2009", "Mitutoyo(Japan)"),
    ("Vernier Calipers", "0~1000mm", "1", "2009", "Mitutoyo(Japan)"),
]

FACILITY_PHOTOS = [
    ("facility-01.jpg", "대형 선반(Lathe) — Φ1500 × 10000(L)"),
    ("facility-02.jpg", "장척 가공용 선반 및 소재 적치 구역"),
    ("facility-03.jpg", "선반 가공기"),
    ("facility-04.jpg", "범용 선반(Lathe)"),
    ("facility-05.jpg", "레이디얼 드릴링 머신(Radial Drill M/C) — 2,000(L)"),
    ("facility-06.jpg", "밀링 머신(Milling Machine) 가공 작업"),
    ("facility-07.jpg", "CNC 선반(PUMA 시리즈)"),
    ("facility-08.jpg", "머시닝 센터"),
    ("facility-09.jpg", "CNC 선반 — Dainichi"),
    ("facility-10.jpg", "유압 시험기(Hydraulic test M/C) — 700bar"),
    ("facility-11.jpg", "호이스트 크레인이 설치된 공장동 전경"),
    ("facility-12.jpg", "정반(定盤) — 500 × 2000"),
    ("facility-13.jpg", "도장 부스(Paint booth)"),
]


def data_table(caption, rows, first_col):
    body = "".join(
        "<tr>"
        f"<td>{escape(a)}</td><td>{escape(b)}</td>"
        f'<td class="num">{escape(c)}</td><td>{escape(d)}</td><td>{escape(e)}</td>'
        "</tr>"
        for a, b, c, d, e in rows
    )
    return f"""<p class="scroll-hint">표를 좌우로 밀어 나머지 항목을 볼 수 있습니다.</p>
<div class="table-scroll" tabindex="0" role="region" aria-label="{escape(caption)} 표">
  <table class="data-table">
    <caption>{escape(caption)} — 총 {len(rows)}종</caption>
    <thead>
      <tr>
        <th scope="col">{escape(first_col)}</th>
        <th scope="col">Capacity</th>
        <th scope="col">Q&rsquo;ty</th>
        <th scope="col">Installed Date</th>
        <th scope="col">Maker</th>
      </tr>
    </thead>
    <tbody>{body}</tbody>
  </table>
</div>"""


def build_facility():
    photos = "".join(
        f'<figure class="tile">'
        f'<span class="tile__frame"><img src="assets/img/{src}" alt="{escape(cap)}" loading="lazy"></span>'
        f'<figcaption class="tile__cap">{escape(cap)}</figcaption></figure>'
        for src, cap in FACILITY_PHOTOS
    )
    content = f"""<h2>가공장비 현황</h2>
{data_table('가공장비 현황', MACHINES, 'Facility')}

<h2>계측기 현황</h2>
{data_table('계측기 현황', GAUGES, 'Facility')}

<h2>설비 사진</h2>
<p>부산 화전산단 공장에 설치된 주요 가공·검사 설비입니다.</p>
<div class="gallery gallery--wide gallery--photo">{photos}</div>
<p class="note">
  설비 사진의 장비명은 원본 이미지에 캡션이 없어, 위 가공장비 현황표와 대조해 붙였습니다.
  개별 장비 식별은 ※확인 필요 ({TODAY} 판단)
</p>"""
    return sub_page("facility.html", "설비현황 (가공장비·계측기)",
                    "나우하이텍 보유 가공장비 18종, 계측기 26종 목록과 공장 설비 사진.",
                    content)


# =========================================================
# location.html — 오시는길
# =========================================================
def build_location():
    kakao = "https://map.kakao.com/?q=" + "부산광역시 강서구 화전산단3로 102"
    content = f"""<h2>오시는길 안내</h2>
<table class="info-table">
  <tbody>
    <tr><th scope="row">주소</th>
        <td>({COMPANY['zip']}) 부산광역시 강서구 화전산단3로 102<br>
            <span style="color:var(--muted);font-size:14px">(지번) 부산광역시 강서구 녹산동 화전산단</span></td></tr>
    <tr><th scope="row">전화</th><td><a href="tel:{COMPANY['tel_href']}">{COMPANY['tel']}</a></td></tr>
    <tr><th scope="row">팩스</th><td>{COMPANY['fax']}</td></tr>
    <tr><th scope="row">이메일</th><td><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></td></tr>
  </tbody>
</table>

<div class="map-frame">
  <div>
    <p>원본 페이지의 다음 지도 위젯은 외부 스크립트에 의존해 이 정적 사이트에서는 걷어냈습니다.</p>
    <a class="btn" href="{escape(kakao)}" target="_blank" rel="noopener">카카오맵에서 위치 보기</a>
  </div>
</div>
<p class="note">
  지도 API 키를 발급해 넣으면 이 자리에 지도를 다시 임베드할 수 있습니다.
  어떤 지도 서비스를 쓸지 ※확인 필요
</p>"""
    return sub_page("location.html", "오시는길",
                    "나우하이텍 찾아오시는 길 — 부산광역시 강서구 화전산단3로 102.",
                    content)


# =========================================================
# products.html — 유압장치 및 부품
# =========================================================
PRODUCTS = [
    ("product-cosma1800-press.jpg", "COSMA1800 PRESS", "프레스용 유압 실린더 3본"),
    ("product-posco-intermesh-cylinder.jpg", "POSCO Intermesh cylinder", "제철 설비용 인터메시 실린더"),
    ("product-posco-travers-car-cylinder.jpg", "POSCO Travers car cylinder", "트래버스 카 구동 유압 실린더"),
    ("product-gm2250-press.jpg", "GM2250 PRESS", "프레스용 대형 유압 실린더"),
    ("product-1600ton-scrap-shear.jpg", "1600Ton SCRAP SHEAR", "스크랩 절단기용 유압 실린더"),
    ("product-moving-cylinder-oscillator.jpg", "Moving cylinder for Oscillator", "오실레이터용 무빙 실린더"),
    ("product-posco-pot-hydraulic-system.jpg", "POSCO POT Hydraulic system", "포트 설비용 유압 시스템"),
    ("product-dam-gate-cylinder.jpg",
     "Synchronous Controlled Extra Large Hydraulic Cylinder for Dam Gate Positioning",
     "댐 수문 위치제어용 동기 제어 초대형 유압 실린더"),
    ("product-marine-winch-break-cylinder.jpg", "해상 윈치용 Break Cylinder", "선박 윈치 브레이크 실린더"),
    ("product-500ton-block-lifter-cylinder.jpg", "Hydraulic cylinder for 500Ton Block lifter",
     "500톤 블록 리프터용 유압 실린더"),
    ("product-dsme-h2298-cylinder.jpg", "DSME H2298 Hydraulic cylinder", "선박 H2298 호선용 유압 실린더"),
    ("product-2300ton-balance-cylinder.jpg", "Balance Cylinder for 2300Ton blanking Press",
     "2300톤 블랭킹 프레스용 밸런스 실린더"),
    ("product-korea-institute.jpg", "KOREA INSTITUTE", "한국기계연구원 납품 유압 실린더"),
    ("product-100ton-ludder-truck-cylinder.jpg", "Hydraulic cylinder for 100Ton ludder truck",
     "100톤급 래더 트럭용 유압 실린더"),
]


def build_products():
    tiles = "".join(
        f'<figure class="tile">'
        f'<span class="tile__frame"><img src="assets/img/{src}" alt="{escape(title)} — {escape(desc)}" loading="lazy"></span>'
        f'<figcaption class="tile__cap">{escape(title)}</figcaption>'
        f'<p class="tile__meta">{escape(desc)}</p></figure>'
        for src, title, desc in PRODUCTS
    )
    content = f"""<h2>유압장치 및 부품</h2>
<p>
  선박설비·제철설비·산업기계에 들어가는 표준 및 특수 유압 실린더와 유압 시스템을 제작합니다.
  아래는 주요 납품 실적입니다.
</p>
<div class="gallery gallery--wide gallery--photo">{tiles}</div>
<p class="note">
  제품명은 원본 이미지에 인쇄된 영문 캡션을 그대로 옮겼습니다.
  각 항목의 한글 설명은 제품명을 풀어 쓴 것으로, 사양 확인이 필요하면 담당자에게 문의하세요. ({TODAY} 판단)
</p>"""
    return sub_page("products.html", "유압장치 및 부품",
                    "나우하이텍 유압 실린더·유압 시스템 주요 납품 실적 14건.",
                    content)


# =========================================================
# drawings.html — 도면소개
# =========================================================
DRAWINGS = [
    ("drawing-nwmb-90r.jpg", "MANIFOLD BLOCK (NWMB TYPE)", "1.pdf",
     [("MODEL", "NWMB-90R-220/125-1040"), ("WORKING PRESSURE", "220 bar"), ("TEST PRESSURE", "300 bar")]),
    ("drawing-nwmb-90l.jpg", "MANIFOLD BLOCK (NWMB TYPE)", "2.pdf",
     [("MODEL", "NWMB-90L-220/125-1040"), ("WORKING PRESSURE", "220 bar"), ("TEST PRESSURE", "300 bar")]),
    ("drawing-nwmb-180l.jpg", "MANIFOLD BLOCK (NWMB TYPE)", "3.pdf",
     [("MODEL", "NWMB-180L-220/125-1040"), ("WORKING PRESSURE", "220 bar"), ("TEST PRESSURE", "300 bar")]),
    ("drawing-nwmb-180r.jpg", "MANIFOLD BLOCK (NWMB TYPE)", "4.pdf",
     [("MODEL", "NWMB-180R-220/125-1040"), ("WORKING PRESSURE", "220 bar"), ("TEST PRESSURE", "300 bar")]),
    ("drawing-hydraulic-unit.jpg", "HYDRAULIC UNIT 조립도", "5.pdf",
     [("작동유", "ISO VG 46"), ("MODEL", "※확인 필요")]),
    ("drawing-cylinder-assy.jpg", "HYDRAULIC CYLINDER 조립도", "6.pdf",
     [("MODEL", "※확인 필요")]),
    ("drawing-telescopic-cylinder.jpg", "TELESCOPIC HYDRAULIC CYLINDER ASSEMBLY", "7.pdf",
     [("MODEL", "NW140-FB-250/180-3450")]),
]


def build_drawings():
    tiles = []
    for src, title, pdf, metas in DRAWINGS:
        meta_html = '<dl class="tile__meta">' + "".join(
            f"<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>" for k, v in metas
        ) + "</dl>"
        tiles.append(
            f'<figure class="tile">'
            f'<span class="tile__frame"><img src="assets/img/{src}" alt="{escape(title)} 도면" loading="lazy"></span>'
            f'<figcaption class="tile__cap">{escape(title)}</figcaption>{meta_html}'
            f'<a class="btn-pdf" href="assets/pdf/{pdf}" target="_blank" rel="noopener">'
            f'파일 보기 <span class="sr-only">({escape(title)})</span></a></figure>'
        )
    content = f"""<h2>도면소개</h2>
<p>매니폴드 블록, 유압 유닛, 텔레스코픽 실린더 도면입니다. 각 항목의 PDF 버튼을 누르면 원본 도면이 새 창으로 열립니다.</p>
<div class="gallery gallery--wide">{''.join(tiles)}</div>
<p style="color:var(--muted);font-size:14px">LADLE TILTING HYDRAULIC CYLINDER FOR MANIFOLD BLOCK</p>
<p class="note">
  원본에서 &ldquo;PDF 파일 보기&rdquo; 버튼은 이미지에 그려진 이미지맵이었습니다. 실제 링크(<code>pdf/1.pdf</code>~<code>7.pdf</code>)를
  그대로 살려 HTML 버튼으로 바꿨습니다. 5·6번 도면의 모델명은 썸네일 해상도로는 판독되지 않아 비워 뒀습니다. ※확인 필요
</p>"""
    return sub_page("drawings.html", "도면소개",
                    "나우하이텍 매니폴드 블록(NWMB TYPE), 유압 유닛, 텔레스코픽 실린더 도면 7종.",
                    content)


# =========================================================
# quality.html — 품질방침
# =========================================================
def build_quality():
    content = f"""<h2>품질방침</h2>
<div class="callout">
  <p><strong>고객만족을 위한 제품 · 품질제일을 위한 경영 · 품질보증 활동의 생활화</strong></p>
</div>
<p>
  나우하이텍(이하 &ldquo;당사&rdquo;라 함)은 전사원이 개선의식, 품질의식, 원가의식, 위기의식의 고취를 통하여
  고객이 요구하는 품질의 제품을 적기에 공급함으로써 고객만족 경영을 실현하기 위하여,
  다음과 같이 품질방침을 정한다. 따라서, 이를 달성하기 위해서 전사원은 성실하고 정직한 자세로
  맡은 바 책임을 다하여야 하며 품질방침을 효율적으로 수행하기 위하여 당사는 ISO 9001 : 2000 규격을
  기본으로 품질경영 시스템을 수립하고 방침관리 PROCESS에 따라 연도별 사업계획 및 목표를 설정하고
  다음 각 항을 원칙으로 품질방침을 실행한다. 본인은 공장장을 품질경영대리인으로 선정하며
  아래와 같이 책임과 권한을 위임한다.
</p>

<h2>직무</h2>
<ol class="list-num">
  <li>품질경영시스템에 필요한 프로세스가 수립되고 실행, 유지</li>
  <li>품질경영시스템 성과 및 개선필요성에 대하여 대표이사에게 보고</li>
  <li>조직 전반에 고객요구사항을 반영하기 위한 관리</li>
  <li>품질경영시스템 운영상 발생되는 조직간의 문제해결</li>
</ol>

<h2>품질경영시스템 인증서 (KIC)</h2>
{cert_tiles([
    ("cert-kic-quality-1.jpg", "품질경영시스템 인증서 (국문)",
     [("규격", "ISO 9001:2000 / KS A 9001:2007"), ("발행", "MSA Certification")],
     "MSA Certification 발행 품질경영시스템 인증서 국문 스캔본"),
    ("cert-kic-quality-2.jpg", "품질경영시스템 인증서 (사본)",
     [("규격", "ISO 9001:2000 / KS A 9001:2007"), ("발행", "MSA Certification")],
     "MSA Certification 발행 품질경영시스템 인증서 사본 스캔본"),
])}
<p class="note">
  본문에 적힌 기준 규격은 원본 그대로 ISO 9001 : 2000 입니다.
  <a href="certification.html">인증현황</a> 페이지에는 ISO 9001:2015 인증서가 함께 게시돼 있어,
  현행 방침문의 규격 표기 갱신 여부는 ※확인 필요
</p>"""
    return sub_page("quality.html", "품질방침",
                    "나우하이텍 품질방침 전문과 품질경영대리인 직무, 품질경영시스템 인증서.",
                    content)


# =========================================================
# environment.html — 환경방침
# =========================================================
ENV_ITEMS = [
    "환경관련 법규와 수립된 환경시스템 및 그 밖의 요건을 준수함으로 환경관리의 효율성을 제고한다.",
    "폐기물의 분리수거, 재활용 및 재이용을 통하여 오염물질 발생 최소화를 지속적으로 개선한다.",
    "제품 재료의 유해화학물질의 관리와 각 국가의 법 규제 요구사항을 준수한다.",
    "모든 이해관계자들과 원활한 의사소통으로 환경품질보증에 대한 의지 및 투명성을 보장한다.",
    "주요 환경측면을 파악하고 이에 대한 환경목표 및 세부목표를 수립 실행하며, "
    "감사와 경영자 검토를 통해 환경품질보증 시스템의 효율성을 파악한다.",
    "환경품질보증 Manual의 문서가 활용되기 위해 모든 종업원에게 전달, 교육을 실시하여 숙지시킨다.",
    "당사의 환경방침은 전 종업원이 볼 수 있도록 게시한다.",
]


def build_environment():
    items = "".join(f"<li>{escape(t)}</li>" for t in ENV_ITEMS)
    content = f"""<h2>환경방침</h2>
<div class="callout">
  <p><strong>끊임없는 환경개선을 통해 어떤 예외도 없이 고객을 만족, 감동 시키기 위해 최선을 다한다.</strong></p>
</div>
<p>
  나우하이텍(이하 &ldquo;당사&rdquo;라 한다.)은 당사의 모든 활동, 제품 및 서비스 환경에 미치는 영향을 깊이
  인식하고, 환경오염방지 및 재난예방에 최선을 다하며, 이를 위하여 다음과 같은 환경방침을 설정하여
  지속적인 개선과 환경오염방지를 전개할 것을 선언합니다.
</p>

<ol class="list-num">{items}</ol>

<p style="color:var(--muted)">
  위 사항을 성실히 이행하기 위하여 지속적인 교육을 실시하며, 대외에 공개하여 투명성을 유지하며,
  환경친화적인 기업으로써 환경경영을 성취하고자 사장 본인이 서약 선포합니다.
</p>

<h2>환경경영시스템 인증서 (KIC)</h2>
{cert_tiles([
    ("cert-kic-env-1.jpg", "환경경영시스템 인증서 (국문)",
     [("규격", "ISO 14001:2004 / KS A 14001:2004"), ("발행", "MSA Certification")],
     "MSA Certification 발행 환경경영시스템 인증서 국문 스캔본"),
    ("cert-kic-env-2.jpg", "환경경영시스템 인증서 (영문)",
     [("규격", "ISO 14001:2004 / DIN EN ISO 14001:2005"), ("발행", "MSA Certification")],
     "MSA Certification 발행 환경경영시스템 인증서 영문 스캔본"),
])}"""
    return sub_page("environment.html", "환경방침",
                    "나우하이텍 환경방침 7개 항목 전문과 환경경영시스템 인증서.",
                    content)


# =========================================================
# notice.html — 공지사항
# =========================================================
NOTICES = [
    (3, "나우하이텍 확장이전 했습니다.", "2010-08-26", "관리자", True,
     ["화전산업단지로 이사를 왔습니다.",
      "여러분의 성원과 도움으로 좋은 환경에서 더 좋은 제품을 만들 수 있게 되었습니다.",
      "앞으로도, 많은 관심 부탁드립니다."]),
    (1, "홈페이지가 오픈 되었습니다.", "2006-10-18", "관리자", False, []),
]


def build_notice():
    articles = []
    for num, title, date, writer, pinned, paras in NOTICES:
        body = "".join(f"<p>{escape(p)}</p>" for p in paras) or \
               '<p style="color:var(--muted)">등록된 본문이 없습니다.</p>'
        badge = '<span class="notice-list__badge">공지</span> ' if pinned else ""
        articles.append(f"""<article id="post-{num}" class="post">
  <h2 class="post__title">{badge}{escape(title)}</h2>
  <p style="font-size:14px;color:var(--muted);margin-bottom:16px">
    작성자 {escape(writer)} · <time datetime="{date}">{date}</time>
  </p>
  {body}
</article>""")
    content = f"""<h2>공지사항</h2>
<p style="font-size:14px;color:var(--muted)">총 {len(NOTICES)}건</p>
<ul class="notice-list">
  <li><a href="#post-3"><span class="notice-list__badge">공지</span>
    <span class="notice-list__title">나우하이텍 확장이전 했습니다.</span>
    <time class="notice-list__date" datetime="2010-08-26">2010-08-26</time></a></li>
  <li><a href="#post-1">
    <span class="notice-list__title">홈페이지가 오픈 되었습니다.</span>
    <time class="notice-list__date" datetime="2006-10-18">2006-10-18</time></a></li>
</ul>

{''.join(articles)}

<p class="note">
  원본 게시판은 PHP로 돌아가는 동적 게시판입니다. 이 정적 사이트에는 {TODAY} 기준 등록돼 있던
  공지 {len(NOTICES)}건을 그대로 옮겨 담았습니다. 글쓰기·댓글 기능은 백엔드가 있어야 합니다. ※확인 필요
</p>"""
    return sub_page("notice.html", "공지사항",
                    "나우하이텍 공지사항 — 확장이전 안내, 홈페이지 오픈 안내.",
                    content)


# =========================================================
# qna.html — Q&A (빈 상태)
# =========================================================
def build_qna():
    content = f"""<h2>Q&amp;A</h2>
<p>제품 사양, 견적, 납기 문의를 남겨 주시면 담당자가 확인 후 연락드립니다.</p>

<div class="empty">
  <h2>아직 공개된 문의글이 없습니다</h2>
  <p>원본 Q&amp;A 게시판은 글쓰기·답변이 서버에서 처리되는 동적 게시판입니다.<br>
     정적 사이트로 옮기면서 목록은 비워 두었습니다.</p>
  <a class="btn" href="mailto:{COMPANY['email']}?subject=%5B%EB%AC%B8%EC%9D%98%5D%20">이메일로 문의하기</a>
  <a class="btn btn--ghost" href="tel:{COMPANY['tel_href']}" style="margin-left:8px">전화 문의</a>
</div>

<h2>문의처</h2>
<table class="info-table">
  <tbody>
    <tr><th scope="row">전화</th><td><a href="tel:{COMPANY['tel_href']}">{COMPANY['tel']}</a></td></tr>
    <tr><th scope="row">팩스</th><td>{COMPANY['fax']}</td></tr>
    <tr><th scope="row">이메일</th><td><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></td></tr>
    <tr><th scope="row">주소</th><td>({COMPANY['zip']}) {COMPANY['addr']}</td></tr>
  </tbody>
</table>"""
    return sub_page("qna.html", "Q&A",
                    "나우하이텍 제품 사양·견적·납기 문의처 안내.",
                    content)


# =========================================================
# 404.html
# =========================================================
def build_404():
    body = """<main id="main" class="wrap error-page">
  <p class="error-page__code">404</p>
  <h1>요청하신 페이지를 찾을 수 없습니다</h1>
  <p>주소가 바뀌었거나 삭제된 페이지입니다.</p>
  <a class="btn" href="index.html">홈으로 이동</a>
  <a class="btn btn--ghost" href="greeting.html" style="margin-left:8px">회사소개 보기</a>
</main>"""
    return page("404.html", "페이지를 찾을 수 없습니다", body, "요청하신 페이지를 찾을 수 없습니다.")


# =========================================================
def main():
    built = [
        build_index(),
        build_greeting(),
        build_organization(),
        build_history(),
        build_certification(),
        build_facility(),
        build_location(),
        build_products(),
        build_drawings(),
        build_quality(),
        build_environment(),
        build_qna(),
        build_notice(),
        build_404(),
    ]
    print(f"{len(built)}개 페이지 생성 완료")
    for b in built:
        print("  -", b)


if __name__ == "__main__":
    main()
