from selenium import webdriver
import pickle
import time
# TODO: use cookiejar to store cookies in netscape format rather than pickle
from http.cookiejar import MozillaCookieJar, Cookie


def newDriver(argd):
    #options = webdriver.ChromeOptions()
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'normal'
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Firefox(options=options)
    return driver

def main(argd):
    if argd.get("action") is None:
        raise ValueError("Please specify an action (use: pld --help)")
    if argd.get("action") == "download":
        download(argd)
    elif argd.get("action") == "login":
        authenticate(argd)
    else:
        raise ValueError("Unknown action: {}".format(argd.get("action")))

def authenticate(argd):
    driver = newDriver(argd)
    login_flow(argd, driver)
    save_cookies(argd, driver)
    driver.quit()

def login_flow(argd, driver):
    driver.get("https://www.patreon.com/login")
    time.sleep(35)
    cookies = driver.get_cookies()
    print(cookies)

def load_cookies(argd, driver):
    """Load cookies from file."""
    cookies = pickle.load(open(argd["cookies"], "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def save_cookies(argd, driver):
    """Save cookies to file."""
    pickle.dump(driver.get_cookies(), open(argd["cookies"], "wb"))

def inject_cookies(argd, driver, cookies):
    driver.get("https://www.patreon.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

def login(argd, driver):
    driver.get("https://www.patreon.com/login")

def download(argd):
    driver = newDriver(argd)
    cookies = load_cookies(argd, driver)
    #inject_cookies(argd, driver, cookies)

    for page in argd.get("pages"):
        driver.get(page)
        time.sleep(30)
    driver.quit()
