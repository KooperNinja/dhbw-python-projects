import time
import os

actions = {
    0: "Kontostand Prüfen",
    1: "Geld Abheben",
    2: "Geld Einzahlen",
}

currentAction = -1
balance = 420

waitSeconds = 5

def throwActionInputError():
    print("Bitte wählen sie einen der genannten Nummern")
    global currentAction
    currentAction = -1


def checkBalance():
    global waitSeconds
    waitSeconds = 5
    print(f"Ihre Aktueller Kontostand beträgt {balance:.2f}€")


def askForFloatInput():
    try:
        inputFloat = round(float(input("> ")), 2)
    except:
        print("Bitte geben sie ihre Zahl in diesem Format an X.XX")
        return False, 0
    if inputFloat < 0:
        print("Bitte geben sie eine positive Zahl an")
        return False, 0
    return True, inputFloat


def isZeroToReturnToMenu(input):
    if input != 0:
        return False
    print("Sie haben 0 ausgewält - Sie kehren zurück zum Menü")
    return True


def withdrawMoney():
    global balance
    print("Geben sie an, wie viel Geld sie Abheben möchten:")
    valid = False
    while not valid:
        valid, withdrawInput = askForFloatInput()

    if isZeroToReturnToMenu(withdrawInput):
        return

    if withdrawInput > balance:
        print(f"Sie haben nicht genug Geld um {withdrawInput:.2f}€ abzuheben")
        checkBalance()
        return

    balance -= withdrawInput
    print(f"Sie heben {withdrawInput:.2f}€ ab")
    checkBalance()


def depositMoney():
    global balance
    print("Geben sie an, wie viel Geld sie Einzahlen möchten:")

    valid = False
    while not valid:
        valid, depositInput = askForFloatInput()

    if isZeroToReturnToMenu(depositInput):
        return

    balance += depositInput
    print(f"Sie zahlen {depositInput:.2f}€ ein")
    checkBalance()


# Main Loop
def main():
    os.system('clear')
    global currentAction, waitSeconds
    while currentAction != -2:
        print("Willkommenm bei Ihrer Simple Bank!\nBitte wählen Sie nun eine der Folgenden Aktionen:")
        for actionId, actionTitle in actions.items():
            print(f"{actionId} : {actionTitle}")
        currentAction = input("> ")
        # Avoid malicous input to fail programm
        try:
            currentAction = int(currentAction)
        except:
            throwActionInputError()
            continue

        if currentAction > len(actions) - 1 or currentAction < 0:
            throwActionInputError()
            continue

        print(f"Sie haben \"{actions[currentAction]}\" gewählt\n")

        match (currentAction):
            case 0:
                checkBalance()
            case 1:
                withdrawMoney()
                waitSeconds = 8
            case 2:
                depositMoney()
                waitSeconds = 8
        
        print(f"\nSie kehren zurück zum Menü", end="", flush=True)
        for i in range(0, waitSeconds):
            print(".", end="", flush=True)
            time.sleep(1)

        os.system('clear')


main()
