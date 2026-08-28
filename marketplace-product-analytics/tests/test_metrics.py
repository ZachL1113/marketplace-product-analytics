import unittest

from src.data import make_demo_data
from src.metrics import build_seller_performance, calculate_kpis, prepare_order_level


class MetricTests(unittest.TestCase):
    def setUp(self):
        self.tables = make_demo_data()
        self.order_level = prepare_order_level(self.tables)

    def test_order_grain_is_preserved(self):
        self.assertEqual(self.order_level["order_id"].nunique(), len(self.order_level))

    def test_kpis_have_expected_ranges(self):
        kpis = calculate_kpis(self.order_level)
        self.assertEqual(kpis["orders"], 10.0)
        self.assertGreater(kpis["gmv"], 0.0)
        self.assertGreaterEqual(kpis["repeat_purchase_rate"], 0.0)
        self.assertLessEqual(kpis["repeat_purchase_rate"], 1.0)
        self.assertGreaterEqual(kpis["on_time_delivery_rate"], 0.0)
        self.assertLessEqual(kpis["on_time_delivery_rate"], 1.0)

    def test_seller_metrics_return_one_row_per_seller(self):
        seller = build_seller_performance(self.tables, self.order_level)
        self.assertEqual(seller["seller_id"].nunique(), len(seller))
        self.assertEqual(set(seller["seller_id"]), {"s01", "s02", "s03"})


if __name__ == "__main__":
    unittest.main()

