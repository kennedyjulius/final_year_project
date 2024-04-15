import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading
import os

# Import file recovery functions
from Search import jpg_search, pdf_search, docx_search

class RecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Recovery Tool")
        self.root.geometry("600x400")  # Set window size

        self.drive_letter = 'C:'  # Default drive set to 'C:'
        self.selected_types = []

        self.label = tk.Label(root, text="Select Drive:")
        self.label.pack(pady=(20, 5))

        vcmd = root.register(self.validate_drive_entry)  # Register validation function
        self.drive_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))  # Apply validation
        self.drive_entry.pack(pady=5)
        self.drive_entry.insert(0, self.drive_letter)  # Set default drive in the entry field

        self.select_drive_button = ttk.Button(root, text="Browse Drive", command=self.browse_drive)
        self.select_drive_button.pack(pady=5)

        self.label_types = tk.Label(root, text="Select file types to recover:")
        self.label_types.pack(pady=(20, 5))

        self.check_var_jpg = tk.IntVar()
        self.check_var_pdf = tk.IntVar()
        self.check_var_docx = tk.IntVar()

        self.check_jpg = tk.Checkbutton(root, text="jpg", variable=self.check_var_jpg)
        self.check_jpg.pack()
        self.check_pdf = tk.Checkbutton(root, text="pdf", variable=self.check_var_pdf)
        self.check_pdf.pack()
        self.check_docx = tk.Checkbutton(root, text="docx", variable=self.check_var_docx)
        self.check_docx.pack()

        self.start_recovery_button = ttk.Button(root, text="Start Recovery", command=self.start_recovery)
        self.start_recovery_button.pack(pady=20)

        self.results_label = tk.Label(root, text="Recovered Items:")
        self.results_label.pack()

        self.results_listbox = tk.Listbox(root)
        self.results_listbox.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        self.results_listbox.bind('<Double-Button-1>', self.open_file)  # Bind double click event to open file

    def validate_drive_entry(self, value):
        return len(value) <= 1 and value.isalpha()  # Validate input: single character, alphabetic

    def browse_drive(self):
        drive = filedialog.askopenfilename(initialdir='C:/', title="Select System Drive")  # Open file dialog
        if drive:
            drive_letter, _ = os.path.splitdrive(drive)
            if drive_letter:
                self.drive_letter = drive_letter.upper()  # Extract and convert drive letter to uppercase
                self.drive_entry.delete(0, tk.END)
                self.drive_entry.insert(0, self.drive_letter)
            else:
                messagebox.showerror("Error", "Please select a valid system drive.")

    def start_recovery(self):
        self.results_listbox.delete(0, tk.END)  # Clear previous results

        if not self.drive_letter:
            messagebox.showerror("Error", "Please select a drive.")
            return

        if not (self.check_var_jpg.get() or self.check_var_pdf.get() or self.check_var_docx.get()):
            messagebox.showerror("Error", "Please select at least one file type.")
            return

        # Create a thread for each selected file type to search and recover concurrently
        threads = []
        if self.check_var_jpg.get():
            thread = threading.Thread(target=self.recover_files, args=(jpg_search, "jpg"))
            threads.append(thread)
            thread.start()
        if self.check_var_pdf.get():
            thread = threading.Thread(target=self.recover_files, args=(pdf_search, "pdf"))
            threads.append(thread)
            thread.start()
        if self.check_var_docx.get():
            thread = threading.Thread(target=self.recover_files, args=(docx_search, "docx"))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    def recover_files(self, search_function, file_type):
        try:
            recovered_files = search_function(self.drive_letter)
            if not recovered_files:
                messagebox.showinfo("No Files Found", f"No {file_type.upper()} files found on the drive.")
            else:
                for file_path in recovered_files:
                    self.results_listbox.insert(tk.END, f"{file_type.upper()} - {file_path}")
        except Exception as e:
            self.results_listbox.insert(tk.END, f"{file_type} - Recovery Failed: {e}")

    def open_file(self, event):
        selected_item = self.results_listbox.curselection()
        if selected_item:
            file_path = self.results_listbox.get(selected_item[0]).split(" - ")[1]
            os.system(f'start {file_path}')  # Open the file using default system program

def main():
    root = tk.Tk()
    app = RecoveryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
