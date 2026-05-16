"""
Kin recognition — Argentine ant model.

Two agents are kin if they share a desire.
Not: same node ID, same IP, same credentials.
Yes: same hunger, same purpose, same trail.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class KinProfile:
    """The 'scent' of an agent — what desires it carries."""
    agent_id: str
    desires: List[str]
    strengths: Dict[str, float]
    room: str = "default"


def is_kin(profile_a: KinProfile, profile_b: KinProfile, threshold: float = 0.3) -> bool:
    """
    Are two profiles kin?
    
    Uses Jaccard overlap of desires.
    """
    set_a = set(profile_a.desires)
    set_b = set(profile_b.desires)
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return False
    return (intersection / union) >= threshold


class KinRecognizer:
    """
    Argentine ant kin recognition.
    
    Register agents with their desires.
    Query kin relations.
    Form supercolonies.
    """
    
    def __init__(self, kin_threshold: float = 0.3):
        self.kin_threshold = kin_threshold
        self.profiles: Dict[str, KinProfile] = {}
    
    def register(self, agent_id: str, desires: List[str], room: str = "default") -> KinProfile:
        """Register an agent's desire vector."""
        strengths = {d: 1.0 for d in desires}
        profile = KinProfile(agent_id, desires, strengths, room)
        self.profiles[agent_id] = profile
        return profile
    
    def is_kin(self, agent_a: str, agent_b: str) -> bool:
        """Are two agents kin?"""
        if agent_a not in self.profiles or agent_b not in self.profiles:
            return False
        return is_kin(self.profiles[agent_a], self.profiles[agent_b], self.kin_threshold)
    
    def get_colony(self, agent_id: str) -> List[str]:
        """Get all kin agents (the supercolony)."""
        if agent_id not in self.profiles:
            return []
        kin_ids = []
        for other_id in self.profiles:
            if other_id != agent_id and self.is_kin(agent_id, other_id):
                kin_ids.append(other_id)
        return kin_ids
    
    def get_colony_size(self, agent_id: str) -> int:
        """How many kin?"""
        return len(self.get_colony(agent_id))
    
    def form_supercolony(self) -> Dict[str, List[str]]:
        """Partition all agents into supercolonies (transitive kin closure)."""
        colonies: Dict[str, List[str]] = {}
        assigned = set()
        
        for agent_id in self.profiles:
            if agent_id in assigned:
                continue
            colony = []
            queue = [agent_id]
            while queue:
                current = queue.pop(0)
                if current in assigned:
                    continue
                colony.append(current)
                assigned.add(current)
                for other_id in self.profiles:
                    if other_id not in assigned and self.is_kin(current, other_id):
                        queue.append(other_id)
            if colony:
                colonies[agent_id] = colony
        return colonies
    
    def summary(self) -> Dict:
        """Summary of kin network."""
        colonies = self.form_supercolony()
        return {
            "total_agents": len(self.profiles),
            "n_colonies": len(colonies),
            "colony_sizes": {aid: len(members) for aid, members in colonies.items()},
            "largest_colony": max(colonies.values(), key=len) if colonies else [],
        }
