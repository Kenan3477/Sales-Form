#!/usr/bin/env python3
"""
ASIS Type Definitions
Enhanced by True Self-Modification Engine
"""

from typing import Dict, List, Any, Optional, Union, Callable, Tuple, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

# Common ASIS types
ASISResponse = Dict[str, Any]
ASISConfig = Dict[str, Union[str, int, float, bool]]
ASISMetrics = Dict[str, float]

# Generic type variables
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

@dataclass
class ASISResult(Generic[T]):
    """Generic result container for ASIS operations"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ASISStatus(Enum):
    """ASIS system status enum"""
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PROCESSING = "processing"
    ERROR = "error"

class ASISProcessor(ABC):
    """Abstract base class for ASIS processors"""
    
    @abstractmethod
    async def process(self, data: Any) -> ASISResult[Any]:
        """Process data and return result"""
        pass
    
    @abstractmethod
    def get_status(self) -> ASISStatus:
        """Get current processor status"""
        pass

# Type aliases for common patterns
ASISCallback = Callable[[Any], None]
ASISAsyncCallback = Callable[[Any], Awaitable[None]]
ASISProcessor_T = TypeVar('ASISProcessor_T', bound=ASISProcessor)
