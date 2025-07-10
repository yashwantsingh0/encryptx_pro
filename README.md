# 🔐 EncryptX Pro

Military-grade encryption for everyone.  
Built for Linux. Designed for humans. Trusted by nerds.

![EncryptX Pro Screenshot 1](https://github.com/yashwantsingh0/encryptx_pro/blob/main/Screenshot%20From%202025-07-11%2001-07-54.png)
![EncryptX Pro Screenshot 2](https://raw.githubusercontent.com/yashwantsingh0/encryptx_pro/refs/heads/main/Screenshot%20From%202025-07-11%2001-07-17.png)


---

## 🚀 Features

- ✅ **AES-256-GCM** encryption
- ✅ **Argon2id** password hashing (memory-hard)
- ✅ **Multiple file encryption** with drag & drop support
- ✅ **Batch decrypt** .enc files
- ✅ **Dark & Light mode toggle** (Monokai theme included)
- ✅ **Password vault & tamper detection** (coming soon)
- ✅ **Professional UI** built in PyQt6
- ✅ Portable `.AppImage`, `.deb`, and `.tar.zst` packages
- ✅ 100% offline – no network dependency, ever

---

## 🔧 Technology Used

| Layer             | Stack                                                      |
|------------------|------------------------------------------------------------|
| 💻 GUI            | Python 3.13 + PyQt6                                        |
| 🔐 Encryption     | AES-256 in GCM mode (via `cryptography` package)           |
| 🔑 KDF            | Argon2id – secure against GPU, ASIC, and brute-force       |
| 🧱 Packaging      | PyInstaller + AppImage + dpkg + tar.zst                    |
| 🧪 Testing        | `pytest` with full coverage                                |
| 📦 Structure      | `src/`-based layout + `pyproject.toml` (PEP 621 compliant) |

---

## 📸 GUI Preview

<p align="center">
  <img src="https://raw.githubusercontent.com/yashwantsingh0/encryptx_pro/refs/heads/main/Screenshot%20From%202025-07-11%2001-07-45.png" width="800"/>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/yashwantsingh0/encryptx_pro/refs/heads/main/Screenshot%20From%202025-07-11%2001-12-15.png" width="800"/>
</p>

---

## 📦 Installation

Choose the format best suited to your Linux distribution. All builds are fully self-contained — no Python, pip, or external dependencies required.

---

### 🔹 AppImage (Recommended – Universal, All Distros)

📥 [Download AppImage (v0.1.0)](https://github.com/yashwantsingh0/encryptx_pro/releases/download/v0.1.0/EncryptXPro_v0.1.0.AppImage)

```bash
chmod +x EncryptXPro_v0.1.0.AppImage
./EncryptXPro_v0.1.0.AppImage
```

✅ Runs on all major Linux distros  
✅ No installation needed — just run  
✅ Ideal for portable or air-gapped use

---

### 🔹 Debian / Ubuntu (.deb)

📥 [Download .deb Package](https://github.com/yashwantsingh0/encryptx_pro/releases/download/v0.1.0/EncryptXPro-v0.1.0.deb)

```bash
sudo dpkg -i EncryptXPro-v0.1.0.deb
```

Then launch from:

- 🔍 App menu → “EncryptX Pro”
- Or CLI:
  ```bash
  encryptx_pro
  ```

---

### 🔹 Arch / Manjaro / pacman (.tar.zst)

📥 [Download .tar.zst](https://github.com/yashwantsingh0/encryptx_pro/releases/download/v0.1.0/encryptxpro-linux.tar.zst)

```bash
tar -I zstd -xvf encryptxpro-linux.tar.zst
cd encryptxpro-tar
./usr/bin/encryptx_pro
```

🧰 AUR package coming soon!

---

Want an `install.sh` script or auto-updater setup (`.zsync`, `deb-get`, or `pacman -U`)? I can generate that for you too.


## 📂 File Types

| Extension | Meaning                      |
|-----------|------------------------------|
| `.enc`    | Encrypted output from EncryptX Pro |
| any       | Accepts any input file type  |

Only `.enc` files are accepted for decryption.

---

## 🔐 Security Design

EncryptX Pro is built on **zero-trust principles**:

- AES-256-GCM (NIST-certified, AEAD mode)
- Argon2id KDF (OWASP-recommended, time+memory hardened)
- Password input never logged or exposed
- No internet connectivity — fully local
- PyInstaller `.spec` hardened (no evals, imports frozen)
- GUI securely isolated — no shell passthrough

---

## 🔧 Developers

```bash
git clone https://github.com/yashwantsingh0/encryptx_pro.git
cd encryptx_pro
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m encryptx_pro.gui
```

---

## 🛠 Build Instructions

### 🔹 AppImage

```bash
pyinstaller src/encryptx_pro/gui.py --name=encryptx_pro --onefile
chmod +x AppDir/usr/bin/encryptx_pro
./appimagetool-x86_64.AppImage AppDir EncryptXPro.AppImage
```

### 🔹 .deb

```bash
dpkg-deb --build encryptxpro-deb
```

### 🔹 .tar.zst

```bash
tar --zstd -cvf encryptxpro-linux.tar.zst encryptxpro-tar/
```

---

## ✨ Coming Soon

- 🔏 Encrypted Password Vault
- 🧪 File tamper detection (HMAC + header validation)
- 🧠 Argon2id benchmarking (per-device tuning)
- 🌐 AUR + GitHub CI workflows
- 🎨 Splash screen and animations

---

## 🧑‍💻 Author

**Yashwant Singh**  
🔗 [yashwantsingh0.github.io](https://yashwantsingh0.github.io)

Licensed under the MIT License.
