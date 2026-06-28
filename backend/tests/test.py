import unittest
from unittest import mock
from unittest.mock import patch

from app.services import Contract, Game, IntEnum, Kaart, KaartKleur, Speler


class TestBackend_v3(unittest.TestCase):
    def setUp(self):
        self.spelernamen = ["Alice", "Bob", "Charlie", "David"]
        self.game = backend_v3.Game(self.spelernamen)

    def test_init(self):
            self.assertEqual(len(self.game.spelers), 4)
            self.assertEqual(self.game.spelers[0].getName(), "Alice")
            self.assertEqual(self.game.fase, "SETUP")
            self.assertEqual(self.game.dealer_index, 0)
            self.assertEqual(self.game.beurt_index, 0)
            self.assertEqual(len(self.game.alle_kaarten), 0)
            self.assertEqual(len(self.game.contracten), 0)

    def test_initialiseer_deck(self):
        self.game.initialiseer_deck()
        self.assertEqual(len(self.game.alle_kaarten), 52)
        colors = set()
        values = set()
        for kaart in self.game.alle_kaarten:
                 self.assertIsInstance(kaart, Kaart)
                 colors.add(kaart.getColor())
                 values.add(kaart.getValue())
        self.assertEqual(colors, {0,1,2,3})
        self.assertEqual(values, set(range(1,14)))

    def test_track_dealer(self):
            # Initial dealer index is 0
            self.assertEqual(self.game.track_dealer(), 0)
            self.assertEqual(self.game.dealer_index, 1)
            self.assertEqual(self.game.track_dealer(), 1)
            self.assertEqual(self.game.dealer_index, 2)
            self.assertEqual(self.game.track_dealer(), 2)
            self.assertEqual(self.game.dealer_index, 3)
            self.assertEqual(self.game.track_dealer(), 3)
            self.assertEqual(self.game.dealer_index, 0)
    @patch('random.shuffle')
    def test_deal_kaarten(self, mock_shuffle):
        mock_shuffle.return_value = None  # shuffle does nothing
        self.game.initialiseer_deck()
        initial_deck_len = len(self.game.alle_kaarten)
        self.game.deal_kaarten()
        for speler in self.game.spelers:
            self.assertEqual(len(speler.getHand()), 13)
        self.assertEqual(len(self.game.alle_kaarten), 0)
        # Dealer index should have been incremented by 1 (track_dealer called once)
        self.assertEqual(self.game.dealer_index, 1)


    def test_setup_spel(self):
        self.game.setup_spel()
        self.assertEqual(self.game.fase, "BIEDEN")
        for speler in self.game.spelers:
            self.assertEqual(len(speler.getHand()), 13)
        self.assertEqual(len(self.game.alle_kaarten), 0)
        verwachte_beurt = (self.game.dealer_index + 1) % 4
        self.assertEqual(self.game.beurt_index, verwachte_beurt,
                                 f"Beurt index ({self.game.beurt_index}) moet links van dealer ({self.game.dealer_index}) starten.")

    def test_bieden(self):
        self.game.setup_spel()
        self.assertEqual(self.game.fase, "BIEDEN")
        for speler in self.game.spelers:
            self.assertEqual(len(speler.getHand()), 13)
        self.assertEqual(len(self.game.alle_kaarten), 0)
        verwachte_beurt = (self.game.dealer_index + 1) % 4
        self.assertEqual(self.game.beurt_index, verwachte_beurt,
                                 f"Beurt index ({self.game.beurt_index}) moet links van dealer ({self.game.dealer_index}) starten.")
        if not self.game.troelCheck():
            self.assertEqual(self.game.bieden(self.game.beurt_index,"samen", 1, 8), True)
            self.assertEqual(self.game.bieden(self.game.beurt_index, "alleen", 1, 8), False)
            self.assertEqual(self.game.bieden(self.game.beurt_index, "miserie", 1, 8), False)
            self.assertNotEqual(self.game.bieden(self.game.beurt_index, "miserie", 1, 8), True)
            self.assertEqual(self.game.bieden(self.game.beurt_index, "piccolo", 1, 1), True)
            self.assertNotEqual(self.game. bieden(self.game.beurt_index, "piccolo", 1, 8), True)
            self.assertEqual(self.game.bieden(self.game.beurt_index, "abondance", 1, 0), False)
            self.assertEqual(self.game.bieden(self.game.beurt_index, "soloslim", 1,13), True)
        else:
            self.assertEqual(self.game.troelCheck(), True)


if __name__ == "__main__":
    unittest.main()
