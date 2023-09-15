from tkinter import *

import pandas
import pandas as pd
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# -----------------Flashcard------------------

try:
    df_flash_cards = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/DE_to_EN - Top 100 words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = df_flash_cards.to_dict(orient='records')


def pick_new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="German", fill='black')
    canvas.itemconfig(word_text,text=current_card['DE'],fill='black')
    canvas.itemconfig(flash_card, image=card_front_img)
    flip_timer = window.after(3000,flip_card)

def flip_card():
    canvas.itemconfig(flash_card, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill='white')
    canvas.itemconfig(word_text,text=current_card['EN'], fill='white')

def memorized():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index = False)
    pick_new_word()

# -----------------UI------------------


# Window and canvas
window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000,flip_card)

# Card canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_back_img = PhotoImage(file="./images/card_back.png")
card_front_img = PhotoImage(file="./images/card_front.png")
flash_card = canvas.create_image(400, 268, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

# Text
title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))


# Buttons
check_button_img = PhotoImage(file="./images/right.png")
check_button = Button(image=check_button_img, highlightthickness=0,command= lambda:[memorized()])
check_button.grid(row=1, column=0)

unsure_button_img = PhotoImage(file="./images/wrong.png")
unsure_button = Button(image=unsure_button_img, highlightthickness=0,command= lambda:[pick_new_word()])
unsure_button.grid(row=1, column=1)

pick_new_word()

window.mainloop()
