import time

from fastapi import APIRouter

from config import settings
import requests

bcRouter = APIRouter()


def getNodeList():
    url = "https://api.boce.com/v3/node/list?"
    params = {
        "key": settings.boce.API_KEY
    }
    resp = requests.get(url, params=params)
    node_id_list = ""
    for node in resp.json()["data"]["list"]:
        node_id_list += str(node["id"]) + ","
    return node_id_list[:-1]


def getTaskId(domain: str):
    url = "https://api.boce.com/v3/task/create/curl?"
    params = {
        "key": settings.boce.API_KEY,
        "node_ids": getNodeList(),
        "host": domain
    }
    print(getNodeList())
    resp = requests.get(url, params=params)

    return resp.json()["data"]["id"]


@bcRouter.get("/boceInfo/{domain}", summary="获取拨测结果", description="传入要拨测的域名",
                operation_id="get_boceInfo")
async def get_boceInfo(domain: str):
    print(getTaskId(domain))
    url = "https://api.boce.com/v3/task/curl/" + getTaskId(domain) + "?"
    params = {
        "key": settings.boce.API_KEY
    }

    for i in range(5):
        time.sleep(10)
        resp = requests.get(url, params=params)
        print(resp.json()["done"])
        if resp.json()["done"] is True:
            return resp.json()["list"]
        else:
            continue
