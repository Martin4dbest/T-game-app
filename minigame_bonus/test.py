import tkinter as tk
from tkinter import ttk, simpledialog, Toplevel, Label, Button, PhotoImage, END, NORMAL
import pyttsx3
import sqlite3
from pygame import mixer

def reset_password():
    pass  # Implement reset password functionality

def minigame():
    minigame_window = Toplevel()
    minigame_window.title("MiniGame")
    minigame_window.geometry("400x300")
    Label(minigame_window, text="Welcome to the Minigame!", font=("Arial", 14)).pack(pady=10)
    Button(minigame_window, text="Close", command=minigame_window.destroy).pack()
    minigame_window.mainloop()

def main_game(category, username):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[0].id)
    
    mixer.init()
    mixer.music.load("kbc.mp3")
    mixer.music.play(-1)

    def select(event):
        b = event.widget
        value = b["text"]

        for i in range(15):
            if value == correct_answers[i]:
                if value == correct_answers[14]:
                    def close():
                        root2.destroy()
                        root.destroy()
                    def playagain():
                        root2.destroy()
                        questionArea.delete(1.0, END)
                        questionArea.insert(END, question[0])
                        optionButton1.config(text=First_options[0])
                        optionButton2.config(text=Second_options[0])
                        optionButton3.config(text=Third_options[0])
                        optionButton4.config(text=Fourth_options[0])
                        entered_category = simpledialog.askstring("Input", "INPUT CATEGORY PLAYED AND CHECK LEADERBOARD:")
                        if entered_category:
                            amount_won = 100000000
                            conn = sqlite3.connect("users.db")
                            c = conn.cursor()
                            c.execute("INSERT INTO leaderboard (username, category_played, amount_won) VALUES (?, ?, ?)",
                                      (username, entered_category, amount_won))
                            conn.commit()
                            conn.close()
                    
                    mixer.music.stop()
                    mixer.music.load("kbcwon.mp3")
                    mixer.music.play()
                    root2 = Toplevel()
                    root2.config(bg="black")
                    root2.geometry("500x400+140+30")
                    root2.title("You won 100,000,000 pounds")
                    Label(root2, text="You Won", font=("arial", 40, "bold"), bg='black', fg="white").pack()
                    Button(root2, text="Play MiniGame", command=minigame).pack()
                    Button(root2, text="Play Again", command=playagain).pack()
                    Button(root2, text="Close", command=close).pack()
                    root2.mainloop()
                    break
                
                questionArea.delete(1.0, END)
                questionArea.insert(END, question[i+1])
                optionButton1.config(text=First_options[i+1])
                optionButton2.config(text=Second_options[i+1])
                optionButton3.config(text=Third_options[i+1])
                optionButton4.config(text=Fourth_options[i+1])
                amountLabel.configure(image=amountImages[i])
                amountLabel.image = amountImages[i]

            if value not in correct_answers:
                def close():
                    root1.destroy()
                    root.destroy()
                def tryagain():
                    root1.destroy()
                    questionArea.delete(1.0, END)
                    questionArea.insert(END, question[0])
                    optionButton1.config(text=First_options[0])
                    optionButton2.config(text=Second_options[0])
                    optionButton3.config(text=Third_options[0])
                    optionButton4.config(text=Fourth_options[0])
                    amountLabel.config(image=amountImages[0])
                
                root1 = Toplevel()
                root1.config(bg="black")
                root1.geometry("500x400+140+30")
                root1.title("You won 0 pounds")
                Label(root1, text="You lose", font=("arial", 40, "bold"), bg='black', fg="white").pack()
                Button(root1, text="Try Again", command=tryagain).pack()
                Button(root1, text="Close", command=close).pack()
                root1.mainloop()
                break
