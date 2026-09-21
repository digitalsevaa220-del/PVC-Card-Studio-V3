from pathlib import Path
import json
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QPixmap, QImage
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem, QSpinBox, QDoubleSpinBox,
    QComboBox, QGroupBox, QFormLayout
)

PRESETS = {
    "CR80 PVC Card": (85.60, 53.98),
    "ID Card": (85.60, 53.98),
    "Custom": (85.60, 53.98),
}

class CardScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.card_w_mm = 85.60
        self.card_h_mm = 53.98
        self.scale_px = 5
        self.refresh()

    def refresh(self):
        self.clear()
        w = self.card_w_mm * self.scale_px
        h = self.card_h_mm * self.scale_px
        self.setSceneRect(0, 0, w, h)
        card = self.addRect(
            QRectF(0, 0, w, h),
            QPen(Qt.black, 2),
            QBrush(Qt.white)
        )
        card.setZValue(-100)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PVC Card Studio V3")
        self.resize(1200, 760)
        self.scene = CardScene()
        self.build_ui()

    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        main = QHBoxLayout(root)

        left = QVBoxLayout()
        title = QLabel("<h2>PVC Card Studio V3</h2>")
        left.addWidget(title)

        box = QGroupBox("Card Settings")
        form = QFormLayout(box)

        self.preset = QComboBox()
        self.preset.addItems(PRESETS.keys())
        self.preset.currentTextChanged.connect(self.change_preset)
        form.addRow("Preset", self.preset)

        self.w = QDoubleSpinBox()
        self.w.setRange(10, 500)
        self.w.setDecimals(2)
        self.w.setValue(85.60)
        form.addRow("Width (mm)", self.w)

        self.h = QDoubleSpinBox()
        self.h.setRange(10, 500)
        self.h.setDecimals(2)
        self.h.setValue(53.98)
        form.addRow("Height (mm)", self.h)

        self.dpi = QSpinBox()
        self.dpi.setRange(72, 1200)
        self.dpi.setValue(300)
        form.addRow("DPI", self.dpi)

        left.addWidget(box)

        for text, fn in [
            ("Add Text", self.add_text),
            ("Add Photo", self.add_photo),
            ("Add Rectangle", self.add_rectangle),
            ("Open File", self.open_file),
            ("Save Project", self.save_project),
            ("Load Project", self.load_project),
            ("Export PDF", self.export_pdf),
        ]:
            b = QPushButton(text)
            b.clicked.connect(fn)
            left.addWidget(b)

        left.addStretch()
        main.addLayout(left, 0)

        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setBackgroundBrush(Qt.lightGray)
        main.addWidget(self.view, 1)

        self.statusBar().showMessage("Ready")

    def change_preset(self, name):
        w, h = PRESETS[name]
        self.w.setValue(w)
        self.h.setValue(h)
        self.scene.card_w_mm = w
        self.scene.card_h_mm = h
        self.scene.refresh()

    def add_text(self):
        item = QGraphicsTextItem("Double-click to edit")
        item.setDefaultTextColor(Qt.black)
        item.setPos(20, 20)
        self.scene.addItem(item)

    def add_rectangle(self):
        self.scene.addRect(40, 40, 180, 80, QPen(Qt.black), QBrush(Qt.NoBrush))

    def add_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "",
            "Images (*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff)"
        )
        if not path:
            return
        pix = QPixmap(path)
        if pix.isNull():
            QMessageBox.warning(self, "Photo", "Could not load image.")
            return
        pix = pix.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.scene.addPixmap(pix).setPos(40, 40)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open document",
            "",
            "Supported files (*.pdf *.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff *.docx *.csv *.txt *.json)"
        )
        if path:
            self.statusBar().showMessage(f"Selected: {Path(path).name}")

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "card.pcstudio",
            "PVC Studio Project (*.pcstudio)"
        )
        if not path:
            return
        data = {
            "version": 3,
            "width_mm": self.w.value(),
            "height_mm": self.h.value(),
            "dpi": self.dpi.value(),
            "preset": self.preset.currentText()
        }
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.statusBar().showMessage("Project saved.")

    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Project", "", "PVC Studio Project (*.pcstudio)"
        )
        if not path:
            return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            self.w.setValue(float(data.get("width_mm", 85.6)))
            self.h.setValue(float(data.get("height_mm", 53.98)))
            self.dpi.setValue(int(data.get("dpi", 300)))
            self.scene.card_w_mm = self.w.value()
            self.scene.card_h_mm = self.h.value()
            self.scene.refresh()
            self.statusBar().showMessage("Project loaded.")
        except Exception as e:
            QMessageBox.critical(self, "Load error", str(e))

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "card.pdf", "PDF (*.pdf)"
        )
        if not path:
            return
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import mm
            c = canvas.Canvas(path, pagesize=(self.w.value()*mm, self.h.value()*mm))
            c.setStrokeColorRGB(0, 0, 0)
            c.rect(0, 0, self.w.value()*mm, self.h.value()*mm)
            c.save()
            self.statusBar().showMessage("PDF exported.")
        except Exception as e:
            QMessageBox.critical(self, "Export error", str(e))
