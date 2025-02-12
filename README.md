# T-game-app

# Quiz Game with Integrated Minigame

## Overview

This project is an interactive **Who Wants to Be a Millionaire?**-style quiz game built using **Pygame** and **Tkinter** for UI handling. The game features multiple-choice questions, lifelines, and scoring mechanisms. Additionally, a **minigame** has been integrated to enhance user engagement, serving as a challenge that influences the quiz progression.

## Features

### Quiz Game

- Multiple-choice questions
- Lifelines (50-50, audience poll, phone-a-friend)
- Scoring system with leaderboard
- Dynamic difficulty adjustments based on player performance
- Smooth UI transitions with Tkinter

### Minigame Integration

- Unlocks after a set number of quiz questions
- Difficulty scales based on quiz performance
- Power-ups and penalties based on quiz scores
- Standalone scoring system for the minigame
- Required for progression in certain quiz sections

## Project Structure

### **Quiz Game Directory**

```
$ ls
50-50.png          calling.mp3    Kbcwon.mp3      phone.png          Picture10.png  Picture15.png  Picture6.png  registration_codes.txt  user_accounts.json
50-50-X.png        center.png     lay.png         phoneAFriend.png   Picture11.png  Picture2.png   Picture7.png  requirements.txt        user_accounts.txt
app.py             game_pins.txt  leaderboard.db  phoneAFriendX.png  Picture12.png  Picture3.png   Picture8.png  sad.png                 users.db
audiencePole.png   happy.png      logo8.png       Picture0.png       Picture13.png  Picture4.png   Picture9.png  timerr.png              venv/
audiencePoleX.png  kbc.mp3        logo90.png      Picture1.png       Picture14.png  Picture5.png   README.md     ui_enhancements.py      vercel.json      
```

### **Minigame Directory**

```
$ ls
env/  images/  main.py  README.md  requirements.txt  scores.txt  file.py
```

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Pygame
- Tkinter
- Virtual environment setup (optional but recommended)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Martin4dbest/T-game-app
   ```

2. Navigate to the project directory:

   ```sh
   cd T-game-app
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the game:

   ```sh
   python app.py
   ```

## Integration Details

- The minigame is triggered at intervals during the quiz.
- Quiz scores dynamically adjust minigame difficulty.
- Minigame success or failure impacts quiz progression.
- Both games share a unified UI/UX for seamless transitions.

## Future Enhancements

- Implement a leaderboard for minigame scores
- Expand minigame options for variety
- Add more lifelines to the quiz for improved gameplay

## License

This project is open-source under the MIT License.

---



---

## **Project Structure**

```
quiz_game/
│── assets/                    # Store images, sounds, and other static assets
│   ├── images/                # Shared images for both quiz and minigame
│   ├── sounds/                # Sound effects and background music
│── database/                  # Store user-related data
│   ├── leaderboard.db         # SQLite database for leaderboard
│   ├── users.db               # SQLite database for user accounts
│   ├── registration_codes.txt
│   ├── user_accounts.json
│   ├── user_accounts.txt
│── game_logic/                # Core game logic and state management
│   ├── quiz_game.py           # The main quiz game logic
│   ├── minigame/              # Minigame folder (integrated)
│   │   ├── images/            # Minigame-specific images
│   │   ├── main.py            # Minigame logic (adapted from your minigame)
│   │   ├── file.py            # Minigame initialization script
│   │   ├── scores.txt         # Stores minigame scores dynamically
│   │   ├── __init__.py        # Makes it a package
│   ├── game_manager.py        # Handles transitions between quiz and minigame
│── ui/                        # UI enhancements and rendering logic
│   ├── ui_enhancements.py     # Handles UI/UX improvements
│── sounds/                    # Game sounds for effects
│── main.py                    # Entry point for running the game
│── requirements.txt           # Dependencies required to run the game
│── README.md                  # Documentation
│── vercel.json                # Deployment configuration
│── .gitignore                 # Ignore unnecessary files
│── venv/                      # Virtual environment for dependencies
│── env/                       # Minigame-specific virtual environment
```

---



🚀 **LETS GET STARTED**🎮
