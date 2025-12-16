from sqlmodel import Field, SQLModel


class HeroBase(SQLModel):
    """Base model for Hero with common attributes."""

    name: str = Field(title="Name", description="The public name of the hero.")
    age: int | None = Field(
        default=None, title="Age", description="The age of the hero."
    )


class Hero(HeroBase, table=True):
    """Database model for Hero with the extra fields that are not always in the other models."""

    id: int | None = Field(
        default=None,
        title="Hero ID",
        description="The unique identifier for the hero.",
        primary_key=True,
    )
    secret_name: str = Field(
        title="Secret Name", description="The secret identity of the hero."
    )


class HeroPublic(HeroBase):
    """Public model for Hero without sensitive information."""

    id: int


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
