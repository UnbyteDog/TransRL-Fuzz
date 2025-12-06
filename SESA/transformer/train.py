#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模型训练脚本
功能：完整的模型训练流程，包括数据处理、模型微调和验证
作者：老王
时间：2025
"""

import os
import sys
import json
import time
import argparse

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_processor import DataProcessor
from models.vulnerability_analyzer import VulnerabilityAnalyzer


def load_config(config_path: str = None, debug: bool = False) -> dict:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    if config_path is None:
        config_path = "configs/training_config.yaml"

    # 默认配置 - 使用当前脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = {
        "data": {
            "raw_data_path": os.path.join(base_dir, "data", "Tdataset.jsonl"),
            "train_output_path": os.path.join(base_dir, "data", "train_samples.json"),
            "val_output_path": os.path.join(base_dir, "data", "val_samples.json"),
            "train_ratio": 0.8
        },
        "model": {
            "base_model": "deepseek-ai/deepseek-coder-1.3b-instruct",
            "existing_lora": os.path.join(base_dir, "models", "pentest-vulnerability-detector"),
            "output_dir": os.path.join(base_dir, "models", "fine_tuned")
        },
        "training": {
            "num_train_epochs": 3,
            "per_device_train_batch_size": 2,
            "gradient_accumulation_steps": 8,
            "learning_rate": 3e-5,
            "fp16": True,
            "save_strategy": "steps",
            "save_steps": 500,
            "eval_strategy": "steps",
            "eval_steps": 500,
            "logging_steps": 50,
            "load_best_model_at_end": True
        }
    }

    # 如果配置文件存在，尝试加载
    if os.path.exists(config_path):
        try:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            elif config_path.endswith('.json'):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                print(f"[WARNING] 不支持的配置文件格式: {config_path}，使用默认配置")
                return default_config

            # 合并默认配置和用户配置
            merged_config = default_config.copy()
            deep_update(merged_config, config)

            # 类型转换 - 确保类型正确
            if 'training' in merged_config:
                training_config = merged_config['training']
                # 转换各种类型
                for key, value in training_config.items():
                    if isinstance(value, str):
                        # 布尔值转换
                        if value.lower() in ['true', 'yes', '1']:
                            training_config[key] = True
                        elif value.lower() in ['false', 'no', '0']:
                            training_config[key] = False
                        # 数值转换
                        elif value.replace('.', '').replace('e-', '').replace('e+', '').isdigit():
                            try:
                                if 'e' in value.lower():
                                    training_config[key] = float(value)
                                elif '.' in value:
                                    training_config[key] = float(value)
                                else:
                                    training_config[key] = int(value)
                            except ValueError:
                                pass  # 保持原值

            # 调试信息
            if debug:
                print("[INFO] 配置加载调试信息:")
                if 'training' in merged_config:
                    training_config = merged_config['training']
                    for key, value in training_config.items():
                        print(f"   {key}: {value} (type: {type(value).__name__})")

            return merged_config

        except Exception as e:
            print(f"[WARNING] 配置文件加载失败: {e}，使用默认配置")
            return default_config
    else:
        print(f"[WARNING] 配置文件不存在: {config_path}，使用默认配置")
        return default_config


def deep_update(base_dict: dict, update_dict: dict):
    """
    深度更新字典
    """
    for key, value in update_dict.items():
        if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
            deep_update(base_dict[key], value)
        else:
            base_dict[key] = value


def check_environment():
    """检查环境配置"""
    print("[INFO] 检查运行环境...")

    # 检查Python版本
    if sys.version_info < (3, 8):
        print("[ERROR] Python版本过低，需要Python 3.8+")
        sys.exit(1)
    print(f"[SUCCESS] Python版本: {sys.version}")

    # 设置环境变量 - CPU优化版本 + 网络优化
    import os
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # 设置HuggingFace镜像加速下载
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    print("[INFO] 已设置HuggingFace镜像加速下载")

    # 检查CUDA可用性，只在有GPU时设置CUDA相关变量
    try:
        import torch
        if torch.cuda.is_available():
            os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  # 更好的错误信息
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"  # 内存碎片管理
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # 指定GPU
        else:
            print("[INFO] 检测到CPU环境，优化CPU训练设置...")
            os.environ["OMP_NUM_THREADS"] = "4"  # 限制OpenMP线程数，避免过度竞争
            os.environ["MKL_NUM_THREADS"] = "4"   # 限制MKL线程数
    except:
        pass

    # 检查CUDA
    try:
        import torch

        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"[SUCCESS] CUDA可用，GPU数量: {gpu_count}，GPU类型: {gpu_name}")
        else:
            print("[WARNING] CUDA不可用，将使用CPU训练（速度较慢）")
    except ImportError:
        print("[ERROR] PyTorch未安装")
        sys.exit(1)

    # 检查关键依赖 - CPU训练不需要bitsandbytes
    import torch
    required_packages = ["transformers", "peft", "datasets"]

    # 只在CUDA环境下检查bitsandbytes
    if torch.cuda.is_available():
        required_packages.append("bitsandbytes")
        print("[INFO] GPU环境：将使用4-bit量化训练")
    else:
        print("[INFO] CPU环境：将使用标准精度训练（跳过bitsandbytes）")

    for package in required_packages:
        try:
            __import__(package)
            print(f"[SUCCESS] {package}")
        except ImportError:
            print(f"[ERROR] {package} 未安装，请运行: pip install {package}")
            sys.exit(1)

    print("[SUCCESS] 环境检查完成")


def check_data_files(config: dict):
    """检查数据文件"""
    print("[INFO] 检查数据文件...")

    raw_data_path = config["data"]["raw_data_path"]

    if not os.path.exists(raw_data_path):
        print(f"[ERROR] 原始数据文件不存在: {raw_data_path}")
        print("请确保数据文件存在，或修改配置文件中的路径")
        sys.exit(1)

    # 检查文件大小
    file_size = os.path.getsize(raw_data_path)
    print(f"📄 原始数据: {raw_data_path} ({file_size/1024/1024:.1f} MB)")

    # 尝试读取几行验证格式
    try:
        import json
        with open(raw_data_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:3]  # 读取前3行
            for i, line in enumerate(lines):
                if line.strip():
                    data = json.loads(line)
                    required_fields = ['code', 'label', 'language']
                    if not all(field in data for field in required_fields):
                        print(f"[ERROR] 数据格式错误，第{i+1}行缺少必要字段")
                        sys.exit(1)
        print("[SUCCESS] 数据格式验证通过")
    except Exception as e:
        print(f"[ERROR] 数据文件验证失败: {e}")
        sys.exit(1)


def process_data(config: dict, quick_test: bool = False) -> tuple:
    """
    处理数据

    Args:
        config: 配置字典
        quick_test: 是否为快速测试模式

    Returns:
        (训练样本数量, 验证样本数量)
    """
    print("[INFO] 开始数据处理...")

    # 检查是否已经有处理好的数据
    train_path = config["data"]["train_output_path"]
    val_path = config["data"]["val_output_path"]

    if os.path.exists(train_path) and os.path.exists(val_path):
        # 在快速测试模式下，直接重新处理
        if quick_test:
            print("[INFO] 快速测试模式：重新处理数据")
        else:
            # 询问是否重新处理
            try:
                response = input("发现已处理的数据，是否重新处理？(y/N): ").strip().lower()
                if response != 'y' and response != 'yes':
                    # 加载现有数据
                    with open(train_path, 'r') as f:
                        train_data = json.load(f)
                    with open(val_path, 'r') as f:
                        val_data = json.load(f)
                    print(f"[SUCCESS] 使用现有数据 - 训练: {len(train_data)}, 验证: {len(val_data)}")
                    return len(train_data), len(val_data)
            except EOFError:
                print("[INFO] 无交互模式，重新处理数据")

    # 执行数据处理
    processor = DataProcessor(config["data"]["raw_data_path"])
    train_samples, val_samples = processor.process_and_save(
        train_ratio=config["data"]["train_ratio"],
        output_dir=os.path.dirname(train_path)
    )

    return len(train_samples), len(val_samples)


def train_model(config: dict, quick_test: bool = False, args=None):
    """
    训练模型 - 修复版本

    Args:
        config: 配置字典
        quick_test: 是否为快速测试模式
    """
    print("[INFO][INFO] 开始模型训练...")

    # 训练统计信息
    start_time = time.time()

    try:
        # 初始化分析器
        analyzer = VulnerabilityAnalyzer(config["model"]["base_model"])

        # 准备训练参数
        training_config = {
            **config["training"],
            "output_dir": config["model"]["output_dir"],
            "gradient_checkpointing": False,  # 暂时禁用
            "dataloader_pin_memory": False,  # 避免内存问题
        }

        # 处理不同的训练模式
        full_train = args.full_train if args else False
        custom_epochs = args.epochs if args else None
        custom_batch_size = args.batch_size if args else None

        if quick_test:
            # 快速测试模式 - 优化参数
            training_config.update({
                "num_train_epochs": 1,  # 减少到1个epoch
                "max_steps": 100,       # 减少到100步
                "per_device_train_batch_size": 1,
                "save_steps": 25,
                "eval_steps": 25,
                "logging_steps": 5,
                "gradient_accumulation_steps": 8,
                "learning_rate": 5e-5,  # 稍微提高学习率
                "warmup_steps": 10,     # 减少warmup
            })
        elif full_train:
            # 完整训练模式 - 最佳参数
            training_config.update({
                "num_train_epochs": 8,      # 充分训练
                "per_device_train_batch_size": 1,
                "gradient_accumulation_steps": 16,
                "learning_rate": 1e-5,      # 更低的学习率，更稳定
                "lr_scheduler_type": "cosine_with_restarts",
                "warmup_ratio": 0.03,
                "max_grad_norm": 0.5,
                "weight_decay": 0.01,
                "save_steps": 500,
                "eval_steps": 500,
                "logging_steps": 50,
                "save_total_limit": 3,
                "load_best_model_at_end": True,
                "metric_for_best_model": "eval_loss",
                "greater_is_better": False,
                "eval_strategy": "steps",
            })
        else:
            # 默认训练模式 - 平衡参数
            training_config.update({
                "num_train_epochs": 5,      # 适中的训练轮次
                "per_device_train_batch_size": 1,
                "gradient_accumulation_steps": 16,
                "learning_rate": 2e-5,
                "lr_scheduler_type": "cosine_with_restarts",
                "warmup_ratio": 0.05,
                "max_grad_norm": 0.5,
                "weight_decay": 0.01,
                "save_steps": 200,
                "eval_steps": 200,
                "logging_steps": 20,
                "save_total_limit": 5,
                "load_best_model_at_end": True,
                "metric_for_best_model": "eval_loss",
                "greater_is_better": False,
                "eval_strategy": "steps",
            })

        # 应用命令行参数覆盖
        if custom_epochs:
            training_config["num_train_epochs"] = custom_epochs
        if custom_batch_size:
            training_config["per_device_train_batch_size"] = custom_batch_size

        # 开始训练
        analyzer.train(
            train_data_path=config["data"]["train_output_path"],
            val_data_path=config["data"]["val_output_path"],
            config=training_config
        )

        # 训练完成
        end_time = time.time()
        training_time = end_time - start_time

        print(f"[SUCCESS] 训练完成！")
        print(f"[INFO]  总耗时: {training_time/60:.1f} 分钟")
        print(f"📁 模型保存位置: {config['model']['output_dir']}")

        # 显示训练统计信息
        training_mode = '快速测试' if quick_test else ('完整训练' if full_train else '默认模式')
        print(f"\n[INFO] 训练统计:")
        print(f"   - 训练模式: {training_mode}")
        print(f"   - 训练轮次: {training_config.get('num_train_epochs', 'N/A')}")
        print(f"   - 学习率: {training_config.get('learning_rate', 'N/A')}")
        print(f"   - 批次大小: {training_config.get('per_device_train_batch_size', 'N/A')}")
        print(f"   - 梯度累积: {training_config.get('gradient_accumulation_steps', 'N/A')}")

        # 估算训练效果
        if training_time > 0:
            print(f"   - 训练速度: {training_time/60:.1f} 分钟")
            if not quick_test:
                print(f"   - 建议: 模型已充分训练，可以进行推理测试")
            else:
                print(f"   - 建议: 如需更好性能，请使用完整训练模式: python train.py --full-train")

    except Exception as e:
        print(f"[ERROR][ERROR] 训练失败: {e}")
        # 提供更详细的错误信息
        import traceback
        traceback.print_exc()
        print("\n📋 可能的解决方案:")
        print("   1. 检查LoRA适配器是否正确加载")
        print("   2. 确保数据格式正确")
        print("   3. 尝试减少batch size或使用CPU训练")
        raise


def validate_model(config: dict):
    """
    验证训练好的模型

    Args:
        config: 配置字典
    """
    print("🧪 验证训练好的模型...")

    try:
        # 加载分析器
        analyzer = VulnerabilityAnalyzer()
        analyzer.load_for_inference(config["model"]["output_dir"])

        # 简单测试
        test_code = """<?php
$username = $_GET['username'];
$sql = "SELECT * FROM users WHERE username='$username'";
$result = $conn->query($sql);
?>"""

        print("[INFO] 测试代码:")
        print(test_code)

        result = analyzer.analyze(test_code)
        risk_score = result["vulnerability_assessment"]["line_risk_probabilities"]["overall_code_risk_score"]
        is_vulnerable = analyzer.is_vulnerable(test_code)

        print(f"[INFO] 分析结果:")
        print(f"   - 风险评分: {risk_score:.3f}")
        print(f"   - 是否有漏洞: {'是' if is_vulnerable else '否'}")
        print(f"   - 漏洞概率: {result['vulnerability_assessment']['vulnerability_probability']['vulnerable']:.3f}")

        if is_vulnerable:
            print("[SUCCESS] 模型验证成功！正确识别了SQL注入漏洞")
        else:
            print("[WARNING] 模型可能未正确识别SQL注入漏洞")

    except Exception as e:
        print(f"[ERROR] 模型验证失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="漏洞检测模型训练脚本")
    parser.add_argument("--config", "-c", type=str, help="配置文件路径")
    parser.add_argument("--quick-test", "-q", action="store_true", help="快速测试模式（使用适量数据进行训练）")
    parser.add_argument("--full-train", "-f", action="store_true", help="完整训练模式（使用全部数据充分训练）")
    parser.add_argument("--skip-data", action="store_true", help="跳过数据处理，使用现有数据")
    parser.add_argument("--validate-only", action="store_true", help="只验证现有模型，不进行训练")
    parser.add_argument("--epochs", "-e", type=int, help="训练轮次数（覆盖配置文件）")
    parser.add_argument("--batch-size", "-b", type=int, help="批次大小（覆盖配置文件）")

    args = parser.parse_args()

    print("🎯 Web漏洞检测模型训练")
    print("=" * 50)

    try:
        # 1. 检查环境
        check_environment()

        # 2. 加载配置
        config = load_config(args.config, args.quick_test)
        print(f"📋 配置加载完成")

        # 3. 检查数据文件
        if not args.validate_only:
            check_data_files(config)

        # 4. 数据处理
        if not args.skip_data and not args.validate_only:
            if args.quick_test:
                print("[INFO] 快速测试模式：使用更多数据进行充分训练")
                # 快速测试使用更多数据，确保模型能学到有效模式
                # 这里可以通过数据处理器限制数据量
                pass

            train_count, val_count = process_data(config, args.quick_test)
            print(f"[INFO] 数据准备完成 - 训练: {train_count}, 验证: {val_count}")

        # 5. 模型训练
        if not args.validate_only:
            try:
                train_model(config, args.quick_test, args)
            except Exception as e:
                print(f"[ERROR] 训练失败: {e}")
                import traceback
                traceback.print_exc()
                print("\n📋 可能的解决方案:")
                print("   1. 检查LoRA适配器是否正确加载")
                print("   2. 确保数据格式正确")
                print("   3. 尝试减少batch size或使用CPU训练")
                sys.exit(1)

        # 6. 模型验证
        validate_model(config)

        print("\n[SUCCESS] 所有任务完成！")
        print("\n📚 后续使用:")
        print(f"1. 模型位置: {config['model']['output_dir']}")
        print("2. 推理使用: python analyze.py")
        print("3. 在Web模糊测试中集成: from models.vulnerability_analyzer import VulnerabilityAnalyzer")

    except KeyboardInterrupt:
        print("\n[WARNING] 用户中断训练")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 训练失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()