import boto3
from fastapi import APIRouter

from config import settings

elbRouter = APIRouter()


def get_client(region_name: str):
    # 创建elbv2客户端
    client = boto3.client('elbv2', region_name=region_name, aws_access_key_id=settings.aws.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.aws.aws_secret_access_key)
    return client


@elbRouter.get("/getAllElbInfo/{region}", summary="获取elb的信息", description="传入region",
                operation_id="get_all_elb")
async def get_all_elb(region: str):
    # 获取所有LoadBalancer的详细信息
    response = get_client(region).describe_load_balancers()

    # 提取Load Balancer信息
    load_balancers = response['LoadBalancers']
    return load_balancers
