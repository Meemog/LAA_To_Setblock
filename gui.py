from converter import Converter
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

class ConverterGui:

    def showWindow(self):
        self.__window = tk.Tk()
        width = 100
        height = 100
        self.__window.geometry(f"{width}x{height}")
        
        button = tk.Button(text="Select File", command=self.__getFile)
        button.pack(side="top")
        
        self.__window.mainloop()
    
    def __getFile(self):
        folder_path = filedialog.askopenfilename(title="Select Litematica Analysis File", defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*")))
        print(folder_path)
        con = Converter(input_name=folder_path)
        block_arr = con.readInput()
        commands = con.commandify(block_arr)
        
        messagebox.showinfo("Info", "Loaded commands\nChoose where to save them")
        output_path = filedialog.asksaveasfilename(initialfile="output",defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*")))
        
        con.output(commands, output_path)
        subprocess.run([output_path], shell=True)  
        
        self.__window.destroy()

if __name__ == "__main__":
    gui = ConverterGui()
    gui.showWindow()