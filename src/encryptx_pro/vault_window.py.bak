from PyQt6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from encryptx_pro.vault import Vault, VAULT_FILE
import platform
import subprocess
import shutil


class VaultManagerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Vault Manager")
        self.setMinimumSize(600, 500)
        self.vault = None

        if self.system_prefers_dark():
            self.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                }
                QPushButton {
                    background-color: #444;
                    color: #fff;
                    border-radius: 4px;
                    padding: 5px 10px;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #fff;
                    border: 1px solid #666;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: #fff;
                }
            """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Vault icon
        icon_label = QLabel()
        icon_pixmap = QPixmap(":/icons/vault.png")
        icon_label.setPixmap(icon_pixmap.scaledToWidth(64, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(icon_label)

        # Password input
        self.password_row = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter vault password")

        self.toggle_pw = QPushButton("👁️")
        self.toggle_pw.setCheckable(True)
        self.toggle_pw.setFixedWidth(30)
        self.toggle_pw.clicked.connect(self.toggle_password_visibility)

        self.password_row.addWidget(self.password_input)
        self.password_row.addWidget(self.toggle_pw)
        self.layout.addLayout(self.password_row)

        # Unlock vault button
        self.unlock_button = QPushButton("Unlock Vault")
        self.unlock_button.clicked.connect(self.unlock_vault)
        self.layout.addWidget(self.unlock_button)

        # Red warning banner
        self.warning = QLabel("⚠️ <b style='color:red;'>WARNING:</b> Forgotten passwords <u><b>CANNOT</b></u> be recovered due to <b>hardened encryption</b>.<br><br><b>Resetting is the ONLY option.</b>")
        self.warning.setWordWrap(True)
        self.warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning.setStyleSheet("color: red; font-weight: bold; padding: 8px;")
        self.layout.addWidget(self.warning)

        # Reset vault
        self.reset_button = QPushButton("💥 Reset Vault")
        self.reset_button.clicked.connect(self.reset_vault)
        self.layout.addWidget(self.reset_button)

        # Vault unlocked status
        self.status_label = QLabel()
        self.status_label.setVisible(False)
        self.layout.addWidget(self.status_label)

        # Vault entries
        self.entries_list = QListWidget()
        self.entries_list.setVisible(False)
        self.layout.addWidget(self.entries_list)

        # Action buttons
        self.btn_layout = QHBoxLayout()
        self.add_button = QPushButton("➕ Add")
        self.add_button.clicked.connect(self.add_entry)
        self.remove_button = QPushButton("❌ Remove")
        self.remove_button.clicked.connect(self.remove_selected)
        self.lock_button = QPushButton("🔒 Lock Vault")
        self.lock_button.clicked.connect(self.lock_vault)
        self.change_pw_button = QPushButton("🔑 Change Password")
        self.change_pw_button.clicked.connect(self.change_password)

        self.btn_layout.addWidget(self.add_button)
        self.btn_layout.addWidget(self.remove_button)
        self.btn_layout.addWidget(self.lock_button)
        self.btn_layout.addWidget(self.change_pw_button)

        self.layout.addLayout(self.btn_layout)
        self.add_button.setVisible(False)
        self.remove_button.setVisible(False)
        self.lock_button.setVisible(False)
        self.change_pw_button.setVisible(False)

        # Auto lock timer
        self.lock_timer = QTimer()
        self.lock_timer.timeout.connect(self.lock_vault)
        self.lock_timer.setInterval(5 * 60 * 1000)  # 5 minutes
        self.lock_timer.start()

    def system_prefers_dark(self):
        try:
            if platform.system() == "Linux":
                theme = subprocess.check_output([
                    "gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"
                ]).decode().strip().lower()
                return "dark" in theme
        except Exception:
            pass
        return False

    def toggle_password_visibility(self):
        if self.toggle_pw.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def unlock_vault(self):
        password = self.password_input.text().strip()
        if not password:
            QMessageBox.warning(self, "Missing Password", "Please enter your vault password.")
            return

        try:
            self.vault = Vault(password)
            self.vault.load()
        except Exception as e:
            QMessageBox.critical(self, "Vault Error", f"Failed to load vault: {str(e)}")
            return

        self.password_input.hide()
        self.toggle_pw.hide()
        self.unlock_button.hide()
        self.warning.hide()
        self.reset_button.hide()

        self.status_label.setText("✅ Vault Status: Unlocked")
        self.status_label.setVisible(True)
        self.entries_list.setVisible(True)
        self.add_button.setVisible(True)
        self.remove_button.setVisible(True)
        self.lock_button.setVisible(True)
        self.change_pw_button.setVisible(True)
        self.refresh_entries()
        self.adjustSize()

    def lock_vault(self):
        self.entries_list.setVisible(False)
        self.add_button.setVisible(False)
        self.remove_button.setVisible(False)
        self.lock_button.setVisible(False)
        self.change_pw_button.setVisible(False)
        self.status_label.setVisible(False)
        self.password_input.setDisabled(False)
        self.toggle_pw.setDisabled(False)
        self.password_input.clear()
        self.entries_list.clear()
        self.password_input.show()
        self.toggle_pw.show()
        self.unlock_button.show()
        self.warning.show()
        self.reset_button.show()
        self.unlock_button.setDisabled(False)
        self.adjustSize()

    def refresh_entries(self):
        self.entries_list.clear()
        for entry in self.vault.get_all():
            text = f"{entry['title']} – {entry['username']} ({entry.get('notes', '')})"
            self.entries_list.addItem(QListWidgetItem(text))

    def add_entry(self):
        title, ok1 = QInputDialog.getText(self, "Add Entry", "Title:")
        if not ok1 or not title:
            return

        username, ok2 = QInputDialog.getText(self, "Add Entry", "Username:")
        if not ok2:
            return

        password, ok3 = QInputDialog.getText(self, "Add Entry", "Password:")
        if not ok3:
            return

        notes, ok4 = QInputDialog.getText(self, "Add Entry", "Notes (optional):")
        if not ok4:
            notes = ""

        self.vault.add_entry(title, username, password, notes)
        self.vault.save()
        self.refresh_entries()

    def remove_selected(self):
        selected = self.entries_list.selectedItems()
        if not selected:
            return

        for item in selected:
            title = item.text().split(" – ")[0]
            self.vault.remove_entry(title)

        self.vault.save()
        self.refresh_entries()


    def change_password(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("🔑 Change Vault Password")
        dlg.setMinimumSize(400, 250)
        dlg_layout = QVBoxLayout()
        dlg.setLayout(dlg_layout)
    
        if self.system_prefers_dark():
            dlg.setStyleSheet("""
                QDialog {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: white;
                    border: 1px solid #666;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                }
            """)
    
        # Old password field
        old_pw = QLineEdit()
        old_pw.setPlaceholderText("Enter current password")
        old_pw.setEchoMode(QLineEdit.EchoMode.Password)
        old_toggle = QPushButton("👁️")
        old_toggle.setCheckable(True)
        old_toggle.setFixedWidth(30)
        old_toggle.clicked.connect(lambda checked: old_pw.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        row1 = QHBoxLayout()
        row1.addWidget(old_pw)
        row1.addWidget(old_toggle)
        dlg_layout.addLayout(row1)
    
        # New password field
        new_pw1 = QLineEdit()
        new_pw1.setPlaceholderText("Enter new password")
        new_pw1.setEchoMode(QLineEdit.EchoMode.Password)
        new_toggle1 = QPushButton("👁️")
        new_toggle1.setCheckable(True)
        new_toggle1.setFixedWidth(30)
        new_toggle1.clicked.connect(lambda checked: new_pw1.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        row2 = QHBoxLayout()
        row2.addWidget(new_pw1)
        row2.addWidget(new_toggle1)
        dlg_layout.addLayout(row2)
    
        # Confirm new password
        new_pw2 = QLineEdit()
        new_pw2.setPlaceholderText("Re-enter new password")
        new_pw2.setEchoMode(QLineEdit.EchoMode.Password)
        new_toggle2 = QPushButton("👁️")
        new_toggle2.setCheckable(True)
        new_toggle2.setFixedWidth(30)
        new_toggle2.clicked.connect(lambda checked: new_pw2.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        row3 = QHBoxLayout()
        row3.addWidget(new_pw2)
        row3.addWidget(new_toggle2)
        dlg_layout.addLayout(row3)
    
        # Live password match feedback
        match_feedback = QLabel("")
        match_feedback.setStyleSheet("font-weight: bold;")
        dlg_layout.addWidget(match_feedback)
    
        def check_match():
            if new_pw1.text() and new_pw2.text():
                if new_pw1.text() == new_pw2.text():
                    match_feedback.setText("✅ Passwords match")
                    match_feedback.setStyleSheet("color: green; font-weight: bold;")
                else:
                    match_feedback.setText("❌ Passwords do not match")
                    match_feedback.setStyleSheet("color: red; font-weight: bold;")
            else:
                match_feedback.setText("")
    
        new_pw1.textChanged.connect(check_match)
        new_pw2.textChanged.connect(check_match)
    
        # Confirm button logic (moved inline)
        def confirm_change():
            if old_pw.text().strip() != self.vault.password:
                QMessageBox.warning(self, "Incorrect Password", "Old password is incorrect.")
                return
            if not new_pw1.text() or not new_pw2.text():
                QMessageBox.warning(self, "Missing Fields", "New password fields cannot be empty.")
                return
            if new_pw1.text() != new_pw2.text():
                QMessageBox.warning(self, "Mismatch", "New passwords do not match.")
                return
    
            self.vault.password = new_pw1.text()
            self.vault.save()
            QMessageBox.information(self, "Success", "Vault password changed successfully.")
            dlg.accept()
    
        confirm_btn = QPushButton("✅ Change Password")
        confirm_btn.clicked.connect(confirm_change)
        dlg_layout.addWidget(confirm_btn)
    
        dlg.exec()




    def reset_vault(self):
        confirm, ok = QInputDialog.getText(self, "Confirm Reset", "Type 'Yes, delete this vault.' to confirm permanent deletion:")
        if not ok or confirm != "Yes, delete this vault.":
            return

        if VAULT_FILE.exists():
            VAULT_FILE.unlink()

        # Prompt for new password
        new_pw1, ok1 = QInputDialog.getText(self, "Set New Password", "Enter new password:", QLineEdit.EchoMode.Password)
        if not ok1 or not new_pw1:
            return

        new_pw2, ok2 = QInputDialog.getText(self, "Set New Password", "Re-enter new password:", QLineEdit.EchoMode.Password)
        if not ok2 or new_pw1 != new_pw2:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return

        # Save empty vault
        self.vault = Vault(new_pw1)
        self.vault.save()
        QMessageBox.information(self, "Vault Reset", "Vault has been reset and re-encrypted.")
        self.unlock_vault()
