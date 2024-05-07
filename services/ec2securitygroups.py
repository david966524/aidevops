from fastapi import APIRouter, HTTPException
from typing import List
import boto3
from dynaconf import Dynaconf

from config import settings
from services.ec2Model import Ec2SgItem
from services.resp import Resp

# settings = Dynaconf(
#     envvar_prefix="DYNACONF",
#     settings_files=['settings.toml', 'AiDevOps/.secrets.toml'],
# )


ec2sgRouter = APIRouter()


def get_client(region_name: str):
    try:
        client = boto3.client('ec2', region_name=region_name, aws_access_key_id=settings.aws.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.aws.aws_secret_access_key)
        return client
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@ec2sgRouter.get("/getallsg/{region}", summary="获取ec2安全组信息", description="请求路径/region",
                 operation_id="get_security_groups", response_model=Resp)
async def get_all_sg(region: str):
    security_groups = get_client(region).describe_security_groups()
    return Resp(HttpCode=200, Data=security_groups)


@ec2sgRouter.post('/addsgingress/{region}', summary="添加ec2安全组入站规则", description="请求路径/region",
                  operation_id="add_security_groups_ingress", response_model=Resp)
async def add_security_groups_ingress(region: str, ec2sg: Ec2SgItem):
    # 添加入站规则
    response = get_client(region).authorize_security_group_ingress(
        GroupId=ec2sg.GroupId,
        IpProtocol=ec2sg.IpProtocol,
        FromPort=ec2sg.FromPort,
        ToPort=ec2sg.ToPort,
        CidrIp=ec2sg.CidrIp)

    return Resp(HttpCode=200, Data=response)


@ec2sgRouter.post("/revokeingress/{region}", summary="删除ec2安全组入站规则", description="请求路径/region",
                  operation_id="revoke_security_group_ingress", response_model=Resp)
async def revoke_security_group_ingress(region: str, ec2sg: Ec2SgItem):
    try:
        response = get_client(region).revoke_security_group_ingress(
            GroupId=ec2sg.GroupId,  # 替换为你的安全组ID
            IpPermissions=[
                {
                    'IpProtocol': ec2sg.IpProtocol,
                    'FromPort': ec2sg.FromPort,
                    'ToPort': ec2sg.ToPort,
                    'IpRanges': [{'CidrIp': ec2sg.CidrIp}]
                },
            ]
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    else:
        return Resp(HttpCode=200, Data=response)
