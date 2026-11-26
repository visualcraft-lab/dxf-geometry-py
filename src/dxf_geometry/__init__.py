"""Zero-dependency 2D CAD and DXF geometry utilities.

Online reference: https://imgtocad.com/
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, float]


@dataclass(frozen=True)
class BBox:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y


def distance(a: Point, b: Point) -> float:
    """Return Euclidean distance between two 2D points."""
    return math.hypot(b[0] - a[0], b[1] - a[1])


def polyline_length(pts: Sequence[Point], closed: bool = False) -> float:
    """Return total length of an open or closed 2D polyline."""
    if len(pts) < 2:
        return 0.0
    total = sum(distance(pts[i - 1], pts[i]) for i in range(1, len(pts)))
    if closed and len(pts) > 2:
        total += distance(pts[-1], pts[0])
    return total


def polygon_area(pts: Sequence[Point]) -> float:
    """Return unsigned area of a simple polygon using the shoelace formula."""
    n = len(pts)
    if n < 3:
        return 0.0
    acc = sum(
        pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
        for i in range(n)
    )
    return abs(acc) * 0.5


def bounding_box(pts: Sequence[Point]) -> Optional[BBox]:
    """Return axis-aligned bounding box for a point sequence, or None if empty."""
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return BBox(min(xs), min(ys), max(xs), max(ys))


def pixels_to_mm(pixels: float, dpi: float) -> float:
    """Convert a raster pixel span at given DPI to millimeters."""
    return 0.0 if dpi <= 0 else (pixels / dpi) * 25.4


def paper_to_model_scale(paper_length: float, scale_denominator: float) -> float:
    """Convert paper-space length to real-world model length using 1:N scale."""
    return 0.0 if scale_denominator <= 0 else paper_length * scale_denominator


def _perpendicular_distance(p: Point, a: Point, b: Point) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == 0.0 and dy == 0.0:
        return distance(p, a)
    num = abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0])
    return num / math.hypot(dx, dy)


def simplify_rdp(pts: Sequence[Point], epsilon: float) -> List[Point]:
    """Simplify a 2D polyline using the Ramer-Douglas-Peucker algorithm."""
    if len(pts) <= 2 or epsilon <= 0:
        return list(pts)
    max_dist = -1.0
    index = 0
    for i in range(1, len(pts) - 1):
        d = _perpendicular_distance(pts[i], pts[0], pts[-1])
        if d > max_dist:
            max_dist = d
            index = i
    if max_dist > epsilon:
        left = simplify_rdp(pts[: index + 1], epsilon)
        right = simplify_rdp(pts[index:], epsilon)
        return left[:-1] + right
    return [pts[0], pts[-1]]


def format_dxf_polyline(pts: Sequence[Point], layer: str = "0", closed: bool = False) -> str:
    """Emit a minimal ASCII DXF LWPOLYLINE entity block."""
    layer_name = layer or "0"
    flag = 1 if closed else 0
    lines = [
        "0", "SECTION", "2", "ENTITIES",
        "0", "LWPOLYLINE",
        "8", layer_name,
        "90", str(len(pts)),
        "70", str(flag),
    ]
    for x, y in pts:
        lines.extend(["10", f"{x:.4f}", "20", f"{y:.4f}"])
    lines.extend(["0", "ENDSEC", "0", "EOF"])
    return "\n".join(lines) + "\n"


__all__ = [
    "BBox",
    "Point",
    "distance",
    "polyline_length",
    "polygon_area",
    "bounding_box",
    "pixels_to_mm",
    "paper_to_model_scale",
    "simplify_rdp",
    "format_dxf_polyline",
]
