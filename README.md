# HashAdder

A simple command-line tool for calculating cryptographic hashes of files. Useful for verifying file integrity, checking downloads, or comparing files against known hash values (e.g. malware signatures, vendor-published checksums).

## Features

- Calculates MD5, SHA-1, SHA-256, and SHA-512 in one pass
- Reads files in chunks, so it handles large files without high memory use
- Works interactively (prompts for a file path) or via command-line arguments
- Optional comparison mode: check a computed hash against a value you provide
- Choose specific algorithms instead of running all four

## Requirements

- Python 3.8+
- No external dependencies (uses the built-in `hashlib`)

## Usage

### Interactive mode

```bash
python3 hashadder.py
```

You'll be prompted to enter a file path.

### Command-line mode

```bash
python3 hashadder.py path/to/file.exe
```

### Choose specific algorithms

```bash
python3 hashadder.py path/to/file.exe -a md5 sha256
```

### Compare against a known hash

```bash
python3 hashadder.py path/to/file.exe -c 5d41402abc4b2a76b9719d911017c592
```

This prints whether the provided hash matches any of the computed digests — handy for verifying a download against a publisher's checksum.

### Full options

```
usage: hashadder.py [-h] [-a {md5,sha1,sha256,sha512} [{md5,sha1,sha256,sha512} ...]] [-c HASH] [file]

positional arguments:
  file                  Path to the file to hash. If omitted, you'll be prompted.

options:
  -h, --help            show this help message and exit
  -a, --algorithms      Specific algorithms to run (default: all four)
  -c, --compare HASH    Compare the computed hash(es) against this value
```

## Example output

```
HashAdder Python Hash Calculator

File: sample.txt
Size: 13 bytes
--------------------------------------------------
MD5     : d6eb32081c822ed572b70567826d9d9d
SHA1    : 4fe2b8dd12cd9cd6a413ea960cd8c09c25f19527
SHA256  : a1fff0ffefb9eace7230c24e50731f0a91c62f9cefdfe77121c2f607125dffae
SHA512  : b22137a0e8969282b85e3f9375448307d14c5aabf41be66c4f6a0323bd03a3935972021e4c34aa30914e37b03c22594fe180eea9790e9ff147016c9dfae39d5a
```

## Notes on MD5 and SHA-1

Both are included for compatibility (some vendors still publish MD5/SHA-1 checksums, and malware databases often reference them), but they are **not collision-resistant** and should not be relied on for security-critical integrity verification. Prefer SHA-256 or SHA-512 when you have a choice.

## Possible future additions

- Recursive hashing of an entire directory
- Output to a file (CSV/JSON) for logging or batch verification
- CRC32 support
