from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    polza_api_key: str
    env: str = "development"
    cors_origins: str = ""
    polza_model: str = "openai/gpt-4o-mini"
    rate_limit_per_minute: int = 20

    @property
    def is_development(self) -> bool:
        return self.env.lower() == "development"

    @property
    def extra_cors_origins(self) -> list[str]:
        if not self.cors_origins.strip():
            return []
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
