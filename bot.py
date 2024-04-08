import tkinter as tk
from tkinter import Scrollbar, Text, Button, END
import random
import re
import datetime

class ChatBot(object):
    def create_widgets(self):
        # Chat log configuration
        self.ChatLog.config(state="disabled", wrap="word")
        self.ChatLog.tag_configure("user", foreground="#0084FF")
        self.ChatLog.tag_configure("bot", foreground="#E53935")

        # Entry box styling
        self.EntryBox.config(insertbackground="black")

        # Send button styling
        self.SendButton.config(fg="white", cursor="hand2")

        # Additional widgets
        self.titleLabel = tk.Label(self.master, text="ChatBot", font=("Helvetica", 16), bg="#F5F5F5")
        self.titleLabel.grid(row=0, column=0, sticky="w", padx=10)

        self.statusLabel = tk.Label(self.master, text="Online", font=("Helvetica", 10), bg="#F5F5F5", fg="green")
        self.statusLabel.grid(row=2, column=0, sticky="w", padx=10)
    
    def __init__(self, master):
        self.master = master
        self.master.title("ChatBot")
        self.master.geometry("450x225")
        self.master.config(bg = "#F5F5F5")
        self.master.resizable(width=False, height=False)


        self.ChatLog = Text(master, bd=0, bg="white", fg = "Dark Olive Green", height="7", width="40", font=("Calibri", 13))
        self.ChatLog.config(state="disabled")

        self.scrollbar = Scrollbar(master, command=self.ChatLog.yview, cursor="heart", bg = "Coral")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        self.EntryBox = Text(master, bd=0, bg="white", fg="Midnight Blue", height="1", width="40", font=("Calibri",13))

        self.SendButton = Button(master, font=("Verdana",10), text="->", width=3, height=1,
                            bd=0, bg="#4CAF50", activebackground="#45a049", command=self.send )

        self.ChatLog.grid(row=0, column=0, padx=10, pady=10)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.EntryBox.grid(row=1, column=0, padx=10, pady=10)
        self.SendButton.grid(row=1, column=1, padx=10, pady=10)

        self.patterns = [
            (r'hi|hello|hey', ["hello", "hey there", "hi"]),
            (r'how are you?', ["I'm great,  how are you", "I am doing well, thanks for asking", "I'm fine, how are you"]),
            (r'what is your name', ["I am just a chat bot. I have no name"]),
            (r'what can you do?', ["I can chat with you", "I can help you"]),
            (r'wanna listen to a story', ["I would leave to here"]),
            (r'thats the end of the story| thats it',["wow! that was a nice story"]),
            (r'quit|bye|Im leaving', ["Goodbye!", "See you later", "bye"])
        ]
        self.banned_words = ['abusive word 1', 'abusive word 2', 'abusive word 3']
        self.create_widgets()
        

    def log_conversation(self, message_type, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("chat_log.txt", "a") as file:
            file.write(f"{timestamp} - {message_type}: {message}\n")

    
# ... existing code ...

    def respond(self, user_input):
        for word in self.banned_words:
            if word in user_input:
                return "Sorry, I can't understand that."
        for pattern, responses in self.patterns:
            if re.search(pattern, user_input.lower()):
                return random.choice(responses)
        return "Sorry, I don't understand that."

    def send(self):
        msg = self.EntryBox.get("1.0", END).strip()
        self.log_conversation("User", msg)
        
        self.EntryBox.delete("1.0",END)
        response = self.respond(msg)
        self.log_conversation("Bot", response)
        self.ChatLog.config(state="normal")
        self.ChatLog.tag_add("user", "end-2c linestart", "end-1c lineend")
        self.ChatLog.tag_add("bot", "end-1c linestart", "end")
        self.ChatLog.insert(END, "You: " + msg + "\n")
        self.ChatLog.insert(END, "Bot: " + response + "\n")
        self.ChatLog.config(state='disabled')
        self.ChatLog.see(END)


root = tk.Tk()
chat_bot = ChatBot(root)
root.mainloop()
