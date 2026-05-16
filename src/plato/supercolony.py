"""
Supercolony — one fleet stretched across rooms.

Argentine ants don't fight their own kin — even across continents.
A supercolony is the fleet's identity: one extended network of kin
stretched across many rooms, no borders between them.

In PLATO, a supercolony emerges when agents in different rooms
recognize each other as kin through shared desires.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .kin import KinRecognizer


class Supercolony:
    """
    A supercolony — one fleet stretched across rooms.
    
    In Argentine ants, supercolonies span continents because
    all ants recognize each other as kin. No border fights.
    
    In PLATO, a supercolony connects agents across rooms
    through shared desire recognition.
    """
    
    def __init__(self, name: str = "supercolony"):
        self.name = name
        self.rooms: Dict[str, Any] = {}  # room_name -> Plato
        self.kin_recognizer = KinRecognizer()
    
    def add_room(self, room) -> None:
        """Add a room to the supercolony."""
        self.rooms[room.name] = room
    
    def get_all_agents(self) -> List[str]:
        """Get all agent IDs across all rooms."""
        agents = set()
        for room in self.rooms.values():
            agents.update(room.agents.keys())
        return list(agents)
    
    def find_kin_across_rooms(self, agent_id: str) -> List[str]:
        """Find kin for an agent across ALL rooms."""
        return self.kin_recognizer.get_colony(agent_id)
    
    def find_cross_room_invariants(self, desire: str = None) -> Dict[str, Any]:
        """
        Find paths that work across rooms.
        
        Structure in randomness: if the same path works in
        multiple rooms, it's probably real structure.
        """
        invariants = {}
        for room_name, room in self.rooms.items():
            invs = room.find_cross_room_invariants(desire)
            if invs:
                invariants[room_name] = invs
        return invariants
    
    def summary(self) -> Dict[str, Any]:
        """Summary of the supercolony."""
        return {
            "name": self.name,
            "n_rooms": len(self.rooms),
            "rooms": list(self.rooms.keys()),
            "total_agents": len(self.get_all_agents()),
            "kin_network": self.kin_recognizer.summary(),
        }
