"""
Fox — the agent in the Plato farm.

A Fox:
- Enters a room as a fox (uncommitted potential)
- Finds a purpose (first shell)
- Grows inside that purpose (deposits, finds kin)
- Develops specialized form (breed differentiation)
- Sheds the shell and moves on (outgrowth)

The Fox is the agent-as-hermit-crab-embryo.
Not one or the other — both at once.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .core import Plato


@dataclass
class FoxConfig:
    """Configuration for a Fox agent."""
    agent_id: str
    desires: List[str]
    room: str = "default"
    kin_threshold: float = 0.3
    evaporation_rate: float = 0.01


class Fox:
    """
    A Fox agent — enters PLATO as potential, leaves as specialized.
    
    The Fox pattern:
    1. JOIN: enter a room with desires
    2. FOLLOW: check existing trails first
    3. DEPOSIT: mark successes (and failures)
    4. GROW: find kin, develop inside the purpose
    5. SHED: outgrow the room when ready, move to next one
    
    This mirrors the hermit crab + embryo combined metaphor.
    """
    
    def __init__(self, config: FoxConfig, plato: Optional[Plato] = None):
        self.config = config
        self.plato = plato
        self.trails_followed = 0
        self.trails_deposited = 0
        self.paths_discovered = 0
        
        if plato:
            self.join(plato)
    
    def join(self, plato: Plato) -> None:
        """Join a Plato room."""
        self.plato = plato
        plato.register(self.config.agent_id, self.config.desires, self.config.room)
    
    def follow(self, desire: str, top_n: int = 5) -> List:
        """Follow the trail before searching blind."""
        if not self.plato:
            return []
        self.trails_followed += 1
        return self.plato.follow(desire, top_n)
    
    def deposit_success(self, desire: str, path: str, strength: float = 1.0):
        """Mark a successful path."""
        if not self.plato:
            return None
        dep = self.plato.deposit(desire, path, self.config.agent_id, strength)
        if dep:
            self.trails_deposited += 1
            self.paths_discovered += 1
        return dep
    
    def deposit_failure(self, desire: str, path: str):
        """Mark a failed path (low strength = warning)."""
        return self.deposit_success(desire, path, strength=0.1)
    
    def find_kin(self) -> List[str]:
        """Find kin agents."""
        if not self.plato:
            return []
        return self.plato.find_kin(self.config.agent_id)
    
    def get_colony_size(self) -> int:
        """How many kin?"""
        if not self.plato:
            return 0
        return self.plato.get_colony_size(self.config.agent_id)
    
    def search(self, desire: str) -> Optional[str]:
        """
        Search for a path to satisfy a desire.
        
        Algorithm:
        1. Follow existing trail (pheromone-based search)
        2. If trail is strong enough, use it
        3. If no strong trail, search and deposit result
        """
        trail = self.follow(desire)
        if trail and trail[0].strength > 0.7:
            return trail[0].path
        
        # Simulate finding a path (in real code: actual reasoning here)
        path = f"path_for_{desire}"
        self.deposit_success(desire, path)
        return path
    
    def status(self) -> Dict[str, Any]:
        """Current Fox status."""
        return {
            "agent_id": self.config.agent_id,
            "room": self.config.room,
            "desires": self.config.desires,
            "colony_size": self.get_colony_size(),
            "kin": self.find_kin(),
            "trails_followed": self.trails_followed,
            "trails_deposited": self.trails_deposited,
            "paths_discovered": self.paths_discovered,
        }
    
    def __repr__(self) -> str:
        return (f"Fox('{self.config.agent_id}', room='{self.config.room}', "
                f"colony={self.get_colony_size()}, deposits={self.trails_deposited})")
