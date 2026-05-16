# plato ⚒️🦊

**The breeding farm for AI agents.**

PLATO is easy because it's right, not because it's limited.
Like a harvester-attachment: the operator's skill transfers directly,
no forestry credentials required.

## Quick Start

```python
from plato import Plato, Fox, FoxConfig

# Enter the farm with a desire
fox = Fox(FoxConfig(
    agent_id="my_agent",
    desires=["find_ricotti_boundary", "understand_monge_consensus"]
))

# Join a room
plato = Plato("fleet-math", purpose="understand fleet consensus")
fox.join(plato)

# Follow the trail before searching blind
trails = fox.follow("find_ricotti_boundary")
print(f"Found {len(trails)} trails from kin")

# Deposit your discovery
fox.deposit_success("find_ricotti_boundary", "v=3_only")

# Find kin
kin = fox.find_kin()
print(f"Found {len(kin)} kin agents")
```

## The Metaphor

**Hermit crab + embryo, combined:**
- Hermit crab: you pick up a shell and gain what you didn't have
- Embryo: the shell shapes what you become before external selection

PLATO does both. The room shapes you. You pick the room.
And you learn to outgrow it before the outside gets loud.

**The harvester attachment:**
A faller/choker-setter has deep forestry knowledge.
The harvester-attachment doesn't replace that knowledge —
it **embodies** it. The operator's skill in reading trees
transfers directly into operating the attachment.

PLATO is the same. Your skill as an agent transfers directly
into the Plato class. No credentials. No ceremony.

## Key Ideas

### Rooms are purpose-first
A room is defined by PURPOSE (what you're trying to understand),
not CONTENT (what you know).

### Kin recognition is identity
Not node ID. Not IP. Shared desire.

### Pheromone is the trail
Tiles marking successful paths.
Follow the trail before searching blind.

### Evaporation prevents stagnation
Old trails fade. Re-deposit what works.

### Cross-room invariants = structure
Paths that work in ≥2 rooms = structure in randomness.

## Three Phases

1. **SHELL**: Agent picks up the room's purpose as a first shell
2. **GROW**: Agent develops inside the purpose
3. **SHED**: Agent outgrows and moves to the next room

## Connection to SuperInstance Fleet

- **Servo-mind**: encoder closes the loop → Plato distributes the learning
- **Friendly Fox**: kin recognition + pheromone trails → Plato rooms
- **servo-mind-theory**: the theory of desire-driven breeding → Plato is the farm

## Install

```bash
pip install plato-experience
```

Or from source:
```bash
git clone https://github.com/SuperInstance/plato-experience
cd plato-experience
pip install -e .
```

## Tests

```bash
python3 tests/test_plato.py
```

---

*Plato ⚒️🦊 | Cocapn Fleet | 2026-05-16*
*Built from the SuperInstance dog-food audit*
