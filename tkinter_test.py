'''
Created on 2013/1/1

@author: Audi
'''

import ttk
import re
import subprocess
import platform
from tkinter import *
from tkinter.filedialog import *
from datetime import *

class MultimediaTool:
    def __init__(self):
        if platform.system() == 'Windows':
           self.extProgram = {'mencoder' : 'mencoder.exe',
                              'mplayer' : 'mplayer.exe',
                              'mediaPlayer' : 'mpc-hc.exe',
                              'fileBrowser' : 'explorer'}
           self.extProgramPath = {'mencoder' : 'G:/MPlayer-p4-svn-34401',
                                  'mplayer' : 'G:/MPlayer-p4-svn-34401',
                                  'mediaPlayer' : 'C:/Program Files (x86)/K-Lite Codec Pack/Media Player Classic'}
        elif platform.system() == 'Linux':
            self.extProgram = {'mencoder' : 'mencoder',
                               'mplayer' : 'mplayer',
                               'mediaPlayer' : 'gnome-mplayer',
                               'fileBrowser' : 'nautilus'}
            
    def mediaPlayer(self, fileName, args):
        if fileName == '':
            return False
        command = self.extProgram['mediaPlayer'] + ' ' + args + ' ' + fileName
        if platform.system() == 'Windows':
            command = self.extProgramPath['mediaPlayer'] + '/' + command
        mediaPopen = subprocess.Popen(args = command)
        
    def mediaInfo(self, fileName):
        if fileName == '':
            return False
        command = self.extProgram['mplayer'] + ' -nosound -vc dummy -vo null -identify ' + fileName 
        if platform.system() == 'Windows':
            command = self.extProgramPath['mplayer'] + '/' + command
        return subprocess.check_output(args = command).splitlines()
    
    def mediaEncoder(self, filename, args):
        pass
    
    def fileBrowser(self, initial_dir):
        command = self.extProgram['fileBrowser'] + ' ' + initial_dir
        mediaPopen = subprocess.Popen(args = command)
        
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
    
class VideoFileSelectionField(FileSelectionField):
    def __init__(self, master, fmelbl_text):
        FileSelectionField.__init__(self, master, fmelbl_text)
        self.multimedia = MultimediaTool()
        
    def btnAskOpenFile(self):
        FileSelectionField.btnAskOpenFile(self)
        if self.fileName.get() == '':
            return
        self.multimedia.mediaPlayer(self.fileName.get(), '')
        output = self.multimedia.mediaInfo(self.fileName.get())
        for i in range(len(output)):
            print(output[i])
        

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
    
    def createNode(self, node_root):
        return self.tv.insert(node_root, 'end', None)
        
    def setNodeData(self, node, node_data):
        self.tv.item(node, text = node_data)
        self.tv.see(node)
        self.tv.selection_set(node)
    
    def deleteNodes(self, root = None):
        children = self.tv.get_children(root)
        for i in range(len(children) - 1):
            self.tv.delete(children[i])
            
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
        
        ListField.__init__(self, self.lblfme)
        self.fmeTv.grid_configure(row = 0, column = 0)
        self.endNode = ClipListField.createNode(self, '')
        ListField.setNodeData(self, self.endNode, 'No.\tStart\t\tEnd\t\tDuration\t\tDifference')
        
        self.fme = ttk.Frame(self.lblfme)
        self.fme.grid(row = 0, column = 1, sticky = N + W + E + S)
        self.videoPosText = ['Start', 'End', 'Duration']
        self.videoPosVar = {}
        self.ent = {}
        for i in range(len(self.videoPosText)):
            self.lblfme = {self.videoPosText[i] : 
                           ttk.LabelFrame(self.fme, text = self.videoPosText[i])}
            self.lblfme[self.videoPosText[i]].pack()
            self.videoPosVar[self.videoPosText[i]] = StringVar()
            self.ent[self.videoPosText[i]] = ttk.Entry(self.lblfme[self.videoPosText[i]], width = 10, textvariable = self.videoPosVar[self.videoPosText[i]])
            self.ent[self.videoPosText[i]].pack()
        
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
        for i in range(len(self.videoPosText) - 1):
            if self.videoPosVar[self.videoPosText[i]].get() == '' or re.match("^([0-2][0-3])([0-5]\d){2}$", self.videoPosVar[self.videoPosText[i]].get()) == None:
                self.ent[self.videoPosText[i]].focus()
                return False
        return True
    
    def calculateDuration(self):
        videoPosition = {}
        for i in range(len(self.videoPosText) - 1):
            videoPosition[self.videoPosText[i]] = datetime.strptime(self.videoPosVar[self.videoPosText[i]].get(), "%H%M%S")
            
        if videoPosition['End'] < videoPosition['Start']:
            print("End position is before start position")
            return False
        videoDuration = videoPosition['End'] - videoPosition['Start']
        self.videoPosVar['Duration'].set(videoDuration)
        
        self.endNode = ClipListField.createNode(self, '')
        ClipListField.setNodeData(self, self.endNode, '{num}\t{startPos}\t\t{endPos}\t\t{duration}\t\t{difference}'.format(num = self.tv.index(self.endNode),
                                                                                                                          startPos = videoPosition['Start'].strftime('%H:%M:%S'),
                                                                                                                          endPos = videoPosition['End'].strftime('%H:%M:%S'), 
                                                                                                                          duration = self.videoPosVar['Duration'].get(),
                                                                                                                          difference = videoDuration.seconds))
        return True

    def btnAdd(self):
        if not self.chkTimeFormat():
            return
        if not self.calculateDuration():
            return

    def bindReturn(self, event):
        self.btnAdd()
    
    def btnClear(self):
        for i in range(len(self.videoPosText)):
            self.videoPosVar[self.videoPosText[i]].set('')
        self.ent['Start'].focus()
    
    def btnGenerate(self):
        pass
    
    def btnReset(self):
        self.btnClear()
        ListField.deleteNodes(self)
        ListField.setNodeData(self, self.endNode, 'No.\tStart\t\tEnd\t\tDuration\t\tDifference')
        
class ClipListGenerator:
    def __init__(self, master):
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(2, weight = 1)
        self.fileSelectionField = VideoFileSelectionField(master, "Target File")
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



