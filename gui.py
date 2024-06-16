from converter import Converter
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

class ConverterGui:
    __input_file = "Select File"
    __output_file = "Select or Create File"

    def showWindow(self):
        self.__window = tk.Tk()
        width = 700
        height = 400
        self.__window.geometry(f"{width}x{height}")
        
        input_text = tk.Label(text="Input File:")
        input_text.pack()
        
        self.__input_button = tk.Button(text=self.__input_file, command=self.__getInput)
        self.__input_button.pack()
        
        output_text = tk.Label(text="Output File:")
        output_text.pack()
        
        self.__output_button = tk.Button(text=self.__output_file, command=self.__getOutput)
        self.__output_button.pack()
        
        space = tk.Label(text="")
        space.pack()
        
        submit_button = tk.Button(text="Submit", command=self.__submit)
        submit_button.pack()
        
        self.__window.mainloop()
    
    def __submit(self):
        issues = []
        if self.__input_file == "Select File":
            issues.append("Input file not chosen")
        elif self.__input_file[-4:] != ".txt":
            issues.append("Input must be .txt file")
            
        if self.__output_file == "Select or Create File":
            issues.append("Output file not chosen")
        elif self.__output_file[-4:] != ".txt":
            issues.append("Output must be .txt file")
            
        if len(issues) != 0:
            issue_str = "\n".join(issues)
            messagebox.showerror("Notice", f"Please fix the following issues:\n\n{issue_str}")
            return
        
        con = Converter(input_name=self.__input_file)
        block_arr = con.readInput()
        commands = con.commandify(block_arr)
        con.output(commands, self.__output_file)
    
        subprocess.run([self.__output_file], shell=True)  
        
    
    def __getInput(self):
        self.__input_file = filedialog.askopenfilename(title="Select Litematica Analysis File", defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*")))
        self.__input_button.configure(text=self.__input_file)
    
    def __getOutput(self):
        self.__output_file = filedialog.asksaveasfilename(initialfile="output",defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*")))
        self.__output_button.configure(text=self.__output_file)

if __name__ == "__main__":
    gui = ConverterGui()
    gui.showWindow()