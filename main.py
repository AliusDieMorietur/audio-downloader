#! /usr/bin/env python3

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QPushButton, QInputDialog, QMainWindow
from PyQt5 import uic
from os import path 
import sys
import re
import youtube_dl

# Initialize app
class Ui(QMainWindow):
  def __init__(self):
    super(Ui, self).__init__()
    if path.exists(sys.path[0] + '/path'):
      self.path = open(sys.path[0] + '/path', 'r').read()
    else: 
      self.path = ''
    # Get interface path
    print(self.path)
    print(sys.path[0])
    self.ui = uic.loadUi(sys.path[0] + '/interface.ui')
    
    # Move window to the center
    screenGeometry = QApplication.desktop().screenGeometry()
    x = int((screenGeometry.width() - self.ui.width()) / 2)
    y = int((screenGeometry.height() - self.ui.height()) / 2)
    self.ui.move(x, y)
    
    # Add button listener
    self.ui.downloadBtn.clicked.connect(self.getVideo)

    if self.path == '':  
      filePath = self.showDialog()
      self.path = filePath
      file = open('path', 'w')
      file.write(filePath)

    self.ui.show()

  def showDialog(self):
    text, ok = QInputDialog.getText(self.ui, 'Input Dialog', 'Enter path to download folder')
    if ok:
      return str(text)
    return None  

  def getVideo(self):

    # Get value from input
    inputValue = self.ui.input.text()

    # Check if url is valid 
    regularExp = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    valid = re.match(regularExp, inputValue)
    if (valid):
      self.downloadVideo(inputValue)
    self.ui.input.setText('')

  
  def downloadVideo(self, url):
    # Video download progress hook
    def progessHook(d):
      if d['status'] == 'finished':
        print('Done downloading, now converting ...')
      if d['status'] == 'downloading':
        value = int(float(d['_percent_str'].replace('%','')))
        # Pass value to progress bar
        self.ui.progress.setValue(value)
        # print(d['filename'], d['_percent_str'], d['_eta_str'])

    print(self.path)

    # Video download options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': self.path + '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progessHook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      # Add track name to list
      meta = ydl.extract_info(url, download=False) 
      self.ui.downloaded.addItem(meta['title'])
      # Start download
      ydl.download([url])

app = QApplication(sys.argv)
window = Ui()
app.exec_()
