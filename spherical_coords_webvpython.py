Web VPython 3.2
# ===========================================================
#  [자료 A] 구면좌표계 - 지구 위의 한 점을 각 2개로 나타내기
#  중학교 3학년 <삼각비의 활용> 수업용
#  -----------------------------------------------------------
#   * 북극이 +z 축(화면 위쪽)에 오도록 맞추었습니다.
#   * theta(천정각) : 북극에서 잰 각        0도 ~ 180도
#   * phi(방위각)   : 본초자오선에서 동쪽   0도 ~ 360도
#   * 위도 = 90 - theta ,  경도 = phi
# ===========================================================

R_KM = 6371.0     # 실제 지구 반지름(km)
Rd   = 6.0        # 화면에 그릴 반지름

USE_TEXTURE    = True   # False 로 두면 지구 그림 없이 격자만 표시
TEX_LON_OFFSET = 0      # 지구 그림 경도 보정(도) - 아래 슬라이더로도 조절

scene = canvas(title='', width=900, height=540,
               background=color.gray(0.06),
               center=vec(0, 0, 0), range=9.8)
scene.up      = vec(0, 0, 1)
scene.forward = vec(-0.72, -0.46, -0.50)

def rad(d):
    return d * pi / 180.0

def fmt(x, n):
    m = 10 ** n
    return str(round(x * m) / m)

# -----------------------------------------------------------
# 1. 지구  (북극을 +z 축으로 세운다)
# -----------------------------------------------------------
if USE_TEXTURE:
    earth = sphere(pos=vec(0,0,0), radius=Rd, texture=textures.earth,
                   opacity=0.62, shininess=0)
else:
    earth = sphere(pos=vec(0,0,0), radius=Rd, color=vec(0.12,0.36,0.78),
                   opacity=0.50, shininess=0)

# 지구 그림(텍스처)의 북극은 원래 +y 축에 놓인다.
# x축을 중심으로 90도 돌려서 북극을 +z 축으로 옮긴다.  <-- 핵심 한 줄
earth.rotate(angle=pi/2, axis=vec(1,0,0), origin=vec(0,0,0))

tex_now = 0.0
if TEX_LON_OFFSET != 0:
    earth.rotate(angle=rad(TEX_LON_OFFSET), axis=vec(0,0,1), origin=vec(0,0,0))
    tex_now = TEX_LON_OFFSET

# -----------------------------------------------------------
# 2. 좌표축
# -----------------------------------------------------------
L = Rd * 1.5
ac = color.gray(0.75)
arrow(pos=vec(0,0,0), axis=vec(L,0,0), shaftwidth=0.05, color=ac)
arrow(pos=vec(0,0,0), axis=vec(0,L,0), shaftwidth=0.05, color=ac)
arrow(pos=vec(0,0,0), axis=vec(0,0,L), shaftwidth=0.05, color=ac)
label(pos=vec(L+0.4,0,0), text='x', color=ac, box=False, opacity=0, height=16)
label(pos=vec(0,L+0.4,0), text='y', color=ac, box=False, opacity=0, height=16)
label(pos=vec(0,0,L+0.5), text='z (북극)', color=ac, box=False, opacity=0, height=16)

# -----------------------------------------------------------
# 3. 위도선 / 경도선
# -----------------------------------------------------------
def latitude_line(lat_deg, col, rr, op):
    th = rad(90.0 - lat_deg)
    c = curve(color=col, radius=rr, opacity=op)
    k = 0
    while k <= 72:
        ph = rad(k * 5.0)
        c.append(vec(Rd*sin(th)*cos(ph), Rd*sin(th)*sin(ph), Rd*cos(th)))
        k = k + 1

def longitude_line(lon_deg, col, rr, op):
    ph = rad(lon_deg)
    c = curve(color=col, radius=rr, opacity=op)
    k = 0
    while k <= 36:
        th = rad(k * 5.0)
        c.append(vec(Rd*sin(th)*cos(ph), Rd*sin(th)*sin(ph), Rd*cos(th)))
        k = k + 1

gc = color.gray(0.6)
lat = -60
while lat <= 60:
    if lat != 0:
        latitude_line(lat, gc, 0.012, 0.45)
    lat = lat + 30

lon = 30
while lon < 360:
    longitude_line(lon, gc, 0.012, 0.45)
    lon = lon + 30

latitude_line(0, color.yellow, 0.03, 0.9)      # 적도
longitude_line(0, color.orange, 0.03, 0.9)     # 본초자오선

# -----------------------------------------------------------
# 4. 도시 표시 (지구 그림이 잘 맞았는지 눈으로 확인)
# -----------------------------------------------------------
def surface_pos(lat_deg, lon_deg, scale):
    th = rad(90.0 - lat_deg)
    ph = rad(lon_deg)
    return vec(Rd*scale*sin(th)*cos(ph), Rd*scale*sin(th)*sin(ph), Rd*scale*cos(th))

city_name = ['서울', '시드니', '그리니치', '뉴욕']
city_lat  = [37.57, -33.87, 51.48, 40.71]
city_lon  = [126.98, 151.21, 0.0, -74.01]

i = 0
while i < len(city_name):
    sphere(pos=surface_pos(city_lat[i], city_lon[i], 1.0), radius=0.11,
           color=color.white, emissive=True)
    label(pos=surface_pos(city_lat[i], city_lon[i], 1.10), text=city_name[i],
          color=color.white, box=False, opacity=0, height=12)
    i = i + 1

# -----------------------------------------------------------
# 5. 점 P 와 보조선 / 각의 호
# -----------------------------------------------------------
Pc  = color.red
Pt  = sphere(pos=vec(Rd,0,0), radius=0.17, color=Pc, emissive=True)
OP  = cylinder(pos=vec(0,0,0), axis=vec(Rd,0,0), radius=0.04, color=Pc)
Pp  = sphere(pos=vec(Rd,0,0), radius=0.10, color=color.white, emissive=True)
cOP = curve(color=color.white, radius=0.025)     # O  -> P'
cPP = curve(color=color.white, radius=0.025)     # P' -> P
lbP  = label(pos=vec(Rd,0,0), text='P', color=Pc, box=False, opacity=0,
             height=17, xoffset=15, yoffset=15)
lbPp = label(pos=vec(Rd,0,0), text="P'", color=color.white, box=False, opacity=0,
             height=14, xoffset=12, yoffset=-15)

arcT = curve(color=color.cyan,  radius=0.055)
arcP = curve(color=color.green, radius=0.055)
lbT  = label(text='θ', color=color.cyan,  box=False, opacity=0, height=18)
lbF  = label(text='φ', color=color.green, box=False, opacity=0, height=18)

# -----------------------------------------------------------
# 6. 갱신 함수
# -----------------------------------------------------------
spin = False

def update(w=None):
    th = rad(sl_th.value)
    ph = rad(sl_ph.value)
    st = sin(th)
    ct = cos(th)
    sp = sin(ph)
    cp = cos(ph)

    P     = vec(Rd*st*cp, Rd*st*sp, Rd*ct)
    Pfoot = vec(P.x, P.y, 0)

    Pt.pos  = P
    OP.axis = P
    Pp.pos  = Pfoot
    lbP.pos  = P
    lbPp.pos = Pfoot

    cOP.clear()
    cOP.append(vec(0,0,0))
    cOP.append(Pfoot)
    cPP.clear()
    cPP.append(Pfoot)
    cPP.append(P)

    # 천정각 호 (z축 -> OP)
    rT = Rd * 0.55
    arcT.clear()
    k = 0
    n = 40
    while k <= n:
        a = th * k / n
        arcT.append(vec(rT*sin(a)*cp, rT*sin(a)*sp, rT*cos(a)))
        k = k + 1
    am = th * 0.55
    lbT.pos = vec(rT*1.16*sin(am)*cp, rT*1.16*sin(am)*sp, rT*1.16*cos(am))

    # 방위각 호 (x축 -> OP')
    rP = Rd * 0.80
    arcP.clear()
    k = 0
    while k <= n:
        a = ph * k / n
        arcP.append(vec(rP*cos(a), rP*sin(a), 0))
        k = k + 1
    am2 = ph * 0.5
    lbF.pos = vec(rP*1.14*cos(am2), rP*1.14*sin(am2), 0)

    # 숫자판
    lat_v = 90.0 - sl_th.value
    lon_v = sl_ph.value
    if lon_v > 180:
        lon_v = lon_v - 360.0
    ns = '북위 '
    if lat_v < 0:
        ns = '남위 '
    ew = '동경 '
    if lon_v < 0:
        ew = '서경 '

    wt_th.text = fmt(sl_th.value, 1)
    wt_ph.text = fmt(sl_ph.value, 1)
    wt_tex.text = fmt(sl_tex.value, 0)

    s1 = '  구면좌표  :  R = 6371 km ,  θ = ' + fmt(sl_th.value,1) + '° ,  φ = ' + fmt(sl_ph.value,1) + '°'
    s2 = '  직교좌표  :  x = ' + fmt(R_KM*st*cp,0) + ' km ,  y = ' + fmt(R_KM*st*sp,0) + ' km ,  z = ' + fmt(R_KM*ct,0) + ' km'
    s3 = '  지도 표기  :  ' + ns + fmt(abs(lat_v),1) + '° ,  ' + ew + fmt(abs(lon_v),1) + '°'
    out.text = '\n' + s1 + '\n' + s2 + '\n' + s3 + '\n'

def fix_tex(s):
    global tex_now
    d = s.value - tex_now
    earth.rotate(angle=rad(d), axis=vec(0,0,1), origin=vec(0,0,0))
    tex_now = s.value
    update()

def go(th_v, ph_v):
    sl_th.value = th_v
    sl_ph.value = ph_v
    update()

def go_seoul(b):
    go(90.0-37.57, 126.98)

def go_sydney(b):
    go(90.0+33.87, 151.21)

def go_zero(b):
    go(90.0, 0.0)

def go_pole(b):
    go(0.0, 0.0)

def set_spin(c):
    global spin
    spin = c.checked

# -----------------------------------------------------------
# 7. 조작판
# -----------------------------------------------------------
scene.append_to_caption('\n')
sl_th = slider(min=0, max=180, value=90.0-37.57, step=0.1, length=380, bind=update)
scene.append_to_caption('  천정각 θ = ')
wt_th = wtext(text='')
scene.append_to_caption('°   (북극 0° · 적도 90° · 남극 180°)\n\n')

sl_ph = slider(min=0, max=360, value=126.98, step=0.1, length=380, bind=update)
scene.append_to_caption('  방위각 φ = ')
wt_ph = wtext(text='')
scene.append_to_caption('°   (본초자오선에서 동쪽으로 잰 각)\n\n')

sl_tex = slider(min=-180, max=180, value=TEX_LON_OFFSET, step=1, length=250, bind=fix_tex)
scene.append_to_caption('  지구 그림 경도 맞추기 = ')
wt_tex = wtext(text='')
scene.append_to_caption('°   (도시 표시와 어긋나면 이 값을 조절)\n\n')

scene.append_to_caption('  ')
button(text=' 서울 ', bind=go_seoul)
scene.append_to_caption(' ')
button(text=' 시드니 ', bind=go_sydney)
scene.append_to_caption(' ')
button(text=' 적도 · 본초자오선 ', bind=go_zero)
scene.append_to_caption(' ')
button(text=' 북극 ', bind=go_pole)
scene.append_to_caption('    ')
cb_spin = checkbox(text=' 자전 (φ 만 증가)', checked=False, bind=set_spin)
scene.append_to_caption('\n')

out = wtext(text='')
update()

# -----------------------------------------------------------
# 8. 실행 루프
# -----------------------------------------------------------
while True:
    rate(60)
    if spin:
        v = sl_ph.value + 0.5
        if v >= 360:
            v = v - 360
        sl_ph.value = v
        update()
