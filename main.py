from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data_to_learn = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/italian_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data_to_learn.to_dict(orient="records")

# ---------------------------- GET NEXT CARD ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="Italiano", fill="black")
    canvas.itemconfig(word_text, text=current_card["Italiano"], fill="black")
    canvas.itemconfig(card_img, image=card_front)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_img, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")

# ---------------------------- REMOVE KNOWN CARD ------------------------------- #
def remove_card():
    to_learn.remove(current_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_img = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

known_button = Button(image=right_img, highlightthickness=0, command=remove_card)
unknown_button = Button(image=wrong_img, highlightthickness=0, command=next_card)

canvas.grid(column=0, row=0, columnspan=2)
known_button.grid(column=0, row=1)
unknown_button.grid(column=1, row=1)

next_card()

window.mainloop()
