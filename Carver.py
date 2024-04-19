import threading
import os
import pickle
import psutil

from Search import open_drive
from signatures.Search import openDrive

def SearchUsingTrailer(signatures, file_path):
    print(signatures)
    nCtr = 0
    nMax = 10000000
    cur = b'0'
    prev = b'0'
    sector = 512
    startSplice = 0
    endSplice = 1
    MaxSize = 10000000
    with open(file_path, 'rb') as drive:
        while nCtr < nMax:
            drive.seek(nCtr * sector)
            # Read bytes from the drive
            data = drive.read(len(signatures[0]))
            # Check if the data matches the file signature
            if data == signatures[0]:
                print("Header found at position", nCtr)
                # Read the rest of the file to determine its end
                while True:
                    data = drive.read(len(signatures[1]))
                    if data == signatures[1]:
                        print("Trailer found at position", drive.tell())
                        break
                    if not data:
                        break
            nCtr += 1

def main():
    headers = {'jpg': [b'\xFF\xD8', b'\xFF\xD9'],
               'pdf': [b'\x25\x50', b'\x0A\x25\x25\x45\x4F\x46'],
               'docx': [b'\x50\x4B\x03\x04\x14\x00\x06\x00', b'\x50\x4B\x05\x06']}

    filename = 'headers.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(headers, file)

    with open(filename, 'rb') as file:
        headers = pickle.load(file)

    choices = []
    while True:
        print("Choose which file types you want to recover:")
        print("jpg")
        print("pdf")
        print("docx")
        choice = input("Enter choice (type the file type): ").lower()
        choices.append(choice)
        ask_more = int(input("Do you want to input more files? (0/1): "))
        if ask_more != 1:
            break

    drives = [drive.device for drive in psutil.disk_partitions()]
    print("Available file partitions:")
    for drive in drives:
        print(drive)

    drive_letter = input("Enter the letter of the file partition to scan: ").upper()

    if drive_letter not in drives:
        print("Invalid file partition letter. Please select a valid file partition.")
        return

    file_path = input("Enter the full path of the file to scan: ")

    if not os.path.exists(file_path):
        print("Invalid file path. Please enter a valid file path.")
        return

    # Create a thread for each file type to search concurrently
    threads = []
    for choice in choices:
        if choice in headers:
            thread = threading.Thread(target=SearchUsingTrailer, args=(headers[choice], file_path))
            threads.append(thread)
            thread.start()
        else:
            print("Sorry, '{}' file type is not supported.".format(choice))

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
