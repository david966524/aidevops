from pydantic import BaseModel, Field


class CfItem(BaseModel):
    zone_id: str
    zone_name: str


class CfRecordItem(BaseModel):
    zone_id: str = Field(title="zone id", description="zoneID")
    zone_name: str = Field(title="zoneName", description="zoneName")
    record_type: str = Field(title="recordType", description="recordType", examples=["A", "CNAME"])
    record_name: str = Field(title="Subdomain", description="Subdomain")
    record_content: str = Field(title="recordIp", description="recordIp")
    record_proxied: bool = Field(title="proxied", description="proxied")
    record_ttl: str = "60"
