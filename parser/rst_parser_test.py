__author__ = 'Andriy.Malaman'

import unittest
import rst_parser
import urllib.request
from bs4 import BeautifulSoup
import os

def connect_to_url():
    """
    Reads HTML content from http://auto.ria.com
    """
    return urllib.request.urlopen("http://rst.ua")

class ConnectionTest(unittest.TestCase):
    def testConnectionToURL(self):
        """
        Tests connection to the auto.ria.co site


        """
        try:
            connect_to_url()
            connect_to_url().close()
        except:
            raise (Exception, "Unable to connect to URL")

class ParserTest(unittest.TestCase):
    def test_get_all_prices_per_page_usd(self):
        """
        Tests functions auto_ria_parser.get_all_prices_per_page_usd
        input argument for function is locally stored html file
        if function prints some list of values, then test is passed
        """

        f = open(os.path.join(os.path.dirname(__file__), './add/rst_parser_test/rst_sample.html'),"rt",encoding="utf-8")
        soup = BeautifulSoup(f,"html")
        res = rst_parser.get_all_prices_per_page_usd(soup)
        if res:
            print(res)
        else:
            raise (Exception,"Failure of test_get_all_prices_per_page_usd")



if __name__ == "__main__":
    unittest.main()
