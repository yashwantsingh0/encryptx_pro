import os
import json
from pathlib import Path
from encryptx_pro.crypto import encrypt_file, decrypt_file

# Constants for vault storage location
VAULT_DIR = Path.home() / ".encryptx_pro"
VAULT_FILE = VAULT_DIR / "vault.json.enc"
PLAINTEXT_TEMP = VAULT_DIR / "vault.json"  # Temporary decrypted vault

class Vault:
    def __init__(self, password: str):
        """
        Initialize the Vault with a password.
        Creates the directory if it doesn't exist.
        """
        self.password = password
        self.data = {"version": 1, "entries": []}

        VAULT_DIR.mkdir(parents=True, exist_ok=True)

    def load(self):
        """
        Decrypt and load the vault file into memory.
        If the file doesn't exist, a new vault is assumed.
        """
        if not VAULT_FILE.exists():
            return  # New vault (empty)

        try:
            decrypt_file(str(VAULT_FILE), str(PLAINTEXT_TEMP), password=self.password)
            with open(PLAINTEXT_TEMP, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        finally:
            if PLAINTEXT_TEMP.exists():
                PLAINTEXT_TEMP.unlink()  # Always clean up temp file

    def save(self):
        """
        Encrypt the in-memory vault data and save to disk.
        """
        with open(PLAINTEXT_TEMP, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

        encrypt_file(str(PLAINTEXT_TEMP), str(VAULT_FILE), password=self.password)
        PLAINTEXT_TEMP.unlink()

    def add_entry(self, title, username, password, notes=""):
        """
        Add a new entry to the vault.
        """
        self.data["entries"].append({
            "title": title,
            "username": username,
            "password": password,
            "notes": notes
        })

    def remove_entry(self, title):
        """
        Remove an entry by its title.
        """
        self.data["entries"] = [
            entry for entry in self.data["entries"]
            if entry.get("title") != title
        ]

    def get_all(self):
        """
        Return a list of all vault entries.
        """
        return self.data.get("entries", [])

    def find_entry(self, title):
        """
        Return an entry by its title (case-insensitive).
        """
        for entry in self.get_all():
            if entry["title"].lower() == title.lower():
                return entry
        return None
