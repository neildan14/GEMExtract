# GEMExtract 📊
**Business Development Data Management System**

GEMExtract is a standalone, enterprise-grade Python desktop application built for GEMPHIL Technologies, Inc. It allows teams to securely manage, filter, analyze, and export project data across a shared network drive.

## ✨ Core Features
* **Secure Authentication & RBAC:** Encrypted passwords (bcrypt) with strict Role-Based Access Control differentiating Administrators and standard Users.
* **Data Management (CRUD):** Add, edit, and delete records seamlessly with dynamic column sizing and text wrapping.
* **Advanced Filtering & Search:** Instantly filter data by Client, Location, Currency, or Progress, alongside a global text search.
* **Interactive Dashboard:** Built-in `Matplotlib` analytics visualizing the Top 5 Clients and total system records in real-time.
* **Excel Integration:** Quick import/export functionality using `pandas` and `openpyxl`, including customizable column selection and alphabetical sorting.
* **Smart File Previews:** Double-click table cells to instantly open Google Drive web links or local file paths (PDFs, Images) using the system's default viewer.
* **Network-Drive Ready:** Optimized SQLite concurrent read-handling with write-timeouts to prevent database locking across multiple networked computers.
* **System Backups:** One-click timestamped database backups for administrators.

## 🛠️ Tech Stack
* **Language:** Python 3
* **GUI Framework:** PyQt6
* **Database:** SQLite3
* **Analytics:** Matplotlib
* **Data Processing:** Pandas, Openpyxl
* **Security:** Bcrypt
* **Executable Compilation:** PyInstaller

## 🚀 Deployment Notes
This software is compiled into a standalone `.exe` using PyInstaller. It uses relative pathing and dynamic working directory assignment (`os.chdir`), ensuring it can be launched via desktop shortcuts while the main executable and `data` folder remain securely housed on a centralized network drive.
