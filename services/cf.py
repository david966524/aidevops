from typing import Optional

from CloudFlare import cloudflare
from dynaconf import Dynaconf
from fastapi import APIRouter, HTTPException
from fastapi.params import Query

from config import settings
from services.cfModel import CfRecordItem


def getCfclient():
    return cloudflare.CloudFlare(settings.cloudflare.EMAIL, settings.cloudflare.API_KEY, raw=True)


cfRouter = APIRouter()


@cfRouter.get("/getAllDomain", summary="获取cloudflare中所有的域名", description="获取cloudflare中所有的域名",
              operation_id="getCloudflareAllDomain")
async def get_all_domain():
    try:
        page_number = 0
        zoneList = []
        while True:
            page_number += 1
            raw_results = getCfclient().zones.get(params={'per_page': 150, 'page': page_number})
            zones = raw_results['result']

            for zone in zones:
                zoneList.append({"id": zone['id'], "name": zone['name']})

            total_pages = raw_results['result_info']['total_pages']
            if page_number == total_pages:
                break
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return zoneList



@cfRouter.get("/addDomain/{domainName}", summary="向cloudflare添加域名，返回的name_servers字段是需要修改的ns地址",
              description="/addDomain/需要添加的域名",
              operation_id="addCloudflareZone")
async def add_domain(domainName: str):
    try:
        zone_data = {'name': domainName}
        result = getCfclient().zones.post(data=zone_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return result



@cfRouter.post("/addRecord", summary="提供zone id，向zone添加域名解析", description="/addRecord",
               operation_id="addCloudflareZoneRecord")
async def add_records(cfRecordItem: CfRecordItem):
    try:
        print(cfRecordItem)
        zone_id = cfRecordItem.zone_id
        dns_record = {
            "type": cfRecordItem.record_type,
            "name": cfRecordItem.record_name,
            "content": cfRecordItem.record_content,
            "proxied": cfRecordItem.record_proxied
        }

        dns_record = getCfclient().zones.dns_records.post(zone_id, data=dns_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return dns_record


@cfRouter.get("/getRecords/{zoneName}", summary="提供zone name，查询zone解析", description="/getRecords/{zoneName}",
              operation_id="queryZoneRecord")
async def getRecord_zone(zoneName: str):
    try:
        raw_results = getCfclient().zones.get()
        zones = raw_results['result']
        # 根据区域名称查询区域ID
        zone_id = ''
        for zone in zones:
            print(zone['name'])
            if zone['name'] == zoneName:  # 使用您的区域名称替换 'your_zone_name'
                zone_id = zone['id']
                break

        if zone_id == '':
            return '未找到区域名称'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # 获取特定区域下的所有 DNS 记录
        dns_records = getCfclient().zones.dns_records.get(zone_id)
        return dns_records


@cfRouter.delete("/deleteZone/{zoneName}", summary="提供zone name，删除zone", description="/deleteZone/{zoneName}",
                 operation_id="deleteZone")
async def delete_zone(zoneName: str):
    try:
        raw_results = getCfclient().zones.get()
        zones = raw_results['result']

        # 根据区域名称查询区域ID
        zone_id = ''
        for zone in zones:
            if zone['name'] == zoneName:  # 使用您的区域名称替换 'your_zone_name'
                zone_id = zone['id']
                break
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        result = getCfclient().zones.delete(zone_id)
        return result


@cfRouter.delete("/deleteZoneRecord/{zoneName}/{recordName}", summary="提供zone name和record name，删除zone解析", description="/deleteZoneRecord/{zoneName}/{recordName}",
                 operation_id="deleteZoneRecord")
async def delete_record_zone(zoneName: str, recordName: str):
    # 获取所有区域
    raw_results = getCfclient().zones.get()
    zones = raw_results['result']

    # 根据区域名称查询区域ID
    zone_id = ''
    for zone in zones:
        if zone['name'] == zoneName:  # 使用您的区域名称替换 'your_zone_name'
            zone_id = zone['id']
            break

    # 获取指定区域的所有 DNS 记录
    dns_records = getCfclient().zones.dns_records.get(zone_id)

    # 找到目标 DNS 记录的 ID
    record_id = ''
    for record in dns_records['result']:
        if record['name'] == recordName+"."+zoneName:  # 使用您的DNS记录名称替换 'your_dns_record_name'
            record_id = record['id']
            break

    # 删除指定的 DNS 记录
    result = getCfclient().zones.dns_records.delete(zone_id, record_id)
    return result
