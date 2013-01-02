'''
Created on 2013/1/1

@author: Audi
'''

import ttk
from tkinter import *
from tkinter.filedialog import *

class FileSelectionField:    
    def __init__(self, master, fmelbl_text):
        self.fmelbl = ttk.LabelFrame(master, text = fmelbl_text)
        self.fmelbl.grid(sticky = N + W + E + S)
        self.fmelbl.grid_columnconfigure(0, weight = 1)
        
        self.fileName = StringVar()
        self.entry = ttk.Entry(self.fmelbl, textvariable = self.fileName)
        self.entry.grid(row = 0, column = 0, sticky = W + E)
        
        self.button = ttk.Button(self.fmelbl, text = "...", width = 1,
                                 command = self.btnAskOpenFile)
        self.button.grid(row = 0, column = 1, sticky = W + E)
        
    def btnAskOpenFile(self):
        self.fileName.set(askopenfilename(initialdir = '~',
                                          filetypes = self.typeList))
        
    def setDialogDefaultFileTypes(self, list):
        self.typeList = list
        
    def getFileName(self):
        return self.fileName.get()
        
class OptionsField:
    def __init__(self, master):
        self.fmelbl = ttk.LabelFrame(master, text = "Options")
        self.fmelbl.grid(sticky = N + W + E + S)
        self.fmelbl.grid_columnconfigure(1, weight = 1)
        
        self.optionsText = ["New Name", "List Name", "mencoder arugments"]
        for i in range(3):
            self.lbl = {self.optionsText[i] : 
                        ttk.Label(self.fmelbl, text = self.optionsText[i])}
            self.lbl[self.optionsText[i]].grid(row = i, 
                                               column = 0,
                                               sticky = N + W + E + S)
        for i in range(2):
            self.ent = {self.optionsText[i] : ttk.Entry(self.fmelbl)}
            self.ent[self.optionsText[i]].grid(row = i, 
                                               column = 1, 
                                               sticky = N + W + E + S)
        self.cmbox = ttk.Combobox(self.fmelbl)
        self.cmbox.grid(row = 2, column = 1, sticky = N + W + E + S)
    
class ListField:
    def __init__(self, master, enVerticalScrbar = True):
        self.fmeTv = ttk.Frame(master)
        self.fmeTv.grid(sticky = N + W + E + S)
        self.fmeTv.grid_columnconfigure(0, weight = 1)
        self.fmeTv.grid_rowconfigure(0, weight = 1)
        
        self.tv = ttk.Treeview(self.fmeTv, show = 'tree')
        self.tv.grid(column = 0, row = 0, sticky = N + W + E + S)
        self.tv.grid_columnconfigure(0, weight = 1)
        self.tv.grid_rowconfigure(0, weight = 1)
        
        if enVerticalScrbar:
            self.sv = ttk.Scrollbar(self.fmeTv, orient = 'vertical', 
                                    command = self.tv.yview())
            self.sv.grid(column = 1, row = 0, sticky = N + W + E + S)
            self.tv.configure(yscrollcommand = self.sv.set)
        
class ClipListField(ListField):
    def __init__(self, master, lblfme_text):
        self.lblfme = ttk.LabelFrame(master, text = lblfme_text)
        self.lblfme.grid(sticky = N + W + E + S)
        self.lblfme.grid_columnconfigure(0, weight = 1)
        self.lblfme.grid_rowconfigure(0, weight = 1)
        
        super(ClipListField, self).__init__(self.lblfme)
        self.fmeTv.grid_configure(row = 0, column = 0)
        
        self.fme = ttk.Frame(self.lblfme)
        self.fme.grid(row = 0, column = 1, sticky = N + W + E + S)
        self.clipTimeText = ['Start', 'End', 'Duration']
        for i in range(len(self.clipTimeText)):
            self.lblfme = {self.clipTimeText[i] : 
                           ttk.LabelFrame(self.fme, text = self.clipTimeText[i])}
            self.lblfme[self.clipTimeText[i]].pack()
            self.ent = {self.clipTimeText[i] : 
                        ttk.Entry(self.lblfme[self.clipTimeText[i]], width = 10)}
            self.ent[self.clipTimeText[i]].pack()
        
        self.btnText = ['Add', 'Clear', 'Generate', 'Reset']
        for i in range(len(self.btnText)):
            self.btn = {self.btnText[i] : 
                        ttk.Button(self.fme, text = self.btnText[i], width = 9)}
            self.btn[self.btnText[i]].pack()
        
        
class ClipListGenerator:
    def __init__(self, master):
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(2, weight = 1)
        self.fileSelectionField = FileSelectionField(master, "Target File")
        self.optionsField = OptionsField(master)
        self.clipListField = ClipListField(master, "Clip List")
        
        fileTypeList = (("", "*.avi"),
                        ("", "*.mov"),
                        ("", "*.wmv"),
                        ("", "*.mp4"))
        self.fileSelectionField.setDialogDefaultFileTypes(fileTypeList)
        
class VideoSplitter:
    def __init__(self, master):
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(1, weight = 1)
        self.fileSelectionField = FileSelectionField(master, "List File")
        self.clipListField = ListField(master)
        self.progressValue = IntVar()
        self.prgbar = ttk.Progressbar(master, maximum = 100, 
                                      mode = 'determinate', 
                                      variable = self.progressValue)
        self.prgbar.grid(sticky = N + W + E + S)

rootListGen = Tk()
rootVideoSplitter = Tk()
rootListGen.title("Clip List Generator")
listGen = ClipListGenerator(rootListGen)
rootVideoSplitter.title("Video Splitter")
videoSplitter = VideoSplitter(rootVideoSplitter)
rootListGen.mainloop()
rootVideoSplitter.mainloop()



