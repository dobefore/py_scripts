from os import path
from PyQt5.QtWidgets import (QPushButton,
QGridLayout,QWidget,QFileDialog,QLabel,QLineEdit,
QTextEdit)
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from PyQt5.QtGui import QPalette,QColor
import threading,os,shutil,time
from PIL import Image
from file_oprate import txt_list,list_txt,clear_txt

class ResizePicWindow(QWidget):
    valueChanged = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ResizePicWindow, self).__init__(parent)
        self.resize(700,500)
        #创建窗口标题
        self.setWindowTitle('调整图片尺寸')

        self.dir_path_list=[]
        self.lineedit_output_list=[]
        self.txt_dir_path=r'txt_file\dir_path.txt'
        self.txt_dst_path=r'txt_file\dir__dst_path.txt'
        self.txt_size_point_path=r'txt_file\size_point.txt'
        # create widgets

         # create Label 
        self.label_dir=QLabel('<h3><font color=red>请选择文件夹</h3>') 
        self.label_target_size_show=QLabel('<h3><font color=red>请输入目标尺寸</h3>') 
        #create lineedit for input replace str
        self.lineedit_target_size=QLineEdit()
        self.lineedit_target_size.setText('尺寸（700,500）')
         #   Add lineedit signal to input_
        self.lineedit_target_size.textChanged.connect(self.return_target_size)
        
        self.valueChanged.connect(self.on_value_changed)

        # create textedit for print process output
        self.textedit_output_print=QTextEdit()
        self.textedit_output_print.setPlainText('waiting for process to run...')
        #  create button
        self.button_choose_dir = QPushButton()
        self.button_target_size_confirm = QPushButton()
        self.button_trigger_run = QPushButton()
        self.button_open_dst_folder = QPushButton()
         # add button attributes
        self.button_choose_dir.setText("选择源文件夹")
        self.button_choose_dir.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
        self.button_target_size_confirm.setText("确认添加目标尺寸")
        self.button_target_size_confirm.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
        self.button_trigger_run.setText("开始运行")
        self.button_trigger_run.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")

        self.button_open_dst_folder.setText("打开目标文件夹")
        self.button_open_dst_folder.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        # add button click events
        self.button_choose_dir.clicked.connect(self.choose_display_dir)
        self.button_target_size_confirm.clicked.connect(self.target_size_show_label)
        self.button_trigger_run.clicked.connect(self.on_clicked)
        self.button_open_dst_folder.clicked.connect(self.open_dst_file)
        
         # Create layout and add widgets to layout
        layout = QGridLayout()

         #布局内标签初始坐标设置（标签，格子0行，格子0列）默认标签大小显示
        layout.addWidget(self.label_dir,0,0)
        layout.addWidget(self.button_choose_dir,0,1)
        layout.addWidget(self.lineedit_target_size,1,0)
        layout.addWidget(self.button_target_size_confirm,1,1)
        layout.addWidget(self.label_target_size_show,2,0,1,2)
        layout.addWidget(self.button_trigger_run,3,0)
        layout.addWidget(self.button_open_dst_folder,3,1)
        layout.addWidget(self.textedit_output_print,4,0,1,2)

        # Set widget layout
        self.setLayout(layout)
    
    @pyqtSlot()
    def on_clicked(self):
        t1=threading.Thread(target=self.run,daemon=True)
        t1.start()
    @pyqtSlot(str)
    def on_value_changed(self,value:str):
        self.textedit_output_print.append(value)

    def resize_info(self,src_path:str,dst_path:str,size_point:str):
        """
        cp to a new dir and resize pic 
        """
        image_formats=['.jpg','.png','.jpeg']
        file_list=[i for i in os.listdir(src_path) if os.path.isfile(os.path.join(src_path,i)) and os.path.splitext(i)[-1] in image_formats]
        # convert size point str to tuple int point
        split_size_str=size_point.split(',')
        size_point_tuple=tuple((int(split_size_str[0]),int(split_size_str[1])))
        total_file_num=len(file_list)
        self.valueChanged.emit(f"""
chosen dir is {src_path}
dst dir is {dst_path}
found files: {total_file_num}  
""")

        # cp and resize pic
        for fn in file_list:
            
            src_file_path=os.path.join(src_path,fn)
            dst_file_path=os.path.join(dst_path,fn)
            shutil.copy(src_file_path,dst_file_path)
            self.valueChanged.emit(f'copy file  {fn} to {dst_path}')
        time.sleep(0.02)
        for fn in file_list:
            dst_file_path=os.path.join(dst_path,fn)
            im = Image.open(dst_file_path)
            im_size=im.size
            self.valueChanged.emit(f"""
size of pic {fn} is  {im_size}
resize pic {fn}...
""")
            im_resized=im.resize(size_point_tuple,Image.ANTIALIAS)
            im_resized.save(dst_file_path)

    def iscorrect_size_point(self,size_point:str):
        """
        size_point: '123,' or '100,200'
        return true if point like this 100,200
        """
        split_point=size_point.split(',')
        True_false=[]
        for i in split_point:
            try:
                int(i)
            except ValueError:
                True_false.append(False)
            True_false.append(True)
        return all(True_false)
    def run(self):

        # get src_dir from txt 
        src_dirl=[]
        txt_list(self.txt_dir_path,src_dirl)
        # get replaced_str from txt
        tempt_size_point_li=[]
        txt_list(self.txt_size_point_path,tempt_size_point_li)
        # check if src  path or str_repl_li  
        # is empty
        if src_dirl==['']:
            src_dirl.pop(0) 
        if tempt_size_point_li==['']:
            tempt_size_point_li.pop(0)   

        if src_dirl !=[] and tempt_size_point_li  !=[]:
            # set button bgcr to red when task running
            time.sleep(0.01)
            self.button_trigger_run.setText("running...")
            self.button_trigger_run.setStyleSheet("QPushButton{background: red;}")
            # not empty
            # get dst and src path 
            src_dir=src_dirl[-1] 
             # mk dst dir 
            dst_dirl=[]
            src_root_dir=os.path.dirname(src_dir)
            dst_path=src_root_dir+'/resized_img'
            dst_dirl.append(dst_path)
            try:
                os.makedirs(dst_path)
            except FileExistsError:
                shutil.rmtree(dst_path)
                os.makedirs(dst_path)
            list_txt(self.txt_dst_path,dst_dirl)
            # read str_repl from list
            size_point=tempt_size_point_li[-1]
            self.resize_info(src_dir,dst_path,size_point)
            # clear contents
            src_dirl.clear() 
            time.sleep(0.01)
            # set button bgcr to green when task done
            self.button_trigger_run.setText("job done!!!")
            self.button_trigger_run.setStyleSheet('QPushButton{background: green;}')
            # set button bgcr to green that means
            # dst_file_foleder can be opened
            self.button_open_dst_folder.setText("已准备好，打开目标文件夹")
            self.button_open_dst_folder.setStyleSheet("QPushButton{background: green;}")
            
        else:
            # empty
            self.valueChanged.emit('dir_path or size_point_path  not found!!!')
            self.button_trigger_run.setText("未准备好，不能运行")
            self.button_trigger_run.setStyleSheet("QPushButton{background: red;}")
        
             

    def target_size_show_label(self):
        """
        display last lineedit input in label
        after button being clicked
        """
        if self.lineedit_output_list!=[]:
            last_lineedit_output=self.lineedit_output_list[-1]
            # write str-repl to txt
            temp_size_point_li=[]
            temp_size_point_li.append(last_lineedit_output)
            
            if ',' in last_lineedit_output:
                split_str=last_lineedit_output.split(',')
                w=split_str[0]
                h=split_str[-1]
                if self.iscorrect_size_point(last_lineedit_output):
                    list_txt(self.txt_size_point_path,temp_size_point_li)
                    self.label_target_size_show.setText('<h3><font color=green>目标尺寸：'+w+':'+h+'</h3>')
                else:
                    self.label_target_size_show.setText('<h3><font color=red>invalid format</h3>')
            else:
                self.label_target_size_show.setText('<h3><font color=red>invalid format</h3>')

        else:
            self.label_target_size_show.setText('<h3><font color=red>未输入目标尺寸</h3>')
    def open_dst_file(self):
        """
        open dst folder from txt_file_path
        after fn fun was run
        """
        dst_path=[]
        if os.path.exists(self.txt_dst_path):
            txt_list(self.txt_dst_path,dst_path)
            if dst_path !=[] and dst_path!=['']:
                dst_path_str=dst_path[-1]
                path = os.path.realpath(dst_path_str)
                os.startfile(path)
            else:
                self.button_open_dst_folder.setText("未准备好，不能打开目标文件夹")
                self.button_open_dst_folder.setStyleSheet("QPushButton{background: red}")
        else:
            self.button_open_dst_folder.setText("未准备好，不能打开目标文件夹")
            self.button_open_dst_folder.setStyleSheet("QPushButton{background: red}")
    def choose_display_dir(self):
        """
        choose src_dir
        mk dst dir
        display dir path in label
        """
        # get abs path dir by selete dir
        directory = QFileDialog.getExistingDirectory()
        self.dir_path_list.append(directory)
        last_dir_from_list=self.dir_path_list[-1]
        #put dir_path to txt file
        temp_list=[]
        temp_list.append(last_dir_from_list)
        if last_dir_from_list !='':
            self.label_dir.setText('<h3><font color=green>'+last_dir_from_list+'</h3>')
            list_txt(self.txt_dir_path,temp_list)

        else:
            # this is applied to that cancel from choose dir
            self.label_dir.setText('<h3><font color=red>请选择文件夹</h3>')
        self.dir_path_list.clear()
    def return_target_size(self,text):
        """
        return str_repl_list after lineedit input
        """
        self.lineedit_output_list.append(text)
    def main(self):
        clear_txt(self.txt_dir_path)
        clear_txt(self.txt_dst_path)
        clear_txt(self.txt_size_point_path)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('#a8c971'))
        self.setPalette(palette) 
        self.show()