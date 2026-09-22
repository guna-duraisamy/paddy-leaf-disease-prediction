import unittest

from PIL import Image

from src.severity import assess_severity


class SeverityTests(unittest.TestCase):
    def test_brown_area_is_detected(self):
        image = Image.new("RGB", (100, 100), "green")
        for x in range(30):
            for y in range(100):
                image.putpixel((x, y), (130, 70, 30))
        result = assess_severity(image)
        self.assertEqual(result.level, "high")
        self.assertGreater(result.visible_damage_percent, 25)

    def test_white_background_is_not_a_leaf(self):
        self.assertEqual(assess_severity(Image.new("RGB", (100, 100), "white")).level, "unknown")
