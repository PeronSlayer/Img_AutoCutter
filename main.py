import os
import sys
import time
#
from PIL import Image
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QCoreApplication, QRectF
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QSplashScreen, QMainWindow, QProgressDialog,
    QApplication, QDesktopWidget, QWidget,
    QLabel, QVBoxLayout, QPushButton, QFormLayout, QLineEdit,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QTreeView, QFileSystemModel, QDialog
)
from qdarkstyle import load_stylesheet_pyqt5
from imgtopdf import ConvertPNGtoPDFApp
from shared import ControlButtons, MainBar


class FileExplorerWindow(QDialog):
    file_selected_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        script_directory = os.path.dirname(os.path.abspath(__file__))

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(QCoreApplication.applicationDirPath())

        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index(script_directory))
        self.tree_view.setFixedSize(500, 250)

        self.open_button = QPushButton('Open', self)
        # noinspection PyUnresolvedReferences
        self.open_button.clicked.connect(self.open_selected_file)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_view)
        layout.addWidget(self.open_button)

    def open_selected_file(self):
        selected_index = self.tree_view.currentIndex()
        selected_path = self.file_system_model.filePath(selected_index)
        if os.path.isfile(selected_path):
            # noinspection PyUnresolvedReferences
            self.file_selected_signal.emit(selected_path)


class ImgCutter(QMainWindow):
    def __init__(self):
        super().__init__()

        # Var Initialization
        self.mainBar_widget = None
        self.controlButtons_widget = None
        self.skip_x_entry, self.height_startEntry, self.weight_startEntry = None, None, None
        self.image_item, self.graphics_scene, self.graphics_view = None, None, None
        self.weightStart, self.heightStart, self.skip_x = 1000, 1000, 200
        self.pdf_converter_window = None
        self.file_explorer_window = None
        self.image_path = None

        # Call of UI method ( Starting program )
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Img AutoCutter - Alberto Lopez')
        self.setMinimumSize(800, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)

        self.image_item = QGraphicsPixmapItem()
        self.graphics_scene.addItem(self.image_item)

        labels = [
            ("Set the cut Width: (px)", self.weight_startEntry, str(self.weightStart)),
            ("Set the cut Height: (px)", self.height_startEntry, str(self.heightStart)),
            ("Set the Skip for the next cut: (px)", self.skip_x_entry, str(self.skip_x))
        ]

        footer_lbl = ("Copyright 2024 Alberto Lopez - This is software is Under the MIT License. ")

        self.mainBar_widget = MainBar(self)
        self.mainBar_widget.setFixedHeight(30)
        layout.addWidget(self.mainBar_widget)
        
        layout.addWidget(self.graphics_view)

        form_layout = QFormLayout()
        for label_text, entry, default_value in labels:
            label = QLabel(label_text)
            entry = QLineEdit(default_value)
            form_layout.addRow(label, entry)

        layout.addLayout(form_layout)

        self.controlButtons_widget = ControlButtons(self)
        self.controlButtons_widget.zoom_in_signal.connect(self.zoom_in_action)
        self.controlButtons_widget.zoom_out_signal.connect(self.zoom_out_action)
        self.controlButtons_widget.show_explorer_signal.connect(self.show_fileExplorer)
        self.mainBar_widget.show_explorer_signal.connect(self.show_fileExplorer)
        self.controlButtons_widget.cut_signal.connect(self.cut_apply)
        self.controlButtons_widget.show_pdf_converter_signal.connect(self.show_pdf_converter)

        layout.addWidget(self.controlButtons_widget)

    # noinspection PyPep8Naming
    def show_fileExplorer(self):
        if self.file_explorer_window is None or not self.file_explorer_window.isVisible():
            self.file_explorer_window = FileExplorerWindow(self)
            self.file_explorer_window.setWindowTitle('File Explorer')
            main_pos = self.pos()
            file_explorer_pos = main_pos + QPoint(self.width(), 0)
            self.file_explorer_window.move(file_explorer_pos)
            self.file_explorer_window.show()
        else:
            self.file_explorer_window.close()
        # noinspection PyUnresolvedReferences
        self.file_explorer_window.file_selected_signal.connect(self.handle_selected_file)

    def show_pdf_converter(self):
        if self.pdf_converter_window is None or not self.pdf_converter_window.isVisible():
            self.pdf_converter_window = ConvertPNGtoPDFApp()
            self.pdf_converter_window.setGeometry(300, 200, 600, 600)
            self.pdf_converter_window.show()

    def handle_selected_file(self, selected_file_path):
        self.image_path = selected_file_path
        self.load_image()

    def zoom_in_action(self):
        self.graphics_view.scale(1.2, 1.2)

    def zoom_out_action(self):
        self.graphics_view.scale(1 / 1.2, 1 / 1.2)

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_item.setPixmap(pixmap)
        self.graphics_view.setSceneRect(QRectF(pixmap.rect()))
        self.graphics_view.resetTransform()

    def cut_apply(self):
        if self.image_path:
            try:
                self.weightStart = int(self.weight_startEntry.text())
                self.heightStart = int(self.height_startEntry.text())
                self.skip_x = int(self.skip_x_entry.text())

                progress_dialog = QProgressDialog("Applying cut...", None, 0, 0, self)
                progress_dialog.setWindowModality(Qt.WindowModal)
                progress_dialog.setWindowTitle("Cutting...")
                progress_dialog.show()

                self.cut_image(self.image_path, "output", self.weightStart, self.heightStart, self.skip_x,
                               progress_dialog)

                progress_dialog.close()

            except ValueError:
                print("Error")

    # noinspection PyUnusedLocal
    @staticmethod
    def cut_image(input_path, output_path, weight_start, height_start, skip_x, progress_dialog):
        image = Image.open(input_path)
        weight_tot, height_tot = image.size

        current_step = 0

        colons = (weight_tot // weight_start)
        rows = (height_tot // height_start)
        total_steps = rows * colons

        program_directory = os.path.dirname(sys.argv[0])

        output_folder = os.path.join(program_directory, "cut")
        os.makedirs(output_folder, exist_ok=True)

        for riga in range(rows):
            for colons in range(colons):
                x = colons * weight_start + colons * skip_x

                parte = image.crop((x, 0, x + weight_start, height_start))
                output_file_path = os.path.join(output_folder, f"part_{riga + 1}_{colons + 1}.png")
                parte.save(output_file_path)

                current_step += 1
                progress_dialog.setValue(current_step)

                if current_step % 10 == 0:
                    QApplication.processEvents()

        progress_dialog.setValue(total_steps)

    def move_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())

    splash_pix = QPixmap('icons/splashscreen.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    for i in range(1, 11):
        splash.showMessage(f"Loading... {i * 10}%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
        time.sleep(0.2)
        app.processEvents()

    splash.close()

    ex = ImgCutter()
    app.setWindowIcon(QIcon('icons/icon.png'))
    ex.setGeometry(300, 200, 600, 600)
    ex.move_center()
    ex.show()
    sys.exit(app.exec_())
