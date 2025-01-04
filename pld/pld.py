from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import pickle
import time
import re
import tqdm
import pathlib
import datetime

# TODO: use cookiejar to store cookies in netscape format rather than pickle
from http.cookiejar import MozillaCookieJar, Cookie


def newDriver(argd):
    # options = webdriver.ChromeOptions()
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = "normal"
    if argd.get("output"):
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        # set the download path
        options.set_preference("browser.download.dir", str(argd["output"].absolute()))
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Firefox(options=options)
    return driver


def main(argd):
    if argd.get("action") is None:
        raise ValueError("Please specify an action (use: pld --help)")
    if argd.get("action") == "download":
        download(argd)
    elif argd.get("action") == "login":
        authenticate(argd)
    elif argd.get("action") == "logout":
        delete_cookies(argd)
    else:
        raise ValueError("Unknown action: {}".format(argd.get("action")))


def authenticate(argd):
    driver = newDriver(argd)
    login_flow(argd, driver)
    save_cookies(argd, driver)
    driver.quit()


def delete_cookies(argd):
    path = pathlib.Path(argd["cookies"])
    if path.is_file():
        path.unlink()
    else:
        raise ValueError(
            f"{argd['cookies']} does not exist or is not a file skipping deletion"
        )


def login_flow(argd, driver):
    driver.get("https://patreon.com/login")
    time.sleep(35)
    cookies = driver.get_cookies()


def load_cookies(argd, driver):
    """Load cookies from file."""
    driver.get("https://patreon.com")
    cookies = pickle.load(open(argd["cookies"], "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()


def save_cookies(argd, driver):
    """Save cookies to file."""
    pickle.dump(driver.get_cookies(), open(argd["cookies"], "wb"))


def inject_cookies(argd, driver, cookies):
    driver.get("https://patreon.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()


def login(argd, driver):
    driver.get("https://patreon.com/login")


def download(argd):
    path = pathlib.Path(argd["output"])
    path.mkdir(exist_ok=True, parents=True)
    driver = newDriver(argd)
    cookies = load_cookies(argd, driver)
    include_regex = re.compile("|".join(argd["include"]))
    exclude_regex = re.compile("|".join(argd["exclude"]))
    # print("include regex: ", include_regex)
    # print("exclude regex: ", exclude_regex)

    for page in argd.get("pages"):
        driver.get(page)
        time.sleep(3) #TODO: add a full WebDriverWait
        elems = driver.find_elements(by=By.TAG_NAME, value="a")
        # print(f"Found {len(elems)} elements on page {page}")
        links = []
        for elem in elems:
            try:
                link = elem.get_attribute("href")
                if link:
                    links.append(link)
            except StaleElementReferenceException:
                print(f"Stale element reference: `{elem}`. The page has changed and the reference to the link is no longer valid since first scan.")
                pass
        if len(links) == 0:
            print(f"No links found on page {page}")
            continue
        # use regex filters to remove unwanted links
        files = [
            link
            for link in links
            if include_regex.match(link) and not exclude_regex.match(link)
        ]
        print(f"Found {len(files)} files on page {page}")
        timeout = 120
        for file in (pbar := tqdm.tqdm(files)):
            download_file(argd, driver, pbar, file)
    driver.quit()


def download_file(argd, driver, pbar, file, attempt=0):
    dir = pathlib.Path(argd["output"])
    # count the number of NON-temp files in output directory
    original_files = get_current_files(argd)
    start = datetime.datetime.utcnow()
    pbar.set_description(file)
    # open file in new tab
    driver.execute_script(f"window.open('{file}', '_blank');")
    time.sleep(1)
    while not is_download_finished(argd, original_files):
        time.sleep(1)
        if datetime.datetime.utcnow() - start > datetime.timedelta(
            seconds=argd["timeout"]
        ):
            print(f"Timed out downloading file (attempt {attempt}): {file}")
            new_files = get_current_files(argd) - original_files
            delete_temp_files(argd)
            delete_files(argd, files=new_files)
            if argd["max_attempts"] == -1:
                download_file(argd, driver, pbar, file, attempt + 1)
            elif attempt < argd["max_attempts"]:
                download_file(argd, driver, pbar, file, attempt + 1)
            else:
                print(f"Failed to download file after {attempt} attempts: {file}")
                return

def get_current_files(argd) -> set[pathlib.Path]:
    """Get current files in output directory that are NOT temp files."""
    dir = pathlib.Path(argd["output"])
    return set(dir.glob("*.*")) - (set(dir.glob("*.part")) | set(dir.glob("*.crdownload")))

def delete_temp_files(argd):
    dir = pathlib.Path(argd["output"])
    for file in dir.glob("*.part"):
        file.unlink()
    for file in dir.glob("*.crdownload"):
        file.unlink()

def delete_files(argd, files: set):
    dir = pathlib.Path(argd["output"])
    for file in files:
        file.unlink()

def is_download_finished(argd, original_files: set):
    """Check if download is finished in output folder.

    This is an incredibly hacky way to check if the download is finished.
    We cant ask the browser, so we must check the contents of the output dir.
    The caveat being that this only works if this is the only process that
    modifies the directory.
    """
    dir = pathlib.Path(argd["output"])
    firefox_temp_file = sorted(dir.glob("*.part"))
    chrome_temp_file = sorted(dir.glob("*.crdownload"))
    downloaded_files = sorted(dir.glob("*.*"))
    new_files = get_current_files(argd) - original_files
    if (
        (len(firefox_temp_file) == 0)
        and (len(chrome_temp_file) == 0)
        and (len(downloaded_files) > 0)
        and (len(new_files) == 1)
    ):
        return True
    else:
        return False
