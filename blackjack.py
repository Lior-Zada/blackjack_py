import random


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.value = 0
        self.cards = []
        self.aces = 0

    def add_card(self, card):
        # card passed in
        # from Deck.deal()
        self.cards.append(card)
        self.value += values[card.rank]
        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How much would you like to bet?"))
        except:
            print("How much would you like to bet? please enter a number.")
        else:
            if chips.bet > chips.total:
                print("Sorry, you don't have enough chips, you have {}".format(
                    chips.total))
            else:
                break


def take_hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input('Hit or Stand? type h or s\n')
        if x[0].lower() == 'h':
            take_hit(deck, hand)
            break
        elif x[0].lower() == 's':
            print('Player stands. Dealers turn.')
            playing = False
            break
        else:
            print("Sorry, i didn't understand. Please type h or s")
            continue


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print(dealer.cards[0])
    print("\nPlayer's Hand:")
    print(*player.cards, sep = "\n") 


def show_all(player, dealer):
    print("\nDealer's Hand:",)
    print( *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:")
    print( *player.cards, sep='\n ')
    print("Player's Hand =",player.value)


def player_busts(player, dealer, chips):
    print('Player Busts! you lose {} chips!'.format(chips.bet))
    chips.lose_bet()


def dealer_busts(player, dealer, chips):
    print('Dealer Busts! you win {} chips!'.format(chips.bet))
    chips.win_bet()


def player_wins(player, dealer, chips):
    print('Player Wins! you win {} chips!'.format(chips.bet))
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('Dealer Wins! you lose {} chips!'.format(chips.bet))
    chips.lose_bet()


def push(player, dealer):
    print('Player and dealer tie! PUSH')


while True:
    # Print welcome statement!
    print('Welcome to blackjack!')
    # Create and shuffle the deck, deal two cards to each player.
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealder_hand = Hand()
    dealder_hand.add_card(deck.deal())
    dealder_hand.add_card(deck.deal())

    # Set up players chips
    player_chips = Chips()

    # Prompt player for their bet
    take_bet(player_chips)

    # Show cards, keep one dealer card hidden
    show_some(player_hand, dealder_hand)

    while playing:
        # promt player to hit or stand
        hit_or_stand(deck, player_hand)
        # Show cards, keep one dealer card hidden
        show_some(player_hand, dealder_hand)

        # if Player's hand exceeds 21, player busts
        if player_hand.value > 21:
            player_busts(player_hand, dealder_hand, player_chips)

            break
    # if player hasn't busted, dealer play until dealers hand is bigger than player's hand
    if player_hand.value <= 21:
        while dealder_hand.value < player_hand.value:
            dealder_hand.add_card(deck.deal())

        # show all cards
        show_all(player_hand, dealder_hand)

        # run different wining scenarios
        if dealder_hand.value > 21:
            dealer_busts(player_hand, dealder_hand, player_chips)
        elif dealder_hand.value > player_hand.value:
            dealer_wins(player_hand, dealder_hand, player_chips)
        elif dealder_hand.value > player_hand.value:
            player_wins(player_hand, dealder_hand, player_chips)
        else:
            push(player_hand, dealder_hand)

    # inform player how many chips he has.
    print("\n Player total chips: {}".format(player_chips.total))

    # ask player if want to play another game
    new_game = input('Would you like to play another hand? type y or n')

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing! Goodbye!')
        break
