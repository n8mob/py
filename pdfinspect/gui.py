import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdfinspect.utility import fetch_data


class PDFStreamInspector(tk.Tk):
  def __init__(self):
    super().__init__()
    self.data = None
    self.detail_text = None
    self.treeview = None
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
      pdf_dir = os.path.dirname(pdf_path)
      pdf_filename = os.path.basename(pdf_path)
    else:
      messagebox.showerror("Error", "No PDF file selected")
      return

    db_path = filedialog.asksaveasfilename(
      title="Save Database As",
      defaultextension=".db",
      filetypes=(("SQLite Database Files", "*.db"), ("All Files", "*.*")),
      initialdir=pdf_dir,
      initialfile=pdf_filename.replace(".pdf", "_pdf")
    )

    if not db_path:
      messagebox.showerror("Error", "No database filename selected")
      return


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
    if self.detail_text:
      self.detail_text.destroy()

    self.treeview = ttk.Treeview(self, columns=("ID", "Parent ID", "headings"))
    self.treeview.heading("ID", text="Stream ID")
    self.treeview.heading("Parent ID", text="Parent ID")
    self.treeview.pack(side=tk.LEFT, fill=tk.Y)
    self.treeview.bind("<<TreeviewSelect>>", self.on_select)

    self.detail_text = tk.Text(self, wrap=tk.WORD)
    self.detail_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    for item in self.data:
      self.treeview.insert("", tk.END, values=(item[0], item[1], item[2]))

  def on_select(self, event):
    selected_item = self.treeview.selection()[0]
    item = self.treeview.item(selected_item)
    selected_index = self.treeview.index(selected_item)
    selected_data = self.data[selected_index]

    self.detail_text.delete(1.0, tk.END)
    self.detail_text.insert(tk.END, f"Dictionary:\n{selected_item[2]}\n\nDecompressed Stream:\n{selected_item[3]}")


if __name__ == "__main__":
  app = PDFStreamInspector()
  app.mainloop()
