from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Rocket:
    id: str
    name: str
    
    @classmethod
    def from_api(cls, data: dict):
        return cls(id=data['id'], name=data['name'])

@dataclass
class Launchpad:
    id: str
    name: str
    locality: Optional[str]
    
    @classmethod
    def from_api(cls, data: dict):
        return cls(id=data['id'], name=data['name'], locality=data.get('locality'))

@dataclass
class Launch:
    id: str
    name: str
    date_utc: str
    rocket: str
    launchpad: str
    success: Optional[bool]
    
    @classmethod
    def from_api(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            date_utc=data['date_utc'],
            rocket=data['rocket'],
            launchpad=data['launchpad'],
            success=data.get('success')
        ) 