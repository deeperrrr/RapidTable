# -*- encoding: utf-8 -*-
import sys
import warnings

import pytest


@pytest.mark.skipif(
    sys.version_info.major == 3 and sys.version_info.minor < 12,
    reason="仅在python>=3.12时测试",
)
def test_regex_syntax_warning():
    """测试捕获正则表达式中无效转义序列产生的 SyntaxWarning"""

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # 使用 compile() 来编译包含无效转义序列的代码，这会触发 SyntaxWarning
        code_with_invalid_escape = """
import re
thead_part = '<td></td> rowspan="2"></b></td>'
isolate_pattern = (
'<td></td> rowspan="(\d)+" colspan="(\d)+"></b></td>|'
'<td></td> colspan="(\d)+" rowspan="(\d)+"></b></td>|'
'<td></td> rowspan="(\d)+"></b></td>|'
'<td></td> colspan="(\d)+"></b></td>'
)
re.finditer(isolate_pattern, thead_part)
"""

        # 编译代码时会产生 SyntaxWarning
        compile(code_with_invalid_escape, "<string>", "exec")

        # 检查是否捕获到 SyntaxWarning
        syntax_warnings = [
            warn for warn in w if issubclass(warn.category, SyntaxWarning)
        ]
        assert (
            len(syntax_warnings) > 0
        ), f"未捕获到 SyntaxWarning: {[str(warn.message) for warn in w]}"

        # 应该捕获到无效转义序列的警告
        for warning in syntax_warnings:
            assert "invalid escape sequence" in str(warning.message)


@pytest.mark.skipif(
    sys.version_info.major == 3 and sys.version_info.minor < 12,
    reason="仅在python>=3.12时测试",
)
def test_correct_regex_pattern():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # 这不会触发 SyntaxWarning
        code_with_invalid_escape = """
import re
thead_part = '<td></td> rowspan="2"></b></td>'
isolate_pattern_raw = (
r'<td></td> rowspan="(\d)+" colspan="(\d)+"></b></td>|'
r'<td></td> colspan="(\d)+" rowspan="(\d)+"></b></td>|'
r'<td></td> rowspan="(\d)+"></b></td>|'
r'<td></td> colspan="(\d)+"></b></td>'
)
re.finditer(isolate_pattern_raw, thead_part)
"""
        compile(code_with_invalid_escape, "<string>", "exec")

        # 检查是否捕获到 SyntaxWarning
        syntax_warnings = [
            warn for warn in w if issubclass(warn.category, SyntaxWarning)
        ]
        assert (
            len(syntax_warnings) == 0
        ), f"正常写法捕获到 SyntaxWarning: {[str(warn.message) for warn in w]}"
