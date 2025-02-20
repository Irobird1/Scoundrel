# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:22:59 2025

@author: sbwiz
SCOUNDREL
"""


import random


class Card:
    
    def __init__(self, val, suit):
        self.value = int(val)
        self.suit = suit
        self.attached = []
    
    # def give_value(self, val):
    #     self.value = val
        
    # def give_suit(self, suit):
    #     self.suit = suit
    
    def __str__(self):
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
        self.attached.append(card)


class Deck:
    
    def __init__(self, main):
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
        output=""
        for card in self.cards:
            output += str(card)+", "
        return output[:len(output)-2]
    
    def shuffle(self):
        random.shuffle(self.cards)
        print("Shuffling...")
    

class Game:
    
    def __init__(self):
        self.deck = Deck(True)
        self.discard = Deck(False)
        self.equipment = Deck(False)
        self.health = 20
        self.played = Deck(False)
        self.can_run = 2
        self.turn()
        self.can_heal = True
        
    def deal(self):
        while len(self.played.cards) < 4 and len(self.deck.cards) > 0:
            self.can_heal = True
            self.played.cards.append(self.deck.cards.pop(0))
    
    def __str__(self):
        return "Cards remaining in Deck: "+str(len(self.deck.cards))+"          Health: "+str(self.health)+"\n\
           ..... "+str(self.played)+" .....\n\
             .......... "+str(self.equipment)+" .........."
    
    def translate(self, inp):
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
        self.played.shuffle()
        while len(self.played.cards) > 0:
            self.deck.cards.append(self.played.cards.pop(0))
        self.deal()
        print("Successfully Ran!")
    
    def heal(self, val):
        self.health += val
        if self.health > 20:
            self.health = 20
        self.can_heal = False
        print("Healed to "+str(self.health)+" health")
        
    def equip(self, equipped):
        if len(self.equipment.cards) > 0:
            self.discard.cards.append(self.equipment.cards.pop(0))
            print("Discarded "+str(self.discard.cards[-1]))
        self.equipment.cards.append(equipped)
        print("Equipped "+str(self.equipment.cards[0]))
        
    def shop(self):
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
        if len(self.equipment.cards) > 0:
            bare_handed = input("Fight bare handed? (y/n): ").lower()
            if bare_handed != "y":
                if len(self.equipment.cards[0].attached) > 0:
                    if self.equipment.cards[0].attached[-1].value > self.equipment.cards[0].value:
                        if mob.value > self.equipment.cards[0].value:
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
                    if mob.value > self.equipment.cards[0].value:
                        print("Took "+str(mob.value - self.equipment.cards[0].value)+" dmg!")
                        self.health -= (mob.value - self.equipment.cards[0].value)
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
        #PRETURN
        if len(self.played.cards) < 2:
            self.deal()
            if len(self.deck.cards) == 0:
                print("The final room.\nMay your fight be legendary and\nend\nin\ntriumph.")
        print(self)
        
        #RUN
        if self.can_run > 1 and len(self.played.cards) == 4:
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
        if str(Card(card_move[:-1],card_move[-1])) in str(self.played):
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
                        
                
                
        #ENDTURN
        self.can_run += 1
        self.gameover()
    
    def gameover(self):
        if self.health <= 0:
            print("Gameover!")
            print("Remaining Cards: "+str(len(self.deck.cards)+len(self.played.cards)))
        elif len(self.deck.cards)+len(self.played.cards) == 0:
            print("Victory!!!!!")
        else:
            self.turn()
        
        
        
        
    
    






def main ():
    new_game = Game()
    
    
if __name__ == "__main__":
    main()
    
            
        
        
        
        
        
        
        
        
        
        
        
        
        