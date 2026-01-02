"""GSB WiFi Auto Connect Application.

This application provides a simple user interface for automatically connecting
to the GSB dormitory WiFi network. It securely stores login credentials and
offers seamless connectivity.

Example:
    $ python main.py
"""

from ui import WindowMain
from connection import connect_to_wifi

if __name__ == "__main__":
    # connect_to_wifi is passed but handled internally by new UI controller
    ui = WindowMain(connect_to_wifi)
    ui.run()
