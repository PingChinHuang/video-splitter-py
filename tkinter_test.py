'''
Created on 2013/1/1

@author: Audi
'''

import os
import re
import subprocess
import platform
from time import sleep
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import *
from datetime import *
from threading import Thread

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
        return subprocess.Popen(args = command, stdout = subprocess.PIPE)
    
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
        
        self.fullName = StringVar()
        self.entry = ttk.Entry(self.fmelbl, textvariable = self.fullName)
        self.entry.grid(row = 0, column = 0, sticky = W + E)
        
        self.button = ttk.Button(self.fmelbl, text = "...", width = 1,
                                 command = self.btnAskOpenFile)
        self.button.grid(row = 0, column = 1, sticky = W + E)
        self.setDialogDefaultFileTypes((("", "")))
        
    def btnAskOpenFile(self):
        self.fullName.set(askopenfilename(initialdir = '~',
                                          filetypes = self.typeList))
        if self.fullName.get() == '':
            messagebox.showinfo(message = 'No file is selected', icon = 'warning', type = 'ok', title = 'Warning')
            return False
        self.filePath, self.fileName = os.path.split(self.fullName.get())
        self.fileNameSplit = os.path.splitext(self.fileName)
        return True
                
    def setDialogDefaultFileTypes(self, list):
        self.typeList = list
        
    def getFullName(self):
        return self.fullName.get()
    
    def getFileName(self):
        return self.fileName
    
    def getMainName(self):
        return self.fileNameSplit[0]
    
    def getExtentionName(self):
        return self.fileNameSplit[1]
    
    def getFilePath(self):
        return self.filePath
    
    def clearFileNameEntry(self):
        self.fullName.set('')
    
class VideoFileSelectionField(FileSelectionField):
    def __init__(self, master, fmelbl_text):
        FileSelectionField.__init__(self, master, fmelbl_text)
        self.multimedia = MultimediaTool()
        
    def btnAskOpenFile(self):
        if not FileSelectionField.btnAskOpenFile(self):
            return False
        #self.multimedia.mediaPlayer(self.fullName.get(), '')
        #mediaInfo = self.multimedia.mediaInfo(self.fullName.get())
        #t = Thread(target = self.readVideoInfoThread, args = (mediaInfo, ))
        #t.start()
        #t.join(10)
        #self.showVideoInfo()
        return True
        
    def showVideoInfo(self):
        topVideoInfo = Toplevel()
        topVideoInfo.title('Video Information')
        topVideoInfo.resizable(1, 0)
        topVideoInfo.grid_columnconfigure(1, weight = 1)
        lbl = {}
        ent = {}
        for name in range(len(self.infoName)):
            lbl[self.infoName[name]] = ttk.Label(topVideoInfo, text = self.infoName[name])
            ent[self.infoName[name]] = ttk.Entry(topVideoInfo, 
                                                 textvariable = self.infoValue[self.infoName[name]], 
                                                 state = 'readonly')
            lbl[self.infoName[name]].grid(row = name, column = 0, sticky = N + W + E + S)
            ent[self.infoName[name]].grid(row = name, column = 1, sticky = N + W + E + S)    
    
    def readVideoInfoThread(self, mediaInfo):
        self.infoName = []
        self.infoValue = {}
        while True:
            line = mediaInfo.stdout.readline()
            if not line:
                break
            else:
                m = re.match('ID_VIDEO_([A-Z]+)\=(.*)', str(line, 'utf-8'))
                if m != None:
                    self.infoName.append(m.group(1).rstrip())
                    self.infoValue[m.group(1).rstrip()] = StringVar()
                    self.infoValue[m.group(1).rstrip()].set(m.group(2).rstrip())
                else:
                    m = re.match('ID_([A-Z]+)\=(.*)', str(line, 'utf-8'))
                    if m != None:
                        self.infoName.append(m.group(1).rstrip())
                        self.infoValue[m.group(1).rstrip()] = StringVar()
                        self.infoValue[m.group(1).rstrip()].set(m.group(2).rstrip())
                sleep(0.001)

class OptionsField:
    def __init__(self, master):
        self.fmelbl = ttk.LabelFrame(master, text = "Options")
        self.fmelbl.grid(sticky = N + W + E + S)
        self.fmelbl.grid_columnconfigure(1, weight = 1)
        
        self.optionsText = ["Rename", "List Name", "mencoder arguments"]
        self.lbl = {}
        self.entVariable = {}
        self.chkBtnValue = {}
        self.ent = {}
        for i in range(2):
            self.entVariable[self.optionsText[i]] = StringVar()
            self.chkBtnValue[self.optionsText[i]] = IntVar()
            self.lbl[self.optionsText[i]] = ttk.Checkbutton(self.fmelbl, 
                                                            text = self.optionsText[i],
                                                            variable = self.chkBtnValue[self.optionsText[i]])
            self.ent[self.optionsText[i]] = ttk.Entry(self.fmelbl, 
                                                      textvariable = self.entVariable[self.optionsText[i]])
            self.lbl[self.optionsText[i]].grid(row = i, 
                                               column = 0,
                                               sticky = N + W + E + S)
            self.ent[self.optionsText[i]].grid(row = i, 
                                               column = 1, 
                                               sticky = N + W + E + S)
        
        self.entVariable['List Name'].set('{filename}'.format(filename = datetime.today().strftime("%Y%m%d_%H%M")))
        
        self.argsList = ["-ofps 29.97 -vf harddup -oac mp3lame -lameopts abr:br=128 -ovc x264 -x264encopts bitrate=",
                         "-ovc copy -oac mp3lame -lameopts abr:br=128",
                         "-ofps 29.97 -vf harddup -oac pcm -ovc x264 -x264encopts bitrate="]
        self.entVariable[self.optionsText[2]] = StringVar()
        self.lbl[self.optionsText[2]] = ttk.Label(self.fmelbl, text = self.optionsText[2])
        self.cmbox = ttk.Combobox(self.fmelbl,
                                  values = self.argsList,
                                  textvariable = self.entVariable[self.optionsText[2]])
        self.lbl[self.optionsText[2]].grid(row = 2, column = 0, sticky = N + W + E + S)
        self.cmbox.grid(row = 2, column = 1, sticky = N + W + E + S)
        
        self.setDefaultArgs(0)
        
    def setDefaultArgs(self, idx):
        self.entVariable[self.optionsText[2]].set(self.argsList[idx])
        
    def getMencoderArgs(self):
        return self.entVariable[self.optionsText[2]].get()
    
    def setMencoderArgs(self, value):
        self.entVariable[self.optionsText[2]].set(value)
    
    def getRenameChkBtnValue(self):
        return self.chkBtnValue[self.optionsText[0]].get()

    def getListNameChkBtnValue(self):
        return self.chkBtnValue[self.optionsText[1]].get()
    
    def getListName(self):
        return self.entVariable[self.optionsText[1]].get()
    
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
    
    def getNodeData(self, node):
        return self.tv.item(node, 'text')
        
    def getChildrenList(self, root = None):
        return self.tv.get_children(root)
    
    def deleteNodes(self, root = None):
        children = self.getChildrenList(root)
        for item in children:
            self.tv.delete(item)
        
            
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
        ListField.setNodeData(self, self.endNode, 'No.\tStart\t\tEnd')
        
        self.fme = ttk.Frame(self.lblfme)
        self.fme.grid(row = 0, column = 1, sticky = N + W + E + S)
        self.videoPosText = ['Start', 'End']
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
            
        self.btn[self.btnText[0]].configure(command = self.btnAdd)
        self.btn[self.btnText[1]].configure(command = self.btnClear)
        self.ent[self.videoPosText[0]].bind('<Key-Return>', self.bindReturn)
        self.ent[self.videoPosText[1]].bind('<Key-Return>', self.bindReturn)
        #self.ent[self.videoPosText[2]].configure(state = 'readonly')
        
    def chkTimeFormat(self):
        for i in range(len(self.videoPosText) - 1):
            if self.videoPosVar[self.videoPosText[i]].get() == '' or re.match("^([0-2][0-3])([0-5]\d){2}$", self.videoPosVar[self.videoPosText[i]].get()) == None:
                self.ent[self.videoPosText[i]].focus()
                messagebox.showinfo(message = "Format: [HHMMSS]\nHH should be between 0 and 23, \nand MM and SS should be between 00 and 59. \nAll characters should be digital.",
                                    icon = 'error', type = 'ok', title = 'Incorrect Position Format')
                return False
        return True
    
    def calculateDuration(self):
        videoPosition = {}
        for i in range(len(self.videoPosText)):
            videoPosition[self.videoPosText[i]] = datetime.strptime(self.videoPosVar[self.videoPosText[i]].get(), "%H%M%S")
            
        if videoPosition[self.videoPosText[1]] < videoPosition[self.videoPosText[0]]:
            messagebox.showinfo(message = "End position is before start position", 
                                icon = 'error', type = 'ok', title = 'Incorrect Position')
            return False
        self.endNode = ClipListField.createNode(self, '')
        ClipListField.setNodeData(self, self.endNode, 
                                  '{num}\t{startPos}\t\t{endPos}'.format(num = self.tv.index(self.endNode),
                                                                         startPos = videoPosition[self.videoPosText[0]].strftime('%H:%M:%S'),
                                                                         endPos = videoPosition[self.videoPosText[1]].strftime('%H:%M:%S')))
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
        self.ent[self.videoPosText[0]].focus()
        
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
        
        self.clipListField.btn[self.clipListField.btnText[2]].configure(command = self.btnGenerate, state = 'disabled')
        self.clipListField.btn[self.clipListField.btnText[3]].configure(command = self.btnReset)
        
        self.fileSelectionField.button.configure(command = self.btnAskOpenFile)
        
    def btnGenerate(self):
        clipListFileName = os.path.join(os.path.sep, 
                                        self.fileSelectionField.getFilePath(), 
                                        self.fileSelectionField.getMainName() + '.clip')
        clipListFile = open(clipListFileName, "w+")
        try:
            clipListFile.write(self.fileSelectionField.getFileName() + '\n')
            clipListFile.write(self.optionsField.getMencoderArgs() + '\n')
            
            clips = self.clipListField.getChildrenList()
            for i in range(1, len(clips)):
                dataList = str.split(self.clipListField.getNodeData(clips[i]))
                for j in range(1, len(dataList)):
                    clipListFile.write(dataList[j] + ' ')
                clipListFile.write('\n')
        finally:
            clipListFile.close()
        
        if self.optionsField.getListNameChkBtnValue():
            jobListFileName = os.path.join(os.path.sep, 
                                           'C:/temp',
                                           self.optionsField.getListName() + '.list')
            jobListFile = open(jobListFileName, "a+")
            try:
                jobListFile.write(clipListFileName + '\n')
            finally:
                jobListFile.close()
            
    def btnReset(self):
        self.clipListField.btnClear()
        self.clipListField.deleteNodes()
        self.clipListField.endNode = self.clipListField.createNode('')
        self.clipListField.setNodeData(self.clipListField.endNode, 'No.\tStart\t\tEnd\t\tDuration\t\tDifference')
        self.fileSelectionField.clearFileNameEntry()
        self.clipListField.btn[self.clipListField.btnText[2]].configure(state = 'disabled')
        
    def btnAskOpenFile(self):
        if not self.fileSelectionField.btnAskOpenFile():
            return
        
        videoFormat = {'.avi' : 0,
                       '.wmv' : 0,
                       '.mp4' : 1,
                       '.mov' : 2}
        fileExt = self.fileSelectionField.getExtentionName()
        if str.lower(fileExt) in videoFormat:
            self.optionsField.setDefaultArgs(videoFormat[fileExt])
        else:
            self.optionsField.setDefaultArgs(1)
        
        #if str.lower(fileExt) == '.wmv' or str.lower(fileExt) == '.mov':
        #    self.optionsField.setMencoderArgs(self.optionsField.getMencoderArgs() + str(int(int(self.fileSelectionField.infoValue['BITRATE'].get()) / 1000 / 5 * 4)))
        self.clipListField.btn[self.clipListField.btnText[2]].configure(state = 'enabled')
        
class VideoSplitter:
    def __init__(self, master):
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(1, weight = 1)
        self.fileSelectionField = FileSelectionField(master, "List File")
        self.clipListField = ListField(master)
        self.progressField = ProgressField(master, 100, 
                                           'determinate', 'horizontal')
        self.multimediaTool = MultimediaTool();
        self.btn = ttk.Button(self.progressField.fme, text = 'Start', 
                              width = 10,
                              command = self.btnStartSplitting)
        self.btn.grid(row = 0, column = 2, sticky = N + W + S + E)
        
        fileTypeList = (("", "*.list"),
                        ("All Files", "*"))
        self.fileSelectionField.setDialogDefaultFileTypes(fileTypeList)
    
    def btnStartSplitting(self):
        self.btn.configure(text = 'Processing...', state = 'disabled')
        self.clipListField.deleteNodes()
        
        try:
            jobListFile = open(self.fileSelectionField.getFullName(), "r")
        except FileNotFoundError:
            messagebox.showinfo(message = 'File not found', icon = 'error', type = 'ok', title = 'Error')
            self.btn.configure(text = 'Start', state = 'enabled')            
            return
        
        try:
            while True:
                clipListFileName = jobListFile.readline().rstrip()
                filePath, useless = os.path.split(clipListFileName)
                if not clipListFileName:
                    break;
                listRoot = self.clipListField.createNode('')
                self.clipListField.setNodeData(listRoot, clipListFileName)
                clipListFile = open(clipListFileName, "r")
                try:
                    fileName = os.path.splitext(clipListFile.readline().rstrip())
                    args = clipListFile.readline().rstrip()
                    while True:
                        line = clipListFile.readline().split()
                        if not line:
                            break;
                        self.splitVideo(filePath, fileName, args, line, listRoot)
                finally:
                    clipListFile.close()
        finally:
            jobListFile.close()
            
        self.btn.configure(text = 'Start', state = 'enabled')
        
    def splitVideo(self, filePath, fileName, args, line, listRoot):
        videoDuration = self.calculateDuration(line)
        outputFileName = self.generateOutputFileName(filePath, fileName[0], line)
        endNode = self.clipListField.createNode(listRoot)
        self.clipListField.setNodeData(endNode, outputFileName + '\tProcessing...')
        self.setProcessingProgress(50)
        self.clipListField.setNodeData(endNode, outputFileName + '\tDone')
        
    def setProcessingProgress(self, value):
        self.progressField.setProgress(value)
    
    @classmethod    
    def calculateDuration(cls, line):
        videoPosition = [datetime.strptime(line[0], "%H:%M:%S"), datetime.strptime(line[1], "%H:%M:%S")]
        videoDuration = videoPosition[1] - videoPosition[0]
        return videoDuration

    @classmethod
    def generateOutputFileName(cls, filePath, filename, line):
        return "{path}/{name}_{startPos}_{endPos}.avi".format(path=filePath,
                                                              name = filename,
                                                              startPos = str.replace(line[0], ':', ''),
                                                              endPos = str.replace(line[1], ':', ''))
        
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



