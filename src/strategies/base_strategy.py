from abc import ABC, abstractmethod
import numpy as np


class BasePickingStrategy(ABC):
    """Abstract base class for seismic data picking strategies.

    Methods:
        pick(data: np.ndarray) -> np.ndarray:
    """

    @abstractmethod
    def pick(self, data: np.ndarray) -> np.ndarray:
        """Abstract method to perform first-break picking on seismic data."""
