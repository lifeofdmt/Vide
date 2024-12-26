from widgets import widget
from tkinter import mainloop
#from speechbrain.pretrained import SpeakerRecognition

"""verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
score, prediction = verification.verify_files("test3.wav", "test1.wav") # Same Speaker

print(prediction)

"""

screen = widget()

mainloop()
