import sys
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF

#NOT WORKING, TO-DO

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Viewer with OCR")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set a layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a QLabel to display PDF pages
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Create a QLabel to display OCR text
        self.ocr_label = QLabel(self)
        layout.addWidget(self.ocr_label)

        # Create navigation buttons
        self.prev_button = QPushButton("Previous Page", self)
        self.prev_button.clicked.connect(self.show_previous_page)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next Page", self)
        self.next_button.clicked.connect(self.show_next_page)
        layout.addWidget(self.next_button)

        # Initialize page index
        self.current_page = 0

        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # Create an "Open PDF" action
        open_action = file_menu.addAction("Open PDF")
        open_action.triggered.connect(self.open_pdf)

    def open_pdf(self):
        # Open a file dialog to choose a PDF file
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.load_pdf(file_path)

    def load_pdf(self, file_path):
        # Load the PDF file and display the first page as an image
        self.pdf_document = fitz.open(file_path)
        self.show_page()

    def show_page(self):
        # Display the current page as an image
        page = self.pdf_document[self.current_page]
        image = page.get_pixmap()

        # Convert PyMuPDF image to QImage
        qimage = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)

        # Set the QImage to QLabel
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        # Perform OCR on the current page
        ocr_text = self.perform_ocr(image)
        
        # Display OCR text in the GUI
        self.ocr_label.setText("OCR Text:\n" + ocr_text)
        self.ocr_label.setAlignment(Qt.AlignLeft)

    def perform_ocr(self, image):
        # Perform OCR using pytesseract
        image.save("temp.png")  # Save the image temporarily
        ocr_text = pytesseract.image_to_string("temp.png")
        return ocr_text

    def show_previous_page(self):
        # Show the previous page
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def show_next_page(self):
        # Show the next page
        if self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.show_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
