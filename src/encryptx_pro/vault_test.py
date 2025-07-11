from encryptx_pro.vault import Vault

# 🛡️ Use a test password here
import getpass
password = getpass.getpass("Enter your vault password: ")


# 🔏 Load or create the vault
vault = Vault(password)
vault.load()

# 👤 Add sample entries
vault.add_entry("Gmail", "me@gmail.com", "hunter2", "Personal email account")
vault.add_entry("GitHub", "yashwantsingh0", "ghp_exampletoken", "Open source dev account")

# 💾 Save the vault encrypted
vault.save()
print("✅ Vault saved and encrypted successfully.")

# 🔁 Reload and print entries to verify
vault.load()
print("\n📂 Vault contents:")

for entry in vault.get_all():
    print(f"🔹 {entry['title']}: {entry['username']} / {entry['password']}")
