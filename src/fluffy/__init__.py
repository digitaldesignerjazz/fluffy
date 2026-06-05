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

__all__ = ["FluffyPet", "main", "__version__"]
