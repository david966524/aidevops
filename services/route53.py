import boto3
from fastapi import APIRouter

from config import settings
from services.route53Model import R53Item

r53Router = APIRouter()


def get_client():
    client = boto3.client('route53', aws_access_key_id=settings.aws.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.aws.aws_secret_access_key)
    return client


@r53Router.get("/getHostedZone", summary="获取route53 中的域名信息", description="get请求",
               operation_id="getHostedZone")
async def get_hosted_zone():
    response = get_client().list_hosted_zones()
    for zone in response['HostedZones']:
        print('HostedZone ID:', zone['Id'])
        print('HostedZone Name:', zone['Name'])
    return response['HostedZones']


@r53Router.post("/create_record", summary="创建域名解析", description="传入zone_id ，Type， ResourceRecords value",
                operation_id="create_record")
async def create_record(i: R53Item):
    response = get_client().change_resource_record_sets(
        HostedZoneId=i.zone_id,  # HostedZone的ID
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'CREATE',  # 操作类型，可以是 'CREATE' | 'DELETE' | 'UPSERT'
                    'ResourceRecordSet': {
                        'Name': i.domain_name,  # 需要添加解析的域名
                        'Type': i.record_type,
                        # 记录类型，可以是 'A' | 'AAAA' | 'CNAME' | 'MX' | 'NAPTR' | 'NS' | 'PTR' | 'SOA' | 'SPF' | 'SRV' | 'TXT'
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': i.record_value  # 记录值
                            },
                        ],
                    }
                },
            ]
        }
    )

    return response
