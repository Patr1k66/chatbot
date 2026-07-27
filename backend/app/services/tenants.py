import json
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


CLIENTS_DIR = Path(__file__).resolve().parent.parent.parent / "clients"


class TenantConfig(BaseModel):
    bot_id: str
    business_name: str
    allowed_domains: list[str] = Field(default_factory=list)
    system_prompt: str
    escalation_contact: str
    primary_color: str = "#2563eb"
    welcome_message: str = "Здравствуйте! Чем могу помочь?"


@lru_cache
def _load_all_tenants() -> dict[str, TenantConfig]:
    tenants: dict[str, TenantConfig] = {}
    if not CLIENTS_DIR.exists():
        return tenants

    for path in CLIENTS_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        tenant = TenantConfig.model_validate(data)
        tenants[tenant.bot_id] = tenant

    return tenants


def get_tenant(bot_id: str) -> TenantConfig | None:
    return _load_all_tenants().get(bot_id)


def get_allowed_origins() -> list[str]:
    origins: set[str] = set()
    for tenant in _load_all_tenants().values():
        for domain in tenant.allowed_domains:
            origins.add(f"https://{domain}")
            origins.add(f"http://{domain}")
    return sorted(origins)


def reload_tenants() -> None:
    _load_all_tenants.cache_clear()
