from scoring import Hand, PeggingPile
from player import RandomPlayer, Player, HumanPlayer
from card import Deck
import random


class CribbageGame():
    def __init__(self, player_one=RandomPlayer('AI 1'), player_two=RandomPlayer('AI 2')):
        self._deck = Deck()
        self._player_one = player_one
        self._player_two = player_two
        self._crib = Hand()
        self._pegging_pile = PeggingPile()
        self._dealer = random.randint(0, 1)
        self._turn = (self._dealer + 1) % 2

    def __str__(self) -> str:
        s = '[Game'
        s += '\n\tPlayer 1: ' + str(self.player_one) + str(self.player_one.hand)
        if self.dealer == self.player_one:
            s += ' <- DEALER'
        s += '\n\tPlayer 2: ' + str(self.player_two) + str(self.player_two.hand)
        if self.dealer == self.player_two:
            s += ' <- DEALER'
        
        s += '\n\tCrib: ' + str(self.crib)
        s += '\n\tPegging Pile: ' + str(self.pegging_pile)
        s += '\n\tDeck: ' + str(self.deck)

        return s + '\n]'

    def __repr__(self) -> str:
        return str(self)

    @property
    def player_one(self) -> Player:
        """
        Return player one
        """
        return self._player_one
    
    @property
    def player_two(self) -> Player:
        """
        Return player two
        """
        return self._player_two

    @property
    def crib(self) -> Hand:
        """
        Returns the Hand representing a crib
        """
        return self._crib

    @property
    def pegging_pile(self) -> PeggingPile:
        """
        Returns the PeggingPile for this game
        """
        return self._pegging_pile

    @property
    def deck(self) -> Deck:
        """
        Returns the deck for this game, with any cards handed out to players not included
        """
        return self._deck

    @property
    def dealer(self) -> Player:
        """
        Returns the current dealer
        """
        if self._dealer == 0:
            return self.player_one
        return self.player_two

    @property
    def turn(self) -> Player:
        """
        Returns the player who's turn it currently is
        """
        if self._turn == 0:
            return self.player_one
        return self.player_two

    def reset_game(self):
        """
        Reset the game by sending all cards back to the deck, changing the dealer and resetting the turn counter
        """
        self.deck.return_cards_to_deck(self.player_one.clear_hand())
        self.deck.return_cards_to_deck(self.player_two.clear_hand())
        self.deck.return_cards_to_deck(self.crib.cards)
        self.deck.return_cards_to_deck(self.pegging_pile.end_pegging())
        self.crib.discard(self.crib.cards)
        self._turn = self._dealer
        self._dealer = (self._dealer + 1) % 2
        
    def initialize_round(self):
        """
        Initialize a round by shuffling and cutting the deck
        """
        self.deck.shuffle()
        self.deck.cut()

    def deal_cards(self):
        """
        Deal cards to both players
        """
        self.player_one.get_cards([self.deck.deal_card() for _ in range(6)])
        self.player_two.get_cards([self.deck.deal_card() for _ in range(6)])

    def handle_discards(self):
        """
        Handles discards for the two players, puts their discards into the crib
        """
        self.crib.add_cards(self.player_one.select_discards() + self.player_two.select_discards())