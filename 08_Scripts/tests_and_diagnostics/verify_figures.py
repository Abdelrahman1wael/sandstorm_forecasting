from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

figs = [
    PROJECT_ROOT / 'figures/thesis/fig1_data_architecture_and_spatial_domain.png',
    PROJECT_ROOT / 'figures/thesis/fig2_yeo_johnson_distribution_balancing.png',
    PROJECT_ROOT / 'figures/thesis/fig3_line_a_nwp_bias_correction.png',
    PROJECT_ROOT / 'figures/thesis/fig4_line_b_models_and_pinn_loss.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai1_global_and_permutation_importance.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai2_shap_global_beeswarm.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai2_shap_local_waterfall.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai3_pdp_ice_curves.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai3_2d_interaction_pdp.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai4_surrogate_and_counterfactual_sensitivity.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai5a_transformer_4head_attention.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai5b_lstm_gate_dynamics.png',
    PROJECT_ROOT / 'figures/thesis/xai/xai6_stgnn_spatial_and_modality_attribution.png',
    PROJECT_ROOT / 'data/meta_model/results/roc_curves.png',
]

for p in figs:
    print(f'{p.name}: exists={p.exists()}, size={p.stat().st_size if p.exists() else 0} bytes')
