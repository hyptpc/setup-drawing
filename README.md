setup-drawing
=============

Generates a publication-quality overview figure of the J-PARC E72
experimental setup in the K1.8BR beam line, output as PDF via PostScript.

![Example](example.png)

Setup
-----

Create a virtual environment and install the dependencies (PyYAML):

```sh
$ python3 -m venv .venv
$ .venv/bin/pip install pyyaml
```

Usage
-----

```sh
$ source .venv/bin/activate
$ ./run.py > tmp.ps
$ ps2pdf tmp.ps tmp.pdf
$ pdfcrop --margins 10 tmp.pdf tmp.pdf
```

`pdfcrop` (TeX Live) trims the output to the drawn content. As an
alternative, set `bbox: [x0, y0, x1, y1]` (page mm) in `config.yml` and
use `ps2pdf -dEPSCrop`.

Drawing settings (paper size, scale, fonts, colors, tracks) live in
`config.yml`; an alternative file can be passed as the first argument:
`./run.py myconfig.yml > tmp.ps`.

Modules
-------

- `run.py` -- entry point; draws all components.
- `module/config.py` -- loads `config.yml` into module attributes.
- `module/pshelper.py` -- PostScript drawing primitives (paths, arcs,
  text tags).
- `module/geomhelper.py` -- FF-coordinate helpers (`ff_angle`,
  `ff_to_xy`).
- `module/shs.py` -- SHS magnet, HypTPC, target, tracks from the target.
- `module/counter.py` -- counters (BAC, BH2, BHT, KVC, FTOF, ...).
- `module/driftchamber.py` -- BLC1a/b and BLC2a/b drift chambers.
- `module/beamline.py` -- K1.8BR beam line elements (D3/D4/D5 bending
  magnets, Q7/Q8 quadrupoles, S3 slit).

The element geometries are taken from the CAD drawings (kept locally;
excluded from this repository) and reference documents; details are
documented as comments in each module.
