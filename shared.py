# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QAction, QProgressDialog, QApplication, QDesktopWidget, QWidget,
                             QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout, QLineEdit, QGraphicsView,
                             QGraphicsScene, QGraphicsPixmapItem, QToolButton, QTreeView, QSizePolicy, QFileSystemModel,
                             QDialog)
# noinspection PyUnresolvedReferences
from PyQt5.QtGui import QPixmap, QIcon
# noinspection PyUnresolvedReferences
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QDir, QPoint, QCoreApplication, QSize
from qtawesome import icon


# noinspection PyUnresolvedReferences,PyPep8,PyPep8Naming
class ControlButtons(QWidget):
    zoomIn_btn: QToolButton | QToolButton
    zoom_in_signal = pyqtSignal()
    zoom_out_signal = pyqtSignal()
    show_explorer_signal = pyqtSignal()
    cut_signal = pyqtSignal()
    show_pdf_converter_signal = pyqtSignal()
    wip_message_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        icon_size = QSize(50, 50)

        self.zoomIn_btn = QToolButton(self)
        self.zoomIn_btn.setIconSize(icon_size)
        self.zoomIn_btn.setIcon(icon('fa5s.search-plus', color='white'))
        self.zoomIn_btn.clicked.connect(self.zoom_in)
        self.zoomIn_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomIn_btn.setFixedSize(74, 74)

        self.zoomOut_btn = QToolButton(self)
        self.zoomOut_btn.setIconSize(icon_size)
        self.zoomOut_btn.setIcon(icon('fa5s.search-minus', color='white'))
        self.zoomOut_btn.clicked.connect(self.zoom_out)
        self.zoomOut_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomOut_btn.setFixedSize(74, 74)

        self.openExplorer = QToolButton(self)
        self.openExplorer.setIconSize(icon_size)
        self.openExplorer.setIcon(icon('fa5s.folder-open', color='white'))
        self.openExplorer.clicked.connect(self.show_fileExplorer)
        self.openExplorer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.openExplorer.setFixedSize(74, 74)

        self.exit_btn = QToolButton(self)
        self.exit_btn.setIconSize(icon_size)
        self.exit_btn.setIcon(icon('fa5s.sign-out-alt', color='white'))
        self.exit_btn.clicked.connect(QApplication.instance().quit)
        self.exit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exit_btn.setFixedSize(74, 74)

        self.applyCut_btn = QToolButton(self)
        self.applyCut_btn.setIconSize(icon_size)
        self.applyCut_btn.setIcon(icon('fa5s.cut', color='white'))
        self.applyCut_btn.clicked.connect(self.apply_cut)
        self.applyCut_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.applyCut_btn.setFixedSize(74, 74)

        self.pdfConv_btn = QToolButton(self)
        self.pdfConv_btn.setIconSize(icon_size)
        self.pdfConv_btn.setIcon(QIcon('icons/pdf-icon.png'))
        self.pdfConv_btn.clicked.connect(self.show_pdf_converter)
        self.pdfConv_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pdfConv_btn.setFixedSize(74, 74)
        self.pdfConv_btn.setEnabled(False)

        self.zoomIn_lbl = QLabel('Zoom In', self)
        self.zoomIn_lbl.setAlignment(Qt.AlignCenter)

        self.zoomOut_lbl = QLabel('Zoom Out', self)
        self.zoomOut_lbl.setAlignment(Qt.AlignCenter)

        self.explorer_lbl = QLabel('Open', self)
        self.explorer_lbl.setAlignment(Qt.AlignCenter)

        self.exit_lbl = QLabel('Close', self)
        self.exit_lbl.setAlignment(Qt.AlignCenter)

        self.apply_lbl = QLabel('Cut', self)
        self.apply_lbl.setAlignment(Qt.AlignCenter)

        self.pdf_lbl = QLabel('PDF Converter', self)
        self.pdf_lbl.setAlignment(Qt.AlignCenter)
        self.pdf_lbl.setStyleSheet("color: gray")

        zoomIn_layout = QVBoxLayout()
        zoomIn_layout.addWidget(self.zoomIn_lbl)
        zoomIn_layout.addWidget(self.zoomIn_btn)

        zoomOut_layout = QVBoxLayout()
        zoomOut_layout.addWidget(self.zoomOut_lbl)
        zoomOut_layout.addWidget(self.zoomOut_btn)

        explorer_layout = QVBoxLayout()
        explorer_layout.addWidget(self.explorer_lbl)
        explorer_layout.addWidget(self.openExplorer)

        exit_layout = QVBoxLayout()
        exit_layout.addWidget(self.exit_lbl)
        exit_layout.addWidget(self.exit_btn)

        apply_layout = QVBoxLayout()
        apply_layout.addWidget(self.apply_lbl)
        apply_layout.addWidget(self.applyCut_btn)

        pdf_layout = QVBoxLayout()
        pdf_layout.addWidget(self.pdf_lbl)
        pdf_layout.addWidget(self.pdfConv_btn)

        button_layout = QHBoxLayout()
        button_layout.addLayout(zoomIn_layout)
        button_layout.addLayout(zoomOut_layout)
        button_layout.addLayout(explorer_layout)
        button_layout.addLayout(apply_layout)
        button_layout.addLayout(pdf_layout)
        button_layout.addLayout(exit_layout)

        button_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(button_layout)

    def zoom_in(self):
        self.zoom_in_signal.emit()

    def zoom_out(self):
        self.zoom_out_signal.emit()

    def show_fileExplorer(self):
        self.show_explorer_signal.emit()

    def show_pdf_converter(self):
        #self.show_pdf_converter_signal.emit()
        self.wip_message_signal.emit()

    def apply_cut(self):
        self.cut_signal.emit()


# noinspection PyPep8,PyUnresolvedReferences
class ConversionControls(QWidget):
    zoom_in_signal = pyqtSignal()
    zoom_out_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Add any specific control buttons or widgets for PNG to PDF conversion
        self.convert_button = QPushButton('Convert to PDF', self)
        self.convert_button.clicked.connect(self.parent().convert_to_pdf)

        layout = QVBoxLayout(self)
        layout.addWidget(self.convert_button)


# noinspection PyUnresolvedReferences
class MainBar(QMainWindow):
    show_explorer_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        main_bar = self.menuBar()
        file_menu = main_bar.addMenu('File')
        conf_menu = main_bar.addMenu('Configurations')
        help_menu = main_bar.addMenu('Help')

        open_action = QAction('File Explorer(Open)', self)
        open_action.triggered.connect(self.show_fileExplorer)
        file_menu.addAction(open_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_action)

        info_action = QAction('About ImgCutter', self)
        info_action.triggered.connect(self.show_info_dialog)
        help_menu.addAction(info_action)

        license_action = QAction('License terms', self)
        license_action.triggered.connect(self.license_win)
        help_menu.addAction(license_action)

        default_path = QAction('Paths', self)
        default_path.triggered.connect(self.show_confPath)
        conf_menu.addAction(default_path)

        

    def wip_message(self):
        info_msg = QMessageBox()
        info_msg.setIcon(QMessageBox.Information)
        info_msg.setText("Actually I'm working on this function, wait until the next update.")
        info_msg.setWindowTitle("Img AutoCutter - Work in Progress.")
        info_msg.exec_()

    def show_fileExplorer(self):
        self.show_explorer_signal.emit()

    def show_confPath(self):
        self.wip_message()
    
    def show_info_dialog(self):
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle('Info')

        icon_label = QLabel(info_dialog)
        pixmap = QPixmap('icons/icon.png')
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        info_label = QLabel('''
                            "Img AutoCutter" is a PyQt5 tool for easy image cutting and extraction. 
                            It allows users to open images, perform customizable cuts,and explore files.
                            The user-friendly interface includes zoom options and essential file actions.
                            Cut parts are saved as separate PNG files, 
                            making it a simple tool for basic image manipulation.
                            ''')

        info_label.setAlignment(Qt.AlignCenter)

        # Create a layout for the information dialog
        info_dialog_layout = QHBoxLayout()
        info_dialog_layout.addWidget(icon_label)
        info_dialog_layout.addWidget(info_label)

        info_dialog.setLayout(info_dialog_layout)
        info_dialog.exec_()
    
    def license_win(self):
        pass

    
