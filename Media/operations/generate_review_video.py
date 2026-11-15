import os
import sys
import json
import asyncio
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont

# Base directories
BASE_DIR = r"c:\Users\hp\Desktop\sandstorm_forecasting\Media"
ASSETS_DIR = os.path.join(BASE_DIR, "video_assets")
SLIDES_DIR = os.path.join(ASSETS_DIR, "slides")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
CLIPS_DIR = os.path.join(ASSETS_DIR, "clips")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
PRODUCTION_DIR = os.path.join(BASE_DIR, "production")

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(PRODUCTION_DIR, exist_ok=True)

FINAL_VIDEO = os.path.join(PRODUCTION_DIR, "sand_dust_storm_ml_presentation.mp4")
FINAL_SRT = os.path.join(PRODUCTION_DIR, "sand_dust_storm_subtitles.srt")
FINAL_METADATA = os.path.join(PRODUCTION_DIR, "video_metadata.json")

# 10 Detailed Scenes structured from "Review points.docx"
SCENES = [
    {
        "id": 1,
        "title": "Scene 1: Research Formulation & Title",
        "tag": "RESEARCH FORMULATION",
        "time": "0:00–0:40",
        "image_file": "img_01.jpg",
        "image_caption": "Severe dust storm wall advancing across arid transport corridors in Northern China",
        "voiceover": "Welcome to the research presentation on applying machine learning algorithms to improve the accuracy of medium- to long-term sand and dust storm forecasting. Sand and dust storms represent severe atmospheric hazards across arid and semi-arid regions of East Asia. This study, conducted at the University of Science and Technology Beijing, addresses the critical predictability gap at sub-seasonal to seasonal horizons, specifically from 3 to 15 days up to monthly trends. By integrating multi-modal observations, reanalysis data, and physics-constrained deep learning architectures, we establish an end-to-end framework to transform hazard warning from reactive emergency response to proactive scientific defense.",
        "key_points": [
            "Research Title: Applying ML Algorithms for Medium- to Long-Term SDS Forecasting",
            "Academic Institution: University of Science and Technology Beijing (USTB)",
            "Target Horizons: Extended-range 3 to 15 days, sub-seasonal and monthly trends",
            "Core Mission: Multi-modal fusion & physics-constrained deep learning architectures",
            "Strategic Goal: Shifting hazard management from reactive response to proactive defense"
        ],
        "tags": ["USTB Proposal", "3-15 Day Lead Time", "Atmospheric AI", "Hazard Mitigation"]
    },
    {
        "id": 2,
        "title": "Scene 2: Climate Change Drivers in China",
        "tag": "CLIMATE FORCING & DRIVERS",
        "time": "0:40–1:35",
        "image_file": "img_02.jpg",
        "image_caption": "Regional temperature anomalies, desiccation and satellite dust tracking over East Asia",
        "voiceover": "China is experiencing pronounced environmental shifts that alter dust storm frequency and intensity. First, extreme warming across the Mongolian Plateau and northern China causes rapid topsoil drying, making loose sediments easily mobilized into the air. Second, severe precipitation deficits and below-average snow cover throughout the Gobi Desert and Inner Mongolia deplete surface moisture. Third, more active spring Mongolian cyclones create intense gale-force wind systems capable of lifting massive dust plumes across thousands of kilometers. Furthermore, land degradation and agricultural expansion have stripped natural vegetative soil anchors, while long-term ecological projects such as the Three-North Shelter Forest are frequently overwhelmed by acute regional climate anomalies, as evidenced by the severe Harbin darkening events.",
        "key_points": [
            "Extreme Warming: Rapid temperature rise drying out Mongolian Plateau topsoil",
            "Moisture Deficits: Depleted spring snow cover & rainfall in Gobi & Inner Mongolia",
            "Cyclonic Forcing: High-velocity spring Mongolian cyclones lifting transboundary plumes",
            "Ecological Stress: Land degradation vs. afforestation defenses overwhelmed by anomalies",
            "Regional Extremes: Dramatic May and June storm surges turning northern cities pitch-dark"
        ],
        "tags": ["Mongolian Cyclones", "Topsoil Desiccation", "Three-North Forest", "Regional Warming"]
    },
    {
        "id": 3,
        "title": "Scene 3: Causes & Physical Mechanisms of SDS",
        "tag": "PHYSICAL & LAND MECHANISMS",
        "time": "1:35–2:25",
        "image_file": "img_03.jpg",
        "image_caption": "Geographic proximity of Gobi & Taklimakan Deserts and spring frontal wind systems",
        "voiceover": "Sand and dust storm initiation is governed by complex land-atmosphere couplings. Major source regions, including the vast Taklimakan Desert in northwestern China and the Gobi Desert across northern China and Mongolia, provide an abundant reservoir of fine mineral dust. When strong cold fronts and baroclinic atmospheric systems sweep across these arid expanses, surface friction velocity exceeds aerodynamic threshold levels, lifting fine sediments into the boundary layer. The availability of erodible particles is tightly coupled to antecedent conditions over days, months, and seasons, including soil moisture, surface roughness, temperature anomalies, and prolonged drought. Consequently, dust storms cannot be modeled as isolated instantaneous events, but as cross-scale physical phenomena driven by delayed environmental memory.",
        "key_points": [
            "Primary Sources: Vast sediment reservoirs in Taklimakan Desert and Gobi Desert",
            "Trigger Dynamics: Spring cold fronts, baroclinic systems & aerodynamic friction threshold",
            "Cross-Scale Memory: 1-to-12-month antecedent drought & soil moisture controls",
            "Nonlinear Couplings: Vegetation phenology and soil moisture governing sediment erodibility",
            "Forecast Horizon: Requires incorporating delayed environmental memory into AI models"
        ],
        "tags": ["Taklimakan & Gobi", "Threshold Friction Wind", "Cold Front Dynamics", "Lagged Drivers"]
    },
    {
        "id": 4,
        "title": "Scene 4: Multi-Scale Impacts & Public Health",
        "tag": "SOCIOECONOMIC HAZARDS",
        "time": "2:25–3:15",
        "image_file": "img_04.jpg",
        "image_caption": "Severe visibility drop, PM10/PM2.5 hazardous spikes and civil transportation disruption",
        "voiceover": "Sandstorms pose extraordinary challenges to societal operations and public health worldwide, impacting over 330 million people in 151 nations. In northern and eastern China, severe events cause near-zero visibility, plunging cities into daytime darkness, grounding commercial aviation, and causing catastrophic traffic disruption. High airborne concentrations of PM10 and PM2.5 trigger severe respiratory and cardiovascular morbidity. Epidemiological findings published in Nature Communications demonstrate substantial increases in hospital admissions and cause-specific mortality during dust outbreaks. Furthermore, toxic oxidative-potential components and persistent free radicals carried by mineral particles cause cellular damage, while deposition across agricultural zones ruins crop yields and exacerbates desertification.",
        "key_points": [
            "Global Reach: Over 330 million people affected across 151 countries worldwide",
            "Transportation Shutdown: Near-zero daytime visibility, flight groundings, highway closures",
            "Public Health Risk: Spikes in PM10 & PM2.5, respiratory & cardiovascular mortality",
            "Biochemical Toxicity: Mineral dust carries oxidative-potential components & free radicals",
            "Agricultural Damage: Farmland topsoil erosion, crop burial, and accelerated desertification"
        ],
        "tags": ["Public Health Hazard", "PM10 & PM2.5 Spikes", "Aviation Disruption", "Ecosystem Impact"]
    },
    {
        "id": 5,
        "title": "Scene 5: Traditional NWP & Bottlenecks",
        "tag": "NWP LIMITATIONS & BOTTLENECKS",
        "time": "3:15–4:05",
        "image_file": "img_05.jpg",
        "image_caption": "Chaotic error accumulation and boundary layer parameterization bottlenecks in NWP",
        "voiceover": "Operational dust forecasting has traditionally relied on numerical weather prediction models and chemical transport simulations. While these physical systems capture synoptic dynamics, they face critical operational bottlenecks. Initial atmospheric condition uncertainties, empirical dust-emission parameterizations, and boundary-layer turbulence approximations lead to rapid error accumulation. Because atmospheric flow is chaotic, numerical forecast accuracy decays sharply beyond 48 to 72 hours, rendering 3-to-15-day sub-seasonal forecasting highly unreliable. Furthermore, running multi-scale physical ensembles demands enormous computational resources, leaving emergency agencies with a post-event response posture rather than true proactive lead time.",
        "key_points": [
            "Physical Basis: Synoptic atmospheric transport & chemical dispersion modeling",
            "Critical Bottlenecks: Emission parameterization errors & boundary-layer uncertainties",
            "Predictability Barrier: Rapid chaotic error compounding beyond 48 to 72 hours",
            "Computational Barrier: Enormous computational cost preventing dense real-time ensembles",
            "Operational Result: Reliance on passive post-event responses instead of early warning"
        ],
        "tags": ["NWP Limitations", "Error Compounding", "Chaos Theory", "Lead-Time Decay"]
    },
    {
        "id": 6,
        "title": "Scene 6: The AI Revolution in Earth Systems",
        "tag": "MACHINE LEARNING REVOLUTION",
        "time": "4:05–4:55",
        "image_file": "img_06.jpg",
        "image_caption": "AI-GAMFS multi-element intelligent sensing and Google NeuralGCM deep modeling",
        "voiceover": "Machine learning offers a transformative paradigm to overcome the limitations of classical numerical prediction. By extracting high-dimensional nonlinear patterns from petabytes of satellite, surface, and atmospheric data, modern AI models learn complex relationships without rigid mathematical assumptions. Breakthrough systems such as AI-GAMFS and Google's NeuralGCM have demonstrated that data-driven architectures can match or exceed traditional atmospheric models in speed and precision. In sandstorm forecasting, machine learning models effectively integrate multi-modal heterogeneous inputs, identify slowly varying environmental memory signals, and correct systematic numerical biases.",
        "key_points": [
            "Data-Driven Paradigm: Mining high-dimensional nonlinear Earth observation records",
            "Frontier Milestones: AI-GAMFS and Google NeuralGCM show AI prowess in weather modeling",
            "Multi-Modal Integration: Fusing ground stations, satellite retrievals & reanalysis tensors",
            "Systematic Error Correction: Learning and eliminating numerical model biases",
            "Extended Horizon: Harnessing slowly varying climate memory for sub-seasonal outlooks"
        ],
        "tags": ["AI-GAMFS", "Google NeuralGCM", "Data-Driven Modeling", "Nonlinear Synergy"]
    },
    {
        "id": 7,
        "title": "Scene 7: Deep Learning Spatiotemporal Models",
        "tag": "ADVANCED MODEL ARCHITECTURES",
        "time": "4:55–5:55",
        "image_file": "img_07.jpg",
        "image_caption": "Spatiotemporal neural architectures: CNN-LSTM, Transformers, Bi-GRU and GNNs",
        "voiceover": "To capture both temporal persistence and spatial advection, our research investigates a comprehensive hierarchy of advanced deep learning architectures. For time-series dependencies, Long Short-Term Memory networks and Bidirectional Gated Recurrent Units with attention mechanisms retain multi-day environmental forcing. To model continuous spatial dust advection, Convolutional Neural Networks and Spatiotemporal Transformers capture multi-scale atmospheric flow fields. Most crucially, Graph Neural Networks represent the geographic topography and spatial propagation network of dust source regions, tracking plume transport along realistic meteorological corridors. For tabular and ensemble post-processing, gradient boosting models including XGBoost, CatBoost, and LightGBM provide robust bias correction.",
        "key_points": [
            "Recurrent Sequence Models: LSTM & Bi-GRU with attention for long-term temporal memory",
            "Spatiotemporal Attention: Transformers capture cross-scale atmospheric correlations",
            "Graph Neural Networks (GNN): Message passing across spatial dust propagation networks",
            "Gradient Boosting Ensembles: XGBoost, CatBoost & LightGBM for numerical post-processing",
            "Multi-Scale Representation: Jointly learning local emission thresholds and regional advection"
        ],
        "tags": ["Spatiotemporal GNN", "LSTM & Bi-GRU", "Transformers", "Gradient Boosting"]
    },
    {
        "id": 8,
        "title": "Scene 8: Physics-Informed ML & Interpretability",
        "tag": "PHYSICS CONSTRAINTS & XAI",
        "time": "5:55–6:50",
        "image_file": "img_08.jpg",
        "image_caption": "Physics-informed loss constraints (PINNs) and SHAP feature attribution heatmaps",
        "voiceover": "Pure data-driven models risk making unphysical predictions under extreme out-of-distribution conditions. To ensure physical validity, we incorporate physics-informed neural network principles by embedding atmospheric constraints, such as mass conservation and aerodynamic threshold friction velocities, directly into network loss functions. To ensure operational credibility for meteorologists, we employ Explainable AI methodologies. Using SHAP value attributions and neural attention weight visualizations, we quantitatively isolate the exact influence of soil moisture, wind shear, upstream dust loading, and surface roughness on every forecast decision, ensuring the model is trustworthy and scientifically sound.",
        "key_points": [
            "Physics-Informed Constraints: Embedding mass conservation & threshold friction velocity",
            "Physical Consistency: Constrained optimization prevents unphysical out-of-distribution output",
            "SHAP Value Attribution: Decomposing contributions of soil moisture, wind shear & temperature",
            "Attention Weight Heatmaps: Visualizing active dust transport corridors for forecasters",
            "Trust & Transparency: Enhancing scientific interpretability and operational adoption"
        ],
        "tags": ["PINNs", "Physical Constraints", "SHAP Framework", "Attention Visualization"]
    },
    {
        "id": 9,
        "title": "Scene 9: Methodology & 5-Step Pipeline",
        "tag": "EXPERIMENTAL METHODOLOGY",
        "time": "6:50–7:45",
        "image_file": "img_09.jpg",
        "image_caption": "End-to-end 5-step technical pipeline across four benchmark meteorological stations",
        "voiceover": "The core methodology is structured around five systematic steps evaluated across four benchmark meteorological stations in China. Step 1 acquires and harmonizes multi-source data from ECMWF, China Meteorological Administration stations, ERA5 reanalysis, and MODIS satellite retrievals. Step 2 constructs three feature tiers: surface emission conditions, dynamic transport features, and historical upstream memory. Step 3 develops our dual-track modeling framework: Line A for numerical bias correction and Line B for end-to-end spatiotemporal risk forecasting. Step 4 resolves extreme event class imbalance using SMOTE oversampling, cost-sensitive focal loss, and probability calibration. Step 5 conducts multi-metric validation using Threat Scores, ROC-AUC, and retrospective severe storm case studies.",
        "key_points": [
            "Data Integration: ECMWF, CMA 4 stations, ERA5 reanalysis & MODIS satellite tensors",
            "3-Tier Feature Engineering: Emission conditions, atmospheric transport & upstream memory",
            "Dual-Track Modeling: Line A (NWP Bias Correction) + Line B (End-to-End Deep Spatiotemporal)",
            "Class Imbalance Handling: SMOTE oversampling, cost-sensitive focal loss & calibration",
            "Comprehensive Validation: Threat Score (TS), ETS, ROC-AUC, and severe event case studies"
        ],
        "tags": ["5-Step Pipeline", "ERA5 & MODIS", "SMOTE & Cost Loss", "Threat Score Validation"]
    },
    {
        "id": 10,
        "title": "Scene 10: Milestones, Deliverables & Impact",
        "tag": "TIMELINE & SOCIETAL VALUE",
        "time": "7:45–8:35",
        "image_file": "img_10.jpg",
        "image_caption": "7-phase master's research timeline at USTB and early-warning societal resilience",
        "voiceover": "Spanning September 2025 through June 2027, the research roadmap culminates in a validated, operational-ready forecasting system and master's dissertation defense. The expected deliverables include high-resolution 3-to-15-day risk probability maps, an open benchmark dataset, and publication in top-tier environmental informatics journals. By extending warning lead times up to five full days, this intelligent framework empowers aviation scheduling, civil protection, and solar and wind energy infrastructure. In summary, uniting physics-informed AI with multi-source Earth observations will advance China's capacity to anticipate sandstorms and protect human communities. Thank you for your attention.",
        "key_points": [
            "7 Research Phases: September 2025 to June 2027 concluding with USTB thesis defense",
            "Core Deliverables: 3 to 15 day probabilistic risk grids, open benchmark & publications",
            "Civil Resilience: 5-day warning window protecting aviation, public health & green energy",
            "Decisive Shift: Moving environmental meteorology toward proactive AI resilience",
            "Department: USTB School of Energy and Environmental Engineering"
        ],
        "tags": ["USTB Timeline", "3-15d Outlooks", "Civil Protection", "Proactive Resilience"]
    }
]

# Audio Synthesis using edge-tts
async def generate_scene_audio(scene, voice="en-US-ChristopherNeural"):
    audio_path = os.path.join(AUDIO_DIR, f"audio_{scene['id']:02d}.mp3")
    print(f"Generating audio for Scene {scene['id']} using {voice}...")
    communicate = edge_tts.Communicate(scene["voiceover"], voice)
    await communicate.save(audio_path)
    print(f"Saved audio: {audio_path}")

async def generate_all_audios():
    for scene in SCENES:
        await generate_scene_audio(scene)

# Audio Duration via FFprobe
def get_audio_duration(file_path):
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
        return 35.0

# Render 1920x1080 Academic Slide
def create_slide_image(scene, output_path):
    width, height = 1920, 1080
    im = Image.new("RGB", (width, height), color="#090d16")
    draw = ImageDraw.Draw(im)

    # Gradient background styling (slate-navy)
    for y in range(height):
        r = int(9 + (15 - 9) * (y / height))
        g = int(13 + (25 - 13) * (y / height))
        b = int(22 + (42 - 22) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Top accent bar
    draw.rectangle([(0, 0), (width, 8)], fill="#3b82f6")
    draw.rectangle([(0, 8), (width // 3, 10)], fill="#60a5fa")

    # Load system fonts
    try:
        font_univ = ImageFont.truetype("arialbd.ttf", 26)
        font_tag = ImageFont.truetype("arialbd.ttf", 20)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_heading = ImageFont.truetype("arialbd.ttf", 30)
        font_body = ImageFont.truetype("arial.ttf", 25)
        font_bullet = ImageFont.truetype("arialbd.ttf", 26)
        font_caption = ImageFont.truetype("arial.ttf", 20)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_univ = font_tag = font_title = font_heading = font_body = font_bullet = font_caption = font_badge = ImageFont.load_default()

    # University Header Bar
    draw.rectangle([(80, 40), (80 + 380, 82)], fill="#1e293b", outline="#334155", width=1)
    draw.text((95, 48), "USTB Research • 北京科技大学", fill="#38bdf8", font=font_univ)
    draw.text((480, 48), "Master's Thesis Proposal • Environmental Engineering", fill="#94a3b8", font=font_univ)

    # Scene Badge Right
    scene_num_txt = f"SCENE {scene['id']:02d} OF 10  |  {scene['time']}"
    draw.rectangle([(width - 480, 40), (width - 80, 82)], fill="#1e293b", outline="#3b82f6", width=1)
    draw.text((width - 460, 48), scene_num_txt, fill="#60a5fa", font=font_badge)

    # Divider line
    draw.line([(80, 105), (width - 80, 105)], fill="#1e293b", width=2)

    # Scene Tag / Phase
    draw.rectangle([(80, 126), (80 + 320, 164)], fill="#172554", outline="#2563eb", width=1)
    draw.text((95, 132), f"SECTION: {scene['tag']}", fill="#93c5fd", font=font_tag)

    # Scene Title
    clean_title = scene["title"].split(": ", 1)[-1]
    draw.text((80, 180), clean_title, fill="#f8fafc", font=font_title)

    # Main Left Card: Highlights
    left_x = 80
    left_w = 980
    card_y = 265

    draw.rectangle([(left_x, card_y), (left_x + left_w, 880)], fill="#0f172a", outline="#1e293b", width=2)
    # Header inside card
    draw.rectangle([(left_x, card_y), (left_x + left_w, card_y + 55)], fill="#1e293b")
    draw.text((left_x + 30, card_y + 12), "COMPREHENSIVE REVIEW POINTS & FRAMEWORK", fill="#e2e8f0", font=font_heading)

    # Key Points Bullets
    curr_y = card_y + 80
    for pt in scene["key_points"]:
        # Bullet marker
        draw.rectangle([(left_x + 30, curr_y + 6), (left_x + 44, curr_y + 20)], fill="#38bdf8")
        
        words = pt.split(" ")
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 55:
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
        
        for l_idx, line in enumerate(lines):
            color = "#f1f5f9" if l_idx == 0 else "#cbd5e1"
            draw.text((left_x + 58, curr_y), line, fill=color, font=font_bullet if l_idx == 0 else font_body)
            curr_y += 34
        curr_y += 14

    # Tags along bottom of left card
    tag_x = left_x + 30
    tag_y = 825
    draw.text((tag_x, tag_y), "Key Concepts:", fill="#64748b", font=font_tag)
    tag_x += 160
    for t in scene["tags"][:4]:
        tw = len(t) * 11 + 24
        draw.rectangle([(tag_x, tag_y - 4), (tag_x + tw, tag_y + 28)], fill="#1e293b", outline="#3b82f6", width=1)
        draw.text((tag_x + 12, tag_y + 2), t, fill="#93c5fd", font=font_tag)
        tag_x += tw + 14

    # Right side: Visual Diagram & Card
    right_x = left_x + left_w + 40
    right_w = width - right_x - 80
    img_card_y = card_y

    draw.rectangle([(right_x, img_card_y), (right_x + right_w, 880)], fill="#0f172a", outline="#1e293b", width=2)
    draw.rectangle([(right_x, img_card_y), (right_x + right_w, img_card_y + 55)], fill="#1e293b")
    draw.text((right_x + 25, img_card_y + 12), "SCIENTIFIC VISUALIZATION", fill="#e2e8f0", font=font_heading)

    # Load and place image
    img_path = os.path.join(IMAGES_DIR, scene["image_file"])
    if os.path.exists(img_path):
        try:
            sci_img = Image.open(img_path).convert("RGB")
            img_target_w = right_w - 40
            img_target_h = 440
            sci_img.thumbnail((img_target_w, img_target_h), Image.Resampling.LANCZOS)
            img_box_x = right_x + 20 + (img_target_w - sci_img.width) // 2
            img_box_y = img_card_y + 75 + (img_target_h - sci_img.height) // 2
            im.paste(sci_img, (img_box_x, img_box_y))
            draw.rectangle([(img_box_x - 1, img_box_y - 1), (img_box_x + sci_img.width + 1, img_box_y + sci_img.height + 1)], outline="#38bdf8", width=1)
        except Exception as e:
            print(f"Error drawing image {img_path}: {e}")

    # Image Caption Box
    caption_y = img_card_y + 535
    draw.rectangle([(right_x + 20, caption_y), (right_x + right_w - 20, 855)], fill="#1e293b", outline="#334155", width=1)
    draw.text((right_x + 35, caption_y + 14), "Visual Scope & Environmental Context:", fill="#38bdf8", font=font_badge)
    
    # Wrap caption text
    c_words = scene["image_caption"].split(" ")
    c_lines = []
    c_cur = []
    for cw in c_words:
        c_cur.append(cw)
        if len(" ".join(c_cur)) > 44:
            c_cur.pop()
            c_lines.append(" ".join(c_cur))
            c_cur = [cw]
    if c_cur:
        c_lines.append(" ".join(c_cur))
    
    c_text_y = caption_y + 48
    for cline in c_lines:
        draw.text((right_x + 35, c_text_y), cline, fill="#cbd5e1", font=font_caption)
        c_text_y += 26

    # Bottom Footer Bar
    draw.rectangle([(0, 930), (width, 1080)], fill="#020617")
    draw.line([(0, 930), (width, 930)], fill="#1e293b", width=2)
    
    draw.text((80, 955), "SPEECH NARRATION / CLOSED CAPTIONS PREVIEW:", fill="#60a5fa", font=font_badge)
    preview_narration = scene["voiceover"][:135] + ("..." if len(scene["voiceover"]) > 135 else "")
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
        dur = scene_durations.get(scene["id"], 35.0)
        text = scene["voiceover"]
        
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

    with open(FINAL_SRT, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    print(f"SRT subtitles saved at {FINAL_SRT}")

# Main execution routine
async def main():
    print("=== Step 1: Synthesizing English Academic Voiceover (edge-tts) ===")
    await generate_all_audios()

    print("\n=== Step 2: Measuring Durations and Building HD Slides ===")
    scene_durations = {}
    for scene in SCENES:
        audio_file = os.path.join(AUDIO_DIR, f"audio_{scene['id']:02d}.mp3")
        dur = get_audio_duration(audio_file)
        scene_durations[scene['id']] = dur + 0.6  # 0.6s breathing margin
        print(f"Scene {scene['id']}: {dur:.2f}s (with padding: {dur + 0.6:.2f}s)")

        slide_file = os.path.join(SLIDES_DIR, f"slide_{scene['id']:02d}.png")
        create_slide_image(scene, slide_file)

    print("\n=== Step 3: Generating Synchronized SRT Subtitles ===")
    generate_srt(scene_durations)

    print("\n=== Step 4: Rendering Individual HD Video Clips with FFmpeg ===")
    ffmpeg_bin = "ffmpeg"
    clip_files = []
    concat_list_path = os.path.join(CLIPS_DIR, "concat_list.txt")

    with open(concat_list_path, "w") as f_concat:
        for scene in SCENES:
            slide_file = os.path.join(SLIDES_DIR, f"slide_{scene['id']:02d}.png")
            audio_file = os.path.join(AUDIO_DIR, f"audio_{scene['id']:02d}.mp3")
            clip_file = os.path.join(CLIPS_DIR, f"clip_{scene['id']:02d}.mp4")
            dur = scene_durations[scene['id']]

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
                f_concat.write(f"file '{clip_file.replace(os.sep, '/')}'\n")
                clip_files.append(clip_file)

    print(f"\n=== Step 5: Concatenating All {len(clip_files)} Clips into Master Video ===")
    concat_cmd = [
        ffmpeg_bin, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        FINAL_VIDEO
    ]
    res = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        total_size_mb = os.path.getsize(FINAL_VIDEO) / (1024 * 1024)
        total_dur = sum(scene_durations.values())
        print(f"SUCCESS! Master Video Rendered: {FINAL_VIDEO}")
        print(f"Total Duration: {total_dur:.1f}s ({total_dur / 60:.1f} minutes), File Size: {total_size_mb:.2f} MB")
    else:
        print(f"FFmpeg concat error: {res.stderr.decode('utf-8', errors='ignore')[:300]}")

    print("\n=== Step 6: Writing Rich Video Metadata ===")
    metadata = {
        "title": "Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting",
        "institution": "University of Science and Technology Beijing (北京科技大学)",
        "source_document": "Review points.docx",
        "video_file": os.path.basename(FINAL_VIDEO),
        "subtitles_file": os.path.basename(FINAL_SRT),
        "total_duration_sec": sum(scene_durations.values()),
        "total_duration_formatted": f"{int(sum(scene_durations.values()) // 60)}m {int(sum(scene_durations.values()) % 60)}s",
        "scenes": []
    }
    for scene in SCENES:
        metadata["scenes"].append({
            "id": scene["id"],
            "title": scene["title"],
            "tag": scene["tag"],
            "time": scene["time"],
            "duration": scene_durations[scene["id"]],
            "voiceover": scene["voiceover"],
            "key_points": scene["key_points"],
            "tags": scene["tags"],
            "slide_image": f"video_assets/slides/slide_{scene['id']:02d}.png",
            "audio_file": f"video_assets/audio/audio_{scene['id']:02d}.mp3",
            "clip_file": f"video_assets/clips/clip_{scene['id']:02d}.mp4"
        })

    with open(FINAL_METADATA, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Metadata saved: {FINAL_METADATA}")

if __name__ == "__main__":
    asyncio.run(main())
