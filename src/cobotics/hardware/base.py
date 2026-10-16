"""Abstract hardware interfaces.

These abstractions let the rest of the system talk to devices without caring
whether they are simulated or real. Implement these for a real robot and
register them in place of the simulator classes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class DeviceKind(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"


@dataclass
class Reading:
    """A single sensor reading."""

    sensor: str
    value: Any
    unit: str = ""

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        unit = f" {self.unit}" if self.unit else ""
        return f"{self.sensor}: {self.value}{unit}"


class Device(ABC):
    """Base class for any physical (or simulated) device."""

    kind: DeviceKind

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def status(self) -> dict[str, Any]:
        """Return a dict describing the device's current state."""


class Sensor(Device):
    """A device that produces readings."""

    kind = DeviceKind.SENSOR

    @abstractmethod
    def read(self) -> Reading:
        """Take a single reading."""


class Actuator(Device):
    """A device that performs actions in the world."""

    kind = DeviceKind.ACTUATOR

    @abstractmethod
    def actuate(self, **kwargs: Any) -> dict[str, Any]:
        """Perform an action; return a result dict."""
