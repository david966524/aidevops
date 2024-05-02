from pydantic import BaseModel, Field


class R53Item(BaseModel):
    zone_id: str = Field(title="zone_id", description="zoneID")
    domain_name: str = Field(title="domain_name", description="domainName")
    record_type: str = Field(title="record_type", description="recordType")
    record_value: str = Field(title="record_value", description="recordValue")
