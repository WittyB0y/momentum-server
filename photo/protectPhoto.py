from io import BytesIO

import pyAesCrypt
from momentumServer.settings import SECRET_KEY

BUFFER = 1024 * 64


def encrypting(file):
    buffer_size = BUFFER
    file_data = file.read()
    file.seek(0)
    encrypted_data = BytesIO()
    pyAesCrypt.encryptStream(BytesIO(file_data), encrypted_data, SECRET_KEY, buffer_size)
    encrypted_data.seek(0)
    return encrypted_data


def decrypting(file):
    buffer_size = BUFFER
    file_data = file.read()
    file.seek(0)
    encrypted_data = BytesIO()
    pyAesCrypt.decryptStream(BytesIO(file_data), encrypted_data, SECRET_KEY, buffer_size)
    encrypted_data.seek(0)
    return encrypted_data
