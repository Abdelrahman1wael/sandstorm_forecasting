"""Update Chapter 2 (Literature Review) and References in the thesis .docx
to use ONLY the exact 61 references [1]-[61] provided by the user, with
accurate in-text citations and clean formatting.
"""

from pathlib import Path
import docx
from docx.oxml import OxmlElement

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL.docx"
)

REFERENCES_61 = [
    "[1] KARIMIAN H, LI Q, WU C, et al. Evaluation of different machine learning approaches to forecasting PM2.5 mass concentrations[J]. Aerosol and Air Quality Research, 2019, 19(6): 1400-1410.",
    "[2] Chen Siyu, Du Shikang, Bi Hongru, et al. A review of research on the identification and forecasting methods of sand-dust weather[J]. Journal of Desert Research, 2024, 44(01): 11-21.",
    "[3] HUANG M, PENG G, ZHANG J, et al. Application of artificial neural networks to the prediction of dust storms in Northwest China[J]. Global and Planetary change, 2006, 52(1-4): 216-224.",
    "[4] LU Z, ZHANG Q, ZHAO Z. SVM in the sand-dust storm forecasting[C]//2006 International Conference on Machine Learning and Cybernetics. IEEE, 2006: 3677-3681.",
    "[5] XIE Y, LIU Y, FU Q. Imbalanced data sets classification based on SVM for sand-dust storm warning[J]. Discrete Dynamics in Nature and Society, 2015, 2: 1-8.",
    "[6] ZHANG Z, MA C, XU J, et al. A novel combinational forecasting model of dust storms based on rare classes classification algorithm[C]//Geo-Informatics in Resource Management and Sustainable Ecosystem, 2015: 520-537.",
    "[7] KABOODVANDPOUR S, AMANOLLAHI J, QHAVAMI S, et al. Assessing the accuracy of multiple regressions, ANFIS, and ANN models in predicting dust storm occurrences in Sanandaj, Iran[J]. Natural Hazards, 2015, 78: 879-893.",
    "[8] AL MURAYZIQ T S, KAPETANAKIS S, PETRIDIS M. Intelligent signal processing for dust storm prediction using ensemble case-based reasoning[C]//2017 IEEE 29th International Conference on Tools with Artificial Intelligence (ICTAI). IEEE, 2017: 1267-1271.",
    "[9] SHAIBA H A, ALAASHOUB N S, ALZAHRANI A A. Applying machine learning methods for predicting sand storms[C]//2018 1st International Conference on Computer Applications & Information Security (ICCAIS). IEEE, 2018: 1-5.",
    "[10] LI T, REN Q, QIU Y. Application of improved naive bayesian-CNN classification algorithm in sandstorm prediction in inner mongolia[J]. Advances in Meteorology, 2019, 2019: 1-13.",
    "[11] HARBA H S, HARBA E, FARTTOOS M. Prediction of dust storm direction from satellite images by utilized deep learning neural network[C]//2020 6th International Engineering Conference “Sustainable Technology and Development”(IEC). IEEE, 2020: 179-184.",
    "[12] REN Q, QIU Y, LI T. Application of Convolution Neural Network Based on Transfer Learning in Sandstorm Prediction in Inner Mongolia[C]//2020 5th International Conference on Computer and Communication Systems (ICCCS). IEEE, 2020: 120-124.",
    "[13] EBRAHIMI-KHUSFI Z, TAGHIZADEH-MEHRJARDI R, MIRAKBARI M. Evaluation of machine learning models for predicting the temporal variations of dust storm index in arid regions of Iran[J]. Atmospheric Pollution Research, 2021, 12(1): 134-147.",
    "[14] ROUSE J W, HAAS R H, SCHELL J A, et al. Monitoring vegetation systems in the Great Plains with ERTS[J]. NASA Spec. Publ, 1974, 351(1): 309.",
    "[15] MAHMOUDI L, DOUMARI S A, SAFARIANZENGIR V, et al. Monitoring and prediction of dust and investigating its environmental impacts in the western half of Iran and the eastern borders of Turkey and Iraq, using remote sensing and GIS[J]. Journal of the Indian Society of Remote Sensing, 2021, 49: 713-724.",
    "[16] REN Q, LI N, ZHANG W. Research on sand-dust storm forecasting based on deep neural network with stacking ensemble learning[J]. IEEE Access, 2022, 10: 111855-111863.",
    "[17] HUANG C, BAI C, CHAN S, et al. MMSTN: A Multi‐Modal Spatial‐Temporal Network for Tropical Cyclone Short‐Term Prediction[J]. Geophysical Research Letters, 2022, 49(4): e2021GL096898.",
    "[18] HUANG C, BAI C, CHAN S, et al. MGTCF: multi-generator tropical cyclone forecasting with heterogeneous meteorological data[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2023, 37(4): 5096-5104.",
    "[19] ALEMANY S, BELTRAN J, PEREZ A, et al. Predicting hurricane trajectories using a recurrent neural network[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2019, 33(01): 468-475.",
    "[20] CHEN R, ZHANG W, WANG X. Machine learning in tropical cyclone forecast modeling: A review[J]. Atmosphere, 2020, 11(7): 676.",
    "[21] SHI X, CHEN Z, WANG H, et al. Convolutional LSTM network: A machine learning approach for precipitation nowcasting[J]. Advances in neural information processing systems, 2015, 28: 802-810.",
    "[22] WANG Y, LONG M, WANG J, et al. PredRNN: recurrent neural networks for predictive learning using spatiotemporal LSTMs[C]//Proceedings of the 31st International Conference on Neural Information Processing Systems. 2017: 879-888.",
    "[23] BAI C, SUN F, ZHANG J, et al. Rainformer: Features extraction balanced network for radar‐based precipitation nowcasting[J]. IEEE Geoscience and Remote Sensing Letters, 2022, 19: 1-5.",
    "[24] GAO Z, SHI X, WANG H, et al. Earthformer: Exploring space-time transformers for earth system forecasting[J]. Advances in Neural Information Processing Systems, 2022, 35: 25390-25403.",
    "[25] Song Hongkai. Disaster Weather Prediction and Analysis Based on Automated Machine Learning[D]. Liaoning: Shenyang University of Technology, 2024.",
    "[26] Pu Xiushu, Liu Xinchao, Song Yixuan, et al. Road Meteorological Condition Prediction Based on Numerical Weather Prediction and Machine Learning Technology[J]. Journal of Tropical Meteorology, 2024, 40(6): 993-1004.",
    "[27] Tao Tianyou, Deng Peng, Wang Hao, et al. Research Progress and Reflections on Short-term Prediction of Extreme Wind Fields Based on Machine Learning[J]. Acta Aerodynamica Sinica, 2025, 43(5): 78-91.",
    "[28] Luo Huan, Duan Bolong. Multi-scale Prediction Model of Disastrous Weather Based on Machine Learning[J]. Meteorology and Disaster Reduction Research, 2023, 46(3): 221-226.",
    "[29] Guan Donghe, Su Bo. Research on Weather Prediction Model Based on Big Data and Artificial Intelligence[J]. Modern Information Technology, 2025, 9(6): 93-99,104.",
    "[30] Zhao Zekun, Gao Yan, An Jingjing, et al. Research on Regional Building Electric Load Forecasting Based on Shallow and Deep Machine Learning Algorithms[J]. Building Science, 2025, 41(2): 229-236.",
    "[31] Zhao Xuanze, Jiao Zilong, Jing Yongtao, et al. Analysis and Impact Risk Prediction of Strong Convective Weather at Aerospace Launch Sites Based on the AeolusStorm Model[J]. Spacecraft Environment Engineering, 2025, 42(5): 504-515.",
    "[32] Bai Ziyi, Xu Ying, Feng Jian, et al. Long-term and Short-term Prediction Model of NWP ZTD Based on Machine Learning[J]. Journal of Navigation and Positioning, 2024, 12(4): 34-44.",
    "[33] Liu Fangjie. Research on Wind Speed/Power Interval Prediction Based on Machine Learning and Numerical Weather Prediction[D]. Hubei: Huazhong University of Science and Technology, 2022.",
    "[34] Bai Jiayi, Wei Wei, Zhang Hongsheng, et al. Research on Prediction Method of Atmospheric Boundary Layer Height Based on Machine Learning[J]. Journal of Atmospheric Sciences, 2025, 48(3): 404-416.",
    "[35] An Wenhan, Liu Jianhua, Liu Jiying. Analysis of Predictive Capability of Solar Irradiance Machine Learning Models[J]. Gas & Heat, 2025, 45(1): 26-31.",
    "[36] Liao Wenxi. Short-term Wind Power/Photovoltaic Power Prediction Method Based on Feature Engineering Optimization and Machine Learning[C]//Proceedings of the 2025 Smart Design and Construction Experience Exchange Conference. 2025: 1-4.",
    "[37] Cao Ruizhe, Qin Anzhen. Research on Prediction of Reference Crop Evapotranspiration Based on Time Series and Machine Learning[J]. Journal of Irrigation and Drainage, 2025, 44(8): 45-52.",
    "[38] Shi Junbin. Machine Learning Improves the Accuracy of Weather and Climate Prediction[J]. Henan Science and Technology, 2024, 51(14): 3.",
    "[39] Zheng Xinshi, Liang Shouyu, Su Xiao, et al. Load Characteristic Analysis and Prediction Based on Bayesian Method and Interpretable Machine Learning[J]. Automation of Electric Power Systems, 2023, 47(13): 56-68.",
    "[40] Liang Yicheng. Research on Prediction of the Highest Usable Frequency in Short-wave Communication Based on Machine Learning and Chaos Theory[J]. Communication Power Technology, 2025, 42(7): 46-48,97.",
    "[41] Du Jiali. PM2.5 Level Prediction Based on Machine Learning K-nearest Neighbor and Decision Tree Algorithms[J]. Computer Era, 2025(7): 38-40,46.",
    "[42] Che Xiang. Research on Prediction of Ambient Air VOCs Concentrations in Typical Industrial Areas Based on Machine Learning Algorithms[J]. Environmental Science Research, 2024, 37(8): 1694-1702.",
    "[43] Wang Wei, Ren Xiufang, Dong Junyu. Design and Implementation of a Machine Learning Room Temperature Prediction Model in Intelligent Heating[J]. Shandong Industrial Technology, 2025(5): 73-79.",
    "[44] Zhao Peng, Chai Rongmu, Yuan Fujiang, et al. Research on a Flood Prediction Model Based on the Combination of Blockchain and Machine Learning[J]. Information Technology & Informatization, 2025(4): 60-65.",
    "[45] Zhang Zhihao, Cui Ping, Zhou Xinlei. Prediction of Supply Water Temperature in Secondary Pipe Networks Based on Machine Learning[J]. Gas & Heat, 2024, 44(12): 21-27.",
    "[46] Zhao Xiaohua, Qi Hang, Yao Ying, et al. Risk Prediction and Cause Analysis of Expressway Interchange Exits Based on an Interpretable Machine Learning Framework[J]. Journal of Southeast University (Natural Science Edition), 2022, 52(1): 152-161.",
    "[47] Song Hongkai, Duan Yong, Zhao Tingting. Prediction of Thunderstorm and Gale Weather in Liaoning Based on Automated Machine Learning[J]. Artificial Intelligence and Robotics Research, 2024, 13(1): 90-97.",
    "[48] Zhang Siyi. Research on the Application of Machine Learning Methods in Short-term and Ultra-short-term Wind Power Prediction[D]. Guangdong: South China University of Technology, 2024.",
    "[49] Zhang Zhihao. Research on Supply Water Temperature Prediction and Optimal Control of Civil Heat Exchange Stations Based on Machine Learning[D]. Shandong: Shandong Jianzhu University, 2024.",
    "[50] Chen Duo. Research on Uncertainty Prediction of Rail Transit Passenger Flow Based on Big Data-driven and Machine Learning[D]. Lanzhou Jiaotong University, 2024.",
    "[51] Zhao Kai. Research and Application of Natural Gas Load Forecasting Based on Machine Learning Combination Models[D]. Shaanxi: Xi'an University of Architecture and Technology, 2024.",
    "[52] Zhang Yuanding, Gong Weiwei, Ye Yu, et al. Application of Machine Learning Technology to Predict Snow Accumulation during Strong Rain and Snow Weather Processes[J]. Science Technology and Engineering, 2019, 19(15): 58-69.",
    "[53] Haider S T, Ge W, Li J, et al. An Ensemble Machine Learning Framework for Cotton Crop Yield Prediction Using Weather Parameters: A Case Study of Pakistan[J]. Access, IEEE, 2024, 12(000): 124045-124061.",
    "[54] Thayanandeswari C S S, Jaya T, Ahamed S N, et al. A Machine Learning Approach for Crop Yield Prediction Using Weather Condition[J]. 2024 International Conference on Advancement in Renewable Energy and Intelligent Systems (AREIS), 2024: 1-5.",
    "[55] Ramadhan A J, Priya S R K, Pavithra V, et al. Machine Learning Techniques for Sugarcane Yield Prediction Using Weather Variables[J]. BIO web of conferences, 2024, 97(000): 9.",
    "[56] Mahavik N, Kangerd A, Masthawee F, et al. Optimizing rainfall prediction in central Thailand with weather radar and machine learning during the monsoon[J]. Environmental Earth Sciences, 2025, 84(5): 1-18.",
    "[57] Kammerlander C, Kolb V, Luegmair M, et al. Machine Learning Models for Soil Parameter Prediction Based on Satellite, Weather, Clay and Yield Data[J]. 2025.",
    "[58] Mugemangango C, Nzabanita J, Muhoza D N, et al. MACHINE LEARNING TECHNIQUES FOR PREDICTION OF RICE YIELD IN RWANDA BASED ON WEATHER AND SOIL PARAMETERS[J]. African Journal of Food, Agriculture, Nutrition & Development, 2025, 25(4).",
    "[59] Ajith S, Debnath M K, Karthik R. Statistical and machine learning models for location-specific crop yield prediction using weather indices[J]. International Journal of Biometeorology, 2024, 68(12).",
    "[60] Chana A M, Bernabé Batchakui, Nges B B. Real-Time Crop Prediction Based on Soil Fertility and Weather Forecast Using IoT and a Machine Learning Algorithm[J]. Journal of Agricultural Sciences (English), 2023, 14(5): 645-664.",
    "[61] Brandt P, Munim Z H, Chaal M, et al. Maritime accident risk prediction integrating weather data using machine learning[J]. Transportation Research Part D, 2024, 136.",
]

CH2_CONTENT = [
    ("Heading 2", "2.1 Traditional Sand and Dust Storm Forecasting Approaches"),
    ("Heading 3", "2.1.1 Numerical Weather Prediction Models"),
    ("Normal", "Numerical weather prediction (NWP) models are physically based systems that forecast atmospheric evolution by solving coupled equations governing atmospheric dynamics, thermodynamics, and aerosol-chemical processes [2]."),
    ("Heading 3", "2.1.2 Bottlenecks and Limitations of Traditional Forecasting"),
    ("List Paragraph", "Highly nonlinear and complex interactions: Sandstorms result from coupled interactions among atmospheric dynamics and surface conditions such as soil moisture, vegetation cover, and terrain [2]."),
    ("List Paragraph", "High computational costs: Running a high-precision global dynamical forecast requires substantial supercomputing time, limiting rapid updates and emergency response."),
    ("List Paragraph", "Extended-range and seasonal forecasts (internal variability): As lead time increases, the influence of initial conditions diminishes while internal variability and boundary forcings dominate, causing dynamical model skill to decline significantly."),
    ("List Paragraph", "Traditional \"post-event response\" warning mode: Limited lead time and accuracy narrow the emergency response window and result in passive prevention and control."),
    ("Heading 2", "2.2 AI Applications in Sand and Dust Storm Forecasting"),
    ("Normal", "Machine learning and deep learning algorithms offer strong nonlinear fitting, high-dimensional feature extraction, and complex pattern recognition for sand-dust forecasting [2]."),
    ("Heading 3", "2.2.1 Machine Learning for Sandstorm Detection and Forecasting"),
    ("Normal", "Early ANN and SVM studies."),
    ("List Paragraph", "An ANN model based on a multi-layer perceptron (Huang et al. [3]) assigned occurrence indices to sandstorm and non-occurrence days across four meteorological stations in Northwest China, outperforming traditional regression models."),
    ("List Paragraph", "An SVM model (Lu et al. [4]) introduced atmospheric potential field inputs—including 500 hPa geopotential height, zonal and meridional winds, and temperature—using recall as the primary evaluation metric."),
    ("Normal", "Ensemble learning and other machine learning models."),
    ("List Paragraph", "Hybrid adaptive sampling: Targeted sampling of minority-class (sandstorm) events enabled an SVM model to better capture sandstorm characteristics and improved warning accuracy (Xie et al. [5])."),
    ("List Paragraph", "A rare-class combinational forecasting model combining AdaBoost with random forest classification was applied to sandstorm prediction in China (Zhang et al. [6])."),
    ("List Paragraph", "Multiple regression, adaptive network-based fuzzy inference system (ANFIS), and ANN models were compared for predicting dust storm occurrences in Sanandaj, Iran (Kaboodvandpour et al. [7])."),
    ("List Paragraph", "Multiple machine learning algorithms, including CART decision trees and naive Bayes, were evaluated for predicting sandstorms in Saudi Arabia (Shaiba et al. [9])."),
    ("List Paragraph", "Remote sensing and GIS indicators combined with dust monitoring and prediction models were applied to 28 high-incidence stations in western Iran and neighbouring border regions over 29 years to assess dust trends and environmental impacts (Mahmoudi et al. [15])."),
    ("Heading 3", "2.2.2 Deep Learning and Hybrid Models"),
    ("Normal", "Deep learning and other representative studies."),
    ("List Paragraph", "A convolutional neural network applied to infrared satellite cloud-image datasets using transfer learning explored sandstorm outbreak patterns in Inner Mongolia (Ren et al. [12])."),
    ("List Paragraph", "A stacking ensemble of LSTM and CNN, using a fully connected network and an SVM as meta-classifiers, outperformed single LSTM and CNN models across multiple indicators in Inner Mongolia (Ren et al. [16])."),
    ("List Paragraph", "Deep neural networks applied to satellite imagery predicted dust storm movement direction using feature pyramid networks for segmentation and region proposal networks for target classification (Harba et al. [11])."),
    ("List Paragraph", "Multi-dimensional factors—including climate, soil characteristics, NDVI [14], and land use—were combined with machine learning models to predict monthly dust storm index variations in arid regions (Ebrahimi-Khusfi et al. [13])."),
    ("Normal", "Hybrid models that overcome model bias."),
    ("List Paragraph", "Combining Bayesian networks with ensemble case-based reasoning (Al Murayziq et al. [8]) integrated wind speed, air pressure, temperature, and humidity for dust storm prediction."),
    ("List Paragraph", "The INB-CNN model (Li et al. [10]) integrates naive Bayes and convolutional neural networks, extracting spatial features from atmospheric circulation data to improve sandstorm classification."),
    ("Heading 2", "2.3 Machine Learning in Meteorology and Related Fields"),
    ("Normal", "Machine learning applications in meteorology span direct prediction of disastrous weather, prediction of key meteorological parameters, and downstream sectors including energy, transportation, agriculture, and air quality."),
    ("Heading 3", "2.3.1 Direct Prediction of Disastrous Weather"),
    ("Normal", "Disastrous weather, owing to its sudden onset and strong destructive power, has been a major focus of machine learning research across cyclones, convective storms, precipitation, and extreme winds."),
    ("List Paragraph", "Tropical cyclones and spatiotemporal nowcasting: Recurrent neural networks [19], multi-modal spatiotemporal networks (MMSTN [17], MGTCF [18]), and cyclone forecast reviews [20] improved trajectory and intensity prediction, while ConvLSTM [21], PredRNN [22], Rainformer [23], and Earthformer [24] advanced radar precipitation and Earth-system sequence forecasting."),
    ("List Paragraph", "Thunderstorm and gale prediction: Automated machine learning frameworks (such as AutoFeat-TPOT [25] and AutoGluon) simplified modelling workflows and achieved a hit rate of 96.72% in Liaoning [47]."),
    ("List Paragraph", "Severe convective weather: The AeolusStorm model [31] and random forest regression were used to construct atmospheric instability risk indices at aerospace launch sites."),
    ("List Paragraph", "Floods: A multi-layer perceptron combined with blockchain technology selected key indicators via correlation analysis for reliable flood early warning [44]."),
    ("List Paragraph", "Snow: CART decision trees and deep learning models were coupled in series to predict daily snow accumulation during strong rain-snow processes [52]."),
    ("List Paragraph", "Extreme winds and multi-scale weather: A recent review synthesised machine learning and hybrid methods for short-term extreme wind prediction [27]; a firefly-optimised SVM built a multi-scale disastrous-weather model in Chengdu [28]; and big data with regression and decision trees supported general weather prediction under climate uncertainty [29]."),
    ("Heading 3", "2.3.2 Prediction of Key Meteorological Parameters"),
    ("List Paragraph", "Tropospheric delay (NWP ZTD) affecting satellite navigation accuracy was predicted using BP neural networks and support vector machines [32]."),
    ("List Paragraph", "Atmospheric boundary layer height in Beijing was predicted with XGBoost using surface observations and wind-profile radar, outperforming multiple linear and support vector regression [34]."),
    ("List Paragraph", "Monsoon rainfall in central Thailand was optimised by combining weather radar with random forest and related machine learning models [56]."),
    ("List Paragraph", "Reference crop evapotranspiration [37] and short-wave communication highest usable frequency combining chaos theory and machine learning [40] further demonstrated parameter-level forecasting skill."),
    ("Heading 3", "2.3.3 Energy, Power Load, and Thermal Systems"),
    ("List Paragraph", "Regional building electric load forecasting compared shallow and deep machine learning algorithms, showing strong accuracy for XGBoost and LSTM [30], while an interpretable Bayesian time-varying coefficient and CatBoost framework improved small-sample extreme-weather load prediction [39]."),
    ("List Paragraph", "Wind and solar power forecasting utilised Bi-GRU encoder-decoder attention models [48], CatBoost and LightGBM with feature engineering and error compensation [36], and EALSTM-QR neural networks coupled with NWP for wind speed/power interval prediction [33], alongside SVM regression and Elman networks for solar irradiance [35]."),
    ("List Paragraph", "Thermal pipe networks, intelligent heating, and natural gas load forecasting combined weather factors with random forests and model predictive control [43, 45, 49], as well as VMD-attention GRU models [51]."),
    ("Heading 3", "2.3.4 Transportation and Maritime"),
    ("List Paragraph", "Rail transit passenger flow uncertainty was modelled using decomposition-ensemble and graph convolutional neural networks [50]."),
    ("List Paragraph", "Expressway interchange exit risk prediction coupled XGBoost with SHAP interpretability to quantify weather and traffic causal factors [46]."),
    ("List Paragraph", "Maritime accident risk prediction integrated wind and sea-level pressure into LightGBM [61], while NWP outputs linked to decision trees forecast 24-hour road icing and wetness conditions [26]."),
    ("Heading 3", "2.3.5 Agriculture and Air Quality"),
    ("Normal", "Agriculture."),
    ("List Paragraph", "Location-specific crop yield prediction using weather indices showed non-linear ML models outperforming linear baselines [59], while the RFXG ensemble framework predicted cotton yield from weather parameters [53]."),
    ("List Paragraph", "Decision tree, random forest, and K-nearest neighbour models predicted crop and sugarcane yields [54, 55], XGBoost predicted rice yield in Rwanda from weather and soil parameters [58], satellite and soil data predicted soil parameters [57], and IoT sensors with random forests enabled real-time crop recommendations [60]."),
    ("Normal", "Air quality."),
    ("List Paragraph", "PM2.5 mass concentration and level prediction compared multiple ML approaches including K-nearest neighbours, decision trees, and random forests [1, 41]."),
    ("List Paragraph", "Industrial-area ambient VOCs concentrations were predicted using LSTM networks combining NWP and enterprise activity data [42]."),
    ("Heading 2", "2.4 AI Forecasting Platforms and Early-Warning Systems"),
    ("Normal", "Recent AI meteorological large models have demonstrated operational sandstorm and weather forecasting capabilities [38]."),
    ("List Paragraph", "Aerosol-meteorology coupled AI systems deliver high-resolution (5 km) sandstorm forecasts updated twice daily, reducing East Asian forecast errors by 38% to 74% relative to ECMWF and NASA baselines and capturing cross-regional dust transport up to 120 hours in advance."),
    ("List Paragraph", "Global machine learning weather and climate models such as NeuralGCM exemplify the integration of physical dynamical cores with learned parameterisations [38]."),
    ("Heading 2", "2.5 Overall Characteristics, Challenges and Future Directions"),
    ("Normal", "Overall characteristics of current research."),
    ("List Paragraph", "Model architectures are evolving from single traditional algorithms (SVM, random forests) toward deep learning (LSTM, GRU, Transformers, graph neural networks) and automated machine learning frameworks."),
    ("List Paragraph", "Machine learning is increasingly integrated with numerical weather prediction and physical constraints rather than replacing them."),
    ("List Paragraph", "Greater emphasis is placed on feature engineering and model interpretability to understand atmospheric mechanisms."),
    ("List Paragraph", "Applications are becoming increasingly domain-specific, with models tailored to regional hazards and operational needs."),
    ("Heading 2", "2.6 Research Gaps and Motivation"),
    ("Normal", "Current status of research. Compared with other meteorological disasters, sandstorm forecasting that integrates multi-source remote sensing with AI remains at an exploratory stage with limited publicly available benchmarks [1, 2]."),
    ("Normal", "Research gaps."),
    ("List Paragraph", "Existing research focuses mainly on short-term monitoring, identification, or binary classification rather than medium- to long-term forecasting."),
    ("List Paragraph", "Many studies still rely on traditional machine learning (SVM, random forests) and have not fully adopted modern spatiotemporal deep learning architectures."),
    ("List Paragraph", "Input features rely heavily on ground stations and underutilise multi-modal reanalysis and satellite remote sensing products."),
    ("List Paragraph", "Varying data sources, spatiotemporal resolutions, and target definitions hinder fair cross-study comparisons."),
    ("List Paragraph", "Physical interpretability of current black-box models remains weak, and severe class imbalance biases models against rare dust storm events."),
    ("Normal", "Rationale and approach. This study addresses these gaps by: (i) fusing multi-modal NWP, reanalysis, satellite remote sensing, and surface environmental data into a unified dataset for medium- to long-term forecasting; (ii) developing and benchmarking spatiotemporal and ensemble architectures with class-imbalance optimisation; and (iii) enhancing physical interpretability and forecast verification."),
    ("Normal", "Justification for the Saudi Arabian study. Distinguishing between monthly dust-storm frequency and individual medium- to long-term events requires tailored outcome definitions and validation metrics (sensitivity, specificity, precision, F1-score, and ROC-AUC) to support early preparedness and resilience in Riyadh and across Saudi Arabia."),
]


def insert_para_before(anchor_el, text: str, style_name: str, doc: docx.Document) -> None:
    p = doc.add_paragraph(text, style=style_name)
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)


def main() -> None:
    doc = docx.Document(str(DOC_PATH))

    ch2_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 2" in p.text)
    ch3_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 3" in p.text)
    refs_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "References" in p.text)
    res_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Resume" in p.text)

    # Capture anchor elements and elements to remove BEFORE mutating the XML tree
    ch3_el = doc.paragraphs[ch3_idx]._element
    res_el = doc.paragraphs[res_idx]._element
    ch2_to_remove = [doc.paragraphs[i]._element for i in range(ch2_idx + 1, ch3_idx)]
    refs_to_remove = [doc.paragraphs[i]._element for i in range(refs_idx + 1, res_idx)]

    for el in ch2_to_remove:
        el.getparent().remove(el)
    for el in refs_to_remove:
        el.getparent().remove(el)

    # Insert new Chapter 2 content before Chapter 3 heading
    for style_name, text in CH2_CONTENT:
        insert_para_before(ch3_el, text, style_name, doc)

    # Insert exact 61 references before Resume heading
    ref_style = "Normal"
    for ref in REFERENCES_61:
        insert_para_before(res_el, ref, ref_style, doc)

    try:
        doc.save(str(DOC_PATH))
        out_path = DOC_PATH
    except PermissionError:
        out_path = DOC_PATH.with_name(DOC_PATH.stem + "_EXACT61_REFS.docx")
        doc.save(str(out_path))
    print(f"Updated Chapter 2 ({len(CH2_CONTENT)} paragraphs) and References ({len(REFERENCES_61)} items) in {out_path.name}.")


if __name__ == "__main__":
    main()
