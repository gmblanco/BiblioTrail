# 📚 BiblioTrail  
**Modular Web Platform for Centralized Library Management**

> Final Degree Project (TFG) – Universidad Pontificia Comillas (ICAI School of Engineering)  
> Author: *Guadalupe Martínez Blanco*  
> Supervisor: *Luis Francisco Sánchez Merchante*  
> Collaborating Entity: *ICAI – Universidad Pontificia Comillas*  

---

## 🧠 Project Overview

**BiblioTrail** is a web application designed to modernize and unify library management.  
The platform allows centralized access to multiple independent libraries through a single environment, maintaining their autonomy while ensuring effective communication between systems via **REST APIs** and **HTTP requests**.

Users can:
- Search and borrow books  
- Register for events  
- Reserve study rooms  
- Access multiple library systems from one website  

This project aims to **improve user experience**, **simplify administrative workflows**, and **optimize the use of available resources** in academic and institutional libraries.

---

## 🏗️ System Architecture

BiblioTrail is structured as a **distributed, modular system** composed of three independent Django projects:
1. **Central Aggregator Platform** – integrates data and provides a unified web interface  
2. **External Library Instances** – each with its own database and logic  
3. **REST API Layer** – ensures communication between libraries and the central system  

Each library exposes its own REST API, and the central platform queries these APIs to consolidate data.  
This modular architecture allows scalability, flexibility, and secure interaction between systems.

