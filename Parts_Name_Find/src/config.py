import os

PORTAL_URL = "https://portal.garantie.in/portal"

USERNAME = "claims_admin"
PASSWORD = "Garantie@0255"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "input", "input.xlsx")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "output.xlsx")

WAIT_TIME = 20