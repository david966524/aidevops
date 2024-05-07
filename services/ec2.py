from fastapi import APIRouter, HTTPException
from typing import List
import boto3
from dynaconf import Dynaconf

from config import settings
from services.ec2Model import Ec2Item

# settings = Dynaconf(
#     envvar_prefix="DYNACONF",
#     settings_files=['settings.toml', 'AiDevOps/.secrets.toml'],
# )


ec2Router = APIRouter()


def get_client(region_name: str):
    try:
        client = boto3.client('ec2', region_name=region_name, aws_access_key_id=settings.aws.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.aws.aws_secret_access_key)
        return client
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@ec2Router.get("/getEc2Info/{region}", summary="获取ec2信息", description="请求路径/region", operation_id="getEc2Info")
async def get_ec2_info(region: str):
    """
    获取指定区域的EC2实例信息。

    - **region**: AWS 区域代码，例如 'us-east-1'
    - **返回**: 区域中所有EC2实例的详细信息列表
    """
    try:
        client = get_client(region)
        response = client.describe_instances()

        all_instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                all_instances.append(instance)

    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    else:
        return all_instances



@ec2Router.post("/stopEc2", summary="停止ec2", description="传入region 和 ec2id", operation_id="stopEc2")
async def stop_ec2(ec2Model: Ec2Item):
    try:
        print(ec2Model.region, ec2Model.instance_id)
        client = get_client(ec2Model.region)
        response = client.stop_instances(InstanceIds=[ec2Model.instance_id], DryRun=False)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    else:
        return response


@ec2Router.post("/rebootEc2", summary="重启ec2", description="传入region 和 ec2id", operation_id="rebootEc2")
async def reboot_ec2(ec2Model: Ec2Item):
    try:
        print(ec2Model.region, ec2Model.instance_id)
        client = get_client(ec2Model.region)
        response = client.reboot_instances(InstanceIds=[ec2Model.instance_id], DryRun=False)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    else:
        return response


@ec2Router.post("/terminateEc2", summary="终止ec2", description="传入region 和 ec2id", operation_id="terminateEc2")
async def terminate_ec2(ec2Model: Ec2Item):
    try:
        print(ec2Model.region, ec2Model.instance_id)
        client = get_client(ec2Model.region)
        response = client.terminate_instances(InstanceIds=[ec2Model.instance_id])
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    else:
        return response

