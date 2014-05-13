#!/usr/bin/python

from Tkinter import *
import tkFileDialog as fd

import argparse
import os.path

import app

class GUIApp:

	def __init__(self, master):

		self.frame = Frame(master)
		self.frame.grid(padx=20, pady=15)
		self.title = Label(self.frame, text="Peter", font=("Arial",24))
		self.desc = Label(self.frame, text="UK Data Archive CodeBook to Caddies Parser")
		self.title.grid()
		self.desc.grid(row=1, pady=10)

	def draw(self):
		self.drawInput();
		self.drawOptions();
		self.drawOutput();
		self.drawStatus();

	def drawInput(self):
		self.input = {}
		self.input['frame'] = Frame(self.frame)

		self.input['button'] = Button(self.input['frame'], text="Browse", command=self.getInputFilename)
		self.input['text'] = Text(self.input['frame'], width=60, height=1)
		self.input['button'].grid(row=0, padx=2)
		self.input['text'].grid(row=0, column=1, padx=2)

		self.input['frame'].grid(row=2,pady=2)

	def drawOptions(self):
		self.options = {}
		self.options['frame'] = Frame(self.frame)
		
		self.options['frame'].grid(row=3,pady=2)

	def drawOutput(self):
		self.output = {}
		self.output['frame'] = Frame(self.frame)

		self.output['button'] = Button(self.output['frame'], text="Browse", command=self.getInputFilename)
		self.output['text'] = Text(self.output['frame'], width=60, height=1)
		self.output['button'].grid(row=0, padx=2)
		self.output['text'].grid(row=0, column=1, padx=2)

		self.output['frame'].grid(row=4, pady=2)

	def drawStatus(self):
		self.status = {}
		self.status['frame'] = Frame(self.frame)

		self.status['text'] = Text(self.status['frame'], width=30, height=1) 
		self.status['text'].insert('1.0', "Ready")
		self.output['text'].grid(row=0, column=0, padx=2)

		self.status['frame'].grid(row=5, pady=2)

	def getInputFilename(self):
		input_filename = fd.askopenfilename(title="Input File", filetypes=(("XML File", "*.xml"),("All files", "*.*")))
		self.input['text'].delete('1.0')
		self.input['text'].insert('1.0', input_filename)

	def getOutputFoldername(self):
		self.output_filename = fd.askdirectory(mustexist=true, title="Output Folder")


root = Tk()

app = GUIApp(root)

app.draw()

root.mainloop()
