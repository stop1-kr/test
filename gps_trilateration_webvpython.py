Web VPython 3.2
# ===========================================================
#  [자료 B] GPS 삼변측량 - 거리 3개로 내 위치를 찾는다
#  중학교 3학년 <삼각비의 활용> 수업용
#  -----------------------------------------------------------
#   위성 1개 -> 후보가 구면 전체 (무수히 많다)
#   위성 2개 -> 후보가 원 하나
#   위성 3개 -> 후보가 점 2개
#   위성 4개 -> 위치 + 시계 오차까지 확정
#   * 아래 버튼으로 위성을 하나씩 늘려 가며 보여 주세요.
# ===========================================================

Re    = 2.4        # 지구 반지름(화면)
Rsat  = 10.0       # 위성 궤도 반지름(화면) - 실제 비율(약 4.2배)에 맞춤
Re_KM = 6371.0     # 실제 지구 반지름(km)

scene = canvas(title='', width=900, height=560,
               background=vec(0.03, 0.03, 0.08),
               center=vec(0,0,0), range=13.0)
scene.up      = vec(0, 0, 1)
scene.forward = vec(-0.70, -0.50, -0.45)

def rad(d):
    return d * pi / 180.0

def fmt(x, n):
    m = 10 ** n
    return str(round(x * m) / m)

def sph_pos(r, lat_deg, lon_deg):
    th = rad(90.0 - lat_deg)
    ph = rad(lon_deg)
    return vec(r*sin(th)*cos(ph), r*sin(th)*sin(ph), r*cos(th))

# -----------------------------------------------------------
# 1. 지구  (지구 그림을 입히고 북극을 +z 축으로)
# -----------------------------------------------------------
earth = sphere(pos=vec(0,0,0), radius=Re, texture=textures.earth,
               shininess=0, opacity=1.0)
earth.rotate(angle=pi/2, axis=vec(1,0,0), origin=vec(0,0,0))   # 북극을 z축으로
TEX_LON_OFFSET = 0
if TEX_LON_OFFSET != 0:
    earth.rotate(angle=rad(TEX_LON_OFFSET), axis=vec(0,0,1), origin=vec(0,0,0))

label(pos=vec(0,0,-Re-0.55), text='지구', color=color.cyan,
      box=False, opacity=0, height=13)

# -----------------------------------------------------------
# 2. 수신기(내 스마트폰) - 지구 표면 위, 서울
# -----------------------------------------------------------
rx_lat = 37.57
rx_lon = 126.98
receiver_pos = sph_pos(Re, rx_lat, rx_lon)
receiver = sphere(pos=receiver_pos, radius=0.16, color=color.red, emissive=True)
lb_rx = label(pos=receiver_pos, text='내 스마트폰', color=color.red,
              box=False, opacity=0, height=13, xoffset=18, yoffset=18)

# -----------------------------------------------------------
# 3. 위성 4개
# -----------------------------------------------------------
sat_lat = [ 62.0,  18.0, 46.0, -12.0]
sat_lon = [100.0, 168.0, 55.0, 122.0]
sat_col = [color.yellow, color.orange, color.magenta, vec(0.4,0.9,1.0)]

N = 4
sat_base = []
sats     = []
shells   = []
links    = []
sat_lbl  = []

i = 0
while i < N:
    p = sph_pos(Rsat, sat_lat[i], sat_lon[i])
    sat_base.append(p)
    s = sphere(pos=p, radius=0.22, color=sat_col[i], emissive=True)
    sats.append(s)
    sat_lbl.append(label(pos=p, text='위성 ' + str(i+1), color=sat_col[i],
                         box=False, opacity=0, height=12, xoffset=14, yoffset=14))
    d = mag(p - receiver_pos)
    shells.append(sphere(pos=p, radius=d, color=sat_col[i],
                         opacity=0.10, shininess=0))
    links.append(curve(pos=[p, receiver_pos], color=sat_col[i],
                       radius=0.018, opacity=0.7))
    i = i + 1

# 위성 2개일 때 생기는 교차원(빨간 링), 3개일 때 남는 후보점 2개
ring12 = ring(pos=vec(0,0,0), axis=vec(0,0,1), radius=1, thickness=0.06,
              color=color.green, opacity=0.9)
cand   = []
cand.append(sphere(pos=vec(0,0,0), radius=0.15, color=color.white, emissive=True))
cand.append(sphere(pos=vec(0,0,0), radius=0.15, color=color.white, emissive=True))
cand_lbl = []
cand_lbl.append(label(text='후보 1', color=color.white, box=False, opacity=0,
                      height=12, xoffset=14, yoffset=-16))
cand_lbl.append(label(text='후보 2', color=color.white, box=False, opacity=0,
                      height=12, xoffset=14, yoffset=-16))

# -----------------------------------------------------------
# 4. 계산 함수
# -----------------------------------------------------------
def two_sphere_ring(p1, r1, p2, r2):
    # 두 구가 만나서 생기는 원의 중심과 반지름을 돌려준다
    dv = p2 - p1
    dm = mag(dv)
    a  = (r1*r1 - r2*r2 + dm*dm) / (2*dm)
    h2 = r1*r1 - a*a
    if h2 < 0:
        h2 = 0
    return [p1 + (a/dm)*dv, sqrt(h2), norm(dv)]

def three_sphere_points(p1, r1, p2, r2, p3, r3):
    # 세 구가 만나는 점 2개를 돌려준다
    ex = norm(p2 - p1)
    ii = dot(ex, p3 - p1)
    tmp = (p3 - p1) - ii*ex
    ey = norm(tmp)
    ez = cross(ex, ey)
    dd = mag(p2 - p1)
    jj = dot(ey, p3 - p1)
    xx = (r1*r1 - r2*r2 + dd*dd) / (2*dd)
    yy = (r1*r1 - r3*r3 + ii*ii + jj*jj) / (2*jj) - (ii/jj)*xx
    z2 = r1*r1 - xx*xx - yy*yy
    if z2 < 0:
        z2 = 0
    zz = sqrt(z2)
    base = p1 + xx*ex + yy*ey
    return [base + zz*ez, base - zz*ez]

# -----------------------------------------------------------
# 5. 화면 갱신
# -----------------------------------------------------------
nshow  = 1        # 지금 보여 주는 위성 수
moving = True
show_shell = True
t = 0.0

msg = ['위성 1개 :  내 위치의 후보는 구면 전체 -> 무수히 많다',
       '위성 2개 :  두 구가 만나 생긴 원 위 -> 아직 무수히 많다',
       '위성 3개 :  후보가 점 2개로 좁혀진다 -> 하나는 지구 밖',
       '위성 4개 :  위치(x, y, z) 와 시계 오차까지 4개를 모두 확정']

def redraw():
    i = 0
    while i < N:
        on = (i < nshow)
        sats[i].visible   = on
        sat_lbl[i].visible = on
        links[i].visible  = on
        shells[i].visible = on and show_shell
        d = mag(sats[i].pos - receiver_pos)
        shells[i].pos    = sats[i].pos
        shells[i].radius = d
        links[i].modify(0, pos=sats[i].pos)
        links[i].modify(1, pos=receiver_pos)
        sat_lbl[i].pos = sats[i].pos
        i = i + 1

    # 위성 2개 : 교차원
    if nshow == 2:
        r1 = mag(sats[0].pos - receiver_pos)
        r2 = mag(sats[1].pos - receiver_pos)
        res = two_sphere_ring(sats[0].pos, r1, sats[1].pos, r2)
        ring12.pos     = res[0]
        ring12.radius  = res[1]
        ring12.axis    = res[2]
        ring12.visible = True
    else:
        ring12.visible = False

    # 위성 3개 : 후보점 2개
    if nshow == 3:
        r1 = mag(sats[0].pos - receiver_pos)
        r2 = mag(sats[1].pos - receiver_pos)
        r3 = mag(sats[2].pos - receiver_pos)
        pts = three_sphere_points(sats[0].pos, r1, sats[1].pos, r2, sats[2].pos, r3)
        k = 0
        while k < 2:
            cand[k].pos = pts[k]
            cand[k].visible = True
            cand_lbl[k].pos = pts[k]
            cand_lbl[k].visible = True
            k = k + 1
    else:
        cand[0].visible = False
        cand[1].visible = False
        cand_lbl[0].visible = False
        cand_lbl[1].visible = False

    receiver.visible = (nshow >= 3)
    lb_rx.visible    = (nshow >= 4)

    txt = '\n  ' + msg[nshow-1] + '\n\n'
    i = 0
    while i < nshow:
        dk = mag(sats[i].pos - receiver_pos) / Re * Re_KM
        txt = txt + '   위성 ' + str(i+1) + ' 까지의 거리 = ' + fmt(dk, 0) + ' km\n'
        i = i + 1
    out.text = txt

def set1(b):
    global nshow
    nshow = 1
    redraw()

def set2(b):
    global nshow
    nshow = 2
    redraw()

def set3(b):
    global nshow
    nshow = 3
    redraw()

def set4(b):
    global nshow
    nshow = 4
    redraw()

def set_move(c):
    global moving
    moving = c.checked

def set_shell(c):
    global show_shell
    show_shell = c.checked
    redraw()

# -----------------------------------------------------------
# 6. 조작판
# -----------------------------------------------------------
scene.append_to_caption('\n  ')
button(text='  위성 1개  ', bind=set1)
scene.append_to_caption(' ')
button(text='  위성 2개  ', bind=set2)
scene.append_to_caption(' ')
button(text='  위성 3개  ', bind=set3)
scene.append_to_caption(' ')
button(text='  위성 4개  ', bind=set4)
scene.append_to_caption('     ')
cb_shell = checkbox(text=' 거리를 나타내는 구 보이기 ', checked=True, bind=set_shell)
scene.append_to_caption('  ')
cb_move = checkbox(text=' 위성 움직이기 ', checked=True, bind=set_move)
scene.append_to_caption('\n')
out = wtext(text='')
redraw()

# -----------------------------------------------------------
# 7. 실행 루프
# -----------------------------------------------------------
while True:
    rate(30)
    if moving:
        t = t + 0.01
        i = 0
        while i < N:
            a = t * 0.6 + i * pi / 2
            base = sat_base[i]
            side = norm(cross(base, vec(0,0,1)))
            up2  = norm(cross(side, base))
            sats[i].pos = base + 0.7*sin(a)*side + 0.7*cos(a)*up2
            i = i + 1
    redraw()
