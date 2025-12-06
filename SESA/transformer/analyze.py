#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
漏洞分析推理脚本
功能：使用训练好的模型进行代码漏洞分析
作者：老王
时间：2025
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.vulnerability_analyzer import VulnerabilityAnalyzer


def print_analysis_result(code: str, result: dict, language: str = "php"):
    """
    打印格式化的分析结果

    Args:
        code: 分析的代码
        result: 分析结果
        language: 代码语言
    """
    print(f"\n" + "=" * 60)
    print(f"🔍 代码漏洞分析结果")
    print(f"=" * 60)

    # 基本信息
    vuln_prob = result["vulnerability_assessment"]["vulnerability_probability"]
    label_info = result["vulnerability_assessment"]["label_mapping"]
    risk_score = result["vulnerability_assessment"]["line_risk_probabilities"]["overall_code_risk_score"]

    print(f"📊 风险评估:")
    print(f"   - 漏洞概率: {vuln_prob['vulnerable']:.3f}")
    print(f"   - 安全概率: {vuln_prob['safe']:.3f}")
    print(f"   - 模型置信度: {vuln_prob['confidence']:.3f}")
    print(f"   - 综合风险评分: {risk_score:.3f}")
    print(f"   - 预测结果: {'有漏洞' if label_info['predicted_label'] == 1 else '无漏洞'}")

    # 漏洞类型分析
    vuln_types = result["vulnerability_assessment"]["vulnerability_types"]
    main_type = max(vuln_types.items(), key=lambda x: x[1])

    print(f"\n🏷️  漏洞类型分析:")
    for vuln_type, prob in sorted(vuln_types.items(), key=lambda x: x[1], reverse=True):
        indicator = "🔥" if vuln_type == main_type[0] else "  "
        print(f"   {indicator} {vuln_type}: {prob:.3f}")

    # 行级风险分析
    line_risks = result["vulnerability_assessment"]["line_risk_probabilities"]
    print(f"\n📍 行级风险分析:")

    if line_risks["high_risk_lines"]:
        print(f"   🔴 高风险行:")
        for line_info in line_risks["high_risk_lines"]:
            code_snippet = line_info["code_snippet"][:80] + "..." if len(line_info["code_snippet"]) > 80 else line_info["code_snippet"]
            print(f"      - 第{line_info['line_number']}行 (风险: {line_info['risk_probability']:.3f})")
            print(f"        代码: {code_snippet}")
            if "risk_factors" in line_info and line_info["risk_factors"]:
                print(f"        风险因素: {', '.join(line_info['risk_factors'])}")

    if line_risks["medium_risk_lines"]:
        print(f"   🟡 中风险行:")
        for line_info in line_risks["medium_risk_lines"]:
            code_snippet = line_info["code_snippet"][:60] + "..." if len(line_info["code_snippet"]) > 60 else line_info["code_snippet"]
            print(f"      - 第{line_info['line_number']}行 (风险: {line_info['risk_probability']:.3f})")
            print(f"        代码: {code_snippet}")

    if not line_risks["high_risk_lines"] and not line_risks["medium_risk_lines"]:
        print(f"   ✅ 未发现明显的风险代码行")

    # 攻击面向分析
    attack_vectors = result["vulnerability_assessment"]["attack_vectors"]
    print(f"\n🌐 攻击面向分析:")
    for vector, prob in attack_vectors.items():
        level = "🔴" if prob > 0.7 else "🟡" if prob > 0.3 else "🟢"
        print(f"   {level} {vector}: {prob:.3f}")

    # 输入验证评估
    input_val = result["vulnerability_assessment"]["input_validation_assessment"]
    print(f"\n🔧 输入验证评估:")
    print(f"   - 存在用户输入: {'是' if input_val['user_input_present'] > 0.5 else '否'} ({input_val['user_input_present']:.3f})")
    print(f"   - 应用清理函数: {'是' if input_val['sanitization_applied'] > 0.5 else '否'} ({input_val['sanitization_applied']:.3f})")
    print(f"   - 存在验证逻辑: {'是' if input_val['validation_present'] > 0.5 else '否'} ({input_val['validation_present']:.3f})")
    print(f"   - 使用参数化查询: {'是' if input_val['parameterized_queries'] > 0.5 else '否'} ({input_val['parameterized_queries']:.3f})")

    # 风险等级和建议
    print(f"\n⚠️  风险等级和建议:")
    if risk_score > 0.8:
        print(f"   🔴 高风险 - 建议立即修复")
        print(f"   📋 修复建议:")
        if input_val['user_input_present'] > 0.7 and input_val['parameterized_queries'] < 0.5:
            print(f"      - 使用参数化查询或预编译语句")
            print(f"      - 对用户输入进行严格的验证和清理")
        print(f"      - 实施最小权限原则")
    elif risk_score > 0.5:
        print(f"   🟡 中风险 - 建议尽快修复")
        print(f"   📋 修复建议:")
        print(f"      - 加强输入验证")
        print(f"      - 考虑使用更安全的编码方式")
    else:
        print(f"   🟢 低风险 - 代码相对安全")
        print(f"   📋 建议:")
        print(f"      - 保持良好的编码习惯")
        print(f"      - 定期进行安全审查")

    print(f"\n📄 原始代码 ({language}):")
    print("-" * 40)
    print(code)
    print("-" * 40)


def analyze_single_code(code: str, language: str = "php", model_path: str = None):
    """
    分析单个代码片段

    Args:
        code: 要分析的代码
        language: 代码语言
        model_path: 模型路径
    """
    print("🔍 开始单代码分析...")

    try:
        # 初始化分析器
        analyzer = VulnerabilityAnalyzer()
        analyzer.load_for_inference(model_path)

        # 执行分析
        start_time = time.time()
        result = analyzer.analyze(code, language)
        analysis_time = time.time() - start_time

        print(f"✅ 分析完成，耗时: {analysis_time:.2f} 秒")

        # 打印结果
        print_analysis_result(code, result, language)

        return result

    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None


def analyze_file(file_path: str, model_path: str = None):
    """
    分析代码文件

    Args:
        file_path: 文件路径
        model_path: 模型路径
    """
    print(f"📁 开始文件分析: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return None

    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # 检测文件类型
        file_ext = Path(file_path).suffix.lower()
        language_map = {
            '.php': 'php',
            '.py': 'python',
            '.java': 'java',
            '.js': 'javascript',
            '.html': 'html',
            '.htm': 'html'
        }
        language = language_map.get(file_ext, 'php')

        # 分析代码
        result = analyze_single_code(code, language, model_path)
        return result

    except Exception as e:
        print(f"❌ 文件分析失败: {e}")
        return None


def analyze_batch(codes: list, languages: list = None, model_path: str = None):
    """
    批量分析代码

    Args:
        codes: 代码列表
        languages: 语言列表
        model_path: 模型路径
    """
    print(f"🔄 开始批量分析 ({len(codes)} 个代码片段)...")

    try:
        # 初始化分析器
        analyzer = VulnerabilityAnalyzer()
        analyzer.load_for_inference(model_path)

        # 批量分析
        start_time = time.time()
        results = analyzer.batch_analyze(codes, languages)
        analysis_time = time.time() - start_time

        print(f"✅ 批量分析完成，总耗时: {analysis_time:.2f} 秒")
        print(f"📊 平均每个: {analysis_time/len(codes):.2f} 秒")

        # 统计信息
        vulnerable_count = sum(1 for r in results if r["vulnerability_assessment"]["label_mapping"]["predicted_label"] == 1)
        avg_risk = sum(r["vulnerability_assessment"]["line_risk_probabilities"]["overall_code_risk_score"] for r in results) / len(results)

        print(f"\n📈 批量分析统计:")
        print(f"   - 总代码数: {len(codes)}")
        print(f"   - 发现漏洞: {vulnerable_count} ({vulnerable_count/len(codes)*100:.1f}%)")
        print(f"   - 平均风险评分: {avg_risk:.3f}")

        # 详细结果
        for i, (code, result) in enumerate(zip(codes, results), 1):
            print(f"\n{'='*40} 代码 {i}/{len(codes)} {'='*40}")
            risk_score = result["vulnerability_assessment"]["line_risk_probabilities"]["overall_code_risk_score"]
            is_vulnerable = result["vulnerability_assessment"]["label_mapping"]["predicted_label"] == 1

            print(f"📊 风险评分: {risk_score:.3f} | 状态: {'🔴有漏洞' if is_vulnerable else '🟢无漏洞'}")

            # 只显示前几行代码
            code_lines = code.strip().split('\n')[:3]
            print(f"📄 代码预览:")
            for line in code_lines:
                print(f"   {line}")
            if len(code.strip().split('\n')) > 3:
                print("   ...")

        return results

    except Exception as e:
        print(f"❌ 批量分析失败: {e}")
        return None


def interactive_mode(model_path: str = None):
    """
    交互式分析模式

    Args:
        model_path: 模型路径
    """
    print("🎯 交互式漏洞分析模式")
    print("输入 'quit' 或 'exit' 退出，输入 'help' 查看帮助")

    # 初始化分析器
    print("🤖 初始化分析器...")
    analyzer = VulnerabilityAnalyzer()
    analyzer.load_for_inference(model_path)
    print("✅ 分析器就绪")

    while True:
        try:
            # 获取用户输入
            print("\n" + "-" * 50)
            code_input = input("请输入要分析的代码（或输入命令）:\n")

            # 处理命令
            if code_input.lower() in ['quit', 'exit']:
                print("👋 再见！")
                break
            elif code_input.lower() == 'help':
                print_help()
                continue
            elif code_input.lower() == 'clear':
                analyzer.clear_cache()
                print("🧹 缓存已清空")
                continue
            elif code_input.lower() == 'cache':
                cache_info = analyzer.get_cache_info()
                print(f"💾 缓存信息: {cache_info}")
                continue
            elif code_input.startswith('file '):
                # 文件分析模式
                file_path = code_input[5:].strip()
                if file_path:
                    analyze_file(file_path, model_path)
                else:
                    print("❌ 请指定文件路径")
                continue
            elif code_input.startswith('lang '):
                # 语言设置
                language = code_input[5:].strip()
                print(f"📝 语言设置为: {language}")
                continue

            # 代码分析
            if code_input.strip():
                language = 'php'  # 默认语言
                result = analyzer.analyze(code_input, language)

                # 简化输出
                vuln_prob = result["vulnerability_assessment"]["vulnerability_probability"]
                risk_score = result["vulnerability_assessment"]["line_risk_probabilities"]["overall_code_risk_score"]
                is_vulnerable = analyzer.is_vulnerable(code_input)

                print(f"\n🔍 快速分析结果:")
                print(f"   - 风险评分: {risk_score:.3f}")
                print(f"   - 漏洞概率: {vuln_prob['vulnerable']:.3f}")
                print(f"   - 判定结果: {'🔴有漏洞' if is_vulnerable else '🟢无漏洞'}")

                # 询问是否查看详细结果
                detail = input("\n查看详细分析结果？(y/N): ").strip().lower()
                if detail in ['y', 'yes']:
                    print_analysis_result(code_input, result, language)

        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 分析失败: {e}")


def print_help():
    """打印帮助信息"""
    print("\n📖 命令帮助:")
    print("  help          - 显示此帮助信息")
    print("  quit/exit     - 退出程序")
    print("  clear         - 清空分析缓存")
    print("  cache         - 显示缓存信息")
    print("  file <path>   - 分析指定文件")
    print("  lang <name>   - 设置代码语言（默认php）")
    print("\n示例:")
    print("  file /path/to/vulnerable.php")
    print("  lang python")
    print("  $sql = \"SELECT * FROM users WHERE id='$id'\";")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Web漏洞分析推理脚本")
    parser.add_argument("--code", "-c", type=str, help="要分析的代码")
    parser.add_argument("--file", "-f", type=str, help="要分析的文件路径")
    parser.add_argument("--batch", "-b", type=str, help="批量分析文件（每行一个代码片段）")
    parser.add_argument("--language", "-l", type=str, default="php", help="代码语言，默认php")
    parser.add_argument("--model", "-m", type=str, help="模型路径")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")

    args = parser.parse_args()

    print("🔍 Web漏洞检测分析器")
    print("=" * 50)

    try:
        # 检查模型文件
        model_path = args.model
        if model_path and not os.path.exists(model_path):
            print(f"❌ 模型路径不存在: {model_path}")
            sys.exit(1)

        # 交互式模式
        if args.interactive:
            interactive_mode(model_path)
            return

        # 单代码分析
        if args.code:
            print("🔍 单代码分析模式")
            analyze_single_code(args.code, args.language, model_path)
            return

        # 文件分析
        if args.file:
            print("📁 文件分析模式")
            analyze_file(args.file, model_path)
            return

        # 批量分析
        if args.batch:
            print("📊 批量分析模式")
            if not os.path.exists(args.batch):
                print(f"❌ 批量文件不存在: {args.batch}")
                sys.exit(1)

            with open(args.batch, 'r', encoding='utf-8') as f:
                codes = [line.strip() for line in f if line.strip()]

            if codes:
                languages = [args.language] * len(codes)
                analyze_batch(codes, languages, model_path)
            else:
                print("❌ 批量文件为空")
            return

        # 如果没有指定任何模式，进入交互模式
        print("⚠️ 未指定分析模式，进入交互模式...")
        interactive_mode(model_path)

    except KeyboardInterrupt:
        print("\n👋 再见！")
    except Exception as e:
        print(f"❌ 程序失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()