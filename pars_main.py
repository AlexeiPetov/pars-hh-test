
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import sqlite3

class ParsHH:

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    browser = webdriver.Chrome(chrome_options=options)

    db = sqlite3.connect('SQL.db') #подключил БД
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS users (
        NAMEVACANCY TEXT,
        COMPENSATION TEXT,
        NAMEORGANIZATION TEXT,
        LINKVACANCY TEXT
    )''') #создал таблицу
    db.commit()

    list_vacancy = []

    def __init__(self, link="https://novosibirsk.hh.ru/", imp_wait=0.1):
        self.link = link
        self.imp_wait = imp_wait
        self.browser.get(self.link)
        self.browser.implicitly_wait(imp_wait)

    def go_to_the_page(self):
        element_seartch = self.browser.find_element_by_css_selector('input[data-qa="search-input"]')
        element_seartch.click()
        element_seartch.send_keys('QA Automation')
        element_seartch.send_keys(Keys.ENTER)

    def search_vacancy(self):
        count = self.browser.find_elements_by_css_selector('div.vacancy-serp-item')
        for i in count:
            self.list_vacancy = []
            self.list_vacancy.append(i.find_element_by_css_selector('a[data-qa="vacancy-serp__vacancy-title"]').text)

            try:
                self.list_vacancy.append(i.find_element_by_css_selector('span[data-qa="vacancy-serp__vacancy-compensation"]').text)
            except:
                self.list_vacancy.append('None')

            self.list_vacancy.append(i.find_element_by_css_selector('a[data-qa="vacancy-serp__vacancy-employer"]').text)
            self.list_vacancy.append(i.find_element_by_css_selector('a[data-qa="vacancy-serp__vacancy-title"]').get_attribute("href"))
            self.sql.execute("INSERT INTO users VALUES(?, ?, ?, ?);", self.list_vacancy)
            self.db.commit()

    def output_db(self):
        for val in self.sql.execute('SELECT * FROM users'):
            print('Наименование вакансии: ' + val[0])
            print('ЗП: ' + val[1])
            print('Организация: ' + val[2])
            print('Ссылка на ваканмию: ' + val[3])
            print('------------------------------')
        


if __name__ == "__main__":
    os.system('cls')
    x = ParsHH()
    x.go_to_the_page()
    x.search_vacancy()
    x.output_db()