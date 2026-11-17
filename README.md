# FOODLOOP
### AI-Powered Surplus Food Rescue and Redistribution Platform

## About the Project
FOODLOOP is a platform designed to connect food donors, NGOs, and volunteers to reduce food wastage and support food redistribution.

Donors can register surplus food. NGOs can view and accept or decline donations. Volunteers can verify food handovers using QR codes.

## Features
- Donor Dashboard
- Food Donation Registration
- SQLite Database
- NGO Matching System
- NGO Dashboard
- Volunteer Dashboard
- QR Code Generation and Scanning
- Donation Status Tracking
- Impact Dashboard

## Technologies Used
- Python
- Streamlit
- SQLite
- Pandas
- OpenCV
- QR Code
- Scikit-learn

## Project Modules
1. app.py – Main application
2. database.py – Database operations
3. ai_matching.py – NGO matching logic
4. ngo.py – NGO dashboard
5. volunteer.py – Volunteer dashboard
6. qr_system.py – QR code generation

## How to Run

Install the required packages:

```bash
pip install streamlit pandas scikit-learn "qrcode[pil]" pillow opencv-python-headless
```

Run the application:

```bash
python -m streamlit run app.py
```

## Project Goal
To reduce surplus food wastage by improving coordination between donors, NGOs, and volunteers.