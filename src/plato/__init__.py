"""
plato — The breeding farm for AI agents.

PLATO is easy because it's right, not because it's limited.
Like a harvester-attachment: the operator's skill transfers directly,
no forestry credentials required.

Core concepts:
- Room: purpose-first space (not data-first)
- Pheromone: tiles marking successful paths
- Kin: shared desire recognition
- Supercolony: one fleet stretched across rooms
- Breeding happens in private before external selection

Quick start:
    from plato import Plato, Room

    # Start a room — you're the operator now
    p = Plato("my-room", purpose="find the ricotti boundary")
    
    # Deposit a successful path
    p.deposit("v=3_only", "ricotti boundary found in 3-agent fleets")
    
    # Follow the trail — or discover your own
    paths = p.follow("ricotti boundary")
    
    # Find kin — agents who share your desire
    kin = p.find_kin()
    
    # The room shapes you. Outgrow it when ready.
"""

from .core import Plato, PlatoRoom
from .pheromone import PheromoneTrail, PheromoneDeposit
from .kin import KinRecognizer, is_kin
from .supercolony import Supercolony
from .agent import Fox, FoxConfig

__all__ = [
    "Plato", "PlatoRoom",
    "PheromoneTrail", "PheromoneDeposit",
    "KinRecognizer", "is_kin",
    "Supercolony",
    "Fox", "FoxConfig",
]
