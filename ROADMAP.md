# Roadmap

A rough, non-binding plan for where Cobotics is headed. Priorities may shift;
feedback and contributions are welcome (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Near term

- Real-hardware drivers behind the existing `Sensor`/`Actuator` abstractions
  (serial / GPIO / ROS examples).
- Streaming responses from the Nebius/Nemotron backend for lower latency.
- Tool/function-calling so the AI agent can invoke actuators directly from
  natural language, not just suggest commands.
- Richer `/status` output and a persistent command history across sessions.

## Mid term

- Pluggable perception modules (camera/lidar adapters) feeding the world view.
- Scriptable task sequences (run a list of commands from a file).
- Configurable world/robot definitions loaded from YAML.
- Expanded test coverage, including a fake backend for exercising the agent loop.

## Longer term

- Multi-robot coordination through the agent runtime.
- Simulation of obstacles and path planning in the motion planner.
- Optional web/TUI front end on top of the same core.

## Non-goals (for now)

- Becoming a full robotics framework (ROS already exists); Cobotics stays a thin,
  AI-driven control/reasoning layer that integrates with such frameworks.
