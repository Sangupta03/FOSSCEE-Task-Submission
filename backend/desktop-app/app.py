import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QInputDialog, QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

BASE_URL = "http://127.0.0.1:8000/api"


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(950, 700)

        # store auth after prompt
        self.AUTH = None

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

        # Summary table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Metric", "Value"])
        layout.addWidget(self.table)

        # Chart
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # ask auth once
        if not self.ensure_auth():
            self.status.setText("Status: Login cancelled")
            return

        self.fetch_summary()

    def ensure_auth(self):
        """Prompt for username/password and store in self.AUTH."""
        if self.AUTH and self.AUTH[0] and self.AUTH[1]:
            return True

        user, ok1 = QInputDialog.getText(self, "Login", "Username:")
        if not ok1 or not user.strip():
            return False

        pwd, ok2 = QInputDialog.getText(
            self, "Login", "Password:", echo=QLineEdit.Password
        )
        if not ok2 or not pwd:
            return False

        self.AUTH = (user.strip(), pwd)
        return True

    def upload_csv(self):
        if not self.ensure_auth():
            return

        path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            with open(path, "rb") as f:
                files = {"file": f}
                r = requests.post(f"{BASE_URL}/upload/", files=files, auth=self.AUTH, timeout=15)

            if r.status_code == 401:
                QMessageBox.warning(self, "Auth", "Login failed. Please re-enter credentials.")
                self.AUTH = None
                if self.ensure_auth():
                    return self.upload_csv()
                return

            if r.status_code not in (200, 201):
                QMessageBox.critical(self, "Upload Failed", f"{r.status_code}\n{r.text}")
                return

            self.status.setText("Status: Upload successful ✅")
            self.fetch_summary()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def fetch_summary(self):
        if not self.ensure_auth():
            return

        try:
            r = requests.get(f"{BASE_URL}/summary/", auth=self.AUTH, timeout=15)

            if r.status_code == 401:
                QMessageBox.warning(self, "Auth", "Login failed. Please re-enter credentials.")
                self.AUTH = None
                if self.ensure_auth():
                    return self.fetch_summary()
                return

            if r.status_code != 200:
                QMessageBox.critical(self, "Error", f"{r.status_code}\n{r.text}")
                return

            data = r.json()

            if isinstance(data, dict) and data.get("message"):
                self.status.setText(f"Status: {data['message']}")
                self.table.setRowCount(0)
                self.draw_chart({})
                return

            # ✅ WOW FEATURE: Alert count in status bar
            alerts = data.get("alerts", []) if isinstance(data, dict) else []
            self.status.setText(f"Status: Summary loaded ✅ | Alerts: {len(alerts)}")

            self.show_summary_table(data)
            self.draw_chart(data.get("type_distribution", {}) if isinstance(data, dict) else {})

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, "Backend Not Running",
                "Cannot connect to Django backend.\n\nStart Django:\npython manage.py runserver 8000"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_summary_table(self, summary):
        if not isinstance(summary, dict):
            self.table.setRowCount(0)
            return

        items = list(summary.items())
        self.table.setRowCount(len(items))

        for i, (k, v) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.table.setItem(i, 1, QTableWidgetItem(str(v)))

        self.table.resizeColumnsToContents()

    def draw_chart(self, dist):
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        if dist:
            ax.bar(list(dist.keys()), list(dist.values()))
            ax.set_title("Equipment Type Distribution")
        else:
            ax.set_title("No data yet")

        self.canvas.draw()

    def download_pdf(self):
        if not self.ensure_auth():
            return

        try:
            r = requests.get(f"{BASE_URL}/report/pdf/", auth=self.AUTH, timeout=15)

            if r.status_code == 401:
                QMessageBox.warning(self, "Auth", "Login failed. Please re-enter credentials.")
                self.AUTH = None
                if self.ensure_auth():
                    return self.download_pdf()
                return

            if r.status_code != 200:
                QMessageBox.critical(self, "PDF Error", f"{r.status_code}\n{r.text}")
                return

            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF", "equipment_report.pdf", "PDF Files (*.pdf)"
            )
            if not save_path:
                return

            with open(save_path, "wb") as f:
                f.write(r.content)

            self.status.setText("Status: PDF saved ✅")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, "Backend Not Running",
                "Cannot connect to Django backend.\n\nStart Django:\npython manage.py runserver 8000"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
