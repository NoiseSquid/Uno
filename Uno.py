#backup 2:
#AI will now only pick +2s and +4s if needed
#Discard pile starting card is now random

#***Can no longer play any card after a wildcard
# NOTES: card validation is proper fucked

from random import randint


class Card:

    def __init__(self, number, colour):
        self.num = number
        self.col = colour


class Deck:

    def __init__(self):
        self.__card_list = []


    def addCard(self, card):

        self.__card_list.append(card)


    def drawCard(self):

        return_card = self.__card_list[len(self.__card_list) - 1]
        del self.__card_list[len(self.__card_list) - 1]
        return return_card


    def shuffle(self):

        deck_size = len(self.__card_list)
        deck_order = []
        deck_shuffled = []
        
        for i in range(deck_size):
            while True: # do while statement
                number = randint(0, deck_size - 1)
                if number not in deck_order:
                    deck_order.append(number)
                    break

        for index in deck_order:
            deck_shuffled.append(self.__card_list[index])

        self.__card_list = deck_shuffled


class Player:

    def __init__(self, name, ai):
        self.name = name
        self.__ai = ai
        self.__card_list = []


    def isAi(self):

        return self.__ai


    def giveCard(self, card):

        self.__card_list.append(card)


    def removeCard(self, card):

        for cnum in range(len(self.__card_list)):

            cur_card = self.__card_list[cnum]

            if ((cur_card.num == card.num)
            and (cur_card.col == card.col)):
                del self.__card_list[cnum]
                return


    def showHand(self):

        print(" --- HAND --- ")
        
        for cnum in range(len(self.__card_list)):

            cur_card = self.__card_list[cnum]
            display = ""

            display += cur_card.col
            display += " "
            display += cur_card.num
            
            print("%i. %s" % (cnum + 1, display))


    def selectCard(self, TopCard, must_match_num):

        print(" --- %s'S TURN --- " % (self.name.upper()))

        if not self.__ai:

            print("Discard pile: %s %s" % (TopCard.col, TopCard.num))

            print()
            self.showHand()

            card_num = -1
            while card_num < 0 or card_num >= len(self.__card_list):

                card_num = input("select card: ")

                try:
                    card_num = int(card_num) - 1
                    card = self.__card_list[card_num]

                    if (must_match_num) and card.num != TopCard.num:
                        print("ERROR: card numbers must match")
                        card_num = -1
                    
                except ValueError:
                    print("ERROR: you need to enter a number")
                    card_num = -1
                    
                except IndexError:
                    print("ERROR: the number is too big or too small")
                    card_num = -1

            return self.__card_list[card_num]

        else:

            print("Discard pile: %s %s" % (TopCard.col, TopCard.num))
            print("they have %i cards" % (len(self.__card_list)))

            card_num = randint(0, len(self.__card_list) - 1)
            card = self.__card_list[card_num]

            if not must_match_num:
                while ((card.num != TopCard.num)
                and (card.col != TopCard.col)
                and (card.num != "")
                and (TopCard.num != "")):
                    card_num = randint(0, len(self.__card_list) - 1)
                    card = self.__card_list[card_num]

            else:
                while ((card.num != TopCard.num)):
                    card_num = randint(0, len(self.__card_list) - 1)
                    card = self.__card_list[card_num]

            print("%s has played %s %s" % (self.name,
                                           self.__card_list[card_num].col,
                                           self.__card_list[card_num].num))

            return self.__card_list[card_num]


    def hasWon(self):

        if len(self.__card_list) == 0:
            return True
        else:
            return False


    def hasCard(self, card):

        for cnum in range(len(self.__card_list)):

            cur_card = self.__card_list[cnum]

            if ((card.num in ["", cur_card.num])
            and (card.col in ["", cur_card.col])):
                return True

        return False


    def chooseColour(self):

        if not self.__ai:

            colour = input("Select colour: ").lower()
            while colour not in ["red", "green", "blue", "yellow"]:
                print("invalid colour!")
                print()
                colour = input("Select colour: ").lower()

            return colour

        else:

            col_freq = [0, 0, 0, 0]#red green blue yellow

            for card in self.__card_list:

                if card.col == "red":
                    col_freq[0] += 1
                    continue

                if card.col == "green":
                    col_freq[1] += 1
                    continue

                if card.col == "blue":
                    col_freq[2] += 1
                    continue

                if card.col == "yellow":
                    col_freq[3] += 1
                    continue

            highest_freq = 0
            for freq in col_freq:
                if freq > highest_freq:
                    highest_freq = freq

            possible_choices = []

            if col_freq[0] == highest_freq:
                possible_choices.append("red")

            if col_freq[1] == highest_freq:
                possible_choices.append("green")

            if col_freq[2] == highest_freq:
                possible_choices.append("blue")

            if col_freq[3] == highest_freq:
                possible_choices.append("yellow")

            choice = possible_choices[randint(0, len(possible_choices) - 1)]

            print("%s has changed the colour to %s" % (self.name, choice))
            return choice


    def canPlayACard(self, top_card):

        for cnum in range(len(self.__card_list)):

            cur_card = self.__card_list[cnum]

            if ((cur_card.num == top_card.num)
            or (cur_card.col == top_card.col)
            or (cur_card.num == "")
            or (top_card.num == "")):
                return True

        return False


    def sayUno(self):

        if len(self.__card_list) == 1:
            print("%s says UNO!" % (self.name))


    def numOfCards(self):

        return len(self.__card_list)
            



class PlayerList:

    def __init__(self, num_players, num_ais):
        
        self.__num_pls = num_players
        self.__players = []
        self.__order = "clockwise"
        self.__cur_player = 0

        for i in range(num_players):

            is_ai = (i < num_ais)

            if is_ai:
                name = "Player " + str(i + 1)
            else:
                name = input("Enter your name: ")
            
            NewPlayer = Player(name, is_ai)
            self.__players.append(NewPlayer)


    def numPlayers(self):

        return len(self.__players)


    def changeOrder(self):

        if self.__order == "clockwise":
            self.__order = "anti-clockwise"
        else:
            self.__order = "clockwise"


    def advance(self):

        if self.__order == "clockwise":

            self.__cur_player += 1
            if self.__cur_player >= len(self.__players):
                self.__cur_player -= len(self.__players)

        if self.__order == "anti-clockwise":

            self.__cur_player -= 1
            if self.__cur_player < 0:
                self.__cur_player += len(self.__players)


    def giveCard(self, card):

        self.__players[self.__cur_player].giveCard(card)


    def removeCard(self, card):

        self.__players[self.__cur_player].removeCard(card)


    def selectCard(self, TopCard, must_match_num):

        return self.__players[self.__cur_player].selectCard(TopCard, must_match_num)


    def getWinner(self):

        for player in self.__players:

            if player.hasWon():
                return player

        return None


    def hasCard(self, card):

        return self.__players[self.__cur_player].hasCard(card)


    def chooseColour(self):

        return self.__players[self.__cur_player].chooseColour()


    def canPlayACard(self, top_card):

        return self.__players[self.__cur_player].canPlayACard(top_card)
        

    def name(self):

        return self.__players[self.__cur_player].name


    def sayUno(self):

        return self.__players[self.__cur_player].sayUno()


    def numOfCards(self):

        return self.__players[self.__cur_player].numOfCards()



class DeckCreator:

    def __init__(self):
        pass


    def createADeck(self):

        NewDeck = Deck()
        all_nums = ["1", "2", "3", "4", "5",
                    "6", "7", "8", "9",
                    "+2", "reverse", "skip"]
        all_cols = ["red", "green", "blue", "yellow"]
        num_of_plus4s = 4
        num_of_wildcards = 4

        for num in all_nums:
            for col in all_cols:

                for count in range(2):
                    NewCard = Card(num, col)
                    NewDeck.addCard(NewCard)

        for col in all_cols:

            NewCard = Card("0", col)
            NewDeck.addCard(NewCard)

        for i in range(num_of_plus4s):
            
            NewCard = Card("+4", "")
            NewDeck.addCard(NewCard)

        for i in range(num_of_wildcards):

            NewCard = Card("", "wildcard")
            NewDeck.addCard(NewCard)

        NewDeck.shuffle()

        return NewDeck


class DiscPile:

    def __init__(self):
        self.__disc_pile = []
        self.__cur_num = ""
        self.__cur_col = ""


    def addCard(self, card):

        self.__disc_pile.append(card)
        self.__cur_num = card.num
        self.__cur_col = card.col


    def setCurNum(self, num):

        self.__cur_num = num


    def setCurCol(self, col):

        self.__cur_col = col


    def top(self):

        return Card(self.__cur_num, self.__cur_col)


    def showTop(self):

        print("Discard pile: %s %s" % (self.__cur_col, self.__cur_num))

        


def DebugTestPlayerHands():

    NewPlayer = Player("Matt")

    CardList = []
    CardList.append(Card("2", "red"))
    CardList.append(Card("+4", ""))
    CardList.append(Card("", "wildcard"))
    CardList.append(Card("+2", "blue"))

    for EachCard in CardList:
        NewPlayer.giveCard(EachCard)

    NewPlayer.selectCard()



class GameManager():

    def __init__(self):

        self.TheDeck = None
        self.DPile = DiscPile()
        self.Players = None

        self.accum_plus2s = 0
        self.accum_plus4s = 0
        self.already_drawn = False


    def setUpGame(self, num_ais):

        #create the draw deck
        dc = DeckCreator()
        self.TheDeck = dc.createADeck()

        #create the players
        self.Players = PlayerList(num_ais + 1, num_ais)

        #give 7 cards to each player
        for p in range(self.Players.numPlayers()):

            for c in range(7):
                TopCard = self.TheDeck.drawCard()
                self.Players.giveCard(TopCard)

            self.Players.advance()

        #put a card on the discard pile
        TopCard = self.TheDeck.drawCard()
        self.DPile.addCard(TopCard)


    def playGame(self):

        #while all players have cards
        while (self.Players.getWinner() == None):

            self.already_drawn = False

            if self.pickUp2Turn():
                input("End of turn")
                print()
                continue
            
            if self.pickUp4Turn():
                input("End of turn")
                print()
                continue
            
            if self.drawExtraCard():
                input("End of turn")
                print()
                continue

            self.selectCard()

            self.Players.advance()
            input("End of turn")
            print()

        print()
        self.displayWinner()


    def pickUp2Turn(self):

        #if accumulated pick-up 2 greater than 0
        if self.accum_plus2s > 0:
    
            #if player has a pick-up-2 ask player to select a card
            if self.Players.hasCard(Card("+2", "")):
                SelectedCard = Card("", "")

                #if card not puck-up-2 ask again
                while SelectedCard.num != "+2":
                    SelectedCard = self.Players.selectCard(self.DPile.top(), True)
                self.Players.removeCard(SelectedCard)
                self.Players.sayUno()
                self.Players.advance()
                self.accum_plus2s += 1

                return True #end turn
                
            #otherwise give player corrisponding number of cards
            else:
                print("%s was forced to draw %i cards" % (self.Players.name(), self.accum_plus2s * 2))
                for i in range(self.accum_plus2s * 2):
                    TopCard = self.TheDeck.drawCard()
                    self.Players.giveCard(TopCard)
                self.accum_plus2s = 0
                self.already_drawn = True


    def pickUp4Turn(self):

        #if accumulated pick-up-4 greater than 0
        #same as pick-up-2 essentially
        if self.accum_plus4s > 0:
    
            #if player has a pick-up-2 ask player to select a card
            if self.Players.hasCard(Card("+4", "")):
                SelectedCard = Card("", "")

                #if card not puck-up-2 ask again
                while SelectedCard.num != "+4":
                    SelectedCard = self.Players.selectCard(self.DPile.top(), True)
                self.Players.removeCard(SelectedCard)
                self.Players.sayUno()

                new_colour = self.Players.chooseColour()
                self.DPile.setCurCol(new_colour)

                self.accum_plus4s += 1
                self.Players.advance()

                return True #end turn
                
            #otherwise give player corrisponding number of cards
            else:
                print("%s was forced to draw %i cards" % (self.Players.name(), self.accum_plus4s * 4))
                for i in range(self.accum_plus4s * 4):
                    TopCard = self.TheDeck.drawCard()
                    self.Players.giveCard(TopCard)
                self.accum_plus4s = 0
                self.already_drawn = True


    def drawExtraCard(self):

        #check if player can't play any cards
        if not self.Players.canPlayACard(self.DPile.top()):

            if not self.already_drawn:
                print("%s can't play any cards, so must draw 1" % (self.Players.name()))
                TopCard = self.TheDeck.drawCard()
                self.Players.giveCard(TopCard)
        
            if not self.Players.canPlayACard(self.DPile.top()):

                print("%s still can't play any cards" % (self.Players.name()))

                self.Players.advance()
                return True #end turn


    def validCard(self, SelectedCard):

        TopCard = self.DPile.top()
        
        if (TopCard.num == SelectedCard.num):
            return True

        if (TopCard.col == SelectedCard.col):
            return True

        if (TopCard.num == ""):
            return True

        if (TopCard.col == ""):
            return True

        if (SelectedCard.num == ""):
            return True

        if (SelectedCard.num == ""):
            return True

        return False


    def selectCard(self):

        #ask player to select a card
        SelectedCard = self.Players.selectCard(self.DPile.top(), False)
        while not self.validCard(SelectedCard):
            print("selected card is invalid")
            print()
            SelectedCard = self.Players.selectCard(self.DPile.top(), False)

        #if card is playable, put on discard pile
        self.Players.removeCard(SelectedCard)
        self.Players.sayUno()
        self.DPile.addCard(SelectedCard)

        #additional card actions:
        
        if SelectedCard.num == "+2":
            self.accum_plus2s += 1

        if SelectedCard.num == "+4":
            self.accum_plus4s += 1
            new_colour = self.Players.chooseColour()
            self.DPile.setCurCol(new_colour)
        
        #if card was reverse order, switch play order
        if SelectedCard.num == "reverse":
            self.Players.changeOrder()


        if SelectedCard.num == "skip":
            self.Players.advance()
        
        #if card was a wildcard, ask for new colour
        if SelectedCard.col == "wildcard":
            new_col = self.Players.chooseColour()
            self.DPile.setCurCol(new_col)


    def displayWinner(self):

        Winner = self.Players.getWinner()
        print("%s has won!" % (Winner.name))
        print()
        for p in range(self.Players.numPlayers()):
            print("%s had %i cards" % (self.Players.name(),
                                       self.Players.numOfCards()))
            
            self.Players.advance()

        



if __name__ == "__main__":

    
        gm = GameManager()
        gm.setUpGame(3)

        gm.playGame()
        

    




