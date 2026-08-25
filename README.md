# 삼각비의 활용 — 삼각측량에서 GPS, 그리고 구면좌표계

중학교 3학년 수학 `삼각비의 활용` 단원 수업용 웹앱입니다.

## 담긴 것
- 그림 4장(삼각측량 원리 / 삼각측량망 / GPS 삼변측량 / 위성 4개의 이유)
- 수업 대본을 따라 읽으며 채우는 빈칸 문항 총 8개 구역
- 구면좌표계 Web VPython 시뮬레이션 코드 (복사 버튼, 파일 저장 버튼)
- 입력 자동 저장(localStorage), 진행률 표시, 인쇄/PDF 저장

## GitHub Pages 배포 방법
1. GitHub 에서 새 저장소(repository)를 만듭니다. 예: `trig-gps-lesson`
2. `index.html` 파일을 저장소 최상위에 업로드합니다.
3. 저장소 상단 `Settings` → 왼쪽 메뉴 `Pages` 로 들어갑니다.
4. `Source` 를 `Deploy from a branch`, `Branch` 를 `main` / `(root)` 로 지정하고 `Save`.
5. 1~2분 뒤 `https://<사용자이름>.github.io/<저장소이름>/` 주소로 접속됩니다.

## 그림을 저장소에 함께 올리고 싶다면
현재 `index.html` 은 그림을 외부 주소에서 불러옵니다. 저장소에 함께 두려면
1. 저장소에 `images` 폴더를 만들고 그림 4장을 `fig1.png` ~ `fig4.png` 로 올립니다.
2. `index.html` 안의 `var IMAGES = { ... }` 부분을 아래처럼 바꿉니다.

```js
var IMAGES = {
  fig1: "images/fig1.png",
  fig2: "images/fig2.png",
  fig3: "images/fig3.png",
  fig4: "images/fig4.png"
};
```

## Web VPython 실행
`spherical_coords_webvpython.py` 의 내용을 https://www.glowscript.org 편집창에
붙여넣고 Run 을 누릅니다. 맨 윗줄 `Web VPython 3.2` 를 반드시 포함해야 합니다.

- 지구 텍스처의 경도가 어긋나 보이면 코드 상단 `TEX_LON_OFFSET` 값(도 단위)을 조절합니다.
- 텍스처 없이 격자만 보려면 `USE_TEXTURE = False` 로 바꿉니다.
