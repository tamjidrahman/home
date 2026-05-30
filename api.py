import os
import inspect
from pathlib import Path
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
import toml
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from homeassistant import client
from homeassistant.commandable import CommandableGroup
from homeassistant.door import Door
from homeassistant.light import Light, LightGroup
from homeassistant.speaker import Speaker, SpeakerGroup
from homeassistant.thermostat import Thermostat
from homeassistant.vacuum import Vacuum


class StripApiPrefixMiddleware(BaseHTTPMiddleware):
    # Tailscale serve forwards the full path to the backend, so requests sent to
    # https://home.tail2318fb.ts.net/api/foo arrive here as /api/foo. Strip it
    # so existing routes (mounted at /) still match.
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path == "/api" or path.startswith("/api/"):
            new_path = path[len("/api"):] or "/"
            request.scope["path"] = new_path
            request.scope["raw_path"] = new_path.encode()
        return await call_next(request)


class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Schema + docs are public — /openapi.json already exposes the full
        # surface, so locking the rendered UIs adds no security.
        if request.url.path in ("/health", "/openapi.json", "/docs", "/redoc"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header with Bearer token required"}
            )

        # Set token for downstream use
        token = auth_header[7:]
        client.set_token(token)

        return await call_next(request)


app = FastAPI()
app.add_middleware(TokenAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL (Next.js dev server)
    allow_credentials=False,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc)
    allow_headers=["*"],  # Allow all headers (e.g. Authorization, Content-Type)
)
# Added last so it runs first (outermost) — must strip /api before routing/auth.
app.add_middleware(StripApiPrefixMiddleware)


@app.get("/health")
def health():
    return {"status": "ok"}


def load_config():
    config_file = os.getenv("HOME_CONFIG_PATH", Path.home() / ".config/home/config.toml")
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    return toml.load(config_path)


config = load_config()


from makefun import create_function, with_signature

_TYPE_MAP = {int: "number", float: "number", bool: "boolean", str: "string"}


def _describe_params(cmd):
    params = []
    for name, param in inspect.signature(cmd).parameters.items():
        if name == "self":
            continue
        type_str = _TYPE_MAP.get(param.annotation, "string")
        default = param.default if param.default is not inspect.Parameter.empty else None
        params.append({"name": name, "type": type_str, "default": default})
    return params


def register_routes(entity_name: str, devices, app: FastAPI):
    device_lookup = {device.name: device for device in devices}
    commands = [cmd for cmd in devices[0].get_commands()]  # assume uniform

    @app.get(f"/{entity_name}/commands", tags=[entity_name])
    def get_commands():
        return [{"name": cmd.__name__, "params": _describe_params(cmd)} for cmd in commands]

    for cmd in commands:
        cmd_name = cmd.__name__
        route = f"/{entity_name}/{cmd_name}"
        sig = inspect.signature(cmd)

        parameters = [
            inspect.Parameter(
                name="names",
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=Query(None, alias=entity_name),
                annotation=list[str] | None,
            )
        ]

        for name, param in sig.parameters.items():
            if name == "self":
                continue
            annotation = param.annotation if param.annotation is not inspect.Parameter.empty else str
            default = param.default if param.default is not inspect.Parameter.empty else ...
            parameters.append(
                inspect.Parameter(
                    name=name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    default=Query(default),
                    annotation=annotation,
                )
            )

        new_sig = inspect.Signature(parameters)

        def make_logic(cmd):
            def logic(**kwargs):
                selected_names = kwargs.pop("names", None)
                selected = (
                    [device_lookup[name] for name in selected_names if name in device_lookup]
                    if selected_names else device_lookup.values()
                )
                result = {}
                for device in selected:
                    method = getattr(device, cmd.__name__)
                    result[device.name] = method(**kwargs)
                return result
            return logic

        logic_fn = make_logic(cmd)

        # ✅ Wrap with FastAPI-compatible signature
        handler = with_signature(new_sig)(logic_fn)

        method = app.get if cmd_name == "status" else app.post
        method(route, tags=[entity_name])(handler)

""" Lights """
lights = [Light(light["entity_id"], light["automation"]) for light in config["lights"]]
register_routes("light", lights, app)

""" Speakers """
speakers = [Speaker(s["entity_id"]) for s in config["speakers"]]
register_routes("speaker", speakers, app)

""" Thermostat """
thermostats = [Thermostat(config["thermostat"]["entity_id"])]
register_routes("thermostat", thermostats, app)

""" Vacuum """
vacuums = [Vacuum(config["vacuum"]["entity_id"])]
register_routes("vacuum", vacuums, app)

""" Doors """
doors = [Door(d["entity_id"], lock_id=d.get("lock_id")) for d in config["doors"]]
register_routes("door", doors, app)
