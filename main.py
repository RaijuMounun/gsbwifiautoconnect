"""GSB WiFi Auto Connect Application.

This application provides a simple GUI for automatically connecting to 
the GSB dormitory WiFi network. It automatically saves and uses login credentials
for seamless connectivity.

Example:
    Simply run the script to start the application:
        $ python main.py
"""

from ui import WindowMain
from connection import connect_to_wifi

if __name__ == "__main__":
    ui = WindowMain(connect_to_wifi)
    ui.run()
