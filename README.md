# Microsoft 365 MFA Bombing Script

This Python script automates the authentication process for Microsoft 365 by using the device code flow and Selenium for automated login.
It keeps bombing the user with MFA requests and stores the access_token once the MFA was approved.

## Usage

### Installation

1. Clone this repository.

2. Install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
    ```

### Running the Script
To run the script, execute the following command:

```bash

python m365-fatigue.py --user <username> [--password <password>] [--interval <seconds> (default: 60)]
````

Replace <username> with your Microsoft 365 username. The password can be provided directly after the --password flag, or the script will prompt for it if not supplied.

The --interval flag allows you to set the polling interval in seconds (default is 60 seconds).

# TODO
The fireprox implementation is yet not finished and may or may not be implemented in the future...

# Notes
This script utilizes Selenium, which requires a compatible WebDriver (in this case, Chrome WebDriver... but you can change it towards something else if you need to).

# Credits & Acknowledgements
Heavily inspired by the awesome work of Steve Borosh ([@rvrsh3ll](https://github.com/rvrsh3ll)) and Beau Bullock ([@dafthack](https://github.com/dafthack)). Could not have made this without their work.

# License
This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE).

