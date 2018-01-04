"""
@name: timepunch.main
@author: frndlytm

@description:
    Uses Selenium to connect to ADP and clock in.
"""
from time import sleep
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import settings

class ADPBot:
    name = "ADPBot"
    root = "https://workforcenow.adp.com/public/index.htm"

    def __init__(self, username, password, driver=webdriver.Firefox()):
        self.driver = driver
        self.username = username
        self.password = password



    def get_current_url(self):
        """
        Return the current_url without exposing
        the driver.
        """
        return self.driver.current_url


    def login(self):
        """
        Login to ADP Workforce now by looking
        for the input fields, and sending
        a username and password.
        """
        print("[...] Logging in...")
        try:
            self.driver.get(self.root)
            assert "Login" in self.driver.title
            print('\t[+] Request to {} successful. Logging in...'.format(self.name))
            user_field = self.driver.find_element_by_xpath("//input[@name='USER']")
            pass_field = self.driver.find_element_by_xpath("//input[@name='PASSWORD']")
            user_field.send_keys(self.username)
            pass_field.send_keys(self.password)
            pass_field.send_keys(Keys.RETURN)
            assert 'ADP' in self.driver.title
            print('\t[+] Passed Login assertion. Login successful.')
        except AssertionError as a:
            print('\t[-] {} : Login failed.'.format(a))


    def go_to_etime(self):
        """
        Navigate to the eTIME gateway by
        clicking the Quick Link.
        """
        try:
            print('\n[...] Going to eTIME...')
            click_link = WebDriverWait(self.driver, 300).until( # Link is clickable, OR 5 minutes
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Enterprise eTIME Gateway']"))
            )
            sleep(10) # seconds. Because the link is clickable, but not really?
            click_link.send_keys(Keys.CONTROL + Keys.RETURN)
            sleep(5)
            # self.open_link_in_new_window(click_link.get_attribute('href'))
            self.driver.switch_to_window(self.driver.window_handles[-1])
            assert 'Attendance' in self.driver.title
            print('\t[+] Passed Attendance assertion. Continuing setup...')
            print('\t\t'+self.driver.current_url)
        except AssertionError as a:
            print('\t[-] {} eTIME failed.'.format(a))


    def setup_etime(self):
        """
        If setup is needed before clocking in,
        select the HTML option to make accessing
        elements easier.
        """
        assert 'Welcome' in self.driver.current_url
        print('\n[...] Setting up eTIME for HTML...')
        try:
            option = WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@value='HTML' and @type='radio']")
                )
            )
            submit = (
                self
                .driver
                .find_element_by_xpath("//input[@value='Submit' and @type='submit']")
            )
            option.click()
            submit.click()
            print('\t[+] Setup successful. Continuing to clock in...')
        except exceptions.ElementNotVisibleException as e:
            print('\t[-] {} Setup unsuccessful.'.format(e))


    def clock_in(self):
        """
        Assuming we've passed setup, change to
        'contentPane' and click the Time Punch
        button.
        """
        print('\n[...] Clocking in...')
        try:
            frame = self.driver.find_element_by_xpath("//iframe[@id='contentPane']")
            self.driver.switch_to_frame(frame)
            print('\t[+] Switched to contentPane')
            button = self.driver.find_element_by_xpath("//a[text()='Record Time Stamp']")
            button.click()
            print('\t[+] Clock in successful.')
            print('\t[...] Terminating browser session.')
            self.driver.quit()
        except exceptions.ElementNotVisibleException as e:
            print('\t[-] {} Clock in failed.'.format(e))




if __name__ == '__main__':
    #
    # Log in to ADP Workforce Now.
    #
    bot = ADPBot(settings.UNAME, settings.PASS)
    bot.login()
    sleep(5)
    bot.go_to_etime()
    sleep(5)
    if 'Welcome' in bot.get_current_url():
        bot.setup_etime()
        sleep(5)
    bot.clock_in()
