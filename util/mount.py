from fastapi.staticfiles import StaticFiles


class MountFiles(StaticFiles):
    """StaticFiles with fail-over"""

    async def get_response(self, path, scope):
        """Rewrite to / if 404"""
        response = await super().get_response(path, scope)
        if response.status_code != 404:
            return response
        return await super().get_response("", scope)
