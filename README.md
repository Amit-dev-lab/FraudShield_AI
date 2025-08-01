# 🛡️ FraudShield AI

FraudShield AI is a real-time fraud detection web application designed to safeguard users against suspicious UPI transactions. Developed during a 24-hour hackathon by a team of 4, the platform leverages explainable AI and full-stack technologies to offer **Fraud Detection as a Service (FDaaS)**.

> 🚀 **Live Demo**: [https://fraudshield-ai-fo1s.onrender.com/](https://fraudshield-ai-fo1s.onrender.com/)

> 🏆 **Top 50 out of 800+ teams** at **Central India Hackathon 2.0 2025**, organized by **Suryodaya College of Engineering and Technology, Nagpur**

---

## 📌 Features

- 🔐 Real-time fraud prediction for UPI transactions
- 🧠 AI/ML model with 99.98% accuracy using XGBoost
- 🧾 Manual fraud check form with probability score
- 📩 Email alerts for high-risk activity
- 👨‍💻 Admin interface to manage flagged records
- 🧪 API tested with Postman
- 🌐 Fully responsive UI with professional UX

---

## 👨‍💻 Team Contributions

| Team Member    | Contribution                              |
|----------------|-------------------------------------------|
| Amit Bangde    | Frontend, API Integratio, Deployment ,Postman Testing |
| Jayendrajeet Chauhan| ML, feature engineering, and training  |
| Mohammed Tailor   | Backend, Django REST API integration      |
| Jagdish Jadhav     | Tailwind UI and design     |

---

## 🧰 Tech Stack

- **Frontend**: html,CSS, Tailwind CSS  
- **Backend**: Django, Django REST Framework  
- **ML Model**: XGBoost  
- **Database**: SQLlite
- **Deployment**: Render (with cron job to prevent sleep)  
- **Testing**: Postman  

---

## 🛠️ Installation & Setup

### ⚙️ Backend (Django)

```bash
git clone https://github.com/yourusername/fraudshield_ai.git
cd fraudshield_ai/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables (use .env)
# Example:
# SECRET_KEY=your-secret-key
# DEBUG=True
# DATABASE_URL=your-database-url

# Run migrations
python manage.py migrate

# Start backend server
python manage.py runserver
```
🧪 API Testing with Postman
Import fraudshield_api.postman_collection.json

-Test routes:
-/api/predict/
-/api/manual-check/
/-api/transactions/

🙌 Acknowledgements
-Developed at Central India Hackathon 2025
-Organized by Suryodaya College of Engineering and Technology, Nagpur
-Selected as Top 50 team among 800+ participants
-Built to tackle real-world UPI fraud detection using AI

📄 License
This project is licensed under the MIT License.

📬 Connect with Us
LinkedIn – https://www.linkedin.com/in/amit-bangde-4a5499259/
For inquiries or demo requests, feel free to connect!
Mobile :- 8856023298
Email: bangdeamit538@gmail.com
