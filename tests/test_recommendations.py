import unittest

from src.recommendations import get_recommendation, normalize_label


class RecommendationTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize_label("Brown Spot"), "brown_spot")

    def test_known_disease(self):
        result = get_recommendation("leaf_smut")
        self.assertEqual(result.disease, "Leaf smut")
        self.assertTrue(result.fertilizer)

    def test_unknown_disease_is_safe(self):
        self.assertIn("verify", get_recommendation("new disease").pesticide[0])


if __name__ == "__main__":
    unittest.main()
