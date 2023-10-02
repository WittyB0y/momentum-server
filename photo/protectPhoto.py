import sys
from io import BytesIO

import pyAesCrypt
from momentumServer.settings import SECRET_KEY


def encrypting(file):
    buffer_size = 1024 * 64
    file_data = file.read()
    file.seek(0)
    encrypted_data = BytesIO()
    pyAesCrypt.encryptStream(BytesIO(file_data), encrypted_data, SECRET_KEY, buffer_size)
    encrypted_data.seek(0)
    return encrypted_data
