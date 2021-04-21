from .pages.page import Page
import pytest
from time import sleep

page_link = 'https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all'
customer_name = 'Giovanni Rovelli'
customer_address = 'Via Ludovico il Moro 22'
customer_city = 'London'
expected_customers = 6
data_to_add = {
    'CustomerName': 'Boy who lived',
    'ContactName': 'Harry Potter',
    'Address': '4 Privet Drive',
    'City': 'Little Whinging',
    'PostalCode': '111',
    'Country': 'Great Britain'
}
default_customers_count = 91


@pytest.mark.sql
class TestSqlQueries(object):
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        '''general setup for all tests'''
        self.link = page_link
        self.browser = browser

    @pytest.mark.t1
    def test_customer_have_valid_address(self, browser, contact=customer_name, address=customer_address):
        '''test 1: check address by customer name'''
        page = Page(browser, self.link)
        page.open()
        page.execute_sql('SELECT * FROM Customers')
        page.compare_address_by_name(contact, address)

    @pytest.mark.t2
    def test_city_have_valid_customers_count(self, browser, city=customer_city, count=expected_customers):
        '''test 2: check customers count by city'''
        page = Page(browser, self.link)
        page.open()
        page.execute_sql(f"SELECT * FROM Customers WHERE City = '{city}'")
        page.check_result_count(count)

    @pytest.mark.t3
    def test_add_customer_data_success(self, browser, data=data_to_add):
        '''test 3: add new customer'''
        page = Page(browser, self.link)
        page.open()
        page.execute_sql('SELECT * FROM Customers')
        page.check_result_count(default_customers_count)
        keys, values = zip(*[(k, repr(v)) for k, v in data.items()])
        page.execute_sql(f'INSERT INTO Customers ({", ".join(keys)}) VALUES ({", ".join(values)})')
        page.execute_sql('SELECT * FROM Customers')
        page.check_result_count(default_customers_count+1)

    @pytest.mark.t4
    def test_update_customer_row_success(self, browser, data=data_to_add):
        '''test 4: update customer data'''
        page = Page(browser, self.link)
        page.open()
        data_items = [k + " = " + repr(v) for k, v in data_to_add.items()]
        data_values = [val for val in data_to_add.values()]
        page.execute_sql(f'UPDATE Customers SET {", ".join(data_items)} WHERE CustomerID = 1')
        sleep(1)
        page.execute_sql('SELECT * FROM Customers WHERE CustomerID=1')
        page.compare_row_results(['1']+data_values)

    @pytest.mark.t5
    def test_no_duplicates_in_customers(self, browser):
        '''test 5: check if Customers table have no duplicates by address'''
        page = Page(browser, self.link)
        page.open()
        page.execute_sql('SELECT COUNT(*) FROM Customers GROUP BY Address HAVING COUNT(*) > 1')
        sleep(1)
        page.check_no_results()
