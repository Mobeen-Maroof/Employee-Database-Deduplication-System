import sys
import pandas as pd

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class EmployeeCleaner(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Employee Database Deduplication")
        self.setGeometry(200, 100, 950, 600)

        self.df = None

        # ----------------- Modern Style -----------------
        self.setStyleSheet("""
        QWidget{
            background:qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #4facfe,
                stop:1 #00f2fe);
            font-family:'Segoe UI';
            font-size:14px;
        }

        QLabel{
            color:white;
            font-size:24px;
            font-weight:bold;
            padding:10px;
        }

        QPushButton{
            background-color:white;
            color:#0078d7;
            border:none;
            border-radius:12px;
            padding:12px;
            font-size:15px;
            font-weight:bold;
        }

        QPushButton:hover{
            background-color:#0078d7;
            color:white;
        }

        QPushButton:pressed{
            background-color:#005a9e;
        }

        QTableWidget{
            background:white;
            border-radius:10px;
            gridline-color:#cccccc;
            selection-background-color:#4facfe;
            selection-color:white;
        }

        QHeaderView::section{
            background:#0078d7;
            color:white;
            font-size:14px;
            font-weight:bold;
            padding:8px;
            border:none;
        }

        QScrollBar:vertical{
            background:#eeeeee;
            width:12px;
        }

        QScrollBar::handle:vertical{
            background:#0078d7;
            border-radius:5px;
        }

        QMessageBox{
            background:white;
        }
        """)

        # ----------------- Layout -----------------
        layout = QVBoxLayout()

        self.label = QLabel("👨‍💼 Employee Database Deduplication System")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.loadBtn = QPushButton("📂 Load Excel File")
        self.loadBtn.setFixedHeight(45)
        self.loadBtn.clicked.connect(self.load_file)
        layout.addWidget(self.loadBtn)

        self.cleanBtn = QPushButton("🧹 Remove Duplicates")
        self.cleanBtn.setFixedHeight(45)
        self.cleanBtn.clicked.connect(self.clean_data)
        layout.addWidget(self.cleanBtn)

        self.saveBtn = QPushButton("💾 Save Clean Dataset")
        self.saveBtn.setFixedHeight(45)
        self.saveBtn.clicked.connect(self.save_file)
        layout.addWidget(self.saveBtn)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    # ----------------- Load Excel -----------------
    def load_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Excel File",
            "",
            "Excel Files (*.xlsx)"
        )

        if filename:
            try:
                self.df = pd.read_excel(filename)
                self.show_table()

                QMessageBox.information(
                    self,
                    "Success",
                    "Dataset Loaded Successfully!"
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )

    # ----------------- Show Data -----------------
    def show_table(self):

        if self.df is None:
            return

        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iloc[i, j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

        self.table.resizeRowsToContents()

    # ----------------- Remove Duplicates -----------------
    def clean_data(self):

        if self.df is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please load an Excel file first."
            )
            return

        if "Name" in self.df.columns:
            self.df["Name"] = self.df["Name"].astype(str).str.strip().str.title()

        original_rows = len(self.df)

        self.df = self.df.drop_duplicates()

        removed = original_rows - len(self.df)

        self.show_table()

        QMessageBox.information(
            self,
            "Completed",
            f"{removed} duplicate record(s) removed successfully!"
        )

    # ----------------- Save File -----------------
    def save_file(self):

        if self.df is None:
            QMessageBox.warning(
                self,
                "Warning",
                "No data available to save."
            )
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Clean Dataset",
            "clean_employee_data.xlsx",
            "Excel Files (*.xlsx)"
        )

        if filename:
            self.df.to_excel(filename, index=False)

            QMessageBox.information(
                self,
                "Saved",
                "Clean dataset saved successfully!"
            )


# ----------------- Main -----------------
app = QApplication(sys.argv)

window = EmployeeCleaner()
window.show()

sys.exit(app.exec_())