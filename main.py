import tkinter as tk
import lexer as lex

code_font = "consolas 16"
label_font = "Times 16"
background = "white"
foreground = "black"
     

class UpdateApp():
    def __init__( self ):
        self.line = 0
    def __call__( self, code_input, line_box, code_output, reset):
        if  self.line < (int(code_input.index('end-1c').split('.')[0])):
            # Update the line we are currently processing
            self.line += 1
            tk_line_beg = '{}.{}'.format(self.line, 0)
            tk_line_end = '{}.end'.format(self.line)
            
            # Update the line box
            line_box.config(state=tk.NORMAL)
            line_box.delete('0', tk.END)
            line_box.insert(tk.END, self.line)
            line_box.config(state=tk.DISABLED)
            
            # Take a line from the input box 
            input_string = code_input.get(tk_line_beg, tk_line_end)
            
            # Create an array of tokens (strings)
            token_array = lex.tokenize(input_string)
            
            # Now print every token in the array
            code_output.config(state=tk.NORMAL)
            
            for token in token_array:
                code_output.insert(tk.END, token + '\n')
            
            
            code_output.config(state=tk.DISABLED)
            
        if reset:
            self.line = 0
            
            line_box.config(state=tk.NORMAL)
            line_box.delete('0', tk.END)
            line_box.config(state=tk.DISABLED)
            
            code_output.config(state=tk.NORMAL)
            code_output.delete('0.0', tk.END)
            code_output.config(state=tk.DISABLED)


            
# Here I instantiate the function object (a function that retains state between calls)
next_line = UpdateApp()

def quit_app():
    window.destroy()
    exit()
    
    
# Create the window.
window = tk.Tk()
window.title("Lexical Analyzer for TinyPie")
window.configure(background=background)

# Add the source code input label:
tk.Label(window, text="Source Code Input:", bg=background, fg=foreground, font=label_font).grid(row=1, column=0, sticky="w")


#### Add the source code input box: 
code_input = tk.Text(window, width=64, height=16, bg=background, fg=foreground, font=code_font)
code_input.grid(row=2, column=0, sticky="w")

# Add the current processing line label:
tk.Label(window, text="Current Processing Line:", bg=background, fg=foreground, font=label_font).grid(row=3, column=0, sticky="w")

#### Add the current processing line input box:
line_box = tk.Entry(window, width=3, bg=background, fg=foreground, font=code_font)
line_box.grid(row=4, column=0, sticky="w")
line_box.config(state=tk.DISABLED)


# Add an output label:
tk.Label(window, text="Lexical Analyzed Result:", bg=background, fg=foreground, font=label_font).grid(row=1, column=1, sticky="w")

#### Add the output box:
code_output = tk.Text(window, width=64, height=16, bg=background, fg=foreground, font=code_font)
code_output.grid(row=2, column=1, sticky="w")
code_output.config(state=tk.DISABLED)

# Add a quit button:
tk.Button(window, text="Quit", bg=background, fg=foreground, font=label_font, width=4, command=quit_app).grid(row=6, column=0, sticky="w")


#### Add a next line button:
# I have to use a lambda here because I want to pass the function next_line to command, not the output of next_line.
tk.Button(window, text="Next Line", bg=background, fg=foreground, font=label_font, width=9, command=lambda: next_line(code_input, line_box, code_output, False)).grid(row=5, column=0, sticky="w")

# Add a reset button:
tk.Button(window, text="Reset", bg=background, fg=foreground, font=label_font, width=5, command=lambda: next_line(code_input, line_box, code_output, True)).grid(row=5, column=1, sticky="w")


# Run the main loop.
if __name__ == "__main__":
    window.mainloop()