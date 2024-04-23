from fastapi.openapi.utils import get_openapi

from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, HttpUrl

from services import ec2 as ec2Service
from services import cf as cfService

app = FastAPI()


# OpenApi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AiDevOps",
        version="2.5.0",
        description="chatgpt",
        routes=app.routes,
    )
    openapi_schema["servers"] = [{"url": "https://test.davidops.club:8081"}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# 定义API密钥头部
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# 依赖函数，检查API密钥
async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "xxxxxx":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


# 路由
app.include_router(ec2Service.ec2Router, prefix="/ec2Api", tags=["ec2"], dependencies=[Depends(get_api_key)])
app.include_router(cfService.cfRouter, prefix="/cfApi", tags=["cloudflare"], dependencies=[Depends(get_api_key)])
# 跨域处理
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],

)


# @app.middleware("http")
# async def m2(request: Request, call_next):
#     print("request")
#     # if request.headers.get("auth") != "123456":
#     #     return Response(content="no login", status_code=401)
#     response = await call_next(request)
#     print("response")
#     return response


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
