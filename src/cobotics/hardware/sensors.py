"""Real-hardware sensor stubs.

Fill these in with actual driver calls (serial, ROS, GPIO, etc.) when wiring
cobotics to physical devices. They mirror the simulator sensors so the rest of
the system does not change.
"""

from __future__ import annotations

from typing import Any

from cobotics.hardware.base import Reading, Sensor


class RealSensor(Sensor):
    """Placeholder for a real sensor driver."""

    def __init__(self, name: str, driver: Any = None) -> None:
        super().__init__(name)
        self._driver = driver

    def read(self) -> Reading:
        raise NotImplementedError(
            "Connect a real driver and implement read() for this sensor."
        )

    def status(self) -> dict[str, Any]:
        return {"name": self.name, "driver": repr(self._driver)}
