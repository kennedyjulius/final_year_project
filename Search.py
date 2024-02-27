def open_drive(drive_letter):
    drive = open(f"{drive_letter}:", 'rb')
    return drive


def read_and_write(image, drive):
    byte = drive.read(1)
    image.write(byte)
    return byte

def jpg_search(drive_letter):
    n_ctr = 0
    n_max = 10000000
    prev = b'0'
    cur = b'0'
    sector = 512
    image_ctr = 0
    jpeg_max_size = 10000000

    drive = open_drive(drive_letter)
    while n_ctr < n_max:
        try:
            drive.seek(n_ctr * sector)
            cur = drive.read(1)

            if cur == b'\xFF':
                next_byte = drive.read(1)
                if next_byte == b'\xD8':
                    print("FOUND - ", n_ctr)
                    image_ctr += 1
                    with open(f"found\\{image_ctr}.jpg", "wb") as image:
                        image.write(b'\xFF\xD8')
                        m_ctr = 0
                        while m_ctr < jpeg_max_size:
                            cur = read_and_write(image, drive)
                            if cur == b'\xD9' and prev == b'\xFF':
                                print("Image Saved")
                                break
                            prev = cur
                            m_ctr += 1
                        else:
                            print("Image Saved - failed")
        except Exception as e:
            print(f"An error occurred: {e}")
        n_ctr += 1

def pdf_search(drive_letter):
    n_ctr = 0
    n_max = 10000000
    sector = 512
    pdf_max_size = 100000000

    while n_ctr < n_max:
        try:
            with open_drive(drive_letter) as drive:
                drive.seek(n_ctr * sector)
                cur = drive.read(1)

                if cur == b'\x25':
                    next_byte = drive.read(1)
                    if next_byte == b'\x50':
                        print("FOUND - ", n_ctr)
                        with open(f"found\\{n_ctr}.pdf", "wb") as image:
                            image.write(b'\x25\x50')
                            m_ctr = 0
                            while m_ctr < pdf_max_size:
                                cur = read_and_write(image, drive)
                                if cur == b'\x0A':
                                    trailer = drive.read(4)
                                    if trailer == b'\x25\x25\x45\x4F':
                                        print("PDF Saved")
                                        break
                                m_ctr += 1
                            else:
                                print("PDF Saved - failed")
        except Exception as e:
            print(f"An error occurred: {e}")
        n_ctr += 1

def docx_search(drive_letter):
    n_ctr = 0
    n_max = 10000000
    sector = 512
    docx_max_size = 100000000

    while n_ctr < n_max:
        try:
            with open_drive(drive_letter) as drive:
                drive.seek(n_ctr * sector)
                cur = drive.read(1)

                if cur == b'\x50':
                    next_byte = drive.read(1)
                    if next_byte == b'\x4B':
                        next_byte = drive.read(1)
                        if next_byte == b'\x03':
                            next_byte = drive.read(1)
                            if next_byte == b'\x04':
                                next_byte = drive.read(1)
                                if next_byte == b'\x14':
                                    next_byte = drive.read(1)
                                    if next_byte == b'\x00':
                                        next_byte = drive.read(1)
                                        if next_byte == b'\x06':
                                            print("FOUND DOCX - ", n_ctr)
                                            with open(f"found\\{n_ctr}.docx", "wb") as image:
                                                image.write(b'\x50\x4B\x03\x04\x14\x00\x06\x00')
                                                m_ctr = 0
                                                while m_ctr < docx_max_size:
                                                    cur = read_and_write(image, drive)
                                                    if cur == b'\x50':
                                                        trailer = drive.read(3)
                                                        if trailer == b'\x4B\x05\x06':
                                                            print("DOCX Saved")
                                                            break
                                                    m_ctr += 1
                                                else:
                                                    print("DOCX Saved - failed")
        except Exception as e:
            print(f"An error occurred: {e}")
        n_ctr += 1

def main():
    print("Weuh! Yaani imework")
    jpg_search()

if __name__ == "__main__":
    main()
