from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest
import time


"""
    Does the login/register pages load the forms expected?
"""
class Test_Login_And_Register_Page(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    # Function returns True/False is element exists
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    # Can the login page load?
    def test_connect_to_webpage(self):
        self.driver.get("https://src-demo-1.herokuapp.com/")

    # Does the load screen take the user to the Login page?
    def test_login_page_rendered(self):
        self.driver.get("https://src-demo-1.herokuapp.com/")
        self.assertIn("Login", self.driver.title)
        self.assertEquals(self.driver.current_url, "https://src-demo-1.herokuapp.com/login/?next=/")

    # Does login form exist?
    def test_login_form(self):
        self.driver.get("https://src-demo-1.herokuapp.com/")
        self.assertTrue(self.is_element_present(By.NAME, "username"))
        self.assertTrue(self.is_element_present(By.NAME, "password"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Sign Up"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Reset Password"))

    # Does the register button take the user to the Register page?
    def test_register_link_and_page_rendered(self):
        self.driver.get("https://src-demo-1.herokuapp.com/")
        self.driver.find_element_by_link_text("Sign Up").click()
        self.assertIn("Register", self.driver.title)
        self.assertEquals(self.driver.current_url, "https://src-demo-1.herokuapp.com/register/")

    # Does register form exist?
    def test_register_form(self):
        self.driver.get("https://src-demo-1.herokuapp.com/register/")
        self.assertTrue(self.is_element_present(By.NAME, "username"))
        self.assertTrue(self.is_element_present(By.NAME, "first_name"))
        self.assertTrue(self.is_element_present(By.NAME, "last_name"))
        self.assertTrue(self.is_element_present(By.NAME, "email"))
        self.assertTrue(self.is_element_present(By.NAME, "password1"))
        self.assertTrue(self.is_element_present(By.NAME, "password2"))
        self.assertTrue(self.is_element_present(By.NAME, "submit"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Login"))

    # Does the login button take the user to the Login page?
    def test_register_page_rendered(self):
        self.driver.get("https://src-demo-1.herokuapp.com/register/")
        self.driver.find_element_by_link_text("Login").click()
        self.assertIn("Login", self.driver.title)
        self.assertEquals(self.driver.current_url, "https://src-demo-1.herokuapp.com/login/")

"""
    Does the admin view show all admin pages as expected
"""
class Test_Admin_Views(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    # Function returns True/False is element exists
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    # Automatically logs in Admin user
    def log_in_admin(self, driver):
        driver.get("https://src-demo-1.herokuapp.com/")
        username = driver.find_element_by_name("username")
        username.send_keys("admin")
        password = driver.find_element_by_name("password")
        password.send_keys("admin")
        driver.find_element_by_name("submit").click()

    # Does an Admin user log into the admin dashboard?
    def test_login_admin_user(self):
        self.log_in_admin(self.driver)
        self.assertIn("Dashboard", self.driver.title)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Dashboard"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "All Agents"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Agent Activity"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "My Settings"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Logout"))
        self.assertFalse(self.is_element_present(By.ID, "agent-dashboard"))

    # Does the agent list page render?
    def test_agent_list_page_rendered(self):
        self.log_in_admin(self.driver)
        self.driver.find_element_by_link_text("All Agents").click()
        self.assertIn("Agent List", self.driver.title)
        self.assertEquals(self.driver.current_url, "https://src-demo-1.herokuapp.com/agent_list/")
        self.assertTrue(self.is_element_present(By.ID, "list_of_agents_table"))

    # Does the agent list page render?
    def test_agent_list_table_function(self):
        self.log_in_admin(self.driver)
        self.driver.find_element_by_link_text("All Agents").click()
        time.sleep(1)
        before_filter = len(self.driver.find_elements_by_link_text("View"))
        search = self.driver.find_element_by_xpath("//input[@data-index='0'][@type='text']")
        search.send_keys("Test2")
        time.sleep(1)
        after_filter = len(self.driver.find_elements_by_link_text("View"))
        self.assertNotEqual(before_filter, after_filter)

    # Can the Admin access an agent dashboard?
    def test_admin_get_agent_dashboard(self):
        self.log_in_admin(self.driver)
        self.driver.find_element_by_link_text("All Agents").click()
        time.sleep(1)
        search = self.driver.find_element_by_xpath("//input[@data-index='0'][@type='text']")
        search.send_keys("Test2")
        self.driver.find_element_by_link_text("View").click()
        self.assertIn("User Page", self.driver.title)
        self.assertIn("https://src-demo-1.herokuapp.com/agent/", self.driver.current_url)
        self.assertTrue(self.is_element_present(By.ID, "agent-dashboard"))

"""
    Does the admin view show all admin pages as expected
"""
class Test_Agent_Views(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    # Function returns True/False is element exists
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    # Automatically logs in Admin user
    def log_in_admin(self, driver):
        driver.get("https://src-demo-1.herokuapp.com/")
        username = driver.find_element_by_name("username")
        username.send_keys("Test1")
        password = driver.find_element_by_name("password")
        password.send_keys("Happy123+")
        driver.find_element_by_name("submit").click()

    # Does an Admin user log into the admin dashboard?
    def test_login_admin_user(self):
        self.log_in_admin(self.driver)
        self.assertIn("User Page", self.driver.title)
        self.assertIn("https://src-demo-1.herokuapp.com/agent/", self.driver.current_url)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Dashboard"))
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "All Agents"))
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "Agent Activity"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "My Settings"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Logout"))
        self.assertFalse(self.is_element_present(By.ID, "agent-dashboard"))

"""
    Does the admin view show all admin pages as expected
"""
class Test_All_User_Views(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    # Function returns True/False is element exists
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    # Automatically logs in Admin user
    def log_in_admin(self, driver):
        driver.get("https://src-demo-1.herokuapp.com/")
        username = driver.find_element_by_name("username")
        username.send_keys("admin")
        password = driver.find_element_by_name("password")
        password.send_keys("admin")
        driver.find_element_by_name("submit").click()

    # Check if class exists
    def class_exist(self, element, class_name):
        if class_name in element.get_attribute('class').split():
            return True
        else:
            return False

    # Toggle Table Display
    def toggle_table(self, element, text):
        self.assertTrue(self.is_element_present(By.ID, element))
        self.assertFalse(self.class_exist(self.driver.find_element_by_id(element), "in"))
        self.driver.find_element_by_xpath('//button[text()="' + text + '"]').click()
        time.sleep(1)
        self.assertTrue(self.class_exist(self.driver.find_element_by_id(element), "in"))
        self.driver.find_element_by_xpath('//button[text()="' + text + '"]').click()
        time.sleep(1)
        self.assertFalse(self.class_exist(self.driver.find_element_by_id(element), "in"))

    # Toggle Table Display
    def change_settings(self, driver, lower_val, upper_val):
        driver.find_element_by_link_text("My Settings").click()
        lower = driver.find_element_by_name("call_lower_limit")
        upper = driver.find_element_by_name("call_upper_limit")
        lower.clear()
        upper.clear()
        lower.send_keys(lower_val)
        upper.send_keys(upper_val)
        driver.find_element_by_name("Update Information").click()
        driver.find_element_by_link_text("Dashboard").click()

    # Does the dashboard load all elements expected?
    def test_login_admin_user(self):
        self.log_in_admin(self.driver)

        # Upper banner
        self.assertTrue(self.is_element_present(By.ID, "total-calls"))
        self.assertTrue(self.is_element_present(By.ID, "calls-outside-limit"))
        self.assertTrue(self.is_element_present(By.ID, "average-call-length"))
        self.assertTrue(self.is_element_present(By.ID, "select-date-range"))

        # Table objects and functionality
        self.toggle_table("call_outcome_table_row", "Call Outcome Table")
        self.toggle_table("services_table_row", "Services Table")
        self.toggle_table("brands_table_row", "Brands Table")
        self.toggle_table("criteria_contact_table_row", "Report Table")

        # Chart objects
        self.assertTrue(self.is_element_present(By.ID, "brands-chart"))
        self.assertTrue(self.is_element_present(By.ID, "call-outcome-chart"))
        self.assertTrue(self.is_element_present(By.ID, "services-chart"))

    # Can agent settings page render
    def test_agent_settings(self):
        self.log_in_admin(self.driver)
        self.driver.find_element_by_link_text("My Settings").click()
        self.assertIn("My Settings", self.driver.title)
        self.assertIn(self.driver.current_url, "https://src-demo-1.herokuapp.com/agent_settings/")
        self.assertTrue(self.is_element_present(By.NAME, "profile_pic"))
        self.assertTrue(self.is_element_present(By.NAME, "brands"))
        self.assertTrue(self.is_element_present(By.NAME, "teams"))
        self.assertTrue(self.is_element_present(By.NAME, "call_lower_limit"))
        self.assertTrue(self.is_element_present(By.NAME, "call_upper_limit"))
        self.assertTrue(self.is_element_present(By.NAME, "Update Information"))

    # Does an agent changing their settings change the returned data
    def test_agent_changing_their_settings_and_altering_returned_data(self):
        self.log_in_admin(self.driver)
        self.change_settings(self.driver, "00:10:00", "00:40:00")
        first_HTML = self.driver.find_element_by_id("total-calls")
        self.change_settings(self.driver, "00:20:00", "00:30:00")
        second_HTML = self.driver.find_element_by_id("total-calls")
        self.assertNotEqual(first_HTML, second_HTML)

    # Does the agent successfully log out
    def test_agent_logout(self):
        self.log_in_admin(self.driver)
        self.driver.find_element_by_link_text("Logout").click()
        self.assertIn("Login", self.driver.title)
        self.assertEquals(self.driver.current_url, "https://src-demo-1.herokuapp.com/login/")
        

if __name__ == "__main__":
    unittest.main()
