# Centralized Website Project – Assignment Submission

This repository contains a project for creating a **centralized website system** integrated with **two individual websites: ILP and Centralized**. The primary objective is to implement a seamless authentication system where a user logged into the Centralized website can directly access the ILP website without re-authentication.

## 🌐 Project Overview

- **Centralized Website:** Acts as the core authentication system.
- **ILP Website:** Connected to the centralized system, allows user access if authenticated via Centralized.
- Both sites are built with a **modular frontend-backend architecture**, containerized with Docker, and equipped with **CI/CD pipelines** for efficient deployment.

---

## 📁 Directory Structure

├── centralized/ │<br>
  ├── frontend/ <br>
  │└── backend/<br> 
  ├── docker-compose.centralized.yaml <br>
├── ilp/ │ <br>
  ├── frontend/ <br>
  │└── backend/ <br>
  ├── docker-compose.yaml <br>
  ├── README.md<br>


- `centralized/`: Contains the **frontend** and **backend** code for the centralized authentication website.
- `ilp/`: Contains the **frontend** and **backend** code for the ILP website.
- `docker-compose.centralized.yml`: Manages containerization of the Centralized website.
- `docker-compose.ilp.yml`: Manages containerization of the ILP website.

---

## 🐳 Docker Architecture

Each website (Centralized & ILP) is containerized using **Docker Compose**, which includes:

- **Frontend (React/Vite/Other)**  
- **Backend (Django/Node/Other)**  
- **Database (PostgreSQL/MySQL/MongoDB etc.)**

Each component has its own dedicated `Dockerfile`.

---

## 🔁 CI/CD Pipeline

- **Frontend CI/CD:** Automatically deployed to **Vercel** on every push to the relevant branch.
- **Backend CI/CD:** Backend images are automatically pushed to **Docker Hub** using GitHub Actions or similar CI tools.

---

## 🔐 Authentication Flow

- User logs in to the **Centralized Website**.
- Session/token-based authentication is shared across services.
- The **ILP Website** checks with Centralized authentication before granting access.

---

## 🚀 Deployment Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
docker-compose -f docker-compose.centralized.yml up --build
docker-compose -f docker-compose.ilp.yml up --build
