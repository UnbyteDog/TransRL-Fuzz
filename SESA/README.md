**语义增强静态分析阶段（Semantic-Enhanced Static Analysis Phase）**

通过污点分析与轻量级Transformer的协同，解决传统静态分析对新型漏洞特征（如编码拼接、间接变量传递）的漏报问题。

Transformer模型学习代码语义特征，输出风险概率并与污点分析结果融合，生成高风险分支表与插桩指导文件。
