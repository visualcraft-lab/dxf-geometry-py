import unittest
from dxf_geometry import (
    bounding_box,
    format_dxf_polyline,
    paper_to_model_scale,
    pixels_to_mm,
    polygon_area,
    polyline_length,
    simplify_rdp,
)


class TestDxfGeometry(unittest.TestCase):
    def test_polyline_and_area(self):
        sq = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
        self.assertAlmostEqual(polyline_length(sq, False), 30.0)
        self.assertAlmostEqual(polyline_length(sq, True), 40.0)
        self.assertAlmostEqual(polygon_area(sq), 100.0)

    def test_bbox_and_scales(self):
        bbox = bounding_box([(-2.0, 5.0), (8.0, -3.0), (4.0, 12.0)])
        self.assertIsNotNone(bbox)
        self.assertAlmostEqual(bbox.width, 10.0)
        self.assertAlmostEqual(bbox.height, 15.0)
        self.assertAlmostEqual(pixels_to_mm(300.0, 300.0), 25.4)
        self.assertAlmostEqual(paper_to_model_scale(20.0, 50.0), 1000.0)

    def test_simplify_and_dxf(self):
        pts = [(0.0, 0.0), (5.0, 0.05), (10.0, 0.0), (10.0, 10.0)]
        out = simplify_rdp(pts, 0.2)
        self.assertEqual(len(out), 3)
        dxf = format_dxf_polyline(out, "WALLS", True)
        self.assertIn("LWPOLYLINE", dxf)
        self.assertIn("WALLS", dxf)
        self.assertIn("EOF", dxf)


if __name__ == "__main__":
    unittest.main()
