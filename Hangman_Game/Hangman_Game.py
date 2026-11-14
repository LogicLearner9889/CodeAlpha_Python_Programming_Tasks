import random
import sys

def get_valid_guess(guessed_letters: set) -> str:
    """Prompts the user for a single alphabetical character and validates it."""
    while True:
        try:
            guess = input("\nGuess a letter:- ").strip().lower()

            if not guess:
                print("Input cannot be empty. Please enter a letter.")
                continue

            if len(guess) != 1 or not guess.isalpha():
                print("Invalid input. Please enter a single English alphabet letter (a-z).")
                continue

            if guess in guessed_letters:
                print(f"You already guessed '{guess}'. Try a different letter.")
                continue

            return guess

        except (KeyboardInterrupt, EOFError):
            print("\n\nGame interrupted by user. Exiting safely...")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected input error occurred: {e}")


def play_hangman() -> None:
    """Main game loop for Hangman."""
    word_list = ["python", "coding", "intern", "script", "github"]
    secret_word = random.choice(word_list)
    guessed_letters = set()
    max_attempts = 6
    incorrect_guesses = 0

    print("=" * 40)
    print("WELCOME TO HANGMAN")
    print("=" * 40)
    print(f"The word has {len(secret_word)} letters. You have {max_attempts} incorrect guesses allowed.")

    while incorrect_guesses < max_attempts:
        # Display current word progress
        display_word = " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])
        print(f"\nWord:- {display_word}")
        print(f"Incorrect guesses left:- {max_attempts - incorrect_guesses}")
        if guessed_letters:
            print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")

        # Check win condition
        if "_" not in display_word:
            print(f"\nCongratulations! You guessed the word:- '{secret_word.upper()}'!")
            return

        guess = get_valid_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Good job! '{guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")

    print("\n" + "=" * 40)
    print(f"GAME OVER! You ran out of guesses. The word was: '{secret_word.upper()}'.")
    print("=" * 40)


if __name__ == "__main__":
    while True:
        play_hangman()
        try:
            replay = input("\nDo you want to play again? (y/n):- ").strip().lower()
            if replay != "y":
                print("Thanks for playing! Goodbye.")
                break
        except (KeyboardInterrupt, EOFError):
            print("\nExiting game. Goodbye!")
            break