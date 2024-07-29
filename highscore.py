import os
import hashlib

HIGHSCORE_FILE = "highscore.txt"
SECRET_KEY = "secretKey"


def hash_score(score):
    return hashlib.sha256(f"{score}{SECRET_KEY}".encode()).hexdigest()


def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as file:
            try:
                lines = file.readlines()
                score = int(lines[0].strip())
                score_hash = lines[1].strip()
                if score_hash == hash_score(score):
                    return score
                else:
                    print("High score file tampered!")
                    return 0
            except (ValueError, IndexError):
                return 0
    return 0


def save_highscore(score):
    score_hash = hash_score(score)
    with open(HIGHSCORE_FILE, 'w') as file:
        file.write(f"{score}\n{score_hash}")

# Old highscore.py file in case you want to manipulate the highscore.txt - the main.py remain unchanged for both
# situations.

# HIGHSCORE_FILE = "highscore.txt"

# def load_highscore():
#    if os.path.exists(HIGHSCORE_FILE):
#        with open(HIGHSCORE_FILE, 'r') as file:
#            try:
#                return int(file.read())
#            except ValueError:
#                return 0
#    return 0

# def save_highscore(score):
#    with open(HIGHSCORE_FILE, 'w') as file:
#        file.write(str(score))
