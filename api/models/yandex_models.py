from pydantic import BaseModel, ConfigDict, Field


class BaseYandexModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class LinkResponse(BaseYandexModel):
    href: str
    method: str
    templated: bool = False


class CopyResourceRequest(BaseModel):
    from_path: str
    path: str
    overwrite: bool = False


class LinkRequest(BaseModel):
    path: str
    overwrite: bool = True


class ErrorResponse(BaseYandexModel):
    error: str
    message: str
    description: str
