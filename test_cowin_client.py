import unittest

import httpretty

from cowin_client import CoWinClient


class TestCoWinClient(unittest.TestCase):
    @httpretty.activate
    def test_get_under_45_capacity(self):
        lucknow_district_id = 670
        client = CoWinClient(lucknow_district_id)
        # register cowin url
        with open('test_data.json', 'rb') as f:
            httpretty.register_uri(
                method=httpretty.GET,
                uri=client.url,
                body=f.read()
            )
        capacity = client.get_under_45_capacity()
        self.assertEqual(capacity['total'], 123)
        self.assertEqual(capacity['dose_1'], 65)
        self.assertEqual(capacity['dose_2'], 58)


if __name__ == '__main__':
    unittest.main()
