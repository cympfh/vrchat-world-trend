import requests
from typing import Any
import os


class VRCError(Exception):
    pass


class VRChat:
    """さくらサーバからだと認証が通らないっぽい"""

    USER_AGENT = "cympfh;mail@cympfh.cc"

    def __init__(self):
        auth_key = os.environ.get("VRCHAT_AUTH_KEY")
        assert auth_key, "Set ENV VRCHAT_AUTH_KEY"
        self.auth_key = auth_key

    def get(self, endpoint: str, params: dict[str, Any] | None = None):
        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
        }
        cookies = {"auth": self.auth_key}
        endpoint = endpoint.removeprefix("/")
        response = requests.get(
            f"https://api.vrchat.cloud/{endpoint}",
            headers=headers,
            cookies=cookies,
            params=params,
        )
        return response.json()

    def worlds(self, params: dict):
        """GET /api/1/worlds"""
        try:
            result = self.get("/api/1/worlds/active", params)
            if "error" in result:
                raise VRCError(result["error"])
            return result
        except Exception as err:
            raise VRCError(err)

    def world(self, world_id: str):
        """GET a World by ID"""
        try:
            result = self.get(f"/api/1/worlds/{world_id}")
            if "error" in result:
                raise VRCError(result["error"])
            return result
        except Exception as err:
            raise VRCError(err)
