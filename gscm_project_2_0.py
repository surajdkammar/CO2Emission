# -*- coding: utf-8 -*-
"""GSCM Project 2.0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aEMszoiKhYJHyo7aieydao-pZEbwylgW
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# Load dataset and preprocess
data = pd.read_csv("automotive_co2_data_full.csv")
X = data.drop("CO2_emissions", axis=1)
y = data["CO2_emissions"]

categorical_features = [col for col in X.columns if X[col].dtype == 'object']
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_data = encoder.fit_transform(X.loc[:, categorical_features])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_features))
X = X.drop(columns=categorical_features)
X = pd.concat([X, encoded_df], axis=1)

# Train model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Feature importance
feature_importances = rf_model.feature_importances_
feature_importance_df = pd.DataFrame({"Feature": X.columns, "Importance": feature_importances})
feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)

# Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("CO2 Emissions Prediction Dashboard"),
    dcc.Graph(id='feature-importance-graph'),
    html.Div(id='top-feature-suggestions'),
    html.Label("Enter Feature Values:"),
    html.Div([dcc.Input(id=feature, type='text', placeholder=feature) for feature in X.columns]),
    html.Button("Predict", id='predict-button', n_clicks=0),
    html.H3("Predicted CO2 Emissions: "),
    html.Div(id='prediction-output')
])

@app.callback(
    [Output('feature-importance-graph', 'figure'),
     Output('top-feature-suggestions', 'children'),
     Output('prediction-output', 'children')],
    [Input('predict-button', 'n_clicks')],
    [dash.State(feature, 'value') for feature in X.columns]
)
def update_dashboard(n_clicks, *feature_values):
    feature_values = [float(val) if val is not None else 0 for val in feature_values]
    input_df = pd.DataFrame([feature_values], columns=X.columns)
    prediction = rf_model.predict(input_df)[0]

    fig = px.bar(feature_importance_df.head(10), x='Importance', y='Feature', orientation='h', title="Feature Importances")

    top_features = feature_importance_df["Feature"][:3].tolist()
    suggestions = {  # Example suggestions
        "material_type": "Use environmentally friendly, sustainable materials to reduce emissions significantly.",
        "lathe_efficiency": "Regularly maintain lathes to ensure optimized energy consumption during production.",
        "machine_hours": "Schedule operations efficiently to minimize unnecessary machine runtime and emissions.",
        "energy_consumption": "Transition to renewable energy sources to lower carbon footprints dramatically.",
        "temperature": "Maintain consistent temperature levels to optimize energy use and efficiency.",
        "humidity": "Control humidity levels to ensure machines operate at peak efficiency.",
        "machine_type": "Upgrade machinery to advanced, energy-efficient models for lower emissions.",
        "operational_settings": "Calibrate operational settings for maximum efficiency with minimal energy use.",
        "wastage": "Implement waste reduction strategies and recycling to decrease environmental impact.",
        "certifications": "Acquire certifications promoting energy-efficient and low-carbon production practices.",
        "safety_incidents": "Reduce safety incidents to prevent downtime and energy wastage.",
        "recycling_rate": "Increase recycling rates to minimize production waste and emissions.",
        "first_pass_yield": "Improve first-pass yield rates to reduce waste and rework.",
        "downtime_duration": "Conduct preventive maintenance to limit downtime and energy inefficiencies.",
        "tool_maintenance_frequency": "Increase tool maintenance frequency to ensure efficient operations and longevity.",
        "scrap_handling_efficiency": "Streamline scrap handling processes to improve material reuse and recycling.",
        "rd_investment": "Invest in research to develop eco-friendly and sustainable production methods.",
        "packaging_waste": "Reduce packaging waste by adopting biodegradable or reusable materials.",
        "lifecycle_analysis": "Conduct lifecycle analyses to design products with minimal emissions impact.",
        "renewable_energy": "Integrate renewable energy sources like solar or wind into operations.",
        "surface_emissions": "Use advanced coatings or treatments to minimize surface emissions effectively.",
        "return_rate": "Enhance product quality to lower return rates and associated emissions.",
        "painting_emissions": "Use low-emission or water-based paints to reduce VOC emissions.",
        "heating_energy": "Improve insulation to lower energy consumption for heating operations.",
        "inventory_turnover": "Increase inventory turnover rates to prevent unnecessary storage energy usage.",
        "distance_to_suppliers": "Work with local suppliers to cut down transportation emissions significantly.",
        "carbon_capture_efficiency": "Enhance carbon capture systems to offset and lower emissions directly.",
        "secondary_process_emissions": "Optimize secondary processes to significantly reduce their environmental impact.",
        "worker_experience": "Train workers to operate machines efficiently and minimize resource waste.",
        "tool_wear_level": "Monitor and replace worn tools to maintain operational efficiency levels.",
        "supplier_reliability": "Partner with reliable suppliers to ensure efficient, low-emission supply chains.",
        "on_time_delivery_rate": "Reduce expedited shipping needs to avoid increased transport emissions.",
        "training_hours": "Focus training efforts on sustainable operations and energy-efficient practices.",
        "factory_age": "Retrofit older factories with energy-efficient technologies to reduce emissions.",
        "environmental_fines": "Address underlying issues causing fines to improve sustainability compliance.",
        "automation_ratio": "Increase automation to streamline processes and reduce energy wastage.",
        "water_usage": "Improve water recycling and reuse systems to conserve water resources.",
        "scrap_rate": "Lower scrap rates through precision manufacturing and efficient resource utilization.",
        "energy_source": "Shift to renewable energy sources like solar, wind, or hydropower.",
        "shift_timing": "Optimize shifts to align with energy-efficient production schedules.",
        "transport_emissions": "Use electric or hybrid vehicles for logistics to cut emissions.",
        "machines_in_operation": "Turn off idle machines to conserve energy and reduce emissions.",
        "turnover_rate": "Retain skilled workers to maintain consistent operational efficiency and stability.",
        "compressor_efficiency": "Replace old compressors with energy-efficient models to save power.",
        "ventilation_usage": "Optimize ventilation systems to balance air quality and energy consumption.",
        "inspection_accuracy": "Improve inspection accuracy to reduce defective products and material wastage.",
        "noise_level": "Invest in quieter machinery designed to operate more efficiently.",
        "num_shifts": "Align shifts to maintain optimal energy usage during operations.",
        "maintenance_downtime": "Proactively schedule maintenance to avoid unexpected energy-intensive downtimes.",
        "customer_complaints": "Address issues to avoid returns, replacements, and associated emissions.",
        "cooling_energy": "Use energy-efficient cooling systems to reduce power consumption.",
        "labor_hours_per_unit": "Streamline production workflows to reduce labor inefficiencies and emissions.",
        "material_defect_rate": "Improve material quality to lower defect rates and wastage.",
        "production_volume": "Prevent overproduction by aligning production with demand forecasts.",
        "cycle_time": "Shorten cycle times by optimizing processes to conserve energy.",
        "calibration_frequency": "Calibrate equipment regularly to maintain consistent energy-efficient performance.",
        "startup_emissions": "Automate startups to minimize emissions during initial production phases.",
        "factory_location": "Establish factories closer to raw materials or end markets.",
        "operator_skill": "Enhance operator skills for improved efficiency in machine operation.",
        "renewable_energy_utilization": "Maximize usage of renewable energy in everyday operations.",
        "machine_age": "Replace aging machines with modern, energy-efficient alternatives.",
        "supply_chain_emissions": "Streamline supply chain processes to reduce overall emissions footprint.",
        "water_reuse_rate": "Increase water reuse to conserve resources and cut emissions.",
        "product_weight": "Design lightweight products to reduce transportation and material usage emissions.",
        "batch_size": "Adjust batch sizes to avoid waste and overproduction.",
        "supply_chain_complexity": "Simplify supply chains to make them more sustainable and efficient.",
        "num_suppliers": "Reduce supplier numbers to focus on reliable, eco-friendly partnerships.",
        "inspection_frequency": "Conduct regular inspections to maintain operational efficiency and compliance.",
        "training_costs": "Invest in sustainable training to improve workforce efficiency.",
        "process_variability": "Reduce variability for consistent production efficiency and lower emissions.",
        "packaging_material": "Switch to biodegradable or recycled packaging materials.",
        "hazardous_waste": "Minimize hazardous waste generation through better waste management systems.",
        "line_speed": "Optimize line speeds to balance productivity with energy efficiency.",
        "smart_sensor_usage": "Use sensors to detect inefficiencies and optimize resource use.",
        "cooling_water_temp": "Adjust cooling water temperatures to improve energy efficiency.",
        "workstation_count": "Limit unnecessary workstations to reduce energy use.",
        "logistics_emissions": "Improve logistics strategies to cut emissions from transportation.",
        "lean_practices_frequency": "Implement lean practices to reduce waste and operational inefficiencies.",
        "power_outage_frequency": "Address power outages to ensure uninterrupted, efficient production.",
        "labor_costs": "Automate labor-intensive tasks to improve efficiency and cut emissions.",
        "supplier_proximity": "Source materials from nearby suppliers to reduce transportation emissions.",
        "govt_subsidy_access": "Leverage subsidies to implement sustainable practices and technologies.",
        "regulatory_inspections": "Meet regulations by adopting cleaner technologies and processes.",
        "scrap_reuse_rate": "Increase reuse rates of scrap materials in production processes.",
        "generator_fuel_consumption": "Switch to fuel-efficient or renewable-powered generators.",
        "skilled_labor_availability": "Train workers to minimize inefficiencies and lower emissions.",
        "component_type": "Use components that align with energy-efficient design principles.",
        "raw_material_cost": "Invest in sustainable raw materials to balance cost and efficiency.",
        "pollution_control": "Upgrade pollution control systems to meet environmental standards.",
        "quality_audit_frequency": "Increase audits to ensure consistent product quality and minimal waste.",
        "local_transport_emissions": "Switch to green transport solutions for local deliveries.",
        "worker_wage": "Incentivize workers to adopt efficient, sustainable operational practices.",
        "sustainability_awareness": "Promote company-wide awareness for adopting eco-friendly habits and practices.",
    }
    suggestion_text = [html.P(f"{feature}: {suggestions.get(feature, 'No suggestion available.')}") for feature in top_features]

    return fig, suggestion_text, f"{prediction:.2f} kg"

if __name__ == '__main__':
    app.run_server(debug=True)
