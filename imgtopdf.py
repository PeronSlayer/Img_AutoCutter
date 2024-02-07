from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, QApplication, QFileDialog
from shared import ConversionControls
# import fitz

#NOT WORKING, TO-DO

# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
class ConvertPNGtoPDFApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.conversion_controls = None
        self.png_folder_path = None
        self.init_ui()

    def init_ui(self):
        pdf_bar = self.menuBar()
        file_menu = pdf_bar.addMenu('File')

        open_action = QAction('Select PNG Folder', self)
        open_action.triggered.connect(self.show_folder_selector)
        file_menu.addAction(open_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_action)

        self.setWindowTitle('PNG to PDF Converter')
        # self.setFixedSize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Add any additional widgets or settings needed for PNG to PDF conversion
        self.conversion_controls = ConversionControls(self)
        layout.addWidget(self.conversion_controls)

    def move_center(self):
        # Move the window to the center of the screen
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def show_folder_selector(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, 'Select PNG Folder')
        if folder_dialog:
            self.png_folder_path = folder_dialog
            print(f'Selected folder: {self.png_folder_path}')

    def convert_to_pdf(self):
        if self.png_folder_path:
            # Implement PNG to PDF conversion logic using the selected folder
            print(f'Converting PNGs in folder: {self.png_folder_path} to PDF')
        else:
            print('Please select a PNG folder first.')
