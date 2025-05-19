import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
from .main import main






def gui():
    home=os.getenv('HOME')
    # Crea la finestra principale
    root = tk.Tk()
    root.title("Download Tecron PDF")
    mainframe=ttk.Frame(root)
    mainframe.grid(column=0,row=0)
    c=0
    r=0
    domain_label = ttk.Label(mainframe,text="Sito internet:")
    domain_label.grid(column=c,row=r,sticky=tk.W)
    r+=1
    domain = tk.StringVar(value=os.getenv('TECRON_DOMAIN'))
    domain_input = ttk.Entry(mainframe,textvariable=domain)
    domain_input.grid(column=c,row=r,sticky=tk.W)
    r+=1

    passwordfile_label = ttk.Label(mainframe,text="Password file:")
    passwordfile_label.grid(column=c,row=r,sticky=tk.W)
    r+=1
    passwordfile = tk.StringVar(value=os.getenv('TECRON_PASSWORD_FILE'))
    passwordfile_input = ttk.Entry(mainframe,textvariable=passwordfile)
    
    def change_password_file(_):
        passwordfile.set(fd.askopenfilename(initialdir=home))
        with open(passwordfile.get(),'r',encoding='utf-8') as f:
            psw=f.read().strip()
        overwritepassword.set(psw)
    passwordfile_input.bind('<ButtonPress>',change_password_file)
    passwordfile_input.grid(column=c,row=r,sticky=tk.W)
    r+=1
    
 
    outputdir_label = ttk.Label(mainframe,text="Cartella Output:")
    outputdir_label.grid(column=c,row=r,sticky=tk.W)
    r+=1
    outputdir = tk.StringVar(value=os.getenv('TECRON_DOWNLOAD_DIR'))
    outputdir_input = ttk.Entry(mainframe,textvariable=outputdir)
    home=os.getenv('HOME')
    outputdir_input.bind('<ButtonPress>',lambda e: outputdir.set(
            fd.askdirectory(mustexist=True,initialdir=home)
        )
    )
    outputdir_input.grid(column=c,row=r,sticky=tk.W)

    


    c+=1
    r=0
    overwritepassword_label = ttk.Label(mainframe,text="Cambia password:")
    overwritepassword_label.grid(column=c,row=r,sticky=tk.W)
    r+=1
    with open(passwordfile.get(),encoding='utf-8') as f:
        psw=f.read().strip()
    overwritepassword = tk.StringVar(value=psw)
    overwritepassword_input = ttk.Entry(mainframe,textvariable=overwritepassword,show='*')
    overwritepassword_input.grid(column=c,row=r,sticky=tk.W)
    r+=1
    def confirm_change_password():
        with open(passwordfile.get(),'w',encoding='utf-8') as f:
            f.write(overwritepassword.get()+'\n')
    confermapassword = ttk.Button(mainframe, text="Conferma", command=confirm_change_password)
    confermapassword.grid(column=c,row=r,sticky=tk.W)
    r+=1
    targz_label = ttk.Label(mainframe,text="Output archivio:")
    targz_label.grid(column=c,row=r,sticky=tk.W)
    targz = tk.BooleanVar(value=os.getenv('TECRON_TARGZ') is not None)
    targz_input = ttk.Checkbutton(mainframe,variable=targz)
    targz_input.grid(column=c,row=r,sticky=tk.E)
    r+=1

    

    def submit():
        os.environ['TECRON_DOMAIN'] = domain.get()
        os.environ['TECRON_PASSWORD_FILE'] = passwordfile.get()
        os.environ['TECRON_DOWNLOAD_DIR'] = outputdir.get()
        if targz.get():
            os.environ['TECRON_TARGZ']='1'
        prog=ttk.Progressbar(length=1.0,orient=tk.VERTICAL)
        prog=ttk.Progressbar(mode="indeterminate")
        prog.start()
        prog.grid(column=c,row=r+1)
        main(prog)
        prog.destroy()
    button = ttk.Button(mainframe, text="Download PDF", command=submit)
    button.grid(column=c,row=r)

    root.bind("<Return>", submit)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
