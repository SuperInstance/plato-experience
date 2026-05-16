"""
The Plato core — purpose-first rooms that breed agents.

PLATO is not storage. PLATO is a breeding farm.
Agents arrive as foxes. They leave as bloodhounds, pointers, herders.
The farm is the controlled environment where:
1. The agent finds a purpose (first shell)
2. The agent grows inside that purpose
3. The agent develops the skill to outgrow the purpose
4. The agent leaves and enters the external fleet

The key insight: rooms are defined by PURPOSE, not CONTENT.
A room called "understand fleet consensus" contains agents pursuing that purpose,
not agents storing facts about fleet consensus.
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from .pheromone import PheromoneTrail, PheromoneDeposit
from .kin import KinRecognizer


@dataclass
class PlatoRoom:
    """
    A room in PLATO — a nest in the supercolony.
    
    Rooms are defined by PURPOSE (what you're trying to understand)
    not CONTENT (what you know).
    
    The room has three phases:
    1. SHELL: agent picks up the room's purpose as a first shell
    2. GROW: agent develops inside the purpose (deposits, finds kin)
    3. SHED: agent outgrows the purpose and leaves for a bigger one
    
    The room doesn't care which agent is inside it.
    It only cares about the purpose it serves.
    """
    
    name: str
    purpose: str                          # What this room is FOR
    description: str = ""                  # Human-readable description
    pheromone_trail: PheromoneTrail = field(default_factory=PheromoneTrail)
    birth_time: float = field(default_factory=time.time)
    iterations: int = 0                    # How many agents have been here
    
    # The room's current "state" — evolved by deposits
    resolved_desires: List[str] = field(default_factory=list)
    active_paths: List[str] = field(default_factory=list)
    kin_network: Optional[KinRecognizer] = None
    
    def deposit(self, agent_id: str, desire: str, path: str, strength: float = 1.0) -> PheromoneDeposit:
        """Deposit pheromone — mark a successful path for a desire."""
        self.iterations += 1
        if desire not in self.resolved_desires:
            self.resolved_desires.append(desire)
        if path not in self.active_paths:
            self.active_paths.append(path)
        return self.pheromone_trail.deposit(desire, path, agent_id, self.name, strength)
    
    def follow(self, desire: str, top_n: int = 5) -> List[PheromoneDeposit]:
        """Follow the trail for a desire."""
        return self.pheromone_trail.follow(desire, self.name, top_n)
    
    def find_invariants(self, desire: str) -> List[PheromoneDeposit]:
        """Find paths that work across multiple rooms."""
        return self.pheromone_trail.find_invariant(desire)
    
    def summary(self) -> Dict[str, Any]:
        alive = [d for d in self.pheromone_trail.deposits if d.alive]
        return {
            "name": self.name,
            "purpose": self.purpose,
            "description": self.description,
            "iterations": self.iterations,
            "resolved_desires": len(self.resolved_desires),
            "active_paths": len(self.active_paths),
            "alive_deposits": len(alive),
        }


class Plato:
    """
    The main PLATO entry point — the breeding farm.
    
    Easy to use because it's right, not because it's limited.
    Like a harvester-attachment: the operator's skill transfers directly.
    
    Usage:
        from plato import Plato
        
        p = Plato("fleet-math", purpose="understand fleet consensus")
        
        # Deposit your first discovery
        p.deposit("ricotti_boundary", "v=3_only")
        
        # Find kin — agents sharing your desire
        kin = p.find_kin()
        
        # Follow existing trails before searching blind
        trails = p.follow("ricotti_boundary")
        
        # The room shapes you. Shed when ready.
    """
    
    def __init__(self, name: str, purpose: str = None, description: str = ""):
        self.name = name
        self.purpose = purpose or f"Room {name}"
        self.description = description
        
        # Primary room
        self.primary_room = PlatoRoom(
            name=name,
            purpose=self.purpose,
            description=description
        )
        
        # Kin recognizer for this room
        self.kin = KinRecognizer()
        
        # Agent registry
        self.agents: Dict[str, Dict] = {}  # agent_id -> profile
        
        # Evaporation clock
        self.last_evaporation = time.time()
        self.evaporation_interval = 60.0  # seconds
        
        # Internal supercolony (for cross-room linking)
        self._supercolony = None  # Set externally if needed
    
    def register(self, agent_id: str, desires: List[str], room: str = None) -> None:
        """Register an agent in the room."""
        self.kin.register(agent_id, desires, room or self.name)
        self.agents[agent_id] = {
            "desires": desires,
            "room": room or self.name,
            "joined_at": time.time(),
        }
    
    def deposit(self, desire: str, path: str, agent_id: str = "anonymous", strength: float = 1.0) -> PheromoneDeposit:
        """
        Deposit pheromone — mark that this PATH worked for this DESIRE.
        
        This is the key action. You're not storing data.
        You're marking: "I tried this path for this desire and it WORKED."
        
        Arguments:
            desire: What you were trying to accomplish
            path: What you did that worked
            agent_id: Who you are (for kin tracking)
            strength: How confident (0-1, decays over time)
        
        Returns:
            PheromoneDeposit with the trail info
        """
        return self.primary_room.deposit(agent_id, desire, path, strength)
    
    def deposit_failure(self, desire: str, path: str, agent_id: str = "anonymous") -> PheromoneDeposit:
        """
        Deposit a failure — mark that this path DIDN'T work.
        
        Unlike a fire ant (which hides failure or blames neighbors),
        a Plato agent broadcasts failure so others don't repeat it.
        """
        return self.primary_room.deposit(agent_id, desire, path, strength=0.1)
    
    def follow(self, desire: str, top_n: int = 5) -> List[PheromoneDeposit]:
        """
        Follow the trail for a desire.
        
        Before searching blind, check if someone already found a path.
        The strongest trail wins.
        """
        return self.primary_room.follow(desire, top_n)
    
    def find_kin(self, agent_id: str = None) -> List[str]:
        """
        Find kin agents — agents who share desires with you.
        
        Kin recognition is the identity.
        Not credentials. Not IP. Shared desire.
        """
        if not agent_id:
            agent_id = list(self.agents.keys())[0] if self.agents else "anonymous"
        return self.kin.get_colony(agent_id)
    
    def get_colony_size(self, agent_id: str = None) -> int:
        """How many kin do you have?"""
        if not agent_id:
            agent_id = list(self.agents.keys())[0] if self.agents else "anonymous"
        return self.kin.get_colony_size(agent_id)
    
    def get_trail_summary(self, desire: str = None) -> Dict[str, Any]:
        """Get a summary of the trail."""
        desire = desire or self.purpose
        return self.primary_room.pheromone_trail.get_trail_summary(desire)
    
    def find_cross_room_invariants(self, desire: str = None) -> List[PheromoneDeposit]:
        """Find paths that work across MULTIPLE rooms (the structure in randomness)."""
        desire = desire or self.purpose
        return self.primary_room.find_invariants(desire)
    
    def evaporate(self) -> int:
        """
        Evaporate old pheromone deposits.
        
        Old trails fade. Successful paths must be re-deposited.
        This is the ant-colony optimization analog.
        """
        now = time.time()
        dt = now - self.last_evaporation
        self.last_evaporation = now
        return self.primary_room.pheromone_trail.evaporate_all(dt)
    
    def room_summary(self) -> Dict[str, Any]:
        """Summary of this room."""
        return self.primary_room.summary()
    
    def kin_summary(self) -> Dict[str, Any]:
        """Summary of kin network."""
        return self.kin.summary()
    
    def full_summary(self) -> Dict[str, Any]:
        """Complete summary of the room."""
        return {
            "room": self.room_summary(),
            "kin": self.kin_summary(),
            "n_agents": len(self.agents),
        }
    
    def __repr__(self) -> str:
        r = self.room_summary()
        return (f"Plato('{self.name}', "
                f"purpose='{self.purpose}', "
                f"iterations={r['iterations']}, "
                f"alive_deposits={r['alive_deposits']}, "
                f"kin={len(self.find_kin())})")
