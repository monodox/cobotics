"""Domain-specific exceptions for cobotics."""


class CoboticsError(Exception):
    """Base class for all cobotics errors."""


class DeviceError(CoboticsError):
    """Raised when a hardware device fails or is misused."""


class DeviceNotFoundError(DeviceError):
    """Raised when a requested device is not registered."""


class CommandError(CoboticsError):
    """Raised when a shell command cannot be parsed or executed."""


class AIBackendError(CoboticsError):
    """Raised when the AI backend fails or is misconfigured."""
