"""Device registry — a central place to look devices up by name."""

from __future__ import annotations

from cobotics.hardware.base import Actuator, Device, Sensor
from cobotics.utils.errors import DeviceNotFoundError


class DeviceRegistry:
    """Holds references to all active devices."""

    def __init__(self) -> None:
        self._devices: dict[str, Device] = {}

    def register(self, device: Device) -> None:
        self._devices[device.name] = device

    def get(self, name: str) -> Device:
        try:
            return self._devices[name]
        except KeyError as exc:
            raise DeviceNotFoundError(f"No device named '{name}'") from exc

    def sensors(self) -> list[Sensor]:
        return [d for d in self._devices.values() if isinstance(d, Sensor)]

    def actuators(self) -> list[Actuator]:
        return [d for d in self._devices.values() if isinstance(d, Actuator)]

    def all(self) -> list[Device]:
        return list(self._devices.values())

    def names(self) -> list[str]:
        return list(self._devices.keys())
