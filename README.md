# 👁️ PyScan GUI: Multi-threaded Port Scanner with PDF Reporting

A powerful, user-friendly **Graphical User Interface (GUI)** port scanner built with Python's Tkinter, now featuring robust **scan reporting** capabilities. The tool uses multithreading for speed and generates professional PDF reports of the scan results in a clear tabular format for easy auditing and record-keeping.

## ✨ Features

* **GUI Interface:** Simple, intuitive interface built with Tkinter.
* **Multi-threaded Scanning:** Uses `threading` for rapid, concurrent port checks.
* **PDF Report Generation (NEW!):** Creates detailed, time-stamped PDF files of every scan.
* **Tabular Results:** Presents scan parameters and open ports in clean, organized tables within the PDF report.
* **Custom Range:** Easily define the target host and port range (1-65535).
* **Real-time Feedback:** Updates progress and results without freezing the application.

## 🚀 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/PyScan-GUI.git](https://github.com/YourUsername/PyScan-GUI.git)
    cd PyScan-GUI
    ```

2.  **Install Dependencies:**
    You need **Python 3.x** and the `reportlab` library for PDF generation.

    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Usage

### Starting the Application

Run the main GUI script directly from your terminal:

```bash
python pyscanner_gui.py
