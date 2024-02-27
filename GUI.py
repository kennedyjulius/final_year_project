import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from Search import jpg_search, pdf_search, docx_search

class RecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Recovery Tool")

        self.drive_letter = None
        self.results = []

        self.label = tk.Label(root, text="Select Drive:")
        self.label.pack()

        self.drive_entry = tk.Entry(root)
        self.drive_entry.pack()

        self.select_drive_button = tk.Button(root, text="Browse Drive", command=self.browse_drive)
        self.select_drive_button.pack()

        self.start_recovery_button = tk.Button(root, text="Start Recovery", command=self.start_recovery)
        self.start_recovery_button.pack()

        self.results_label = tk.Label(root, text="Recovered Items:")
        self.results_label.pack()

        self.results_listbox = tk.Listbox(root)
        self.results_listbox.pack()

    def browse_drive(self):
        self.drive_letter = filedialog.askdirectory()
        self.drive_letter = self.drive_letter.split(':')[0]  # Extract drive letter without colon
        self.drive_entry.delete(0, tk.END)
        self.drive_entry.insert(0, self.drive_letter)

    def start_recovery(self):
        if not self.drive_letter:
            messagebox.showerror("Error", "Please select a drive.")
            return

        self.results_listbox.delete(0, tk.END)
        self.results.clear()

        # Pass the drive letter directly without colon
        self.results.extend(jpg_search(self.drive_letter))
        self.results.extend(pdf_search(self.drive_letter))
        self.results.extend(docx_search(self.drive_letter))

        for result in self.results:
            self.results_listbox.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = RecoveryApp(root)
    root.mainloop()
