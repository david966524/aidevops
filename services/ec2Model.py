from pydantic import BaseModel, Field


class Ec2Item(BaseModel):
    instance_id: str = Field(title="instance id", description="instance_id")
    region: str = Field(title="region", description="region")


class Ec2SgItem(BaseModel):
    GroupName: str = Field(default=None,title="GroupName", description="GroupName")
    GroupId: str = Field(title="GroupId", description="GroupId")
    IpProtocol: str = Field(title="IpProtocol", description="IpProtocol")
    FromPort: int = Field(title="FromPort", description="FromPort")
    ToPort: int = Field(title="ToPort", description="ToPort")
    CidrIp: str = Field(title="CidrIp", description="CidrIp")
