import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_claim_page(driver, claim_id):

    driver.get(
        f"https://portal.garantie.in/claims/claims/edit/{claim_id}/EWPLUS"
    )

    # Table container load hone ka wait
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "claimPartsList")
        )
    )

    # AJAX data load hone ka extra wait
    time.sleep(3)


def find_part_by_search_value(driver, search_value):

    search_value = str(search_value).strip().upper()

    time.sleep(2)

    all_rows = driver.find_elements(
        By.XPATH,
        "//table//tbody/tr"
    )

    print(f"Searching For : {search_value}")
    print(f"Total Rows Found : {len(all_rows)}")

    for row in all_rows:

        try:

            cols = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cols) < 6:
                continue

            row_text = row.text.upper()

            if search_value in row_text:

                return {
                    "Part Name": cols[0].text.strip(),
                    "Part Number": cols[1].text.strip(),
                    "Part MRP": cols[2].text.strip(),
                    "Part Status": cols[5].text.strip()
                }

        except:
            continue

    return None