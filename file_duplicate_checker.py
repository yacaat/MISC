import os
import hashlib
import sys


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.key = name + str(size)
        self.hash = None

    def display(self):
        print(f"File: {self.name}")
        print(f"Size: {self.size} bytes")

    def calculate_hash(self, algorithm="md5", block_size=65536):
        hash_func = hashlib.new(algorithm)
        try:
            with open(self.name, 'rb') as file:
                while True:
                    data = file.read(block_size)
                    if not data:
                        break
                    hash_func.update(data)
        except FileNotFoundError:
            print(f"File not found: {self.name}")
        self.hash = hash_func.hexdigest()
def display_help():
    help_text = """
    Usage: python your_script_name.py [path] [--help]

    Description:
    This script analyzes files in a directory to identify and display files with the same size and, if necessary, the same content by calculating their hash values.

    Options:
      path        : The directory path to analyze. If not provided, the script will prompt you for it interactively.
      -h, --help  : Display this help message.

    Examples:
      1. Analyze a specific directory:
         python your_script_name.py /path/to/directory

      2. Prompt for a directory interactively:
         python your_script_name.py

    Note:
    The script will identify files with the same size and then calculate hash values to find files with the same content.

    For assistance, please use the --help option.
    """
    print(help_text)

if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        display_help()
        sys.exit(0)

    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        while not path:
            path = input("Enter the directory path: ").strip()
            if not os.path.isdir(path):
                print(f"'{path}' is not a valid directory. Please enter a valid path.")
                path = None

    file_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            name = os.path.join(root, file)
            size = os.stat(name).st_size
            file_list.append(File(name, size))

    file_list.sort(key=lambda x: x.size, reverse=True)

    same_size_files = {}
    same_hash_files = {}

    for file in file_list:
        if file.size in same_size_files:
            same_size_files[file.size].append(file)
        else:
            same_size_files[file.size] = [file]

    for size, files in same_size_files.items():
        if len(files) > 1:
            for file in files:
                file.calculate_hash()
                if file.hash in same_hash_files:
                    same_hash_files[file.hash].append(file)
                else:
                    same_hash_files[file.hash] = [file]

    for hash, files in same_hash_files.items():
        if len(files) > 1:
            print(hash)
            for file in files:
                file.display()
            print("-----\n")
