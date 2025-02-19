from tkinter import *
import tkinter as tk
from tkinter.ttk import Progressbar
from pygame import mixer
import pyttsx3
from tkinter import ttk, messagebox, simpledialog
import json
from tkinter import Tk, Text, Button, Label, Frame, PhotoImage
import tkinter.messagebox as messagebox
from tkinter import StringVar
from tkinter import Tk,Text,Button,StringVar,Label
import random
import sqlite3
import re
from tkinter import Tk, Entry, Label, Button, messagebox
from tkinter import PhotoImage
import tkinter.simpledialog as simpledialog
import time


from minigame_bonus.main import start_game





#create database


def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, scores INTEGER, amount_won REAL)''')
    conn.commit()
    conn.close()

def update_scores(username, new_score):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET scores = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()

def update_amount_won(username, amount):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET amount_won = ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

    

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def username_exists(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]  # Return the username if authentication is successful
    else:
        return None

def create_leaderboard_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS leaderboard''')  # Drop the existing table if it exists
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                 (username TEXT , amount_won REAL, category_played TEXT)''')  # Recreate the table with the updated schema
    conn.commit()
    conn.close()


create_leaderboard_table()

def update_leaderboard(username, amount_won, category_played):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Check if the username already exists in the leaderboard table
    c.execute("SELECT * FROM leaderboard WHERE username = ?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        # If the username exists, update the amount won
        updated_amount_won = existing_user[1] + amount_won
        c.execute("UPDATE leaderboard SET amount_won = ? WHERE username = ?", (updated_amount_won, username))
    else:
        # If the username doesn't exist, insert a new row
        #c.execute("INSERT INTO leaderboard (username, amount_won, category_played) VALUES (?, ?, ?)", (username,category_played, amount_won, ))
        c.execute("INSERT INTO leaderboard (username, amount_won, category_played) VALUES (?, ?, ?)", (username, amount_won, category_played))

    conn.commit()
    conn.close()





def complete_category(username, category_played):
    # Call this function when a user completes a category
    update_leaderboard(username, 100000000, category_played)  # Update the leaderboard for the logged-in user



def show_leaderboard():
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("1430x1430")

    
    #frame = tk.Frame(leaderboard_window, bg="green")
    #frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create a frame with a colored background
    background_frame = tk.Frame(leaderboard_window, bg="green")
    background_frame.pack(fill="both", expand=True)

    # Create a frame to contain the leaderboard table
    frame = tk.Frame(background_frame, bg="lightyellow", width=1000, height=800)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    frame.config(width=1200, height=900) 


    # Retrieve leaderboard data from the database
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, category_played, amount_won FROM leaderboard ORDER BY amount_won DESC")
    leaderboard_data = c.fetchall()
    conn.close()

    # Create a table to display leaderboard data
    table = ttk.Treeview(frame, columns=("Username", "Category Played", "Amount Won"))
    table.heading("#0", text="Rank")
    table.heading("Username", text="THE CHAMPIONS")
    table.heading("Amount Won", text="Amount Won")
    table.heading("Category Played", text="Category Played")  # Fixed typo here
   
    for i, (username, category_played, amount_won) in enumerate(leaderboard_data, start=1):
        table.insert("", "end", text=str(i), values=(username, category_played, amount_won))

    table.pack(expand=True, fill="both")



"""

def delete_records():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Delete records based on a condition (example: delete all records with amount_won less than 1000)
    c.execute("DELETE FROM leaderboard WHERE amount_won < ?", (10000000,))

    # Alternatively, you can delete all records from the table
    # c.execute("DELETE FROM leaderboard")

    conn.commit()
    conn.close()

# Call the delete_records function to delete records from the leaderboard table
delete_records()

"""

def register():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return
    if len(password) < 6 or not password.isalnum():
        messagebox.showerror("Error", "Password must be alphanumeric and at least 6 characters long.")
        return
    if username_exists(username):
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        return
    if register_user(username, password):
        messagebox.showinfo("Success", "Registration successful. You can now log in.")
    else:
        messagebox.showerror("Error", "Failed to register user.")

category_window = None  


def logout():
    global category_window
    if category_window:
        category_window.destroy()  # Destroy the category selection window
    create_login_window()  # Show the login window again


def exit_game():
    global category_window
    category_window.destroy()




def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return
    if authenticate_user(username, password):
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()  # Destroy the login window
        #update_leaderboard(username, "category_played", 100)  # Adjust this line with the actual category played
        show_category_selection(username)  # Show category selection window
    else:
        messagebox.showerror("Error", "Invalid username or password.")






#def forgot_password():
    #messagebox.showinfo("Forgot Password", "Please contact support for assistance.")

def reset_password():
    # Prompt the user to enter their username
    username = simpledialog.askstring("Forgot Password", "Enter your username:")
    if not username:
        # If the user cancels or closes the dialog, return without resetting the password
        return

    # Connect to the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    if user:
        # Create a new Toplevel window for password reset
        password_window = tk.Toplevel()
        password_window.title("Reset Password")
        
        # Calculate the position to center the password reset window relative to the main login window
        window_width = 200
        window_height = 300
        screen_width = password_window.winfo_screenwidth()
        screen_height = password_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Apply a custom style to the window
        password_window.configure(bg="#f0f0f0")
        password_window.attributes("-topmost", True)  # Bring the window to the front
        password_window.resizable(False, False)  # Disable resizing

        # Create a frame for the password reset form
        frame = ttk.Frame(password_window, padding=20, relief="ridge", borderwidth=2)
        frame.pack(fill="both", expand=True)

        # Prompt the user to enter a new password
        new_password_label = ttk.Label(frame, text="Enter your new password:", font=("Arial", 10, "bold"), foreground="#333333")
        new_password_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        new_password_entry = ttk.Entry(frame, show="*", font=("Arial", 10), width=20)
        new_password_entry.grid(row=0, column=1, padx=5, pady=5)

        # Function to update the password in the databaseF
        def update_password():
            new_password = new_password_entry.get()
            if new_password:
                # Check if the new password meets the validation requirements
                if len(new_password) < 6 or not new_password.isalnum():
                    messagebox.showerror("Error", "Password must be alphanumeric and at least 6 characters long.")
                    password_window.destroy()
                    return
                
                
                # Update the password in the database
                c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
                conn.commit()
                conn.close()
                password_window.destroy()
                messagebox.showinfo("Password Reset", "Your password has been reset successfully.")
                
            else:
                messagebox.showerror("Error", "Please enter a new password.")

        update_button = ttk.Button(frame, text="Update Password", command=update_password, style="Green.TButton")
        update_button.grid(row=1, columnspan=2, pady=10)

        # Define custom style for the update button
        password_window.style = ttk.Style()
        password_window.style.configure("Green.TButton", foreground="white", background="#4CAF50", font=("Arial", 10, "bold"))

    else:
        # If the username does not exist, display an error message
        messagebox.showerror("Error", "Username not found.")
        conn.close()

def show_password():
    if password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def create_leaderboard_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                 (username TEXT, category_played TEXT, amount_won REAL)''')
    conn.commit()
    conn.close()





def show_category_selection(username):
    global category_window
    category_window = tk.Tk()
    category_window.title("Category Selection")
    category_window.geometry("1430x1430")
    category_window.configure(bg="black")

    img = tk.PhotoImage(file="innitlogor.png")
    img_label = tk.Label(category_window, image=img)
    img_label.configure(bg="black")
    img_label.pack()

        # Create a button to show the leaderboard
    #leaderboard_button = tk.Button(category_window, text="Leaderboard", command=show_leaderboard)
    #eaderboard_button.pack(pady=(20, 5))

        # Create the leaderboard button
    leaderboard_button = Button(category_window, text="Leaderboard", font=("arial",10,"bold"), bg="green", fg="white", bd=0, activebackground="blue", activeforeground='black', cursor="hand2", wraplength=130, command=show_leaderboard)
    leaderboard_button.pack(pady=(20, 5))





    categories = ["GENERAL KNOWLEDGE", "GEOGRAPHY", "HISTORY", "LITERATURE", "MUSIC", "POP CULTURE", "SPORT", "COMPUTER SCIENCE", "RIDDLES", "SCIENCE AND TECHNOLOGY"]


    def start_game_with_category(category, username):
        global category_window
        category_window.destroy() 
        score = main_game(category, username)
        if score == 15:  # Assuming the score is 15 when the user completes the category
            complete_category(category)


    category_frame = ttk.Frame(category_window)
    category_frame.pack()
   

    row = 0
    col = 0
    for category in categories:
        #button = ttk.Button(category_frame, text=category, command=lambda cat=category: start_game_with_category(cat))
        button =Button(category_frame, text=category, font=("arial",10,"bold"), width=20, height=2, bg="green", fg="white",bd=0,activebackground="blue",activeforeground='black',cursor="hand2",wraplength=130,command=lambda cat=category: start_game_with_category(cat, username))
        button.grid(row=row, column=col, padx=20, pady=10)
        col += 1
        if col > 2:  # 3 columns
            col = 0
            row += 1

    logout_button=Button(category_window, text= "logout",font=("arial",16,"bold"),bg="red", fg="white",bd=0,activebackground="red",activeforeground='white',cursor="hand2",wraplength=130, command=logout)#width=20)
    logout_button.place(x=20, y=20)
    logout_button.pack(pady=(80, 50)) 


        # Create exit button

    exit_button=Button(category_window, text= "exit",font=("arial",16,"bold"),bg="black", fg="white",bd=0,activebackground="red",activeforeground='white',cursor="hand2",wraplength=130, command=exit_game)#width=20)
    exit_button.place(x=20, y=20)
    


    category_window.mainloop()


def create_login_window():
    global root, username_entry, password_entry, password_var

    root = tk.Tk()
    root.title("Who Wants to Be a Millionaire - Login")
    root.geometry("1430x1430")
    root.resizable(True, True)  # Allow window expansion

    # Add image of Who Wants to Be a Millionaire
    img = tk.PhotoImage(file="innitlogor.png")
    img_label = tk.Label(root, image=img)
    img_label.pack()

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    username_label = ttk.Label(frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    # Create a rounded entry widget for username
    username_entry = ttk.Entry(frame, style="Rounded.TEntry")
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = ttk.Label(frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    # Create a rounded entry widget for password
    password_var = tk.BooleanVar()
    password_entry = ttk.Entry(frame, show="*", style="Rounded.TEntry")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add "Show Password" checkbutton
    password_checkbutton = ttk.Checkbutton(frame, text="Show Password", variable=password_var, command=show_password)
    password_checkbutton.grid(row=2, columnspan=2, pady=5)

    login_button = ttk.Button(frame, text="Login", command=login, style="Green.TButton", cursor="hand2")
    login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    register_button = ttk.Button(frame, text="Register", command=register, cursor="hand2", style="Blue.TButton")
    register_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")


    forgot_password_label = tk.Label(root, text="Forgot Password?", bg= "#FFFFFF",fg="#007BFF", cursor="hand2")
    forgot_password_label.pack(pady=5)
    forgot_password_label.bind("<Button-1>", lambda e: reset_password())

    # Define custom style for rounded entry widgets
    root.style = ttk.Style()
    root.style.theme_use("classic")
    root.style.configure("Rounded.TEntry", padding=(10, 5), relief="raised", foreground="black")
   
  

    root.mainloop()


def main_game(category, username):
    import pyttsx3
    import sqlite3
    from tkinter import Toplevel, Label, Button, simpledialog
    from pygame import mixer
    
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[0].id)
    
    # Initialize mixer and play background music
    mixer.init()
    mixer.music.load("kbc.mp3")
    mixer.music.play(-1)  
    
    question_counter = 0  # Initialize question counter
    
    def select(event):
        nonlocal question_counter  # Ensure we modify the outer scope variable
        callButtton.place_forget()
        progressBarA.place_forget()
        progressBarB.place_forget()
        progressBarC.place_forget()
        progressBarD.place_forget()
        
        progressbarLabelA.place_forget()
        progressbarLabelB.place_forget()
        progressbarLabelC.place_forget()
        progressbarLabelD.place_forget()
        
        b = event.widget
        value = b["text"]
        
        # Check if answer is correct
        if value == correct_answers[question_counter]:
            question_counter += 1  # Increment question count
            
            # If final question is correct
            if question_counter == 15:
                def close():
                    root2.destroy()
                    root.destroy()
                
                def playagain():
                    lifeline50Button.config(state=NORMAL, image=image50)
                    audiencePoleButton.config(state=NORMAL, image=audiencePole)
                    phoneLifeLineButton.config(state=NORMAL, image=phoneImage)
                    root2.destroy()
                    questionArea.delete(1.0, END)
                    questionArea.insert(END, question[0])
                    optionButton1.config(text=First_options[0])
                    optionButton2.config(text=Second_options[0])
                    optionButton3.config(text=Third_options[0])
                    optionButton4.config(text=Fourth_options[0])
                    
                    entered_category = simpledialog.askstring("Input", "INPUT CATEGORY PLAYED AND CHECK LEADERBOARD:")
                    if entered_category:
                        amount_won = 100000000  # Placeholder, replace with actual score data
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
                
                imgLabel = Label(root2, image=centerImage, bd=0, bg="black")
                imgLabel.pack(pady=30)
                
                tryAgainButton = Button(root2, text="Congratulation! Enter the Category played!!", command=playagain)
                tryAgainButton.pack()
                
                winLabel = Label(root2, text="You Won", font=("arial", 40, "bold"), bg='black', fg="white")
                winLabel.pack()
                
                playagainButton = Button(root2, text="Play Again", font=("arial", 20, "bold"), bg="black", fg="white", command=playagain)
                playagainButton.pack()
                
                closeButton = Button(root2, text="Close", font=("arial", 20, "bold"), bg="black", fg="white", command=close)
                closeButton.pack()
                
                root2.mainloop()
                return
            
            # Every 3 questions, trigger the minigame
            
            if question_counter % 15 == 0:
                mixer.music.stop()
                start_game()  # Call minigame
                mixer.music.play(-1)  # Resume background music after minigame

                
            
            # Load next question
            questionArea.delete(1.0, END)
            questionArea.insert(END, question[question_counter])
            optionButton1.config(text=First_options[question_counter])
            optionButton2.config(text=Second_options[question_counter])
            optionButton3.config(text=Third_options[question_counter])
            optionButton4.config(text=Fourth_options[question_counter])
            amountLabel.configure(image=amountImages[question_counter])
            
        else:
            def close():
                root1.destroy()
                root.destroy()
            
            def tryagain():
                lifeline50Button.config(state=NORMAL, image=image50)
                audiencePoleButton.config(state=NORMAL, image=audiencePole)
                phoneLifeLineButton.config(state=NORMAL, image=phoneImage)
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
            
            imgLabel = Label(root1, image=centerImage, bd=0)
            imgLabel.pack(pady=30)
            
            loseLabel = Label(root1, text="You lose", font=("arial", 40, "bold"), bg='black', fg="white")
            loseLabel.pack()
            
            tryagainButton = Button(root1, text="Try Again", font=("arial", 20, "bold"), bg="black", fg="white", command=tryagain)
            tryagainButton.pack()
            
            closeButton = Button(root1, text="Close", font=("arial", 20, "bold"), bg="black", fg="white", command=close)
            closeButton.pack()
            
            root1.mainloop()

    
    



    def lifeline50():
        lifeline50Button.config(image=image50X,state=DISABLED)
        if questionArea.get(1.0,"end-1c")==question[0]:
           optionButton2.config(text='')
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[1]:
           optionButton1.config(text='')
           optionButton2.config(text="")
        if questionArea.get(1.0,"end-1c")==question[2]:
           optionButton1.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[3]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[4]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[5]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[6]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[7]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[8]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[9]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[10]:
           optionButton1.config(text="")
           optionButton2.config(text="")
        if questionArea.get(1.0,"end-1c")==question[11]:
           optionButton3.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[12]:
           optionButton1.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[13]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[14]:
           optionButton2.config(text="")
           optionButton4.config(text="")




    def audiencePoleLifeLine():
        audiencePoleButton.config(image=audiencePoleX, state=DISABLED)
        progressBarA.place(x=580, y=190)
        progressBarB.place(x=620, y=190)
        progressBarC.place(x=660, y=190)
        progressBarD.place(x=700, y=190)

        progressbarLabelA.place(x=580, y=320)
        progressbarLabelB.place(x=620, y=320)
        progressbarLabelC.place(x=660, y=320)
        progressbarLabelD.place(x=700, y=320)

        if questionArea.get(1.0,"end-1c")==question[0]:
           progressBarA.config(value=30)
           progressBarB.config(value=50)
           progressBarC.config(value=90)
           progressBarD.config(value=60)
        if questionArea.get(1.0,"end-1c")==question[1]:
           progressBarA.config(value=30)
           progressBarB.config(value=50)
           progressBarC.config(value=70)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[2]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=40)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[3]:
           progressBarA.config(value=70)
           progressBarB.config(value=20)
           progressBarC.config(value=40)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[4]:
           progressBarA.config(value=20)
           progressBarB.config(value=30)
           progressBarC.config(value=40)
           progressBarD.config(value=70)
        if questionArea.get(1.0,"end-1c")==question[5]:
           progressBarA.config(value=70)
           progressBarB.config(value=40)
           progressBarC.config(value=20)
           progressBarD.config(value=10)
        if questionArea.get(1.0,"end-1c")==question[6]:
           progressBarA.config(value=40)
           progressBarB.config(value=60)
           progressBarC.config(value=30)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[7]:
           progressBarA.config(value=10)
           progressBarB.config(value=60)
           progressBarC.config(value=40)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[8]:
           progressBarA.config(value=20)
           progressBarB.config(value=40)
           progressBarC.config(value=70)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[9]:
           progressBarA.config(value=30)
           progressBarB.config(value=70)
           progressBarC.config(value=50)
           progressBarD.config(value=20)
        if questionArea.get(1.0,"end-1c")==question[10]:
           progressBarA.config(value=20)
           progressBarB.config(value=50)
           progressBarC.config(value=70)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[11]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=50)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[12]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=40)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[13]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=30)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[14]:
           progressBarA.config(value=20)
           progressBarB.config(value=40)
           progressBarC.config(value=70)
           progressBarD.config(value=50)




    def phoneLifeLine():
        mixer.music.load("calling.mp3")
        mixer.music.play()
        callButtton.place(x=70,y=260)
        phoneLifeLineButton.config(image=phoneImageX,state=DISABLED)

       

    def phoneclick():
        for i in range(15):
           if questionArea.get(1.0,'end-1c')==question[i]:
              engine.say(f"The answer is {correct_answers[i]}")
              engine.runAndWait()
              mixer.init()
              mixer.music.load("kbc.mp3")
              mixer.music.play(-1)


#GENERAL KNOWLEDGE

    if category == "GENERAL KNOWLEDGE":
        correct_answers = [
        "Tokyo","Canberra", "Mars","Shakespeare","Pacific Ocean",
        "1776", "Vincent van Gogh", "Yen", "Nitrogen",
        "Albert Einstein", "Japan", "Blue whale",
        "Helium", "Harper Lee", "Ottawa"]

        question=["What is the capital of Japan?",
            "What is the capital city of Australia?",
            "Which planet is known as the Red Planet?",
            "Who wrote 'Romeo and Juliet?",
            "What is the largest ocean on Earth?",
            "In what year did the United States declare its independence?",
            "Who painted the famous artwork \"Starry Night\"?",
            "What is the currency of Japan?",
            "Which gas makes up the majority of Earth's atmosphere?",
            "Who is known as the \"Father of Modern Physics\"?",
            "Which country is known as the \"Land of the Rising Sun\"?",
            "What is the largest mammal in the world?",
            "Which of the following elements is a noble gas?",
            "Who wrote the famous novel \"To Kill a Mockingbird\"?",
            "What is the capital city of Canada?"]

        First_options = [
            "Seoul",
            "Sydney",
            "Venus",
            "Shakespeare",
            "Atlantic Ocean",
            "1776",
            "Pablo Picasso",
            "Won",
            "Oxygen",
            "Isaac Newton",
            "China",
            "Elephant",
            "Oxygen",
            "J.K. Rowling",
            "Vancouver"
        ]
        Second_options = [
        "Beijing","Melbourne", "Mars", "Jane Aust", "Indian Ocean",
        "1789", "Vincent van Gogh", "Yen", "Carbon dioxide",
        "Albert Einstein", "South Korea", "Blue whale",
        "Helium", "Harper Lee", "Toronto"
        ]

        Third_options = [
        "Tokyo","Canberra", "Jupiter", "C.Dickens","Southern Ocean",
        "1800", "Leonardo Vinci", "Baht", "Nitrogen",
        "Galilei", "Japan", "Giraffe",
        "Sodium", "Ernest Hemingway", "Ottawa"
        ]

        Fourth_options = [
        "BangKok","Brisbane", "Saturn","Emily Brontë", "Pacific Ocean",
        "1865", "Claude Monet", "Ringgit", "Hydrogen",
        "Nikola Tesla", "Vietnam","Gorilla",
        "Carbon", "Scott gerald", "Montreal"
        ]     
    
    #GEOGRAPHY 

    elif category == "GEOGRAPHY": 
          correct_answers = [
          "Canberra","Brazil", "Nile","Russia","Canada",
          "Mount Everest", "Tokyo", "France", "Arctic Ocean",
          "India", "Antarctica", "China",
          "Pacific Ocean", "Mexico", "Africa"]
            
          question = ["What is the capital city of Australia?",
              "Which country is the largest by land area?",
              "What is the longest river in the world?",
              "Which country spans across Europe and Asia?",
              "Which is the second largest country by land area?",
              "Which is the highest mountain peak on Earth?",
              "What is the capital city of Japan?",
              "Which country is famous for the Eiffel Tower?",
              "Which ocean is the smallest and shallowest?",
              "Which country is known for the Taj Mahal?",
              "Which continent is entirely located in the Southern Hemisphere?",
              "Which country has the largest population?",
              "Which ocean is the largest and deepest?",
              "Which country is known for the ancient ruins of Chichen Itza?",
              "Which continent is known as the 'Dark Continent'?"]

          First_options = [
              "Sydney",
              "Australia",
              "Amazon",
              "Russia",
              "Finland",
              "Mount Everest",
              "Beijing",
              "Italy",
              "Indian Ocean",
              "Australia",
              "Asia",
              "Mali",      
              "Atlantic Ocean",
              "USA",
              "Asia"
          ]
          Second_options = [
          "Melbourne","England", "Nile", "USA", "Turkey",
          "Kangchenjunga", "Tokyo", "France", "Southern Ocean",
          "India", "Australia", "China",
          "Pacific Ocean", "Mexico", "Europe"
          ]

          Third_options = [
          "Canberra","Brazil", "Mississippi", "Scotland", "Spain",
          "Mont Blanc", "Seoul", "UK", "Arctic Ocean",
          "Japan", "Antarctica", "Norway",
          "Indian Ocean", "Canada", "Africa"
          ]

          Fourth_options = [
          "Perth","Australia", "Ganges", "United States", "Canada",
          "K2", "Osaka", "Germany", "Atlantic Ocean",
          "Chile", "Europe", "Garbon",
          "Southern Ocean", "Spain", "South America"
          ]

        #HISTORY 
    elif category == "HISTORY":
          correct_answers = [
                    "1776",
                    "Julius Caesar",
                    "Marie Curie",
                    "World War II",
                    "Industrial Revolution",
                    "Magna Carta",
                    "Nelson Mandela",
                    "Vietnam War",
                    "Russia",
                    "Napoleon Bonaparte",
                    "Great Depression",
                    "Cleopatra",
                    "Renaissance",
                    "Winston Churchill",
                    "Silk Road"
        ]

          question = [
            "In what year did the United States declare its independence?",
            "Who was the first Roman Emperor?",
            "Who was the first woman to win a Nobel Prize?",
            "During which conflict was the Battle of Stalingrad fought?",
            "Which period saw major advancements in manufacturing, transportation, and technology?",
            "What was the name of the document signed by King John of England in 1215?",
            "Who was the first black President of South Africa?",
            "Which war ended with the fall of Saigon in 1975?",
            "The Bolshevik Revolution of 1917 took place in which country?",
            "Who famously said, 'A soldier will fight long and hard for a bit of colored ribbon'?",
            "What was the name given to the period of severe economic downturn in the 1930s?",
            "Who was the last active pharaoh of ancient Egypt?",
            "Which period in European history is known for its revival of art, literature, and learning?",
            "Who was the British Prime Minister during World War II?",
            "What ancient network of trade routes connected the East and West?"
        ]

          First_options = [
            "1789",
            "Claudius",
            "Margaret Thatcher",
            "World War II",
            "Victorian Era",
            "Magna Carta",
            "Martin Luther King Jr.",
            "Korean War",
            "France",
            "Dust Bowl",
            "World War V",
            "Hatshepsut",
            "Middle Ages",
            "Franklin D. Roosevelt",
            "Spice Route"
        ]

          Second_options = [
            "1800",
            "Augustus",
            "Marie Curie",
            "Vietnam War",
            "Declaration of Independence",
            "Nelson Mandela",
            "Vietnam War",
            "Germany",
            "Napoleon Bonaparte",
            "The triad war",
            "Cleopatra",
            "Renaissance",
            "Winston Churchill",
            "Trans-Saharan Route"
        ]

          Third_options = [
            "1776",
            "Julius Caesar",
            "Rosa Parks",
            "Cold War",
            "Food crisis era",
            "Treaty of Versailles",
            "Malcolm X",
            "Afghanistan War",
            "Russia",
            "Joseph Stalin",
            "Great Depression",
            "Nefertiti",
            "Enlightenment",
            "Mercy Thatcher",
            "Silk Road"
        ]

          Fourth_options = [
            "1865",
            "Nero",
            "Florence Nightingale",
            "Industrial Revolution",
            "Enlightenment",
            "Emancipation Proclamation",
            "Barack Obama",
             "Gulf War",
            "China",
            "Wisdom Churchill",
            "Warm war",
            "Queen Elizabeth I",
            "Industrial Revolution",
            "Neville Chamberlain",
            "Marco Polo Route"
        ]
            #LITERATURE

    
    elif category == "LITERATURE":
          correct_answers = [
            "William Shakespeare",
            "Charles Dickens",
            "Leo Tolstoy",
            "J.K. Rowling",
            "Herman Melville",
            "Romeo and Juliet",
            "George Orwell",
            "Harper Lee",
            "Agatha Christie",
            "Hamlet",
            "J.R.R. Tolkien",
            "Mark Twain",
            "George R.R. Martin",
            "Jane Austen",
            "Miguel de Cervantes"
        ]

          question = [
            "Who is the author of 'Romeo and Juliet'?",
            "Who wrote the novel 'Great Expectations'?",
            "Who wrote 'War and Peace'?",
            "Who is the author of the 'Harry Potter' series?",
            "Who wrote 'Moby-Dick'?",
            "Which play is known as 'The Tragedy of the Prince of Denmark'?",
            "Who wrote '1984'?",
            "Who authored 'To Kill a Mockingbird'?",
            "Who created the fictional detective Hercule Poirot?",
            "Which Shakespearean tragedy features the character Ophelia?",
            "Who wrote 'The Lord of the Rings' trilogy?",
            "Who wrote 'The Adventures of Huckleberry Finn'?",
            "Who is the author of 'A Song of Ice and Fire' series?",
            "Who wrote 'Pride and Prejudice'?",
            "Who wrote 'Don Quixote'?"
        ]

          First_options = [
            "John Milton",
            "Jane Austen",
            "Fyodor Dostoevsky",
            "J.K. Rowling",
            "Stephen King",
            "Romeo and Juliet",
            "Aldous Huxley",
            "Truman Capote",
            "Raymond Chandler",
            "King Lear",
            "J.K. Rowling",
            "F. Scott Fitzgerald", 
            "J.R. Tolkien",
            "Emily Brontë",
           "Fyodor Dostoevsky"
        ]

          Second_options = [
            "George Orwell",
            "George Eliot",
            "Leo Tolstoy",
            "Marks Twaine ",
            "Ernest Hemingway",
            "Macbeth",
            "George Orwell",
            "Harper Lee",
            "Arthur Conan Doyle",
            "Hamlet",
            "George R.R. Martin",
            "Mark Twain",
            "George R.R. Martin"
            "Jane Austins",
            "Leo Tolstoy"
        ]

          Third_options = [
            "William Shakespeare",
            "Charles Dickens",
            "Leo Tolstoy",
            "J.R.R. Tolkien",
            "Charles Dickens",
            "Othello",
            "J.R.R. Tolkien",
            "J.D. Salinger",
            "Agatha Christie", 
            "Things fall apart",
            "J.R.R. Tolkien",
            "Charles Dickens",
            "George R. Martinez",
            "Charlotte Brontë",
            "Miguel de Cervantes" 
        ]

          Fourth_options = [
            "William Wordsworth",
            "Herman Melville",
            "Fyodor Dostoevsky",
            "Dan Brown",
            "Herman Melville", 
            "King Lear",
            "George Orl",
            "Harper Lee",
            "Sir Arthur Conan Doyle",
            "Othello",
            "Mark Titus",
            "Ernest Hemingwa",
            "J.K. Rowling",
            "Jane Austen",
            "Kodor Dostoe"
        ]


        #MUSIC
    elif category == "MUSIC":
          correct_answers = [
            "Michael Jackson",
            "Mozart",
            "The Beatles",
            "Elvis Presley",
            "Adele",
            "Led Zeppelin",
            "Beethoven",
            "Madonna",
            "Bach",
            "Queen",
            "Johnny Cash",
            "Taylor Swift",
            "Pink Floyd",
            "Stevie Wonder",
            "Beyoncé"
        ]

          question = [
            "Who is known as the 'King of Pop'?",
            "Who composed 'The Magic Flute'?",
            "Which band is often referred to as the 'Fab Four'?",
            "Who is often referred to as the 'King of Rock and Roll'?",
            "Which artist released the album '21'?",
            "Which band released the iconic song 'Stairway to Heaven'?",
            "Who composed 'Für Elise'?",
            "Who is often referred to as the 'Queen of Pop'?",
            "Which composer is known for composing 'Air on the G String'?",
            "Which band sang 'Bohemian Rhapsody'?",
            "Who is known as the 'Man in Black'?",
            "Which artist released the album '1989'?",
            "Which band released the album 'The Dark Side of the Moon'?",
            "Who is often referred to as the 'Prince of Motown'?",
            "Which artist released the album 'Lemonade'?"
        ]

          First_options = [
            "Prince",
            "Beethos",
            "The Rolling Stones",
            "Elvis Presley",
            "Pink Flop",
            "Led Zeppelin",  
            "J.S. Bach",
            "Macdonald",
            "Mozar",
            "The Bales",
            "John Cash",
            "Adef",
            "The Beat",
            "Marvin Gaye",
            "Rihanna"
        ]

          Second_options = [
            "Elv Presle",
            "Bechez", 
            "The Beatles",
            "Bob Dylan",
            "Taylor Swiss",
            "Bestert",
            "Beethoven",
            "Madonna",
            "Thovan",
            "Queen",
            "Ned Seppelin",
            "Taylor Swift",
            "Pink Floyd",
            "Stevie Wonder",
            "Britney Spears"
        ]

          Third_options = [
            "Michael Jackson",
            "Mozart",
            "The Beach Boys",
            "Chuck Berry",
            "Mariah Carey",
            "The Eagles",
            "Johann Strauss II",
            "Whitney Houston",
            "Bach",
            "The Rollers",
            "Johnny Cash",
            "Ariana Grande",
            "The Rolling Stones",
            "Ray Charles",
            "Beyoncé"
        ]

          Fourth_options = [
            "Stevie Wood",
            "Beethos",
            "The Beles",
            "Elton John",
            "Adele", 
            "AC/DC",
            "Frederic Chopin",
            "Celine Dion",
            "Brahms",
            "Pire Floy",
            "David Bowie", 
            "Katy Perry",
            "Ledo Zeppelins",
            "B.B. King",
            "Mariah Carey"
        ]

        #POP CULTURE
    elif category == "POP CULTURE":
          correct_answers = [
            "Beyoncé",
            "Leonardo DiCaprio",
            "Taylor Swift",
            "Kim Kardashian",
            "Harry Potter",
            "Stranger Things",
            "Drake",
            "Ariana Grande",
            "Game of Thrones",
            "Michael Jackson",
            "Friends",
            "Beyoncé and Jay-Z",
            "BTS",
            "Lady Gaga",
            "Justin Bieber"
        ]

          question = [
            "Who is known as the 'Queen B' of music?",
            "Who won an Oscar for Best Actor for his role in 'The Revenant'?",
            "Who is known as the 'Queen of Pop'?",
            "Who became famous after a leaked tape with Ray J?",
            "Which book series features a character named Hermione Granger?",
            "Which TV series features a group of kids facing supernatural events in a small town called Hawkins?",
            "Who released the album 'Scorpion' in 2018?",
            "Which singer is known as the 'Princess of Pop'?",
            "Which TV series is based on the book series 'A Song of Ice and Fire'?",
            "Who is known as the 'King of Pop'?",
            "Which TV series revolves around the lives of six friends living in New York City?",
            "Which celebrity couple is often referred to as 'Bey-Z'?",
            "Which K-pop group has members named RM, Jin, Suga, J-Hope, Jimin, V, and Jungkook?",
            "Who performed the halftime show at the Super Bowl LI in 2017?",
            "Who gained popularity after being discovered by talent manager Scooter Braun on YouTube?"
        ]

          First_options = [
            "Adele",
            "Johnny Depp",
            "Rihanna",
            "Kim Kardashian",
            "Twilight",
            "Stranger Things",
            "Kanye West",
            "Britney Spears",
            "Breaking Bad",
            "Elvis Presley",
            "How I Met Your Mother",
            "Kanye West and Kim Kardashian",
            "BLACKPINK",
            "Rihanna",
            "Selena Gomez"
        ]

          Second_options = [
            "Taylor Swift",
            "Tom Cruise", 
            "Taylor Swift",
            "Paris Hilton",
            "The Hunger Games",
            "The Crown",  
            "Drake",
            "Ariana Grande",
            "Stranger Things",
            "Michael Jackson",
            "The Office",
            "Beyoncé and Jay-Z",
            "BTS",
            "Lady Gaga", 
            "Justin Timberlake"
        ]

          Third_options = [
            "Beyoncé",
            "Leonardo DiCaprio",
            "Lady G",
            "Kylie Jenner",
            "Game of Thrones",  
            "Riverdale",
            "Eminem",
            "Katy Perry",
           "Game of Thrones",
            "Prince",
            "Friends",
            "Jay-Z and Rihanna",
            "NCT",
            "Beyoncé",
            "Justin Bieber"
        ]

          Fourth_options = [
            "Ariana Grane",
            "Brad Pitt",
            "Madonna", 
            "Kendall Jenner",
            "Harry Potter",
            "Gossip Girl",
            "Justin Mark",
            "Lady Gaga",
            "The Witcher",
            "Justice Biebers",
            "Glee",
            "Selena Gomez and Justin Bieber",
            "EXO",
            "Katy Perry",
           "Shawn Mendes"
        ]
   
        #SPORT
    elif category == "SPORT" :
          correct_answers = [
            "Michael Jordan",
            "Muhammad Ali",
            "Cristiano Ronaldo",
            "Serena Williams",
            "Lionel Messi",
            "Usain Bolt",
            "Basketball",
            "Novak Djokovic",
            "Roger Federer",
            "Michael Phelps",
            "Simone Biles",
            "Tiger Woods",
            "Rafael Nadal",
            "Tom Brady",
            "Sachin Tendulkar"
        ]

          question = [
            "Who is often considered the greatest basketball player of all time?",
            "Who is known as 'The Greatest' in boxing?",
            "Which footballer has won the most FIFA Ballon d'Or awards?",
            "Who holds the record for the most Grand Slam singles titles in tennis?",
            "Who has won the most FIFA Ballon d'Or awards in football?",
            "Who holds the world record for the 100m sprint?",
            "Which sport is associated with Wilt Chamberlain?",
            "Who has won the most Australian Open titles in men's singles tennis?",
            "Which tennis player has won the most Wimbledon titles?",
            "Who holds the record for the most Olympic gold medals in swimming?",
            "Who is often regarded as the greatest gymnast of all time?",
            "Who is considered one of the greatest golfers of all time?",
            "Who has won the most French Open titles in men's singles tennis?",
            "Who is the quarterback with the most Super Bowl wins?",
            "Who is often referred to as the 'God of Cricket'?"
        ]

          First_options = [
            "Kobe Bryant",
            "Mike Tyson",
            "Serena Williams",
            "Venus Williams",
            "Cristian Ronaldino",
            "Usain Bolt",
            "Football",
            "Raf Nerd",
            "Andy Murray", 
            "Mark Spitz",
            "Nadia Comăneci",
            "Jack Nicklaus",
            "Andre Agassi",
            "Peyton Manning",
            "Virat Kohli"
        ]

          Second_options = [
            "LeBron James",
            "Floyd Mayweather Jr.",
            "Cristiano Ronaldo",
            "Ronaldinho Ronald",  
            "Diego Maradona",
            "Carl Lewis",
            "Basketball",
            "Novak Djokovic",
            "Rafael Nadal",
            "Michael Phelps",
            "Aly Raisman", 
            "Tiger Woods",
            "Rogers Feder",
            "Tom Brady",
            "Ricky Ponting"  
        ]

          Third_options = [
            "Michael Jordan",
            "Muhammad Ali",
            "Neymar",
            "Steffi Graf",
            "Neymar",
            "Asafa Powell",
            "Golf",
            "Stan Wawrinka",
            "Roger Federer"
            "Hsaisen Bolt",
            "Simone Biles",
            "Phil Mickelson",
            "Rafael Nadal",
            "Joe Montana",
            "Sachin Tendulkar"
        ]

          Fourth_options = [
            "Magic Johnson", 
            "Sugar Ray Robinson",
            "Diego Maradona",
            "Margaret Court",
            "Lionel Messi",
            "Michael Johnson",
            "Tennis",  
            "Novak Djokovic",
            "Pete Sampras",
            "LeBron James",
            "Nastia Liukin",
            "Arnold Palmer", 
            "Novak Djokovic",
            "Tom Branek",
            "Brian Lara"
        ]

        # COMPUTER SCIENCE 
    elif category == "COMPUTER SCIENCE":
          correct_answers = [
            "To analyze algorithm complexity",
            "A programming paradigm based on objects",
            "TCP provides reliable data delivery, while UDP is connectionless and unreliable",
            "To translate high-level code into machine code",
            "To eliminate redundancy and improve data integrity",
            "Symmetric encryption uses the same key for encryption and decryption",
            "It allows the execution of programs larger than physical memory",
            "A machine learning model inspired by the human brain",
            "To reduce the size of data for storage or transmission",
            "To store frequently accessed data for faster access",
            "A stack follows Last In, First Out (LIFO) principle",
            "Encourages code reusability and modularity",
            "A linked list stores elements sequentially in memory",
            "Recursion involves a function calling itself until a base case is reached",
            "HTTP is unencrypted, while HTTPS encrypts data for secure transmission"
        ]

          question = [
            "What is Big O notation used for in computer science?",
            "Explain the concept of object-oriented programming.",
            "What are the primary differences between TCP and UDP protocols?",
            "Describe the role of a compiler in software development.",
            "What is data normalization in databases and why is it important?",
            "Differentiate between symmetric and asymmetric encryption algorithms.",
            "Explain the concept of virtual memory in operating systems.",
            "What is a neural network and how does it differ from traditional algorithms?",
            "Describe the principles of data compression.",
            "What is the purpose of a cache in computer architecture?",
            "Differentiate between a stack and a queue in data structures.",
            "What are the advantages and disadvantages of object-oriented programming?",
            "Explain the difference between a linked list and an array.",
            "How does recursion work in algorithm design?",
            "Describe the role of HTTP and HTTPS in web communication."
        ]

          First_options = [
            "To analyze algorithm complexity",
            "A programming paradigm based on procedures",
            "TCP is connectionless, while UDP provides reliable data delivery",
            "To translate high-level code into machine code",
            "To organize data in a hierarchical structure",
            "Symmetric encryption uses the same key for encryption and decryption",
            "It allows multiple processes to share a single CPU",
            "A machine learning model for natural language processing",
            "To reduce the size of data for storage or transmission",
            "To enhance the functionality of CPU registers",
            "To facilitate parallel processing",
            "Encourages code reusability and modularity",
            "An array provides constant-time access to elements",
            "Recursion involves a function calling itself indefinitely",
            "HTTP is unencrypted, while HTTPS encrypts data for secure transmission"
        ]

          Second_options = [
            "To store large datasets efficiently",
            "A programming paradigm based on functions",
            "TCP provides reliable data delivery, while UDP is connectionless and unreliable",
            "To interpret code line by line during execution",
            "To eliminate redundancy and improve data integrity",
            "Asymmetric encryption is faster than symmetric encryption",
            "It allows the execution of programs larger than physical memory",
            "A search algorithm for finding optimal solutions",
            "To increase the size of data for better analysis",
            "To store frequently accessed data for faster access",
            "A queue follows First In, First Out (FIFO) principle",
            "Encourages procedural programming",
            "A linked list stores elements sequentially in memory",
            "Recursion involves dividing a problem into smaller subproblems",
            "HTTP compresses data for faster transmission"
        ]

          Third_options = [
            "To design user interfaces",
            "A programming paradigm based on objects",
            "TCP guarantees packet delivery, while UDP doesn't guarantee",
            "To manage hardware resources and provide services",
            "To optimize database query performance",
            "Symmetric encryption is more secure than asymmetric encryption",
            "It increases the execution speed of programs",
            "A sorting algorithm for arranging data alphabetically",
            "To eliminate data redundancy for better storage efficiency",
            "Both have the same principlesA stack follows Last In, First Out (LIFO) principle",
            "Encourages functional programming",
            "Both have the same characteristics",
            "Recursion involves sorting elements sequentially",
            "HTTP adds layers of security to data transmission"
        ]

          Fourth_options = [
            "To measure the speed of data transmission",
            "A programming paradigm based on events",
            "TCP is faster than UDP",
            "To debug code during development",
            "To increase redundancy for data recovery",
            "Asymmetric encryption is more secure than symmetric encryption",
            "It simulates the behavior of a physical memory",
            "A machine learning model inspired by the human brain",
            "To improve data compression ratio",
            "To allocate memory for program execution",
            "None of the above",
            "None of the above",
            "None of the above",
            "Recursion involves a function calling itself until a base case is reached",
            "HTTPS slows down web communication"
        ]

            # RIDDLES

    elif category == "RIDDLES":


          correct_answers = [
            "A piano",
            "A candle",
            "The letter 'm'",
            "A coin",
            "Footsteps",
            "The piano",
            "A stamp",
            "A towel",
            "Rain",
            "Your name",
            "A bottle",
            "A leg",
            "A clock",
            "A joke",
            "A map"
    ]       
          question = [
            "What has keys but can't open locks?",
            "I'm tall when I'm young, and I'm short when I'm old. What am I?",
            "What comes once in a minute, twice in a moment, but never in a thousand years?",
            "What has a head, a tail, is brown, and has no legs?",
            "The more you take, the more you leave behind. What am I?",
            "What has many keys but can't open a single lock?",
            "What can travel around the world while staying in a corner?",
            "What gets wet while drying?",
            "What comes down but never goes up?",
            "What belongs to you, but other people use it more than you do?",
            "What has a neck but no head?",
            "What has a bottom at the top?",
            "What has a face and two hands but no arms or legs?",
            "What can be cracked, made, told, and played?",
            "What has cities, but no houses; forests, but no trees; and rivers, but no water?"
        ]

          First_options = [
            "A piano",
            "A tree",
            "The letter 'a'",
            "A snake",
            "Leaves", 
            "The piano",
            "The book",
            "A sponge",
            "Rain",
            "Your phone number",
            "A book",
            "A leg",
            "A watch",
            "A riddle",
            "A map"
        ]

          Second_options = [
            "A keyboard",
            "A pecil",
            "The letter 'e'",
            "A penny",
            "Footsteps",
            "A keyboard",
            "A stamp",
            "A towel",
            "Sunset",
            "Your name",
            "A giraffe",
            "A hat",
            "A clock",
            "A song",
            "A globe"
        ]

          Third_options = [
            "A book",
            "A candle",
            "The letter 'm'",
            "A coin",
            "Memories",
            "A remote",
            "A stone",
            "A mirror",
            "A bird",
            "Your email address",
            "A bottle",
            "A snake",
            "A mirror",
            "A story",
            "A dictionary"
        ]

          Fourth_options = [
            "A flute",
            "A coin",
            "The letter 'o'",
            "A dog",
            "Time",
            "A password",
            "A wind",
            "A hairdryer",
            "A moon",
            "Your social security number",
            "A niddle",
            "A tree",
            "A clamp",
            "A joke",
            "A forest"
        ]



            # SCIENCE AND TECHNOLOGY
        
    elif category == "SCIENCE AND TECHNOLOGY":


          correct_answers = [
                "Photosynthesis",
                "Albert Einstein",
                "Atom",
                "Central Processing Unit",
                "Mercury",
                "Tim Berners-Lee",
                "Deoxyribonucleic Acid",
                "Carbon Dioxide",
                "H2O",
                "Meteorology",
                "Cheetah",
                "mass",
                "Newton",
                "Evaporation",
                "Skin"
        ]

          question = [
            "What is the process of converting light energy into electrical energy known as?",
            "Which famous scientist developed the theory of relativity?",
            "What is the smallest unit of matter?",
            "What does CPU stand for in the context of computing?",
            "What is the name of the closest planet to the Sun in our solar system?",
            "Who is credited with inventing the World Wide Web?",
            "What does DNA stand for in biology?",
            "Which gas do plants use for photosynthesis?",
            "What is the chemical symbol for water?",
            "What is the study of Earth's atmosphere called?",
            "What is the fastest animal on land?",
            "Which is a basic quantity?",
            "What is the SI unit of force?",
            "What is the process of a liquid turning into a gas called?",
            "What is the largest organ in the human body?"
        ]

          First_options = [
            "Photosynthesis",
            "Isaac Newton",
            "Molecule",
            "Central Processing Unit",
            "Mars",
            "Tim Berners-Lee",
            "Ribonucleic Acid",
            "Oxygen",
            "H2O",
            "Geology",
            "Leopard",
            "mass",
            "Joule",
            "Sublimation",
            "Liver"
        ]

          Second_options = [
            "Respiration",
            "Galileo Galilei",
            "Atom",
            "Computer Processing Unit",
            "Mercury",
            "Nikola Tesla",
            "Deoxyribonucleic Acid",
            "Carbon Dioxide",
            "O2",
            "Meteorology",
            "Lion",
            "force",
            "Watt",
            "Evaporation",
            "Brain"
        ]

          Third_options = [
            "Transmutation",
            "Albert Einstein",
            "Proton",
            "Central Power Unit",
            "Venus",
            "Tim Cook",
            "Deoxyribonucleic Acid",
            "Nitrogen",
            "CO",
            "Oceanography",
            "Cheetah",
            "density",
            "Newton",
            "Condensation",
            "Skin"
        ]

          Fourth_options = [
            "Solarization",
            "Johannes Kepler",
            "Electron",
            "Center Power Unit",
            "Earth",
            "Al Gore",
            "None of the above",
            "Hydrogen",
            "H2O2",
            "Meteorology",
            "Giraffe",
            "weight",
            "Pascal",
            "Deposition",
            "Heart"
        ]

   
    else:
        messagebox.showerror("Invalid Category", "Please select a valid category.")
        return

   
        # Shuffle the questions, options, and correct answers together
    #questions_and_options = list(zip(question, First_options, Second_options, Third_options, Fourth_options, correct_answers))
    #random.shuffle(questions_and_options)

    # Unpack the shuffled values
    #question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)

    # Now your data is shuffled and ready to use in your game

    # Shuffle the lifelines
    #lifelines = [lifeline50, audiencePoleLifeLine, phoneLifeLine]
    #random.shuffle(lifelines)




# Shuffle the questions, options, and correct answers together
    #questions_and_options = list(zip(question, First_options, Second_options, Third_options, Fourth_options, correct_answers))
    #random.shuffle(questions_and_options)

    # Unpack the shuffled values
    #question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)       
        
    #question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)


    root=Tk()
    root.geometry("1430x1430+0+0")
    root.title("who want to be a millionaire created by Terry.G.")

    root.config(bg="black")
    #==============================================Frames=====================================#
    leftframe=Frame(root,bg = "black",padx=90)
    leftframe.grid()

    topFrame = Frame(leftframe,bg="black",pady=15)
    topFrame.grid()

    centerFrame = Frame(leftframe,bg="black",pady=15)
    centerFrame.grid(row=1, column=0)

    bottomFrame = Frame(leftframe)
    bottomFrame.grid(row=2, column=0)

    rightframe=Frame(root,pady=25,padx=50,bg="black")
    rightframe.grid(row=0, column=1)
    #===============================================IMAGES================================================#
    image50=PhotoImage(file="50-50.png")
    image50X=PhotoImage(file="50-50-X.png")

    lifeline50Button = Button(topFrame, image=image50, bg="black",bd=0,activebackground='black',width=180,height=80,command=lifeline50)

    lifeline50Button.grid(row=0,column=0)

    audiencePoleX=PhotoImage(file="audiencePoleX.png")
    audiencePoleButton = Button(topFrame, image=audiencePoleX,bg="black",bd=0,activebackground="black",width=180,height=80,command=audiencePoleLifeLine)
    audiencePoleButton.grid(row=0,column=1)

    audiencePole=PhotoImage(file="audiencePole.png")
    audiencePoleButton = Button(topFrame, image=audiencePole,bg="black",bd=0,activebackground="black",width=180,height=80,command=audiencePoleLifeLine)
    audiencePoleButton.grid(row=0,column=1)

    phoneImage=PhotoImage(file="phoneAFriend.png")
    phoneImageX=PhotoImage(file="phoneAFriendX.png")

    phoneLifeLineButton = Button(topFrame,image=phoneImage,bg="black",bd=0,activebackground='black',width=180,height=80,command=phoneLifeLine)
    phoneLifeLineButton.grid(row=0,column=2)

    callimage=PhotoImage(file="phone.png")
    callButtton=Button(root,image=callimage,bd=0,bg="black",activebackground="black",cursor="hand2", command=phoneclick)

    centerImage= PhotoImage(file="innitlogor1.png")
    logoLabel=Label(centerFrame, image=centerImage,bg="black",width=300,height=200)
    logoLabel.grid()

    amountImage=PhotoImage(file="Picture0.png")
    amountImage1=PhotoImage(file="Picture1.png")
    amountImage2=PhotoImage(file="Picture2.png")
    amountImage3=PhotoImage(file="Picture3.png")
    amountImage4=PhotoImage(file="Picture4.png")
    amountImage5=PhotoImage(file="Picture5.png")
    amountImage6=PhotoImage(file="Picture6.png")
    amountImage7=PhotoImage(file="Picture7.png")
    amountImage8=PhotoImage(file="Picture8.png")
    amountImage9=PhotoImage(file="Picture9.png")
    amountImage10=PhotoImage(file="Picture10.png")
    amountImage11=PhotoImage(file="Picture11.png")
    amountImage12=PhotoImage(file="Picture12.png")
    amountImage13=PhotoImage(file="Picture13.png")
    amountImage14=PhotoImage(file="Picture14.png")
    amountImage15=PhotoImage(file="Picture15.png")

    amountImages = [amountImage1, amountImage2, amountImage3, amountImage4, amountImage5,
                    amountImage6, amountImage7, amountImage8, amountImage9, amountImage10,
                    amountImage11, amountImage12, amountImage13, amountImage14, amountImage15]
    amountLabel=Label(rightframe,image=amountImage,bg="black")
    amountLabel.grid()

    LayoutImage=PhotoImage(file="lay.png")
    LayoutLabel=Label(bottomFrame, image=LayoutImage,bg="black")
    LayoutLabel.grid()
    #=============================================QUESTION AREA==========================================#
    questionArea=Text(bottomFrame, font=("arial",18,"bold"),width=34,height=2,wrap="word",bg="black",fg="white",bd=0)
    questionArea.place(x=70,y=10)

    questionArea.insert(END,question[0])

    labelA = Label(bottomFrame,font=("arial",16,"bold"), text="A: ", bg="black", fg="white",)
    labelA.place(x=60,y=110)

    optionButton1=Button(bottomFrame, text= First_options[0],font=("arial",10,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#width=20)

    optionButton1.place(x=100, y=100)

    labelB = Label(bottomFrame,font=("arial",15,"bold"), text="B: ", bg="black", fg="white",)
    labelB.place(x=330,y=110)
    optionButton2=Button(bottomFrame, text= Second_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#idth=20)
    optionButton2.place(x=370, y=100)

    labelC = Label(bottomFrame,font=("arial",16,"bold"), text="C: ", bg="black", fg="white",)
    labelC.place(x=60,y=190)
    optionButton3=Button(bottomFrame, text= Third_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#,wraplength=200,width=20)
    optionButton3.place(x=100, y=180)
    labelD = Label(bottomFrame,font=("arial",16,"bold"), text="D: ", bg="black", fg="white",)
    labelD.place(x=330,y=190)
    optionButton4=Button(bottomFrame, text= Fourth_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#width=20)
    optionButton4.place(x=370, y=180)
    #===========================Progress Bar(AUDIENCE POLL BUTTONS AND LABEL)=================================#
    progressBarA=Progressbar(root,orient=VERTICAL,length=120)
    progressBarB=Progressbar(root,orient=VERTICAL,length=120)
    progressBarC=Progressbar(root,orient=VERTICAL,length=120)
    progressBarD=Progressbar(root,orient=VERTICAL,length=120)

    progressbarLabelA=Label(root, text="A", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelB=Label(root, text="B", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelC=Label(root, text="C", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelD=Label(root, text="D", font=("arial",20,"bold"),bg='black', fg="white")
    #option_mapping = {"A": progressBarA, "B": progressbarLabelB, "C": progressbarLabelC, "D": progressbarLabelD}
    #correct_answer=StringVar()



    #=======================================OPTION FUNCTION==================================================#
    optionButton1.bind('<Button-1>', select)
    optionButton2.bind('<Button-1>', select)
    optionButton3.bind('<Button-1>', select)
    optionButton4.bind('<Button-1>', select)
    

  


     #exit , music stops playing
    def exit_game():
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the game?"):
            mixer.music.stop()
            root.destroy()
        # Optionally, you can also return to the category selection window
            show_category_selection(username)
    
    def start_timer(duration):
        while duration:
            mins, secs = divmod(duration, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            timer_label.config(text=timeformat)
            root.update()
            time.sleep(1)
            duration -= 1
        messagebox.showinfo("Time's up", "Time is up, returning to category selection.")
        mixer.music.stop()
        root.destroy()
        # Optionally, you can also return to the category selection window
        show_category_selection(username)
   

    # Set the default style to have a red background
    root.style = ttk.Style()
    root.style.configure(".", background="red", foreground="black")



    exit_button = Button(root, text="Exit", bg="red", fg="white",bd=0,activebackground="red",activeforeground='white',cursor="hand2",wraplength=190, command=exit_game)
    exit_button.grid(row=0, column=4, sticky="ne", padx=10, pady=10)


   

 
    # Create a label to display the timer
    timer_label = ttk.Label(root, text="00:00", font=("Arial", 16), background="red", foreground="white")
    timer_label.grid(row=0, column=0, padx=10, pady=10)

    start_button=Button(root, text="Start Timer", font=("arial",10,"bold"),bg="green", fg="white",bd=0,activebackground="red",activeforeground='white',cursor="hand2",wraplength=130, command=lambda: start_timer(60))
    start_button.grid(row=1, column=0, padx=10, pady=5)



    root.mainloop()



create_login_window()



    










