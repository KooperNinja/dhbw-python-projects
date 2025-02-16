from __future__ import annotations
from enum import Enum
import random

BASE_HEALTH = 10
BASE_DAMAGE = 2

class PokemonType(Enum):
    FIRE = 0
    WATER = 1
    PLANT = 2

class PokemonInfo:
    def __init__(self, type: PokemonType, starter: bool = False):
        self.type = type
        self.starter = starter

def getTypeModifierForTypeAgainstType(type1: PokemonType, type2: PokemonType):
    if type1.value == type2.value: return 1
    if (type1.value - 1) % 3 == type2.value: return 1.5
    return 0.5


class Pokemon:
    def __init__(self, name: str, level: int = 1):
        self._name = name

        info = allPokemon[name]
        if info is None:
            print(f"Pokemon with the name of {name} is not found")
            return

        self._type = info.type 
        self._level = level
        # Resets to 0 after level-up
        self._xp = 0
        self._neededXp = 10 * (1.5 ** (self._level - 1))
        self._maxHealth = BASE_HEALTH + (3 * (self._level - 1))
        self._health = self._maxHealth
        self._damage = BASE_DAMAGE + (2 * (self._level - 1))

    def __eq__(self, other: Pokemon):
        return self.get_name() == other.get_name()
    
    def __str__(self):
        return f"{self._name:<10} | HP: {self._health:>3} | Lvl: {self._level:>3}"

    def get_name(self):
        return self._name
    
    def get_type(self):
        return self._type
    
    def get_level(self):
        return self._level
    
    def get_damage(self, opponentTyp: PokemonType):
        return round(self._damage * getTypeModifierForTypeAgainstType(self._type, opponentTyp))
    
    def is_dead(self):
        return self._health <= 0

    def receive_damage(self, damage: int):
        print(f"{self.get_name()} received {damage} Damage!")
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def receive_xp(self, amount: int):
        print(f"{self.get_name()} received {amount} XP!")
        self._xp += amount
        while self._xp >= self._neededXp:
            self._xp -= self._neededXp
            self.level_up()

    def attack_light(self, opponent: Pokemon):
        print(f"Light Attack hit {opponent.get_name()}")
        opponent.receive_damage(self.get_damage(opponent.get_type()))

    def attack_heavy(self, opponent: Pokemon):
        randomFail = random.randint(1, 3)
        if randomFail == 3:
            print("Heavy Attack failed")
            return
        print(f"Heavy Attack hit {opponent.get_name()}")
        opponent.receive_damage(self.get_damage(opponent.get_type()) * 4)

    def heal(self):
        print(f"{self.get_name()} healed")
        self._health = self._maxHealth

    def level_up(self):
        self._level += 1
        print(f"{self.get_name()} leveled up to {self._level}")
        self._damage += 2
        self._maxHealth += 3
        self._neededXp += 30

class PlayerPokemon(Pokemon):
    def get_name(self):
        return f"My {super().get_name()}"




allPokemon: dict[str, PokemonInfo] = {
    "Charmander": PokemonInfo(PokemonType.FIRE, True),
    "Squirtle": PokemonInfo(PokemonType.WATER, True),
    "Bulbasaur": PokemonInfo(PokemonType.PLANT, True),
    "Vulpix": PokemonInfo(PokemonType.FIRE),
    
}   