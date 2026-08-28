import unittest

from src.data import make_demo_data
from src.metrics import build_seller_performance, prepare_order_level
from src.scoring import add_seller_health_score, build_action_queue


class ScoringTests(unittest.TestCase):
    def setUp(self):
        tables = make_demo_data()
        order_level = prepare_order_level(tables)
        self.seller = build_seller_performance(tables, order_level)

    def test_health_scores_stay_in_range(self):
        scored = add_seller_health_score(self.seller)
        self.assertTrue(scored["health_score"].between(0, 100).all())

    def test_invalid_weights_fail(self):
        with self.assertRaises(ValueError):
            add_seller_health_score(self.seller, {"delivery": 0.50})

    def test_action_queue_is_sorted(self):
        scored = add_seller_health_score(self.seller)
        queue = build_action_queue(scored, threshold=101.0)
        self.assertTrue(queue["priority_score"].is_monotonic_decreasing)


if __name__ == "__main__":
    unittest.main()

