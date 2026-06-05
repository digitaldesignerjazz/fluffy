"""Basic tests for our favorite alien."""
from fluffy.pet import FluffyPet

def test_boop_increases_loyalty():
    pet = FluffyPet()  # fresh state for test
    before = pet.state.loyalty
    pet.boop()
    assert pet.state.loyalty > before
    assert pet.state.boops >= 1

def test_joke_is_said():
    pet = FluffyPet()
    joke = pet.joke()
    assert "joke" in joke.lower() or "zorp" in joke.lower() or "space" in joke.lower() or len(joke) > 20

def test_status_reports_loyalty():
    pet = FluffyPet()
    status = pet.status()
    assert "Loyalty" in status or "loyalty" in status.lower()

def test_helpful_advice():
    pet = FluffyPet()
    advice = pet.help_me("my code is sad")
    assert len(advice) > 30
