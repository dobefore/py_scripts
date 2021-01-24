import sys,os
from PyQt5.QtWidgets import ( QPushButton, QApplication,
    QHBoxLayout,QWidget)
from PyQt5.QtGui import QPalette,QColor
from filter_given_ext import FilterExtWindow
from rename_file import RenameFileWindow
from resize_pic import ResizePicWindow
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(650,350)
        self.check_mk_txtdir()
        #创建窗口标题
        self.setWindowTitle('批量文件操作工具箱')

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('#f2f2b0'))
        self.setPalette(palette) 
        
    def check_mk_txtdir(self):
        """
        mkdir txt_file if dir not exist
        """
        dirname='txt_file'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    def main(self):
        # Create widgets
        
        # create button for filtering given  
        # suffix_format files
        self.button_filter_ext = QPushButton()
        self.button_filter_ext.setText("筛选特定格式文件")
        self.button_filter_ext.setFixedSize(200,300)
        self.button_filter_ext.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
        #create button for rename files 
        self.button_rename_file = QPushButton()
        self.button_rename_file.setText("重命名文件")
        self.button_rename_file.setFixedSize(200,300)
        self.button_rename_file.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
         #create button for remove prefix_str 
         # of filename
        self.button_resize_pic = QPushButton()
        self.button_resize_pic.setText("调整图片尺寸、大小")
        self.button_resize_pic.setFixedSize(200,300)
        self.button_resize_pic.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")

        # Create layout and add widgets
        layout = QHBoxLayout()
       
        layout.addWidget(self.button_filter_ext)
        layout.addWidget(self.button_rename_file)
        layout.addWidget(self.button_resize_pic)
        # Set widget layout
        self.setLayout(layout)
        

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the mainwindow
    mainwindow = MainWindow()
    mainwindow.main()
    mainwindow.show()

    # create an instance of other windows
    filter_ext_window=FilterExtWindow()
    rename_file_window=RenameFileWindow()
    resize_pic_window=ResizePicWindow()
    # Add button signal to slot 
    mainwindow.button_filter_ext.clicked.connect(filter_ext_window.main)
    mainwindow.button_rename_file.clicked.connect(rename_file_window.main)
    mainwindow.button_resize_pic.clicked.connect(resize_pic_window.main)
    
    sys.exit(app.exec_())