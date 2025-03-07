# Scoundrel
This is a recreation of the rogue-like card game "Scoundrel" with some modification. To be played, simply run the .py file. Rules video here: https://www.youtube.com/watch?v=G8a3bzClt7w

Rules:

-- overview --
The game uses a full deck of playing cards, with jokers, minus red cards over the value of 10 (including aces).
The objective of the game is to make it to the end of the deck without dropping from an initial 20 health to 0.

-- cards --
Spades/Clubs:
Black cards act as monsters. They will do the amount of damage listed on the card with Jacks dealing 11, Queens dealing 12, Kings dealing 13, and Aces dealing 14.
Damage dealt to the player is simply removed from their health.
Diamonds:
Diamond cards are weapons/equipment cards. They deal the amount of damage listed on the card. Only one equipment can be held at a time, and picking up a new equipment will remove the old one.
In a fight with a monster, using an equipment will attach the monster to the equipment card and deal (equipment value - monster value) damage to the player. Note that an enemy of higher value can only be attached to an equipment card with no previously attached monsters; otherwise, the weapon will break and be discarded. This is why sometimes opting to fight monsters bare-handed is a viable option.
Additionally, like Solitaire, an equipment can only attach cards in a descending manner. If a 5D defeats a 4C, it can then only be used to defeat monsters with a value of 4 or lower.
Hearts:
Hearts are the simplest cards and simply heal the player for the value listed on the card. Although, the player cannot heal past 20 health.
Also, the player can only heal once per room, and healing twice in the same room will result in the second card being wasted with no benefit.
Jokers:
Jokers act as shops where the player can choose to sell their current equipment to the discard pile if they so choose for health equal to value of the lowest valued card attached to the equipment.
For example, a 6D will sell for 6 health, but a 6D with an attached 5C will only sell for 5 heatlh. Note: a 6D with a QS attached will still only sell for 6 health for reference.

-- rooms --
At the start of a turn, if there is only one card left in a room, cards are dealt from the main deck to fill the room back to four cards.
A room of four cards may include any of the previously mentioned suits. The player may only interact with a single card in the room at a time.
Lastly, the player may choose to run from any given (full) room. If this happens, the cards of the room are moved to the bottom of the deck, and a new room is dealt. The player cannot run from two consecutive rooms, so running comes with inherent risk.

-- console --
The only interface for the game currently is the console. The only interactions will be the following: "6s" for 6 of spades as an example of a standard number card, "qc" as an example of a standard face card, "joker" for jokers, "y" for confirming a prompt, and "n" for rejecting a prompt.

-- abilities --
At the start of the game, the player receives the option to choose one heart face card, and one diamond face card. These act as abilities. Heart cards are passive abilities, whereas diamonds can be activated once during gameplay.
The abilities are the following:
> Jack of Hearts, reveal one additional card per room.
> Queen of Hearts, gain the ability to block strong enemies and take no damage, however equipment is broken in the process.
> King of Hearts, Deal two additional damage, but lose the ability to run.
> Ace of Hearts, The card is added to the deck as a 15 valued heal with the ability to go past 20 health, however the joker cards are removed.
> Jack of Diamonds, reshuffle the dungeon.
> Queen of Diamonds, Clear attached cards from current equipment.
> King of Diamonds, Destroy one card that has been played.
> Ace of Diamonds, equip the Ace of Diamonds equipment.

-- Future Updates --
I plan to add a GUI including a title page with player stats.
I plan to add achievements that unlock the ability cards naturally during play.
I plan to add a method to save the game.
I plan to add a method of looping a run (like many roguelikes)
I plan to add a rules page in the game.
I plan to clean the spaghetti code this game runs on.
