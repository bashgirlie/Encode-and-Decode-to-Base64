#!/usr/bin/env python3

import argparse
import base64
import binascii

def encode_string(input_string):
    """
    Encodes a string to base64.
    Args:
        input_string (str): The string to encode.
    Returns:
        str: The base64 encoded string.
    """
    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
    return encoded_bytes.decode("utf-8")

def decode_string(encoded_string):
    """
    Decodes a base64 encoded string.
    Args:
        encoded_string (str): The base64 encoded string to decode.
    Returns:
        str: The decoded string.
    """
    try:
        decoded_bytes = base64.b64decode(encoded_string.encode("utf-8"), validate=True)
    except (ValueError, binascii.Error):
        # binascii.Error catches padding issues (like "SG")
        # ValueError catches formatting issues
        # UnicodeDecodeError catches cases where the binary data isn't valid text
        raise ValueError("Input string is not valid base64 encoded data.")

    try:
        return decoded_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Separate the two issues so you know exactly what went wrong
        raise ValueError("Notice: Base64 data is valid, but it contains raw binary bytes, not UTF-8 text.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode or decode a string to/from base64.")
    parser.add_argument("-e", "--encode", type=str, help="String to encode to base64.")
    parser.add_argument("-d", "--decode", type=str, help="Base64 encoded string to decode.")
    args = parser.parse_args()
    
    if args.encode:
        encoded = encode_string(args.encode)
        print(f"Encoded string: {encoded}")
    elif args.decode:
        try:
            #wrap func in try/except block to catch invalid base64 error cleanly
            decoded = decode_string(args.decode)
            print(f"Decoded string: {decoded}")
        except ValueError as e:
            print(f"{e}")
    else:
        print("Please provide a string to encode or decode.")
