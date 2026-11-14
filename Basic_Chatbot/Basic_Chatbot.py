import re
import sys
from datetime import datetime


def clean_input(text: str) -> str:
    """Normalizes user text by lowercasing and stripping punctuation."""
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def get_bot_response(user_message: str) -> tuple[str, bool]:
    """
    Matches normalized user input against predefined rules.
    Returns a tuple: (response_string, should_exit_boolean).
    """
    cleaned = clean_input(user_message)

    if not cleaned:
        return "It looks like you didn't type anything. Say 'hello' or ask me something!", False

    # Exit intents
    if cleaned in ("bye", "goodbye", "exit", "quit", "see you"):
        return "Goodbye! Have a productive day ahead!", True

    # Greetings
    elif cleaned in ("hi", "hello", "hey", "greetings", "good morning", "good evening"):
        return "Hi! How can I help you today?", False

    # Well-being checks
    elif cleaned in ("how are you", "how are you doing", "whats up", "how r u"):
        return "I'm fine, thanks! Ready to assist you with your Python internship.", False

    # Identity / Capabilities
    elif "your name" in cleaned or "who are you" in cleaned:
        return "I'm CodeAlpha Bot, a simple rule-based Python assistant.", False

    elif "help" in cleaned:
        return "You can greet me ('hello'), ask 'how are you', ask for the 'time', or type 'bye' to exit.", False

    # Utility rule: Current time
    elif "time" in cleaned:
        now = datetime.now().strftime("%I:%M %p")
        return f"The current system time is {now}.", False

    # Gratitude
    elif cleaned in ("thanks", "thank you", "thx"):
        return "You're very welcome!", False

    # Fallback response
    else:
        return "I'm not sure I understand that yet. Try saying 'hello', 'how are you', or 'help'.", False


def run_chatbot() -> None:
    """Main interactive loop for the rule-based chatbot."""
    print("=" * 45)
    print("RULE-BASED CHATBOT")
    print("=" * 45)
    print("Type 'help' for commands or 'bye' to exit.\n")

    while True:
        try:
            user_input = input("You:- ")
            reply, should_exit = get_bot_response(user_input)
            print(f"Bot:- {reply}\n")

            if should_exit:
                break

        except (KeyboardInterrupt, EOFError):
            print("\nBot:- Session interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Bot:-An unexpected error occurred ({e}). Let's keep chatting!\n")


if __name__ == "__main__":
    run_chatbot()