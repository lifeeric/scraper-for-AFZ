import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# Create a ChromeDriver instance with Chrome options
browser = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(), options=chrome_options
)


# CSV Header
headers = [
    "name",
    "Total",
    "EGFL: Basisprämie",
    "EGFL: Umverteilungsprämie",
    "EGFL: Greening-Prämie",
    "EGFL: Erstattung nicht genutzter Mittel der Krisenreserve",
    "ELER: Agrarumwelt- und Klimaschutzmaßnahmen",
    "ELER: Ausgleichszulage benachteiligte Gebiete",
    "ELER: Basisdienstleistungen und Dorferneuerung",
    "EGFL: Junglandwirteprämie",
    "ELER: Ökologischer Landbau",
    "ELER: Natur- und Gewässerschutz",
    "ELER: Tierschutzmaßnahmen",
    "ELER: LEADER",
    "ELER: Investitionen in materielle Vermögenswerte",
    "ELER: Zusammenarbeit",
]


def scrape_data(zipcode):
    # Open the desired website
    browser.get("https://www.agrar-fischerei-zahlungen.de/Suche")

    try:
        # Locate the input field using its CSS class name
        zip_code = browser.find_element(By.CLASS_NAME, "textPlz")

        # Input data into the field
        zip_code.send_keys(zipcode)

        # Locate and click the submit button
        browser.find_element(By.XPATH, "//input[@type='submit']").click()

        # render 50 rows per page
        dropdown = browser.find_element(By.CLASS_NAME, "listNavSelect")
        dropdown.send_keys("50")
        total_pages, pages = pagination(browser)

        for pn in range(1, int(total_pages) + 1):
            _, pages = pagination(browser)

            # Scrolls up to the top of the page
            browser.execute_script("scrollBy(0,0)")
            scroll_up = browser.find_element(By.TAG_NAME, "html")
            scroll_up.send_keys(Keys.HOME)

            pages.clear()
            pages.send_keys(pn)
            pages.send_keys(Keys.ENTER)

            # Get all the links and iterate over it
            all_elements = browser.find_elements(By.CLASS_NAME, "linkBeg")
            for i, _ in enumerate(all_elements):
                browser.find_elements(By.CLASS_NAME, "linkBeg")[i].click()

                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//p[@style="margin-top: 2em; padding-bottom: 2em;"]',
                        )
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

                write_to_file(
                    {"name": header, "Total": total_price[0].text, **name_price}
                )
                browser.back()

    except Exception as e:
        print("An error occurred:", e)


def pagination(browser):
    # Pagination
    list_nav_right = browser.find_element(By.ID, "listNavRight")
    pages = list_nav_right.find_element(By.CLASS_NAME, "listNavTxtPage")

    total_pages = re.findall("\d+", list_nav_right.text)[0]
    return total_pages, pages


def write_to_file(data):
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        try:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerow(data)
        except:
            print("[❌] ERROR_INCORRECT_DATA")
            print(f"[HEADER] {headers}")
            print(f"[ROW] {data}")


def main():
    with open(
        "georef-germany-postleitzahl.json",
        "r",
        newline="",
    ) as f:
        data = json.load(f)

        for i, row in enumerate(data):
            scrape_data(row["name"])
            printProgressBar(
                i + 1,
                len(data),
                prefix="Progress:",
                suffix="Complete",
                length=70,
            )

    browser.quit()


# Print iterations progress
def printProgressBar(
    iteration, total, prefix="", suffix="", decimals=1, length=100, fill="█"
):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    main()
