from utils.crypto import decrypt, encrypt


class TestCrypto:
    def test_round_trip(self):
        ciphertext, tag, nonce = encrypt(b"foo")
        assert decrypt(ciphertext, tag, nonce) == b"foo"
