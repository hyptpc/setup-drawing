setup-drawing
=============

Generates a publication-quality overview figure of the J-PARC E72
experimental setup in the K1.8BR beam line, output as PDF via PostScript.

```sh
$ ./run.py > tmp.ps
$ ps2pdf tmp.ps tmp.pdf
```

Modules
-------

- `run.py` -- entry point; draws all components.
- `config.py` -- paper size, scale, fonts, colors.
- `pshelper.py` -- PostScript drawing primitives (paths, arcs, text tags).
- `geomhelper.py` -- FF-coordinate helpers (`ff_angle`, `ff_to_xy`).
- `shs.py` -- SHS magnet, HypTPC, target.
- `counter.py` -- counters (BAC, BH2, BHT, KVC, FTOF, SAC/SFV, ...).
- `driftchamber.py` -- BLC1a/b and BLC2a/b drift chambers.
- `beamline.py` -- K1.8BR beam line elements (D3/D4/D5 bending magnets,
  Q7/Q8 quadrupoles, S3 slit).

D5 bending magnet
-----------------

Geometry is taken directly from the CAD drawing (kept locally; excluded
from this repository). The yoke is a 6-vertex gingko shape: outer arc at
r = 2606.6 mm spanning 68.75 deg around the yoke center, two radial
faces, and a square "kaname" (keystone) on the center-of-curvature side.
Coil ends (maroon) and end guards (green) are drawn at both faces.

The beam orbit (rho = 1898.4 mm) crosses the pole-gap aperture center
(r = 1666.7 mm) on both yoke faces; its center of curvature does not
coincide with the yoke center, so the faces are non-normal to the beam
(edge angle ~4.7 deg) and the actual bend angle is 59.43 deg. Particles
bend only inside the yoke; outside, the beam is straight and passes the
straight coil/end-guard apertures slightly off center.

The exit-face beam crossing is anchored at FF z = -1766.0 mm
(309.4 mm upstream of BLC2a, per survey).

Q8 quadrupole
-------------

Drawn in plan view on the straight beam axis upstream of D5: yoke
1070 x 400 mm with a 205 mm beam channel, plus a 30 mm end plate on each
side (120 mm off the body); body center 1240 mm upstream of the D5
entrance-face beam crossing. The yoke is missing from the DXF conversion
of the CAD (likely a proxy/dynamic block), so these dimensions were
probe-measured on the CAD-derived reference PDF (accuracy ~5%).

D4 bending magnet
-----------------

Twin of D5: same rho (Akaishi thesis: 8D440S, bend 60 deg, effective
length 1989 mm -> rho = 1899 mm) and identical CAD coil-leg lines and
bounding rectangles at both magnets, so D5's yoke geometry is reused.
Its exit-face beam crossing sits 1940 mm upstream of the D5 entrance
crossing on the straight beam axis (refs overview probe: 700 mm
upstream of Q8's center).

BLC1
----

BLC1a/b are identical planar MWDCs, 300 mm apart along the beam, with an
effective area of 256 x 256 mm (Akaishi thesis, Table 2.5). They sit on
the upstream straight beam axis between the D5 entrance end guard and
Q8: BLC1b at 310 mm and BLC1a at 610 mm upstream of the D5 entrance-face
beam crossing.

Upstream of D4
--------------

Q7 (Q306, 300 mm body), the S3 slit (200 mm jaws, with the screw
mechanism in the CAD), and the BHT hodoscope sit on the straight beam
axis between D4 and D3, at 676 / 1150 / 1470 mm upstream of the D4
entrance-face crossing (refs overview probes). D3 (6D330S, K1.8BR bend
20 deg, rho = 4730 mm) is the K1.8 / K1.8BR switching magnet: a round
yoke (r = 1187 mm, CAD) with trapezoidal side cuts (chords 908 mm from
the center, tilted +/-15 deg from the fan axis), a 2900 x 1500 return
yoke perpendicular to the fan axis, and a fan-shaped pole gap that
covers both exit channels. The central orbit (blue) runs from D3's exit
through D4 and D5 to the target.
