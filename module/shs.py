import math

from . import config as cfg
from . import geomhelper as geom
from . import pshelper as ps

#______________________________________________________________________________
def draw():
  ps.comment('Superconducting Hyperon Spectrometer')
  x, y = geom.ff_to_xy(-150)
  with ps.transform(x, y, geom.ff_angle):
    draw_magnet()
    draw_htof()
    draw_hyptpc()
  x, y = geom.ff_to_xy(-150-143)
  with ps.transform(x, y, geom.ff_angle):
    draw_target()
  draw_scatter()

#______________________________________________________________________________
def lambda_decay_tracks(p_k, th_star):
  ''' Lorentz kinematics of K- p -> Lambda pi0 at beam momentum p_k,
  with the Lambda emitted forward and decaying to p pi- at angle th_star
  [deg] in its rest frame. Returns ((p, tilt) for proton, pion): lab
  momenta [MeV/c] and angles from the beam axis [deg, + = pion side]. '''
  m_k, m_p, m_l = 493.677, 938.272, 1115.683
  m_pi0, m_pi = 134.977, 139.570
  e_k = math.hypot(p_k, m_k)
  s = (e_k + m_p)**2 - p_k**2
  rs = math.sqrt(s)
  # Lambda in the CM frame, then boosted to the lab (forward emission)
  p_st = math.sqrt((s - (m_l + m_pi0)**2) * (s - (m_l - m_pi0)**2)) / 2 / rs
  beta = p_k / (e_k + m_p)
  gam = 1 / math.sqrt(1 - beta * beta)
  p_lam = gam * (p_st + beta * math.hypot(p_st, m_l))
  e_lam = math.hypot(p_lam, m_l)
  # two-body decay momentum in the Lambda rest frame
  q = math.sqrt((m_l**2 - (m_p + m_pi)**2) *
                (m_l**2 - (m_p - m_pi)**2)) / 2 / m_l
  qz = q * math.cos(math.radians(th_star))
  qt = q * math.sin(math.radians(th_star))
  bl, gl = p_lam / e_lam, e_lam / m_l
  tracks = []
  for m, sz, st in ((m_p, qz, -qt), (m_pi, -qz, qt)):  # pion to the left
    pz = gl * (sz + bl * math.hypot(q, m))
    tracks.append((math.hypot(pz, st),
                   math.degrees(math.atan2(st, pz))))
  return tracks

#______________________________________________________________________________
def draw_scatter():
  ps.comment('Tracks from the target (uniform-field model)')
  # Beam tracks (negative) bend to the KVC veto counter. The Lambda-
  # production trigger pair bends to HTOF: a high-momentum proton to the
  # right, a low-momentum pi- to the left. Conditions from config.yml.
  b_field = cfg.track_b_field
  z_target = -293.0
  r_htof = 345.0                      # HTOF barrel radius
  z_htof = 143.0                      # HTOF center, downstream of target
  x, y = geom.ff_to_xy(z_target)
  with ps.transform(x, y, geom.ff_angle):
    beam_moms = cfg.track_beam_moms if cfg.draw_beam else ()
    for p_beam in beam_moms:
      rho = p_beam / (0.29979 * b_field)
      th_end = math.degrees(math.asin((cfg.track_z_end - z_target) / rho))
      with ps.transform(-rho, 0):     # CoC on the KVC (left) side
        ps.set_color(cfg.color_blue)
        ps.newpath()
        ps.arc(rho, 0, th_end)
        ps.stroke()
    if not cfg.draw_decay:
      return
    (p_p, tilt_p), (p_pi, tilt_pi) = lambda_decay_tracks(
        cfg.track_reaction_mom, cfg.track_decay_angle)
    pair = ((p_p, tilt_p, 1, cfg.color_red),
            (p_pi, tilt_pi, -1, cfg.color_purple))
    for p_mom, tilt, sgn, color in pair:   # proton / pi-
      rho = p_mom / (0.29979 * b_field)
      t_rad = math.radians(tilt)
      hx = z_htof * math.sin(t_rad)   # HTOF center in the tilted frame
      hy = z_htof * math.cos(t_rad)
      lo, hi = 0.0, 120.0             # bisect the HTOF barrel crossing
      for _ in range(40):
        mid = (lo + hi) / 2
        dx = sgn * rho * (1 - math.cos(math.radians(mid))) - hx
        dy = rho * math.sin(math.radians(mid)) - hy
        if math.hypot(dx, dy) < r_htof:
          lo = mid
        else:
          hi = mid
      with ps.transform(0, 0, tilt):
        with ps.transform(sgn * rho, 0):
          ps.set_color(color)
          ps.newpath()
          if sgn > 0:
            ps.arcn(rho, 180, 180 - hi)
          else:
            ps.arc(rho, 0, hi)
          ps.stroke()

#______________________________________________________________________________
def draw_hyptpc():
  ps.comment('HypTPC')
  w = 500.0 / 2
  l = w * math.tan(math.radians(22.5))
  x = [-w, -w, -l, l, w, w, l, -l, -w]
  y = [-l, l, w, w, l, -l, -w, -w, -l]
  with ps.transform():
    ps.draw_polygon(x, y, cfg.color_light_yellow)
  # ps.draw_tag('HypTPC', 0, 250, 0, -1)

#______________________________________________________________________________
def draw_htof():
  ps.comment('HTOF')
  n_layer = 8
  n_seg = 4
  x = 68.0 / 2
  z = 10.0 / 2
  l = 340.0 # distance from center
  for i in range(n_layer):
    with ps.transform():
      ps.rotate(i*45)
      ps.translate_xy(-5*x, -l)
      for j in range(n_seg):
        ps.translate_xy(2*x, 0)
        ps.draw_box(x, z, cfg.color_white)
  # ps.draw_tag('HTOF', 0, 340, 140, -4)

#______________________________________________________________________________
def draw_magnet():
  ps.comment('SHS Magnet')
  yoke_x = 1920 / 2
  yoke_z = 1200 / 2
  yoke_hole_outer_r = 800 /2
  yoke_hole_inner_r = 600 /2
  ps.draw_box(yoke_x, yoke_z, cfg.color_light_pink)
  ps.draw_circle(yoke_hole_outer_r, cfg.color_light_gray)
  ps.draw_circle(yoke_hole_inner_r, 1)
  ps.draw_tag('SHS', 0, 1100, 0, 0)

#______________________________________________________________________________
def draw_target():
  ps.comment('Liquid Hydrogen Target')
  r = (113 + 107) / 2 / 2
  ps.draw_circle(r, cfg.color_white)
  # r = 107 / 2
  # ps.draw_circle(r, cfg.color_white)
  # r = 94 / 2
  # ps.draw_circle(r, cfg.color_white)
  r = 80 / 2
  ps.draw_circle(r, cfg.color_light_cyan)
  # ps.draw_tag('LH|2| Target', 0, 20, -20, -5)
