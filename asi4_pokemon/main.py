from pokemon import Pokemon, PlayerPokemon, PokemonType, allPokemon
import questionary 
import random

def chooseOwnPokemon() -> Pokemon:
    starterQuestion = questionary.select("Choose your Starter Pokémon", choices=[pokemon for pokemon in allPokemon.keys() if allPokemon[pokemon].starter])
    starterName = starterQuestion.ask()

    print(f"You selected {starterName}!")
    return PlayerPokemon(starterName)

def generateOpponent(ownPokemon: Pokemon) -> Pokemon:
    randomPokemonName = random.sample(sorted(allPokemon.keys()), 1)[0]
    return Pokemon(randomPokemonName, random.randint(ownPokemon.get_level(), ownPokemon.get_level() + 1))

def fightPhase(own: Pokemon, opponent: Pokemon): 
    print(f"{'Opponent':<12}", opponent)
    print(f"{'Own Pokemon':<12}", own)

    attacks = [
        questionary.Choice("Light", own.attack_light),
        questionary.Choice("Heavy", own.attack_heavy)
    ]
    fightQuestion = questionary.select("Choose your attack:", choices=attacks)
    attackMethod = fightQuestion.ask()
    attackMethod(opponent)

    if opponent.is_dead(): 
        print(f"{opponent.get_name()} fainted")
        return False

    opponent.attack_light(own)

    if own.is_dead(): return True


def main():
    random.seed()
    ownPokemon = chooseOwnPokemon()
    # Game Loop
    while not ownPokemon.is_dead():
        opponentPokemon = generateOpponent(ownPokemon)

        while not opponentPokemon.is_dead():
            lost = fightPhase(ownPokemon, opponentPokemon)
            if lost: 
                print(f"{ownPokemon.get_name()} fainted")
                break
        
        if ownPokemon.is_dead(): 
            print(f"You lost with your {ownPokemon}")
            break

        print("You won!")
        ownPokemon.receive_xp(10 * opponentPokemon.get_level())
        ownPokemon.heal()
main()