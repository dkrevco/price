from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
import time
import json

class Browser:

    def __init__(self):

        headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={headers}')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_window_size(1920, 1080)
        self.string = f'this is browser class'

    def open_url(self, url):
        self.driver.get(url)
        self.url = url
        time.sleep(3)
        return self.url


class ReStore(Browser):

    def __init__(self):
        self.pagination_link = '?page='
        self.products = {}

        super().__init__()

    def _choose_region(self):
        time.sleep(1)
        city_menu_selector = self.driver.find_element(By.CLASS_NAME, 'choose-region__btn')
        city_menu_selector.click()
        time.sleep(0.5)
        spb = self.driver.find_element(By.XPATH, '//div[@class="choose-city__city"][2]')
        time.sleep(0.5)
        spb.click()
        time.sleep(2)

    def _make_file_name(self):

        self.file_name = self.url.split('/')[-2]
        return self.file_name

    def _get_pagination_depth_number(self):

        pagination = self.driver.find_elements(By.CLASS_NAME, "pagination__item")
        return len(pagination)

    def _get_on_page_products(self):

        self.on_page_products = self.driver.find_elements(By.CLASS_NAME, "product-card.catalog__item.product-card--buy")
        return self.on_page_products

    def _parse_products(self):

        for item in self.on_page_products:

            item_href = item.find_element(By.CLASS_NAME, "product-card__link")
            item_a = item_href.get_attribute('href')
            item_pn = item_a.split('/')[-2]
            # item_hint = item.find_element(By.CLASS_NAME, "product-card__hint").text
            item_price = item.find_element(By.CLASS_NAME, "product-card__price").text
            item_name = item.find_element(By.CLASS_NAME, "product-card__name").text

            self.products[item_pn] = { 'name': item_name,
                                      'link': item_a,
                                       'price': item_price,
                                       # 'hint': item_hint
                                      }


    def _create_local_file(self):

        with open(f'../price/restore/{self.file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(self.products, file, indent=4, ensure_ascii=False)
            file.close()

    def _make_folder(self):

        if not os.path.exists(f'../price/restore/'):
            os.mkdir(f'../price/restore/')

    def _create_data(self):

        self._get_on_page_products()
        self._parse_products()

    def _write_data(self):
        self._make_file_name()
        self._make_folder()
        self._create_local_file()

    def _open_paginated_pages(self):

        for i in range(2,self._get_pagination_depth_number() + 1):
            self.open_url(f'{self.url}{self.pagination_link}{i}')

    def run(self, url: str):

        try:
            self.open_url(url)
            self._choose_region()
            self._create_data()
            if self._get_pagination_depth_number() > 1:
                self._open_paginated_pages()
                self._create_data()
            self._write_data()
        except Exception as ex:
            print(ex)
