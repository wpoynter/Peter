#!/usr/bin/python

from Tkinter import *
import tkFileDialog as fd

import os

import app as Peter

class GUIApp:

	def __init__(self, master):
                self.master = master
		self.frame = Frame(master)
		self.frame.grid(padx=20, pady=15)
		self.title = Label(self.frame, text="Peter", font=("Arial",24))
		self.desc = Label(self.frame, text="UK Data Archive CodeBook to Caddies Parser")
		self.title.grid()
		self.desc.grid(row=1, column=0, pady=10)

	def draw(self):
		self.drawInput();
		self.drawOptions();
		self.drawOutput();
		self.drawStatus();
		self.input['button'] = Button(self.frame, text="Run", command=self.run, state = DISABLED) 
		self.input['button'].grid(row=6)

	def drawInput(self):
		self.input = {}
		self.input['frame'] = Frame(self.frame)
		self.input['label'] = Label(self.input['frame'], text="Input File")
		self.input['label'].grid(row=0, columnspan=2, pady=2)

		self.input['button'] = Button(self.input['frame'], text="Browse", command=self.getInputFilename)
		self.input['text'] = Text(self.input['frame'], width=50, height=1)
		self.input['button'].grid(row=1, padx=2)
		self.input['text'].grid(row=1, column=1, padx=2)

		self.input['frame'].grid(row=2, column=0, pady=2)

	def drawOptions(self):
		self.options = {}
		self.options['frame'] = Frame(self.frame, height=80)
		self.options['label'] = Label(self.options['frame'], text="Options")
		self.options['label'].grid(row=0, pady=2)
		
		self.options['frame'].grid(row=3, column=0, pady=2)

	def drawOutput(self):
		self.output = {}
		self.output['frame'] = Frame(self.frame)
                self.output['label'] = Label(self.output['frame'], text="Output Folder")
                self.output['label'].grid(row=0, columnspan=2, pady=2)

		self.output['button'] = Button(self.output['frame'], text="Browse", command=self.getOutputFoldername)
		self.output['text'] = Text(self.output['frame'], width=50, height=1)
		self.output['button'].grid(row=1, column=0, padx=2)
		self.output['text'].grid(row=1, column=1, padx=2)

		self.output['frame'].grid(row=4, pady=2)

	def drawStatus(self):
		self.status = {}
		self.status['frame'] = Frame(self.frame)

		self.status['text'] = Text(self.status['frame'], width=28, height=1)
		self.status['progress'] = Text(self.status['frame'], width=28, height=1)
		self.status['text'].insert('1.0', "Ready")
		self.status['text'].grid(row=0, column=0, padx=2)
		self.status['progress'].grid(row=0, column=1, padx=2)

		self.status['frame'].grid(row=5, pady=4)

	def getInputFilename(self):
		input_filename = fd.askopenfilename(title="Input File", filetypes=(("XML File", "*.xml"),("All files", "*.*")))
		self.input['text'].delete('1.0')
		self.input['text'].insert('1.0', input_filename)
		self.update()

	def getOutputFoldername(self):
		output_filename = fd.askdirectory(mustexist=True, title="Output Folder")
		self.output['text'].delete('1.0')
		self.output['text'].insert('1.0', output_filename)
		self.update()

        def canRun(self):
                return os.path.isfile(self.input['text'].get('0.0', END).rstrip()) and os.path.isdir(self.output['text'].get('0.0', END).rstrip())

        def update(self):
                if (self.canRun()):
                        self.input['button']['state'] = NORMAL
                else:
                        self.input['button']['state'] = DISABLED

	def run(self):
                infilename = self.input['text'].get('0.0', END).rstrip()
                outfolder = self.output['text'].get('0.0', END).rstrip()
                
                if not os.path.exists(infilename):
                        pass
                else:
                        infile = open(infilename,'r')
                
                outfile = outfolder + "/" + os.path.basename(infilename)
                if outfile.rfind(".xml", len(outfile)-4) != -1:
                        outfile = outfile[0:len(outfile)-3] + "sql"
                self.status['text'].delete('0.0', END)
		self.status['text'].insert('0.0', "Running")
		self.master.update_idletasks()
                Peter.main(infile, outfile, 1, True, True)
                self.status['text'].delete('0.0', END)
		self.status['text'].insert('0.0', "Finished")


root = Tk()

gui = GUIApp(root)

gui.draw()

root.mainloop()
