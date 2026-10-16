"""Perception: turn raw sensor readings into a consolidated world view."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cobotics.hardware.base import Reading
from cobotics.hardware.registry import DeviceRegistry


@dataclass
class WorldView:
    """A snapshot of what the system currently perceives."""

    readings: dict[str, Reading] = field(default_factory=dict)

    def get(self, sensor: str) -> Any:
        reading = self.readings.get(sensor)
        return reading.value if reading else None

    def as_dict(self) -> dict[str, Any]:
        return {name: r.value for name, r in self.readings.items()}


class PerceptionPipeline:
    """Reads all sensors and assembles a WorldView."""

    def __init__(self, registry: DeviceRegistry) -> None:
        self._registry = registry

    def perceive(self) -> WorldView:
        view = WorldView()
        for sensor in self._registry.sensors():
            view.readings[sensor.name] = sensor.read()
        return view
