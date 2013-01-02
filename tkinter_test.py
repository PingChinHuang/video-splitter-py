'''
Created on 2013/1/1

@author: Audi
'''

import ttk
import re
from tkinter import *
from tkinter.filedialog import *
from datetime import *

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
        self.setDialogDefaultFileTypes((("", "")))
        
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
        
        self.optionsText = ["New Name", "List Name", "mencoder arguments"]
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
        
        self.listFileName = StringVar()
        self.ent["List Name"].configure(textvariable = self.listFileName)
        self.listFileName.set('{filename}'.format(filename = datetime.today().strftime("%Y%m%d_%H%M")))
        
        self.argsList = ["-ofps 29.97 -vf harddup -ovc x264 -x264encopts bitrate=1000 -oac mp3lame -lameopts abr:br=128",
                         "-ovc copy -oac mp3lame -lameopts abr:br=128",
                         "-ofps 29.97 -vf harddup -ovc x264 -x264encopts bitrate=2500 -oac mp3lame -lameopts abr:br=128",
                         "-ofps 29.97 -vf harddup -ovc x264 -x264encopts bitrate=3000 -oac pcm"]
        self.defaultArgs = StringVar()
        self.setDefaultArgs(0)
        self.cmbox = ttk.Combobox(self.fmelbl, values = self.argsList, textvariable = self.defaultArgs)
        self.cmbox.grid(row = 2, column = 1, sticky = N + W + E + S)
        
    def setDefaultArgs(self, idx):
        self.defaultArgs.set(self.argsList[idx])
    
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
            
class ProgressField:
    def __init__(self, master, prgbarMaximum, prgbarMode, prgbarOrient):
        self.fme = ttk.Frame(master)
        self.fme.grid(sticky = N + W + E + S)
        self.fme.grid_columnconfigure(1, weight = 1)
        self.progressString = StringVar()
        self.ent = ttk.Entry(self.fme, width = 5,
                             state = 'readonly',
                             textvariable = self.progressString)
        self.ent.grid(row = 0, column = 0, sticky = N + W + S + E)
        self.prgbar = ttk.Progressbar(self.fme, 
                                      mode = prgbarMode,
                                      orient = prgbarOrient)
        self.prgbar["value"] = 0
        self.prgbar["maximum"] = prgbarMaximum
        self.prgbar.grid(row = 0, column = 1, sticky = N + W + E + S)
    
    def setProgress(self, value):
        self.prgbar["value"] = value
        self.progressString.set('{percent}%'.format(percent = value / self.prgbar["maximum"] * 100))
        
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
        self.clipTimeVar = {}
        self.ent = {}
        for i in range(len(self.clipTimeText)):
            self.lblfme = {self.clipTimeText[i] : 
                           ttk.LabelFrame(self.fme, text = self.clipTimeText[i])}
            self.lblfme[self.clipTimeText[i]].pack()
            self.clipTimeVar[self.clipTimeText[i]] = StringVar()
            self.ent[self.clipTimeText[i]] = ttk.Entry(self.lblfme[self.clipTimeText[i]], width = 10, textvariable = self.clipTimeVar[self.clipTimeText[i]])
            self.ent[self.clipTimeText[i]].pack()
        
        self.btnText = ['Add', 'Clear', 'Generate', 'Reset']
        self.btn = {}
        for i in range(len(self.btnText)):
            self.btn[self.btnText[i]] = ttk.Button(self.fme, text = self.btnText[i], width = 9)
            self.btn[self.btnText[i]].pack()
            
        self.btn['Add'].configure(command = self.btnAdd)
        self.btn['Clear'].configure(command = self.btnClear)
        self.btn['Generate'].configure(command = self.btnGenerate)
        self.btn['Reset'].configure(command = self.btnReset)
        self.ent['Start'].bind('<Key-Return>', self.bindReturn)
        self.ent['End'].bind('<Key-Return>', self.bindReturn)
        self.ent['Duration'].configure(state = 'readonly')
        
    def chkTimeFormat(self):
        if self.clipTimeVar['Start'].get() == '':
            print("self.clipTimeVar['Start'] is empty")
            self.ent['Start'].focus()
            return False
        if self.clipTimeVar['End'].get() == '':
            print("self.clipTimeVar['End'] is empty")
            self.ent['End'].focus()
            return False
        if re.match("^([0-2][0-3])([0-5]\d){2}$", self.clipTimeVar['Start'].get()) == None:
            self.ent['Start'].focus()
            print("Incorrect Time Format(1)")
            return False
        if re.match("^([0-2][0-3])([0-5]\d){2}$", self.clipTimeVar['End'].get()) == None:
            self.ent['End'].focus()
            print("Incorrect Time Format(2)")
            return False
        return True
    
    def calculateDuration(self):
        print("calculate clip duration")
        startTime = datetime.strptime(self.clipTimeVar['Start'].get(), "%H%M%S")
        endTime = datetime.strptime(self.clipTimeVar['End'].get(), "%H%M%S")
        if endTime < startTime:
            print("End time is less than start time")
            return False
        durationTime = endTime - startTime
        self.clipTimeVar['Duration'].set(durationTime)
        return True
    
    def insertClipIntoList(self):
        pass

    def btnAdd(self):
        if not self.chkTimeFormat():
            return
        if not self.calculateDuration():
            return
        self.insertClipIntoList();
    
    def bindReturn(self, event):
        self.btnAdd()
    
    def btnClear(self):
        for i in range(len(self.clipTimeText)):
            self.clipTimeVar[self.clipTimeText[i]].set('')
        self.ent['Start'].focus()
        print('btnClear')
    
    def btnGenerate(self):
        pass
    
    def btnReset(self):
        pass
        
class ClipListGenerator:
    def __init__(self, master):
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(2, weight = 1)
        self.fileSelectionField = FileSelectionField(master, "Target File")
        self.optionsField = OptionsField(master)
        self.clipListField = ClipListField(master, "Clip List")
        
        fileTypeList = (("", "*.avi *.AVI"),
                        ("", "*.mov *.MOV"),
                        ("", "*.wmv *.WMV"),
                        ("", "*.mp4 *.MP4"),
                        ("All Files", "*"))
        self.fileSelectionField.setDialogDefaultFileTypes(fileTypeList)
        
        
class VideoSplitter:
    def __init__(self, master):
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(1, weight = 1)
        self.fileSelectionField = FileSelectionField(master, "List File")
        self.clipListField = ListField(master)
        self.progressField = ProgressField(master, 100, 
                                           'determinate', 'horizontal')
        self.btn = ttk.Button(self.progressField.fme, text = 'Start', 
                              width = 10,
                              command = self.btnStartSplitting)
        self.btn.grid(row = 0, column = 2, sticky = N + W + S + E)
    
    def btnStartSplitting(self):
        self.btn.configure(text = 'Processing...', state = 'disabled')
        self.setProcessingProgress(50)
        
    def setProcessingProgress(self, value):
        self.progressField.setProgress(value)
        
def deleteVideoSplitterWM():
    rootListGen.focus()
    topVideoSplitter.destroy()

rootListGen = Tk()
rootListGen.title("Clip List Generator")
rootListGen.geometry('640x480+50+100')
listGen = ClipListGenerator(rootListGen)

topVideoSplitter = Toplevel()
topVideoSplitter.title("Video Splitter")
topVideoSplitter.geometry('640x480+800+100')
topVideoSplitter.protocol('WM_DELETE_WINDOW', deleteVideoSplitterWM)
videoSplitter = VideoSplitter(topVideoSplitter)

rootListGen.mainloop()



