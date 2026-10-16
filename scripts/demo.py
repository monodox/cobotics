"""Quick, non-interactive demo of the cobotics stack against the simulator.

Run from the project root:
    python scripts/demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cobotics.ai.providers import StubBackend  # noqa: E402
from cobotics.control.planner import MotionPlanner  # noqa: E402
from cobotics.core.agent import Agent  # noqa: E402
from cobotics.hardware.simulator import build_simulator  # noqa: E402
from cobotics.perception.pipeline import PerceptionPipeline  # noqa: E402


def main() -> None:
    registry, world = build_simulator()
    agent = Agent(
        backend=StubBackend(),
        perception=PerceptionPipeline(registry),
        planner=MotionPlanner(registry),
    )

    print("Initial sensors:")
    for name, reading in agent.perception.perceive().readings.items():
        print(f"  {reading}")

    print("\nMoving to (3, 4)...")
    print(" ", agent.planner.move_to(3.0, 4.0))

    print("\nClosing gripper...")
    print(" ", agent.planner.grip("close"))

    print("\nSensors after move:")
    for name, reading in agent.perception.perceive().readings.items():
        print(f"  {reading}")

    print("\nChat:")
    print("  user> how do I move?")
    print("  cobotics>", agent.chat("how do I move?"))


if __name__ == "__main__":
    main()
