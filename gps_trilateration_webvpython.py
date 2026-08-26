Web VPython 3.2

# ==============================================================
#  GPS 삼변측량 시뮬레이션 - 우주에서 보기
#  중학교 3학년 <삼각비의 활용>  04. GPS 는 각도가 아니라 거리를 잰다
#
#  [실행 방법]
#   1) https://trinket.io/glowscript  (로그인 없이 바로 실행)
#      또는 https://www.glowscript.org  접속 -> 로그인 -> Create New Program
#   2) 이 코드를 통째로 붙여넣기  (맨 윗줄 "Web VPython 3.2" 반드시 포함)
#   3) 오른쪽 위 Run 버튼 클릭
#
#  [조작 방법]
#   - 마우스 왼쪽 드래그 : 시점 회전  /  휠 : 확대, 축소
#   - 아래 버튼 : 위성을 1개 -> 2개 -> 3개 -> 4개 로 늘려 가며 관찰
# ==============================================================


# ---------- 0. 수업 중 바꿔 볼 수 있는 상수 ----------
RE_KM = 6371.0           # 지구 반지름 (km)
RE    = 2.0              # 화면에서의 지구 반지름
KM    = RE_KM / RE       # 화면 1 단위가 몇 km 인가
ORB   = 4.17 * RE        # GPS 궤도 반지름 (지구 중심에서 약 26,560 km)
INC   = 55.0             # 궤도 경사각 (실제 GPS 위성과 같은 값)
WSPD  = 0.5              # 위성이 궤도를 도는 빠르기 (도/초)

USE_TEXTURE = True       # False 로 두면 텍스처 없이 파란 지구
TEX_LON_OFFSET = 90       # 지구 텍스처의 경도가 어긋나 보이면 이 값(도)을 조절

C_SAT = [vec(1.00, 0.85, 0.20), vec(1.00, 0.55, 0.15), vec(0.95, 0.40, 0.80), vec(0.35, 0.85, 1.00)]


# ---------- 1. 무대 설정 ----------
u1 = "<b style='font-size:20px'>GPS 는 각도가 아니라 거리를 잰다</b><br>"
u2 = "위성이 하나씩 늘어날 때마다 내 위치의 후보가 어떻게 줄어드는지 관찰해 보자.<br>"
u3 = "<span style='color:#888'>왼쪽 드래그 : 시점 회전 &nbsp;|&nbsp; 휠 : 확대 축소</span><br>"
scene.title = u1 + u2 + u3

scene.width = 880
scene.height = 600
scene.background = vec(0.04, 0.05, 0.10)
scene.up = vec(0, 0, 1)                  # z축이 화면 위쪽 (북극이 위)
scene.forward = vec(-0.85, -1.0, -0.42)
scene.range = 10.5
scene.ambient = color.gray(0.45)


# ---------- 2. 지구 (지구 사진을 입힌다) ----------
if USE_TEXTURE:
    earth = sphere(pos=vec(0,0,0), radius=RE, texture=textures.earth, shininess=0.05)
else:
    earth = sphere(pos=vec(0,0,0), radius=RE, color=vec(0.12,0.40,0.85), shininess=0.05)

# 지구 그림은 원래 북극이 +y 를 향한다. x축 둘레로 90도 돌려 북극을 +z 로 세운다.
earth.rotate(angle=pi/2, axis=vec(1,0,0))
if TEX_LON_OFFSET != 0:
    earth.rotate(angle=radians(TEX_LON_OFFSET), axis=vec(0,0,1))


# ---------- 3. 지표면 위의 한 점 : 내 스마트폰 ----------
def on_globe(lat_deg, lon_deg, r):
    # 위도, 경도를 구면좌표로 바꾼다.  여기에 삼각비가 그대로 쓰인다.
    t = radians(90.0 - lat_deg)
    p = radians(lon_deg)
    return vec(r*sin(t)*cos(p), r*sin(t)*sin(p), r*cos(t))

RX = on_globe(37.6, 127.0, RE)          # 서울
receiver = sphere(pos=RX, radius=RE*0.055, color=color.red, emissive=True)
lab_rx = label(pos=RX*1.45, text="내 스마트폰 (서울)", color=color.red, height=13, box=False, opacity=0, line=False)


# ---------- 4. 인공위성 4개 ----------
RAAN  = [100.0, 0.0, 160.0, 310.0]     # 궤도면이 놓인 방향
PHASE = [40.0, 70.0, -10.0, -180.0]    # 궤도 위에서의 출발 위치

def sat_pos(i, f_deg):
    o = radians(RAAN[i])
    f = radians(f_deg)
    u = vec(cos(o), sin(o), 0)
    w = vec(-sin(o)*cos(radians(INC)), cos(o)*cos(radians(INC)), sin(radians(INC)))
    return ORB*(cos(f)*u + sin(f)*w)

sats  = []
balls = []
labs  = []
rays  = []
i = 0
while i < 4:
    p = sat_pos(i, PHASE[i])
    s = sphere(pos=p, radius=RE*0.10, color=C_SAT[i], emissive=True)
    b = sphere(pos=p, radius=mag(p - RX), color=C_SAT[i], opacity=0.09, shininess=0)
    lb = label(pos=p, text="위성 " + str(i+1), color=C_SAT[i], height=12, box=False, opacity=0, line=False, yoffset=18)
    ry = curve(color=C_SAT[i], radius=RE*0.008)
    ry.append(p)
    ry.append(RX)
    sats.append(s)
    balls.append(b)
    labs.append(lb)
    rays.append(ry)
    i = i + 1


# ---------- 5. 두 구가 만나서 생기는 원 ----------
ring_12 = ring(pos=vec(0,0,0), axis=vec(0,0,1), radius=1, thickness=RE*0.012, color=color.white, opacity=0.9)

def update_ring(i1, i2):
    d = sats[i2].pos - sats[i1].pos
    dm = mag(d)
    r1 = mag(sats[i1].pos - RX)
    r2 = mag(sats[i2].pos - RX)
    a = (r1*r1 - r2*r2 + dm*dm) / (2*dm)
    h2 = r1*r1 - a*a
    if h2 < 0:
        h2 = 0
    ring_12.pos = sats[i1].pos + (a/dm)*d
    ring_12.axis = norm(d)
    ring_12.radius = sqrt(h2)


# ---------- 6. 세 구가 만나는 두 점 ----------
cand_a = sphere(radius=RE*0.06, color=color.white, emissive=True)
cand_b = sphere(radius=RE*0.06, color=color.white, emissive=True)
lab_a = label(text="후보 1", color=color.white, height=12, box=False, opacity=0, line=False, yoffset=16)
lab_b = label(text="후보 2", color=color.white, height=12, box=False, opacity=0, line=False, yoffset=16)

def trilaterate():
    # 구 3개가 만나는 점 2개를 구한다.
    P1 = sats[0].pos
    P2 = sats[1].pos
    P3 = sats[2].pos
    r1 = mag(P1 - RX)
    r2 = mag(P2 - RX)
    r3 = mag(P3 - RX)
    ex = norm(P2 - P1)
    ii = dot(ex, P3 - P1)
    tv = P3 - P1 - ii*ex
    ey = norm(tv)
    ez = cross(ex, ey)
    dd = mag(P2 - P1)
    jj = dot(ey, P3 - P1)
    x = (r1*r1 - r2*r2 + dd*dd) / (2*dd)
    y = (r1*r1 - r3*r3 + ii*ii + jj*jj) / (2*jj) - (ii/jj)*x
    zz = r1*r1 - x*x - y*y
    if zz < 0:
        zz = 0
    z = sqrt(zz)
    base = P1 + x*ex + y*ey
    return [base + z*ez, base - z*ez]


# ---------- 7. 숫자 표시용 도우미 ----------
def fx(v, n):
    m = 1.0
    i = 0
    while i < n:
        m = m * 10.0
        i = i + 1
    return str(round(v*m)/m)

def f0(v):
    return str(round(v))


# ---------- 8. 화면 갱신 ----------
nvis = 1

def redraw():
    i = 0
    while i < 4:
        on = (i < nvis)
        sats[i].visible = on
        labs[i].visible = on
        rays[i].visible = on
        balls[i].visible = on
        if on:
            p = sats[i].pos
            labs[i].pos = p
            balls[i].pos = p
            balls[i].radius = mag(p - RX)
            rays[i].modify(0, pos=p)
            rays[i].modify(1, pos=RX)
        i = i + 1

    ring_12.visible = (nvis == 2)
    if nvis == 2:
        update_ring(0, 1)

    show_cand = (nvis >= 3)
    cand_a.visible = show_cand
    cand_b.visible = show_cand
    lab_a.visible = (nvis == 3)
    lab_b.visible = (nvis == 3)
    if show_cand:
        cc = trilaterate()
        cand_a.pos = cc[0]
        cand_b.pos = cc[1]
        lab_a.pos = cc[0]
        lab_b.pos = cc[1]

    s = "<div style='font-size:15px;line-height:1.8'>"
    i = 0
    while i < nvis:
        d = mag(sats[i].pos - RX) * KM
        s = s + "위성 " + str(i+1) + " 까지의 거리 = <b>" + f0(d) + " km</b> &nbsp; "
        s = s + "<span style='color:#888'>( 전파가 날아온 시간 " + fx(d/300000.0, 4) + " 초 × 초속 30만 km )</span><br>"
        i = i + 1

    if nvis == 1:
        s = s + "<b style='color:#e6a800'>후보는 무수히 많다.</b> 위성 하나를 중심으로 하는 <b>구 위</b> 어디든 될 수 있다.<br>"
    elif nvis == 2:
        s = s + "<b style='color:#e6a800'>후보가 원 하나로 줄었다.</b> 두 구가 만나서 생긴 <b>흰 원</b> 위에 내가 있다.<br>"
    elif nvis == 3:
        s = s + "<b style='color:#e6a800'>후보가 2개로 줄었다.</b> 두 후보 중 하나는 지구 표면이 아니므로 버린다.<br>"
    else:
        s = s + "<b style='color:#39d353'>위치가 확정되었다.</b> 네 번째 위성은 스마트폰 시계의 오차까지 함께 잡아 준다.<br>"
    s = s + "</div>"
    info.text = s


# ---------- 9. 조작 위젯 ----------
# 줄바꿈은 역슬래시 n 대신 HTML 태그 <br> 을 쓴다. (붙여넣기 사고를 막기 위해)
scene.append_to_caption("<br>")

def set_n(n):
    global nvis
    nvis = n
    redraw()

def b1(b):
    set_n(1)

def b2(b):
    set_n(2)

def b3(b):
    set_n(3)

def b4(b):
    set_n(4)

button(text=" 위성 1개 ", bind=b1)
scene.append_to_caption(" ")
button(text=" 위성 2개 ", bind=b2)
scene.append_to_caption(" ")
button(text=" 위성 3개 ", bind=b3)
scene.append_to_caption(" ")
button(text=" 위성 4개 ", bind=b4)
scene.append_to_caption(" &nbsp;&nbsp; ")

run = True

def b_run(b):
    global run
    run = not run
    if run:
        b.text = " 일시 정지 "
    else:
        b.text = " 다시 움직이기 "

button(text=" 일시 정지 ", bind=b_run)

scene.append_to_caption("<br><br>")
info = wtext(text="")
scene.append_to_caption("<br>")


# ---------- 10. 실행 ----------
tsec = 0.0
redraw()

while True:
    rate(60)
    if run:
        tsec = tsec + 1.0/60.0
        i = 0
        while i < 4:
            sats[i].pos = sat_pos(i, PHASE[i] + WSPD*tsec)
            i = i + 1
        redraw()
