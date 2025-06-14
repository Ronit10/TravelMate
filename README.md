# TravelMate
Connect Solo Travelers
# 🌍 TravelMate - Your Ultimate Travel Companion

**TravelMate** is a web-based platform designed to connect solo travelers heading to the same destination. It offers a complete travel experience by helping users match with fellow travelers, estimate trip costs (hotels, food, adventures), and auto-generate day-wise itineraries — all in one place.

---

## ✨ Features

- 🔍 **Location-based Trip Matching**  
  Find other solo travelers heading to the same place on the same date and connect with them.

- 💬 **Real-time Chat**  
  Chat with matched travelers to plan your journey together.

- 💰 **Cost Estimator**  
  Get budget estimates for:
  - Hotels
  - Food
  - Adventures

- 🗺️ **Itinerary Generator**  
  Instantly generate a day-wise travel plan for your destination.

---

## 🛠️ Tech Stack

### Frontend:
- HTML, CSS, JavaScript

### Backend:
- Python (Flask Framework)
- MySQL (Database)
- JWT (Authentication)
- CORS Enabled APIs

---

## 📁 Project Structure

/TravelMate
│
├── frontend/ # All HTML/CSS/JS files
├── backend/
│ ├── app.py # Flask main app
│ ├── config.py # DB config & app setup
│ ├── models/ # MySQL models
│ ├── routes/ # All route files (auth, trip, hotel, food, adventure, chat, match, cost)
│ └── services/ # Helper functions and services
│
└── README.md # You're here!
