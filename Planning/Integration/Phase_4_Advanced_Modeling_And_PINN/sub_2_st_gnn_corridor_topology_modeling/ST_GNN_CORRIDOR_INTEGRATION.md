# 🌐 Phase 4 • Subfolder 2: ST-GNN Corridor Topology Modeling
### *14-Node East Asian Graph Construction, Bidirectional Diffusion & Multi-Scale Fusion*
**Phase Horizon:** September 2026 – December 2026  
**Parent Phase:** Phase 4 (Advanced Modeling and Mid-Term Review)

---

## 🎯 1. Operational Goal & Corridor Graph Mapping

Phase 4.2 constructs the topological graph adjacency matrix $\mathbf{A} \in \mathbb{R}^{14 \times 14}$ linking the 14 major sandstorm source, corridor, and receptor cities across East Asia:

```
Nodes Index & Geographic Function:
├── Node 0: Taklamakan Desert (Primary western sand source)
├── Node 1: Badain Jaran Desert (Primary northern sand source)
├── Node 2: Dunhuang (Western corridor gate)
├── Node 3: Zhangye (Hexi Corridor bottleneck)
├── Node 4: Wuwei (Hexi Corridor exit)
├── Node 5: Tengger Desert (Central sand source)
├── Node 6: Yinchuan (Ningxia Plain crossing)
├── Node 7: Hohhot (Inner Mongolia pathway)
├── Node 8: Zhangjiakou (Northern mountain pass to Beijing)
├── Node 9: Yan'an (Loess Plateau transport)
├── Node 10: Beijing Capital (Major receptor megacity)
├── Node 11: Shijiazhuang / Jinan (North China Plain receptor)
├── Node 12: Xi'an / Guanzhong (Central plain receptor)
└── Node 13: Qinling Mountains / Chengdu Basin (Southern mountain barrier)
```

---

## 📐 2. Adjacency Weighting Formulation

Edge weights $A_{ij}$ are calculated combining geodesic distance $d_{ij}$ and alignment with dominant synoptic wind vectors $\theta_{\text{wind}}$:

$$A_{ij} = \exp\left(-\frac{d_{ij}^2}{2\sigma_d^2}\right) \cdot \max\left(0, \ \cos\left(\theta_{ij} - \bar{\theta}_{\text{wind}}\right)\right)$$

Self-loops ($A_{ii} = 1.0$) are added, and the matrix is row- and column-normalized into $P_{\text{fwd}}$ and $P_{\text{bwd}}$ for the 3-support Chebyshev diffusion layer.

---

## 📋 3. Phase 4.2 Deliverables
* Validated `st_gnn.py` module achieving lower multi-step error accumulation than standard RNNs across lead times $120\text{h} - 360\text{h}$.
