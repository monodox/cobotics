from cobotics.ai.providers import StubBackend
from cobotics.control.planner import MotionPlanner
from cobotics.core.agent import Agent
from cobotics.hardware.simulator import build_simulator
from cobotics.perception.pipeline import PerceptionPipeline


def _make_agent() -> Agent:
    registry, _world = build_simulator()
    return Agent(
        backend=StubBackend(),
        perception=PerceptionPipeline(registry),
        planner=MotionPlanner(registry),
    )


def test_agent_chat_returns_text():
    agent = _make_agent()
    reply = agent.chat("hello")
    assert isinstance(reply, str)
    assert reply


def test_agent_records_history():
    agent = _make_agent()
    agent.chat("hi there")
    roles = [m.role for m in agent.session.messages()]
    assert "system" in roles
    assert "user" in roles
    assert "assistant" in roles


def test_planner_move_through_agent():
    agent = _make_agent()
    result = agent.planner.move_to(2.0, 0.0)
    assert result["to"] == (2.0, 0.0)
