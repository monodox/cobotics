"""Real-hardware actuator stubs.

Mirror the simulator actuators. Implement actuate() with real driver calls when
connecting cobotics to physical hardware.
"""

from __future__ import annotations

from typing import Any

from cobotics.hardware.base import Actuator


class RealActuator(Actuator):
    """Placeholder for a real actuator driver."""

    def __init__(self, name: str, driver: Any = None) -> None:
        super().__init__(name)
        self._driver = driver

    def actuate(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError(
            "Connect a real driver and implement actuate() for this actuator."
        )

    def status(self) -> dict[str, Any]:
        return {"name": self.name, "driver": repr(self._driver)}
