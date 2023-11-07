import tkinter as tk
from tkinter import ttk

if __name__ == '__main__':
  window = tk.Tk()
  window.title("Hello, Tk")
  window.geometry("250x150+500+500")


  def handle_quit():
    window.destroy()


  button = ttk.Button(text='Quit', command=handle_quit)
  button.pack()

  window.mainloop()
