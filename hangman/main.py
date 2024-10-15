import random
import tkinter as tk
import ttkbootstrap as ttk
import time
import os
import sys

turns = 0
word = ''
hint = ''
guessed = []
topic = ''

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def begin_game():
    play_button.state(['disabled'])
    global word
    global guessed
    global topic
    global turns
    global hint
    turns = 6
    # getting a random list of words, and selecting a random word from that list
    topic = random.choice([
        'animal_hints',
        'people_hints',
        'random_hints',
        'scenes_hints',
        'simple_hints',
        'nature_simple',
        'nature_harder'])
    word_dict = {}
    
    # Use resource_path to load the dictionary file
    with open(resource_path(f'assets/{topic}.txt')) as file:
        for line in file:
            word, hint = line.split(':')
            word_dict[word] = hint
    word = random.choice(list(word_dict.keys()))
    hint = word_dict[word]
    guessed = ['_' for _ in word]
    word_dict.clear()
    topic, tmp = topic.split('_')
    create_buttons()
    update_display()

def create_buttons():
    for number in range(97,123):
        letter = chr(number)
        letter_button = ttk.Button(letter_button_frame, text=letter.upper(), padding=8)
        letter_button['command'] = lambda l=letter, button=letter_button: guess(l, button)
        letter_button.pack(side='left', ipadx=1, ipady=1)

def update_display():
    if turns >= 3:
        hint_label.config(text=f'Hint: {topic.upper()}')
    else:
        hint_label.config(text=f'Hint: {hint}')   
    update_gallows()
    turns_label.config(text=f'Turns: {turns}')
    word_label.config(text=' '.join(guessed))
    if '_' not in guessed:
        destroy_buttons()
        word_label.config(text=f'Winner!\nYour Word: {word.upper()}')
        play_button.state(['!disabled'])
    elif turns <= 0:
        destroy_buttons()
        word_label.config(text='You Lose!')
        play_button.state(['!disabled'])

def destroy_buttons():
    for widget in letter_button_frame.winfo_children():
        widget.destroy()

def guess(letter, button):
    button.state(['disabled'])
    global turns
    if letter in word:
        update_guessed(letter)
    else:
        turns -= 1
    if turns <= 0:
        turns = 0
    update_display()

def update_guessed(letter):
    for index, char in enumerate(word):
        if char == letter and index == 0:
            guessed[index] = letter.upper()
        elif char == letter:
            guessed[index] = letter

def update_gallows():
    # Use resource_path to load the gallows image
    image = tk.PhotoImage(file=resource_path(f'assets/gallows_{turns}.png'))
    gallows_label.config(image=image)
    gallows_label.image = image

# setup main window
root = ttk.Window(themename='darkly')
root_width = 800
root_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - root_width/2)
center_y = int(screen_height/2 - root_height/2)
root.geometry(f'{root_width}x{root_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.title('Hangman')
root.iconbitmap(resource_path('assets/hangman.ico'))  # Use resource_path for icon
icon_image = tk.PhotoImage(file=resource_path('assets/hangman.png'))  # Use resource_path for icon image

gallows_frame = ttk.Frame(root, borderwidth=5, relief='raised')
gallows_frame.place(relx=0.5, rely=0.3, anchor='center')
gallows_label = ttk.Label(gallows_frame, image=icon_image)
gallows_label.pack()

play_button = ttk.Button(root, text='Play', command=begin_game)
play_button.place(relx=0.5, rely=0.92, anchor='center')

turns_label = ttk.Label(root, text='', font=('Courier', 12))
turns_label.place(relx=0.5, rely=0.05, anchor='center')

hint_label = ttk.Label(root, text='', font=('Courier', 10))
hint_label.place(relx=0.5, rely=0.1, anchor='center')

word_label = ttk.Label(root, text=' '.join(guessed), font=('Courier', 30))
word_label.place(relx=0.5, rely=0.6, anchor='center')
word_label.config(text='Hangman!')

letter_button_frame = ttk.Frame(root, width=600, height=100)
letter_button_frame.place(relx=0.5, rely=0.8, anchor='center')

if __name__ == "__main__":
    root.mainloop()
