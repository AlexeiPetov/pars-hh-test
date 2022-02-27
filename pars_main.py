from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class ParsHH:
    browser = webdriver.Chrome()
    list_vacancy = [] #name/href/pay/company
    def __init__(self, link="https://novosibirsk.hh.ru/", imp_wait=3):
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
            print(i.find_element_by_css_selector('a[data-qa="vacancy-serp__vacancy-title"]').text)
        


















if __name__ == "__main__":
    x = ParsHH()
    x.go_to_the_page()
    x.search_vacancy()
    input()