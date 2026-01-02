"""Credential management module for secure storage of sensitive data.

This module handles secure storage of passwords using the OS keyring
and stores non-sensitive preferences in a local JSON config file.
Supports multiple accounts with metadata (quota, last update).
"""

import json
import os
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import datetime

import keyring

from config import KEYRING_SERVICE_ID, APP_DATA_FOLDER, CONFIG_FILENAME


class CredentialManager:
    """Manages user credentials and application settings.
    
    Passwords are stored securely in the OS keyring.
    Account list, preferences, and metadata are stored in JSON.
    
    JSON Structure:
    {
        "accounts": {
            "user1": {
                "quota": "15.4 GB", 
                "last_update": "2026-01-03 14:00"
            },
            "user2": {
                "quota": "0.0 GB", 
                "last_update": "..."
            }
        },
        "last_used": "user1"
    }
    """

    def __init__(self):
        """Initialize the credential manager and resolve config path."""
        self.config_path = self._get_config_path()
        self._migrate_legacy_config()

    def _get_config_path(self) -> Path:
        """Determine the appropriate config file path based on the OS."""
        if os.name == 'nt':  # Windows
            base_path = os.getenv('LOCALAPPDATA')
            if not base_path:
                base_path = os.path.expanduser("~")
            base_dir = Path(base_path)
        else:  # Linux / Mac
            base_dir = Path.home() / ".config"

        app_dir = base_dir / APP_DATA_FOLDER
        app_dir.mkdir(parents=True, exist_ok=True)
        
        return app_dir / CONFIG_FILENAME

    def _migrate_legacy_config(self) -> None:
        """Migrate old formats to the new dictionary-based account structure."""
        if not self.config_path.exists():
            return
            
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Case 1: Already in new format (accounts is a dict)
            if "accounts" in data and isinstance(data["accounts"], dict):
                return

            # Case 2: Intermediate format (accounts is a list)
            if "accounts" in data and isinstance(data["accounts"], list):
                new_accounts = {}
                for user in data["accounts"]:
                    new_accounts[user] = {"quota": "---", "last_update": "---"}
                
                data["accounts"] = new_accounts
                self._save_config(data)
                return

            # Case 3: Legacy format (last_username only)
            if "last_username" in data:
                old_username = data["last_username"]
                if old_username:
                    new_data = {
                        "accounts": {
                            old_username: {"quota": "---", "last_update": "---"}
                        },
                        "last_used": old_username
                    }
                    self._save_config(new_data)
                    
        except (json.JSONDecodeError, IOError):
            pass

    def _load_config(self) -> dict:
        """Load config from file."""
        if not self.config_path.exists():
            return {"accounts": {}, "last_used": None}
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Ensure structure integrity if file was manually edited
                if "accounts" not in data or not isinstance(data["accounts"], dict):
                    data["accounts"] = {}
                    
                return data
        except (json.JSONDecodeError, IOError):
            return {"accounts": {}, "last_used": None}

    def _save_config(self, config: dict) -> None:
        """Save config to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Failed to write config file: {e}")

    def get_all_accounts(self) -> List[str]:
        """Get list of all saved account usernames."""
        config = self._load_config()
        return list(config.get("accounts", {}).keys())

    def get_account_metadata(self, username: str) -> Dict[str, Any]:
        """Get metadata (quota, date) for a specific account."""
        config = self._load_config()
        return config.get("accounts", {}).get(username, {})

    def update_account_metadata(self, username: str, quota: str) -> None:
        """Update quota and timestamp for an account."""
        config = self._load_config()
        if username in config["accounts"]:
            now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            config["accounts"][username]["quota"] = quota
            config["accounts"][username]["last_update"] = now_str
            self._save_config(config)

    def add_account(self, username: str, password: str) -> None:
        """Add a new account or update existing account password."""
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        # Store password in secure keyring
        try:
            keyring.set_password(KEYRING_SERVICE_ID, username, password)
        except Exception as e:
            print(f"Keyring error: {e}")
            raise e

        # Update config
        config = self._load_config()
        
        # If new account, initialize metadata
        if username not in config["accounts"]:
            config["accounts"][username] = {"quota": "---", "last_update": "---"}
            
        config["last_used"] = username
        self._save_config(config)

    def remove_account(self, username: str) -> None:
        """Remove an account from the saved list."""
        try:
            keyring.delete_password(KEYRING_SERVICE_ID, username)
        except Exception:
            pass

        config = self._load_config()
        if username in config["accounts"]:
            del config["accounts"][username]
        
        if config["last_used"] == username:
            remaining = list(config["accounts"].keys())
            config["last_used"] = remaining[0] if remaining else None
        
        self._save_config(config)

    def get_password(self, username: str) -> Optional[str]:
        """Get password for a specific username."""
        try:
            return keyring.get_password(KEYRING_SERVICE_ID, username)
        except Exception:
            return None

    def set_last_used(self, username: str) -> None:
        """Set the last used account."""
        config = self._load_config()
        if username in config["accounts"]:
            config["last_used"] = username
            self._save_config(config)

    def get_last_used(self) -> Optional[str]:
        """Get the last used account username."""
        config = self._load_config()
        return config.get("last_used")
    
    # --- Legacy API Support ---
    
    def save_credentials(self, username: str, password: str) -> None:
        self.add_account(username, password)

    def get_last_credentials(self) -> Tuple[str, str]:
        username = self.get_last_used()
        if not username:
            return "", ""
        password = self.get_password(username)
        return username, password if password else ""

    def delete_credentials(self, username: str) -> None:
        self.remove_account(username)