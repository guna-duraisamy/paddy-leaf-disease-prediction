import unittest
from pathlib import Path

from src.dataset import inspect_dataset


class DatasetTests(unittest.TestCase):
    def test_missing_classes_are_reported(self):
        missing = Path(__file__).resolve().parents[1] / "dataset" / "not_present"
        with self.assertRaisesRegex(ValueError, "does not exist"):
            inspect_dataset(missing)


if __name__ == "__main__":
    unittest.main()
