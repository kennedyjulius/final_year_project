drive_path = r"\\.\X:"  # Path to the drive (raw bytes)
fileD = open(drive_path, "rb")
chunk_size = 512        # Size of bytes to read per iteration
offset = 0              # Initial offset
recovery_mode = False   # Recovery mode flag
recovered_count = 0     # Counter for recovered files

while True:
    byte = fileD.read(chunk_size)  # Read a chunk of bytes
    if not byte:  # If end of file is reached, break the loop
        break

    # Search for the start of a JPEG file signature
    start_marker_index = byte.find(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46')
    if start_marker_index >= 0:
        recovery_mode = True
        print(f"==== Found JPG at location: {hex(start_marker_index + (chunk_size * offset))} ====")
        
        # Create a new file for the recovered JPEG
        with open(f"{recovered_count}.jpg", "wb") as fileN:
            fileN.write(byte[start_marker_index:])  # Write the current chunk from the start marker index
            while recovery_mode:
                byte = fileD.read(chunk_size)  # Read the next chunk of bytes
                end_marker_index = byte.find(b'\xff\xd9')  # Search for the end of the JPEG marker
                if end_marker_index >= 0:
                    fileN.write(byte[:end_marker_index + 2])  # Write the remaining bytes until the end marker
                    fileD.seek((offset + 1) * chunk_size)  # Move the file pointer to the next chunk
                    print(f"==== Wrote JPG to location: {recovered_count}.jpg ====\n")
                    recovery_mode = False
                    recovered_count += 1  # Increment the recovered file counter
                else:
                    fileN.write(byte)  # Write the entire chunk if end marker not found

    offset += 1

fileD.close()
