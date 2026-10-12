
# Sand/Dust Storm Forecasting Project

Project:
Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting

Notebook purpose:
This is a Kaggle prototype for medium- to long-term sand/dust risk forecasting.

Dataset:
- Prototype dataset: Beijing Multi-Site Air-Quality Data Set from Kaggle
- Input variables: PM10/PM2.5, wind speed, rainfall, pressure, temperature, pollutants
- Target: proxy sand/dust event label created from high PM + high wind + low rain

Important note:
The proxy target is not a true official sandstorm label.
For the final thesis, replace this target with real SDS labels from:
1. WMO present-weather codes
2. Satellite dust products
3. FY-4A dust-storm datasets
4. MODIS dust storm frequency products
5. CMA operational SDS records if available

Forecast horizons:
[3, 7, 15]

Generated folders:
- data/: processed datasets
- models/: trained ML models
- figures/: charts
- metrics/: evaluation results and feature importance
- predictions/: risk prediction outputs
- config.json: experiment configuration
- label_thresholds.json: proxy-label threshold information

Created:
2026-10-06T08:32:37.310552 UTC
