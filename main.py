from PyQt5.QtWidgets import (
    QProgressBar, QWidget,QLabel,QSlider,
    QVBoxLayout,QHBoxLayout,
    QPushButton,QListWidget,
    QGroupBox,QFileDialog,
    QApplication
    )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize,QTimer
from mutagen.mp3 import MP3
from pygame import mixer
import sys,os,time
import stylesheet

mixer.init()
class Player(QWidget):
    count=0
    index=0
    songlength=0
    playing=False
    volume=70
    muteVolume=False
    songlist=[]
    def __init__(self):
        super().__init__()
        self.setFixedSize(450,250)
        self.setWindowTitle('MuzicPlayer')
        self.setWindowIcon(QIcon('Resources\icons8-music-library-48.png'))
        self.setStyleSheet('background-color:black')
        self.GUI()
        self.show()

    def GUI(self):
        self.Widget()
        self.Layout()

    def Widget(self):
        ###  progress bar
        self.progressbar=QProgressBar()
        self.progressbar.setStyleSheet(stylesheet.progressbar_stylesheet)       
        self.progressbar.setTextVisible(False)
        self.progressbar.setMaximumHeight(15)
        self.timer=QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timechanged)

        ### time label 
        self.time_label=QLabel('00:00 / 00:00')

        ### brows button
        self.brows_button=QPushButton()
        self.brows_button.setIcon(QIcon('Resources\\brows.png'))
        self.brows_button.setIconSize(QSize(36,36))
        self.brows_button.clicked.connect(self.brows_song)

        ### replay button
        self.stop_button=QPushButton()
        self.stop_button.setIcon(QIcon('Resources\\stop.png'))
        self.stop_button.setIconSize(QSize(36,36))
        self.stop_button.clicked.connect(self.stopSong)

        ### play button
        self.play_button=QPushButton()
        self.play_button.setIcon(QIcon('Resources\\play.png'))
        self.play_button.setIconSize(QSize(36,36))
        self.play_button.clicked.connect(self.playSong)

        ### next button
        self.next_button=QPushButton()
        self.next_button.setIcon(QIcon('Resources\\next.png'))
        self.next_button.setIconSize(QSize(36,36))
        self.next_button.clicked.connect(self.nextSong)

        ### back button
        self.back_button=QPushButton()
        self.back_button.setIcon(QIcon('Resources\\back.png'))
        self.back_button.setIconSize(QSize(36,36))
        self.back_button.clicked.connect(self.prevSong)

        ## mute_button
        self.mute_button=QPushButton()
        self.mute_button.setIcon(QIcon('Resources\\mute.png'))
        self.mute_button.setIconSize(QSize(36,36))
        self.mute_button.clicked.connect(self.mute)

        ### volume slider
        self.volume_slider=QSlider(Qt.Horizontal)
        self.volume_slider.valueChanged.connect(self.volumeChange)
        self.volume_slider.setValue(70)
        self.volume_slider.setRange(0,100)
        mixer.music.set_volume(0.7)

        ### muzic list
        self.muzic_list=QListWidget()    
        self.muzic_list.setStyleSheet('background-color:#fcc324')
        self.muzic_list.doubleClicked.connect(self.playSong)
        self.muzic_list.setSelectionMode(1)


    def Layout(self):
        self.MainLayout=QVBoxLayout()
        self.TopMainLayout=QVBoxLayout()
        self.TopMainGroupBox=QGroupBox('Muzic player')
        self.TopLayout=QVBoxLayout()
        self.MiddleLayout=QHBoxLayout()
        self.BottomMainLayout=QHBoxLayout()

        ###Top layout setting widget 
        self.TopLayout.addStretch()
        self.TopLayout.addWidget(self.progressbar)
        self.TopLayout.addWidget(self.time_label)
        
        ### Middle lay out Attribute and wideget
        self.MiddleLayout.addWidget(self.brows_button)
        self.MiddleLayout.addWidget(self.stop_button)
        self.MiddleLayout.addWidget(self.play_button)
        self.MiddleLayout.addWidget(self.back_button)
        self.MiddleLayout.addWidget(self.next_button)
        self.MiddleLayout.addWidget(self.volume_slider)
        self.MiddleLayout.addWidget(self.mute_button)

        ### Top MainLayout setting layout and group box
        self.TopMainGroupBox.setLayout(self.TopMainLayout)
        self.TopMainGroupBox.setStyleSheet("background-color:#fcc324")
        self.TopMainLayout.addLayout(self.TopLayout)
        self.TopMainLayout.addLayout(self.MiddleLayout)

        ### Bottom Main layout widget 
        self.BottomMainLayout.addWidget(self.muzic_list)

        ### Main Layout setting wideget and layouot
        self.MainLayout.addWidget(self.TopMainGroupBox)
        self.MainLayout.addLayout(self.BottomMainLayout)

        ### self window
        self.setLayout(self.MainLayout)


    def brows_song(self):
        url,ok=QFileDialog.getOpenFileName(self,'add sound','D:\muzic','Sound File (*.mp3)')
        if url not in Player.songlist and ok:
            Player.songlist.append(url)
            self.muzic_list.addItem(os.path.basename(url))
    

    def playSong(self):
        if self.muzic_list.currentItem():
            ################### setting index for playing song##################
            Player.index=self.muzic_list.currentRow()
            self.play()


    def play(self):
        if Player.playing:
            self.stopSong()
            Player.playing=False

        url=self.songlist[Player.index]
        mixer.music.load(url)
        mixer.music.play()
        sound=MP3(url)
        Player.songlength=int(sound.info.length)
        Player.playing=True
        self.timer.start()
        self.TopMainGroupBox.setTitle(os.path.basename(url))
        self.progressbar.setValue(0)
        self.progressbar.setRange(0,int(Player.songlength))


    def prevSong(self):
        if Player.playing and Player.songlist.__len__()!=1:
            Player.index-=1
            if Player.index==-1:
                Player.index=Player.songlist.__len__()-1
            self.play()


    def nextSong(self):
        if Player.playing and Player.songlist.__len__()!=1:
            Player.index+=1
            if Player.index==Player.songlist.__len__():
                Player.index=0
            self.play()


    def stopSong(self):
        mixer.music.stop()
        self.timer.stop()
        Player.count=0
        Player.length=0
        Player.playing=False
        self.time_label.setText('00:00 / 00:00')


    def volumeChange(self):
        mixer.music.set_volume(self.volume_slider.value()/100.0)
        icon=None
        if self.volume_slider.value()>0:
            icon=QIcon('Resources\\volume-up.png')
        else:
            icon=QIcon('Resources\mute.png')

        self.mute_button.setIcon(icon)
        

    def timechanged(self):
        strtime=time.strftime('%M:%S',time.gmtime(Player.songlength))
        if Player.count<Player.songlength:
            self.progressbar.setValue(Player.count)
            self.time_label.setText(f"{time.strftime('%M:%S',time.gmtime(Player.count))} /{strtime}")
            Player.count+=1
        else:
            self.timer.stop()
            Player.count=0
            Player.length=0
            Player.playing=False
            self.time_label.setText('00:00 / 00:00')


    def mute(self):
        if not Player.muteVolume:
            Player.muteVolume=True
            Player.volume=self.volume_slider.value()
            mixer.music.set_volume(0)
            self.volume_slider.setValue(0)
            self.mute_button.setIcon(QIcon('Resources\\mute.png'))
        else:
            Player.muteVolume=False
            mixer.music.set_volume(Player.volume)
            self.volume_slider.setValue(Player.volume)
            self.mute_button.setIcon(QIcon('Resources\\volume-up.png'))
            

def main():
    app=QApplication(sys.argv)
    window=Player()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
