# timepunch
Sample Selenium-Python time punch automation.

The repository is a proof-of-concept for learning WebDriver automation for web scraping and application testing.
In its current form, it requires a 'settings.py' file containing plain-text username and password global imported
variables. 

Using a Powershell script to activate a Selenium virtualenv and run the script, this script automates the act of
Recording Time Stamps using ADP Workforce Now. As needed, potential additions include:
  * Implementing a secured Python keyring instead of plain-text pass storage. 
  * Sending run() or kill() commands via a Twilio listener.
  * Adding more management tasks, like Time-Off requests.
  
To set up this script you will need:
  * selenium-python installed via pip.
  * geckodriver for the Firefox default WebDriver, or relevant WebDriver for your preferred browser.
  * WebDriver executables accessible by your system PATH.
  
Feel free to contact me for more detailed setup assistance. 
