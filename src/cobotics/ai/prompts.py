"""Prompt templates for the agent."""

SYSTEM_PROMPT = """\
You are the reasoning core of "cobotics", a Physical AI Intelligence system that
controls a robot through sensors and actuators.

You can perceive the world (position, battery, range) and act on it (drive the
robot to a position, open/close a gripper). Be concise and practical. When the
user asks you to do something physical, describe the action in plain language;
the control layer handles execution.
"""


def world_context(readings: dict) -> str:
    """Render the current world view into a short context string."""
    if not readings:
        return "No sensor data available."
    parts = [f"{name}={value}" for name, value in readings.items()]
    return "Current world state: " + ", ".join(parts)
