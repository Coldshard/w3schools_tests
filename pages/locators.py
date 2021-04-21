from selenium.webdriver.common.by import By


class PageLocators(object):
    CODE_BLOCK = (By.CSS_SELECTOR, ".CodeMirror-code")
    RUN_BUTTON = (By.CSS_SELECTOR, ".w3-green")
    SQL_COUNTER = (By.CSS_SELECTOR, "#divResultSQL>div>div")
    SQL_RESULT = (By.CSS_SELECTOR, "#divResultSQL tbody tr td")
    SQL_NO_RESULT = (By.CSS_SELECTOR, "#divResultSQL > div")
