import unittest
import os
import shutil
from icad.parts.brk001 import build_brk001
from icad.parts.act001 import build_act001
from icad.parts.ncr001 import build_ncr001
from icad.engine import CADEngine

class TestICAD(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_output"
        self.engine = CADEngine(output_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_brk001_generation(self):
        params = {"length": 50, "width": 30, "thickness": 4}
        shape = build_brk001(params)
        self.assertIsNotNone(shape)
        self.engine.export_part(shape, "BRK-TEST")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "BRK-TEST.step")))

    def test_act001_generation(self):
        params = {"length": 70, "width": 40}
        shape = build_act001(params)
        self.assertIsNotNone(shape)
        self.engine.export_part(shape, "ACT-TEST")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "ACT-TEST.step")))

    def test_ncr001_generation(self):
        params = {"outer_diameter": 40, "length": 15}
        shape = build_ncr001(params)
        self.assertIsNotNone(shape)
        self.engine.export_part(shape, "NCR-TEST")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "NCR-TEST.step")))

    def test_report_generation(self):
        shape = build_brk001({})
        metadata = {"material": "Alu", "density": 0.0027}
        report_path = self.engine.generate_report(shape, "RPT-TEST", metadata)
        self.assertTrue(os.path.exists(report_path))

if __name__ == "__main__":
    unittest.main()
