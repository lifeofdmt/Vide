import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText
from PIL import ImageTk, Image
from tkinter import Label, Frame, IntVar
from commands import *

class widget():
    # Set window properties
    def __init__(self):
        self.root = tb.Window(themename="solar")
        self.root.title("VIDE")
        self.root.geometry("500x400")
        self.root.minsize(width=500, height=400)
        self.root.iconbitmap("images/favicon.ico")

        # Set initial number of generated rows
        self.initial_row_count = 5
    

        # Store data on all speaker on system ({audio}:{speaker})
        self.speakers = []
        frames = self.draw_frames()

        # Style frames
        self.style_side(frames[0], frames[1])
        self.draw_voice(frames[1])

        # Fill screen
        self.fill_screen()


    def draw_frames(self):
        """
        Draw the side and main frames onto the screen and return the two frames (side, main)
        Sidepanel - The frame at the left
        Mainpanel - The frame at the middle of the screen
        """
        sideframe = tb.Frame(self.root, bootstyle="dark")
        mainframe = tb.Frame(self.root)

        # Use the grid geometry manager
        sideframe.grid(row=0, column=0, sticky="nsew")
        mainframe.grid(row=0, column=1, sticky="nsew")
        return (sideframe, mainframe)


    def style_side(self, sideframe, mainframe):
         # Style Side_panel
        global image

        inner_frame = tb.Frame(sideframe, bootstyle="dark")
        inner_frame.pack(fill=Y)

        image = ImageTk.PhotoImage(Image.open("images/vide.ico"))
        icon =  Label(inner_frame, image=image, height=140)
        icon.pack(fill=X, padx=10, pady=(10,10))

        box = tb.Combobox(inner_frame, values=["VIDE","ffjfj"], bootstyle="info")
        box.pack(padx=10, pady=(10,10), fill=X)
        box.bind("<Motion>", button_hover)
        box.current(0)

        tools = tb.Label(inner_frame, text="TOOLS", bootstyle="default", font=("Helvetica", 16), justify=LEFT, foreground="white", background="#116EBF", padding=5)
        tools.pack(fill=X, padx=10, pady=(10,10))

        options = ['Voice Classification', "Speech-To-Text", "Voice Library"]
        commands = [lambda:self.draw_voice(mainframe), lambda:self.draw_speech(mainframe), lambda:self.draw_libary(mainframe)]

        i = 0
        for option in options:
            button = tb.Button(inner_frame, text=option, bootstyle="info outline", padding=15, command=commands[i])
            button.pack(fill=X, padx=10, pady=(10,10))
            button.bind("<Motion>", button_hover)
            i += 1

        button = tb.Button(inner_frame, text="Check Me Out", bootstyle="info link", padding=15, command=open_portfolio)
        button.pack(fill=X, padx=10, pady=(10,10))
        button.bind("<Motion>", button_hover)


    def draw_voice(self, mainframe):
        delete_children(mainframe)
        header_frame = self.draw_header(mainframe, title="Voice Classification")

        # Add icons to the header
        global info_icon
        global add_icon
        global trash_icon

        add_icon = ImageTk.PhotoImage(Image.open("images/add.png"))
        trash_icon = ImageTk.PhotoImage(Image.open("images/trash.png"))
        info_icon = ImageTk.PhotoImage(Image.open("images/info.png"))

        # Create table container
        table_container = tb.Frame(mainframe, bootstyle='dark')
        table_container.pack(pady=(25,0), fill=X)

        # Create table
        table = ScrolledFrame(table_container, autohide=False)
        table.pack(fill=BOTH, expand=YES, padx=(10), pady=10)

        # Create header for table
        header = Frame(table)
        name_header = tb.Label(header, text="|  Name", anchor=W)
        audio_header = tb.Label(header, text="|  Audio Data", anchor=W)
        speech_header = tb.Label(header, text="|  Speech", anchor=W)

        name_header.grid(row=0, column=0, pady=(5,5), padx=10)
        audio_header.grid(row=0, column=1, pady=(5,5), padx=10)
        speech_header.grid(row=0, column=2, sticky=W+E, pady=(5,5), padx=10)

        header.pack(side=LEFT)

        self.draw_table(table)


        # Add separators
        sep = tb.Separator(mainframe)
        sep.pack(fill=X)

        # Add button to record
        label = tb.Label(mainframe, bootstyle="dark inverse", padding=10, width=80, text="")

        global microphone_icon
        microphone_icon = ImageTk.PhotoImage(Image.open("images/microphone.png"))

        button = tb.Label(mainframe, image=microphone_icon, width=200)
        button.bind("<Motion>", button_hover)
        button.bind("<Button-1>", lambda event: classify_voice(event, label, self.speakers))
        button.pack(pady=(30,20))

        # Draw icons to screen
        icons = [add_icon, trash_icon, info_icon]
        """commands = [lambda: self.add_row(tools, row_type="voice"), show_creator, show_creator]

        column = 1
        for icon in range(len(icons)):
            button = tb.Button(header_frame, bootstyle=LINK, command=commands[icon], image=icons[icon])
            button.bind("<Motion>", button_hover)
            button.grid(row=0, column=column, padx=2)
            column += 1
        """
        label.pack()



    def draw_speech(self, mainframe):
        delete_children(mainframe)

        header_frame = self.draw_header(mainframe, title="Speech-To-Text")

        # Draw icon
        button = tb.Button(header_frame, bootstyle=LINK, command=show_creator, image=info_icon)
        button.bind("<Motion>", button_hover)

        label = tb.Label(mainframe, text="Convert Audio File To Text", padding=10, font=("Noto Sans", 18))
        label.pack(pady=(10,0))
        label.bind("<Motion>", text_hover)

        # Add text field
        text_field = ScrolledText(mainframe, height=20)
        text_field.pack(pady=(5,10), fill=X, padx=20)

        # Add choose file button
        button = tb.Button(mainframe, text="Choose File", padding=10, bootstyle="info", command=lambda: speech_to_text(text_field))
        button.pack(pady=5)
        button.bind("<Motion>", button_hover)


        # Add progress bar
        flood = tb.Progressbar(mainframe, bootstyle="info striped", maximum=100, value=10, length=200)
        flood.pack(pady=(20,10))


    def draw_libary(self, mainframe):
        delete_children(mainframe)

        header_frame = self.draw_header(mainframe, title="Voice Library")

        tool_title = tb.Label(mainframe, text="Convert text to speech", font=("Open Sans", 18), bootstyle=("info"), padding=5)
        tool_title.pack(pady=(5,5))

        text_field = ScrolledText(mainframe, height=20)
        text_field.pack(pady=(20,10), padx=20, fill=X)
        
        # Add button to initialize start
        generate = tb.Button(mainframe, text="Generate Audio", bootstyle="info", padding=10, command=lambda: text_to_speech(text_field))
        generate.bind("<Motion>", button_hover)
        generate.pack(pady=(10,20))


    def draw_header(self, mainframe, title):
        # Style main panel
        main_header = tb.Frame(mainframe)
        main_header.pack(fill=X)

        header_frame = tb.Frame(main_header)
        header_frame.pack(fill=X)

        category = tb.Label(header_frame, text=title, bootstyle="default", font=("Open Sans Bold", 20), anchor=W, width=60)
        category.grid(row=0, column=0, pady=(10,15), padx=(10,10))
        category.bind("<Motion>", text_hover)

        # Seperator
        sep = tb.Separator(main_header)
        sep.pack(fill=X)
        return header_frame


    def fill_screen(self):
        """
        Resize all frame to completely occupythe screen
        """

        # Configure column widths
        screen_width = self.root.winfo_screenwidth()
        
        frame1_width = int(screen_width * 0.2)
        frame2_width = int(screen_width * 0.8)

        self.root.columnconfigure(0, weight=1, minsize=frame1_width)
        self.root.columnconfigure(1, weight=1, minsize=frame2_width)
        self.root.rowconfigure(0, weight=1)

    
    # Header button functionality
    def add_row(self, widget, row_type):
        button_click()
        if row_type == 'voice':
            self.row_voice += 1
            self.no_of_rows_voice += 1
            name_label = tb.Entry(widget, bootstyle="success")

            frame = tb.Frame(widget)
            speech_label = tb.Label(frame, text='', justify="left", width=128)  
            
            check_var = IntVar()
            check = tb.Checkbutton(frame, bootstyle="dark", command=lambda check_var=check_var: box_checked(check_var), onvalue=1, offvalue=0, variable=check_var)

            voice_button = tb.Button(widget, text="Choose Audio", bootstyle="info", command=lambda speech_label=speech_label, row=self.no_of_rows_voice-1: choose_audio(speech_label, row))
            voice_button.bind("<Motion>", button_hover)
                    
            name_label.grid(row=self.row_voice, column=0, pady=(5,2), padx=10)
            voice_button.grid(row=self.row_voice, column=1, pady=(5,2), padx=10)

            speech_label.pack(side=LEFT)
            check.pack(pady=10)
            frame.grid(row=self.row_voice, column=2, pady=(5,2), padx=10, sticky=W+E)

        elif row_type == 'library':
            self.draw_table(widget, text=("Male | Female", "Choose File", ""), no_of_rows=1, row=self.row_libary)
            self.row_libary += 1
            self.no_of_rows_lib += 1
        
    def draw_table(self, table):
        # Create table rows
        for row in range(self.initial_row_count):
            table_row = Frame(table)

            name_field = tb.Entry(table_row, bootstyle="primary")
            choose_button = tb.Label(table_row, bootstyle='primary', text='Choose File')
            speech_field = tb.Entry(table_row, bootstyle="primary")

            name_field.grid(row=row, column=0, padx=10, pady=5)
            choose_button.grid(row=row, column=1, padx=10, pady=5)
            speech_field.grid(row=row, column=2, sticky=W+E, padx=10, pady=5, )

            table_row.pack()
    


