import random
from enum import IntEnum


class KaartKleur(IntEnum):
    HARTEN = 0
    RUITEN = 1
    KLAVER = 2
    SCHOPPEN = 3

    @classmethod
    def is_stronger_than(cls, kleur_a: int, kleur_b: int) -> bool:
        return cls(kleur_a) < cls(kleur_b)

class Contract:
    TYPE_RANK = {
        "samen": 1,
        "alleen": 2,
        "miserie": 3,
        "piccolo": 4,
        "abondance": 5,
        "soloslim": 6,
        "troel": 7,
    }

    def __init__(self, type: str, troefkleur: int, slagen: int, player_name : str):
        if type not in self.TYPE_RANK:
            raise ValueError(f"Onbekend contracttype: {type}")
        self.type = self.TYPE_RANK[type]
        self.doel_slagen = slagen
        self.min_doel_slagen = 0
        self.contractOwner = player_name
        self.troefkleur = troefkleur
        self.persoonDieMeegaat = ""

    def Calculate_min_doel_slagen(self) -> bool:
        modified = False
        if self.type == 1:
            self.min_doel_slagen = 8
        elif self.type == 2:
            self.min_doel_slagen = 5
        elif self.type == 3: # Miserie
            self.min_doel_slagen = 0
            if self.doel_slagen != 0:
                self.doel_slagen = 0
                modified = True
        elif self.type == 4: # Piccolo
            self.min_doel_slagen = 1
            if self.doel_slagen != 1:
                self.doel_slagen = 1
                modified = True
        elif self.type == 5: # Abondance
             self.min_doel_slagen = 9
             if self.doel_slagen < self.min_doel_slagen:
                 self.doel_slagen = 9
                 modified = True
        elif self.type == 6: # Soloslim
            self.min_doel_slagen = 13
            if self.doel_slagen != 13:
                self.doel_slagen = 13
                modified = True
        return modified



    def getDoelslagen(self) -> int:
        return self.doel_slagen

    def getTroefKleur(self):
        return self.troefkleur

    def getSoortType(self) -> int:
        return self.type

    def setContractOwner(self, contractOwner: str):
        self.contractOwner = contractOwner

    def getContractOwner(self) -> str:
        return self.contractOwner

    def setPersoonDieMeegaat(self, persoon):
        self.persoonDieMeegaat = persoon

    def getPersoonDieMeegaat(self):
        return self.persoonDieMeegaat

    def get_waarde(self):
        return self.type * 100 + self.doel_slagen

    def get_prioriteit(self, vreemd_kleur, vreemd_aantalslagen) -> bool:
        if KaartKleur.is_stronger_than(self.troefkleur, vreemd_kleur):
            if self.doel_slagen > vreemd_aantalslagen:
                return True
            else:
                return False
        else:
            return False



class Kaart:
    def __init__(self, color, value):
        if not 0 <= color <= 3:
            raise ValueError("Ongeldige kleur")
        self.color = color
        self.value = value  # 1=Aas, 2-10=cijfers, 11=Boer, 12=Vrouw, 13=Koning

    def get_label(self):
        """Geeft de naam terug voor de speler (bijv. 'A' of '10')."""
        labels = {1: "A", 11: "J", 12: "Q", 13: "K"}
        return labels.get(self.value, str(self.value))

    def get_rank(self):
        """
        Geeft de sterkte van de kaart terug.
        Volgens de spelregels: Aas(14) > K(13) > Q(12) > J(11) > 10... > 2
        """
        if self.value == 1:
            return 14  # Aas is altijd de hoogste
        if self.value == 13:
            return 13  # Koning
        if self.value == 12:
            return 12  # Vrouw
        if self.value == 11:
            return 11  # Boer
        return self.value  # 2 t/m 10

    def getColor(self):
        return self.color

    def getValue(self):
        return self.value

    def sort_priority(self):
        return self.get_rank()


    def getColorName(self) -> str:
        return KaartKleur(self.color).name.capitalize()


    def is_stronger_color_than(self, other: 'Kaart') -> bool:
        return KaartKleur.is_stronger_than(self.color, other.color)

    def get_sterkte(self, troefkleur : int = None) -> int:
        if troefkleur is not None and self.color == troefkleur:
            return self.get_rank() + 15
        return self.get_rank()


class Speler:
    def __init__(self, name : str):
        self.name = name
        self.hand = []
        self.sortedHand = []
        self.score = int
        self.heeftGepassed = False

    def setHand(self, Kaart):
        self.hand.append(Kaart)

    def getHand(self):
        return self.hand

    def getName(self):
        return self.name

    def getHeeftGepassed(self):
        return self.heeftGepassed

    def setHeeftGepassed(self, heeftGepassed):
        self.heeftGepassed = heeftGepassed


    def sort_hand(self):
        color_0 = []
        color_1 = []
        color_2 = []
        color_3 = []
    #    stilSorting = True
        for kaart in self.hand[:]:  # [:] maakt een kopie
            color = kaart.getColor()
            if color == 0:
                color_0.append(kaart)
            elif color == 1:
                color_1.append(kaart)
            elif color == 2:
                color_2.append(kaart)
            elif color == 3:
                color_3.append(kaart)

        self.sortedHand = []
        for kleur in [color_0, color_1, color_2, color_3]:
            for f in sorted(kleur, key=Kaart.sort_priority):
                self.sortedHand.append(f)
                print(f.color, f.value)

    def getSortedHand(self):
        return self.sortedHand


#game logic

class Game:
    def __init__(self, spelernamen):
        self.spelers = [Speler(naam) for naam in spelernamen]
        self.alle_kaarten = []
        self.contracten = []
        self.hoogste_contract = None
        self.dealer_index = 0
        self.beurt_index = 0
        self.fase = "SETUP"

    def setup_spel(self):
        self.initialiseer_deck()
        self.deal_kaarten()
        self.fase = "BIEDEN"
        self.beurt_index =(self.dealer_index + 1) % 4



    def initialiseer_deck(self):
        for i in range(4):
            for b in range(1, 14):
                self.alle_kaarten.append(Kaart(i, b))


    def track_dealer(self):
        current = self.dealer_index
        self.dealer_index += 1
        if self.dealer_index >= 4:
            self.dealer_index = 0
        return current

    def deal_kaarten(self):
        eerste_keer_delen = True
        self.track_dealer()
        if eerste_keer_delen:
            random.shuffle(self.alle_kaarten)
            for _ in range(4):
                for speler in self.spelers:
                    kaart = self.alle_kaarten.pop(0)
                    speler.setHand(kaart)
            for _ in range(4):
                for speler in self.spelers:
                    kaart = self.alle_kaarten.pop(0)
                    speler.setHand(kaart)
            for _ in range(5):
                for speler in self.spelers:
                    kaart = self.alle_kaarten.pop(0)
                    speler.setHand(kaart)
            eerste_keer_delen = False
        elif len(self.alle_kaarten) == 52:
            for _ in range(4):
                for speler in self.spelers:
                    kaart = self.alle_kaarten.pop(0)
                    speler.setHand(kaart)
            for _ in range(4):
                for speler in self.spelers:
                    kaart = self.alle_kaarten.pop(0)
                    speler.setHand(kaart)
            for _ in range(5):
                for speler in self.spelers:
                    kaart = self.alle_kaarten.pop(0)
                    speler.setHand(kaart)

    def contractCheck(self, c: Contract) -> bool:
        if self.hoogste_contract is None:
            return True

        elif c.get_waarde() > self.hoogste_contract.get_waarde():
            return True
        return False

    def troelCheck(self) -> bool:
        aantal_aas = 0
        for i in range(len(self.spelers)):
            aantal_aas = 0
            for r in range(len(self.spelers[i].getHand())):
                if self.spelers[i].getHand()[r].get_rank() == 14:
                    aantal_aas += 1
                if aantal_aas == 3:
                    return True
        if aantal_aas == 0:
            return False



    def bieden(self, speler_idx: int, bod_type: str, bod_kleur: int, slagen: int) -> bool:
        if speler_idx is not None and bod_type is not None and bod_kleur is not None and slagen is not None:
            c =  Contract(bod_type, bod_kleur, slagen, self.spelers[speler_idx].getName())
            if not c.Calculate_min_doel_slagen():
                if self.contractCheck(c) and self.checkHoogsteContract(c):
                    self.hoogste_contract = c
                    self.contracten.append(c)
                    return True
                else:
                    return False
            else:
                return False
        else:
            c =  Contract("troel", bod_kleur, slagen, self.spelers[speler_idx].getName())
            if not c.Calculate_min_doel_slagen():
                if self.contractCheck(c) and self.checkHoogsteContract(c):
                    self.hoogste_contract = c
                    self.contracten.append(c)
                    return True
                else:
                    return False
            else:
                return False

    def checkHoogsteContract(self, c: Contract):
        if not self.contracten:
            return True
        return c.get_waarde() > max(ex.get_waarde() for ex in self.contracten)
