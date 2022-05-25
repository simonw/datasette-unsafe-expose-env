from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_env(monkeypatch):
    monkeypatch.setenv("FOO", "foo")
    monkeypatch.setenv("BAR", "bar")
    monkeypatch.setenv("BAR", "bar")
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/env")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "FOO=foo" in response.text
    assert "BAR=bar" in response.text


@pytest.mark.asyncio
async def test_default_redaction(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "secret")
    monkeypatch.setenv("GPG_KEY", "secret")
    monkeypatch.setenv("DATASETTE_SECRET", "secret")
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/env")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "DATABASE_URL=***" in response.text
    assert "GPG_KEY=***" in response.text
    assert "DATASETTE_SECRET=***" in response.text


@pytest.mark.asyncio
async def test_custom_redaction(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "not-secret")
    monkeypatch.setenv("GPG_KEY", "not-secret")
    monkeypatch.setenv("DATASETTE_SECRET", "secret")
    monkeypatch.setenv("EXTRA", "secret")
    datasette = Datasette(
        [],
        memory=True,
        metadata={
            "plugins": {
                "datasette-unsafe-expose-env": {"redact": {"DATASETTE_SECRET", "EXTRA"}}
            }
        },
    )
    response = await datasette.client.get("/-/env")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "DATABASE_URL=not-secret" in response.text
    assert "GPG_KEY=not-secret" in response.text
    assert "DATASETTE_SECRET=***" in response.text
    assert "EXTRA=***" in response.text
