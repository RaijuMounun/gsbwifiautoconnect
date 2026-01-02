import PyInstaller.__main__
import customtkinter
import os
import shutil

# Get CustomTkinter path for --add-data
ctk_path = os.path.dirname(customtkinter.__file__)

# Define separator for --add-data (semicolon for Windows)
sep = ';' if os.name == 'nt' else ':'

# Build arguments
args = [
    'src/main.py',                        # Script to build
    '--name=GSB Wifi Auto Connect',       # Name of executable
    '--onefile',                          # Single file
    '--windowed',                         # No console window
    '--noconfirm',                        # Overwrite output
    f'--add-data={ctk_path}{sep}customtkinter', # Include CustomTkinter assets
    f'--add-data=icons{sep}icons',        # Include Applciation icons
    '--hidden-import=PIL._tkinter_finder', # Fix commonly missed import
]

print("Building GSB Wifi Auto Connect with arguments:")
for arg in args:
    print(f"  {arg}")

PyInstaller.__main__.run(args)

print("\n\nBuild Complete!")
print(f"Executable is located in: {os.path.abspath('dist')}")
