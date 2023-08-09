# FastSvelte = FastAPI + Svelte

A Template for Single-page App using [FastAPI](https://fastapi.tiangolo.com/) + [Svelte](https://svelte.dev/)

## Why?

- [FastAPI](https://fastapi.tiangolo.com/)
    - Typed & Fast Way to build a API Server using Python
- [Svelte](https://svelte.dev/)
    - Fast & Easy to Modern Front-end
    - and supporting TypeScript!

## Start up Sample Project

Clone this, then

```bash
# on local
make build
make serve
```

```bash
# on docker
make build-docker
make serve-docker
```

And open `localhost:8080`.

## Development

### Server Side (Python/FastAPI)

Check `./server.py`

```python
# Define API functions
@app.get("/api/greeting")
def greeting(name: Optional[str] = None):
    """Greeting you"""
    if name:
        return {"msg": f"Hello {name}!"}
    return {"msg": "Hi!"}

# URLs other than APIs are
# - static files under `web/public` if exists
#    - /aaa/bbb -> `./web/public/aaa/bbb`
# - Returns `web/public/index.html` else
#    - SPA on Front-end side
app.mount("/", MountFiles(directory="web/public", html=True), name="static")
```

Use `make dev` to enable hot-reloading.

### Front-end Side (TypeScript/Svelte)

cd `web/` and check `src/App.svelte`.

Use `make dev` to enable hot-reloading.
