"""multishift CLI：一篇长文 → 多平台文案。"""

from pathlib import Path

import typer

from .rewriters import list_templates, rewrite

app = typer.Typer(help="多平台爆文改写器 multishift")


@app.command()
def templates():
    """列出可用的平台模板。"""
    for name in list_templates():
        typer.echo(name)


@app.command()
def rewrite_cmd(
    input: Path = typer.Argument(..., help="输入文件（txt/md）"),
    platform: str = typer.Option("all", "--platform", "-p", help="目标平台：all 或模板名"),
    output_dir: Path = typer.Option(Path("out"), "--out", "-o", help="输出目录"),
):
    """把一篇长文改写成目标平台文案。"""
    text = input.read_text(encoding="utf-8").strip()
    if not text:
        raise typer.BadParameter("输入文件为空")

    platforms = list_templates() if platform == "all" else [platform]
    output_dir.mkdir(parents=True, exist_ok=True)

    for pf in platforms:
        typer.echo(f"正在改写 → {pf} ...")
        result = rewrite(text, pf)
        out = output_dir / f"{input.stem}.{pf}.md"
        out.write_text(result, encoding="utf-8")
        typer.echo(f"已写入 {out}")


def main():
    app()


# typer 入口别名：project.scripts 指向 multishift.cli:app
rewrite_cmd.__name__ = "rewrite"

if __name__ == "__main__":
    # 兼容 `python -m multishift.cli rewrite ...`
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rewrite":
        sys.argv[1] = "rewrite-cmd"
    app()
