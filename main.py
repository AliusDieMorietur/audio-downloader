#!/usr/local/bin/python

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5 import uic
import sys
import youtube_dl

# Initialize app
class App():
  def __init__(self):
    self.app = QApplication(sys.argv)

    # Get interface path
    path = str(__file__).rsplit('/', 1)[0] + '/interface.ui'
    self.ui = uic.loadUi(path)
    
    # Move window to the center
    screenGeometry = QApplication.desktop().screenGeometry()
    x = int((screenGeometry.width() - self.ui.width()) / 2)
    y = int((screenGeometry.height() - self.ui.height()) / 2)
    self.ui.move(x, y)
    
    # Add button listener
    self.ui.downloadBtn.clicked.connect(self.getVideo)

    self.ui.show()
    sys.exit(self.app.exec())

  def getVideo(self):
    # Get value from input
    inputValue = self.ui.input.text()
    if (inputValue):
      self.ui.input.setText('')
      self.downloadVideo(inputValue)

  
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

    # Video download options
    ydl_opts = {
        'format': 'bestaudio/best',
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


app = App()
