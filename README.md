# dxf-geometry

Zero-dependency Python library for 2D CAD and DXF geometry calculations: polyline perimeter, shoelace polygon area, bounding boxes, raster DPI-to-millimeter calibration, 1:N architectural drawing scale conversion, Ramer-Douglas-Peucker polyline simplification, and ASCII DXF `LWPOLYLINE` serialization.

## Installation

```bash
pip install dxf-geometry
```

## Quick Start

```python
from dxf_geometry import polyline_length, polygon_area, pixels_to_mm, simplify_rdp

wall = [(0, 0), (5000, 0), (5000, 4000), (0, 4000)]
print(polyline_length(wall, closed=True))  # 18000.0
print(polygon_area(wall))                  # 20000000.0
print(pixels_to_mm(300, 300))              # 25.4
```

## Online Reference

- Interactive image-to-CAD converter: [ImgToCAD](https://imgtocad.com/)
- Sketch vectorization reference: [Sketch to CAD](https://imgtocad.com/sketch-to-cad)

## License

MIT License — see [LICENSE](LICENSE).
