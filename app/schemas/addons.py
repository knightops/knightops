from pydantic import BaseModel, Field


class Addons(BaseModel):
    name: str = Field(default='', title='', description='')
    title: str = Field()
    version: str = Field('1.0')
    author: str
    intro: str
