"""
test_mcp_light_server.py — Integration tests for Lightweight MemPalace MCP Server.
"""

import json
import pytest
from mempalace import mcp_light_server, mcp_server
from mempalace.palace_graph import invalidate_graph_cache


def _patch_light_server(monkeypatch, config, kg):
    """Patch mcp_server and mcp_light_server state for fixtures."""
    monkeypatch.setattr(mcp_server, "_config", config)
    monkeypatch.setattr(mcp_server, "_get_kg", lambda *a, **kw: kg)
    monkeypatch.setattr(mcp_server, "_taxonomy_cache", None)
    monkeypatch.setattr(mcp_server, "_taxonomy_cache_time", 0.0)
    monkeypatch.setattr(mcp_server, "_READ_ONLY", False)
    monkeypatch.setattr(mcp_server, "_vector_disabled", False)
    invalidate_graph_cache()


class TestLightMcpProtocol:
    def test_initialize(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-11-25"},
        }
        res = mcp_light_server.handle_light_request(req)
        assert res["id"] == 1
        assert res["result"]["serverInfo"]["name"] == "mempalace-light"
        assert "tools" in res["result"]["capabilities"]

    def test_tools_list_default(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        res = mcp_light_server.handle_light_request(req)
        assert res["id"] == 2
        tools = res["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert tool_names == ["palace_query", "palace_exec", "palace_coordinate"]

    def test_tools_list_read_only(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        monkeypatch.setattr(mcp_server, "_READ_ONLY", True)
        req = {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}
        res = mcp_light_server.handle_light_request(req)
        tools = res["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert tool_names == ["palace_query"]


class TestPalaceQuery:
    def test_status_query(self, monkeypatch, config, collection, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": "STATUS"},
        }
        res = mcp_light_server.handle_light_request(req)
        assert res["id"] == 10
        payload = json.loads(res["result"]["content"][0]["text"])
        assert "total_drawers" in payload or "wings" in payload

    def test_aaak_spec_query(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": "AAAK SPEC"},
        }
        res = mcp_light_server.handle_light_request(req)
        payload = json.loads(res["result"]["content"][0]["text"])
        assert "aaak_spec" in payload

    def test_taxonomy_and_wings(self, monkeypatch, config, seeded_collection, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {
            "jsonrpc": "2.0",
            "id": 12,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": "TAXONOMY"},
        }
        res = mcp_light_server.handle_light_request(req)
        payload = json.loads(res["result"]["content"][0]["text"])
        assert "taxonomy" in payload

    def test_kg_stats_query(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {
            "jsonrpc": "2.0",
            "id": 13,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": "KG STATS"},
        }
        res = mcp_light_server.handle_light_request(req)
        payload = json.loads(res["result"]["content"][0]["text"])
        assert "entities" in payload or "triples" in payload

    def test_check_dup_query(self, monkeypatch, config, collection, kg):
        _patch_light_server(monkeypatch, config, kg)
        req = {
            "jsonrpc": "2.0",
            "id": 14,
            "method": "tools/call",
            "params": {
                "name": "palace_query",
                "arguments": 'CHECK DUP "some memory content" THRESHOLD 0.85',
            },
        }
        res = mcp_light_server.handle_light_request(req)
        payload = json.loads(res["result"]["content"][0]["text"])
        assert "is_duplicate" in payload


class TestPalaceExec:
    def test_add_and_get_drawer(self, monkeypatch, config, collection, kg):
        _patch_light_server(monkeypatch, config, kg)
        # 1. Add drawer
        add_req = {
            "jsonrpc": "2.0",
            "id": 20,
            "method": "tools/call",
            "params": {
                "name": "palace_exec",
                "arguments": 'ADD IN test_wing/test_room "OAuth2 token rotation guide" SOURCE auth.md',
            },
        }
        res = mcp_light_server.handle_light_request(add_req)
        assert res["id"] == 20
        payload = json.loads(res["result"]["content"][0]["text"])
        assert payload.get("success") is True
        drawer_id = payload["drawer_id"]
        assert drawer_id

        # 2. Get drawer via palace_query
        get_req = {
            "jsonrpc": "2.0",
            "id": 21,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": f"DRAWER {drawer_id}"},
        }
        get_res = mcp_light_server.handle_light_request(get_req)
        get_payload = json.loads(get_res["result"]["content"][0]["text"])
        assert get_payload.get("drawer_id") == drawer_id
        assert get_payload.get("wing") == "test_wing"
        assert get_payload.get("room") == "test_room"
        assert "OAuth2 token rotation" in get_payload.get("content", "")

    def test_kg_add_and_query(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        # 1. KG ADD
        add_req = {
            "jsonrpc": "2.0",
            "id": 30,
            "method": "tools/call",
            "params": {
                "name": "palace_exec",
                "arguments": "KG ADD Arthur -> leads -> Camelot FROM 2026-01-01",
            },
        }
        res = mcp_light_server.handle_light_request(add_req)
        payload = json.loads(res["result"]["content"][0]["text"])
        assert payload.get("success") is True

        # 2. KG Query
        query_req = {
            "jsonrpc": "2.0",
            "id": 31,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": "KG Arthur"},
        }
        q_res = mcp_light_server.handle_light_request(query_req)
        q_payload = json.loads(q_res["result"]["content"][0]["text"])
        assert q_payload.get("entity") == "Arthur"
        facts = q_payload.get("facts", [])
        assert any(f.get("predicate") == "leads" and f.get("object") == "Camelot" for f in facts)

    def test_diary_write_and_read(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        # 1. Diary Write
        write_req = {
            "jsonrpc": "2.0",
            "id": 40,
            "method": "tools/call",
            "params": {
                "name": "palace_exec",
                "arguments": 'DIARY WRITE antigravity TOPIC proto "SESSION:built lightweight mcp prototype"',
            },
        }
        res = mcp_light_server.handle_light_request(write_req)
        payload = json.loads(res["result"]["content"][0]["text"])
        assert payload.get("success") is True

        # 2. Diary Read
        read_req = {
            "jsonrpc": "2.0",
            "id": 41,
            "method": "tools/call",
            "params": {"name": "palace_query", "arguments": "DIARY antigravity LAST 5"},
        }
        read_res = mcp_light_server.handle_light_request(read_req)
        read_payload = json.loads(read_res["result"]["content"][0]["text"])
        assert read_payload.get("agent") == "antigravity"
        assert len(read_payload.get("entries", [])) >= 1


class TestPalaceCoordinate:
    def test_task_create_and_event_list(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        cmd = (
            'TASK CREATE project:mempalace from:windows:antigravity:mempalace '
            'to:windows:claude:mempalace goal:"Implement PQL query engine" '
            'branch:feat/pql base:e4f5a6b7 done:"All unit tests pass"'
        )
        req = {
            "jsonrpc": "2.0",
            "id": 50,
            "method": "tools/call",
            "params": {"name": "palace_coordinate", "arguments": cmd},
        }
        res = mcp_light_server.handle_light_request(req)
        assert res["id"] == 50
        payload = json.loads(res["result"]["content"][0]["text"])
        assert payload.get("success") is True
        task_event = payload.get("task", {})
        assert task_event.get("type") == "task.request"

        # List events
        list_req = {
            "jsonrpc": "2.0",
            "id": 51,
            "method": "tools/call",
            "params": {
                "name": "palace_coordinate",
                "arguments": "EVENT LIST stream:project/mempalace limit:10",
            },
        }
        list_res = mcp_light_server.handle_light_request(list_req)
        list_payload = json.loads(list_res["result"]["content"][0]["text"])
        events = list_payload.get("events", [])
        assert len(events) >= 1

    def test_artifact_put_and_get(self, monkeypatch, config, kg):
        _patch_light_server(monkeypatch, config, kg)
        put_cmd = 'ARTIFACT PUT kind:note created_by:antigravity content:"Architecture decision record: PQL 3-tool triad"'
        put_req = {
            "jsonrpc": "2.0",
            "id": 60,
            "method": "tools/call",
            "params": {"name": "palace_coordinate", "arguments": put_cmd},
        }
        put_res = mcp_light_server.handle_light_request(put_req)
        put_payload = json.loads(put_res["result"]["content"][0]["text"])
        assert put_payload.get("success") is True
        art_id = put_payload["artifact"]["id"]

        get_req = {
            "jsonrpc": "2.0",
            "id": 61,
            "method": "tools/call",
            "params": {"name": "palace_coordinate", "arguments": f"ARTIFACT GET {art_id}"},
        }
        get_res = mcp_light_server.handle_light_request(get_req)
        get_payload = json.loads(get_res["result"]["content"][0]["text"])
        assert get_payload["artifact"]["content"] == "Architecture decision record: PQL 3-tool triad"
