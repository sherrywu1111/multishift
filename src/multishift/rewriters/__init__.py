"""改写器：加载 YAML 平台模板，用 Jinja2 渲染 prompt，调 LLM 生成。"""

from importlib.resources import files
from pathlib import Path

import yaml
from jinja2 import Template

from multishift.llm import complete

TEMPLATE_DIR = files("multishift") / "templates"


def list_templates() -> list[str]:
    names = []
    for p in sorted(Path(str(TEMPLATE_DIR)).glob("*.yaml")):
        names.append(p.stem)
    return names


def load_template(platform: str) -> dict:
    path = Path(str(TEMPLATE_DIR)) / f"{platform}.yaml"
    if not path.exists():
        raise ValueError(f"未知平台模板：{platform}（可用：{', '.join(list_templates())}）")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def rewrite(text: str, platform: str) -> str:
    tpl = load_template(platform)
    system = tpl["system_prompt"]
    user = Template(tpl["user_template"]).render(text=text)
    return complete(system, user)
