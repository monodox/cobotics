import pytest

from cobotics.ai.providers import StubBackend, build_backend
from cobotics.config.settings import Settings
from cobotics.utils.errors import AIBackendError


def test_build_backend_defaults_to_stub():
    backend = build_backend(Settings(ai_backend="stub"))
    assert isinstance(backend, StubBackend)


def test_build_backend_unknown_raises():
    with pytest.raises(AIBackendError):
        build_backend(Settings(ai_backend="does-not-exist"))


def test_nebius_backend_requires_key(monkeypatch):
    # Ensure no key leaks in from the real environment / .env.
    monkeypatch.delenv("NEBIUS_API_KEY", raising=False)
    # No NEBIUS_API_KEY -> construction must fail, without any network call.
    settings = Settings(ai_backend="nebius", nebius_api_key=None, _env_file=None)
    with pytest.raises(AIBackendError):
        build_backend(settings)


def test_stub_backend_is_offline_and_deterministic():
    from cobotics.ai.base import Message

    backend = StubBackend()
    reply = backend.complete([Message("user", "hello")])
    assert isinstance(reply, str) and reply
