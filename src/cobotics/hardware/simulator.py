"""Simulated hardware so cobotics runs with no physical devices.

The simulator keeps a shared `WorldState` and exposes sensors and actuators
that read from / write to it.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any

from cobotics.hardware.base import Actuator, Reading, Sensor
from cobotics.hardware.registry import DeviceRegistry


@dataclass
class WorldState:
    """Mutable state of the simulated world."""

    bounds: tuple[float, float] = (10.0, 10.0)
    position: list[float] = field(default_factory=lambda: [0.0, 0.0])
    heading: float = 0.0           # radians
    gripper_closed: bool = False
    battery: float = 100.0         # percent

    def clamp(self) -> None:
        self.position[0] = max(0.0, min(self.bounds[0], self.position[0]))
        self.position[1] = max(0.0, min(self.bounds[1], self.position[1]))


class PositionSensor(Sensor):
    def __init__(self, world: WorldState, name: str = "position") -> None:
        super().__init__(name)
        self._world = world

    def read(self) -> Reading:
        x, y = self._world.position
        return Reading(self.name, (round(x, 3), round(y, 3)), "m")

    def status(self) -> dict[str, Any]:
        return {"name": self.name, "position": self._world.position}


class BatterySensor(Sensor):
    def __init__(self, world: WorldState, name: str = "battery") -> None:
        super().__init__(name)
        self._world = world

    def read(self) -> Reading:
        return Reading(self.name, round(self._world.battery, 1), "%")

    def status(self) -> dict[str, Any]:
        return {"name": self.name, "battery": self._world.battery}


class RangeSensor(Sensor):
    """Fake proximity sensor: distance to the nearest world bound."""

    def __init__(self, world: WorldState, name: str = "range") -> None:
        super().__init__(name)
        self._world = world

    def read(self) -> Reading:
        x, y = self._world.position
        bx, by = self._world.bounds
        nearest = min(x, y, bx - x, by - y)
        noisy = max(0.0, nearest + random.uniform(-0.05, 0.05))
        return Reading(self.name, round(noisy, 3), "m")

    def status(self) -> dict[str, Any]:
        return {"name": self.name}


class DriveActuator(Actuator):
    """Moves the robot toward a target position."""

    def __init__(self, world: WorldState, speed: float = 1.0, name: str = "drive") -> None:
        super().__init__(name)
        self._world = world
        self._speed = speed

    def actuate(self, *, x: float, y: float, **_: Any) -> dict[str, Any]:
        start = tuple(self._world.position)
        dx = x - self._world.position[0]
        dy = y - self._world.position[1]
        dist = math.hypot(dx, dy)

        self._world.heading = math.atan2(dy, dx) if dist else self._world.heading
        self._world.position = [x, y]
        self._world.clamp()
        self._world.battery = max(0.0, self._world.battery - dist * 0.5)

        return {
            "from": start,
            "to": tuple(self._world.position),
            "distance": round(dist, 3),
            "battery": round(self._world.battery, 1),
        }

    def status(self) -> dict[str, Any]:
        return {"name": self.name, "speed": self._speed}


class GripperActuator(Actuator):
    def __init__(self, world: WorldState, name: str = "gripper") -> None:
        super().__init__(name)
        self._world = world

    def actuate(self, *, action: str, **_: Any) -> dict[str, Any]:
        action = action.lower()
        if action not in {"open", "close"}:
            raise ValueError("gripper action must be 'open' or 'close'")
        self._world.gripper_closed = action == "close"
        return {"gripper": "closed" if self._world.gripper_closed else "open"}

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "state": "closed" if self._world.gripper_closed else "open",
        }


def build_simulator(
    bounds: tuple[float, float] = (10.0, 10.0),
    start_position: tuple[float, float] = (0.0, 0.0),
    move_speed: float = 1.0,
) -> tuple[DeviceRegistry, WorldState]:
    """Create a world + registry populated with simulated devices."""
    world = WorldState(bounds=bounds, position=list(start_position))
    registry = DeviceRegistry()

    registry.register(PositionSensor(world))
    registry.register(BatterySensor(world))
    registry.register(RangeSensor(world))
    registry.register(DriveActuator(world, speed=move_speed))
    registry.register(GripperActuator(world))

    return registry, world
