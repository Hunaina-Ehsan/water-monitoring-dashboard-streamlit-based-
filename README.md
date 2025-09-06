# 💧 Water Monitoring Dashboard (Prototype)

This project is a prototype dashboard for monitoring household water usage and electricity consumption, designed as part of an IoT-inspired system.

---

## 🚀 Features
- Real-time **tank visualizations** with proportional height and smooth water-fill animation  
- **Daily, weekly, and monthly** consumption plots  
- **Electricity usage** (pump hours and units)  
- **Alerts**:  
  - Bore flow rate issues  
  - Critical low water level  
  - Leak detection (abnormal usage)  

---

## 📊 Demo Screenshots
*(Simulated data – real dataset not included for privacy reasons)*

![Tank Visualization](<img width="1300" height="634" alt="image" src="https://github.com/user-attachments/assets/ee49cf0b-1db7-453d-b54e-b8afe6f6b2df" />)

![Water Consumption Trends](<img width="1343" height="481" alt="image" src="https://github.com/user-attachments/assets/e6ca33d4-5d9f-493d-b73f-b80fea4dec3f" />)

![Alerts](<img width="1277" height="334" alt="image" src="https://github.com/user-attachments/assets/e8971d99-5b12-4929-9da4-1b344f8d1266" />)


---

## ⚙️ How It Works
- Current version uses **simulated data** (`numpy` and `pandas`)  
- Real sensor data will be integrated via APIs/CSV/MQTT once available  

---

## 🔒 Data Privacy
Real household data has **not been included** in this repository due to privacy reasons.  
This repo contains **only the prototype UI + dummy data** for demonstration purposes.  

---

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/) → for interactive dashboard  
- [Plotly](https://plotly.com/python/) → for plotting  
- Python (`pandas`, `numpy`) → for data simulation and handling  

---

## ▶️ Run Locally
```bash
# Clone the repo
git clone <your-repo-url>
cd water-monitoring-dashboard

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
