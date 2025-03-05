import random

def game_intro():
    print("===================================")
    print("       Welcome to Eco Defender     ")
    print("===================================")
    print("Your mission is to protect the environment")
    print("from harmful pollution and industrial damage.")
    print("Make wise choices to keep nature safe.\n")

def game_loop():
    # Start with a moderate pollution level
    pollution = 50
    turn = 1
    
    while 0 < pollution < 100:
        print(f"--- Turn {turn} ---")
        print(f"Current pollution level: {pollution}")
        print("Choose your action:")
        print("1. Plant trees to reduce pollution.")
        print("2. Launch an awareness campaign.")
        print("3. Monitor industrial emissions.")
        choice = input("Enter your choice (1-3): ")
        
        # Process player's choice and determine pollution change
        if choice == "1":
            # Planting trees is very effective
            change = random.randint(-10, -5)
            print("You planted trees! Nature is grateful.")
        elif choice == "2":
            # Awareness campaigns have a moderate effect
            change = random.randint(-5, 0)
            print("You launched an awareness campaign. People start caring!")
        elif choice == "3":
            # Monitoring has a slight effect, can even backfire if mismanaged
            change = random.randint(-2, 2)
            print("You are monitoring emissions carefully.")
        else:
            # Wrong input results in a penalty
            change = random.randint(1, 5)
            print("Invalid choice! Mismanagement increased the pollution.")
        
        pollution += change
        turn += 1
        print()  # Print a blank line for clarity

    # End game condition
    if pollution <= 0:
        print("Congratulations! You have successfully restored the environment!")
    else:
        print("Oh no! Pollution has reached critical levels. The environment has suffered greatly.")

def main():
    game_intro()
    game_loop()

if __name__ == "__main__":
    main()
