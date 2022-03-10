from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import sqlite3

class ParsHH:

    def __init__(self, link="https://novosibirsk.hh.ru/",
                        search_profession='QA Automation',
                        imp_wait=0.1):
        self.link = link
        self.search_profession = search_profession
        self.imp_wait = imp_wait

        self.list_vacancy = []

        self.db = sqlite3.connect('SQL.db') #подключил БД
        self.sql = self.db.cursor()
        self.sql.execute('''CREATE TABLE IF NOT EXISTS users (
            NAMEVACANCY TEXT,
            COMPENSATION TEXT,
            NAMEORGANIZATION TEXT,
            LINKVACANCY TEXT
            )''') #создал таблицу
        self.db.commit()


        self.options = webdriver.ChromeOptions()
        self.options.add_argument('log-level=3')

        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.implicitly_wait(imp_wait)

######################################

    def go_to_the_page(self):
        self.browser.get(self.link)
        element_seartch = self.browser.find_element(By.CSS_SELECTOR,'input[data-qa="search-input"]')
        element_seartch.click()
        element_seartch.send_keys(self.search_profession)
        element_seartch.send_keys(Keys.ENTER)


    def search_vacancy(self):
        count = self.browser.find_elements(By.CSS_SELECTOR,'div.vacancy-serp-item')
        for i in count:
            list_vacancy_item = []
            list_vacancy_item.append(i.find_element(By.CSS_SELECTOR,'a[data-qa="vacancy-serp__vacancy-title"]').text)
            try:
                list_vacancy_item.append(i.find_element(By.CSS_SELECTOR,'span[data-qa="vacancy-serp__vacancy-compensation"]').text)
            except:
                list_vacancy_item.append('None')

            list_vacancy_item.append(i.find_element(By.CSS_SELECTOR,'a[data-qa="vacancy-serp__vacancy-employer"]').text)
            list_vacancy_item.append(i.find_element(By.CSS_SELECTOR,'a[data-qa="vacancy-serp__vacancy-title"]').get_attribute("href"))
            self.list_vacancy.append(list_vacancy_item)
        return self.list_vacancy

######################################


    def save_db(self):
        self.sql.execute('DELETE FROM users')
        self.db.commit()
        for val in self.list_vacancy:
            self.sql.execute("INSERT INTO users VALUES(?, ?, ?, ?);", val)
            self.db.commit()        

    def close_db(self):
        self.db.close()

    def clear_db(self):
        self.sql.execute('DELETE FROM users')
        self.db.commit()
######################################

    def output_db(self):
        out_db = []
        for val in self.sql.execute('SELECT * FROM users'):
            out_db.append(val)
        if len(out_db) == 0:
            return 0
        else:
            return out_db


    def output_new_vacancy(self):
        vacancy_db = [val for val in self.sql.execute('SELECT * FROM users')]
        new_vacancy = []
        for val in self.list_vacancy:
            if tuple(val) not in vacancy_db:
                new_vacancy.append(val)
        if len(new_vacancy) == 0:
            return 0
        else:
            return new_vacancy
            
    def output_vacancy(self):
        out_vacancy = self.search_vacancy()
        if len(out_vacancy) == 0:
            return 0
        else:
            return out_vacancy

if __name__ == "__main__":
    os.system('cls')
    x = ParsHH()
    x.clear_db()
    x.go_to_the_page()
    x.search_vacancy()
    x.output_new_vacancy()
    x.output_db()
    x.save_db()
    x.close_db()
    