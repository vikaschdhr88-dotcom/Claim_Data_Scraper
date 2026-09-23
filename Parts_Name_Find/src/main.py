import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import *

from login import login

from claims import (
    open_claim_page,
    find_part_by_search_value
)

from excel_handler import (
    read_input,
    save_output
)

from logger import logger


def create_driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    return driver


def main():

    os.makedirs("output", exist_ok=True)

    driver = create_driver()

    output_records = []

    try:

        logger.info("Starting Login")

        login(
            driver,
            PORTAL_URL,
            USERNAME,
            PASSWORD
        )

        time.sleep(3)

        logger.info("Login Successful")

        df = read_input(INPUT_FILE)

        df.columns = df.columns.str.strip()

        print("Excel Columns Found:")
        print(df.columns.tolist())

        total = len(df)

        print(f"Total Records : {total}")

        for index, row in df.iterrows():

            claim_id = str(
                row["Claim ID"]
            ).strip()

            search_value = str(
                row["Search Value"]
            ).strip()

            print(
                f"\nProcessing "
                f"{index + 1}/{total}"
            )

            print(f"Claim ID : {claim_id}")
            print(f"Search Value : {search_value}")

            try:

                open_claim_page(
                    driver,
                    claim_id
                )

                part = find_part_by_search_value(
                    driver,
                    search_value
                )

                if part:

                    output_records.append({

                        "Claim ID":
                        claim_id,

                        "Search Value":
                        search_value,

                        "Part Name":
                        part["Part Name"],

                        "Part Number":
                        part["Part Number"],

                        "Part MRP":
                        part["Part MRP"],

                        "Part Status":
                        part["Part Status"]
                    })

                else:

                    output_records.append({

                        "Claim ID":
                        claim_id,

                        "Search Value":
                        search_value,

                        "Part Name":
                        "",

                        "Part Number":
                        "",

                        "Part MRP":
                        "",

                        "Part Status":
                        "SEARCH VALUE NOT FOUND"
                    })

                logger.info(
                    f"Completed : {claim_id}"
                )

            except Exception as e:

                logger.error(str(e))

                output_records.append({

                    "Claim ID":
                    claim_id,

                    "Search Value":
                    search_value,

                    "Part Name":
                    "",

                    "Part Number":
                    "",

                    "Part MRP":
                    "",

                    "Part Status":
                    f"ERROR : {str(e)}"
                })

        save_output(
            output_records,
            OUTPUT_FILE
        )

        print("\nOutput File Saved")

    finally:

        driver.quit()

        print("\nProcess Completed")


if __name__ == "__main__":
    main()