# 👁️ OcuVision AI - Retinal Screening Platform

OcuVision AI is a production-grade, AI-powered healthcare web application designed for early detection and grading of **Diabetic Retinopathy (DR)** using Deep Learning. Built with a modern **Next.js (React)** frontend and a robust **FastAPI (Python)** backend, the platform enables clinical practitioners to upload retinal fundus images and receive instantaneous, highly confident severity classifications.

---

## 🌟 Key Features

*   **Secure Authentication**: Medical practitioners can register and log in to manage retinal scans.
*   **AI-Powered Diagnostics**: Utilizes a fine-tuned ResNet-50 Convolutional Neural Network (CNN) to classify fundus images into five severity grades:
    *   *No DR (Normal)*
    *   *Mild*
    *   *Moderate*
    *   *Severe*
    *   *Proliferative DR*
*   **Confidence Scoring**: Real-time confidence percentage output alongside the diagnosis.
*   **Interactive Dashboard**: Provides high-level statistics of total scans, latest diagnosis, and key warning alerts for high-risk patients.
*   **Screening History**: Securely tracks and logs past scans for patient progression analysis.
*   **Modern Glassmorphism UI**: Beautiful, fully responsive frontend optimized for tablets, laptops, and desktops.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Next.js (App Router), React, TypeScript | Fast, server-side rendered client with responsive glassmorphic styling. |
| **Backend** | FastAPI, Python 3.x | Lightweight, high-performance API backend. |
| **Database** | SQLite, SQLAlchemy ORM | Relational database for managing user accounts and prediction histories. |
| **Deep Learning** | PyTorch, Torchvision | Deep Learning framework used to train and run ResNet-50 models. |

---

## 📁 Repository Structure

```text
OcuVision-AI/
├── backend/                # Python FastAPI Backend
│   ├── database.py         # SQLAlchemy connection & session setup
│   ├── main.py             # API endpoints (Auth, Predict, History)
│   ├── ml_model.py         # PyTorch model loader & inference wrapper
│   ├── models.py           # DB tables (User, Prediction)
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/            # App Router pages (Dashboard, Scan, History)
│   │   └── components/     # Reusable layout and sidebars
│   ├── package.json        # Node.js dependencies
│   └── tsconfig.json       # TypeScript configuration
├── utils/                  # Helper modules
├── train_model.py          # Transfer learning training script for ResNet-50
├── requirements.txt        # Top-level Python requirements
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed on your machine:
*   [Python 3.8+](https://www.python.org/downloads/)
*   [Node.js v18+](https://nodejs.org/)
*   [Git](https://git-scm.com/)

---

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend API will run at `http://localhost:8000`.

---

### 2. Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Run the Next.js development server:
   ```bash
   npm run dev
   ```
   Open your browser and navigate to `http://localhost:3000` to interact with the application.

---

### 3. Machine Learning Model Training (Optional)

If you wish to train the model from scratch or fine-tune it further:
1. Download the APTOS 2019 dataset (Gaussian filtered images).
2. Place the dataset in `dataset/archive/gaussian_filtered_images/gaussian_filtered_images`.
3. Run the training script:
   ```bash
   python train_model.py
   ```
4. The trained model weights will be saved in the root directory as `model.pth`.

---

## 🔒 Security & Data Privacy

*   Passwords are encrypted locally using SHA-256 before database insertion.
*   Retinal images are safely stored in local directories for auditable history tracking.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Contributors

*   **Krishna Agarwal** - [GitHub](https://github.com/Krishna-Agarwal04)
*   **Prakhar Goel**

