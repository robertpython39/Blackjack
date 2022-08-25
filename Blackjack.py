# -------------------------------------------------------------------------------
# Name:        Blackjack
# Purpose:     Fun/Games
#
# Author:      rnicolescu
#
# Created:     25/08/2022
# Copyright:   (c) rnicolescu 2022
# Licence:     <your license here>
# ------------------------------------------------------------------------------
import random, sys


class Blackjack:
    # Constants
    HEARTS =   chr(9829) # Character 9829 is '♥'.
    DIAMONDS = chr(9830) # Character 9830 is '♦'.
    SPADES =   chr(9824) # Character 9824 is '♠'.
    CLUBS =    chr(9827) # Character 9827 is '♣'.
    MONEY =    5000
    BACKSIDE = 'backside'


    def __init__(self):
        pass

    def getBet(self, maxBet):
        # Here we ask the player how much he want to bet
        # Check if he enter a valid bet
        # If player wants to quit, sys.exit()
        # Check if the bet is decimal or not

        game_is_on = True
        while game_is_on:
            print(f'How much you want to bet? (1 - {maxBet}, 2 - QUIT')
            bet = input('> ')
            if bet == '2' or bet == 'QUIT'.upper():
                print('Have a nice day!')
                sys.exit()

            if not bet.isdecimal():
                continue

            if bet:
                bet = int(bet)
                if 1 <= bet <= maxBet:
                    return bet

    def getDeck(self):
        """Return a  list of  (rank, suit) tuples for all 52  cards."""
        # Create an empty list fot the deck card
        # Loop in class variables and append them to the deck
        # Shuffle the deck
        # Return the deck
        deck = []
        for suit in (Blackjack.SPADES, Blackjack.CLUBS, Blackjack.DIAMONDS, Blackjack.HEARTS):
            for rank in range(2, 11):
                deck.append((str(rank), suit))
            for rank in ('J', 'K', 'Q', 'A'):
                deck.append(((rank, suit)))

        random.shuffle(deck)
        return deck

    def displayHands(self, playerHand, dealerHand, showDealerHand):
        """Show the   player's and  dealer's cards. Hide  the   dealer's first
            card   if showDealerHand  is False."""
        # Show the dealers hand
        # Hide the dealers first card
        if showDealerHand:
            print('DEALER:', self.getHandsValue(dealerHand))
            self.displayCards(dealerHand)
        else:
            print('DEALER: ???')
            # Hiding dealer's first card
            self.displayCards([Blackjack.BACKSIDE] + dealerHand[1:])

    def getHandsValue(self, cards):
        """Returns the   value of  the   cards. Face  cards are   worth  10,   aces   are
        worth  11  or  1  (this  function picks the   most  suitable ace  value)."""
        # Create two variables (value, numberOfAces with 0 value)
        # Add the value for the non-ace cards
        # Add the value for the aces
        # Return the value
        value = 0
        numberOfAces = 0
        for card in cards:
            rank = card[0]
            if rank == "A":
                numberOfAces += 1
            elif rank in ('K', 'Q', 'J'):
                value += 10
            else:
                value += int(rank)
        value += numberOfAces
        for i in range(numberOfAces):
            if value + 10 < 21:
                value += 10

        return value

    def displayCards(self, cards):
        """Display all  the   cards in the   cards list."""
        rows = ["", "", "", "", ""]
        for i, card in enumerate(cards):
            rows[0] += '___  '
            # Check if card is BACKSIDE
            if card == Blackjack.BACKSIDE:
                rows[1] += '|## | '
                rows[2] += '|###| '
                rows[3] += '|_##| '

            else:
                # Print the cards front
                rank, suit = card
                rows[1] += '|{} | '.format(rank.ljust(2))
                rows[2] += '| {} | '.format(suit)
                rows[3] += '|_{}|  '.format(rank.rjust(2, '_'))

        # Print each row on the screen:
        for row in rows:
            print(row)

    def getMove(self, playerHand, money):
        """Asks   the   player for their  move,  and  returns 'H' for hit,  'S'  for
        stand, and  'D' for double   down."""
        # Keep looping until the player enters a correct move
            # Determine what moves the player can make
        while True:
            moves = ['(H)it', '(S)tand']
        #  The player can  double   down on  their first move,  which  we can tell because they'll have  exactly two  cards"
            if len(playerHand) == 2 and Blackjack.MONEY > 0:
                moves.append('(D)ouble down')
            # Get the players move
            movePromp = ', '.join(moves) + '> '
            move = input(movePromp).upper()
            if move in ('H', 'S'):
                return move
            if move == 'D':
                return move


    def main(self):
        # call all the money
        Blackjack.MONEY
        while True:
            if Blackjack.MONEY <= 0:
                print('You are broke')
                print("Good thing you weren't playing with real money")
                print('Thanks for playing')
                sys.exit()
            # Leting the player enter his bet for this round
            print('Money: {}'.format(Blackjack.MONEY))
            bet = self.getBet(Blackjack.MONEY)

            # Give the dealer and player two cards from the deck each
            deck = self.getDeck()
            dealerHand = [deck.pop(), deck.pop()]
            playerHand = [deck.pop(), deck.pop()]

            # Handle player actions
            print('BET: {}'.format(bet))
            # Keep looping until player stands or busts
            while True:
                self.displayHands(playerHand, dealerHand, False)
                print()
                if self.getHandsValue(playerHand) > 21:
                    break # we exit the loop
                move = self.getMove(playerHand, Blackjack.MONEY - bet)
                # Get the players move( H, S or D)
                if move == 'D':
                    additionalBet= self.getBet(min(bet, (Blackjack.MONEY - bet)))
                    bet += additionalBet
                    print('Bet increased to {}'.format(bet))
                    print('Bet: ', bet)

                if move in ('H', 'D'):
                    # Hit/doubling down takes another card
                    newCard = deck.pop()
                    rank, suit = newCard
                    print('You drew a {} of {}.'.format(rank, suit))
                    playerHand.append(newCard)

                if move in ('S', 'D'):
                    break

            # Handle the dealer's actions
            if self.getHandsValue(playerHand) <= 21:
                while self.getHandsValue(dealerHand) < 17:
                    print('The dealer hits:')
                    dealerHand.append(deck.pop())
                    self.displayHands(playerHand, dealerHand, False)
                    if self.getHandsValue(playerHand) > 21:
                        break
                    input('Press ENTER to continue...')
                    print('\n\n')
            # Showing the final hands
            self.displayHands(playerHand, dealerHand, True)

            playerValue = self.getHandsValue(playerHand)
            dealerValue = self.getHandsValue(dealerHand)

            # Check if the dealer wins or not
            if dealerValue > 21:
                print('You won ${}'.format(bet))
                Blackjack.MONEY += bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print('You lost!')
                Blackjack.MONEY -= bet
            elif playerValue > dealerValue:
                print('You won ${} '.format(bet))
                Blackjack.MONEY += bet
            elif playerHand == dealerHand:
                print("It's a tie. The bet is returned to you")
            input('Pres ENTER to continue')
            print('\n\n')


if __name__ == "__main__":

    bjck = Blackjack()
    bjck.main()
