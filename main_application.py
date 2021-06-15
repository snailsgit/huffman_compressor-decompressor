import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


from huffman_code import HuffmanCoding
import os
# create the root window
root = tk.Tk()
root.title('Huffman compressor-decompressor')
root.resizable(False, False)
root.geometry('600x350')
compressfile_size=""
decompressfile_size=""

# adding a background image
bg_img=Image.open("bg.jpg")
bg_img=bg_img.resize((600,350),Image.ANTIALIAS)
bg_img=ImageTk.PhotoImage(bg_img)

f_lbl=Label(root,image=bg_img)
f_lbl.place(x=0,y=0)       
T = tk.Text(root, height=10, width=60)

# select a file
def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/home',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

    global h
    h=HuffmanCoding(filename)
    content=open(filename)
    #adding a text widget to show content of a file
    data = content.read()
    
    T.pack()
    T.insert(tk.END, data)
        
    

#compress a file
def compressfile():
    global output_path
    output_path = h.compress()
    compressfile_size=(str(os.path.getsize(output_path)/1024) +" kb")
    compress_text.config(text = compressfile_size)
    showinfo(
        title="Compressed file",
        message=output_path
    )


def decompressfile():
    decom_path = h.decompress(output_path)
    decompressfile_size=(str(os.path.getsize(decom_path)/1024) +" kb")
    decompress_text.config(text = decompressfile_size)
    showinfo(
        title="Decompressed file",
        message=decom_path
    )



# open button
open_button = tk.Button(
    root,
    text='Open a File',
    command=select_file,
    bg="yellow",
    font=("times new roman",12,"bold")
)

open_button.pack(expand=True)

#compress button
compress = tk.Button(
    root,
    text='Compress',
    command=compressfile,
    bg="yellow",
    font=("times new roman",12,"bold")
)
compress.place(x=50,y=100)

compress_text=Label(root,text=compressfile_size,font=("times new roman",12,"bold"),bg="yellow",fg="blue")
compress_text.place(x=50,y=140)


#decompress button
decompress = tk.Button(
    root,
    text='Decompress',
    command=decompressfile,
    bg="yellow",
    font=("times new roman",12,"bold"),
)
decompress.place(x=450,y=100)

decompress_text=Label(root,text=decompressfile_size,font=("times new roman",12,"bold"),bg="yellow",fg="blue")
decompress_text.place(x=450,y=140)


#window heading
heading=tk.Label(root, 
		 text="Huffman encoding decoding",
		 fg = "blue",
		 font=("times new roman",24,"bold"),bg="white"
    )

heading.place(relx=0.5,rely=0.1,anchor='center')



# run the application
root.mainloop()