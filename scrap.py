from selenium import webdriver
from pathlib import Path

import os
import os.path
import time
import code_fetcher

DOWNLOAD_DIR = '/data'

REPORTS_FILES = {
    'sales': {
        'file_name': 'SteamSales_2020-04-30_to_2021-05-06',
        'url': 'https://partner.steampowered.com/report_csv.php?file=SteamSales_2020-04-30_to_2021-05-06&params=query=QueryPackageSalesForCSV%5EdateStart=2020-04-30%5EdateEnd=2021-05-06%5EHasDivisions=0%5Einterpreter=PartnerSalesReportInterpreter'
    },
    'wishlists': {
        'file_name': 'SteamWishlists_1239430_2020-02-21_to_2021-05-10',
        'url': 'https://partner.steampowered.com/report_csv.php?file=SteamWishlists_1239430_2020-02-21_to_2021-05-10&params=query=QueryWishlistActionsForCSV%5EappID=1239430%5EdateStart=2020-02-21%5EdateEnd=2021-05-10%5Einterpreter=WishlistReportInterpreter'
    }
}

def get_latest(report):
    if (report in REPORTS_FILES):
        file_name = f"{REPORTS_FILES[report]['file_name']}.csv"
        file_path = f"{DOWNLOAD_DIR}/{file_name}"
        if (os.path.isfile(file_path)):
            try:
                modified_time = int(os.path.getmtime(file_path))
                print(f"modified_time={modified_time}")
                current_time = int(time.time())
                print(f"current_time={current_time}")

                if (current_time - modified_time < 15 * 60):
                    return Path(file_path).read_text()

                else:
                    scrap_latest()
                    return get_latest(report)

            except OSError as exception:
                print(exception)
        else:
            scrap_latest()
            return get_latest(report)


def scrap_latest():
    driver = get_driver()
    print('Driver inited')

    init_url = 'https://partner.steampowered.com'
    driver.get(init_url)
    print('Login opened')

    login(driver)
    print('Loging in..')

    driver.save_screenshot('scripts/after_login.png')

    time.sleep(5)

    print('Fetching code from email..')
    code = code_fetcher.get_code_from_email()
    print('Code fetched: ' + code)

    driver.save_screenshot('scripts/before_authcode.png')
    send_auth_code(driver, code)
    print('Code send..')
    time.sleep(5)
    driver.save_screenshot('scripts/after_authcode.png')

    download_reports(driver)
    expected_files = [(v['file_name']) for k,v in REPORTS_FILES.items()]
    download_wait(DOWNLOAD_DIR, 60, expected_files)

    driver.quit()

def download_reports(driver):
    for key, value in REPORTS_FILES.items():
        print(f"Downloading {key} report to {value['file_name']}")
        driver.get(value['url'])

def download_wait(directory, timeout, expected_files):
    seconds = 0
    is_waiting = True
    while is_waiting and seconds < timeout:
        time.sleep(1)
        is_waiting = False

        files = os.listdir(directory)

        intersection = [value for value in expected_files if value in files]
        if len(intersection) == len(expected_files):
            is_waiting = False

        for fname in files:
            if fname.endswith('.crdownload'):
                is_waiting = True

        seconds += 1
    return seconds    

def send_auth_code(driver, code):
    auth_code_input = driver.find_element_by_id('authcode')
    auth_code_input.send_keys(code)
    driver.find_element_by_css_selector('#auth_buttonset_entercode > div.auth_button.leftbtn').click()

def login(driver):
    with open("./config.json", "r") as configfile:
        config = json.load(configfile)['steam']

    username_input = driver.find_element_by_id('username')
    username_input.send_keys(config['login'])
    password_input = driver.find_element_by_id('password')
    password_input.send_keys(config['password'])
    driver.find_element_by_id("login_btn_signin").click()

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    preferences = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    chrome_options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    return driver

if __name__ == "__main__":
    main()