from fastapi.staticfiles import StaticFiles


class MountFiles(StaticFiles):
    """StaticFiles with fail-over"""

    async def get_response(self, path, scope):
        """Rewrite to / if 404"""
        try:
            response = await super().get_response(path, scope)
            if response.status_code != 404:
                return response
        except Exception:
            pass
        return await super().get_response("", scope)
