import time
import csv
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()


def main():
    # Open the desired website
    browser.get("https://www.agrar-fischerei-zahlungen.de/Suche")

    try:
        # Locate the input field using its CSS class name
        zip_code = browser.find_element(By.CLASS_NAME, "textPlz")

        # Input data into the field
        zip_code.send_keys("84076")

        # Locate and click the submit button
        browser.find_element(By.XPATH, "//input[@type='submit']").click()

        all_elements = browser.find_elements(By.CLASS_NAME, "linkBeg")

        for i, _ in enumerate(all_elements):
            browser.find_elements(By.CLASS_NAME, "linkBeg")[i].click()

            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//p[@style="margin-top: 2em; padding-bottom: 2em;"]')
                )
            )

            # Header
            header = browser.find_element(By.TAG_NAME, "h2").text
            names = browser.find_elements(By.TAG_NAME, "h3")
            prices = browser.find_elements(
                By.XPATH, '//p[@style="margin-bottom: 0; text-align: right;"]'
            )
            total_price = browser.find_element(
                By.XPATH, '//p[@style="margin-top: 2em; padding-bottom: 2em;"]'
            ).find_elements(By.CLASS_NAME, "betrag")

            name_price = {}
            for j in range(len(names)):
                name_price[names[j].text] = prices[j].text

            write_to_file({"name": header, "Total": total_price[0].text, **name_price})
            browser.back()

        time.sleep(5)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser window
        browser.quit()


def write_to_file(data):
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)


if __name__ == "__main__":
    main()
