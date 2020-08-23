#!/usr/local/bin/python

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5 import uic
import sys
import youtube_dl

class App():
  def __init__(self):
    self.app = QApplication(sys.argv)
    self.ui = uic.loadUi('/home/lia/Projects/audio-downloader/interface.ui')
    self.ui.downloadBtn.clicked.connect(self.getVideo)
    self.ui.show()
    sys.exit(self.app.exec())

  def getVideo(self):
    inputValue = self.ui.input.text()
    if (inputValue):
      self.ui.downloaded.addItem(inputValue)
      self.ui.input.setText('')
      self.downloadVideo(inputValue)

  
  def downloadVideo(self, url):
    def progessHook(d):
      if d['status'] == 'finished':
        print('Done downloading, now converting ...')
      if d['status'] == 'downloading':
        value = int(float(d['_percent_str'].replace('%','')))
        self.ui.progress.setValue(value)
        # print(d['filename'], d['_percent_str'], d['_eta_str'])

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
      ydl.download([url])




app = App()






# ui.downloadBtn.clicked.connect(sayHello)

# class Logger(object):
#   def debug(self, msg):
#     pass

#   def warning(self, msg):
#     pass

#   def error(self, msg):
#     print(msg)



