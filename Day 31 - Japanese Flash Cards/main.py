from tkinter import *
import random 
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"
to_learn = {}
current_card = {}
#------------------------------GET WORD FUNCTION --------------------------#

#Try to use the "words_to_learn" file to see what words still need learning
try:
    data = pandas.read_csv("data\words_to_learn.csv")
#If first time running, this will error, so catch error and create the words_to_learn file from the original japanese words list
except FileNotFoundError:
    original_data = pandas.read_csv("data\Japanese Words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



def next_card():
    '''Change the current flash card to a new one'''
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_image, image=front_of_card_image)
    #Randomly choose a new word
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")
    canvas.itemconfig(card_image, image=front_of_card_image)
    canvas.update_idletasks()  # Update the canvas to reflect changes
    #Give the user 4 seconds to say the translated word, before revealing
    flip_timer = window.after(4000,func=flip_card)



def flip_card():
    '''Reveal the english translated word on the back of the flash card'''
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_image, image=back_of_card_image)
    
    
def is_known():
    '''Remove known words from the to learn list so the user does not need to revist them'''
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data\words_to_learn.csv", index=False)


    next_card()
#-----------------------------------------UI--------------------------------#

#Create the window 
window = Tk()
window.title("Japanese Flash Cards")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

#4 Seconds timer
flip_timer = window.after(4000,func=flip_card)

# canvas for the card
canvas = Canvas(width=800, height=700, bg=BACKGROUND_COLOR, highlightthickness=0)
front_of_card_image = PhotoImage(file="images\card_front.png")
back_of_card_image = PhotoImage(file="images\card_back.png")
card_image = canvas.create_image(400, 400, image=front_of_card_image)
card_title = canvas.create_text(400, 250, text="", font=(FONT_NAME, 30, "italic"))
card_word = canvas.create_text(400, 450, text="", font=(FONT_NAME, 60, "bold"))
canvas.grid(column=2, row=0)

# X Button
x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=next_card)
x_button.grid(column=1, row=1)

# Tick Button
tick_image = PhotoImage(file="images/right.png")
tick_button = Button(image=tick_image, highlightthickness=0, command=is_known)
tick_button.grid(column=3, row=1)

next_card()

window.mainloop()