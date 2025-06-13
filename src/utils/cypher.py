class Cypher:
    _private_key = "akucintastima" # BUAT PROTOTYPE AJA GAPAPA KALI YAK TARO DI CODENYA HAHAHAHHAHA

    @staticmethod
    def _apply_xor_cipher(text: str, key: str) -> str:
        result = []
        key_len = len(key)
        for i, char in enumerate(text):
            xor_val = ord(char) ^ ord(key[i % key_len])
            result.append(chr(xor_val))
        return "".join(result)

    @staticmethod
    def encrypt(text: str) -> str:
        return Cypher._apply_xor_cipher(text, Cypher._private_key)
    
    @staticmethod
    def decrypt(text: str) -> str:
        return Cypher._apply_xor_cipher(text, Cypher._private_key)

if __name__ == "__main__":
    original_text = "Hello, Private World! 123"
    
    print(f"Original Text: {original_text}")

    encrypted_text = Cypher.encrypt(original_text)
    print(f"Encrypted Text: {encrypted_text}")
    
    decrypted_text = Cypher.decrypt(encrypted_text)
    print(f"Decrypted Text: {decrypted_text}")

    another_text = "This is a secret message."
    print(f"\nOriginal Text: {another_text}")
    encrypted_another = Cypher.encrypt(another_text)
    print(f"Encrypted Text: {encrypted_another}")
    decrypted_another = Cypher.decrypt(encrypted_another)
    print(f"Decrypted Text: {decrypted_another}")

    print("\n--- Demonstrating wrong key ---")
    Cypher._private_key = "wrongkey"
    decrypted_with_wrong_key = Cypher.decrypt(encrypted_text)
    print(f"Decrypted with wrong key: {decrypted_with_wrong_key}")
    Cypher._private_key = "mysecretkey"