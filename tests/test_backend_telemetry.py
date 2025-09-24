import asyncio
import json
import os
from pathlib import Path

import pytest
from fastapi import BackgroundTasks
from starlette.requests import Request


os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")


import backend.server as server  # noqa: E402


@pytest.fixture()
def telemetry_env(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "ROOT_DIR", Path(tmp_path))
    return tmp_path


async def _run_background_tasks(bg: BackgroundTasks):
    for task in bg.tasks:
        await task()


def _make_request(user_agent: str = "pytest") -> Request:
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/api/log",
        "headers": [(b"user-agent", user_agent.encode("utf-8"))],
    }
    return Request(scope)


def test_log_accepts_monetization_events(telemetry_env):
    payload = server.LogPayload(
        events=[
            server.TelemetryEvent(event="paywall_view", type="card_of_day"),
            server.TelemetryEvent(event="purchase_start", type="premium_monthly"),
            server.TelemetryEvent(event="purchase_success", type="premium_monthly"),
            server.TelemetryEvent(event="purchase_fail", type="premium_annual"),
            server.TelemetryEvent(event="restore_success"),
            server.TelemetryEvent(event="share_click", type="card_of_day"),
        ]
    )

    bg = BackgroundTasks()

    async def _execute():
        response = await server.log_events(payload, _make_request(), bg)
        await _run_background_tasks(bg)
        return response

    response = asyncio.run(_execute())
    assert response.status_code == 204

    logs_dir = Path(telemetry_env) / "logs"
    files = list(logs_dir.glob("telemetry-*.jsonl"))
    assert files, "Expected telemetry log file to be created"

    content = files[0].read_text(encoding="utf-8").strip().splitlines()
    if content:
        logged_events = {json.loads(line)["event"] for line in content}
        expected_events = {event.event for event in payload.events}
        assert logged_events.issubset(expected_events)


def test_log_rejects_unknown_event_payload():
    with pytest.raises(Exception):
        server.LogPayload.model_validate({"events": [{"event": "not_a_valid_event"}]})

