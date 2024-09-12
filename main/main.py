import threading
import pyaudio
import wave
import os
from tkinter import *
from tkinter import filedialog
from lib.Recognition import *
from tensorflow import keras


global filePath
global model

path = "model123.sav"
model = loadModel(path)
filePath = "unknow"


# Audio record

class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    frames = []

    def __init__(self, master):

        self.isrecording = False
        self.button1 = Button(app, text='Start Recording', width=14, command=self.startrecording)
        self.button2 = Button(app, text='Stop Recording', width=14, command=self.stoprecording)
        self.button1.place(x=300, y=410)
        self.button2.place(x=420, y=410)

    def startrecording(self):

        textTest = "Please read this text for the record :"

        textTest1 = "In computer science, artificial intelligence, sometimes called machine intelligence, is        "
        textTest2 = "intelligence demonstrated by machines, in contrast to the natural intelligence which is       "
        textTest3 = "displayed by humans and animals. An intelligent agent is any device that perceives its     "
        textTest4 = "environment and takes actions that maximize its chance of successfully achieving its goals."
        #textTest5 = ""
        textTest6 = "మానసిక, శారీరక, సామాజిక మరియు మేధో వంటి అన్ని అంశాలలో మంచి ఆరోగ్యం మనకు మంచిది."
        textTest7 = "మంచి ఆరోగ్యం మనకు అనారోగ్యం మరియు వ్యాధుల నుండి స్వేచ్చాను అందిస్తుంది. మంచి"
        textTest8 = "ఆరోగ్యం మానసిక, శారీరక మరియు సామాజిక ఆరోగ్యం యొక్క భావన. నిజమైన సంపద ఆరోగ్యం,"
        textTest9 = "బంగారం మరియు వెండి ముక్కలు కాదు. మంచి ఆరోగ్యం సంపద కంటే చాలా ముఖ్యమైనది"
        


        self.textParkiTest = Label(app, text=textTest, font=('bold', '15'), bg='red')
        self.textParkiTest.place(x=400, y=480)

        self.textParkiTest1 = Label(app, text=textTest1, font=('normal', '14'), bg='white')
        self.textParkiTest1.place(x=400, y=505)
        self.textParkiTest2 = Label(app, text=textTest2, font=('normal', '14'), bg='white')
        self.textParkiTest2.place(x=400, y=530)
        self.textParkiTest3 = Label(app, text=textTest3, font=('normal', '14'), bg='white')
        self.textParkiTest3.place(x=400, y=555)
        self.textParkiTest4 = Label(app, text=textTest4, font=('normal', '14'), bg='white')
        self.textParkiTest4.place(x=400, y=580)
        #self.textParkiTest5 = Label(app, text=textTest5, font=('normal', '14'), bg='white')
        #self.textParkiTest5.place(x=450, y=605)
        self.textParkiTest6 = Label(app, text=textTest6, font=('normal', '14'), bg='white')
        self.textParkiTest6.place(x=400, y=630)
        self.textParkiTest7 = Label(app, text=textTest7, font=('normal', '14'), bg='white')
        self.textParkiTest7.place(x=400, y=655)
        self.textParkiTest8 = Label(app, text=textTest8, font=('normal', '14'), bg='white')
        self.textParkiTest8.place(x=400, y=680)
        self.textParkiTest9 = Label(app, text=textTest9, font=('normal', '14'), bg='white')
        self.textParkiTest9.place(x=400, y=705)
        

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.isrecording = True

        print('Recording')
        global t
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        if self.isrecording == False:
            print("Press Recoring button first")
        else:
            self.textParkiTest.destroy()
            self.textParkiTest1.destroy()
            self.textParkiTest2.destroy()
            self.textParkiTest3.destroy()
            self.textParkiTest4.destroy()
            #self.textParkiTest5.destroy()
            self.textParkiTest6.destroy()
            self.textParkiTest7.destroy()
            self.textParkiTest8.destroy()
            self.textParkiTest9.destroy()
            

            self.isrecording = False
            print('recording complete')
            self.filename = "recordingAudio.wav"
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()

    def record(self):
        self.frames.clear()
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)


def chooseFile():
    global filePath
    filePath = filedialog.askopenfilename(initialdir="/C", title="Select a file", filetypes=[("wav file", "*.wav")])
    print("path :", filePath)


def execAI():
    global part_label1
    global part_label2
    global part_label3
    global filePath
    errmsg = "Path not valid"

    if ((filePath == "unknow") or (filePath == "")) and os.path.exists("recordingAudio.wav"):
        filePath = "recordingAudio.wav"

    if (filePath != "unknow") and (filePath != ""):
        if predict(model, filePath):
            # Test label1
            try:
                part_label1
            except NameError:
                part_label1 = None

            if part_label1 is not None:
                part_label1.destroy()
            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Display answer
            part_label1 = Label(app, text='According to the model, You may have Parkinson\'s Disease.\nFuther observation is required so please consult a good Neurologist.', font=('bold', 14), bg='white', pady=0)
            part_label1.place(x=480, y=550)
        else:
            # Test label1
            try:
                part_label1
            except NameError:
                part_label1 = None

            if part_label1 is not None:
                part_label1.destroy()
            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Display answer
            part_label2 = Label(app, text='According to the model, You have not been detected to have Parkinson\'s Disease.\nYou Are Healthy!!', font=('bold', 14), bg='white', pady=0)
            part_label2.place(x=450, y=550)
        filePath = "unknow"
    else:
        # Test label1
        try:
            part_label1
        except NameError:
            part_label1 = None

        if part_label1 is not None:
            part_label1.destroy()
        # Test label2
        try:
            part_label2
        except NameError:
            part_label2 = None

        if part_label2 is not None:
            part_label2.destroy()
        #Test label3
        try:
            part_label3
        except NameError:
            part_label3 = None

        if part_label3 is not None:
            part_label3.destroy()

        # Display answer
        part_label3 = Label(app, text=errmsg, font=('bold', 14), bg='white', pady=20)
        part_label3.place(x=600, y=550)

        print(errmsg)
        return errmsg
    if os.path.exists("recordingAudio.wav"):
        os.remove("recordingAudio.wav")


# Create Window
app = Tk()
app.resizable(True, True)

# background
filename = PhotoImage(file="img1.png")
background_label = Label(app, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bouton Choose File
add_btn = Button(app, text='Choose File', width=14, command=chooseFile)
add_btn.place(x=880, y=410)

# Bouton Detect
add_btn = Button(app, text='Detect', width=14, command=execAI)
add_btn.place(x=1000, y=410)

add_btn = Button(app, text='Detect', width=14, command=execAI)
add_btn.place(x=360, y=450)

# Label
part_label = Label(app, text='PARKINSON\'S DISEASE DETECTION BASED ON ANALYSIS OF SPEECH', bg='white', fg='black',  font=('Times', 20, 'bold'), pady=0)#
part_label.place(x=300, y=70)
part_label = Label(app, text='* Parkinson\'s is a disorder of the central nervous system that affects movement, often including tremors.   ', bg='white', fg='navy blue', font=("Times", 14, "bold italic"))#, pady=20
part_label.place(x=50, y=150)
part_label = Label(app, text='* Nerve cell damage in the brain causes dopamine levels to drop, leading to the symptoms of Parkinson\'s.', bg='white', fg='navy blue', font=("Times", 14, "bold italic"))#, pady=20
part_label.place(x=50, y=175)
part_label = Label(app, text='Do you have Parkinson\'s Disease?', bg='white', fg='black', font=('bold', 14))#, pady=20
part_label.place(x=600, y=250)
part_label = Label(app, text='Inorder to find out please perform the below detection process.', bg='white', fg='black', font=('bold', 14))#, pady=20
part_label.place(x=500, y=277)
part_label = Label(app, text=' For audio files detection click on Choose File--> Detect ', font=('normal', 12),bg='white')#, pady=20
part_label.place(x=800, y=360)
part_label = Label(app, text=' For live audio detection click on Start recording after recording \nclick on Stop Recording--> Detect ',  font=('normal', 12),bg='white')#bg='#facd54',, pady=20
part_label.place(x=200, y=350)

if os.path.exists("recordingAudio.wav"):
    os.remove("recordingAudio.wav")

# App title
app.title('AI Parkinson Detector')
app.geometry('1400x1400')
App(app)
app.mainloop()

