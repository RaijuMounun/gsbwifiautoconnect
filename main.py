""" The application starts here. """

from ui import WindowMain
from connection import connect_to_wifi, disconnect_from_wifi

if __name__ == "__main__":
    ui = WindowMain(connect_to_wifi, disconnect_from_wifi)
    ui.run()
