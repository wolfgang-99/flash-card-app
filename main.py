from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words to learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(cards_background, image=card_back_img)


def is_know():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words to learn.csv", index=False)
    next_card()

# ---------------- next word --------------------------
def next_card():
    global current_card, flip_timer
    current_card = random.choice(to_learn)
    window.after_cancel(flip_timer)

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(cards_background, image=card_front_img)
    window.after(3000, flip_card)

# -------------------- UI Setup ----------------------------------------------
window = Tk()
window.title("Flash app")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
cards_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

check_img = PhotoImage(file="images/right.png")
right_button = Button(image=check_img, highlightthickness=0, command=is_know)
right_button.grid(row=1, column=1)

next_card()


window.mainloop()
