import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import threading
import os
from datetime import datetime # ADDED: Necessary for save_report timestamp
import socket # ADDED: Necessary for hostname error handling (optional, but good practice)

# Import the core logic functions
from core_scanner import start_scan_threads, generate_pdf_report 

class PyScanGUI:
    def __init__(self, master):
        self.master = master
        master.title("PyScan: Tkinter Port Scanner")
        master.geometry("550x450")
        
        # Variables
        self.target_var = tk.StringVar(value="127.0.0.1")
        self.start_port_var = tk.IntVar(value=1)
        self.end_port_var = tk.IntVar(value=1024)
        self.is_scanning = False
        self.ports_scanned = 0
        self.total_ports = 0

        # New variable to hold the last scan data
        self.last_scan_data = {
            'target': None,
            'target_ip': None,
            'start_port': None,
            'end_port': None,
            'results': [] # List of {'port': P, 'status': S}
        }
        
        # --- Layout ---
        
        # 1. Input Frame
        input_frame = tk.Frame(master, padx=10, pady=10)
        input_frame.pack(fill='x')
        
        tk.Label(input_frame, text="Target Host:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(input_frame, textvariable=self.target_var, width=25).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Start Port:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(input_frame, textvariable=self.start_port_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(input_frame, text="End Port:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        tk.Entry(input_frame, textvariable=self.end_port_var, width=10).grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # Button Definitions (These were causing the error if start_scan was missing)
        self.scan_button = tk.Button(input_frame, text="Start Scan", command=self.start_scan, width=15, bg='green', fg='white')
        self.scan_button.grid(row=0, column=3, rowspan=2, padx=15, pady=5, sticky='e')
        
        self.save_button = tk.Button(input_frame, text="Save Report", command=self.save_report, width=15, state='disabled')
        self.save_button.grid(row=2, column=3, padx=15, pady=5, sticky='e')

        # 2. Results Area
        tk.Label(master, text="Scan Results:", anchor='w').pack(fill='x', padx=10, pady=(5, 0))
        self.results_text = scrolledtext.ScrolledText(master, height=15, state='disabled', wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 3. Status Bar
        self.status_bar = tk.Label(master, text="Ready.", bd=1, relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)


    # --- MISSING METHOD: START SCAN (Fixes the AttributeError) ---
    def start_scan(self):
        if self.is_scanning:
            return # Prevent double clicking
        
        # Input Validation
        try:
            target = self.target_var.get().strip()
            start_p = self.start_port_var.get()
            end_p = self.end_port_var.get()
            
            if not target:
                raise ValueError("Target host cannot be empty.")
            if not (1 <= start_p <= 65535 and 1 <= end_p <= 65535 and start_p <= end_p):
                raise ValueError("Invalid port range (1-65535, start <= end).")
                
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
            return

        # Prepare for scan
        self.is_scanning = True
        self.ports_scanned = 0
        self.total_ports = end_p - start_p + 1
        self.scan_button.config(text="Scanning...", state='disabled', bg='gray')
        self.save_button.config(state='disabled') # Disable save during scan
        
        # Clear previous results
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
        
        self.status_bar.config(text="Initializing scan...")

        # Start the scanner in a separate thread to prevent GUI freeze
        self.scan_thread = threading.Thread(
            target=start_scan_threads,
            args=(target, start_p, end_p, 
                  self._update_results_callback, 
                  self._finish_callback, 
                  self._update_progress_callback)
        )
        self.scan_thread.daemon = True 
        self.scan_thread.start()


    # --- HELPER METHODS FOR THREAD COMMUNICATION (Required for start_scan) ---

    def _update_results_callback(self, message, message_type="default"):
        """Called by the scanner threads to update the GUI."""
        self.master.after(0, lambda: self._safe_update_results(message, message_type))

    def _safe_update_results(self, message, message_type):
        """Actual GUI update function, runs in the main thread."""
        self.results_text.config(state='normal')
        
        self.results_text.insert(tk.END, message + "\n")
        
        # Apply tag for coloring/formatting
        if message_type == "open":
            self.results_text.tag_add("open", f"{self.results_text.index(tk.END)}-2c", tk.END)
            self.results_text.tag_config("open", foreground="green", font=('Helvetica', 10, 'bold'))
        elif message_type == "error":
            self.results_text.tag_add("error", f"{self.results_text.index(tk.END)}-2c", tk.END)
            self.results_text.tag_config("error", foreground="red")
            
        self.results_text.see(tk.END) # Scroll to the bottom
        self.results_text.config(state='disabled')

    def _update_progress_callback(self):
        """Called by the scanner threads to update the progress bar/status."""
        self.ports_scanned += 1
        progress = (self.ports_scanned / self.total_ports) * 100
        status_message = f"Scanning... {self.ports_scanned}/{self.total_ports} ports checked ({progress:.1f}%)"
        self.master.after(0, lambda: self.status_bar.config(text=status_message))


    # --- New Reporting Method (Previously provided) ---
    def save_report(self):
        """Triggers the PDF saving process."""
        if not self.last_scan_data['results'] and not self.last_scan_data['target']:
            messagebox.showinfo("No Data", "No successful scan data to save. Run a scan first.")
            return

        target = self.last_scan_data['target'] or "Unknown_Target"
        # Suggest a filename based on the target and current time
        default_filename = f"PyScan_Report_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Open file dialog to choose save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_filename,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Scan Report"
        )

        if not file_path:
            return 

        # Generate the PDF in a thread
        threading.Thread(
            target=self._generate_pdf_in_thread, 
            args=(file_path,)
        ).start()

    def _generate_pdf_in_thread(self, file_path):
        """Runs the PDF generation in a background thread."""
        try:
            self.master.after(0, lambda: self.status_bar.config(text=f"Generating PDF report..."))
            
            generate_pdf_report(
                file_path,
                self.last_scan_data['target'],
                self.last_scan_data['target_ip'],
                self.last_scan_data['start_port'],
                self.last_scan_data['end_port'],
                self.last_scan_data['results']
            )
            
            self.master.after(0, lambda: messagebox.showinfo(
                "Success", f"Scan report successfully saved to:\n{file_path}"
            ))
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror(
                "Error", f"Failed to generate PDF report: {e}"
            ))
        finally:
             self.master.after(0, lambda: self._safe_finish())

    # --- Updated Scanning Methods (Previously provided) ---

    def _finish_callback(self, target, target_ip, start_port, end_port, open_ports):
        """Called when all threads are complete, now stores data and enables save button."""
        self.is_scanning = False
        
        # 1. Store the successful scan data
        self.last_scan_data = {
            'target': target,
            'target_ip': target_ip,
            'start_port': start_port,
            'end_port': end_port,
            'results': open_ports 
        }
        
        self.master.after(0, lambda: self._safe_finish())

    def _safe_finish(self):
        self.scan_button.config(text="Start Scan", state='normal', bg='green')
        # Enable the save button only if a scan completed 
        self.save_button.config(state='normal') 
        self.status_bar.config(text="Scan Complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyScanGUI(root)
    root.mainloop()
