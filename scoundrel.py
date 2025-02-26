# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:22:59 2025

@author: sbwiz
SCOUNDREL

view README for rules.
"""

#Import random for shuffling main deck
import random


class Card:
    
    def __init__(self, val, suit):
        '''
        initializes Card object.
        self.attached represents card objects attached to self.

        Parameters
        ----------
        val : int
            from 2-15, represents the value of the card.
            11 represents jack and so on.
        suit : string/char
            represents suit of the card, with J standing in for joker.

        Returns
        -------
        None.

        '''
        
        self.value = int(val)
        self.suit = suit
        self.attached = []
    
    # def give_value(self, val):
    #     self.value = val
        
    # def give_suit(self, suit):
    #     self.suit = suit
    
    def __str__(self):
        '''

        Returns
        -------
        output : string
            string representation of the card.

        '''
        output = ""
        if self.value <= 10:
            output = str(self.value)+self.suit
        elif self.value == 11:
            output = "J"+self.suit
        elif self.value == 12:
            output = "Q"+self.suit
        elif self.value == 13:
            output = "K"+self.suit
        elif self.value == 14:
            output = "A"+self.suit
        else:
            output = "Joker"
        if len(self.attached) > 0:
            output += " ("
            for card in self.attached:
                output += str(card)
            output += ")"
        return output
    
    def attach(self, card):
        '''

        Parameters
        ----------
        card : Card object
            attaches a card to self. In a similar vain to placing a 9H below 10C in Solitaire FE.

        Returns
        -------
        None.

        '''
        self.attached.append(card)


class Deck:
    
    def __init__(self, main):
        '''
        self.cards is the Python list of cards in self.

        Parameters
        ----------
        main : Boolean
            describes whether the deck is the main deck or not.
            acts as a flag for multiple properties.

        Returns
        -------
        None.

        '''
        self.cards = []
        Rsuits = ["♥","♦"]
        Bsuits = ["♠","♣"]
        if main:
            for x in Rsuits:
                for y in range(2,11):
                    self.cards.append(Card(y,x))
            for x in Bsuits:
                for y in range(2,15):
                    self.cards.append(Card(y,x))
            for x in range(2):
                self.cards.append(Card(15,"J"))
                self.shuffle()
    
    def __str__(self):
        '''
        
        Returns
        -------
        string
            returns string format of this object (list of cards).

        '''
        output=""
        for card in self.cards:
            output += str(card)+", "
        return output[:len(output)-2]
    
    def shuffle(self):
        '''
        shuffles the deck using random.shuffle
        '''
        random.shuffle(self.cards)
        print("Shuffling...")
    

class Game:
    
    def __init__(self):
        '''
        initializes Game object.
        self.deck is the Deck object used as the main deck.
        self.discard is the discard pile. Can be used to add achievements for sequences of moves.
        self.equipment is a Deck object containing at most one Card, the current equipped diamond card.
        self.health is an integer that ends the game if 0 is ever reached. Caps at 20.
        self.played is a Deck displaying the current room of at most 4 cards.
        self.can_run is an int that, when == 2, allows the ability for the player to reshuffle.
        self.can_heal = True by default. Allows player to use heart cards.

        Returns
        -------
        None.

        '''
        
        #playing decks
        self.deck = Deck(True)
        self.discard = Deck(False)
        self.equipment = Deck(False)
        self.played = Deck(False)
        self.side = Deck(False)
        
        #Game stats
        self.health = 20
        self.can_run = 2
        self.can_heal = True
        
        #Ability checks
        self.per_room = 3 #JH
        self.QHON = False #QH
        self.dmg_bonus = 0 #KH
        
        self.start_game()
        
    def deal(self):
        '''
        Deals at most 4 cards into the current room.

        Returns
        -------
        None.

        '''
        while len(self.played.cards) <= self.per_room and len(self.deck.cards) > 0:
            self.can_heal = True
            self.played.cards.append(self.deck.cards.pop(0))
        
    def start_game(self):
        
        #Heart abilities
        usr = input("Input which heart card you'd like to bring (J, Q, K, A)\nOr enter nothing to go without a heart.\n").lower()
        if usr == "j":
            self.per_room = 4
            print("J♥, The Adventurer:\nDiscover one additional card per room.")
        elif usr == "q":
            self.QHON = True
            print("Q♥, The Guardian:\nBlock a strong monster with no reprecussion other than your steel.")
            print("Breaks current equipment at the expense of blocking high power damage.")
        elif usr == "k":
            self.dmg_bonus = 2
            print("K♥, The Berserk:\nRunning was never an option for those with strength.")
            print("+2 damage bonus applies to all equipment, but ability to run is removed.")
        elif usr == "a":
            print("A♥, The Survivor:\nEnduring the path of the Ace is lonely, but for it,\nyou are granted the power of unlimited life.")
            print("The A♥ is added to the deck at the cost of jokers. Additionally, the A♥ can heal past 20.")
            lyst  = []
            for card in self.deck.cards:
                if card.value != 15:
                    lyst.append(card)
            lyst.append(Card(14, "♥"))
            self.deck.cards = lyst
            self.deck.shuffle()
        
        #Diamond abilities
        usr = input("Input which card you'd like to bring (J, Q, K, A)\nOr enter nothing to go without a soul.\n").lower()
        if usr == "j":
            print("J♦, The Cartographer:\nEscape a tough spot at will.\nReshuffle the deck.")
            self.side.cards.append(Card(11,"♦"))
        elif usr == "q":
            print("Q♦, The Blacksmith:\nResharpen your blade.\nClear all attached cards off an equipment.")
            self.side.cards.append(Card(12,"♦"))
        elif usr == "k":
            print("K♦, The Duelist:\nDestroy a foe with your overwhelming experience with the blade.")
            self.side.cards.append(Card(13,"♦"))
        elif usr == "a":
            print("A♦, The Dungeon Master:\nEnduring the path of the Ace is dangerous, but for it,\nyou are granted the power of unlimited power.")
            print("Equip the A♦ at any point, but healing is impossible while wielding its power.")
            self.side.cards.append(Card(14,"♦"))
                    
        
        self.turn()
    
    def __str__(self):
        '''
        

        Returns
        -------
        string
            formatted string representation of a current turn.

        '''
        return "Deck: "+str(len(self.deck.cards))+"                     Health: "+str(self.health)+"\n\
        ..... "+str(self.played)+" .....\n\
          .......... "+str(self.equipment)+" ..........\n"+\
             "Side Board: "+str(self.side)+""
    
    def translate(self, inp):
        '''
        Translates user input to be understood by the Card and Deck classes.
        More can be added to this function to accomodate for various inputs.

        Parameters
        ----------
        inp : string
            user inputted string.

        Returns
        -------
        out : string
            formatted string that can be understood by other classes.

        '''
        inp = inp.lower()
        out = ""
        if inp[0] == 'j' and inp[1] != 'o':
            out += "11"
        elif inp[0] == 'q':
            out += "12"
        elif inp[0] == 'k':
            out += "13"
        elif inp[0] == 'a':
            out += "14"
        elif inp[0] == 'j':
            out += "15"
        else:
            out += str(inp[:-1])
        if inp[-1] == "s":
            out += "♠"
        elif inp[-1] == "h":
            out += "♥"
        elif inp[-1] == "d":
            out += "♦"
        elif inp[-1] == "c":
            out += "♣"
        return out
    
    def run(self):
        '''
        If ables, allows player to reshuffle current room.

        Returns
        -------
        None.

        '''
        self.played.shuffle()
        while len(self.played.cards) > 0:
            self.deck.cards.append(self.played.cards.pop(0))
        self.deal()
        print("Successfully Ran!")
    
    def heal(self, val):
        '''
        increasese player health to at most 20.

        Parameters
        ----------
        val : int
            potential health to be added to self.health.

        Returns
        -------
        None.

        '''
        if not (str(self.equipment.cards[0]) == "A♦"):
            cur_val = val
            while cur_val > 0:
                if self.health < 20 or val == 14:
                    self.health += 1
                cur_val -= 1
            self.can_heal = False
            if val == 14:
                print("Invoked the power of the A♥! health restored.")
            print("Healed to "+str(self.health)+" health")
        else:
            print("A♦'s power blocks even the touch of healing. No health gained.")
        
    def equip(self, equipped):
        '''
        Adds a card to self.equipment and discards previous equipment Card if any.

        Parameters
        ----------
        equipped : card
            diamond card to be equipped.

        Returns
        -------
        None.

        '''
        if len(self.equipment.cards) > 0:
            self.discard.cards.append(self.equipment.cards.pop(0))
            print("Discarded "+str(self.discard.cards[-1]))
        self.equipment.cards.append(equipped)
        print("Equipped "+str(self.equipment.cards[0]))
        
    def shop(self):
        '''
        opens the shop if joker is used. series of if statements to account for various situations.
        Should be changed to switch statement potentially.

        Returns
        -------
        None.

        '''
        do_it = input("shoppp... yessss...?? (y/n): ").lower()
        if do_it == 'y':
            if len(self.equipment.cards) > 0:
                if len(self.equipment.cards[0].attached) > 0:
                    print("Seen some use... eh? Let's see how much 'at'll dock its worth...")
                    if self.equipment.cards[0].attached[-1].value >= int(str(self.equipment.cards[0])[:2].strip("♦")):
                        print("I see it hath slain a powerful beast. For your effort-- full price...")
                        self.heal(int(str(self.equipment.cards[0])[:2].strip("♦")))
                    else:
                        print("This blade is dull. Ya will receive its worth to I...")
                        self.heal(int(str(self.equipment.cards[0].attached[-1])[:-1]))
                else:
                    print("Good...")
                    self.heal(int(str(self.equipment.cards[0])[:2].strip("♦")))
                self.discard.cards.append(self.equipment.cards.pop(0))
            else:
                print("You've nothing for meeee...")
        else:
            print("'Tis shame.")
        print("Farewelll...")
        
    def fight(self, mob):
        '''
        Series of if else statements to represent flow of logic for interacting with a black suited card.

        Parameters
        ----------
        mob : Card
            the interacted black card.

        Returns
        -------
        None.

        '''
        if len(self.equipment.cards) > 0:
            bare_handed = input("Fight bare handed? (y/n): ").lower()
            if bare_handed != "y":
                if len(self.equipment.cards[0].attached) > 0:
                    if self.equipment.cards[0].attached[-1].value > self.equipment.cards[0].value + self.dmg_bonus:
                        if mob.value > self.equipment.cards[0].value + self.dmg_bonus:
                            print("Weapon broke!")
                            print("Took "+str(mob.value)+" dmg!")
                            self.discard.cards.append(self.equipment.cards.pop(0))
                            print("Discarded "+str(self.discard.cards[-1]))
                            
                            self.health -= mob.value
                        else:
                            self.equipment.cards[0].attached.append(Card(mob.value,mob.suit))
                            print("Successfully Slain!")
                    else:
                        if mob.value > self.equipment.cards[0].attached[-1].value:
                            print("Took "+str(mob.value)+" dmg!")
                            self.health -= mob.value
                        else:
                            self.equipment.cards[0].attached.append(Card(mob.value,mob.suit))
                            print("Successfully Slain!")
                else:
                    if mob.value > self.equipment.cards[0].value + self.dmg_bonus:
                        if self.QHON:
                            print("Q♥ defends! Your weapon breaks, but you are safe.")
                            self.discard.cards.append(self.equipment.cards.pop(0))
                        else:
                            print("Took "+str(mob.value - (self.equipment.cards[0].value + self.dmg_bonus))+" dmg!")
                            self.health -= (mob.value - (self.equipment.cards[0].value + self.dmg_bonus))
                            self.equipment.cards[0].attached.append(Card(mob.value,mob.suit))
                    else:
                        self.equipment.cards[0].attached.append(Card(mob.value,mob.suit))
                        print("Successfully Slain!")
            else:
                self.health -= mob.value
                print("Took "+str(mob.value)+" dmg!")
        else:
            self.health -= mob.value
            print("Took "+str(mob.value)+" dmg!")

        
    
    def turn(self):
        '''
        represents the flow of logic at the start of each turn. recurses using self.gameover()

        Returns
        -------
        None.

        '''
        #PRETURN
        if len(self.played.cards) < 2:
            self.deal()
            if len(self.deck.cards) == 0:
                print("The final room.\nMay your fight be legendary and\nend\nin\ntriumph.")
        print(self)
        
        #RUN
        if self.can_run > 1 and len(self.played.cards) == self.per_room + 1:
            run = input("Do you want to run? (y/n): ").lower()
            if run == 'y':
                self.run()
                self.can_run = 0
                print(self)
        
        
        #MOVE
        card_move = self.translate(input("Input move: "))
        if card_move == "15":
            self.shop()
            test_card = Card(15,"J")
            for i in range(len(self.played.cards)):
                if test_card.value == self.played.cards[i].value:
                    self.discard.cards.append(self.played.cards.pop(i))
                    break
        elif str(Card(card_move[:-1],card_move[-1])) in str(self.played):
            if card_move[-1] == "♥":
                if self.can_heal:
                    self.heal(int(card_move[:-1]))
                else:
                    print("You can not heal again in this room.")
            elif card_move[-1] == "♦":
                self.equip(Card(card_move[:-1],card_move[-1]))
            else:
                self.fight(Card(card_move[:-1],card_move[-1]))
                
            test_card = Card(card_move[:-1],card_move[-1])
            for i in range(len(self.played.cards)):
                if test_card.value == self.played.cards[i].value and test_card.suit == self.played.cards[i].suit:
                    self.discard.cards.append(self.played.cards.pop(i))
                    break
        elif str(Card(card_move[:-1],card_move[-1])) in str(self.side):
            if self.side.cards[0].value == 11:
                print("J♦'s exploration has come in handy...\nReshuffling dungeon.")
                for card in self.played.cards:
                    self.deck.cards.append(card)
                self.played.cards.clear()
                self.deck.shuffle()
            elif self.side.cards[0].value == 12:
                print("Q♦ hammers out the nicks of your blade...\nAll attached cards removed.")
                for card in self.equipment.cards[0].attached:
                    self.discard.cards.append(card)
                self.equipment.cards[0].attached.clear()
            elif self.side.cards[0].value == 13:
                print("K♦ summons its power!")
                while True:
                    usr = self.translate(input("Select a card to destroy (Note that Jokers cannot be defeated): "))
                    flag = False
                    for i, card in enumerate(self.played.cards):
                        if str(Card(usr[:-1],usr[-1])) == str(card):
                            print(str(card)+" obliterated!")
                            self.discard.cards.append(self.played.cards.pop(i))
                            flag = True
                            break
                    if flag:
                        break
                    print("Card not listed. Input in the same way you would ordinarily select a card.")
            elif self.side.cards[0].value == 14:
                print("Invoked the power of the A♦!")
                self.equip(self.side.cards[0])

            self.discard.cards.append(self.side.cards.pop(0))
                
                
        #ENDTURN
        self.can_run += 1
        self.gameover()
    
    def gameover(self):
        '''
        game ends if health drops to 0, or there are no cards left in the deck.

        Returns
        -------
        None.

        '''
        if self.health <= 0:
            print("Gameover!")
            print("Remaining Cards: "+str(len(self.deck.cards)+len(self.played.cards)))
            usr = input("Play again? (y/n): ")
            if usr == "y":
                #playing decks
                self.deck = Deck(True)
                self.discard = Deck(False)
                self.equipment = Deck(False)
                self.played = Deck(False)
                self.side = Deck(False)
                
                #Game stats
                self.health = 20
                self.can_run = 2
                self.can_heal = True
                
                #Ability checks
                self.per_room = 3 #JH
                self.QHON = False #QH
                self.dmg_bonus = 0 #KH
                
                self.start_game()
        elif len(self.deck.cards)+len(self.played.cards) == 0:
            print("Victory!!!!!")
        else:
            self.turn()
        
        
        
        
    
    






def main ():
    new_game = Game()
    
    
if __name__ == "__main__":
    main()
    
            
        
        
        
        
        
        
        
        
        
        
        
        
        