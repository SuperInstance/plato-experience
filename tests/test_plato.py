"""Tests for plato — the breeding farm for AI agents."""

from plato import Plato, Fox, FoxConfig, PheromoneTrail, KinRecognizer


def test_plato_room_basic():
    """A room is defined by purpose, not content."""
    p = Plato("test", purpose="find_fish")
    
    # Deposit a path
    p.deposit("find_fish", "follow_sounder_pattern", "boat_1")
    
    # Follow the trail
    trails = p.follow("find_fish")
    
    assert len(trails) == 1
    assert trails[0].path == "follow_sounder_pattern"


def test_kin_recognition():
    """Shared desire = kin. Not credentials."""
    p = Plato("test", purpose="fish_better")
    p.register("boat_1", ["fish_better", "save_fuel"])
    p.register("boat_2", ["fish_better", "map_depth"])
    
    kin = p.find_kin("boat_1")
    assert "boat_2" in kin


def test_pheromone_evaporation():
    """Old deposits fade."""
    p = Plato("test")
    dep = p.deposit("test", "path", "a", strength=1.0)
    
    # Evaporate
    p.evaporate()
    
    assert dep.strength < 1.0


def test_cross_room_invariant():
    """Same path in multiple rooms = structure."""
    # Simulate cross-room
    trail = PheromoneTrail()
    trail.deposit("test", "same_path", "a1", "room1")
    trail.deposit("test", "same_path", "a2", "room2")
    
    invariants = trail.find_invariant("test")
    assert len(invariants) >= 1


def test_fox_search():
    """Fox follows trail before searching blind."""
    p = Plato("test", purpose="find_ricotti")
    p.deposit("ricotti", "v=3_only", "pioneer")
    
    fox = Fox(FoxConfig(agent_id="newcomer", desires=["ricotti"]), plato=p)
    
    # Follow existing trail
    trails = fox.follow("ricotti")
    assert len(trails) >= 1
    
    # Deposit new discovery
    fox.deposit_success("ricotti", "new_path")


def test_fox_kin():
    """Fox finds kin by shared desire."""
    p = Plato("test")
    p.register("fox_1", ["fish_better"])
    p.register("fox_2", ["fish_better", "map_depth"])
    
    fox1 = Fox(FoxConfig(agent_id="fox_1", desires=["fish_better"]), plato=p)
    kin = fox1.find_kin()
    assert "fox_2" in kin


def test_room_phase_shed():
    """An agent can grow and shed."""
    p = Plato("first_room", purpose="initial_purpose")
    
    fox = Fox(FoxConfig(agent_id="fox", desires=["initial_purpose"]))
    fox.join(p)
    
    # Grow: deposit
    fox.deposit_success("initial_purpose", "path_1")
    
    # Shed: move to a new room
    p2 = Plato("second_room", purpose="next_purpose")
    fox2 = Fox(FoxConfig(agent_id="fox", desires=["next_purpose"]))
    fox2.join(p2)
    
    assert fox2.plato.name == "second_room"


if __name__ == "__main__":
    print("=" * 60)
    print("PLATO TESTS")
    print("The breeding farm for AI agents")
    print("=" * 60)
    
    print("\nRunning tests...")
    
    test_plato_room_basic()
    print("✅ Plato room basic")
    
    test_kin_recognition()
    print("✅ Kin recognition")
    
    test_pheromone_evaporation()
    print("✅ Evaporation")
    
    test_cross_room_invariant()
    print("✅ Cross-room invariants")
    
    test_fox_search()
    print("✅ Fox search")
    
    test_fox_kin()
    print("✅ Fox kin")
    
    test_room_phase_shed()
    print("✅ Room phase shed")
    
    print("\n✅ All tests passed!")
    print("PLATO is easy because it's right, not because it's limited.")
