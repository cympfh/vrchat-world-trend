import vrchatapi
from vrchatapi.api import worlds_api
from vrchatapi.api.authentication_api import AuthenticationApi
from vrchatapi.models import LimitedWorld, TwoFactorEmailCode, World


class VRChat:
    def __init__(self, username: str, password: str):
        conf = vrchatapi.Configuration(
            username=username,
            password=password,
        )
        client = vrchatapi.ApiClient(conf)
        auth_api = AuthenticationApi(client)
        try:
            current_user = auth_api.get_current_user()
        except Exception as err:
            print(err)
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
        except Exception:
            return []

    def world(self, world_id: str) -> World | None:
        """GET /api/1/world/{world_id}"""
        try:
            world_api = worlds_api.WorldsApi(self.auth_api.api_client)
            return world_api.get_world(world_id)  # type: ignore
        except Exception:
            return None
