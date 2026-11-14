from pathlib import Path
from docx import Document
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver7.docx"

EN_P1 = (
    "Sand and dust storms (SDS) over the Arabian Peninsula—particularly across Greater Riyadh—pose severe hazards "
    "to aviation safety, respiratory health, solar generation, and urban infrastructure. To deliver reliable 1- to 15-day "
    "(24–360 h) forecasts, this thesis constructs a strictly causal 86,928-hour, 115-feature multi-modal dataset (2015–2024) "
    "fusing ground METAR telemetry, ERA5 boundary-layer physics, detrended satellite retrievals, CAMS aerosol fields, and "
    "seasonal dust-memory descriptors, partitioned chronologically (70%/15%/15%) with 360-hour purge gaps."
)
EN_P2 = (
    "A dual-pipeline architecture is evaluated across five horizons H ∈ {24, 72, 168, 216, 360} h and three random seeds. "
    "In Main Line A, calibrated tabular ensembles lead binary event discrimination on the untouched 2023–2024 test set, with "
    "RandomForest_Cal reaching Test ROC-AUC = 0.8090 (Lift@Top10% = 4.28×, BSS = 0.3218) at 24 h and XGBoost_Cal reaching "
    "0.7655 (PR-AUC = 0.8311) at 360 h, substantially outperforming Persistence_Cal (0.5701 and 0.4721). In Main Line B, "
    "PyTorch sequence and graph networks (RealLSTMNet, RealTransformerNet, RealPINNNet, RealSTGNNNet) achieve competitive "
    "calibrated classification (0.6817–0.7939 ROC-AUC) while halving continuous PM₁₀ regression error relative to non-trivial "
    "Line A models (LineB_STGNN RMSE = 14.86–21.55 μg/m³; LineB_LSTM = 14.13–14.45 μg/m³)."
)
EN_P3 = (
    "Finally, a six-module Explainable AI suite (XAI-1 to XAI-6) confirms physical realism: Ground_METAR (~37.4%), "
    "Calendar_Diurnal (~32.2%), and ERA5_Physics (~23.5%) dominate attributions—led by Shamal seasonal phase (sin_doy), "
    "multi-month dust memory, soil moisture, vapor pressure deficit, and gusts—while PyTorch LSTM saliency peaks at Lag 0 h, "
    "providing transparent operational guidance under inter-annual regime shifts."
)
EN_KW = (
    "Keywords: Sand and Dust Storm Forecasting; Explainable AI (XAI); Physics-Informed Neural Network (PINN); "
    "Spatiotemporal Graph Neural Network (ST-GNN); Calibrated Ensemble Learning; Greater Riyadh"
)

ZH_P1 = (
    "阿拉伯半岛尤其是大利雅得地区频发的沙尘暴（SDS）对航空安全、呼吸系统健康、光伏发电和城市基础设施构成严重威胁。"
    "为实现可靠的1至15天（24—360小时）预报，本文构建了严格因果的86,928小时、115维多模态数据集（2015—2024年），"
    "融合地面METAR观测、ERA5边界层物理场、去趋势卫星反演、CAMS气溶胶场及季节性沙尘记忆特征，"
    "并采用70%/15%/15%时间顺序划分与360小时隔离带（purge gap）防止数据泄露。"
)
ZH_P2 = (
    "双通道架构在五个预报时效 H ∈ {24, 72, 168, 216, 360} h 和三个随机种子下进行了系统评估。"
    "在主线A中，校准表格集成模型在2023—2024年独立测试集上的二分类判别能力领先：RandomForest_Cal在24 h取得"
    "Test ROC-AUC = 0.8090（Lift@Top10% = 4.28×，BSS = 0.3218），XGBoost_Cal在360 h达到0.7655（PR-AUC = 0.8311），"
    "显著优于Persistence_Cal基线（0.5701和0.4721）。在主线B中，PyTorch时序与图神经网络（RealLSTMNet、RealTransformerNet、"
    "RealPINNNet、RealSTGNNNet）不仅保持了稳健的概率分类性能（ROC-AUC = 0.6817—0.7939），还将连续PM₁₀回归误差较"
    "主线A非平凡机器学习模型降低约一半（LineB_STGNN RMSE = 14.86—21.55 μg/m³；LineB_LSTM = 14.13—14.45 μg/m³）。"
)
ZH_P3 = (
    "最后，六模块可解释人工智能审计（XAI-1至XAI-6）验证了模型的物理真实性：Ground_METAR（约37.4%）、"
    "Calendar_Diurnal（约32.2%）和ERA5_Physics（约23.5%）主导全局归因——以夏马风季节相位（sin_doy）、"
    "多月沙尘记忆、土壤湿度、饱和水汽压差及阵风为核心驱动——同时PyTorch LSTM梯度显著性在Lag 0 h达到峰值，"
    "为年际沙尘模态变化下的业务预警提供了透明可靠的决策支持。"
)
ZH_KW = (
    "关键词：沙尘暴预报；可解释人工智能（XAI）；物理信息神经网络（PINN）；时空图神经网络（ST-GNN）；概率校准集成；大利雅得"
)


def set_para_text(p, text, font_size=11):
    p.text = ""
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(font_size)


def main():
    doc = Document(str(DOC_PATH))
    set_para_text(doc.paragraphs[43], EN_P1)
    set_para_text(doc.paragraphs[44], EN_P2)
    set_para_text(doc.paragraphs[45], EN_P3)
    set_para_text(doc.paragraphs[46], EN_KW)

    set_para_text(doc.paragraphs[49], ZH_P1)
    set_para_text(doc.paragraphs[50], ZH_P2)
    set_para_text(doc.paragraphs[51], ZH_P3)
    set_para_text(doc.paragraphs[52], ZH_KW)

    try:
        doc.save(str(DOC_PATH))
        print(f"Updated Abstract (EN + ZH) in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver8.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
