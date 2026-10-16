"""Control: translate high-level intents into actuator commands."""

from __future__ import annotations

from typing import Any

from cobotics.hardware.registry import DeviceRegistry
from cobotics.utils.errors import DeviceNotFoundError
from cobotics.utils.logging import get_logger

log = get_logger("control")


class MotionPlanner:
    """Maps intents onto registered actuators.

    Kept deliberately simple: the simulator teleports to the target. Swap in
    real path planning / kinematics here for physical hardware.
    """

    def __init__(self, registry: DeviceRegistry) -> None:
        self._registry = registry

    @property
    def registry(self) -> DeviceRegistry:
        return self._registry

    def move_to(self, x: float, y: float) -> dict[str, Any]:
        drive = self._registry.get("drive")
        log.debug("move_to %.3f, %.3f", x, y)
        return drive.actuate(x=x, y=y)  # type: ignore[attr-defined]

    def grip(self, action: str) -> dict[str, Any]:
        gripper = self._registry.get("gripper")
        log.debug("grip %s", action)
        return gripper.actuate(action=action)  # type: ignore[attr-defined]

    def has(self, actuator: str) -> bool:
        try:
            self._registry.get(actuator)
            return True
        except DeviceNotFoundError:
            return False
