"""Application configuration and constants.

This module centralizes all configurable values and constants used
throughout the application. Edit this file to customize behavior
without modifying core logic.
"""

# --- Network Configuration ---

# GSB WiFi Portal URLs
PORTAL_BASE_URL = "https://wifi.gsb.gov.tr"
LOGIN_ENDPOINT = "/login/j_spring_security_check"
LOGIN_URL = f"{PORTAL_BASE_URL}{LOGIN_ENDPOINT}"
URL_INDEX = f"{PORTAL_BASE_URL}/index.html"

# Request timeouts (in seconds)
# Reduced for faster response times
INITIAL_REQUEST_TIMEOUT = 3 
LOGIN_REQUEST_TIMEOUT = 10

# SSL verification (set to True if GSB fixes their certificate)
SKIP_SSL_VERIFICATION = True


# --- HTML Parsing Labels ---
LABEL_REMAINING_QUOTA = "Total Remaining Quota"
LABEL_TOTAL_QUOTA = "Total Quota (MB)"
LABEL_NEXT_REFRESH = "Next Refresh Date"
LABEL_LAST_LOGIN = "Last Login"


# --- Credential Storage ---
KEYRING_SERVICE_ID = "GSB_Wifi_Auto_Connect"
APP_DATA_FOLDER = "GSB_Wifi_Connect_App"
CONFIG_FILENAME = "user_preferences.json"


# --- UI Configuration (Midnight Zen - Sharp Edition) ---

# Window settings (Wider for better spacing)
WINDOW_TITLE = "GSB WiFi"
WINDOW_GEOMETRY = "460x650" 

# Color Palette (Midnight Cyberpunk)
COLOR_BG_MAIN = "#020617"       # Rich Black
COLOR_BG_CARD = "#0F172A"       # Slate 900
COLOR_BG_SECONDARY = "#1E293B"  # Slate 800

COLOR_TEXT_MAIN = "#E2E8F0"     # Slate 200
COLOR_TEXT_MUTED = "#64748B"    # Slate 500
COLOR_TEXT_ACCENT = "#A78BFA"   # Pastel Violet

# Accent Colors
COLOR_ACCENT_PRIMARY = "#7C3AED" # Violet 600
COLOR_ACCENT_HOVER = "#6D28D9"   # Violet 700
COLOR_ACCENT_GLOW = "#8B5CF6"    # Violet 500

# Status Colors
COLOR_SUCCESS = "#10B981"       # Emerald 500
COLOR_DANGER = "#EF4444"        # Red 500
COLOR_WARNING = "#F59E0B"       # Amber 500

# Social Media Colors
COLOR_GITHUB = "#24292E"
COLOR_GITHUB_HOVER = "#2D333B"
COLOR_INSTAGRAM = "#E1306C"
COLOR_INSTAGRAM_HOVER = "#C13584"
COLOR_LINKEDIN = "#0A66C2"
COLOR_LINKEDIN_HOVER = "#004182"


# Social media URLs
GITHUB_URL = "https://github.com/RaijuMounun"
INSTAGRAM_URL = "https://www.instagram.com/erenzapkinus"
LINKEDIN_URL = "https://www.linkedin.com/in/eren-keskinoglu"


# --- Resource Paths ---
ICON_DISCONNECTED = "icons/disconnected.png"
ICON_CONNECTED = "icons/connected.png"
ICON_GITHUB = "icons/github.png"
ICON_INSTAGRAM = "icons/instagram.png"
ICON_LINKEDIN = "icons/linkedin.png"
