from django.test import TestCase
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from cars.models import CarMarks,CarSeries
import selenium

# Create your tests here.

class CarSeriesTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(CarSeriesTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CarSeriesTest, cls).tearDownClass()


    def test_car_page(self):
        mark = CarMarks.objects.create(id = 1, name = 'Skoda', auto_ria_id = 70)
        mark.carseries_set.create(name = '100', series_auto_ria_id = 1573)
        mark.carseries_set.create(name = '105', series_auto_ria_id = 645)
        mark.carseries_set.create(name = '120', series_auto_ria_id = 646)
        mark.carseries_set.create(name = 'Fabia', series_auto_ria_id = 649)
        mark.carseries_set.create(name = 'Octavia', series_auto_ria_id = 652)

        self.selenium.get('%s%s' % (self.live_server_url, '/cars'))
        self.selenium.find_element_by_xpath("//select/option[@value='1']").click()
        self.selenium.find_element_by_tag_name('input').click()
















