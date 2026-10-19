"""LLM 调用抽象层：OpenAI 兼容 API，默认 DeepSeek，可换任意兼容端点。"""

from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MULTISHIFT_")

    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.8


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def complete(system: str, user: str) -> str:
    s = get_settings()
    if not s.api_key:
        raise RuntimeError(
            "未配置 API Key：请设置环境变量 MULTISHIFT_API_KEY "
            "（可选 MULTISHIFT_BASE_URL / MULTISHIFT_MODEL 切换模型）"
        )
    client = OpenAI(api_key=s.api_key, base_url=s.base_url)
    resp = client.chat.completions.create(
        model=s.model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=s.temperature,
    )
    return resp.choices[0].message.content or ""
