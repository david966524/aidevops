from pydantic import BaseModel


class Ec2Item(BaseModel):
    instance_id: str
    region: str
