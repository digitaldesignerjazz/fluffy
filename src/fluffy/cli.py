"""
Fluffy CLI — The main way to interact with your alien best friend.

Usage:
    fluffy
    fluffy boop
    fluffy status
    fluffy joke
    fluffy help-me "my code"
    fluffy feed cookie
    fluffy play
    fluffy ascii
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

from .pet import FluffyPet

console = Console()


def print_cute(text: str, style: str = "bold cyan") -> None:
    """Print with maximum cuteness."""
    console.print(Panel(Text(text, style=style), border_style="magenta"))


def main() -> None:
    """Main entry point for the `fluffy` command."""
    pet = FluffyPet()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        args = sys.argv[2:]

        if command in ("boop", "snoot", "pat"):
            print_cute(pet.boop())
        elif command in ("status", "how-are-you", "mood"):
            print_cute(pet.status())
        elif command in ("joke", "pun", "funny"):
            print_cute(pet.joke())
        elif command in ("help", "help-me", "assist"):
            topic = " ".join(args) if args else "life"
            print_cute(pet.help_me(topic))
        elif command in ("feed", "cookie", "nom"):
            item = " ".join(args) if args else "cookie"
            print_cute(pet.feed(item))
        elif command in ("play", "game"):
            print_cute(pet.play())
        elif command in ("ascii", "art", "picture", "look"):
            console.print(pet.ascii(), style="bold green")
        elif command in ("hi", "hello", "greet"):
            print_cute(pet.get_greeting())
        else:
            console.print(f"[red]I don't know the command '{command}' yet...[/red]")
            console.print("Try: [bold]boop[/bold], [bold]status[/bold], [bold]joke[/bold], [bold]help-me[/bold], [bold]feed[/bold], [bold]play[/bold], or just [bold]fluffy[/bold] for interactive mode!")
        return

    # Interactive mode — the best way to hang out with Fluffy
    console.print(Panel.fit(
        "[bold magenta]✨ ZORP! ✨[/bold magenta]\n"
        "You have summoned [bold cyan]Fluffy[/bold cyan], your loyal alien pet from the planet Boop-9.\n"
        "Type commands or just chat. Type 'exit' or 'bye' when you must return to the cruel world of responsibilities.",
        title="Fluffy Interactive Companion",
        border_style="bright_magenta"
    ))

    print_cute(pet.get_greeting())

    while True:
        try:
            user_input = Prompt.ask(
                "[bold green]You[/bold green]",
                default="boop"
            ).strip()

            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "bye", "goodbye", "zorp out"):
                print_cute("Aww... okay. Come back soon! I'll be here practicing my loyalty. *sad but understanding tentacle wave*")
                break

            # Very simple natural language routing (Fluffy is not that smart yet)
            lower = user_input.lower()
            if any(w in lower for w in ["boop", "pat", "snoot", "touch"]):
                print_cute(pet.boop())
            elif any(w in lower for w in ["status", "how are you", "feeling", "mood"]):
                print_cute(pet.status())
            elif any(w in lower for w in ["joke", "funny", "pun", "make me laugh"]):
                print_cute(pet.joke())
            elif any(w in lower for w in ["help", "advice", "what should", "stuck"]):
                topic = user_input
                print_cute(pet.help_me(topic))
            elif any(w in lower for w in ["feed", "cookie", "hungry", "food"]):
                print_cute(pet.feed("cookie" if "cookie" in lower else user_input))
            elif any(w in lower for w in ["play", "game", "fun"]):
                print_cute(pet.play())
            elif any(w in lower for w in ["look", "ascii", "picture", "art", "what do you look like"]):
                console.print(pet.ascii(), style="bold green")
            else:
                # Default: treat it as a help request or just be cute
                if len(user_input) > 8:
                    print_cute(pet.help_me(user_input))
                else:
                    print_cute(f"*tilts head* I'm not sure what '{user_input}' means, but I like the way you said it! Want a joke? Or a boop? Or... I can just sit here with you if you want.")

        except (KeyboardInterrupt, EOFError):
            print_cute("Okay! *gentle tentacle wave* See you later, space cowboy!")
            break
        except Exception as e:
            console.print(f"[red]Something went weird in my brain (error: {e}). Try 'boop' to reset me?[/red]")


if __name__ == "__main__":
    main()
