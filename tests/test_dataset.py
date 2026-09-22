import unittest
from pathlib import Path

from src.dataset import inspect_dataset


class DatasetTests(unittest.TestCase):
    def test_missing_classes_are_reported(self):
        template = Path(__file__).resolve().parents[1] / "dataset" / "raw"
        with self.assertRaisesRegex(ValueError, "Missing class folders"):
            inspect_dataset(template)


if __name__ == "__main__":
    unittest.main()
