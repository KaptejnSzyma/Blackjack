try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter
import random


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))
        # next the face cards
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image, ))


def deal_card(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)
    # and add it to back of the pack
    deck.append(next_card)
    # add the image to a Label and dispaly the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    # Calculate the total score of all cards in the list.
    # Only one ace can have the value 11, and this will reduce to 1 if the hand would bust.
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    global dealer_won
    global player_won
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins!")
        button_config()
        dealer_won += 1
        dealer_won_games.set(dealer_won)
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
        button_config()
        player_won += 1
        player_won_games.set(player_won)
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
        button_config()
        dealer_won += 1
        dealer_won_games.set(dealer_won)
    else:
        result_text.set("Draw!")


def deal_player():
    global dealer_won
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)

    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer wins!")
        button_config()
        dealer_won += 1
        dealer_won_games.set(dealer_won)


def button_config():
    player_button.config(state='disabled')
    dealer_button.config(state='disabled')
    new_game_button.config(state='active')


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    player_button.config(state='active')
    dealer_button.config(state='active')
    new_game_button.config(state='disabled')
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    # embedded frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    # Create the list to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []

    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def shuffle():
    random.shuffle(deck)


mainWindow = tkinter.Tk()

# Set up the screen and frames for the dealer nad player
mainWindow.title("Black Jack")
mainWindow.geometry("600x320")
mainWindow.configure(background='green')
mainWindow.resizable(False, False)
result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text, background='green', fg='white')
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)
# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New game", command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3)

won_games_frame = tkinter.Frame(mainWindow, background='green')
won_games_frame.grid(row=4, column=0, rowspan=2, sticky='w')
tkinter.Label(won_games_frame, text="Dealer's wins: ", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(won_games_frame, text="Player's wins: ", background='green', fg='white').grid(row=1, column=0)

dealer_won = 0
dealer_won_games = tkinter.IntVar()
tkinter.Label(won_games_frame, textvariable=dealer_won_games, background='green', fg='white').grid(row=0, column=1)

player_won = 0
player_won_games = tkinter.IntVar()
tkinter.Label(won_games_frame, textvariable=player_won_games, background='green', fg='white').grid(row=1, column=1)

# load cards
cards = []
load_images(cards)
# Create a new deck of cards and shuffle them

deck = list(cards)
shuffle()

# Create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

new_game()
mainWindow.mainloop()
