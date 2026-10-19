"""模板完整性测试：无需联网。"""

from multishift.rewriters import list_templates, load_template


def test_templates_exist():
    names = list_templates()
    assert set(names) == {"xiaohongshu", "douyin", "wechat"}


def test_template_schema():
    for name in list_templates():
        tpl = load_template(name)
        assert tpl["name"], name
        assert "system_prompt" in tpl and tpl["system_prompt"].strip(), name
        assert "{{ text }}" in tpl["user_template"], name
