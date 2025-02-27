# gui.py
import sqlite3
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

from pdf_db_filename import get_db_path


def fetch_data(db_path):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT id, parent_id, dictionary, decompressed_stream FROM pdf_streams")
  data = cursor.fetchall()
  conn.close()
  return data


class PDFStreamInspector(tk.Tk):
  def __init__(self):
    super().__init__()
    self.data = None
    self.detail_text = None
    self.listbox = None
    self.title("PDF Stream Inspector")
    self.geometry("1600x1200")
    self.create_menu()
    self.db_path = None

    self.lift()
    self.focus_force()

  def create_menu(self):
    menu_bar = tk.Menu(self)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open Database", command=self.open_database)
    file_menu.add_command(label="Create Database", command=self.create_database)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    self.config(menu=menu_bar)

  def open_database(self):
    self.db_path = filedialog.askopenfilename(
      title="Select Database File",
      filetypes=(("SQLite Database Files", "*.db"), ("All Files", "*.*"))
    )
    if self.db_path:
      self.data = fetch_data(self.db_path)
      self.create_widgets()

  def create_database(self):
    pdf_path = filedialog.askopenfilename(
      title="Select PDF File",
      filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )
    if pdf_path:
      db_path = get_db_path(pdf_path)

      db_path = filedialog.asksaveasfilename(
        title="Save Database As",
        defaultextension=".db",
        filetypes=(("SQLite Database Files", "*.db"), ("All Files", "*.*")),
        initialfile=db_path
      )

      try:
        result = subprocess.run(["python", "pdf_stream_extractor.py", pdf_path, "--db-path", db_path], check=True)
        if result.returncode == 0:
          messagebox.showinfo("Success", "Database created successfully!")
        else:
          messagebox.showerror("Error", f'Failed to create database\n\n{result.stderr}')

        self.db_path = db_path
        self.data = fetch_data(self.db_path)
        self.create_widgets()
      except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create database: {e}")

  def create_widgets(self):
    if self.listbox:
      self.listbox.destroy()
    if self.detail_text:
      self.detail_text.destroy()

    self.listbox = tk.Listbox(self, width=40)
    self.listbox.pack(side=tk.LEFT, fill=tk.Y)
    self.listbox.bind("<<ListboxSelect>>", self.on_select)

    self.detail_text = tk.Text(self, wrap=tk.WORD)
    self.detail_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    for item in self.data:
      self.listbox.insert(tk.END, f"Stream ID: {item[0]} (Parent ID: {item[1]})")

  def on_select(self, event):
    selected_index = self.listbox.curselection()[0]
    selected_item = self.data[selected_index]

    self.detail_text.delete(1.0, tk.END)
    self.detail_text.insert(tk.END, f"Dictionary:\n{selected_item[2]}\n\nDecompressed Stream:\n{selected_item[3]}")


if __name__ == "__main__":
  app = PDFStreamInspector()
  app.mainloop()
