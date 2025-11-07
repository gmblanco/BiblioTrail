# 📚 BiblioTrail  
**Modular Web Platform for Centralized Library Management**

> Final Degree Project (TFG) – Universidad Pontificia Comillas (ICAI School of Engineering)  
> Author: *Guadalupe Martínez Blanco*  
> Supervisor: *Luis Francisco Sánchez Merchante*  
> Collaborating Entity: *ICAI – Universidad Pontificia Comillas*
> Grade: *9.5/10*
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
1. **Central Aggregator Platform (Bibliotrail)** – integrates data and provides a unified web interface  
2. **External Library Instances (biblioteca1 & biblioteca2)** – each with its own database and logic  
3. **REST API Layer** – ensures communication between libraries and the central system  

Each library exposes its own REST API, and the central platform queries these APIs to consolidate data.  
This modular architecture allows scalability, flexibility, and secure interaction between systems.

Each library exposes its own **REST API**, and the central platform queries these APIs to display unified information on the website. This approach preserves the independence of each library while enabling centralized access.

**High-level stack:**
```
Frontend  →  HTML, CSS, JavaScript  
Backend   →  Django + Django REST Framework  
Database  →  PostgreSQL (plus local DBs per library)  
APIs      →  REST endpoints (JSON over HTTP)
```

---

## 💡 Key Features

- 🔍 **Centralized Search:** Unified access to the catalogs of multiple independent libraries.  
- 📚 **Book Management:** Search, borrow, and return books from a single interface.  
- 🧾 **Event Registration:** Register and manage participation in library events.  
- 🏠 **Room Reservation:** Book study or meeting rooms directly through the platform.  
- 👥 **User Roles:** Different permissions for users, librarians, and administrators.  
- 🔐 **Security:** Authentication, session management, and permission-based access.  
- 📱 **Responsive Design:** Optimized layout for desktop, tablet, and mobile devices.  
- ⚙️ **Modular Architecture:** Scalable system designed to integrate new libraries easily.  

---

## ⚙️ Technologies Used

| Layer | Technologies |
|--------|---------------|
| **Backend** | Python 3, Django, Django REST Framework |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | PostgreSQL (plus independent DBs for each library) |
| **Communication** | REST APIs, HTTP requests |
| **Version Control** | Git & GitHub |
| **Design Tools** | Figma (mockups and UI planning) |

---

## 📊 Results

The development of **BiblioTrail** successfully met all the objectives defined at the beginning of the project.

- ✅ A functional and intuitive **web platform** was implemented for centralized library management.  
- ✅ Effective **communication between systems** was achieved through REST API queries, maintaining the independence of each library.  
- ✅ Secure **user authentication** and permission management were developed using Django’s built-in tools.  
- ✅ The interface is **responsive, accessible, and easy to navigate**, allowing users to search books, manage loans, and register for events from a single environment.  
- ✅ Proper **version control** was maintained via GitHub throughout the development process.  
- ✅ Migration to **PostgreSQL** and modular design ensured scalability and robustness for future extensions.

Testing confirmed the correct operation of each module, including search, reservations, event registration, and user management, validating the project’s technical and functional success.

---

## 🎯 Conclusions

**BiblioTrail** provides an efficient, modular, and scalable solution for library management, enabling unified access to services while respecting the autonomy of each institution.  
The system demonstrates how distributed architectures and REST-based communication can modernize traditional library systems without requiring changes to their internal logic.

**Key takeaways:**
- The integration of Django and Django REST Framework provided a secure and extensible foundation.  
- The modular approach simplifies future maintenance and integration of new libraries.  
- User experience was prioritized through a clean, accessible, and responsive design.  
- The project highlights the importance of interoperability between independent systems.

To conclude, **BiblioTrail** achieves its goal of centralizing access to independent library systems, improving efficiency and accessibility for users, librarians, and academic institutions alike.
For more informatio 📘 [Read the full TFG report (PDF)](https://repositorio.comillas.edu/jspui/handle/11531/95211)



