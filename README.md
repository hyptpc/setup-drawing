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
- `counter.py` -- counters (BAC, BH2, KVC, FTOF, SAC/SFV, ...).
- `driftchamber.py` -- BLC2a/BLC2b drift chambers.
- `beamline.py` -- K1.8BR beam line elements (D5 bending magnet).

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
