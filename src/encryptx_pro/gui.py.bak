import sys
import os
import getpass
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox,
    QScrollArea, QGridLayout, QMenuBar, QMenu
)
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QAction
from PyQt6.QtCore import Qt, QUrl

from encryptx_pro.crypto import encrypt_file, decrypt_file

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

class FilePreview(QWidget):
    def __init__(self, path, on_remove):
        super().__init__()
        self.path = path
        self.on_remove = on_remove
        self.output_path = self._derive_output_path()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        if Path(path).suffix.lower() in IMAGE_EXTS and Path(path).exists():
            pixmap = QPixmap(path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.GlobalColor.lightGray)

        img_label = QLabel()
        img_label.setPixmap(pixmap)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(img_label)

        name_label = QLabel(Path(path).name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        remove_btn = QPushButton("❌")
        remove_btn.setFixedWidth(30)
        remove_btn.clicked.connect(lambda: self.on_remove(self))
        layout.addWidget(remove_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _derive_output_path(self):
        return self.path[:-4] if self.path.endswith(".enc") else self.path + ".enc"


class DragDropWidget(QWidget):
    def __init__(self, on_files_dropped):
        super().__init__()
        self.on_files_dropped = on_files_dropped
        self.setAcceptDrops(True)
        self.setMinimumHeight(180)
        self.setStyleSheet("border: 2px dashed #888;")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = [url.toLocalFile() for url in urls if url.isLocalFile()]
        if files:
            self.on_files_dropped(files)


class EncryptXGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 EncryptX Pro")
        self.setGeometry(100, 100, 720, 540)
        self.setMinimumSize(720, 540)
        self.file_widgets = []
        self.dark_mode = False
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        tools_menu = menu_bar.addMenu("Tools")
        settings_menu = menu_bar.addMenu("Settings")
        help_menu = menu_bar.addMenu("Help")

        file_menu.addAction(QAction("Select Files", self, triggered=self.open_file_dialog))
        file_menu.addAction(QAction("Exit", self, triggered=self.close))

        toggle_theme_action = QAction("Dark/Light Mode", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(toggle_theme_action)

        help_menu.addAction(QAction("About EncryptX Pro", self, triggered=self.show_about))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.preview_container = QWidget()
        preview_layout = QVBoxLayout(self.preview_container)

        drag_drop = DragDropWidget(self.add_files)
        drag_layout = QVBoxLayout(drag_drop)

        watermark = QLabel("Drag & Drop files here!")
        watermark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        watermark.setStyleSheet("font-size: 24px; color: #bbb; padding: 20px;")
        drag_layout.addWidget(watermark)

        select_btn = QPushButton("📁 Choose Files...")
        select_btn.clicked.connect(self.open_file_dialog)
        select_btn.setFixedWidth(180)
        select_btn.setStyleSheet("padding: 8px; font-size: 14px; background-color: #57b282; color: white; border-radius: 5px;")
        drag_layout.addWidget(select_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        preview_layout.addWidget(drag_drop)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        preview_layout.addWidget(self.grid_widget)

        scroll.setWidget(self.preview_container)
        main_layout.addWidget(scroll)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.password)

        btns = QHBoxLayout()
        enc_btn = QPushButton("Encrypt All")
        dec_btn = QPushButton("Decrypt All")
        enc_btn.clicked.connect(lambda: self.process_all("encrypt"))
        dec_btn.clicked.connect(lambda: self.process_all("decrypt"))
        btns.addWidget(enc_btn)
        btns.addWidget(dec_btn)
        main_layout.addLayout(btns)

        self.status = QLabel("")
        main_layout.addWidget(self.status)

    def toggle_theme(self):
        if not self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #272822;
                    color: #F8F8F2;
                    font-family: Consolas, monospace;
                }
                QPushButton {
                    background-color: #3E3D32;
                    border: 1px solid #75715E;
                    color: #F8F8F2;
                }
                QLineEdit {
                    background-color: #3E3D32;
                    color: #F8F8F2;
                    border: 1px solid #75715E;
                }
            """)
        else:
            self.setStyleSheet("")
        self.dark_mode = not self.dark_mode

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        self.add_files(files)

    def add_files(self, paths):
        for path in paths:
            if path and not any(w.path == path for w in self.file_widgets):
                widget = FilePreview(path, self.remove_file)
                row = len(self.file_widgets) // 4
                col = len(self.file_widgets) % 4
                self.grid_layout.addWidget(widget, row, col)
                self.file_widgets.append(widget)

    def remove_file(self, widget):
        self.grid_layout.removeWidget(widget)
        widget.setParent(None)
        self.file_widgets.remove(widget)

    def process_all(self, mode):
        if not self.file_widgets:
            self.show_error("No files selected.")
            return

        pw = self.password.text()
        if not pw:
            self.show_error("Enter a password.")
            return

        getpass.getpass = lambda _: pw
        failed = []

        for widget in self.file_widgets:
            try:
                if mode == "decrypt":
                    if not widget.path.endswith(".enc"):
                        raise ValueError("Only .enc files can be decrypted.")
                    decrypt_file(widget.path, widget.output_path)
                else:
                    encrypt_file(widget.path, widget.output_path)
            except Exception as e:
                failed.append(Path(widget.path).name + f" ({e})")

        if failed:
            self.status.setText("⚠️ Some files failed:\n" + "\n".join(failed))
        else:
            self.status.setText("✅ All files processed successfully.")

    def show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)


    def show_about(self):
        text = (
            "<b>EncryptX Pro Edition</b><br>"
            "Military-grade encryption software for Linux.<br>"
            "Built with Python 3.13, PyQt6, and the following technologies:<br><br>"
            "<ul>"
            "<li><b>Encryption:</b> AES-256-GCM</li>"
            "<li><b>Password Hashing:</b> Argon2id (memory-hard KDF)</li>"
            "<li><b>File I/O:</b> Secure file streaming</li>"
            "<li><b>Drag & Drop:</b> Qt event system with MIME parsing</li>"
            "<li><b>GUI Framework:</b> PyQt6 (cross-platform native)</li>"
            "<li><b>Packaging:</b> AppImage & .tar.zst ready</li>"
            "</ul><br><br>"
            "<center>Crafted with ❤️ by <a href='https://yashwantsingh0.github.io'>Yashwant Singh</a></center>"
        )
        msg = QMessageBox(self)
        msg.setWindowTitle("About EncryptX Pro")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncryptXGUI()
    window.show()
    sys.exit(app.exec())
