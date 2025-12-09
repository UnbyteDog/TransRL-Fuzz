#!/usr/bin/env python3
# 展示s_get包含的结构

from boofuzz import *

def explain_s_get_structure():
    """解释s_get("Request")包含的内容"""

    print("=== s_get('Request') 包含的内容 ===")
    print()

    # 模拟原代码结构
    print("原代码结构：")
    print("```python")
    print("s_initialize(name='Request')                    # ← 容器开始")
    print("    with s_block('Request-Line'):               # ← 子容器1")
    print("        s_group('Method', ['GET', 'POST'])")
    print("        s_delim(' ')")
    print("        s_string('/index.html')")
    print("        s_static('\\r\\n')")
    print("        # ... 更多头部字段 ...")
    print("        s_static('\\r\\n')                      # ← 空行分隔符")
    print("")
    print("    with s_block('Body-Content'):               # ← 子容器2")
    print("        s_string('Body content ...')")
    print("```")
    print()

    print("s_get('Request') 的包含关系：")
    print("📦 Request (s_get('Request' 获取这个)")
    print("  ├── 📄 Request-Line")
    print("  │   ├── Method")
    print("  │   ├── URI")
    print("  │   ├── Headers...")
    print("  │   └── 空行分隔符")
    print("  └── 📄 Body-Content")
    print("      └── Body内容")
    print()

    print("所以：session.connect(s_get('Request')) 会连接：")
    print("✅ Request-Line 块的所有内容")
    print("✅ Body-Content 块的所有内容")
    print("✅ 两个块之间的分隔符")
    print("✅ 整个完整的HTTP请求")

def demonstrate_connection_options():
    """演示不同的连接方式"""

    print("\n=== 不同的连接方式 ===")
    print()

    print("方式1：连接整个请求（常用）")
    print("```python")
    print("session.connect(s_get('Request'))")
    print("# 生成：")
    print("# GET /index.html HTTP/1.1\\r\\n")
    print("# Host: example.com\\r\\n")
    print("# Content-Length: 16\\r\\n")
    print("# \\r\\n")
    print("# Body content ...")
    print("```")
    print()

    print("方式2：只连接请求行（不完整请求）")
    print("```python")
    print("session.connect(s_get('Request-Line'))")
    print("# 生成：")
    print("# GET /index.html HTTP/1.1\\r\\n")
    print("# Host: example.com\\r\\n")
    print("# Content-Length: 16\\r\\n")
    print("# \\r\\n")
    print("# （没有Body）")
    print("```")
    print()

    print("方式3：只连接Body（不完整请求）")
    print("```python")
    print("session.connect(s_get('Body-Content'))")
    print("# 生成：")
    print("# Body content ...")
    print("# （没有头部，不完整）")
    print("```")
    print()

    print("方式4：连接指定块（高级用法）")
    print("```python")
    print("# 可以单独测试某个部分")
    print("session.connect(s_get('Request-Line'))  # 只测试头部")
    print("session.connect(s_get('Body-Content'))  # 只测试Body")
    print("```")

def show_complete_http_output():
    """展示完整的HTTP输出"""

    print("\n=== s_get('Request') 生成的完整HTTP请求 ===")
    print()

    # 模拟完整的HTTP请求
    complete_request = """POST /index.html HTTP/1.1\r
Host: example.com\r
Content-Length: 16\r
\r
Body content ..."""

    print(complete_request)
    print()
    print("结构分解：")
    print("┌─────────────────────────────────────┐")
    print("│ POST /index.html HTTP/1.1\\r\\n      │ ← Request-Line块")
    print("│ Host: example.com\\r\\n              │ ← Request-Line块")
    print("│ Content-Length: 16\\r\\n              │ ← Request-Line块")
    print("│ \\r\\n                               │ ← Request-Line块结束")
    print("├─────────────────────────────────────┤")
    print("│ Body content ...                    │ ← Body-Content块")
    print("└─────────────────────────────────────┘")
    print()
    print("整个内容都被 s_get('Request') 包含！")

if __name__ == "__main__":
    explain_s_get_structure()
    demonstrate_connection_options()
    show_complete_http_output()