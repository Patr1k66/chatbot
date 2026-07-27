from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.services.llm import build_system_prompt, generate_reply
from app.services.rate_limit import client_ip, rate_limiter
from app.services.tenants import get_tenant

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    bot_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    reply: str


class BotConfigResponse(BaseModel):
    bot_id: str
    business_name: str
    primary_color: str
    welcome_message: str
    escalation_contact: str


@router.get("/config/{bot_id}", response_model=BotConfigResponse)
def get_bot_config(bot_id: str) -> BotConfigResponse:
    tenant = get_tenant(bot_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Bot not found")

    return BotConfigResponse(
        bot_id=tenant.bot_id,
        business_name=tenant.business_name,
        primary_color=tenant.primary_color,
        welcome_message=tenant.welcome_message,
        escalation_contact=tenant.escalation_contact,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    tenant = get_tenant(payload.bot_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Bot not found")

    rate_limiter.check(f"{payload.bot_id}:{client_ip(request)}")

    history = [{"role": msg.role, "content": msg.content} for msg in payload.history]
    system_prompt = build_system_prompt(tenant.system_prompt, tenant.escalation_contact)

    try:
        reply = generate_reply(system_prompt, history, payload.message)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail=(
                "Сервис временно недоступен. "
                f"Напишите нам: {tenant.escalation_contact}"
            ),
        )

    return ChatResponse(reply=reply)
