import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

BASE_URL = "http://127.0.0.1:8000/api"

# ✅ Put your Django superuser here (same one that works in browser admin)
AUTH = ("ridhima", "behappy")   # <-- change password if needed


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(950, 700)

        layout = QVBoxLayout()

        self.status = QLabel("Status: Ready")
        layout.addWidget(self.status)

        btn_row = QHBoxLayout()

        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.clicked.connect(self.upload_csv)
        btn_row.addWidget(self.btn_upload)

        self.btn_refresh = QPushButton("Refresh Summary")
        self.btn_refresh.clicked.connect(self.fetch_summary)
        btn_row.addWidget(self.btn_refresh)

        self.btn_pdf = QPushButton("Download PDF Report")
        self.btn_pdf.clicked.connect(self.download_pdf)
        btn_row.addWidget(self.btn_pdf)

        layout.addLayout(btn_row)

        # Table to show summary key-value pairs
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Metric", "Value"])
        layout.addWidget(self.table)

        # Matplotlib chart
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # Load summary initially
        self.fetch_summary()

    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            with open(path, "rb") as f:
                files = {"file": f}
                r = requests.post(f"{BASE_URL}/upload/", files=files, auth=AUTH, timeout=20)

            if r.status_code not in (200, 201):
                QMessageBox.critical(self, "Upload Failed", r.text)
                return

            self.status.setText("Status: Upload successful ✅")
            self.fetch_summary()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def fetch_summary(self):
        try:
            # 1) Summary
            r = requests.get(f"{BASE_URL}/summary/", auth=AUTH, timeout=20)
            if r.status_code != 200:
                QMessageBox.critical(self, "Error", r.text)
                return

            data = r.json()
            if isinstance(data, dict) and data.get("message"):
                self.status.setText(f"Status: {data['message']}")
                self.table.setRowCount(0)
                self.draw_chart({})
                return

            # ✅ WOW FEATURE #1: Alert count
            alerts = data.get("alerts", [])

            # ✅ WOW FEATURE #2: Trend (from history endpoint)
            trend = "Unknown"
            try:
                r2 = requests.get(f"{BASE_URL}/history/", auth=AUTH, timeout=20)
                if r2.status_code == 200:
                    # if your backend returns {"trend": "..."} this works
                    # if it returns a list, trend stays Unknown (safe)
                    hist_json = r2.json()
                    if isinstance(hist_json, dict):
                        trend = hist_json.get("trend", "Unknown")
            except:
                pass

            # ✅ Status line shows both
            self.status.setText(
                f"Status: Summary loaded ✅ | Alerts: {len(alerts)} | Trend: {trend}"
            )

            self.show_summary_table(data)
            self.draw_chart(data.get("type_distribution", {}))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_summary_table(self, summary: dict):
        items = list(summary.items())
        self.table.setRowCount(len(items))

        for i, (k, v) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.table.setItem(i, 1, QTableWidgetItem(str(v)))

        self.table.resizeColumnsToContents()

    def draw_chart(self, dist: dict):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        if dist:
            ax.bar(list(dist.keys()), list(dist.values()))
            ax.set_title("Equipment Type Distribution")
            ax.set_xlabel("Type")
            ax.set_ylabel("Count")
        else:
            ax.set_title("No chart data (upload a CSV)")

        self.canvas.draw()

    def download_pdf(self):
        try:
            r = requests.get(f"{BASE_URL}/report/pdf/", auth=AUTH, timeout=30)
            if r.status_code != 200:
                QMessageBox.critical(self, "PDF Error", r.text)
                return

            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF", "equipment_report.pdf", "PDF Files (*.pdf)"
            )
            if not save_path:
                return

            with open(save_path, "wb") as f:
                f.write(r.content)

            self.status.setText(f"Status: PDF saved ✅ ({save_path})")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DesktopApp()
    w.show()
    sys.exit(app.exec_())
