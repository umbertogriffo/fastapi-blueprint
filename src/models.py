from typing import Annotated, Literal

import uuid_utils.compat as uuid
from pydantic import GetPydanticSchema
from pydantic_core import core_schema
from sqlmodel import Field, SQLModel
from uuid_utils.compat import UUID


# TODO: Remove this function when Pydantic adds native support for UUID7
#       https://github.com/pydantic/pydantic-extra-types/issues/204
def validate_uuid(val, version: Literal[1, 3, 4, 5, 6, 7, 8]) -> UUID:
    # Convert string to UUID if needed
    if isinstance(val, str):
        try:
            val = UUID(val)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid UUID format: {val}")
    if not isinstance(val, UUID):
        raise ValueError(f"Expected a UUID, got {type(val)}")
    if val.version != version:
        raise ValueError(f"Expected a UUID{version}, got UUID{val.version}")
    return val


UUID7 = Annotated[
    UUID,
    GetPydanticSchema(
        get_pydantic_core_schema=lambda _,
        handler: core_schema.with_info_plain_validator_function(
            lambda val, info: validate_uuid(
                UUID(val) if info.mode == "json" else val, version=7
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda val, info: str(val) if info.mode == "json" else val,
                info_arg=True,
            ),
        ),
        get_pydantic_json_schema=lambda _, handler: {
            **handler(core_schema.str_schema()),
            "format": "uuid7",
        },
    ),
]


class HeroBase(SQLModel):
    """Base model for Hero with common attributes."""

    name: str = Field(title="Name", description="The public name of the hero.")
    age: int | None = Field(
        default=None, title="Age", description="The age of the hero."
    )


class Hero(HeroBase, table=True):
    """Database model for Hero with the extra fields that are not always in the other models."""

    id: UUID7 = Field(
        default_factory=uuid.uuid7,
        title="Hero ID",
        description="The unique identifier for the hero.",
        primary_key=True,
    )
    secret_name: str = Field(
        title="Secret Name", description="The secret identity of the hero."
    )


class HeroPublic(HeroBase):
    """Public model for Hero without sensitive information."""

    id: UUID7


class HeroCreate(HeroBase):
    """Model for creating a new Hero."""

    secret_name: str


class HeroUpdate(HeroBase):
    """Model for updating an existing Hero.
    We don't really need to inherit from HeroBase because we are re-declaring all the fields.
    I'll leave it inheriting just for consistency, but this is not necessary.
    """

    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
