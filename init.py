import os, sys, inspect, thread, time

sys.path.insert(0, "/Users/abhid/Desktop/LeapSDK/lib")

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import random

from Tkinter import *
from PIL import ImageTk, Image
import os
from playsound import playsound
import string

####################################
# init
####################################

def init(data):
    # There is only one init, not one-per-mode
    data.mode = "HomeScreen"
    data.start=False
    data.level=1
    data.playerList=['Stuart Binny','Ross Taylor','Chris Lynn',\
    'Shikhar Dhawan','Jofra Archer',\
    'Rohit Sharma', 'Lasith Malinga','Ben Stokes', 'Jonny Bairstow',\
    'KL Rahul', 'Shahid Afridi','Glenn Maxwell', 'Hardik Pandya', \
    'Virat Kohli','Dwayne Bravo']
    data.upgradePlayerList=['Jos Butler','Andre Russell','David Warner',\
    'Steve Smith','Kane Williamson',\
    'Chris Gayle','Rashid Khan', 'MS Dhoni']
    loadPlayerImages(data) # player images taken from cricbuzz.com
    data.selectedPlayerList=[]
    data.timeCount=0
    data.score=0
    data.level=1
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.wickets=0
    data.target=0
    data.team='CMU'
    data.player= data.playerList[0]
    data.playerScore=0
    data.balls=0
    data.lastBall=0
    data.fill='Red'
    data.centerX=0.8*data.width
    data.centerY=0.5*data.height
    data.stadiumImg=ImageTk.PhotoImage(Image.open('stadium.jpg')) #mspaint
    data.background=ImageTk.PhotoImage(Image.open('loginbg.jpg')) 
    #picture taken from https://www.pinterest.com/pin/822892163138724302/
    data.win=ImageTk.PhotoImage(Image.open('win.jpg'))
    #picture taken from https://www.123rf.com/stock-photo/congratulations_background.html?sti=m6px6tjwliv0btdkuf
    data.loss=ImageTk.PhotoImage(Image.open('loss.jpg')) 
    #picture taken from https://nature.desktopnexus.com/wallpaper/2316631/
    data.leaderboardImage=ImageTk.PhotoImage(Image.open('Leaderboard.jpg'))
    data.letters=['A','B','D','F',\
    'G','H','I','J','K','L','O','R','S',"T",'U','V','W','Y','X']
    data.curLetter=random.choice(data.letters)
    data.letterSets= \
    [['A','E','M','N','S','T','L','O','Y'],['P','H','G','R','U','V','W','K'],\
    ['D','I','J','X','Y','Q','Z']]
    loadLetterImages(data) #letter images taken from supercoloring.com/asl
    loadUpgradeImages(data) #cricbuzz.com
    data.curSet=[]
    data.user=""
    data.curImg=data.letterImages[data.letters.index(data.curLetter)]
    data.password=""
    data.lastMode=''
    data.FalseRegister=False
    data.clickedUser=False
    data.clickedPass=False
    data.wrongPass=False
    data.path="UserData.txt"
    data.highscore=0
    data.movement=(data.width*0.02)
    data.actionCount=0
    data.mf=ImageTk.PhotoImage(Image.open('Help.png'))
    data.batter=ImageTk.PhotoImage(Image.open('cick.png'))
    data.waiter=ImageTk.PhotoImage(Image.open('batting.png'))
    data.sixer=ImageTk.PhotoImage(Image.open('fric.png'))
    #the three images above were taken from https://www.istockphoto.com/photos/cricket
    data.inAction=False
    data.inPlay=False
    data.moveY=0 
    data.innings='1st'
    data.leaderboard=getHighScoreList(data)
    data.playerLetter=[]
    data.status='Loss'
    data.ballSpeed=20
    
    

####################################
# mode dispatcher (citation: concept taken from 112 course website)
####################################

def mousePressed(event, data):
    if (data.mode == "HomeScreen"): HomeScreenMousePressed(event, data)
    elif (data.mode == "HelpScreen"):   HelpMousePressed(event, data)
    elif (data.mode == "Learn"):       LearnPlayMousePressed(event, data)
    elif (data.mode == "Selection"):       SelectionMousePressed(event, data)
    elif (data.mode == "GamePlay"):       GamePlayMousePressed(event, data)
    elif (data.mode == "TwoPlayer"):   TwoPlayerMousePressed(event, data)
    elif (data.mode == "LogIn"):           LogInMousePressed(event,data)
    elif (data.mode == "SignUp"):           SignUpMousePressed(event,data)
    elif (data.mode == "GameSelection"):  GameSelectionMousePressed(event,data)
    elif (data.mode) == "GameOver":        GameOverMousePressed(event,data)
    elif (data.mode == "Leaderboard"):     LeaderboardMousePressed(event,data)
    elif (data.mode == "UpgradePlayers"):UpgradePlayersMousePressed(event,data)
    
def keyPressed(event, data):
    if (data.mode == "HomeScreen"): HomeScreenKeyPressed(event, data)
    elif (data.mode == "HelpScreen"):   HelpKeyPressed(event, data)
    elif (data.mode == "Learn"):       LearnPlayKeyPressed(event, data)
    elif (data.mode == "Selection"):    SelectionKeyPressed(event, data)
    elif (data.mode == "GamePlay"):       GamePlayKeyPressed(event, data)
    elif (data.mode == "TwoPlayer"):       TwoPlayerKeyPressed(event, data)
    elif (data.mode == "LogIn"):           LogInKeyPressed(event,data)
    elif (data.mode == "SignUp"):           SignUpKeyPressed(event,data)
    elif (data.mode == "GameSelection"):    GameSelectionKeyPressed(event,data)
    elif (data.mode == "GameOver"):       GameOverKeyPressed(event,data)
    elif (data.mode == "Leaderboard"):        LeaderboardKeyPressed(event,data)
    elif (data.mode == "UpgradePlayers"):  UpgradePlayersKeyPressed(event,data)
 
def timerFired(data):
    if (data.mode == "HomeScreen"): HomeScreenTimerFired(data)
    elif (data.mode == "HelpScreen"):   HelpTimerFired(data)
    elif (data.mode == "Learn"):       LearnPlayTimerFired(data)
    elif (data.mode == "Selection"):       SelectionTimerFired(data)
    elif (data.mode == "GamePlay"):       GamePlayTimerFired(data)
    elif (data.mode == "TwoPlayer"):       TwoPlayerTimerFired(data)
    elif (data.mode == "LogIn"):           LogInTimerFired(data)
    elif (data.mode == "SignUp"):           SignUpTimerFired(data)
    elif (data.mode == "GameSelection"):      GameSelectionTimerFired(data)
    elif (data.mode == "GameOver"):              GameOverTimerFired(data)
    elif (data.mode == "Leaderboard"):          LeaderboardTimerFired(data)
    elif (data.mode == "UpgradePlayers"): UpgradePlayersTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "HomeScreen"): HomeScreenRedrawAll(canvas, data)
    elif (data.mode == "HelpScreen"):   HelpRedrawAll(canvas, data)
    elif (data.mode == "Learn"):       LearnPlayRedrawAll(canvas, data)
    elif (data.mode == "Selection"):       SelectionRedrawAll(canvas, data)
    elif (data.mode == "GamePlay"):       GamePlayRedrawAll(canvas, data)
    elif (data.mode == "TwoPlayer"):       TwoPlayerRedrawAll(canvas, data)
    elif (data.mode == "LogIn"):           LogInRedrawAll(canvas,data)
    elif (data.mode == "SignUp"):           SignUpRedrawAll(canvas,data)
    elif (data.mode == "GameSelection"):    GameSelectionRedrawAll(canvas,data)
    elif (data.mode) == "GameOver":          GameOverRedrawAll(canvas,data)
    elif (data.mode == "Leaderboard"):      LeaderboardRedrawAll(canvas,data)
    elif (data.mode == "UpgradePlayers"): UpgradePlayersRedrawAll(canvas,data)
    

####################################
# LogIn mode #idea for using clickedPass and clickedUser taken from https://github.com/ankitaku2019/Term-Project-Open-CV/blob/master/logIn.py
####################################

def LogInMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        data.mode=data.lastMode
    if data.width//4<event.x<0.75*data.width and \
    0.25*data.height<event.y<0.375*data.height:
        data.clickedPass=False
        data.clickedUser=True
    elif data.width//4<event.x<0.75*data.width and \
    0.5*data.height<event.y<0.625*data.height:
        data.clickedUser=False 
        data.clickedPass=True
    elif data.width//4<event.x<0.75*data.width and \
    0.80*data.height<event.y<0.90*data.height: 
        if login(data)==False: 
            data.wrongPass=True
        else: 
            data.wrongPass=False
            data.mode="Selection" 

def LogInRedrawAll(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image=data.background)
    
    #creates the background
    
    if data.wrongPass==True:
        canvas.create_text(data.width//2,data.height*0.2,\
        text="Please enter valid login details",\
        fill="white",font="Arial 22 bold")
    #username and its coressponding rectangle
    canvas.create_text(data.width*0.2, data.height//4+25, anchor="center", \
    text="Username:", font="Arial 22 bold", fill="white")
    
    canvas.create_rectangle(0.37*data.width, data.height//4, 0.75*data.width, 0.375*data.height, outline="white", width=7)
    
    #types username for the letters you type in 
    canvas.create_text(data.width*0.56, 0.3125*data.height, \
    font="Helvetica 30 bold", text=data.user)
    
    #password and its corresponding rectangle
    
    canvas.create_text(data.width*0.2, 0.55*data.height, anchor="center", \
    text="Password:", font="Arial 22 bold", fill="white")
    
    canvas.create_rectangle(0.37*data.width, 0.5*data.height, 0.75*data.width, 0.625*data.height, outline="white", width=7)
    
    #types the password that someone types in 
    canvas.create_text(data.width * 0.56, 0.5625*data.height, \
    text=len(data.password)*'*', font="Arial 30 bold",fill='red')
    
    #GO and its corresponding rectangle
    canvas.create_rectangle(data.width*0.37, 0.80*data.height, 0.75*data.width, 0.90*data.height, fill="Red")
    canvas.create_text((data.width*0.56), 0.85*data.height, anchor="center", \
    text="Play", font="Arial 30 bold", fill="White")
    
    #Page Title
    canvas.create_text((data.width*0.5), 0.1*data.height, anchor="center", \
    text="Log In", font = ('Comic Sans MS',30), fill="white")
    
    #BackButton
    
    canvas.create_rectangle(0, 0, 0.25*data.width, 0.1*data.height, fill="Red")
    canvas.create_text((data.width*0.125), 0.05*data.height, anchor="center", \
    text="Back", font="Arial 20 bold", fill="White")
    

def LogInKeyPressed(event, data):
    #draws and checks if user  clicked in box
    if event.char in string.ascii_letters or event.char in string.digits \
    or event.char in string.punctuation==True: 
        if data.clickedUser==True: 
            data.user+=event.char
        if data.clickedPass==True:
            data.password+=event.char
    elif event.keysym=="BackSpace":
        if data.clickedUser==True: 
            data.user=data.user[:-1]
        elif data.clickedPass==True: 
            data.password=data.password[:-1]
    if event.keysym=='q':
        data.mode='Selection'

def LogInTimerFired(data):
    pass

####################################
# SignUp mode
####################################

def SignUpMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        data.mode=data.lastMode
    if data.width//4<event.x<0.75*data.width and \
     0.25*data.height<event.y<0.375*data.height:
        data.clickedPass=False
        data.clickedUser=True
    elif data.width//4<event.x<0.75*data.width and \
    0.5*data.height<event.y<0.625*data.height:
        data.clickedUser=False 
        data.clickedPass=True
    elif data.width//4<event.x<0.75*data.width and \
    0.80*data.height<event.y<0.90*data.height:
        if register(data)==False:
            data.FalseRegister=True
        else: data.mode='Selection'
        

def SignUpRedrawAll(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image=data.background)
    
    
    #creates the background
    
    
    #username and its coressponding rectangle
    canvas.create_text(data.width*0.56, data.height//4 - 25, anchor="center", \
     text="Create New Username:", font="Arial 22 bold", fill="white")
    
    canvas.create_rectangle(0.37*data.width, data.height//4, 0.75*data.width, 0.375*data.height, outline="white", width=7)
    
    #types username for the letters you type in 
    canvas.create_text(data.width*0.56, 0.3125*data.height , \
    font="Helvetica 24 bold", text=data.user, fill='white')
    
    #password and its corresponding rectangle
    canvas.create_text(data.width*0.56, 0.5*data.height -20 , \
    anchor="center", text="Create New Password:", \
    font="Arial 22 bold", fill="white")
    
    canvas.create_rectangle(0.37*data.width, 0.5*data.height, 0.75*data.width, 0.625*data.height, outline="white", width=7)
    
    #types the password that someone types in 
    canvas.create_text(data.width * 0.56, 0.5625*data.height,\
    text=len(data.password)*'*', font="Arial 30 bold",fill='red')
    
    #GO and its corresponding rectangle
    canvas.create_rectangle(data.width*0.37, 0.80*data.height, 0.75*data.width, 0.90*data.height, fill="Red")
    canvas.create_text((data.width*0.56), 0.85*data.height, \
    anchor="center", text="Play", font="Arial 30 bold", fill="White")
    
    #Page Title
    canvas.create_text((data.width*0.5), 0.1*data.height, \
    anchor="center", text="Sign Up", font = ('Comic Sans MS',40), fill="white")
    
    canvas.create_rectangle(0, 0, 0.25*data.width, 0.1*data.height, fill="Red")
    canvas.create_text((data.width*0.125), \
    0.05*data.height, anchor="center", text="Back", \
    font="Arial 20 bold", fill="White")
    
    if data.FalseRegister==True:
        canvas.create_text((data.width*0.5), 0.75*data.height, \
        anchor="center", text="Please change username/password", \
        font="Arial 20 bold", fill="White")
    
   
def SignUpKeyPressed(event, data):
    if event.char in string.ascii_letters or event.char in string.digits \
    or event.char in string.punctuation==True: 
        if data.clickedUser==True: 
            data.user+=event.char
        if data.clickedPass==True:
            data.password+=event.char
    elif event.keysym=="BackSpace":
        if data.clickedUser==True: 
            data.user=data.user[:-1]
        elif data.clickedPass==True: 
            data.password=data.password[:-1]
    

def SignUpTimerFired(data):
    pass

def reset(data):
    #resets all values to initial values
    data.curLetter=random.choice(data.letters)
    data.curImg=data.letterImages[data.letters.index(data.curLetter)]
    data.movement=(data.width*0.02)
    data.actionCount=0
    data.timeCount=0
    data.inAction=False
    data.inPlay=False
    data.start=False
    data.moveY=0 
    data.innings='1st'
    data.score=0
    data.level=1
    data.wickets=0
    data.balls=0
    data.centerX=0.8*data.width
    data.centerY=data.height//2
    
    

####################################
# HomeScreen mode
####################################

import string

def HomeScreenMousePressed(event, data): 
    if 0.125*data.width<event.x<0.375*data.width and 0.75*data.height<event.y<0.875*data.height: 
            data.mode="LogIn"
            data.lastMode="HomeScreen"
    elif 0.625*data.width<event.x<0.875*data.width and 0.75*data.height<event.y<0.875*data.height: 
            data.mode="SignUp"
            data.lastMode="HomeScreen"
        
def HomeScreenKeyPressed(event, data): 
    pass

def HomeScreenRedrawAll(canvas, data): 
    canvas.create_image(data.width//2, data.height//2, image=data.background)
    canvas.create_text(0.5*data.width,0.20*data.height, \
    text="Sign Cricket", font=('Symbol', '50', 'bold italic'), fill='blue')
     #the login and signup buttons are created below
    canvas.create_rectangle(data.width//8, 0.75*data.height, 0.375*data.width, 0.875*data.height, fill="old lace")
    canvas.create_text(0.25*data.width,0.80*data.height, \
    text="Log In", font="Arial 16")
    canvas.create_rectangle(0.625*data.width, 0.75*data.height, \
    0.875*data.width, 0.875*data.height, fill="old lace")
    canvas.create_text(0.75*data.width, 0.80*data.height, \
    text="Sign Up", font="Arial 16")

def HomeScreenTimerFired(data):
    pass
    
####################################
# GameSelection mode
####################################

import string
def GameSelectionMousePressed(event, data): 
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        data.mode=data.lastMode
    if 0.333*data.width<event.x<0.666*data.width:
        if 0.25*data.height<event.y<0.35*data.height:
            data.lastMode='GameSelection'
            data.mode="Learn"
        if 0.45*data.height<event.y<0.55*data.height:
            data.target=random.randint(30,50)
            data.lastMode='GameSelection'
            data.mode="GamePlay"
        if 0.65*data.height<event.y<0.75*data.height:
            data.lastMode='GameSelection'
            data.mode="TwoPlayer"
        
def GameSelectionKeyPressed(event, data): 
    if event.keysym.lower()=='h':
        data.mode='HelpScreen'
    if event.keysym.lower()=='l':
        getHighScoreList(data)
        data.mode='Leaderboard'
    if event.keysym.lower()=='u':
        data.mode='UpgradePlayers'
    pass

def GameSelectionRedrawAll(canvas, data): 
    canvas.create_image(data.width//2, data.height//2, image=data.background)
     #the login and signup buttons are created below
     
    canvas.create_text((data.width*0.5), 0.15*data.height, \
    anchor="center", text="Select Your Game", \
    font = ('Comic Sans MS',30), fill="white")
     
    canvas.create_rectangle(2*data.width//6, 0.25*data.height, 4*data.width//6, 0.35*data.height, fill="old lace")
    
    canvas.create_rectangle(2*data.width//6, 0.45*data.height, 4*data.width//6, 0.55*data.height, fill="old lace")
    
    canvas.create_rectangle(2*data.width//6, 0.65*data.height, 4*data.width//6, 0.75*data.height, fill="old lace")
    
    canvas.create_text(0.5*data.width,0.3*data.height, \
    text="Learn", font="Arial 16")
    
    canvas.create_text(0.5*data.width, 0.5*data.height, \
    text="Competitive", font="Arial 16")
    
    canvas.create_text(0.5*data.width, 0.7*data.height, \
    text="Two Player", font="Arial 16")
    
    canvas.create_text(0.5*data.width, 0.9*data.height, \
    text="Press 'H' for help", font="Arial 20", fill='white')
    canvas.create_text(0.5*data.width, 0.85*data.height,\
     text="Press 'L' to look at the leaderboard", font="Arial 20", fill='white')
    canvas.create_text(0.5*data.width, 0.8*data.height,\
     text="Press 'U' to check out player upgrades", \
     font="Arial 20", fill='white')
    
    canvas.create_rectangle(0, 0, 0.25*data.width, 0.1*data.height, fill="Red")
    canvas.create_text((data.width*0.125), 0.05*data.height, \
    anchor="center", text="Back", font="Arial 20 bold", fill="White")
    
    canvas.create_rectangle(0.60*data.width,0,data.width, \
    0.1*data.height, fill="Blue")
    canvas.create_text((data.width*0.80), 0.05*data.height,\
     anchor="center", text=data.user+ " HS: "+ str(data.highscore) , \
     font="Arial 20 bold", fill="White")
    

def GameSelectionTimerFired(data):
    pass

    
####################################
# ImageLoading 
####################################

def loadPlayerImages(data):
    #loads player images
    #idea taken from 15-112 website about using images
    data.playerImages = [ ]
    for player in data.playerList:
        name = player.replace(' ','')
        filename = "player-name/%s.jpg" % (name)
        img = ImageTk.PhotoImage(Image.open(filename))
        data.playerImages.append(img)

def loadLetterImages(data):
    #loads letter images
    data.letterImages = [ ]
    for letter in data.letters:
        filename = "letters/%s.jpg" % (letter)
        img = ImageTk.PhotoImage(Image.open(filename))
        data.letterImages.append(img)

def loadUpgradeImages(data):
    #loads upgraded player images
    data.upgradePlayerImages = [ ]
    for player in data.upgradePlayerList:
        name = player.replace(' ','')
        filename = "player-name/%s.jpg" % (name)
        img = ImageTk.PhotoImage(Image.open(filename))
        data.upgradePlayerImages.append(img)

####################################
# Selection mode
####################################


def SelectionMousePressed(event, data):
    if event.y in range(60,315) and event.x<470:
        num=calcPosition(event.x,event.y-60)
        if int(num) not in data.selectedPlayerList :
            if len(data.selectedPlayerList)<5:
                data.selectedPlayerList.append(int(num))
        else: data.selectedPlayerList.remove(int(num))
    pass

def calcPosition(x,y):
    #calculates mouse press
    return(x//95 + 5*(y//95))

def SelectionKeyPressed(event, data):
    if event.keysym=='Return' and len(data.selectedPlayerList)==5:
        data.lastMode="Selection"
        data.mode='GameSelection'
    if event.keysym=='l':
        data.selectedPlayerList=[1,2,3,4,5]

def SelectionTimerFired(data):
    pass

def SelectionRedrawAll(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image=data.background)
    margin = 20
    (left, top) = (margin, 60)
    for rank in range(len(data.playerImages)):
        image =  data.playerImages[rank]
        if (left + image.width() > data.width):
            (left, top) = (margin, top + image.height() + margin)
        canvas.create_image(left, top, anchor=NW, image=image)
        canvas.create_text(left+40,top+85,text=data.playerList[rank], \
        fill='white')
        left += image.width() + margin
    canvas.create_text(data.width/2, 20, \
    text='Click on 5 players to select/deselect them from your team', \
    font="Arial 18 bold", fill='white')
    canvas.create_text(data.width/2, 360, \
    text='Your Team: (Press Enter to continue)', font="Arial 24 bold")
    (left, top) = (margin, 385)
    for rank in (data.selectedPlayerList):
        image =  data.playerImages[rank]
        if (left + image.width() > data.width):
            (left, top) = (margin, top + image.height() + margin)
        canvas.create_image(left, top, anchor=NW, image=image)
        canvas.create_text(left+40,top+85,text=data.playerList[rank], \
        fill='white')
        left += image.width() + margin

####################################
# Drawing Stadium
####################################
def createPitch(canvas,data):
    #creates pitch 

    canvas.create_image(data.width//2, data.height*0.5, image=data.stadiumImg)
    if data.start==False and data.innings=="1st" and data.mode != "TwoPlayer":
        canvas.create_text(data.width*0.5,data.height*0.12,text= \
        "Please press 'p' to start/pause", font="Helvetica 18",fill='white')
        canvas.create_text(data.width*0.5,190,text= \
        "Put a fist above the leap motion to start", font="Helvetica 18",fill='white')
        canvas.create_text(data.width*0.5,data.height*0.8,\
        text= "Place a fist above the leap motion to start", font="Helvetica 18",fill='white')
    canvas.create_oval(data.centerX+5,data.centerY+5,data.centerX-5,\
    data.centerY-5, fill='white')
    canvas.create_text(data.width//2,data.height//4,text=data.curLetter,\
    font="Arial 30 bold")

    
def createScorecard(canvas,data):
    #creates scorecard
    score=data.score
    wickets=data.wickets
    team=data.team
    canvas.create_rectangle(data.width*(0.333),\
    data.height*0.85,data.width*0.666,data.height*0.925,fill='gray')
    canvas.create_rectangle(data.width*(0),\
    data.height*0.85,data.width*0.333,data.height*0.925,fill=data.fill)
    canvas.create_rectangle(data.width*(0.666),\
    data.height*0.85,data.width,data.height*0.925,fill='gray')
    canvas.create_rectangle(data.width*(0.333),\
    data.height*0.925,data.width*0.666,data.height,fill='white')
    canvas.create_rectangle(data.width*(0.666),\
    data.height*0.925,data.width,data.height,fill='white')
    canvas.create_text(data.width*0.5,\
    data.height*0.8875,text= team+": " + str(score) + "-" + str(wickets), \
    font="Helvetica 16")
    if data.wickets <5:
        curPlayerIndex=data.selectedPlayerList[data.wickets]
        canvas.create_image(data.width//2, data.height*0.65, image=data.playerImages[curPlayerIndex])
        canvas.create_text(data.width*(0.833),data.height*0.9625,text= data.playerList[curPlayerIndex]+"   " + str(data.playerScore))
    if data.mode=='GamePlay':
        canvas.create_text(data.width*(0.5),data.height*0.9625,text= "Need " + str(data.target-score) + " in " + str(24-data.balls))
        canvas.create_rectangle(data.width*(0),data.height*0.925,\
        data.width*0.333,data.height,fill='white')
        canvas.create_text(data.width*(0.165),data.height*0.9625,\
        text= "Level: " + str(data.level))
    if data.fill=='Red':
        canvas.create_text(data.width*(0.165),data.height*0.8875,\
    text="Leap Motion Off")
    else:         canvas.create_text(data.width*(0.165),data.height*0.8875,\
    text="Leap Motion On")
        
        
    if data.mode=='Learn':
         canvas.create_text(data.width*(0.5),data.height*0.9625,\
         text=str(12-data.balls) +" letters remaining")
    if data.mode=='TwoPlayer' and data.innings=='1st':
        canvas.create_text(data.width*(0.5),data.height*0.9625,\
        text=str(12-data.balls) +" balls remaining")
    if data.mode=='TwoPlayer' and data.innings=='2nd':
        canvas.create_text(data.width*(0.5),data.height*0.9625,text= "Need " + str(data.target-score) + " in " + str(12-data.balls))
        
    canvas.create_text(data.width*(0.833),data.height*0.8875,\
    text="Last Ball:  " + str(data.lastBall))
    canvas.create_rectangle(0, 0, 0.25*data.width, 0.1*data.height, fill="Red")
    canvas.create_text((data.width*0.125), 0.05*data.height, \
    anchor="center", text="Back", font="Arial 20 bold", fill="White")
    
    canvas.create_rectangle(0.60*data.width,0,data.width, \
    0.1*data.height, fill="Blue")
    canvas.create_text((data.width*0.80), 0.05*data.height, \
    anchor="center", text=data.user+ " HS: "+ str(data.highscore) , \
    font="Arial 20 bold", fill="White")
    if data.inAction==True:
        canvas.create_text(data.width*(0.50),data.height*0.50,\
        text=str(data.lastBall), font="Arial 50 bold", fill="Red")
        if data.lastBall=='':
            canvas.create_text(data.width*(0.50),data.height*0.50,\
            text='Hand Not Recognized', font="Arial 25 bold", fill="Black")
            canvas.create_text(data.width*(0.50),data.height*0.80,\
            text="Shake your hand in front of Leap Motion tomake sure it's recognized", font="Arial 14", fill="White")
    canvas.create_line(201,286,201,216,fill='black',width=3)
    if data.lastBall==6 and data.inAction:
        canvas.create_image(200, 245, image=data.sixer)
    elif data.lastBall==2 and data.inAction:
        canvas.create_image(200, 245, image=data.batter)
    
    else:
        canvas.create_image(200, 245, image=data.waiter)

####################################
# GamePlay mode
####################################

def GamePlayMousePressed(event, data):
    #print(data.timeCount)
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        reset(data)
        data.mode=data.lastMode
        data.lastMode='Selection'

def GamePlayKeyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym.lower()=='p':
        data.start= not data.start
    elif event.keysym=='b':
        data.balls=24
    elif event.keysym=='o':
        data.wickets+=1
    elif event.keysym=='t':
        data.score=data.target
    elif int(event.keysym) in range(0,10):
        data.score += int(event.keysym)
        

def GamePlayTimerFired(data):
    #print(data.timeCount,data.actionCount)
    updateLeapMotionData(data)
    startHand(data)
    if data.start==True:
        if data.inAction==False:
            data.timeCount+=1
        else: data.actionCount+=1
        data.centerX-=data.movement
        data.centerY+=data.moveY
        updateLeapMotionData(data)
        printLeapMotionData(data)

def GamePlayRedrawAll(canvas, data):
    createPitch(canvas,data)
    createScorecard(canvas,data)

####################################
# MoveCalculation mode
####################################

def updateLeapMotionData(data):
    data.frame = data.controller.frame()

def printLeapMotionData(data):
    #checks for letter and  calculates score
    frame = data.frame
    data.playerLetter=getLetter(data)
    curPlayerIndex=data.selectedPlayerList[data.wickets]
    getBallSpeed(data)
    if data.timeCount==data.ballSpeed-1:
        playsound("hit.wav",block=False)
        #audio from https://www.audioblocks.com/royalty-free-audio/cricket+bat+hitting+ball
        
    if data.timeCount==data.ballSpeed:
        calculateMove(data)
        data.curLetter=random.choice(data.letters)
        data.curImg=data.letterImages[data.letters.index(data.curLetter)]
        for set in data.letterSets:
            if data.curLetter in set:
                data.curSet= set
        if data.mode=="TwoPlayer":
            data.curLetter=""
        data.inAction=True
        data.timeCount=0
        #print(data.curSet,data.curLetter)
    if data.inAction==True:
        if data.lastBall==0 or data.lastBall=='':
            data.movement=0.005*data.width
            data.moveY=-0.02*data.width
        if data.lastBall==2 or data.lastBall==4:
            data.movement=-0.03*data.width
            data.moveY=-0.02*data.width
        if data.lastBall==6:
            data.movement=-0.07*data.width
            data.moveY=0.02*data.width
            playsound('Applause.wav',block=False)
            #sound from http://soundbible.com/tags-clapping.html
        if data.lastBall=='W':
            data.movement=0.003*data.width
            data.moveY=-0.00*data.width

    if data.actionCount==10:
        data.centerY=0.5*data.height
        data.centerX=0.8*data.width
        data.movement=0.02*data.width * data.level
        data.moveY=0
        data.inAction=False
        data.actionCount=0
        data.ballSpeed=20 // data.level
        if data.mode=='TwoPlayer':
            data.inPlay=False
    
    if data.score>=data.target and data.mode=='Competitive':
        data.level+=1
        data.status='Win'
        changeLevel(data)
        data.mode='GameOver'
   
def calculateMove(data):
    #calculates score at end of each ball
    curPlayerIndex=data.selectedPlayerList[data.wickets]
    letter=data.playerLetter
    if letter==None or letter==[] :
        data.lastBall=''
    else:
        data.balls+=1
        if data.curLetter in letter:
            data.score+=6
            data.playerScore+=6
            data.lastBall=6
        elif checkSimilar(letter,data) and data.playerList[curPlayerIndex] in data.upgradePlayerList:
            data.score+=4
            data.playerScore+=4
            data.lastBall=4
        elif checkSimilar(letter,data):
            data.score+=2
            data.playerScore+=2
            data.lastBall=2
        else:
            data.wickets+=1
            data.lastBall='W'
            if data.wickets <=4:
                data.player=data.playerList[data.wickets]
                data.playerScore=0
            if data.mode=="Learn":
                data.balls-=1
 
    if data.mode=='GamePlay':
        if data.score>data.highscore:
            updateHighScore(data)
            data.highscore=data.score
            data.leaderboard=getHighScoreList(data)
        if data.balls==24 or data.wickets==5: 
            data.status='Loss'
            data.mode='GameOver'
    
    if data.mode=='Learn':
        if data.balls==12: 
            print('a')
            data.status='Win'
            data.mode='GameOver'
        if data.wickets==5:
            data.status='Loss'
            data.mode='GameOver'
    
    if data.innings=='1st' and data.balls==12 and data.mode=="TwoPlayer":
        switch(data)
        
####################################
# Helper Functions
####################################

def checkSimilar(letter,data):
    #checks for similar letters
    for l in letter:
        if l in data.curSet:
            return True
    else: return False
    
def changeLevel(data):
    #changes level
    reset(data)
    data.level+=1
    data.target=data.target+data.level * random.randint(15,20)

def switch(data):
    #switches players
    data.balls=0
    data.start=False
    data.wickets=0
    data.target=data.score+1
    data.score=0
    data.curLetter=""
    data.centerX=0.8*data.width
    data.centerY=data.height//2
    data.innings="2nd"
    data.movement=(data.width*0.02)
    data.actionCount=0
    data.inAction=False
    data.moveY=0 
    data.team="UPitt"

def updatePlayers(data):
    #upgrades players
    index=(data.highscore//10)
    for num in range(index):
        data.playerImages[num]=data.upgradePlayerImages[num]
        data.playerList[num]=data.upgradePlayerList[num]

def getBallSpeed(data):
    curPlayerIndex=data.selectedPlayerList[data.wickets]
    if data.playerList[curPlayerIndex] in data.upgradePlayerList:
        data.ballSpeed=40
        data.movement=0.01*data.width

####################################
# Learn mode
####################################

def LearnPlayMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        reset(data)
        data.mode=data.lastMode
        data.lastMode='Selection'
    pass

def LearnPlayKeyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym.lower()=='p':
        data.start= not data.start
    elif event.keysym=='b':
        data.balls=18
    elif event.keysym=='o':
        data.wickets+=1

def LearnPlayTimerFired(data):
    if data.start==True:
        if data.inAction==False:
            data.timeCount+=1
        else: data.actionCount+=1
        data.centerX-=data.movement
        data.centerY+=data.moveY
        updateLeapMotionData(data)
        printLeapMotionData(data)

def LearnPlayRedrawAll(canvas, data):
    createPitch(canvas,data)
    createScorecard(canvas,data)
    if data.curImg !="":
        canvas.create_image(data.width//2, data.height//4, image=data.curImg)

####################################
# TwoPlayer mode
####################################


def TwoPlayerMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        reset(data)
        data.lastMode='Selection'
        data.mode="GameSelection"
    pass

def TwoPlayerKeyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym=='Return':
        data.start= not data.start
    elif (event.keysym).isalpha() and len(event.keysym)==1 and \
    data.inPlay==False and data.inAction==False:
        data.curLetter=event.keysym.upper()
        data.inPlay=True
    

def TwoPlayerTimerFired(data):
    if data.start==True and data.inPlay==True:
        if data.inAction==False:
            data.timeCount+=1
        else: data.actionCount+=1
        data.centerX-=data.movement
        data.centerY+=data.moveY
        updateLeapMotionData(data)
        printLeapMotionData(data)

def TwoPlayerRedrawAll(canvas, data):
    createPitch(canvas,data)
    createScorecard(canvas,data)
    if data.start==False and data.innings=='1st':
        canvas.create_rectangle(data.width*0.10,\
        data.height*0.10,data.width*0.90,data.height*0.4, fill='white')
        canvas.create_text(data.width*0.5,data.height*0.25,\
        text= "The bowling player must use the letters \n on the keyboard to bowl letters \n to the batting player.The batting player must \n then make the correct gesture \n on the leap motion to get points. \n Press 'Enter' to start", \
        font="Helvetica 18",fill='black')
        
    if data.innings=='2nd' and data.start==False:
         canvas.create_text(data.width*0.5,data.height*0.15,\
         text= "Please switch players and chase the target", \
         font="Helvetica 18",fill='white')


####################################
# Help mode
####################################

def HelpMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        reset(data)
        data.mode='GameSelection'
 
def HelpTimerFired(data):
    pass

def HelpRedrawAll(canvas, data):
    canvas.create_image(data.width//2, 2*data.height//3 -30, image=data.mf)
    canvas.create_text((data.width*0.5), 0.05*data.height, \
    anchor="center", text="Help", font = ('Comic Sans MS',30), fill="Red")
    canvas.create_rectangle(0, 0, 0.25*data.width, 0.1*data.height, fill="Red")
    canvas.create_text((data.width*0.125), 0.05*data.height, \
    anchor="center", text="Back", font="Arial 20 bold", fill="White")
    
####################################
# GameOver mode
####################################

def GameOverMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height and data.status=='Loss':
        reset(data)
        data.lastmode='Selection'
        data.mode='GameSelection'

    elif 0<event.x<0.25*data.width \
    and 0*data.height<event.y<0.1*data.height and data.status=='Win':
        data.mode='GamePlay'
 
def GameOverTimerFired(data):
    pass

def GameOverRedrawAll(canvas, data):
    if data.status=='Loss':
        canvas.create_image(data.width//2, data.height//2, image=data.loss)
        canvas.create_text((data.width*0.5), 0.5*data.height,\
         anchor="center", text="You Lost!", \
         font = ('Comic Sans MS',50), fill="white")
        canvas.create_text((data.width*0.5),\
         0.1*data.height, anchor="center", text="Game Over",\
          font = ('Comic Sans MS',50), fill="white")
        canvas.create_rectangle(0, 0, 0.25*data.width, \
        0.1*data.height, fill="Red")
        canvas.create_text((data.width*0.125), \
        0.05*data.height, anchor="center", text="Play Again", \
        font="Arial 20 bold", fill="White")
    else: 
        canvas.create_image(data.width//2, data.height//2, \
        image=data.win)
        canvas.create_text((data.width*0.5), 0.5*data.height, \
        anchor="center", text="You Won!", \
        font = ('Comic Sans MS',50), fill="white")
        canvas.create_text((data.width*0.5), \
        0.5*data.height, anchor="center", text="You Won!", \
        font = ('Comic Sans MS',50), fill="white")
        canvas.create_rectangle(0, 0, 0.25*data.width, \
        0.1*data.height, fill="Red")
        canvas.create_text((data.width*0.125),\
         0.05*data.height, anchor="center", text="Next Level", \
         font="Arial 20 bold", fill="White")
    
    
####################################
# UpgradePlayers mode
####################################

def UpgradePlayersMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        reset(data)
        data.mode='GameSelection'
        data.lastmode='Selection'
    if 0.25*data.width<event.x<0.75*data.width and 0.7*data.height<event.y<0.8*data.height:
        updatePlayers(data)
 
def UpgradePlayersTimerFired(data):
    pass

def UpgradePlayersRedrawAll(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image=data.background)
    margin = 40
    (left, top) = (margin, 90)
    for rank in range(len(data.upgradePlayerList)):
        image =  data.upgradePlayerImages[rank]
        if (left + image.width() > data.width):
            (left, top) = (margin, top + image.height() + 45)
        canvas.create_image(left, top, anchor=NW, image=image)
        canvas.create_text(left+40,top+85,text=data.upgradePlayerList[rank], fill='white',font="Arial 14")
        canvas.create_text(left+40,top+100,text=str((rank+1)*10) + \
        " points", fill='white', font="Arial 14")
        left += image.width() + margin
    canvas.create_text(data.width/2, 70, \
    text="Clear new high Scores to unlock new players!", \
    fill='white',font="Arial 20 bold")
    canvas.create_rectangle(0, 0, 0.25*data.width, 0.1*data.height, \
    fill="Red")
    canvas.create_text((data.width*0.125), 0.05*data.height,\
     anchor="center", text="Back", font="Arial 20 bold", fill="White")
    canvas.create_rectangle(0.25*data.width, 0.7*data.height, 0.75*data.width, 0.8*data.height, \
    fill="Red")
    canvas.create_text((data.width*0.5), 0.75*data.height,\
     anchor="center", text="Upgrade Players", font="Arial 20 bold", fill="White")
    canvas.create_text(data.width/2, data.height *0.9, \
    text="Upgraded Players have special abilities \n like slower ball speed and scoreboosters!", \
    fill='white',font="Arial 20 bold")
    
####################################
# Leaderboard mode
####################################

def LeaderboardMousePressed(event, data):
    if 0<event.x<0.25*data.width and 0*data.height<event.y<0.1*data.height:
        data.lastmode='Selection'
        data.mode='GameSelection'
 
def LeaderboardTimerFired(data):
    pass

def LeaderboardRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="Black")
    canvas.create_image(data.width//2, data.height//2, \
    image=data.leaderboardImage)
    canvas.create_rectangle(0, 0, 0.15*data.width, 0.1*data.height, \
    fill="Black")
    canvas.create_text(data.width*0.075, 0.05*data.height, \
    anchor="center", text="Back", font="Arial 18 bold", fill="White")
    canvas.create_text(256,103, anchor="center", \
    text=data.leaderboard[0][0], font="Arial 24 bold", fill="White")
    canvas.create_text(256,201, anchor="center", \
    text=data.leaderboard[1][0], font="Arial 24 bold", fill="White")
    canvas.create_text(256,295, anchor="center", \
    text=data.leaderboard[2][0], font="Arial 24 bold", fill="White")
    canvas.create_text(256,390, anchor="center", \
    text=data.leaderboard[3][0], font="Arial 24 bold", fill="White")
    canvas.create_text(388,103, anchor="center", \
    text=str(data.leaderboard[0][1]), font="Arial 24 bold", fill="White")
    canvas.create_text(388,201, anchor="center", \
    text=str(data.leaderboard[1][1]), font="Arial 24 bold", fill="White")
    canvas.create_text(388,295, anchor="center", \
    text=str(data.leaderboard[2][1]), font="Arial 24 bold", fill="White")
    canvas.create_text(388,390, anchor="center", \
    text=str(data.leaderboard[3][1]), font="Arial 24 bold", fill="White")
        
####################################
# UserAuthentication and FileIO
####################################

def register(data):
    #registers new user
    contents=readFile(data.path)
    if data.user=="" or data.password=="":
        return False
    for line in contents:
        info = line.split(" ")
        if len(info)==3:
            if data.user == info[0]:
                return False
    writeFile(data.path,"%s\n%s %s %d" %(contents,\
    data.user,data.password,data.highscore))
   

def login(data):
    #validates existing user
    for line in open("UserData.txt","r").readlines(): 
        info = line.split(" ") 
        if len(info)==3:
            if data.user == info[0] and data.password == info[1]:
                data.highscore=int(info[2])
        if len(info)==3:
            if data.user == info[0] and data.password == info[1]:
                return True
    return False

def getHighScoreList(data):
    #gets a tuple list of top 4 highscores
    highScoreDict={}
    scoreList=[]
    leaderboard=[]
    contents=readFile(data.path)
    for line in contents.splitlines():
        info = line.split(" ")
        if len(info)==3 and info[0]!="":
            username=info[0]
            highscore=int(info[2])
            highScoreDict[username]=int(highscore)
            scoreList.append(int(highscore))
    for n in range(4):
        high=max(scoreList)
        scoreList.remove(high)
        for val in highScoreDict:
            if highScoreDict[val]==high:
                leaderboard.append((val,high))
    return(leaderboard)
    

def updateHighScore(data):
    #updates data if user crosses highscore
    contents=readFile(data.path)
    newContents=contents.replace("%s %s %d"\
     %(data.user,data.password,data.highscore),"%s %s %d" %(data.user,data.password,data.score))
    writeFile(data.path,(newContents))
                    
def writeFile(path, contents): #copied from 112 notes
    with open("UserData.txt", "wt") as f:
        f.write(contents)

def readFile(path): #copied from 112 notes
    with open("UserData.txt", "rt") as f:
        return f.read()

####################################
# LeapMotion Code
####################################

def startHand(data):
    #starts game
    frame=data.frame
    for hand in frame.hands:
        if 'S' in (getLetter(data)):
            data.start=True

def getLetter(data):
    #gets letter from leapmotion data
    frame=data.frame
    for hand in frame.hands:
        data.fill='Green'
        tip=hand.fingers[2].bone(3).next_joint.z
        mid=hand.fingers[2].bone(1).next_joint.z
        index=hand.fingers[2].bone(1).next_joint.z
        ring=hand.fingers[3].bone(1).next_joint.z
        pinky=hand.fingers[4].bone(1).next_joint.z
        wrist=hand.wrist_position.z
        data.curHandLength=tip-wrist
        ringLen=ring-wrist
        pinkyLen=pinky-wrist
        midLen=mid-wrist
        indexLen=index-wrist
        strength=hand.grab_strength
        pointables=hand.pointables
        thumb=pointables[0].direction
        indexFinger=pointables[1].direction
        ringFinger=pointables[3].direction
        middleFinger=pointables[2].direction
        pinkyFinger=pointables[4].direction
        angle=thumb.angle_to(indexFinger)
        indexAngle=indexFinger.angle_to(middleFinger)
        middleAngle=middleFinger.angle_to(ringFinger)
        thumbAngles=(2.5,2.8)
        scale=0.5
        normal=hand.palm_normal
        pinch=hand.pinch_strength
        extensions=False
        thumbtup=thumb.to_tuple()
        
        count=0
        fingerList=[]
        for fing in range(len(hand.fingers)):
            if hand.fingers[fing].is_extended:
                fingerList.append((data.fingerNames[fing],\
                hand.fingers[fing].direction[0],\
                hand.fingers[fing].direction[1],\
                hand.fingers[fing].direction[2]))
                
                count+=1
        if count==0:
            extensions=True
        
        #print(thumb[0],indexFinger[0],ringFinger[0],middleFinger[0])
        #print(thumbtup,'thumbtup')
        #print(strength,'strength')
        # print(angle,'angle')
        #print(indexAngle,'index angle')
        # print(middleAngle,'middle angle')
        #print(count,'count')
        # print(data.curHandLength,'data.handlength')
        #print (normal,'normal')
        # if data.timeCount==20:
        #print(fingerList)
        #print (indexLen,"indexLen")
        
        letters=[]
        if count==3 and 0.0<indexAngle<0.25 and 0.0<middleAngle<0.3:
            print('W')
            letters.append('W')
        
        if count==2 and 0.12<indexAngle<0.4 and 0.5<middleAngle:
            print('V')
            letters.append('V')
        
        if count==3 and 0.5<middleAngle:
            print('K')
            letters.append('K')
        
        if count==2 and indexAngle<0.12 and 0.5<middleAngle:
            print('U')
            letters.append('U')
        
        if count<=2 and hand.fingers[4].is_extended:
            print('I')
            letters.append('I')
        
        if count<=1 and hand.fingers[4].is_extended:
            print('J')
            letters.append('J')
        
        if count==2 and hand.fingers[0].is_extended \
        and hand.fingers[4].is_extended:
            print('Y')
            letters.append('Y')
        
        if count==4 and not hand.fingers[0].is_extended:
            print('B')
            letters.append('B')
        
        if count==1 and hand.fingers[1].is_extended:
            print('D')
            letters.append('D')
        
        if count==1 and hand.fingers[0].is_extended:
            print('A')
            letters.append('A')
        
        if count==2 and hand.fingers[0].is_extended \
        and hand.fingers[1].is_extended:
            print('L')
            letters.append('L')
        
        if count==2 and indexAngle<0.25:
            print('R')
            letters.append('R')
        
        if count==3 and hand.fingers[4].is_extended and \
        hand.fingers[3].is_extended and hand.fingers[2].is_extended:
            print('F')
            letters.append('F')
        
        if count==2 and hand.fingers[0].is_extended and \
        hand.fingers[1].is_extended and fingerList[0][2]< 0.3\
         and fingerList[1][2] < 0.3:
            print('G')
            letters.append('G')
        
        if 1<= count<=3 and fingerList[0][2]< 0.3:
            print('H')
            letters.append('H')
        
        if count==0:
            print('S')
            letters.append('S')
        
        if count==0 and 0.5<=strength<=1:
            print('O')
            letters.append('O')
        
        
        if count==0 and abs(indexLen)>5:
            print('X')
            letters.append('X')
        
        return letters
    
    data.fill='Red'

####################################
# use the run function as-is #run function taken from 15-112 animation framework
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run(500, 500)