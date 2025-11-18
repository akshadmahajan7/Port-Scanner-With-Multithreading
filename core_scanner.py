# core_scanner.py

import socket
import threading
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --- Existing Scan Logic Remains Here ---
# (scan_port and start_scan_threads functions are the same as before, 
# but they now need to ensure `open_ports` contains only the port number 
# or a structured result if you want more detail.)

def scan_port(target_ip, port, results_list, progress_callback):
    """
    Attempts to connect to a single port, storing the port number if open.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) 
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            # Store the structured result (port, status)
            results_list.append({'port': port, 'status': 'OPEN'})
        
        s.close()
    except Exception:
        # Ignore silent errors, but you could log them for debugging
        pass
    
    if progress_callback:
        progress_callback()

def start_scan_threads(target, start_port, end_port, update_result_callback, finish_callback, update_progress_callback):
    # ... (Error handling and setup code remains the same) ...
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        update_result_callback("Hostname could not be resolved. Please check the target.", "error")
        finish_callback()
        return

    update_result_callback(f"Starting scan on {target_ip}...", "info")
    
    total_ports = end_port - start_port + 1
    threads = []
    # This list will hold structured results: [{'port': 80, 'status': 'OPEN'}, ...]
    structured_results = [] 
    
    # ... (Threading loop remains the same, using `structured_results` for the port list) ...

    for port in range(start_port, end_port + 1):
        t = threading.Thread(
            target=scan_port, 
            args=(target_ip, port, structured_results, update_progress_callback)
        )
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # --- Reporting Results ---
    open_ports = [r for r in structured_results if r['status'] == 'OPEN']
    
    if open_ports:
        # Sort and update GUI with open ports
        for result in sorted(open_ports, key=lambda x: x['port']):
             update_result_callback(f"Port {result['port']} is {result['status']}", "open")
        
        # Pass the final structured data and target info back to the GUI callback
        finish_callback(target, target_ip, start_port, end_port, open_ports)
    else:
        update_result_callback("Scan completed. No open ports found in the specified range.", "info")
        finish_callback(target, target_ip, start_port, end_port, [])


# --- NEW PDF GENERATION FUNCTION ---

def generate_pdf_report(filename, target, target_ip, start_port, end_port, results):
    """
    Creates a PDF report containing the scan results in a tabular format.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []
    
    # --- 1. Title and Metadata ---
    title = f"PyScan Report: {target}"
    Story.append(Paragraph(title, styles['Title']))
    Story.append(Spacer(1, 12))
    
    date_str = f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    Story.append(Paragraph(date_str, styles['Normal']))
    Story.append(Spacer(1, 12))

    # --- 2. Scan Parameters Table ---
    params_data = [
        ['Parameter', 'Value'],
        ['Target Host', target],
        ['Target IP', target_ip],
        ['Port Range', f"{start_port} - {end_port}"],
        ['Total Ports Scanned', end_port - start_port + 1],
        ['Open Ports Found', len(results)],
    ]

    param_table = Table(params_data, colWidths=[150, 300])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    Story.append(Paragraph("Scan Parameters:", styles['h2']))
    Story.append(param_table)
    Story.append(Spacer(1, 24))

    # --- 3. Results Table ---
    Story.append(Paragraph("Detailed Results (Open Ports):", styles['h2']))

    if not results:
        Story.append(Paragraph("No open ports found in the specified range.", styles['Normal']))
    else:
        data = [['Port Number', 'Status']]
        for result in sorted(results, key=lambda x: x['port']):
            data.append([str(result['port']), result['status']])

        # Create the table
        res_table = Table(data)
        res_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Highlight the status for OPEN ports
            ('TEXTCOLOR', (1, 1), (1, -1), colors.green) 
        ]))
        Story.append(res_table)
    
    doc.build(Story)
    return True
