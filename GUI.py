import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading
import os
import psutil

# Import file recovery functions
from Search import jpg_search, pdf_search, docx_search
from Carver import SearchUsingTrailer

def create_circle_style():
    style = ttk.Style()
    style.theme_use('clam')  # Set theme to 'clam' for a white window
    style.configure('.', foreground='white', background='white')  # Set text color to black and background to white

    style.layout('CircularProgressbar',
                 [('CircularProgressbar.trough',
                   {'children': [('CircularProgressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'})],
                    'sticky': 'nswe'})])

    style.configure('CircularProgressbar', foreground='green', background='white')

    style.configure('CircularProgressbar.pbar', background='green')

class ProgressWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Progress")
        self.geometry("300x100")

        create_circle_style()

        self.progress_bar = ttk.Progressbar(self, mode='indeterminate', style='CircularProgressbar')
        self.progress_bar.pack(pady=20)

class RecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Recovery Tool")
        self.root.geometry("1200x1200")  # Set window size

        self.selected_drive = tk.StringVar()
        self.selected_drive.set('')  # Default drive set to empty

        self.label = tk.Label(root, text="Select Drive:")
        self.label.pack(pady=(20, 5))

        self.drive_menu = ttk.Combobox(root, textvariable=self.selected_drive, state="readonly")
        self.populate_drive_menu()
        self.drive_menu.pack(pady=5)

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

        self.save_button = ttk.Button(root, text="Save Results", command=self.save_results)
        self.save_button.pack(pady=10)

        self.results_label = tk.Label(root, text="Recovered Items:")
        self.results_label.pack()

        self.results_listbox = tk.Listbox(root)
        self.results_listbox.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        self.results_listbox.bind('<Double-Button-1>', self.open_file)  # Bind double click event to open file

    def populate_drive_menu(self):
        self.selected_drive.set('')  # Clear current drive selection
        drives = self.get_available_drives()
        self.drive_menu['values'] = drives

    def get_available_drives(self):
        drives = []
        for partition in psutil.disk_partitions():
            drives.append(partition.device)
        return drives

    def start_recovery(self):
        self.results_listbox.delete(0, tk.END)  # Clear previous results

        selected_drive = self.selected_drive.get()

        if not selected_drive:
            messagebox.showerror("Error", "Please select a drive.")
            return

        if not (self.check_var_jpg.get() or self.check_var_pdf.get() or self.check_var_docx.get()):
            messagebox.showerror("Error", "Please select at least one file type.")
            return

        progress_window = ProgressWindow(self.root)
        progress_thread = threading.Thread(target=self.perform_recovery, args=(selected_drive, progress_window))
        progress_thread.start()

    def perform_recovery(self, selected_drive, progress_window):
        try:
            # Construct the file type choices based on user selection
            file_types = []
            if self.check_var_jpg.get():
                file_types.append('jpg')
            if self.check_var_pdf.get():
                file_types.append('pdf')
            if self.check_var_docx.get():
                file_types.append('docx')

            # Perform recovery for each selected file type
            recovered_files = []
            for file_type in file_types:
                files = None
                if file_type == 'jpg':
                    files = jpg_search(selected_drive)
                elif file_type == 'pdf':
                    files = pdf_search(selected_drive)
                elif file_type == 'docx':
                    files = docx_search(selected_drive)

                if files:
                    recovered_files.extend(files)

            if not recovered_files:
                raise FileNotFoundError("No files found during recovery process.")

            for file_path in recovered_files:
                self.results_listbox.insert(tk.END, file_path)

        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
            self.restart_program()  # Restart the program if FileNotFoundError occurs
        except Exception as e:
            messagebox.showerror("Recovery Failed", f"Recovery Failed: {e}")
            self.restart_program()  # Restart the program if any other exception occurs

        finally:
            progress_window.destroy()

    def open_file(self, event):
        selected_item = self.results_listbox.curselection()
        if selected_item:
            file_path = self.results_listbox.get(selected_item[0])
            os.system(f'start {file_path}')  # Open the file using default system program

    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for item in self.results_listbox.get(0, tk.END):
                    f.write(item + "\n")

    def restart_program(self):
        self.root.destroy()  # Destroy the current window
        main()  # Restart the program

def main():
    root = tk.Tk()
    app = RecoveryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
