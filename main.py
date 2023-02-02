# --------------------------------- IMPORTS ----------------------------- #
from tkinter import *
import pandas
import random
from tkinter import messagebox


BACKGROUND_COLOR = "#B1DDC6"
font = "Arial"
current_card = {}
data_dict = {}
m = ""
timer = 5000
# --------------------------------- Random Words ----------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    pass
else:
    data_dict = data.to_dict(orient="records")


def next_card():
    global m
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(data_dict)
        french_word = current_card["French"]
        canvas_card.itemconfig(flash_title, text="French", fill="orange")
        canvas_card.itemconfig(flash_word, text=french_word, fill="black")
        canvas_card.itemconfig(card_background, image=card_front_img)
        flip_timer = window.after(timer, func=flip_card)
    except IndexError:
        m = messagebox.showinfo(title="AntonyCJA", message="You have completed all the words")
    else:
        if not m:
            window.mainloop()
        else:
            pass


# Flip Card
def flip_card():
    english_word = current_card["English"]
    canvas_card.itemconfig(flash_title, text="English", fill="Red")
    canvas_card.itemconfig(flash_word, text=english_word, fill="White")
    canvas_card.itemconfig(card_background, image=card_back_img)


def is_known():
    global m
    try:
        data_dict.remove(current_card)
        data_frame = pandas.DataFrame(data_dict)
        data_frame.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    except ValueError:
        m = messagebox.showinfo(title="AntonyCJA", message="You have completed all the words")


# --------------------------------- UI SETUP ----------------------------- #
window = Tk()
window.title("Flash Cards - AntonyCJA")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
# Canvas Card front
canvas_card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_background = canvas_card.create_image(400, 263, image=card_front_img)
flash_title = canvas_card.create_text(400, 150, text="Title", fill="orange", font=(font, 40, "italic"))
flash_word = canvas_card.create_text(400, 263, text="Word", fill="black", font=(font, 60, "bold"))
canvas_card.grid(row=0, column=0, columnspan=2)

# Canvas Card Back
card_back_img = PhotoImage(file="images/card_back.png")


# Buttons
check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

next_card()

if not m:
    window.mainloop()
else:
    pass
