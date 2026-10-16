from cobotics.hardware.simulator import build_simulator
from cobotics.perception.pipeline import PerceptionPipeline


def test_simulator_registers_devices():
    registry, _world = build_simulator()
    names = set(registry.names())
    assert {"position", "battery", "range", "drive", "gripper"} <= names


def test_drive_moves_robot():
    registry, world = build_simulator(start_position=(0.0, 0.0))
    drive = registry.get("drive")
    result = drive.actuate(x=3.0, y=4.0)
    assert result["to"] == (3.0, 4.0)
    assert world.position == [3.0, 4.0]
    assert result["distance"] == 5.0


def test_drive_clamps_to_bounds():
    registry, world = build_simulator(bounds=(5.0, 5.0))
    registry.get("drive").actuate(x=100.0, y=100.0)
    assert world.position == [5.0, 5.0]


def test_gripper_open_close():
    registry, world = build_simulator()
    gripper = registry.get("gripper")
    gripper.actuate(action="close")
    assert world.gripper_closed is True
    gripper.actuate(action="open")
    assert world.gripper_closed is False


def test_perception_reads_all_sensors():
    registry, _world = build_simulator()
    view = PerceptionPipeline(registry).perceive()
    assert "position" in view.readings
    assert "battery" in view.readings
