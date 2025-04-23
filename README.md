# Keylogger

A Python-based keylogger for educational and authorized monitoring purposes.

**Disclaimer:** This keylogger is intended for use on systems you own or have explicit permission to monitor. Unauthorized use of keyloggers is illegal and unethical. I am not responsible for any misuse of this software.

## Description

This keylogger is a Python script that records keystrokes, mouse movements, clicks, and scrolls on a computer. It can also capture screenshots and record audio from the microphone. The collected data is then sent to a specified email address. This tool is designed for educational purposes, such as understanding how keyloggers work, or for authorized system monitoring (e.g., monitoring your computer for unauthorized access).

**Use this tool responsibly and ethically. Do not use it for any illegal or malicious activities.**

## Features

* **Keystroke Logging:** Records all keys pressed on the keyboard.
* **Mouse Activity Logging:** Logs mouse movements, clicks, and scroll events.
* **Screenshot Capture:** Takes screenshots of the user's screen.
* **Microphone Recording:** Records audio from the computer's microphone.
* **Email Reporting:** Sends the collected data (keystrokes, screenshots, audio) to a specified email address.
* **Cross-Platform Compatibility:** Works on Windows and Linux.
* **Error Handling:** Includes error handling for various operations.
* **Module Installation:** Attempts to automatically install missing modules.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Mangesh-Bhattacharya/Keylogger.git
    cd Keylogger
    ```

2.  **Install dependencies:** The script attempts to install missing modules, but it's recommended to create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate   # On Windows
    pip install -r requirements.txt
    ```

3.  **Configure email settings:**

    * Open the `keylogger.py` file.
    * Replace `"YOUR_USERNAME"` with your email address.
    * Replace `"YOUR_PASSWORD"` with your email password or, preferably, an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if using Gmail.
    * **Do not use your main email password directly for security reasons.**
    * If using Gmail, you might need to enable [less secure app access](https://support.google.com/accounts/answer/6010255) (not recommended) or use an App Password.  Note that Google is phasing out "less secure app access."

    ```python
    KEYLOGGER_EMAIL = "your_email@example.com"  # Replace this!
    KEYLOGGER_PASSWORD = "your_app_password"      # Replace this!
    ```

4.   **Set Reporting Interval:**
    * The `SEND_REPORT_EVERY` variable in `keylogger.py` controls how often the keylogger sends reports (in seconds). Adjust this as needed.

    ```python
    SEND_REPORT_EVERY = 60  # Time interval in seconds
    ```

## Usage

1.  **Run the script:**

    ```bash
    python3 keylogger.py
    ```

2.  **The keylogger will start recording data in the background.** Data will be sent to the configured email address at the specified interval.

## Important Considerations

* **Legal and Ethical Use:** This keylogger must only be used on systems you own or have explicit permission to monitor. Unauthorized use is illegal and unethical.
* **Email Security:** Storing your email password (or even an app password) in a script has security implications. If you intend to use this long-term, consider using more secure methods for handling credentials, such as environment variables or configuration files.
* **Antivirus Detection:** Antivirus software can detect keyloggers. If you are using this for legitimate purposes, you may need to add an exception to your antivirus.
* **Resource Usage:** Be mindful of the keylogger's impact on system resources, especially if you frequently capture screenshots or record audio.
* **Data Storage:** The script, as provided, does not store logs locally before emailing them. For long-term logging, you should add local storage.
* **Gmail App Password:** For enhanced security, it is highly recommended that you use a Gmail App Password instead of your regular Gmail password. See the Setup section for instructions.

## Dependencies

* Python 3
* `pynput`
* `pyscreenshot`
* `sounddevice`
* `email`
* `smtplib`

## Disclaimer

This software is provided for educational and authorized monitoring purposes only. The author is not responsible for any misuse of this software. Use this tool responsibly and ethically. By using this software, you agree to these terms.
