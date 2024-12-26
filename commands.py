from tkinter import filedialog, END
from tkinter import messagebox
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.icons import Emoji
import webbrowser
import pygame
from gtts import gTTS

pygame.init()

def button_click():
    sound = pygame.mixer.Sound("sounds/button_click.mp3")
    sound.play()

def box_checked(value, row, clicks):
    """
    Update row table to "row" if checklist on -row "row"
    is clicked
    """
    if value.get():
        if not row in clicks:
            clicks.append(row)
    else:
        clicks.remove(row)
    print(clicks)
    print(f"Row {row}")


def button_hover(event):
    event.widget.configure(cursor="hand2")

def drag(event):
    event.widget.configure(cursor="fleur")

def text_hover(event):
    event.widget.configure(cursor="ibeam")

def open_portfolio():
    webbrowser.open("https://github.com/lifeofdmt?tab=repositories")

def delete_children(mainframe):
    for widget in mainframe.winfo_children():
        widget.destroy()

def delete_row(frame, clicked, reference):
    print(clicked)
    rows = frame.winfo_children()
    for row in range(len(rows)):
        if (row + 1) in clicked:
            print(row+1)
            print(reference)
            frame.winfo_children()[reference[f'{row+1}']].destroy()
            for name in reference:
                if name != str(row+1):
                    if reference[name] != 1:
                        reference[name] -= 1
    clicked = []

def show_creator():
    button_click()
    messagebox.showinfo("Creator Info", "This software was developed by Malik Delana Taiwo and Amir Taiwo")
    toast = ToastNotification(title="Contact Me", message="Check me out as lifeofdmt.github.io", duration=3000, icon=Emoji.get('winking face'), bootstyle='success')
    toast.show_toast()

def open_file():
    filename = filedialog.askopenfilename(initialdir="\C:", title="Select an Audio File", filetypes=(("wav files", "*.wav"),("mp3 files", "*.mp3")))
    return filename

def recognise_speech(audiofile):
    import speech_recognition as sr
    with sr.AudioFile(audiofile) as source:
        speech_rec = sr.Recognizer()

        # Set energy threshold for percieved speech
        speech_rec.energy_threshold = 4000

        # Auto adjust energy threshod for audio ambience
        speech_rec.dynamic_energy_threshold = True
        speech_rec.adjust_for_ambient_noise(source, duration=1)

        # Adjust the pause threshold for registering a phrase
        speech_rec.pause_threshold = 0.3

        # Return audio data from (source)
        audio_data = speech_rec.record(source, duration=source.DURATION)
        
        # Transcribe audio
        speech = speech_rec.recognize_google(pfilter=1, audio_data=audio_data, language='en-US', show_all=False)
    return speech

def update_speakers(speakers, data):
    """
    Update the speakers on the system
    Speaker data is stored as a list of {speaker_name:row:audio} dicts
    """
    for speaker in speakers:
        if speaker["row"] == data["row"]:
            speaker["audio"] = data["audio"]
            return
    speakers.append(data)

def speaker_recognition(audio, speakers):
    """
    Performs speaker recognition by comparing "audio" to the "speakers[audio]"
    Returns "row" where first matched speaker is in table or "speakers name" if matched to a known speaker
    Else returns "False"
    """
    for speaker in speakers:
        from speechbrain.pretrained import SpeakerRecognition
        verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
        score, prediction = verification.verify_files(audio, speaker["audio"])

        if prediction:
            return f"Row {speaker['row'] + 1}"
    return
        
def choose_audio(label, row, speakers):
    filename = open_file()
    
    if filename:
        speech = recognise_speech(filename)
        label.configure(text=speech)

    # Update speakers
    update_speakers(speakers, {"audio": filename, "row": row})

def classify_voice(event, label, speakers):
    """
    Ask user for "filename" to compare against other audio on system
    Calls "speaker_recognition" and updates label to either 
    Speakers name or row in data if there is a match
    """
    filename = open_file()

    if filename:
        speaker = speaker_recognition(filename, speakers)

        if speaker != None:
            label.configure(text=f"{speaker}")
        else:
            label.configure(text="No match")
    
def speech_to_text(widget):
    """
    Calls "recognize_speech" and updates the text in "widget"        
    """
    filename = open_file()

    if filename:
        speech = recognise_speech(filename)    
        widget.configure(bootstyle="light")
        widget.delete("1.0", "end-1c")
        widget.insert("end", speech)

def text_to_speech(widget):
    """
    Converts texts to speech and plays the audio
    """
    text = widget.get('1.0', END)
    if text:
        speech = gTTS(text=widget.get('1.0', END))
        speech.save('Audio_Out.mp3')
        sound = pygame.mixer.Sound('Audio_Out.mp3')
        sound.play()








    