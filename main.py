import subprocess
import sys
from tkinter import *
from PIL import Image, ImageTk


class SpeakNowApp:
    def __init__(self, username):
        self.username = username
        self.root = Tk()
        self.root.title(f"Welcome {self.username} to SpEaK NoW!!")
        self.root.geometry('2000x2000')
        self.root.config(bg='#FF8728')
        self.init_ui()

    def init_ui(self):
        # LABEL
        l1 = Label(self.root, text=f'Welcome {self.username} to SpEaK NoW..!!', font='Verdana 15')
        l1.pack(side=TOP, pady=10)

        # BUTTON to trigger speaknow.py
        image = Image.open(r"speaknow.jpg")
        resized = image.resize((80, 60), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        photo_image = ImageTk.PhotoImage(resized)

        # Button to run speaknow.py
        b = Button(self.root, text='Click Me to Start Speak Now!', image=photo_image, compound=LEFT,
                   command=self.run_speaknow)
        b.pack(pady=20)

    def run_speaknow(self):
        try:
            # Run speaknow.py in a separate process
            subprocess.Popen(["python3", "speaknow.py"])
            print("speaknow.py is running...")
        except Exception as e:
            print(f"Error: {e}")
            self.show_message("Error", f"Failed to run speaknow.py: {e}", "warning")

    def show_message(self, title, message, icon):
        msg = Message(self.root, text=message, width=300)
        msg.pack()

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        app = SpeakNowApp(username)
        app.start()
    else:
        print("No username provided.")
