from pydantic import BaseModel, ConfigDict, Extra
# from starlette.responses import Response

class Response(BaseModel):

    model_config = ConfigDict(
        extra='allow'
    )

