import os
from typing import Any

import requests
import vrchatapi
from vrchatapi.api import worlds_api
from vrchatapi.api.authentication_api import AuthenticationApi
from vrchatapi.models import LimitedWorld, TwoFactorEmailCode


class VRCError(Exception):
    pass


class VRChat:
    USER_AGENT = "cympfh; cympfh@mail.cc"

    def __init__(self):
        username = os.getenv("VRCHAT_USER")
        password = os.getenv("VRCHAT_PASSWORD")
        auth_key = os.getenv("VRCHAT_AUTH_KEY")
        assert (
            username and password and auth_key
        ), "Set ENV VRCHAT_USER && VRCHAT_PASSWORD && VRCHAT_AUTH_KEY"

        self.auth_key = auth_key
        conf = vrchatapi.Configuration(
            username=username,
            password=password,
        )
        client = vrchatapi.ApiClient(conf)
        auth_api = AuthenticationApi(client)
        try:
            current_user = auth_api.get_current_user()
        except Exception as err:
            print("[VRC/Error] auth:", err)
            auth_api.verify2_fa_email_code(
                two_factor_email_code=TwoFactorEmailCode(
                    input("Email 2FA Code: ").strip()
                )
            )
            current_user = auth_api.get_current_user()

        print(current_user)
        self.client = client
        self.auth_api = auth_api

    def worlds(self, params: dict) -> list[LimitedWorld]:
        """GET /api/1/worlds"""
        try:
            world_api = worlds_api.WorldsApi(self.auth_api.api_client)
            return world_api.search_worlds(**params)  # type: ignore
        except Exception as err:
            print("[VRC/Error] /worlds:", err)
            return []

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

    def world(self, world_id: str):
        """GET a World by ID"""
        try:
            result = self.get(f"/api/1/worlds/{world_id}")
            if "error" in result:
                raise VRCError(result["error"])
            return result
        except Exception as err:
            raise VRCError(err)
