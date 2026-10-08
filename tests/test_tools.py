import unittest

from smartphone_recommendation.tools import (
    compare_smartphones,
    load_smartphones,
    recommend_smartphones,
    review_smartphone,
)


class SmartphoneToolsTests(unittest.TestCase):
    def test_dataset_is_normalized(self) -> None:
        dataframe = load_smartphones()

        self.assertGreater(len(dataframe), 800)
        self.assertTrue(dataframe["price"].dtype.kind in "iu")
        self.assertTrue(dataframe["has_5g"].any())

    def test_review_returns_matching_phone(self) -> None:
        result = review_smartphone("OnePlus 11 5G")

        self.assertIn("Review: OnePlus 11 5G", result)
        self.assertIn("Price: Rs. 54,999", result)

    def test_compare_returns_both_phones(self) -> None:
        result = compare_smartphones("OnePlus 11 5G", "OnePlus Nord CE 2 Lite 5G")

        self.assertIn("OnePlus 11 5G", result)
        self.assertIn("OnePlus Nord CE 2 Lite 5G", result)

    def test_recommendation_respects_criteria(self) -> None:
        result = recommend_smartphones(max_price=60_000, min_rating=89, required_5g=True)

        self.assertIn("Recommended smartphones:", result)
        self.assertNotIn("non-5G", result)


if __name__ == "__main__":
    unittest.main()
