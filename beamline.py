from contextlib import contextmanager
import math

import config as cfg
import geomhelper as geom
import pshelper as ps

#______________________________________________________________________________
def draw():
  ps.comment('K1.8BR Beam Line')
  draw_d5()
  draw_q8()
  draw_d4()
  draw_q7()
  draw_s3()
  draw_d3()

#______________________________________________________________________________
# D5 geometry extracted directly from CAD DWG (K1.8BRforE72_fordrawing),
# layer "K1.8BR". Yoke arcs around the yoke center, span 68.75 deg:
#   r = 2606.6 (outer yoke), 1866.7 / 1666.7, 1466.7 (aperture band edges),
#   radial faces down to r = 1014, kaname corners at r = 664.
# Orbit model: the orbit crosses the aperture CENTER (r = 1666.7) on both
# yoke faces, with rho = 1898.4 (CAD); its CoC therefore sits on the
# symmetry axis at x_c = -273.1 (derived in draw_d5), NOT at the yoke
# center, so the faces are non-normal to the beam (edge angle ~4.7 deg).
# Particles bend ONLY inside the yoke (face to face): total bend =
# 59.43 deg (not 60 deg). Outside, the beam is straight and crosses the
# straight coil/end-guard apertures slightly off center (+12..+19 mm).
D5_RHO        = 1898.4              # beam orbit radius
D5_YOKE_HALF  = 34.375              # yoke half span; total 68.75 deg
D5_R_OUTER    = 2606.6              # outer yoke arc (around yoke center)
D5_R_INNER    = 1014.0              # radial face inner endpoint (V3, V6)
D5_R_KANAME   = 664.0               # yoke center to kaname corner (V4, V5)
# Coil end and end-guard plate at each face, from CAD. Both are parallel
# to the (radial) yoke face. Coordinates per plate: s = position along the
# face direction measured from the yoke center, d = distance out from the
# face. Mirror-symmetric between entrance and exit.
# (s0, s1, d0, d1)
D5_COIL      = (1096.6, 2236.7,   0.0, 131.0)   # coil end: 1140 x 131,
                                                # flush with the yoke face
D5_END_GUARD = (1006.7, 2326.7, 150.0, 230.0)   # end guard: 1320 x 80
# Pole-gap aperture where the beam passes the yoke: the band between the
# CAD arcs at r=1466.7 and r=1866.7 around the yoke center. Through the
# coils and end guards the aperture is a STRAIGHT slot, perpendicular to
# the yoke face (CAD: line at s=1666.7 normal to the face).
D5_GAP_R0    = 1466.7
D5_GAP_R1    = 1866.7
D5_R_AP      = 1666.7               # aperture center radius
D5_ORBIT_EXT = 400.0                # straight orbit extension past faces

#______________________________________________________________________________
def d5_orbit():
  ''' D5 orbit geometry in the yoke frame: returns (px, py, x_c, phi_e)
  with P+(px, py) = exit-face crossing at the aperture center, x_c = orbit
  CoC on the symmetry axis, phi_e = half bend angle [deg]. '''
  c = math.cos(math.radians(D5_YOKE_HALF))
  s = math.sin(math.radians(D5_YOKE_HALF))
  px, py = D5_R_AP * c, D5_R_AP * s
  x_c    = px - math.sqrt(D5_RHO**2 - py*py)
  phi_e  = math.degrees(math.atan2(py, px - x_c))
  return px, py, x_c, phi_e

def draw_d5():
  ps.comment('K1.8BR D5')
  # Anchor: face crossing P+ at FF z = -1766.0, outgoing tangent -> +y.
  # The outgoing orbit extends all the way to the target (FF z = -293.1).
  ext_target = 1456.615 + 309.4 - 293.1
  x, y = geom.ff_to_d5()
  with ps.transform(x, y, geom.ff_angle):
    draw_bend('D5', 0, ext_target, tag_perp=300, tag_r=480)

def draw_bend(label, tag_angle, ext_out=D5_ORBIT_EXT, tag_perp=0,
              tag_r=300):
  ''' D5-type bending magnet (D4 is its twin), drawn in a frame whose
  origin is the exit-face beam crossing with the outgoing beam tangent
  along +y. tag_angle compensates the caller frame rotation so the label
  text renders upright. '''
  # 6-vertex gingko: outer arc + 2 radial faces + 3-side kaname (keystone)
  # on the CoC side.
  #   V1 -outer arc CCW- V2 -radial- V3 -horizontal neck- V4
  #   -kaname back- V5 -horizontal neck- V6 -radial- V1
  # Vertices in the YOKE frame (yoke center at origin, +x = symmetry axis).
  th_y = D5_YOKE_HALF
  r_o, r_i, r_k = D5_R_OUTER, D5_R_INNER, D5_R_KANAME
  c = math.cos(math.radians(th_y))
  s = math.sin(math.radians(th_y))
  y_neck = r_i * s                  # V3, V4 share this y (horizontal neck)
  x_kan  = math.sqrt(r_k * r_k - y_neck * y_neck)
  V1 = ( r_o * c, -r_o * s)         # outer arc, entrance side
  V6 = ( r_i * c, -r_i * s)         # radial end, entrance side
  V5 = ( x_kan,   -y_neck)          # kaname corner, entrance side
  V4 = ( x_kan,   +y_neck)          # kaname corner, exit side
  V3 = ( r_i * c,  r_i * s)         # radial end, exit side
  V2 = ( r_o * c,  r_o * s)         # outer arc, exit side
  # Orbit through the aperture centers on the yoke faces (yoke frame):
  # CoC on the symmetry axis at x_c; particles bend ONLY between the
  # faces, so the bend ends exactly at the face crossing P+, at angle
  # +/-phi_e from the axis. The outgoing tangent there is NOT normal to
  # the face, so the whole yoke is tilted w.r.t. the beam axis.
  px, py, x_c, phi_e = d5_orbit()
  c_e = math.cos(math.radians(phi_e))
  s_e = math.sin(math.radians(phi_e))
  with ps.transform():
    # Map P+ -> origin and the outgoing tangent -> +y, then draw
    # everything in the yoke frame (yoke center at origin).
    ps.translate_xy(-x_c * c_e - D5_RHO, x_c * s_e)
    ps.rotate(-phi_e)
    ps.newpath()
    ps.move_to_xy(*V1)
    ps.arc(r_o, -th_y, +th_y)       # outer arc CCW V1 -> V2
    ps.line_to_xy(*V3)
    ps.line_to_xy(*V4)
    ps.line_to_xy(*V5)
    ps.line_to_xy(*V6)
    ps.closepath()
    ps.fill(cfg.color_dark_green)
    ps.stroke()
    # Coil ends and end guards: rotate so the face direction becomes +x,
    # then each plate is an axis-aligned box at y = sign * (d0..d1).
    plates = ((D5_COIL, cfg.color_maroon),
              (D5_END_GUARD, cfg.color_dark_green))
    for sign in (1, -1):                  # exit (+) / entrance (-)
      with ps.transform(0, 0, sign * th_y):
        for (s0, s1, d0, d1), color in plates:
          ps.path_box((s0 + s1) / 2, sign * (d0 + d1) / 2,
                      (s1 - s0) / 2, (d1 - d0) / 2)
          ps.fill(color)
          ps.stroke()
    # Pole-gap aperture: curved white band inside the yoke, plus a
    # straight slot (perpendicular to the face) through the coil and end
    # guard at each face.
    g0, g1 = D5_GAP_R0, D5_GAP_R1
    d_out  = D5_END_GUARD[3]
    ps.path_sector(g0, g1, -th_y, +th_y)
    ps.fill(cfg.color_white)
    for sign in (1, -1):                  # exit (+) / entrance (-)
      with ps.transform(0, 0, sign * th_y):
        ps.path_box((g0 + g1) / 2, sign * d_out / 2,
                    (g1 - g0) / 2, d_out / 2)
        ps.fill(cfg.color_white)
        ps.newpath()
        ps.move_to_xy(g0, 0)
        ps.line_to_xy(g0, sign * d_out)
        ps.move_to_xy(g1, 0)
        ps.line_to_xy(g1, sign * d_out)
        ps.stroke()
    ps.newpath()
    ps.arc(g0, -th_y, +th_y)
    ps.stroke()
    ps.newpath()
    ps.arc(g1, -th_y, +th_y)
    ps.stroke()
    # Central beam orbit (blue): arc up to +/-phi_e around (x_c, 0), then
    # straight extensions past the end guards.
    with ps.transform(x_c, 0):
      ex = D5_ORBIT_EXT
      ps.set_color(cfg.color_blue)
      ps.newpath()
      ps.move_to_xy(D5_RHO * c_e - ex * s_e, -(D5_RHO * s_e + ex * c_e))
      ps.line_to_xy(D5_RHO * c_e, -D5_RHO * s_e)
      ps.arc(D5_RHO, -phi_e, +phi_e)
      ps.line_to_xy(D5_RHO * c_e - ext_out * s_e,
                    D5_RHO * s_e + ext_out * c_e)
      ps.stroke()
    # Label outside the outer yoke arc, on the symmetry axis. Un-rotate by
    # phi_e (plus the caller compensation) so the text renders upright.
    with ps.transform(0, 0, phi_e):
      r_lab = D5_R_OUTER + tag_r
      ps.draw_tag(label, tag_angle,
                  r_lab * c_e + tag_perp * s_e,
                  -r_lab * s_e + tag_perp * c_e, 100)

#______________________________________________________________________________
# D4: twin of D5. Evidence: same rho (Akaishi thesis: 8D440S, bend
# 60 deg, effective length 1989 mm -> rho = 1899 mm = D5's CAD orbit),
# and identical CAD coil-leg lines (1552.4/1353.8/1192.7 mm) and bounding
# rectangles (2900 x 1500) at both magnets. The yoke outline itself is
# missing from the DXF conversion, so D5's yoke geometry is reused.
# Exit-face beam crossing 1940 mm upstream of the D5 entrance crossing
# (refs overview probe: D4 exit face is 700 mm upstream of Q8's center).
D4_DIST = 1940.0

def draw_d4():
  ps.comment('K1.8BR D4')
  px, py, x_c, phi_e = d5_orbit()
  with d5_upstream_frame():
    # D4 exit crossing on the upstream axis; flip so that +y points back
    # downstream (= D4's outgoing beam direction toward Q8/D5).
    ps.translate_xy(0, D4_DIST)
    ps.rotate(180)
    draw_bend('D4', 2 * phi_e)

#______________________________________________________________________________
@contextmanager
def d4_upstream_frame():
  ''' Frame on the straight beam axis upstream of D4: origin at the D4
  entrance-face beam crossing, +y pointing upstream. Yields phi_e; text
  drawn upright needs angle = 4 * phi_e - 180. '''
  px, py, x_c, phi_e = d5_orbit()
  c_e = math.cos(math.radians(phi_e))
  s_e = math.sin(math.radians(phi_e))
  with d5_upstream_frame():
    ps.translate_xy(0, D4_DIST)
    ps.rotate(180)
    ps.translate_xy(-x_c * c_e - D5_RHO, x_c * s_e)
    ps.rotate(-phi_e)
    ps.translate_xy(px, -py)
    ps.rotate(180 - phi_e)
    yield phi_e

#______________________________________________________________________________
# Q7 (Q306, effective length 303 mm), S3 slit, and D3 (6D330S, bend
# 20 deg, effective length 1651 mm -> rho = 4730 mm) on the straight beam
# axis upstream of D4. Positions (mm from the D4 entrance-face crossing)
# and transverse sizes are probe-measured on the refs overview. D3 bends
# the OPPOSITE way to D4/D5 (CoC on the other side of the beam).
Q7_W         = 620.0                # yoke total width
Q7_L         = 300.0                # yoke length along beam
Q7_GAP       = 150.0                # beam channel width
Q7_DIST      = 676.0                # D4 entrance crossing to Q7 center
Q7_PLATE_T   = 30.0                 # end plate thickness
Q7_PLATE_GAP = 37.0                 # gap between yoke and end plate
S3_W         = 450.0                # slit total width
S3_L         = 200.0                # slit length along beam
S3_GAP       = 100.0                # slit opening
S3_DIST      = 1150.0               # D4 entrance crossing to S3 center
D3_RHO       = 4730.0               # K1.8BR orbit radius
D3_BEND      = 20.0                 # K1.8BR bend angle
D3_DIST      = 2200.0               # D4 entrance crossing to D3 exit
# D3 is the K1.8 / K1.8BR switching magnet: a round yoke with a fan-
# shaped pole that covers both exit channels (straight K1.8 and the
# 20 deg K1.8BR bend). Round yoke and fan radii from the CAD (arcs at
# r=1187 / r=750 around its center); the 2900 x 1500 rectangle is the
# return yoke, perpendicular to the K1.8 axis. The yoke center sits
# 620 mm upstream of the K1.8BR exit crossing along the orbit.
D3_YOKE_R    = 1187.0               # round yoke radius
D3_CUT_D     = 908.2                # center to side-cut chords (perp.)
D3_CUT_TILT  = 15.0                 # chord tilt from the fan axis
D3_RECT_L    = 2900.0               # return-yoke rectangle length
D3_RECT_W    = 1500.0               # return-yoke rectangle width
D3_CEN       = 620.0                # exit crossing to yoke center (arc)
D3_FAN_R     = 750.0                # fan pole radius (wide end)
D3_FAN_SPAN  = 80.0                 # fan opening angle
D3_FAN_APEX  = 850.0                # yoke center to fan apex

def draw_q7():
  ps.comment('K1.8BR Q7')
  with d4_upstream_frame() as phi_e:
    for sx in (1, -1):                    # yoke blocks beside the channel
      ps.path_box(sx * (Q7_W + Q7_GAP) / 4, Q7_DIST,
                  (Q7_W - Q7_GAP) / 4, Q7_L / 2)
      ps.fill(cfg.color_orange)
      ps.stroke()
    for sy in (1, -1):                    # end plates, split by the aperture
      d_plate = Q7_L / 2 + Q7_PLATE_GAP + Q7_PLATE_T / 2
      for sx in (1, -1):
        ps.path_box(sx * (Q7_W + Q7_GAP) / 4, Q7_DIST + sy * d_plate,
                    (Q7_W - Q7_GAP) / 4, Q7_PLATE_T / 2)
        ps.fill(cfg.color_orange)
        ps.stroke()
    edges = [Q7_L / 2, Q7_L / 2 + Q7_PLATE_GAP,
             Q7_L / 2 + Q7_PLATE_GAP + Q7_PLATE_T]
    ps.newpath()
    for sy in (1, -1):
      for d_edge in edges:
        ps.move_to_xy(-Q7_GAP / 2, Q7_DIST + sy * d_edge)
        ps.line_to_xy(+Q7_GAP / 2, Q7_DIST + sy * d_edge)
    ps.stroke()
    ps.draw_tag('Q7', 4 * phi_e - 180, -(Q7_W / 2 + 600), Q7_DIST + 300, 0)

def draw_s3():
  ps.comment('K1.8BR S3')
  with d4_upstream_frame() as phi_e:
    for sx in (1, -1):                    # slit jaws beside the opening
      ps.path_box(sx * (S3_W + S3_GAP) / 4, S3_DIST,
                  (S3_W - S3_GAP) / 4, S3_L / 2)
      ps.fill(cfg.color_light_gray)
      ps.stroke()
    # Close the slit opening with a line across it at both faces.
    ps.newpath()
    for sy in (1, -1):
      ps.move_to_xy(-S3_GAP / 2, S3_DIST + sy * S3_L / 2)
      ps.line_to_xy(+S3_GAP / 2, S3_DIST + sy * S3_L / 2)
    ps.stroke()
    ps.draw_tag('S3', 4 * phi_e - 180, -(S3_W / 2 + 600), S3_DIST + 400, 0)

def draw_d3():
  ps.comment('K1.8BR D3')
  with d4_upstream_frame() as phi_e:
    # Straight beam axis (blue) from the D4 entrance up to D3.
    ps.set_color(cfg.color_blue)
    ps.newpath()
    ps.move_to_xy(0, 0)
    ps.line_to_xy(0, D3_DIST)
    ps.stroke()
    ps.translate_xy(0, D3_DIST)
    ps.rotate(180)                        # +y = downstream toward D4
    # K1.8BR exit at the origin. Mirror in x so that the K1.8 channel
    # opens on the correct side of the K1.8BR line (per the refs).
    ps.gsave()
    ps.scale(-1, 1)
    a1 = 180 + D3_BEND
    c1 = math.cos(math.radians(a1))
    s1 = math.sin(math.radians(a1))
    # Yoke center on the orbit, D3_CEN upstream of the exit (arc length).
    d_cen = math.degrees(D3_CEN / D3_RHO)
    cx = D3_RHO * (1 - math.cos(math.radians(d_cen)))
    cy = -D3_RHO * math.sin(math.radians(d_cen))
    kx, ky = s1, -c1                      # K1.8 downstream direction
    k18_mid = math.degrees(math.atan2(ky, kx))   # ~110 deg
    with ps.transform(cx, cy):
      fan_mid = (90 + k18_mid) / 2        # between K1.8BR (+y) and K1.8
      # Return-yoke rectangle, concentric with the round yoke and
      # perpendicular to the fan (symmetry) axis (CAD: 0.7 deg off).
      with ps.transform(0, 0, fan_mid - 90):
        ps.path_box(0, 0, D3_RECT_L / 2, D3_RECT_W / 2)
        ps.fill(cfg.color_dark_green)
        ps.stroke()
      # Round yoke, with its left and right sides cut off inside the
      # return yoke by straight chords (perpendicular distance D3_CUT_D
      # from the center, tilted +/-D3_CUT_TILT from the fan axis, so the
      # cuts form a trapezoid opening toward the exits).
      gam = math.degrees(math.acos(D3_CUT_D / D3_YOKE_R))
      ps.newpath()
      ps.move_to_rtheta(D3_YOKE_R, fan_mid - 105 + gam)
      ps.arc(D3_YOKE_R, fan_mid - 105 + gam, fan_mid + 105 - gam)
      ps.line_to_rtheta(D3_YOKE_R, fan_mid + 105 + gam)
      ps.arc(D3_YOKE_R, fan_mid + 105 + gam, fan_mid + 255 - gam)
      ps.closepath()
      ps.fill(cfg.color_dark_green)
      ps.stroke()
      # Fan-shaped pole gap (white) opening toward both exit channels.
      f0 = fan_mid - D3_FAN_SPAN / 2
      f1 = fan_mid + D3_FAN_SPAN / 2
      ax = D3_FAN_APEX * math.cos(math.radians(fan_mid + 180))
      ay = D3_FAN_APEX * math.sin(math.radians(fan_mid + 180))
      ps.newpath()
      ps.move_to_xy(ax, ay)
      ps.line_to_rtheta(D3_FAN_R, f0)
      ps.arc(D3_FAN_R, f0, f1)
      ps.closepath()
      ps.fill(cfg.color_white)
      ps.stroke()
    ps.grestore()
    ps.draw_tag('D3', 4 * phi_e, D3_RECT_L/2+500,
                -(D3_RECT_W/2+500), 0)

#______________________________________________________________________________
@contextmanager
def d5_upstream_frame():
  ''' Frame on the straight beam axis upstream of D5: origin at the D5
  entrance-face beam crossing, +y pointing upstream. Yields phi_e so
  callers can un-rotate labels back to the ff orientation. '''
  px, py, x_c, phi_e = d5_orbit()
  c_e = math.cos(math.radians(phi_e))
  s_e = math.sin(math.radians(phi_e))
  x, y = geom.ff_to_d5()
  with ps.transform(x, y, geom.ff_angle):
    ps.translate_xy(-x_c * c_e - D5_RHO, x_c * s_e)
    ps.rotate(-phi_e)
    ps.translate_xy(px, -py)
    ps.rotate(180 - phi_e)
    yield phi_e

#______________________________________________________________________________
# Q8 quadrupole, upstream of D5 (in the d5_upstream_frame, distances along
# the beam from the D5 entrance-face crossing). The yoke is missing from
# the DXF conversion (likely a proxy/dynamic block), so dimensions are
# probe-measured on the CAD-derived reference PDF (refs/fa6b640d): yoke
# 1070 x 400 with a ~205 mm beam channel; a 30 mm end plate on each side,
# 120 mm off the body. Body center 1240 mm upstream of the D5 entrance.
Q8_W         = 1070.0               # yoke total width
Q8_L         = 400.0                # yoke length along beam
Q8_GAP       = 205.0                # beam channel width
Q8_DIST      = 1240.0               # D5 entrance crossing to Q8 center
Q8_PLATE_T   = 30.0                 # end plate thickness
Q8_PLATE_GAP = 120.0                # gap between yoke and end plate

def draw_q8():
  ps.comment('K1.8BR Q8')
  with d5_upstream_frame() as phi_e:
    for sx in (1, -1):                    # yoke blocks beside the channel
      ps.path_box(sx * (Q8_W + Q8_GAP) / 4, Q8_DIST,
                  (Q8_W - Q8_GAP) / 4, Q8_L / 2)
      ps.fill(cfg.color_orange)
      ps.stroke()
    for sy in (1, -1):                    # end guards, split by the aperture
      d_plate = Q8_L / 2 + Q8_PLATE_GAP + Q8_PLATE_T / 2
      for sx in (1, -1):
        ps.path_box(sx * (Q8_W + Q8_GAP) / 4, Q8_DIST + sy * d_plate,
                    (Q8_W - Q8_GAP) / 4, Q8_PLATE_T / 2)
        ps.fill(cfg.color_orange)
        ps.stroke()
    # Close each aperture opening with a line across the channel, at both
    # faces of the yoke body and of each end guard.
    edges = [Q8_L / 2, Q8_L / 2 + Q8_PLATE_GAP,
             Q8_L / 2 + Q8_PLATE_GAP + Q8_PLATE_T]
    ps.newpath()
    for sy in (1, -1):
      for d_edge in edges:
        ps.move_to_xy(-Q8_GAP / 2, Q8_DIST + sy * d_edge)
        ps.line_to_xy(+Q8_GAP / 2, Q8_DIST + sy * d_edge)
    ps.stroke()
    # Upstream beam axis (blue) through the channel.
    ps.set_color(cfg.color_blue)
    ps.newpath()
    ps.move_to_xy(0, 0)
    ps.line_to_xy(0, Q8_DIST + Q8_L)
    ps.stroke()
    # Label beside the yoke; un-rotate so the text is upright (ff frame).
    ps.draw_tag('Q8', 2 * phi_e - 180, -(Q8_W / 2 + 300), Q8_DIST + 300, 0)
