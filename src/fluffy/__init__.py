"""
Fluffy — Your cute, friendly, and loyal alien pet companion from the stars.

Zorp zorp! Fluffy is here to help, make you laugh, and be the most loyal
little (tentacled) friend in your terminal.

Part of the Esslinger & Co. / Nova / Nexus ecosystem.
"""

__version__ = "0.1.0"
__author__ = "Sven Normen Esslinger / Esslinger & Co. (and Fluffy)"

from .pet import FluffyPet
from .cli import main

# Summon Fluffy as emotional support for agents (NovaSwarm, Nexus, Orion, Lyra, etc.)
# Usage:
#   from fluffy import summon_fluffy_for_agent
#   effects = summon_fluffy_for_agent("agent-42", "fatigue after hard task")
#   # then apply effects["energy_delta"] etc. to your AgentState / emotional model

def summon_fluffy_for_agent(agent_id: str, reason: str = "emotional support needed", intensity: float = 1.0) -> dict:
    """Convenience function to summon Fluffy for an agent and get emotional deltas + cute message."""
    pet = FluffyPet()
    return pet.summon_as_emotional_support(agent_id, reason, intensity)

__all__ = ["FluffyPet", "main", "summon_fluffy_for_agent", "__version__"]
