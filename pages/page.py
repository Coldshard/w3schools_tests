from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from .locators import PageLocators


class Page(object):
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        """opens browser"""
        self.browser.get(self.url)

    def set_sql(self, code):
        self.browser.execute_script(f'window.editor.setValue("{code}");')

    def run_sql(self):
        button = self.browser.find_element(*PageLocators.RUN_BUTTON)
        button.click()

    def check_result_count(self, expected):
        link = self.browser.find_element(*PageLocators.SQL_COUNTER)
        count = int(link.text.split(': ')[1])
        assert count == expected, f'count not valid: expected {expected} got {count}'

    def check_no_results(self):
        result = self.browser.find_element(*PageLocators.SQL_NO_RESULT)
        assert result.text == 'No result.', 'result error: expected no results, got rows'

    def find_next_sibling_text_by_text(self, text):
        value = self.browser.find_element_by_xpath(f' //*[contains(text(), "{text}")]/following-sibling::td')
        return value.text

    def compare_address_by_name(self, name, address):
        value = self.find_next_sibling_text_by_text(name)
        assert value == address, f'address not valid: expected {address} got {value}'

    def get_row_result(self):
        values = [val.text for val in self.browser.find_elements(*PageLocators.SQL_RESULT)]
        return values

    def compare_row_results(self, expected):
        values = [val.text for val in self.browser.find_elements(*PageLocators.SQL_RESULT)]
        for i, value in enumerate(values):
            assert value == expected[i], f'incorrect value: expected "{expected[i]}" got "{value}"'

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_alert_present(self, timeout=4):
        try:
            alert = self.browser.switch_to.alert
            print(f'ERROR detected: {alert.text}')
        except NoAlertPresentException:
            return True
        return False

    def should_be_run_button(self):
        assert self.is_element_present(*PageLocators.RUN_BUTTON), "No RUN button"

    def should_be_code_block(self):
        assert self.is_element_present(*PageLocators.CODE_BLOCK), "No code block"

    def execute_sql(self, sql):
        self.should_be_code_block()
        self.set_sql(sql)
        self.should_be_run_button()
        self.run_sql()
        self.is_not_alert_present()
