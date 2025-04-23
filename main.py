import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QSplitter, QTextEdit,
    QAction, QFileDialog, QGraphicsView, QGraphicsScene, QPushButton, QColorDialog,
    QVBoxLayout, QWidget, QLabel, QListWidget, QTabWidget, QToolBar, QLineEdit
)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QIcon
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF

class PDFViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.page_images = []
        self.current_page = 0

    def load_pdf(self, file_path):
        self.scene.clear()
        self.page_images = []
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.page_images.append(pixmap)
        self.show_page(0)

    def show_page(self, page_num):
        if 0 <= page_num < len(self.page_images):
            self.current_page = page_num
            self.scene.clear()
            self.scene.addPixmap(self.page_images[page_num])

    def next_page(self):
        if self.current_page + 1 < len(self.page_images):
            self.show_page(self.current_page + 1)

    def prev_page(self):
        if self.current_page - 1 >= 0:
            self.show_page(self.current_page - 1)


class ModernReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QHBoxLayout(self.main_widget)

        # Sidebar for organizing documents
        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderHidden(True)
        self.sidebar.setColumnCount(2)
        self.sidebar.setStyleSheet("""
            QTreeWidget {
                background-color: #f0f0f0;
                font-size: 14px;
            }
            QTreeWidget::item {
                padding: 10px;
            }
            QTreeWidget::item:selected {
                background-color: #e0e0e0;
            }
        """)
        self.sidebar.itemClicked.connect(self.on_item_clicked)

        # Add sample data to the sidebar
        root = QTreeWidgetItem(self.sidebar)
        root.setText(0, "Library")
        recent_folder = QTreeWidgetItem(root)
        recent_folder.setText(0, "Recent")
        book_folder = QTreeWidgetItem(root)
        book_folder.setText(0, "Books")
        research_folder = QTreeWidgetItem(root)
        research_folder.setText(0, "Research Papers")

        self.layout.addWidget(self.sidebar)

        # Splitter for main area
        splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(splitter)

        # Main area for document content
        self.pdf_viewer = PDFViewer()
        splitter.addWidget(self.pdf_viewer)

        # Right sidebar for highlights and notes
        self.right_sidebar = QTabWidget()
        self.right_sidebar.setStyleSheet("""
            QTabWidget::pane {
                border-top: 2px solid #ccc;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                padding: 10px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background-color: #e0e0e0;
            }
        """)
        self.highlights_tab = QListWidget()
        self.highlights_tab.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
            }
        """)
        self.right_sidebar.addTab(self.highlights_tab, "Highlights & Notes")
        splitter.addWidget(self.right_sidebar)

        # Toolbar for actions
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #333;
                spacing: 5px;
            }
            QToolButton {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #555;
            }
        """)
        open_action = QAction(QIcon("icons/open.png"), "Open", self)
        open_action.triggered.connect(self.open_document)
        highlight_action = QAction(QIcon("icons/highlight.png"), "Highlight", self)
        highlight_action.triggered.connect(self.highlight_text)
        settings_action = QAction(QIcon("icons/settings.png"), "Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.toolbar.addAction(open_action)
        self.toolbar.addAction(highlight_action)
        self.toolbar.addAction(settings_action)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Window settings
        self.setWindowTitle("Modern Reader")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
        """)

    def open_document(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Document", "", "EPUB/PDF Files (*.epub *.pdf);;All Files (*)", options=options
        )
        if file_path:
            if file_path.endswith(".pdf"):
                self.pdf_viewer.load_pdf(file_path)
            elif file_path.endswith(".epub"):
                print("Loading EPUB...")
                # TODO: Implement EPUB loading logic here

    def highlight_text(self):
        color = QColorDialog.getColor(Qt.yellow, self, "Choose Highlight Color")
        if color.isValid():
            print(f"Highlighting text with color: {color.name()}")
            # TODO: Implement actual text highlighting logic here

    def open_settings(self):
        print("Opening settings...")
        # TODO: Implement settings dialog


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = ModernReader()
    reader.show()
    sys.exit(app.exec_())