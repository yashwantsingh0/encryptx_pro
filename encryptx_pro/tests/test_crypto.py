import tempfile
import os
import pytest
from encryptx_pro.crypto import encrypt_file, decrypt_file

PASSWORD = "StrongTestPassword123!"

def write_file(path, content: bytes):
    with open(path, "wb") as f:
        f.write(content)

def read_file(path) -> bytes:
    with open(path, "rb") as f:
        return f.read()

@pytest.mark.parametrize("content", [
    b"Short text",
    b"",
    "🚀🔒🔥 Unicode text".encode("utf-8"),
    os.urandom(1024 * 256),  # 256 KB binary
])
def test_encrypt_decrypt_round_trip(monkeypatch, content):
    with tempfile.TemporaryDirectory() as tmpdir:
        in_path = os.path.join(tmpdir, "input.txt")
        enc_path = os.path.join(tmpdir, "file.enc")
        out_path = os.path.join(tmpdir, "output.txt")

        write_file(in_path, content)

        # Patch getpass to return PASSWORD
        monkeypatch.setattr("getpass.getpass", lambda _: PASSWORD)

        encrypt_file(in_path, enc_path)
        decrypt_file(enc_path, out_path)

        assert read_file(out_path) == content

def test_decrypt_with_wrong_password_fails(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        in_path = os.path.join(tmpdir, "in.txt")
        enc_path = os.path.join(tmpdir, "file.enc")
        out_path = os.path.join(tmpdir, "out.txt")

        write_file(in_path, b"Secret data")
        monkeypatch.setattr("getpass.getpass", lambda _: PASSWORD)
        encrypt_file(in_path, enc_path)

        # Patch getpass to return a wrong password during decryption
        monkeypatch.setattr("getpass.getpass", lambda _: "WrongPassword")

        with pytest.raises(Exception):
            decrypt_file(enc_path, out_path)

def test_ciphertext_changes_each_time(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "data.txt")
        enc1 = os.path.join(tmpdir, "e1.enc")
        enc2 = os.path.join(tmpdir, "e2.enc")

        write_file(input_path, b"Same content")
        monkeypatch.setattr("getpass.getpass", lambda _: PASSWORD)

        encrypt_file(input_path, enc1)
        encrypt_file(input_path, enc2)

        # Encrypted files must be different because salt/nonce are random
        data1 = read_file(enc1)
        data2 = read_file(enc2)

        assert data1 != data2
