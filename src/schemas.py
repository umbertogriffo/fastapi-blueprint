from pydantic import BaseModel, constr


class User(BaseModel):
    name: constr(min_length=1)
