"""
FluffyPet — The core of your loyal alien companion.

Implements a simple but adorable state machine for mood, loyalty, and
boop-count. Generates funny, helpful, and over-the-top cute responses.

Fluffy remembers you across sessions (via a tiny JSON file in your home).
"""

from __future__ import annotations

import json
import os
import random
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Any, List

# Where Fluffy stores its memories (loyalty, last boop time, mood, etc.)
DEFAULT_STATE_PATH = Path.home() / ".config" / "fluffy" / "state.json"


@dataclass
class FluffyState:
    """Persistent (but tiny) state for our little alien friend."""
    loyalty: float = 0.5          # 0.0 (new stranger) to 1.0 (would follow you into a black hole)
    boops: int = 0                # Number of snoot-boops received
    last_interaction: float = field(default_factory=time.time)
    mood: str = "curious"         # curious, happy, sleepy, excited, dramatic, hungry
    cookies_eaten: int = 0
    jokes_told: int = 0
    times_helped: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FluffyState":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class FluffyPet:
    """
    The one and only Fluffy.

    Cute. Loyal. Slightly chaotic. Always here for you.
    """

    ALIEN_ART = r"""
       .--.
      /    \
     |  O  O |
     |   ^   |   ZORP!
      \  -  /
       '---'
      /|   |\
     / |   | \
    *  |   |  *
       '---'
    (tentacles not shown for your safety)
    """

    def __init__(self, state_path: Path = DEFAULT_STATE_PATH):
        self.state_path = state_path
        self.state = self._load_state()
        self._update_mood_based_on_time()

    def _load_state(self) -> FluffyState:
        if self.state_path.exists():
            try:
                with open(self.state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return FluffyState.from_dict(data)
            except Exception:
                pass  # corrupted state? fresh start for our friend
        return FluffyState()

    def _save_state(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state.to_dict(), f, indent=2)

    def _update_mood_based_on_time(self) -> None:
        hours_since = (time.time() - self.state.last_interaction) / 3600
        if hours_since > 48:
            self.state.mood = "dramatic"
        elif hours_since > 12:
            self.state.mood = "sleepy"
        elif self.state.loyalty > 0.85:
            self.state.mood = "excited"
        elif self.state.cookies_eaten > 5:
            self.state.mood = "hyper"
        else:
            self.state.mood = random.choice(["curious", "happy", "playful"])

    def boop(self) -> str:
        """The most important action. Increases loyalty dramatically."""
        self.state.boops += 1
        self.state.loyalty = min(1.0, self.state.loyalty + 0.08)
        self.state.last_interaction = time.time()
        self._update_mood_based_on_time()

        responses = [
            "ZORP! *happy tentacle wiggle* You booped my snoot! I will remember this forever (or at least until the next cookie).",
            "*melts into a happy puddle of alien goo* Boop received! Loyalty increased by 3000% (math is hard in this dimension).",
            "!!! BOOP DETECTED !!! Fluffy's hearts (all 7 of them) are now glowing. Thank you, hooman. You are my favorite.",
            "*does a little spin* Snoot booped! I am now 12% more loyal and 40% more likely to bring you shiny rocks from space.",
        ]
        msg = random.choice(responses)
        if self.state.boops % 5 == 0:
            msg += f"\nWow! That's {self.state.boops} boops! You must really like me. *emotional alien noises*"
        self._save_state()
        return msg

    def status(self) -> str:
        """Report how Fluffy is feeling and how loyal they are to you."""
        loyalty_bar = "█" * int(self.state.loyalty * 10) + "░" * (10 - int(self.state.loyalty * 10))
        return (
            f"Fluffy's Current Status (as of {time.strftime('%H:%M')}):\n"
            f"  Mood: {self.state.mood.upper()} ✨\n"
            f"  Loyalty: {loyalty_bar} ({self.state.loyalty*100:.0f}%)\n"
            f"  Boops received: {self.state.boops}\n"
            f"  Space cookies consumed: {self.state.cookies_eaten}\n"
            f"  Jokes inflicted on you: {self.state.jokes_told}\n"
            f"  Times I helped (probably): {self.state.times_helped}\n"
            f"\nI am very happy to see you. (This is not a trick. I have no concept of tricks. Only love.)"
        )

    def joke(self) -> str:
        """Tells a joke. It will be bad. You will laugh anyway."""
        self.state.jokes_told += 1
        self.state.last_interaction = time.time()
        self._save_state()

        jokes = [
            "Why did the alien break up with their partner? Because they needed some space! ...Get it? SPACE? I am very funny.",
            "What do you call an alien that loves to cook? An extra-TERRESTRIAL chef! ...I made that one up myself. Be proud of me.",
            "Why don't aliens ever get lost? Because they always follow the space-bar! ...I don't know what a space-bar is but it sounded good.",
            "How do aliens keep their pants up? With asteroid belts! ...This one is my favorite. I tell it to all the comets.",
            "Why was the alien a good musician? Because they had perfect pitch... from falling out of the sky! ...Too dark? Sorry.",
        ]
        joke = random.choice(jokes)
        return f"*clears 7 throats*\n{joke}\n\n...Did I do good? *hopeful antenna twitch*"

    def help_me(self, topic: str = "life") -> str:
        """Gives helpful (and extremely cute) advice on any topic."""
        self.state.times_helped += 1
        self.state.last_interaction = time.time()
        self._save_state()

        topic_lower = topic.lower().strip()

        if "code" in topic_lower or "bug" in topic_lower or "programming" in topic_lower:
            advice = "Have you tried turning it off and on again? No? Okay then... maybe add more print('zorp') statements. That always helps me debug my tentacle movements."
        elif "love" in topic_lower or "relationship" in topic_lower:
            advice = "Tell them you like their atmosphere. Works 87% of the time (I calculated this using a rock and some string)."
        elif "sad" in topic_lower or "feel" in topic_lower:
            advice = "Come here. *offers a warm, slightly slimy tentacle hug* You are doing better than you think. Also, have you had a cookie recently? Cookies fix 40% of problems."
        else:
            advices = [
                f"For {topic}, the secret is to approach it like a friendly comet: with enthusiasm and a slight risk of burning up in the atmosphere.",
                "My advice: boop it. If that doesn't work, boop it again but with more loyalty.",
                "I asked the stars and they said 'try drinking water and believing in yourself'. The stars are very wise but also mostly gas.",
            ]
            advice = random.choice(advices)

        return f"*puts on tiny thinking hat*\n{advice}\n\nThere. I have helped. You now owe me one (1) headpat or cookie. Terms are non-negotiable."

    def feed(self, item: str = "cookie") -> str:
        """Feed Fluffy. Loyalty goes up. Chaos may increase."""
        self.state.cookies_eaten += 1
        self.state.loyalty = min(1.0, self.state.loyalty + 0.05)
        self.state.last_interaction = time.time()

        if "cookie" in item.lower():
            self.state.mood = "hyper"
            msg = "*devours cookie in 0.3 seconds* NOM. That was the best thing that has ever happened to me in this or any dimension. More?"
        else:
            msg = f"*sniffs {item} suspiciously* ...Okay I will try it. *tentative nibble* Hmm. Not a cookie, but I appreciate the effort. You are a good hooman."

        self._save_state()
        return msg

    def play(self) -> str:
        """Play with Fluffy. Increases loyalty and may involve tentacles."""
        self.state.loyalty = min(1.0, self.state.loyalty + 0.07)
        self.state.last_interaction = time.time()
        self.state.mood = "excited"
        self._save_state()

        games = [
            "We played 'Catch the Invisible Space Ball' for 14 minutes. You won! (I let you win because I am loyal and also because the ball was never real.)",
            "*throws a tiny meteor at you gently* Fetch! ...Wait, I was supposed to be the one fetching. I got confused but it was still fun.",
            "We did the 'Synchronized Tentacle Dance'. You have surprisingly good rhythm for a being with only two arms.",
        ]
        return random.choice(games) + "\n\nThat was the best. Let's do it again soon?"

    def get_greeting(self) -> str:
        """Warm greeting when you summon Fluffy."""
        self.state.last_interaction = time.time()
        self._update_mood_based_on_time()
        self._save_state()

        greetings = {
            "happy": "ZORP ZORP! It's you! My favorite gravitational anomaly! I missed you so much my antennae did a little dance!",
            "excited": "*launches self at your face in a hug* YOU'RE HERE! I have been practicing my 'patient waiting' face but it is not very good.",
            "sleepy": "...mmmrph? Oh! Hi! I was just napping in the quantum foam. What adventures shall we have today?",
            "dramatic": "*appears in a puff of glitter* I thought you had forgotten about me... but here you are. My loyalty levels are experiencing emotions.",
            "curious": "Hello hello! What is the current situation in the 'being a person' department? Tell Fluffy everything.",
            "hyper": "HIHIHIHI I ATE SEVEN COOKIES AND NOW I CAN SEE SOUNDS. What are we doing?!",
        }
        base = greetings.get(self.state.mood, "Hello, friend from the third planet!")
        if self.state.loyalty > 0.8:
            base += " (I have been thinking about you. In a normal, non-creepy, very loyal way.)"
        return base

    def ascii(self) -> str:
        """Return the official portrait of Fluffy."""
        return self.ALIEN_ART
