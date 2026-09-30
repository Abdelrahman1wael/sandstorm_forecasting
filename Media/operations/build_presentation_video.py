import os
import sys
import json
import asyncio
import subprocess
import requests
# pyrefly: ignore [missing-import]
import edge_tts
# pyrefly: ignore [missing-import]
from PIL import Image, ImageDraw, ImageFont

# Set working directory
BASE_DIR = r"c:\Users\hp\Desktop\China_project"
ASSETS_DIR = os.path.join(BASE_DIR, "video_assets")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "sand_dust_storm_ml_presentation.mp4")
SUBTITLES_SRT = os.path.join(BASE_DIR, "sand_dust_storm_subtitles.srt")

os.makedirs(ASSETS_DIR, exist_ok=True)

# 10 Scenes Definition based on user proposal
SCENES = [
    {
        "id": 1,
        "title": "Scene 1: Opening & Research Title",
        "tag": "RESEARCH FORMULATION",
        "time": "0:00–0:40",
        "image_url": "https://images.openai.com/static-rsc-4/CFnzD1QZby7fFtFaPjlJLDJLYwqznxstGCTVgBF4iOWdl-eF1QNCKfUAHtmjQvYAHkEUk8ILF8LDu3Uu8t0AOO3xAWr3qQwkLtBGNUBPngX93vnt-FL4sHh4FwA8GYxxs_s-wZlfwgpBZOFRpyXc8ueNc5hw1vHlCS4gFcdaBlA?purpose=inline",
        "image_caption": "Severe dust storm wall sweeping across arid terrain and transportation corridors",
        "voiceover": "Imagine a massive sandstorm traveling hundreds of kilometers, reducing visibility, disrupting transportation, threatening public health, and affecting millions of people. What if we could predict such an event not just a few hours in advance, but several days or even weeks before it happens? This is the central question behind our research, titled: Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting. This research explores how artificial intelligence and multi-source environmental data can help improve the accuracy, reliability, and lead time of sandstorm forecasting.",
        "key_points": [
            "Research Question: How can AI bridge the medium- to long-term predictability gap?",
            "Forecasting Horizon: 3 to 15 days extended-range, monthly & seasonal trends",
            "Multi-source heterogeneous environmental data & physical constraints",
            "Target: Minimize socioeconomic disruption & protect public health"
        ],
        "tags": ["Medium-to-Long Term", "AI Forecasting", "Public Safety", "USTB Research"]
    },
    {
        "id": 2,
        "title": "Scene 2: Research Background & Problem Statement",
        "tag": "GLOBAL & REGIONAL HAZARDS",
        "time": "0:40–1:35",
        "image_url": "https://images.openai.com/static-rsc-4/5f8HiMHKxTLh3nIAVcC2ABeZ237raUMUzok-s5vtQbDw6Pl4szqknCLIwryMuikHcOxcUlKXx8VZT-D9JfncsBbg6GxYAhhSQaThKcRKbLngeBriIMRVxTxGHpMeSr2Lc55GvwMYe5VlnVQOhGa9Bc-49Ptc_31BFp3IMUs9c4s?purpose=inline",
        "image_caption": "Satellite observation of long-distance transboundary dust plume migration",
        "voiceover": "Sand and dust storms are among the major environmental hazards associated with extreme weather and climate events. According to the research proposal, nearly 330 million people across 151 countries are affected by sandstorms worldwide. In China, northern arid and semi-arid regions are major sources of dust. However, these storms can travel long distances, affecting central, eastern, and even southern regions. Their consequences include reduced visibility, transportation accidents, air pollution, respiratory and cardiovascular health risks, agricultural damage, and land degradation. Traditional forecasting methods rely heavily on numerical weather prediction models that simulate atmospheric and physical processes. Although these models are essential, they face challenges in computational cost, nonlinear interactions, and forecasting accuracy over extended time periods. As the forecast lead time increases, predicting the timing, intensity, and trajectory of sandstorms becomes increasingly difficult. This creates a critical need for intelligent forecasting systems that can provide earlier and more reliable warnings.",
        "key_points": [
            "Global Impact: 330M people across 151 countries affected worldwide",
            "Source Regions: Taklimakan, Gobi, northern arid corridors in China",
            "Severe Hazards: PM10/PM2.5 spikes, transportation halts, cardiovascular risk",
            "NWP Bottleneck: High computational cost, rapid error accumulation beyond 72h",
            "Critical Need: Intelligent early-warning systems with extended lead times"
        ],
        "tags": ["330M Affected", "Numerical Weather Prediction", "Lead Time Decay", "Error Compounding"]
    },
    {
        "id": 3,
        "title": "Scene 3: Research Motivation & Significance",
        "tag": "THEORETICAL & PRACTICAL VALUE",
        "time": "1:35–2:20",
        "image_url": "https://images.openai.com/static-rsc-4/Ex_xAr3w3ZAiwyq2Z8otwd91gaNKO3tIGrfES5iLjax1A-dNBYVkwhsGP3oydg_hM6Ev18nhdY1-lt1ySG_6-3vgN7p-g41ptoyqio5r2zWV8l7dxfw8fd6G9RM9AJMeVceeSpi-S_y41hkqm6y_lkBBd1XtNnRvCnIYcWg_KyE?purpose=inline",
        "image_caption": "Advanced meteorological modeling & AI-GAMFS high-resolution forecasting",
        "voiceover": "Machine learning provides a promising opportunity to address these challenges. By learning patterns from historical observations, satellite imagery, climate reanalysis, and numerical forecasts, machine learning models can identify complex relationships that may be difficult to capture through conventional methods alone. The research proposal highlights recent advances in artificial intelligence-based meteorological forecasting, including the AI-GAMFS system, as evidence of the growing potential of AI in environmental meteorology. However, applying these technologies to medium- and long-term sandstorm prediction remains an important research challenge. The significance of this study is both theoretical and practical. Theoretically, it aims to improve our understanding of the environmental and atmospheric factors influencing sandstorm activity. Practically, it aims to support disaster preparedness, public health protection, transportation planning, renewable energy management, and environmental governance.",
        "key_points": [
            "AI Meteorology Paradigm: Pattern extraction from petabyte reanalysis data",
            "State of the Art: AI-GAMFS demonstrates AI prowess in global weather modeling",
            "Theoretical Depth: Disentangling nonlinear dust emission & boundary dynamics",
            "Practical Benefits: Early civil defense, solar/wind farm management, healthcare alerts"
        ],
        "tags": ["AI-GAMFS", "Pattern Recognition", "Disaster Preparedness", "Green Energy Protection"]
    },
    {
        "id": 4,
        "title": "Scene 4: Literature Review & Current Research",
        "tag": "CHRONOLOGICAL ADVANCEMENTS",
        "time": "2:20–3:30",
        "image_url": "https://images.openai.com/static-rsc-4/PdOgFdPe0Rtb7mZyDoSt4OZWKcL1z8v3AKdgEfK-iFcJ72VKR34MBAG38ap7rFW7WbP1XShmI-a2EaD8wbafGFPhjYdy21SHg4jwWCagtpNPH11HHUwzpoQppmJPKnRyiKaZO6_zSJq2y0z1Cz_zoArKJ80PdjUp0UWBEnpA0Mg?purpose=inline",
        "image_caption": "Evolutionary timeline from shallow ML models to Spatiotemporal Deep Learning",
        "voiceover": "Previous research has explored a wide range of machine learning techniques for sandstorm prediction. Early studies used artificial neural networks and support vector machines to predict sandstorm occurrence based on meteorological observations. Later research introduced methods such as Random Forest, AdaBoost, and synthetic minority oversampling to address the problem of imbalanced datasets, where sandstorm events are much less frequent than normal weather conditions. With the development of deep learning, researchers began applying convolutional neural networks to extract spatial features from atmospheric data and satellite images. Other studies explored transfer learning, ensemble learning, and hybrid architectures combining convolutional neural networks with long short-term memory networks. These approaches have demonstrated improvements in short-term identification, classification, and sandstorm movement prediction. In the broader meteorological field, models such as LSTM, Transformers, and Graph Neural Networks have also shown potential in capturing temporal dependencies and spatial relationships. Nevertheless, the literature review identifies several important research gaps. Most existing sandstorm studies focus on short-term forecasting. Multi-source data fusion remains insufficiently developed, advanced spatiotemporal models require further investigation, and standardized datasets and evaluation frameworks are still lacking. These gaps motivate the direction of the proposed research.",
        "key_points": [
            "Early Phase: ANN & SVM for basic station binary classification",
            "Ensemble & Imbalance: Random Forest, AdaBoost, SMOTE oversampling",
            "Deep Learning: CNN-LSTM hybrids, spatial feature maps, transfer learning",
            "Frontier Models: Transformers & Graph Neural Networks (GNN) for teleconnections",
            "Identified Gaps: Lack of medium-term focus, weak data fusion, missing standard benchmarks"
        ],
        "tags": ["ANN & SVM", "CNN-LSTM", "SMOTE", "Transformers", "GNNs", "Literature Gaps"]
    },
    {
        "id": 5,
        "title": "Scene 5: Research Objectives & Scope",
        "tag": "THREE CORE PILLARS",
        "time": "3:30–4:20",
        "image_url": "https://images.openai.com/static-rsc-4/dPHeuCLaX1BgSpjfzknR9HNCoTIFXd7GytkbZDqF3AMMQI7HRaUQ0p2SnfOhiFsRsdpDC62K-DfHwwAwlVgIn1Ae8LmuhAlNolVlW2uHrjzhbrYpe01IX3ET-_ip8HGIsDCB6P6Pkejo3SJ7jjK-ptM1lyas8u0SU8P2hp6vNeo?purpose=inline",
        "image_caption": "Global & regional observation frameworks integrating remote sensing tensors",
        "voiceover": "The primary objective of this study is to develop a machine learning framework that improves the accuracy of medium- to long-term sandstorm forecasting. The research is organized into three main components. First, the construction of a unified forecasting dataset by integrating numerical weather forecasts, climate reanalysis, satellite remote sensing, and surface environmental information. Second, the development and comparison of machine learning models capable of predicting sandstorm risk probabilities and intensity. Third, the validation and interpretation of these models through rigorous evaluation, representative case studies, and analysis of the physical factors influencing their predictions. The target forecasting scales include three to fifteen days, as well as monthly and seasonal trends.",
        "key_points": [
            "Component 1: Unified Multi-Source Spatiotemporal Dataset Architecture",
            "Component 2: Dual-Track Modeling (Line A: NWP Post-Processing + Line B: End-to-End Deep ML)",
            "Component 3: Physical Validation, Explainable AI (XAI), & Historical Case Studies",
            "Target Horizons: 3–15 days extended range, sub-seasonal, and seasonal trends"
        ],
        "tags": ["Unified Dataset", "Probability Mapping", "Intensity Prediction", "3-15 Days Scale"]
    },
    {
        "id": 6,
        "title": "Scene 6: Methodology & Model Architecture",
        "tag": "TECHNICAL WORKFLOW",
        "time": "4:20–5:50",
        "image_url": "https://images.openai.com/static-rsc-4/tF_6xlDpD1_Pfghtx_zYkiYSElDozay6IpkJihsUlQ4GvRaCbPm3wwU-c1V68kwtyUggXLPSQ2-D06PdG0YpD1ZEGWCBpapSGP_m9CeheWUJqBdzrItDLllmKtBi9DdwgFRjI4DTfAIL12pyEq0La4-E3I-CM_vuemkKJGws7KA?purpose=inline",
        "image_caption": "Spatiotemporal neural network architecture with cross-attention & graph message passing",
        "voiceover": "The proposed methodology consists of several interconnected stages. The first stage is data collection and preprocessing. The study will collect multi-model numerical weather forecasts, ERA5 reanalysis data, satellite observations such as MODIS, and surface environmental parameters. These datasets will undergo quality control, missing-value handling, spatial and temporal alignment, and normalization. The second stage is feature engineering. Three categories of features will be constructed. The first includes dust emission conditions, such as soil moisture, vegetation cover, snow cover, bare land proportion, and friction wind speed. The second includes atmospheric dynamics and transport features, such as near-surface wind, wind shear, pressure fields, boundary layer height, and cold-air pathways. The third includes historical sandstorm information, including upstream dust concentration, event persistence, and spatial neighborhood relationships. The third stage is model development. Two main modeling directions will be investigated. The first is numerical weather prediction enhancement, using Random Forest, XGBoost, and other machine learning methods to correct systematic forecast errors. The second is end-to-end sandstorm risk and intensity forecasting, using LSTM, temporal convolutional networks, Transformers, and Graph Neural Networks. These models will be evaluated for their ability to capture temporal dependencies, spatial heterogeneity, and dust transport relationships.",
        "key_points": [
            "Stage 1: Multi-Modal Data Ingestion (ERA5, ECMWF, CMA, MODIS AOD, Soil moisture)",
            "Stage 2: 3-Tier Feature Engineering (Emission Dynamics, Atmospheric Transport, Upstream History)",
            "Track 1 (Line A): NWP Enhancement & Systematic Bias Correction (XGBoost, LightGBM)",
            "Track 2 (Line B): End-to-End Spatiotemporal Deep Learning (ConvLSTM, Transformer, GNN)",
            "Physical Coupling: Advection-diffusion transport graph network"
        ],
        "tags": ["ERA5 & MODIS", "Feature Engineering", "XGBoost", "Spatiotemporal GNN", "ConvLSTM"]
    },
    {
        "id": 7,
        "title": "Scene 7: Model Optimization & Evaluation",
        "tag": "VALIDATION & EXPLAINABILITY",
        "time": "5:50–6:50",
        "image_url": "https://images.openai.com/static-rsc-4/DYVuhzkBVzGYv7cOvKa_d9FePxZNF54wpcml9J7pkBbhJn_oNy71cR0lqWkMNNjFG8hXpK2nL51WXRedwkaL9OVKzwbC969uEZrQzM65tDHxDjjE_nUYKvQc5hN9DWohIPvabrhnUqEq8XLoFj8zrG0H_VGVPFix_reEmZLBpuk?purpose=inline",
        "image_caption": "Model optimization, loss convergence, and ROC-AUC performance verification",
        "voiceover": "An important challenge in sandstorm forecasting is the rarity of extreme events. To address this issue, the study will investigate resampling techniques, SMOTE-based event augmentation, and cost-sensitive learning. Probability calibration will also be applied to improve the reliability of the predicted risks. Model evaluation will combine event-based verification, regression error analysis, and probabilistic metrics, including the area under the receiver operating characteristic curve, or AUC. The proposed models will be compared against baseline numerical weather prediction systems. In addition, one to two representative severe sandstorm events will be selected for detailed case studies. Interpretability methods, including feature importance, SHAP analysis, and attention-weight visualization, will be used to investigate the factors contributing to model predictions. The final outputs are expected to include sandstorm risk probability maps, intensity forecasts, and an assessment of forecast performance as lead time increases.",
        "key_points": [
            "Extreme Event Imbalance: Resampling, SMOTE event augmentation, focal cost loss",
            "Comprehensive Metrics: Threat Score (TS), ETS, Brier Score, ROC-AUC, RMSE",
            "Benchmark Baselines: Operational CMA-T639, ECMWF IFS, persistence forecasts",
            "Explainable AI (XAI): SHAP value attribution, attention heatmaps, feature importance",
            "Deliverables: High-resolution risk probability grids & lead-time decay curves"
        ],
        "tags": ["SMOTE Augmentation", "ROC-AUC", "SHAP Attribution", "Lead-Time Analysis", "Case Study"]
    },
    {
        "id": 8,
        "title": "Scene 8: Innovation & Expected Contributions",
        "tag": "ACADEMIC & SOCIETAL IMPACT",
        "time": "6:50–7:40",
        "image_url": "https://images.openai.com/static-rsc-4/_ecvZKAmMlpHq2SUC8RETWKQ8F8W2opCFSaM2xXUrntNWY8ZuSqsUfekw854bS9PeAd44XiQEXOzof8gpAj88Oeq9NJ4DGr51nQQPwyOVv-0CFU3FsEzFC_H2Jtc66Z0fJ9UTLFVTSJkuNXMMumAuoRZesxo0ea87IPonNpigYA?purpose=inline",
        "image_caption": "Early warning civil defense and cross-regional disaster management systems",
        "voiceover": "The proposed research aims to contribute in three main areas. The first is multi-source data integration, creating a unified spatiotemporal dataset designed specifically for medium- to long-term sandstorm forecasting. The second is advanced model development, combining numerical forecast post-processing with deep learning architectures and strategies for handling rare events. The third is model interpretability and standardized evaluation, supporting more transparent and comparable forecasting results. From an application perspective, the research could contribute to earlier sandstorm warnings and more proactive risk management. Potential beneficiaries include meteorological departments, emergency management authorities, transportation operators, agricultural communities, renewable energy providers, and environmental protection agencies. The ultimate aim is to support a transition from reactive emergency response toward earlier, data-driven disaster preparedness.",
        "key_points": [
            "Contribution 1: First unified multi-modal 3–15d dust storm benchmark dataset",
            "Contribution 2: Novel hybrid model overcoming classical numerical predictability decay",
            "Contribution 3: Physics-informed interpretable framework validated by meteorologists",
            "Societal Value: Transition from reactive crisis response to proactive AI preparedness"
        ],
        "tags": ["Novel Benchmark", "Physics-Informed ML", "Early Warning", "Societal Resilience"]
    },
    {
        "id": 9,
        "title": "Scene 9: Research Implementation Timeline",
        "tag": "GANTT CHART & MILESTONES",
        "time": "7:40–8:20",
        "image_url": "https://images.openai.com/static-rsc-4/nGQM0xCoWCMTzsO__f71Htw-abOnTQVctN-ahlko2_-bL187c4lDdVUX9Ti2w0oeaXgnBc97-P7Hk4JoBJBTJDYFId60TH4crZGzTejFSMnumbwyefYwuOImn628TAxFYoNmXRZdNtDIw6xLmeed8sYIpP996B2KTS62BMBLLtY?purpose=inline",
        "image_caption": "Comprehensive master's research timeline from September 2025 to June 2027",
        "voiceover": "The research is planned across seven phases, from September 2025 to June 2027. The initial phases focus on literature review, research preparation, and construction of the multi-source dataset. From May to August 2026, the work focuses on baseline model development, preliminary experiments, and performance comparison. From September to December 2026, the study advances to ensemble learning, Graph Neural Networks, and physics-informed modeling. The subsequent phases cover case studies, interpretability analysis, manuscript preparation, dissertation completion, and pre-defense. The final stage, scheduled for June 2027, is the dissertation defense and graduation.",
        "key_points": [
            "Phase 1 & 2 (Sep 2025 – Apr 2026): Literature review, preparation & multi-source data pipeline",
            "Phase 3 (May 2026 – Aug 2026): Baseline models (RF, XGBoost, LSTM) & preliminary benchmarking",
            "Phase 4 (Sep 2026 – Dec 2026): Advanced Spatio-Temporal GNN & physics-informed coupling",
            "Phase 5 & 6 (Jan 2027 – May 2027): Severe storm case studies, paper submission & thesis writing",
            "Phase 7 (Jun 2027): Dissertation defense and master's graduation at USTB"
        ],
        "tags": ["7 Research Phases", "Sep 2025 - Jun 2027", "Milestones", "USTB Defense"]
    },
    {
        "id": 10,
        "title": "Scene 10: Conclusion & Scientific Outlook",
        "tag": "SUMMARY & FUTURE VISION",
        "time": "8:20–8:50",
        "image_url": "https://images.openai.com/static-rsc-4/dU_3jU-NNt_ivp_eH-rwPvJbr3HieiYpJxu48fILdepFlgSgULTF13-YOqSvy5BvNFkrln6z4BlSxr6O_GNpd7Y20VGn_958dXKBucjIz7HoPccyuAd213z0paLM2liem3O4uAvIlT7fqbTyoMicFMQrOglvlMr_PNH837svaOs?purpose=inline",
        "image_caption": "Sustainable environmental monitoring and future climate hazard mitigation",
        "voiceover": "In conclusion, this research seeks to combine machine learning, multi-source environmental data, and meteorological knowledge to address the challenges of medium- to long-term sandstorm forecasting. By integrating advanced algorithms with physical and environmental information, the study aims to improve forecasting accuracy, extend warning lead times, and enhance the interpretability of intelligent forecasting systems. Through these efforts, the research aspires to contribute to scientific understanding, environmental protection, and more effective disaster prevention and mitigation. Thank you for watching.",
        "key_points": [
            "Synthesis: AI + Multi-Source Earth Observations + Atmospheric Physics",
            "Core Outcomes: Extended lead times, reduced forecasting error, transparent AI decisions",
            "Mission: Elevating environmental engineering & safeguarding human communities",
            "Department: USTB School of Energy and Environmental Engineering"
        ],
        "tags": ["Intelligent Meteorology", "Extended Lead Time", "Environmental Protection", "Thank You"]
    }
]

# Download images
def download_images():
    headers = {"User-Agent": "Mozilla/5.0"}
    for scene in SCENES:
        img_path = os.path.join(ASSETS_DIR, f"img_{scene['id']:02d}.jpg")
        if not os.path.exists(img_path) or os.path.getsize(img_path) == 0:
            print(f"Downloading image for Scene {scene['id']}...")
            try:
                r = requests.get(scene['image_url'], headers=headers, timeout=20)
                if r.status_code == 200:
                    with open(img_path, "wb") as f:
                        f.write(r.content)
                    print(f"Saved {img_path}")
            except Exception as e:
                print(f"Error downloading {scene['image_url']}: {e}")

async def generate_scene_audio(scene, voice="en-US-ChristopherNeural", rate="+0%"):
    audio_path = os.path.join(ASSETS_DIR, f"audio_{scene['id']:02d}.mp3")
    print(f"Synthesizing audio for Scene {scene['id']} with {voice}...")
    try:
        communicate = edge_tts.Communicate(scene["voiceover"], voice, rate=rate)
        await communicate.save(audio_path)
        print(f"Generated {audio_path}")
    except Exception as err:
        print(f"edge-tts failed ({err}), falling back to Windows SAPI TTS...")
        wav_path = os.path.join(ASSETS_DIR, f"audio_{scene['id']:02d}.wav")
        ps_cmd = f"""
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.SetOutputToWaveFile('{wav_path}')
$synth.Speak(@'
{scene["voiceover"]}
'@)
$synth.Dispose()
"""
        subprocess.run(["powershell", "-Command", ps_cmd], check=True)
        # convert wav to mp3 with ffmpeg
        ffmpeg_bin = r"C:\msys64\mingw64\bin\ffmpeg.exe"
        subprocess.run([ffmpeg_bin, "-y", "-i", wav_path, "-b:a", "192k", audio_path], check=True)
        print(f"Generated via SAPI fallback: {audio_path}")

async def generate_all_audios():
    for scene in SCENES:
        audio_path = os.path.join(ASSETS_DIR, f"audio_{scene['id']:02d}.mp3")
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            await generate_scene_audio(scene)

# Get audio duration using ffprobe
def get_audio_duration(file_path):
    ffprobe_cmd = r"C:\msys64\mingw64\bin\ffprobe.exe"
    if not os.path.exists(ffprobe_cmd):
        ffprobe_cmd = "ffprobe"
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except:
        return 20.0

# Render 1920x1080 Academic Presentation Slide
def create_slide_image(scene, output_path):
    width, height = 1920, 1080
    im = Image.new("RGB", (width, height), color="#090d16")
    draw = ImageDraw.Draw(im)

    # Gradient background styling
    for y in range(height):
        # subtle deep navy to dark slate
        r = int(9 + (15 - 9) * (y / height))
        g = int(13 + (25 - 13) * (y / height))
        b = int(22 + (42 - 22) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Decorative top glowing banner
    draw.rectangle([(0, 0), (width, 8)], fill="#3b82f6")
    draw.rectangle([(0, 8), (width // 3, 10)], fill="#60a5fa")

    # Load system fonts
    try:
        font_univ = ImageFont.truetype("arialbd.ttf", 26)
        font_tag = ImageFont.truetype("arialbd.ttf", 20)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_heading = ImageFont.truetype("arialbd.ttf", 32)
        font_body = ImageFont.truetype("arial.ttf", 26)
        font_bullet = ImageFont.truetype("arialbd.ttf", 28)
        font_caption = ImageFont.truetype("arial.ttf", 20)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_univ = font_tag = font_title = font_heading = font_body = font_bullet = font_caption = font_badge = ImageFont.load_default()

    # Header Bar
    # University & Department Badge
    draw.rectangle([(80, 40), (80 + 380, 82)], fill="#1e293b", outline="#334155", width=1)
    draw.text((95, 48), "🏛️ 北京科技大学 • USTB Research", fill="#38bdf8", font=font_univ)
    draw.text((480, 48), "Master's Thesis Proposal • Environmental Engineering", fill="#94a3b8", font=font_univ)

    # Scene Badge Right
    scene_num_txt = f"SCENE {scene['id']:02d} OF 10  |  {scene['time']}"
    draw.rectangle([(width - 480, 40), (width - 80, 82)], fill="#1e293b", outline="#3b82f6", width=1)
    draw.text((width - 460, 48), scene_num_txt, fill="#60a5fa", font=font_badge)

    # Divider line
    draw.line([(80, 105), (width - 80, 105)], fill="#1e293b", width=2)

    # Scene Tag / Phase
    draw.rectangle([(80, 130), (80 + 260, 168)], fill="#172554", outline="#2563eb", width=1)
    draw.text((95, 136), f"⚡ {scene['tag']}", fill="#93c5fd", font=font_tag)

    # Scene Title
    draw.text((80, 185), scene["title"].split(": ", 1)[-1], fill="#f8fafc", font=font_title)

    # Layout: Left side (Key Concepts & Narrative Architecture) | Right side (Visual Diagram & Card)
    left_x = 80
    left_w = 980
    card_y = 275

    # Main Left Card
    draw.rectangle([(left_x, card_y), (left_x + left_w, 880)], fill="#0f172a", outline="#1e293b", width=2)
    # Header inside card
    draw.rectangle([(left_x, card_y), (left_x + left_w, card_y + 60)], fill="#1e293b")
    draw.text((left_x + 30, card_y + 14), "CORE RESEARCH PROPOSAL HIGHLIGHTS", fill="#e2e8f0", font=font_heading)

    # Key Points Bullets
    curr_y = card_y + 90
    for pt in scene["key_points"]:
        # Bullet marker
        draw.rectangle([(left_x + 30, curr_y + 8), (left_x + 44, curr_y + 22)], fill="#38bdf8")
        
        # Word wrapping for text
        words = pt.split(" ")
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 56:
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
        
        for l_idx, line in enumerate(lines):
            color = "#f1f5f9" if l_idx == 0 else "#cbd5e1"
            draw.text((left_x + 60, curr_y), line, fill=color, font=font_bullet if l_idx == 0 else font_body)
            curr_y += 36
        curr_y += 18

    # Tags along bottom of left card
    tag_x = left_x + 30
    tag_y = 810
    draw.text((tag_x, tag_y), "Key Attributes:", fill="#64748b", font=font_tag)
    tag_x += 160
    for t in scene["tags"][:4]:
        tw = len(t) * 11 + 24
        draw.rectangle([(tag_x, tag_y - 4), (tag_x + tw, tag_y + 30)], fill="#1e293b", outline="#3b82f6", width=1)
        draw.text((tag_x + 12, tag_y + 2), t, fill="#93c5fd", font=font_tag)
        tag_x += tw + 15

    # Right side: Image Card
    right_x = left_x + left_w + 40
    right_w = width - right_x - 80
    img_card_y = card_y

    draw.rectangle([(right_x, img_card_y), (right_x + right_w, 880)], fill="#0f172a", outline="#1e293b", width=2)
    # Header inside image card
    draw.rectangle([(right_x, img_card_y), (right_x + right_w, img_card_y + 60)], fill="#1e293b")
    draw.text((right_x + 25, img_card_y + 14), "SCIENTIFIC VISUALIZATION", fill="#e2e8f0", font=font_heading)

    # Load and place image
    img_path = os.path.join(ASSETS_DIR, f"img_{scene['id']:02d}.jpg")
    if os.path.exists(img_path):
        try:
            sci_img = Image.open(img_path).convert("RGB")
            # Target image area
            img_target_w = right_w - 40
            img_target_h = 440
            
            # Aspect ratio resize
            sci_img.thumbnail((img_target_w, img_target_h), Image.Resampling.LANCZOS)
            img_box_x = right_x + 20 + (img_target_w - sci_img.width) // 2
            img_box_y = img_card_y + 80 + (img_target_h - sci_img.height) // 2
            
            # Place image
            im.paste(sci_img, (img_box_x, img_box_y))
            # Border around image
            draw.rectangle([(img_box_x - 1, img_box_y - 1), (img_box_x + sci_img.width + 1, img_box_y + sci_img.height + 1)], outline="#38bdf8", width=1)
        except Exception as e:
            print(f"Error drawing image {img_path}: {e}")

    # Image Caption Box
    caption_y = img_card_y + 550
    draw.rectangle([(right_x + 20, caption_y), (right_x + right_w - 20, 850)], fill="#1e293b", outline="#334155", width=1)
    draw.text((right_x + 35, caption_y + 15), "Visual Context & Empirical Scope:", fill="#38bdf8", font=font_badge)
    
    # Wrap caption text
    c_words = scene["image_caption"].split(" ")
    c_lines = []
    c_cur = []
    for cw in c_words:
        c_cur.append(cw)
        if len(" ".join(c_cur)) > 42:
            c_cur.pop()
            c_lines.append(" ".join(c_cur))
            c_cur = [cw]
    if c_cur:
        c_lines.append(" ".join(c_cur))
    
    c_text_y = caption_y + 50
    for cline in c_lines:
        draw.text((right_x + 35, c_text_y), cline, fill="#cbd5e1", font=font_caption)
        c_text_y += 26

    # Bottom Footer Bar (Subtitles / Status Banner)
    draw.rectangle([(0, 930), (width, 1080)], fill="#020617")
    draw.line([(0, 930), (width, 930)], fill="#1e293b", width=2)
    
    # Active Closed Caption Preview
    draw.text((80, 955), "SPEECH NARRATION / CLOSED CAPTIONS:", fill="#60a5fa", font=font_badge)
    
    # Truncated narration line for preview
    preview_narration = scene["voiceover"][:140] + ("..." if len(scene["voiceover"]) > 140 else "")
    draw.text((80, 995), f"\"{preview_narration}\"", fill="#f1f5f9", font=font_body)
    
    # Progress indicator bar at bottom
    progress_w = int(width * (scene["id"] / 10.0))
    draw.rectangle([(0, 1072), (progress_w, 1080)], fill="#3b82f6")

    im.save(output_path, quality=95)
    print(f"Created slide: {output_path}")

# Generate SRT Subtitle file
def generate_srt(scene_durations):
    def format_time(seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    current_time = 0.0
    srt_entries = []
    entry_id = 1

    for scene in SCENES:
        dur = scene_durations.get(scene["id"], 25.0)
        text = scene["voiceover"]
        
        # Split voiceover into 2-3 sentence chunks for natural subtitle pacing
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if not sentences:
            sentences = [text]
            
        chunk_dur = dur / len(sentences)
        for s in sentences:
            s_text = s if s.endswith(".") else s + "."
            start_s = current_time
            end_s = current_time + chunk_dur
            
            srt_entries.append(f"{entry_id}\n{format_time(start_s)} --> {format_time(end_s)}\n{s_text}\n")
            entry_id += 1
            current_time = end_s

    with open(SUBTITLES_SRT, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    print(f"SRT subtitles generated at {SUBTITLES_SRT}")

# Main execution routine
async def main():
    print("=== Step 1: Downloading High-Resolution Scene Images ===")
    download_images()

    print("\n=== Step 2: Synthesizing English Academic Voiceover (edge-tts) ===")
    await generate_all_audios()

    print("\n=== Step 3: Measuring Audio Durations & Building Slides ===")
    scene_durations = {}
    for scene in SCENES:
        audio_file = os.path.join(ASSETS_DIR, f"audio_{scene['id']:02d}.mp3")
        dur = get_audio_duration(audio_file)
        # Add 0.5s padding so speech doesn't cut off abruptly
        scene_durations[scene['id']] = dur + 0.5
        print(f"Scene {scene['id']} duration: {dur:.2f}s (with padding: {dur + 0.5:.2f}s)")

        # Create slide image
        slide_file = os.path.join(ASSETS_DIR, f"slide_{scene['id']:02d}.png")
        create_slide_image(scene, slide_file)

    print("\n=== Step 4: Generating SRT Closed Captions ===")
    generate_srt(scene_durations)

    print("\n=== Step 5: Rendering Individual Scene Video Clips with FFmpeg ===")
    ffmpeg_bin = r"C:\msys64\mingw64\bin\ffmpeg.exe"
    if not os.path.exists(ffmpeg_bin):
        ffmpeg_bin = "ffmpeg"

    clip_files = []
    concat_list_path = os.path.join(ASSETS_DIR, "concat_list.txt")
    with open(concat_list_path, "w") as f_concat:
        for scene in SCENES:
            slide_file = os.path.join(ASSETS_DIR, f"slide_{scene['id']:02d}.png")
            audio_file = os.path.join(ASSETS_DIR, f"audio_{scene['id']:02d}.mp3")
            clip_file = os.path.join(ASSETS_DIR, f"clip_{scene['id']:02d}.mp4")
            dur = scene_durations[scene['id']]

            # FFmpeg render command: loop slide with audio, 1920x1080 @ 30fps
            cmd = [
                ffmpeg_bin, "-y",
                "-loop", "1",
                "-t", str(dur),
                "-i", slide_file,
                "-i", audio_file,
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-preset", "ultrafast",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                clip_file
            ]
            print(f"Rendering Clip {scene['id']} ({dur:.1f}s)...")
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                print(f"FFmpeg error on clip {scene['id']}: {res.stderr.decode('utf-8', errors='ignore')[:300]}")
            else:
                print(f"Clip {scene['id']} completed successfully.")
                clip_files.append(clip_file)
                f_concat.write(f"file '{clip_file.replace(os.sep, '/')}'\n")

    print("\n=== Step 6: Concatenating All Clips into Full Presentation Video ===")
    concat_cmd = [
        ffmpeg_bin, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        OUTPUT_VIDEO
    ]
    res_concat = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_concat.returncode == 0:
        print(f"\n[SUCCESS] Full Academic Presentation Video Created at: {OUTPUT_VIDEO}")
        print(f"Total Video Size: {os.path.getsize(OUTPUT_VIDEO) / (1024*1024):.2f} MB")
    else:
        print(f"Concat error: {res_concat.stderr.decode('utf-8', errors='ignore')[:300]}")

    # Export metadata JSON for interactive HTML5 Studio
    metadata_path = os.path.join(BASE_DIR, "video_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f_meta:
        json.dump({
            "title": "Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting",
            "institution": "University of Science and Technology Beijing (北京科技大学)",
            "video_file": "sand_dust_storm_ml_presentation.mp4",
            "subtitles_file": "sand_dust_storm_subtitles.srt",
            "total_duration_sec": sum(scene_durations.values()),
            "scenes": [
                {
                    **sc,
                    "duration": scene_durations[sc["id"]],
                    "slide_image": f"video_assets/slide_{sc['id']:02d}.png",
                    "audio_file": f"video_assets/audio_{sc['id']:02d}.mp3",
                    "clip_file": f"video_assets/clip_{sc['id']:02d}.mp4"
                }
                for sc in SCENES
            ]
        }, f_meta, indent=2)
    print(f"Saved video metadata to {metadata_path}")

if __name__ == "__main__":
    asyncio.run(main())
