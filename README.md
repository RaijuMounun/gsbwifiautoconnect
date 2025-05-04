# GSBWifiAutoConnect

GSBWifiAutoConnect is a Python application that automates the process of connecting to the Wi-Fi network provided by the Ministry of Youth and Sports (Gençlik ve Spor Bakanlığı) for students residing in their dormitories. The Wi-Fi connection process is often tedious, requiring the user to input credentials every time they try to connect. This program streamlines the process, allowing you to connect automatically.

## Features

- **Automatic Login:** After entering the correct username and password, the application stores them in a JSON file. You no longer have to manually enter your credentials every time.
- **Customtkinter GUI:** A simple and intuitive graphical interface built with Python's `customtkinter` library.
- **Seamless Connection:** Once the credentials are saved, pressing the "Connect" button sends a POST request with your credentials to the Wi-Fi authentication form and connects you automatically.

## How It Works

1. **Launch the Application:** The program starts with a "Connect" button in the center of the screen.
2. **Enter Credentials:** When you click the settings button in the top-right corner, a window will pop up asking for your username and password. These credentials will be saved to a local JSON file for future use.
3. **Automatic Wi-Fi Connection:** When the credentials are entered correctly, the program will automatically send a POST request with your username and password to the network authentication page, logging you in seamlessly.

## Installation

If you are not a developer, you can use the bin file on the Releases tab. Open it with WinRar or 7zip and extract the files. Then you are ready to go.


1. Clone the repository:
   ```bash
   git clone https://github.com/RaijuMounun/gsbwifiautoconnect.git
   ```

2. Navigate to the project folder:
   ```bash
   cd gsbwifiautoconnect
   ```
   
3. Install the necessary Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application:

  ```bash
  python main.py
  ```

On the main screen, click the Settings button to enter your Wi-Fi credentials.

Click connect button to automatically log in to the GSB Wi-Fi.

## Configuration
The username and password you enter will be saved in a local config.json file for convenience. This file will be created automatically upon the first successful login.
This file is not encrypted. So, be aware.
   
