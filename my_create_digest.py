import hashlib


def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


def hash_file(filename, operation):
    """"This function returns the SHA-256 hash
   of the file passed into it"""

    # make a hash object
    if operation == 'SHA2-256':
        h = hashlib.sha256()

    if operation == 'SHA3-256':
        h = hashlib.sha3_256()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def main():
    digest = hash_file("/home/faurecia/Downloads/1mb.bin", "SHA2-256")
    print(digest)
    append_new_line("/home/faurecia/Downloads/1mb_digest.bin", digest)


if __name__ == "__main__":
    main()