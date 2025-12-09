#!/usr/bin/env python3
# 针对XSS靶场的模糊测试

from boofuzz import *

def main():
    session = Session(
        target=Target(connection=TCPSocketConnection("192.168.0.1", 80)),
    )

    s_initialize(name="XSS-Request")
    with s_block("Request-Line"):
        s_group("Method", ["GET", "POST"])
        s_delim(" ")
        s_string("/xss", name="Request-URI")        # ← 关键：指定XSS路径
        s_delim(" ")
        s_string("HTTP/1.1")
        s_static("\r\n")
        s_string("Host:")
        s_delim(" ")
        s_string("192.168.0.1", name="Host-Value")   # ← 写你的服务器IP
        s_static("\r\n")
        s_string("User-Agent:")
        s_delim(" ")
        s_string("Mozilla/5.0", name="User-Agent-Value")
        s_static("\r\n")
        s_static("\r\n")

    # 如果POST请求，添加Body
    with s_block("Body-Content"):
        s_string("<script>alert('xss')</script>", name="XSS-Payload")

    session.connect(s_get("XSS-Request"))
    session.fuzz()

def test_sqli_target():
    """针对SQL注入靶场的测试"""
    session = Session(
        target=Target(connection=TCPSocketConnection("192.168.0.1", 80)),
    )

    s_initialize(name="SQLI-Request")
    with s_block("Request-Line"):
        s_group("Method", ["GET", "POST"])
        s_delim(" ")
        s_string("/sqli", name="Request-URI")        # ← 关键：指定SQL注入路径
        s_delim(" ")
        s_string("HTTP/1.1")
        s_static("\r\n")
        s_string("Host:")
        s_delim(" ")
        s_string("192.168.0.1", name="Host-Value")
        s_static("\r\n")
        s_static("\r\n")

    with s_block("Body-Content"):
        s_string("' OR '1'='1", name="SQL-Payload")

    session.connect(s_get("SQLI-Request"))
    session.fuzz()

def show_explanation():
    """展示说明"""
    print("=== TCP连接和HTTP路径的关系 ===")
    print()
    print("1. TCPSocketConnection 只负责连接到服务器：")
    print("   TCPSocketConnection('192.168.0.1', 80)")
    print("   ↑ 只指定IP地址和端口")
    print()
    print("2. HTTP路径在请求中指定：")
    print("   GET /xss HTTP/1.1    ← 访问XSS靶场")
    print("   GET /sqli HTTP/1.1   ← 访问SQL注入靶场")
    print("   ↑ 这是HTTP请求的一部分")
    print()
    print("3. 完整流程：")
    print("   TCP连接 → 发送HTTP请求 → 服务器根据路径路由到具体应用")
    print("   连接到192.168.0.1:80 → 发送'GET /xss' → 服务器转发给XSS应用")
    print()
    print("4. 所以：")
    print("   ✅ TCPSocketConnection写：TCPSocketConnection('192.168.0.1', 80)")
    print("   ✅ s_string写：s_string('/xss', name='Request-URI')")

if __name__ == "__main__":
    show_explanation()
    print("\n运行XSS测试:")
    main()