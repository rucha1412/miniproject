import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


class SpeakNowApp:
    def __init__(self, username):
        self.username = username
        self.root = Tk()
        self.root.title(f"Welcome {self.username} to SpEaK NoW!!")
        self.root.geometry('800x600')  # Adjusted for better window fitting
        self.root.config(bg='#FF8728')
        self.init_ui()

    def init_ui(self):
        # LABEL
        l1 = Label(self.root, text=f'Welcome {self.username} to SpEaK NoW..!!', font='Verdana 15')
        l1.pack(side=TOP, pady=20)

        # Load and resize image
        try:
            image = Image.open(r"speaknow.jpg")
            resized = image.resize((150, 100), Image.Resampling.LANCZOS)  # Resized for better appearance
            self.photo_image = ImageTk.PhotoImage(resized)  # Keep reference to prevent GC

            # Button to run speaknow.py
            b = Button(self.root, text='Click Me to Start Speak Now!', image=self.photo_image, compound=LEFT,
                       command=self.run_speaknow)
            b.pack(pady=20)
        except Exception as e:
            self.show_message("Error", f"Failed to load image: {e}", "warning")

    """def run_speaknow(self):
        try:
            # Run speaknow.py as a separate process
            process = subprocess.Popen(["python3", "speaknow.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()  # Capture output and error
            if stderr:
                self.show_message("Error", stderr.decode(), "warning")
                print("speaknow.py is running...")
        except Exception as e:
            print(f"Error: {e}")
            self.show_message("Error", f"Failed to run speaknow.py: {e}", "warning")
"""

    def run_speaknow(self):
        try:
            process = subprocess.Popen(
                ["python3", "speaknow.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Ensures output is in string format
            )

            # Print output and errors to PyCharm terminal in real-time
            for line in process.stdout:
                print(line, end="")  # Print stdout from speaknow.py
            for line in process.stderr:
                print("ERROR:", line, end="")  # Print stderr from speaknow.py

        except Exception as e:
            print(f"Error: {e}")
            self.show_message("Error", f"Failed to run speaknow.py: {e}", "warning")

    def show_message(self, title, message, icon):
        if icon == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        app = SpeakNowApp(username)
        app.start()
    else:
        print("No username provided.")
