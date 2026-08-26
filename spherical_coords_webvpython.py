Web VPython 3.2

# ==============================================================
#  구면좌표계(Spherical Coordinates) 시뮬레이션
#  중학교 3학년 <삼각비의 활용> 확장 활동 - 지구 위의 한 점 P
#
#  [실행 방법]
#   1) https://trinket.io/glowscript  (로그인 없이 바로 실행)
#      또는 https://www.glowscript.org  접속 -> 로그인 -> Create New Program
#   2) 이 코드를 통째로 붙여넣기  (맨 윗줄 "Web VPython 3.2" 반드시 포함)
#   3) 오른쪽 위 Run 버튼 클릭
#
#  [조작 방법]
#   - 마우스 왼쪽 드래그 : 지구를 이리저리 굴려 보기
#   - 마우스 휠 / 오른쪽 드래그 : 확대, 축소
#   - 아래 슬라이더 두 개 : 천정각 θ, 방위각 φ 를 직접 바꿔 보기
# ==============================================================


# ---------- 0. 수업 중 바꿔 볼 수 있는 상수 ----------
R = 6371.0              # 지구 반지름 (km)
USE_TEXTURE = True      # False 로 두면 텍스처 없이 파란 반투명 지구
EARTH_OPACITY = 0.62    # 1.0 에 가까울수록 불투명 (내부 보조선이 덜 보임)
TEX_LON_OFFSET = 90      # 지구 텍스처의 경도가 어긋나 보이면 이 값(도)을 조절

C_AXIS = vec(0.30, 0.30, 0.36)   # 좌표축
C_P    = vec(0.86, 0.12, 0.12)   # 점 P, 동경 OP
C_TH   = vec(0.10, 0.35, 0.90)   # 천정각 theta
C_PH   = vec(0.00, 0.58, 0.28)   # 방위각 phi
C_AUX  = vec(0.45, 0.45, 0.52)   # 보조선


# ---------- 1. 무대 설정 ----------
t1 = "<b style='font-size:20px'>구면좌표계로 지구 위의 한 점 나타내기</b><br>"
t2 = "직교좌표 (x, y, z) 는 숫자가 3개, 구면좌표 (R, &theta;, &phi;) 는 실제로 2개면 충분하다.<br>"
t3 = "<span style='color:#666'>왼쪽 드래그 : 지구 회전 &nbsp;|&nbsp; 휠 : 확대 축소</span><br>"
scene.title = t1 + t2 + t3

scene.width = 860
scene.height = 560
scene.background = vec(0.97, 0.97, 0.98)
scene.up = vec(0, 0, 1)                  # z축이 화면 위쪽 (북극이 위)
scene.forward = vec(-0.85, -1.0, -0.45)
scene.range = 1.8 * R
scene.ambient = color.gray(0.5)


# ---------- 2. 지구 ----------
if USE_TEXTURE:
    earth = sphere(pos=vec(0,0,0), radius=R, texture=textures.earth,
                   opacity=EARTH_OPACITY, shininess=0.05)
else:
    earth = sphere(pos=vec(0,0,0), radius=R, color=vec(0.22,0.47,0.78),
                   opacity=EARTH_OPACITY, shininess=0.05)

# 지구 그림은 원래 북극이 +y 를 향한다.
# x축 둘레로 90도 돌려서 북극을 +z 축으로 세운다. (scene.up = z 와 일치)
earth.rotate(angle=pi/2, axis=vec(1,0,0))
if TEX_LON_OFFSET != 0:
    earth.rotate(angle=radians(TEX_LON_OFFSET), axis=vec(0,0,1))


# ---------- 3. 위도, 경도 격자 ----------
GR = R * 1.004

def draw_parallel(lat_deg, col, rad):
    # 위도선 : theta 를 고정하고 phi 를 0~360 으로 돌린다
    t = radians(90.0 - lat_deg)
    c = curve(color=col, radius=rad)
    a = 0
    while a <= 360:
        p = radians(a)
        c.append(vec(GR*sin(t)*cos(p), GR*sin(t)*sin(p), GR*cos(t)))
        a = a + 3
    return c

def draw_meridian(lon_deg, col, rad):
    # 경도선 : phi 를 고정하고 theta 를 0~180 으로 돌린다
    p = radians(lon_deg)
    c = curve(color=col, radius=rad)
    a = 0
    while a <= 180:
        t = radians(a)
        c.append(vec(GR*sin(t)*cos(p), GR*sin(t)*sin(p), GR*cos(t)))
        a = a + 3
    return c

for lat_d in [-60, -30, 30, 60]:
    draw_parallel(lat_d, color.gray(0.55), R*0.0025)

for lon_d in [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
    draw_meridian(lon_d, color.gray(0.55), R*0.0025)

draw_parallel(0, vec(0.15, 0.15, 0.20), R*0.006)    # 적도
draw_meridian(0, vec(0.15, 0.15, 0.20), R*0.006)    # 본초자오선


# ---------- 4. 좌표축 ----------
L = 1.5 * R
arrow(pos=vec(0,0,0), axis=vec(L,0,0), shaftwidth=R*0.016, color=C_AXIS)
arrow(pos=vec(0,0,0), axis=vec(0,L,0), shaftwidth=R*0.016, color=C_AXIS)
arrow(pos=vec(0,0,0), axis=vec(0,0,L), shaftwidth=R*0.016, color=C_AXIS)

label(pos=vec(L*1.10, 0, 0), text="x", height=19, box=False, opacity=0, color=C_AXIS)
label(pos=vec(0, L*1.10, 0), text="y", height=19, box=False, opacity=0, color=C_AXIS)
label(pos=vec(0, 0, L*1.10), text="z", height=19, box=False, opacity=0, color=C_AXIS)


# ---------- 5. 점 P 와 보조 도형 ----------
Pmark  = sphere(radius=R*0.035, color=C_P,   emissive=True)   # 지표면 위의 점 P
Ppmark = sphere(radius=R*0.022, color=C_AUX, emissive=True)   # P 를 xy평면에 내린 점 P'
OP     = arrow(pos=vec(0,0,0), axis=vec(R,0,0), shaftwidth=R*0.012, color=C_P)

def new_dash(col, n):
    # 점선을 흉내내기 위해 짧은 선분 n 개를 만들어 둔다
    segs = []
    i = 0
    while i < n:
        segs.append(curve(color=col, radius=R*0.005))
        i = i + 1
    return segs

def set_dash(segs, a, b):
    n = len(segs)
    i = 0
    while i < n:
        t0 = (1.0*i) / n
        t1 = t0 + 0.62 / n
        segs[i].clear()
        segs[i].append(a + (b - a)*t0)
        segs[i].append(a + (b - a)*t1)
        i = i + 1

dash_xy = new_dash(C_AUX, 14)   # O  -> P'
dash_up = new_dash(C_AUX, 10)   # P' -> P

RT = 0.44 * R                   # 천정각 호의 반지름
RP = 0.30 * R                   # 방위각 호의 반지름
arc_th = curve(color=C_TH, radius=R*0.010)
arc_ph = curve(color=C_PH, radius=R*0.010)

lab_P  = label(text="P",  height=20, box=False, opacity=0, color=C_P)
lab_Pp = label(text="P'", height=15, box=False, opacity=0, color=C_AUX)
lab_th = label(text="θ",  height=23, box=False, opacity=0, color=C_TH)
lab_ph = label(text="φ",  height=23, box=False, opacity=0, color=C_PH)


# ---------- 6. 숫자 표시용 도우미 ----------
def f0(v):
    return "{:.0f}".format(v)

def f1(v):
    return "{:.1f}".format(v)

def f3(v):
    return "{:.3f}".format(v)


# ---------- 7. 화면 갱신 : 여기가 이 수업의 핵심 ----------
def update(w=None):
    th = radians(sl_th.value)      # 천정각 theta
    ph = radians(sl_ph.value)      # 방위각 phi

    st = sin(th)
    ct = cos(th)
    sp = sin(ph)
    cp = cos(ph)

    # ***** 삼각비가 그대로 등장하는 좌표 변환식 *****
    P  = vec(R*st*cp, R*st*sp, R*ct)
    Pp = vec(P.x, P.y, 0)

    Pmark.pos  = P
    Ppmark.pos = Pp
    OP.axis    = P
    lab_P.pos  = P * 1.12
    lab_Pp.pos = Pp * 1.12 + vec(0, 0, R*0.05)

    set_dash(dash_xy, vec(0,0,0), Pp)
    set_dash(dash_up, Pp, P)

    # 천정각 호 : +z 방향에서 OP 방향까지
    zhat = vec(0, 0, 1)
    u = P - zhat*dot(P, zhat)
    if mag(u) < R*0.000001:
        u = vec(1, 0, 0)
    u = norm(u)

    arc_th.clear()
    i = 0
    while i <= 48:
        t = th * (1.0*i) / 48.0
        arc_th.append(RT*(cos(t)*zhat + sin(t)*u))
        i = i + 1
    lab_th.pos = RT*1.24*(cos(th*0.5)*zhat + sin(th*0.5)*u)

    # 방위각 호 : xy평면 위에서 +x 방향부터 OP' 방향까지
    arc_ph.clear()
    i = 0
    while i <= 48:
        a = ph * (1.0*i) / 48.0
        arc_ph.append(vec(RP*cos(a), RP*sin(a), 0))
        i = i + 1
    lab_ph.pos = vec(RP*1.28*cos(ph*0.5), RP*1.28*sin(ph*0.5), R*0.04)

    # ----- 아래쪽 숫자판 -----
    dt = sl_th.value
    dp = sl_ph.value
    wt_th.text = " &nbsp; θ = " + f1(dt) + "°"
    wt_ph.text = " &nbsp; φ = " + f1(dp) + "°"

    lat = 90.0 - dt
    lon = dp
    if lon > 180.0:
        lon = lon - 360.0

    if lat >= 0:
        lat_s = "북위 " + f1(lat) + "°"
    else:
        lat_s = "남위 " + f1(-lat) + "°"

    if lon >= 0:
        lon_s = "동경 " + f1(lon) + "°"
    else:
        lon_s = "서경 " + f1(-lon) + "°"

    s = "<div style='font-size:15px;line-height:1.8'>"
    s = s + "<b>1. 직교좌표 (x, y, z)</b> = ( " + f0(P.x) + ", " + f0(P.y) + ", " + f0(P.z) + " ) km"
    s = s + " &nbsp;&rarr; 외워야 할 숫자 <b>3개</b>, 게다가 전부 지저분한 수<br>"
    s = s + "<b>2. 구면좌표 (R, θ, φ)</b> = ( 6371, " + f1(dt) + "°, " + f1(dp) + "° )"
    s = s + " &nbsp;&rarr; 지표면이면 R은 <b>항상 6371</b>, 실제로 필요한 값은 <b>2개</b><br>"
    s = s + "<b>3. 위도 · 경도</b> = " + lat_s + " , " + lon_s
    s = s + " &nbsp; <span style='color:#666'>(위도 = 90° − θ,&nbsp; 경도 = φ)</span>"
    s = s + "<hr style='border:none;border-top:1px solid #c8c8c8;margin:8px 0'>"
    s = s + "<b style='color:#b01919'>1번과 2번을 이어 주는 다리가 바로 삼각비다.</b><br>"
    s = s + "x = R · sinθ · cosφ = 6371 × " + f3(st) + " × " + f3(cp) + " = " + f0(P.x) + " km<br>"
    s = s + "y = R · sinθ · sinφ = 6371 × " + f3(st) + " × " + f3(sp) + " = " + f0(P.y) + " km<br>"
    s = s + "z = R · cosθ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 6371 × " + f3(ct) + " = " + f0(P.z) + " km"
    s = s + "</div>"
    info.text = s


# ---------- 8. 조작 위젯 ----------
# 줄바꿈은 역슬래시 n 대신 HTML 태그 <br> 을 쓴다. (붙여넣기 사고를 막기 위해)
scene.append_to_caption("<br>")
scene.append_to_caption("<b style='color:#1a5ae6'>천정각 θ</b> &nbsp;(z축, 즉 북극 방향에서부터 잰 각) &nbsp;")
sl_th = slider(min=0, max=180, value=52.4, step=0.1, length=330, bind=update)
wt_th = wtext(text="")

scene.append_to_caption("<br><br>")
scene.append_to_caption("<b style='color:#009447'>방위각 φ</b> &nbsp;(x축, 즉 본초자오선에서부터 잰 각) &nbsp;")
sl_ph = slider(min=0, max=360, value=127.0, step=0.1, length=330, bind=update)
wt_ph = wtext(text="")

scene.append_to_caption("<br><br>")

def goto(t, p):
    sl_th.value = t
    sl_ph.value = p
    update()

def b_seoul(b):
    goto(52.4, 127.0)      # 서울   : 북위 37.6도

def b_sydney(b):
    goto(123.9, 151.2)     # 시드니 : 남위 33.9도

def b_equator(b):
    goto(90.0, 0.0)        # 적도와 본초자오선이 만나는 곳

def b_pole(b):
    goto(0.0, 0.0)         # 북극

button(text=" 서울 ", bind=b_seoul)
scene.append_to_caption(" ")
button(text=" 시드니 ", bind=b_sydney)
scene.append_to_caption(" ")
button(text=" 적도 · 본초자오선 ", bind=b_equator)
scene.append_to_caption(" ")
button(text=" 북극 ", bind=b_pole)
scene.append_to_caption(" &nbsp;&nbsp; ")

spin = False
def b_spin(b):
    global spin
    spin = not spin
    if spin:
        b.text = " 자전 멈춤 "
    else:
        b.text = " 자전 시작 "

button(text=" 자전 시작 ", bind=b_spin)

scene.append_to_caption("<br><br>")
info = wtext(text="")
scene.append_to_caption("<br>")


# ---------- 9. 실행 ----------
update()

while True:
    rate(60)
    if spin:
        v = sl_ph.value + 0.4
        if v >= 360:
            v = v - 360
        sl_ph.value = v
        update()
