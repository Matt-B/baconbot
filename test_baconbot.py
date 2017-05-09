import unittest
from baconbot import parse_order


class TestBaconBot(unittest.TestCase):

    def test_parse_order_with_one_item(self):
        result = parse_order("<@U57Q422TE> order 1", "U57306N2C")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Bacon Baguette (Small)")

    def test_parse_order_with_two_items(self):
        result = parse_order("<@U57Q422TE> order 1 3", "U57306N2C")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Bacon Baguette (Small)")
        self.assertEqual(result[1], "Bacon and Sausage Baguette (Small)")

    def test_parse_order_with_invalid_command(self):
        result = parse_order("<@U57Q422TE> order some cheese", "U57306N2C")
        self.assertEqual(len(result), 0)

    def test_parse_order_with_numbers_not_on_menu(self):
        result = parse_order("<@U57Q422TE> order 75 99", "U57306N2C")
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
