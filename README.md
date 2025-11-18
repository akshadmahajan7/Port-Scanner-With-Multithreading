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
```

## 📄 Generating a Report

The **PyScan GUI** makes generating a comprehensive scan report straightforward and user-friendly.

* **1. Complete a Successful Scan:** Start by entering the **target/ports** and clicking the **Start Scan** button.
* **2. Activate Save Button:** Once the scan is finished, the **Save Report** button will automatically become **active**.
* **3. Save the PDF:** Click **Save Report** to open a file dialog, allowing you to **name the PDF file** and choose the **save location**.

The final PDF report provides all necessary audit information, including:
* **Scan Metadata:** Target, IP, and Port Range.
* **Tabular List:** A clean, organized list of all identified **open ports**.

---

## ⚙️ Technical Details

The project is architecturally designed for clarity and maintainability:

* **`core_scanner.py`**:
    * Houses the **multi-threaded scanning logic**.
    * Contains the **PDF generation function** using the powerful `reportlab` library.
* **`pyscanner_gui.py`**:
    * Manages the primary **Tkinter interface**.
    * Handles **thread-safe updates** to the GUI.
    * Uses the `filedialog` module to manage saving the reports.

---

## ⚠️ Disclaimer

This tool is **strictly** for **educational** and **authorized security testing** purposes. **Network scanning without explicit, written permission is illegal and unethical.** The developers are not responsible for any misuse of this tool.

---

## 🤝 Contribution

We actively welcome contributions to enhance PyScan GUI! Suggested ideas include:

* Adding an option to save reports as a simple **CSV file**.
* Implementing **service version detection (banner grabbing)** and including this data in the report table.
* Improving the overall **PDF template styling** and design.

---

## 📄 License

This project is licensed under the **MIT License** - please refer to the `LICENSE` file for full details.
