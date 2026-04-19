# Engineering Alert Dashboard

A Streamlit-based dashboard for monitoring engineering incidents and identifying high-risk assets.

## Overview

This project is an engineering dashboard that monitors asset incidents and identifies high-risk issues.

It combines:
- Asset data (loaded from an external API)
- Simulated incident data
- Alert logic and risk scoring

The goal is to support engineering decision-making by highlighting critical problems and prioritising assets.

---

## Features

- 📊 Incident monitoring dashboard  
- ⚠️ Critical alert detection (high severity + repeat issues)  
- 📈 Asset risk scoring and ranking  
- 🔍 Filtering by site and severity  
- 📉 Visualisation of incidents by site  

---

## How It Works

1. Asset data is loaded from an external API  
2. Incident data is generated randomly  
3. Data is merged and filtered  
4. Alerts are calculated based on severity and repeat issues  
5. Risk scores are calculated per asset  
6. The dashboard displays insights and rankings  

---

## Example Output

- Critical alerts when high-risk issues are detected  
- Ranked list of assets by risk score  
- Identification of the highest-risk asset  

---

## How to Run

1. Navigate to the project folder:
```bash
cd engineering_alert_dashboard
```

2. Activate virtual environment:
```bash
source ../venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

## Requirements

- streamlit
- pandas
- requests

---

## Notes

This is a learning project demonstrating:

- data integration
- dashboard design
- alert logic
- risk-based decision support

---

## Future Improvements

- Add persistent data storage
- Improve alert rules
- Add more visualisations
- Integrate AI for diagnostics