############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLUB="reading"
CLUB="laneend"
CLUB="bracknellforest"
CLUB="ascot"
CLUB="basingstoke"
CLUB="newbury"

def startBrowser(url):
    print("URL:", url)
    global driver
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "results"}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=r"testing/chromedriver_macos", chrome_options=chromeOptions)
    r = requests.get(url, verify=False)
    if r.status_code == 404:
        raise Exception("Page not found: have you switched on automatic testing?")
    driver.get(url)
    #WebDriverWait(driver, 5)
        
def stopBrowser():
    global driver
    driver.quit()

def clickElement(element):
    global driver
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    
def clickXPath(xpath):
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
    clickElement(element)
        
SEARCH_TEXT = "tables"
driver = None

try:
    url = f"http://www.bridgewebs.com/{CLUB}/"
    startBrowser(f"{url}")
    element = driver.find_element(By.PARTIAL_LINK_TEXT, 'Result')
    clickElement(element)
    
    elements = driver.find_elements(By.XPATH, f'//td[contains(text(),"{SEARCH_TEXT}")]')
    n = len(elements)
    for i in range(n):
        try:
            elements = driver.find_elements(By.XPATH, f'//td[contains(text(),"{SEARCH_TEXT}")]')
            element = elements[i]
            clickElement(element)
            clickXPath('//td/div[contains(text(),"Hands")]')
            clickXPath('//*[@id="downloadaspbn"]')
        except Exception as e:
            element = driver.find_element(By.CSS_SELECTOR, '#result_title')
            print(f"Hands tab missing: {element.text}")
        finally:
            driver.execute_script("window.history.go(-1)")
    stopBrowser()
except Exception as e:
    print(e)

print("Completed Tests")


