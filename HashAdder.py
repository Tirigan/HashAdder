import hashlib

def main():
    print("HashAdder Python Hash Calculator")
    
    file_path = input("Enter file path.")

    try:
        with open(file_path, "rb") as file:
            file_contents = file.read()

        md5_hash = hashlib.md5(file_contents).hexdigest()
        sha256_hash = hashlib.sha256(file_contents).hexdigest()

        print(f"MD5 Hash: {md5_hash}")
        print(f"SHA-256 hash: {sha256_hash}")

    except FileNotFoundError:
        print("File not found. Please enter valid file path.")

if __name__ == "__main__":
    main()