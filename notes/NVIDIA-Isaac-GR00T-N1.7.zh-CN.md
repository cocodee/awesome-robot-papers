# NVIDIA Isaac GR00T N1.7

## 元数据

- 来源：https://github.com/NVIDIA/Isaac-GR00T/blob/main/README.md
- 本地文档：[../papers/NVIDIA-Isaac-GR00T-N1.7.md](../papers/NVIDIA-Isaac-GR00T-N1.7.md)
- 类型：GitHub README / 模型发布文档
- 相关论文：GR00T N1: An Open Foundation Model for Generalist Humanoid Robots，arXiv:2503.14734
- 状态：Early Access 发布

## 研究问题

这份文档展示的是 GR00T N1.7 作为开放 VLA 机器人模型栈的使用方式。核心问题不是单个算法公式，而是：如何把一个预训练的 vision-language-action 模型适配到不同机器人本体、不同数据集和真实部署流程中。

## 核心方法

GR00T N1.7 把视觉语言基础模型和 diffusion transformer 动作头结合起来。模型输入语言、图像、机器人状态和本体配置，输出连续动作块。它支持基础模型推理、微调 checkpoint、自定义机器人微调、open-loop 评估、基于 ZMQ 的 PolicyServer 闭环部署，以及 ONNX / TensorRT 加速。

## 关键创新

- 新 VLM 骨干：用 Cosmos-Reason2-2B / Qwen3-VL 替代 N1.6 的 Eagle backbone。
- 相对末端执行器动作空间：把动作表示为相对当前位姿的 delta，而不是绝对目标位姿，有利于跨本体泛化。
- 人类视频预训练：N1.7 使用 20K 小时 EgoScale 人类视频数据，并结合多样化机器人示教。
- 商业可用：代码采用 Apache 2.0，模型权重使用 NVIDIA Open Model License。
- 工程闭环完整：支持 Hugging Face checkpoint、LeRobot 风格数据集、PolicyServer 推理、ONNX 和 TensorRT 导出。

## 实际解决的问题

GR00T N1.7 解决的是“基础 VLA 模型如何落到真实机器人策略”的问题。它给出了从机器人示教数据、数据格式转换、本体标签、modality 配置、微调、评估到部署的完整路径。

它也针对跨机器人本体泛化做了改进。relative EEF action 让机器人数据和人类操作视频更容易对齐，因此模型可以把人类视频中的操作先验迁移到机器人控制中。

## 实验证据

README 没有给出完整 benchmark 表格。它声明 N1.7 相比 N1.6 保持相近性能，同时提升泛化和语言跟随能力；并提供了 LIBERO、DROID、SimplerEnv Bridge、SimplerEnv Fractal 的微调 checkpoint。文档还提供了 `NEW_EMBODIMENT` 自定义本体微调流程，以及 SO100 示例数据集。

## 局限性

这是 Early Access 版本，稳定性和支持承诺有限。推理至少需要 16 GB 显存，微调建议 40 GB 以上显存。该 README 是工程使用文档，不是 N1.7 的完整论文，因此缺少详细消融实验、完整 benchmark 数字和失败案例分析。

## 应用到我的机器人

如果我的机器人需要语言条件下的操作能力，并且可以采集示教数据，GR00T N1.7 很值得作为基线。实际路线是：

- 把机器人示教转换成 GR00T LeRobot v2 格式，并提供 `meta/modality.json`；
- 用 modality config 明确定义 state、action 和 camera key；
- 从 `nvidia/GR00T-N1.7-3B` 开始，用 `NEW_EMBODIMENT` 做微调；
- 先用 open-loop evaluation 对比预测动作和真实动作；
- 再通过 PolicyServer 接入机器人控制器做闭环测试。

如果我的机器人是类人或全身控制平台，`UNITREE_G1_SONIC` 路线尤其值得关注。它把 VLA 输出的紧凑 latent action 交给 learned whole-body controller，解码成腿、臂、手的协调关节命令。

## 实施建议

不要一开始就做生产部署。先用小数据集验证数据转换、动作维度、相机命名和归一化是否正确，再做 open-loop 评估。最关键的工程决策是动作表示：优先使用 relative EEF delta，并保证夹爪、腕部、底盘和相机坐标约定在训练和部署时完全一致。
