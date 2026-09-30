# 02 深度图网络与物理偏微分先验正则化规范 (Deep Learning & PINN Regularization)

本规范详述主线 B（AI-GAMFS 视觉主干、ST-GNN 空间图网络与物理信息神经网络 PINN）的防过拟合核心技术。深度模型拥有数百万可学习参数，在大气极端样本稀疏场景下极易发生“表象拟合与非物理外推”，必须通过物理机理先验与现代深度学习正则化算子形成强归纳偏置。

---

## 1. 物理先验（PINN）作为无限样本正则化器 (Physics as an Infinite Regularizer)

### 1.1 纯数据驱动深度黑箱的病态外推缺陷
- **现象**：标准 ResNet/Transformer 在训练集上可能取得低 MSE，但在遇到历史未见的超强大风（如 $u_{10} > 30\text{ m/s}$）时，神经元的高维非线性激活会导致输出浓度出现无物理依据的数值暴增（达数万 $\mu\text{g/m}^3$）或负浓度异常。
- **物理约束机制**：PINN 不依赖海量标签标注，而是直接将流体力学物理偏微分方程嵌入损失函数，成为一个覆盖全解空间的“连续无监督正则化器”。

```
Loss_Total = Loss_Data(y_pred, y_obs) + λ_PINN * Loss_PDE(C, u, v, ...)
                                         ^
                                         | 
              [惩罚违背流体连续性与临界起沙的一切非物理假解]
```

### 1.2 欧文跃移门控函数（Owen Gate Regularizer）
严格将流体力学起沙临界速度作为激活门控，从数学结构上切断低风速下的虚假预测：
$$S_{\text{emission}} = c_s \cdot \text{ReLU}(u_* - u_{*t}) \cdot u_*^2 \cdot (1 - \text{SM})$$
- 当摩擦风速 $u_* \le u_{*t}$ 时，$\text{ReLU}(u_* - u_{*t}) \equiv 0$。模型在数学上被硬性剥夺了“在无起沙动力下预测高沙尘”的自由度，有效根除了微风天气下的高浓度误报。

### 1.3 连续性质量守恒残差惩罚
在网格节点上强制执行质量守恒偏微分方程（PDE）残差约束：
$$\mathcal{L}_{\text{PINN}} = \frac{1}{N_{grid}} \sum_{i,j} \left( \frac{\partial C}{\partial t} + u \frac{\partial C}{\partial x} + v \frac{\partial C}{\partial y} - K_h \nabla^2 C - S + D \right)^2$$
任何在无气流输入区域“凭空创生沙尘”或在无沉降条件下“凭空消灭沙尘”的梯度更新都会受到严厉的偏微分惩罚。

---

## 2. ST-GNN 空间图网络防过平滑与图记忆正则化 (DropEdge & DropNode)

### 2.1 图注意力过平滑（Over-smoothing）与邻域记忆
- **问题**：多层图卷积（GCN/GAT）随着网络深度增加，各节点的特征向量会逐渐收敛趋同（过平滑），失去各个城市自身的微环境特征；同时模型容易死记 14 个节点之间特定的几条历史传输路径。
- **解决机制：DropEdge（随机断边正则化）**：
  在每个训练 Batch 中，以概率 $p = 0.20$ 随机将邻接矩阵中的边权重置零。迫使网络在部分空间走廊被动态切断的情况下，依然能够利用其他通道推断气溶胶流动。

```python
import torch

def apply_drop_edge(adj_matrix: torch.Tensor, drop_prob: float = 0.2, training: bool = True) -> torch.Tensor:
    """
    随机断边正则化：训练阶段以概率 drop_prob 掩码部分边，评估阶段保留完整图拓扑。
    """
    if not training or drop_prob <= 0.0:
        return adj_matrix
    
    mask = torch.rand_like(adj_matrix) > drop_prob
    # 强制保留对角线自环 (Self-loop)
    diag_indices = torch.arange(adj_matrix.size(0))
    mask[diag_indices, diag_indices] = True
    
    return adj_matrix * mask.float()
```

---

## 3. 优化器权重衰减与梯度裁剪 (Weight Decay & Gradient Clipping)

### 3.1 权重衰减（AdamW L2 Regularization）
采用解耦权重衰减优化器 `AdamW`，避免标准 Adam 中动量项与 L2 正则化的耦合失真：
```python
import torch.optim as optim

optimizer = optim.AdamW(
    model.parameters(),
    lr=5e-4,
    weight_decay=1e-4,  # L2 正则化惩罚参数矩阵权重范数
    betas=(0.9, 0.999),
    eps=1e-8
)
```

### 3.2 动态梯度裁剪（Gradient Clipping）
沙尘暴爆发时目标值急剧跃变，极易反向传播产生异常巨大梯度，导致参数被破坏性更新：
```python
# 每个 batch 优化前强制裁剪梯度 L2 范数不超过 1.0
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()
```

---

## 4. 余弦退火动态学习率调度 (Cosine Annealing with Warmup)

在训练前 5 个 Epoch 实施线性热身（Linear Warmup），使网络各层适应物理损失的梯度尺度；随后实施余弦退火，防止模型在复杂多峰损失曲面上振荡发散：

```python
from torch.optim.lr_scheduler import LambdaLR
import math

def get_cosine_schedule_with_warmup(optimizer, num_warmup_epochs=5, num_training_epochs=100):
    def lr_lambda(current_epoch):
        if current_epoch < num_warmup_epochs:
            return float(current_epoch) / float(max(1, num_warmup_epochs))
        progress = float(current_epoch - num_warmup_epochs) / float(max(1, num_training_epochs - num_warmup_epochs))
        return max(0.01, 0.5 * (1.0 + math.cos(math.pi * progress)))
    return LambdaLR(optimizer, lr_lambda)
```

---

## 5. 多任务动态梯度平衡 (GradNorm & Uncertainty Weighting)

- **痛点**：若固定超参数 $\lambda_{PINN}$，训练早期物理损失可能远大于数据 MSE，导致网络只关注满足偏微分方程而忽略了观测数据的拟合。
- **解决方案**：引入基于各任务梯度范数的动态自适应加权机制（GradNorm），保证 $\mathcal{L}_{data}, \mathcal{L}_{PINN}, \mathcal{L}_{quantile}, \mathcal{L}_{focal}$ 四个损失在反向传播时维持同等数量级的梯度更新，避免单一任务过拟合或欠拟合。
