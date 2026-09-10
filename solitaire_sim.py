from functools import total_ordering
import random # This is what produces the controlled random card arrangments for Solitaire.
import statistics # Calculates the averages and medians for the data from the simulation.
from dataclasses import dataclass # Automatically creates config classes for the rulesets
CHECKPOINTS = (4, 8, 12, 13) # The intervals of cards in a foundation where a player may bank cards.

SUIT_NAMES = ("Clubs", "Diamonds", "Hearts", "Spades",)

MAX_FOUNDATIONS = 4 

BANK_INTERVAL = 4

FULL_FOUNDATION_SIZE = 13

FULL_FOUNDATION_REWARD = 10

PROGRESSIVE_REWARDS = { #The progressive scoring for each interval of cards banked
    1: 1,  # 1 is 1
    2: 3,  # 2 is 3 
    3: 6,  # 3 is 6
    4: 8, # 4 Intervals Banked is 8 pts
}
@dataclass
class settings:
    simulations: int = 1000 # The amount of games in one simulation

    minimum_points: int = 12 # The minimum score to win.

    progressive_intervals: bool = True # this should enable the reward progression of the intervals
        
    deadwood_enabled: bool = True # Subtracts the unbanked foundations against the banked oens

    tableau_deadwood_enabled: bool = False #When set to true, cards in tableau will count for deadwood.

    banking_strategy: str = "balanced" # Determines how frequently the simulated player will bank foundations.

    time_limit_minutes: float = 15.0 # Real time limit represented in the simulation

    seconds_per_action: float = 3.0 # Estimated time required for one player action

    random_seed: int = 37000 # this should allow the experiment to be reproduced
    @property
    def action_budget(self) -> int:
        total_ordering = self.time_limit_minutes * 60 # Convert the selected minutes into seconds

        estimated_actions = total_seconds / self.seconds_per_action_per_action # divide the available time by action

        return int(estimated_actions) # Return a whole number of actions.
 @dataclass
    class GameResult:
        banked_points: int #These are the points secured through banking.

        deadwood: int # These keep track of the unbanked foundations.

        final_score: int # banked points minus applicable deadwood.

        won: bool # True when final score reaches the minimum.

        actions_used: int # Number of simulated actions used.
 @dataclass
    class Card:
        rank: int # Rank ranges from 1 through 13(Ace-King)

        suit:str # Suit uses a name, Clubs, Spades, Diamond, y Hearts.
  @dataclass 
    class Foundation:
        suit:str

        cards:list #Stores what cards have not been banked
        def can_add_card(self, card): # The card must match the foundation's suit
            if card.suit != self.suit: # This will ensure the card match's the foundations suit
                return False
            if len(self.cards) == 0: # Any card may begin an empty foundaion
                return True
            top_card = self.cards[-1] # This will retrieve the last card
            return card.rank == top_card.rank + 1 # Ensures that the order of cards is ascending.
        
        def add_card(self, card):
            if not self.can_add_card(card): #THis will reject illegal placements
                return False
            self.card.append(card) #Places cards into foundation
            return True # Report a succesful placement.

        def available_intervals(self):
            intervals = len(self.cards) // BANK_INTERVAL

            return intervals
        def is_complete_foundation(self):
            if len(self.cards) != FULL_FOUNDATION_SIZE:
                return False

            if self.cards[0].rank ! 1:
                return False

            if self.cards[-1].rank != 13:
                return False # the rules guarentee matching suits and ascending ranks between ace and king.

            return True

        def can_bank(self):
            if len(self.cards) == 0:
                return False    

            if self.is_complete_foundation():
                return True

            return len(self.cards) % BANK_INTERVAL == 0 #DAMN YOU GITBGASH


  