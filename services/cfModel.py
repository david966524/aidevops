from pydantic import BaseModel, Field


class CfItem(BaseModel):
    zone_id: str
    zone_name: str


class CfRecordItem(BaseModel):
    zone_id: str = Field(title="zone id", description="zoneID")
    zone_name: str = Field(title="zone id", description="zone名字")
    record_type: str = Field(title="zone id", description="解析类型A记录或者CNAME记录", examples=["A", "CNAME"])
    record_name: str = Field(title="zone id", description="子域")
    record_content: str = Field(title="zone id", description="要解析到的IP地址")
    record_proxied: bool = Field(title="zone id", description="是否要代理")
    record_ttl: str = "600"
