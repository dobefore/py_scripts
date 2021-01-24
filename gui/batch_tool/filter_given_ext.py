from PyQt5.QtWidgets import (QPushButton,
QGridLayout,QWidget,QFileDialog,QLabel,QLineEdit,
QTextEdit)
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from PyQt5.QtGui import QPalette,QColor
import os,shutil
import threading
from collections import Counter

class FilterExtWindow(QWidget):
    valueChanged = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__()
        self.resize(700,500)
        #创建窗口标题
        self.setWindowTitle('筛选特定格式文件')

        self.dir_path_list=[]
        self.lineedit_output_list=[]
        self.check_mk_txtdir()
        self.txt_dir_path=r'txt_file\dir_path.txt'
        self.txt_ext_path=r'txt_file\ext.txt'
        self.txt_dst_dir_path=r'txt_file\dst_path.txt'
        
        # create widgets

         # create button for 
         # add ext to label below,seleting dir,
         #  triggering filtering_ext to run 
        self.button_ext_add = QPushButton()
        self.button_choose_dir = QPushButton()
        self.button_invoke_run = QPushButton()
        self.button_open_dst_dir = QPushButton()
        # add button attributes
        self.button_choose_dir.setText("选择源文件夹")
        self.button_choose_dir.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
         
        self.button_ext_add.setText("确认添加后缀")
        self.button_ext_add.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
        self.button_invoke_run.setText("开始运行")
        self.button_invoke_run.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")

        self.button_open_dst_dir.setText("打开目标文件夹")
        self.button_open_dst_dir.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
         # create Label for display dir path,
         # display file extension
        self.label_dir=QLabel('<h3><font color=red>请选择文件夹</h3>') 
        self.label_ext_print=QLabel('<h3><font color=red>未输入文件后缀,请输入一个或多个文件后缀</h3>')
        
        #create lineedit for input ext
        self.lineedit_ext_add=QLineEdit()
        self.lineedit_ext_add.setText('例子：mobi 或 jpg;png')
        # create textedit for print process output
        self.textedit_output_print=QTextEdit()
        self.textedit_output_print.setPlainText('waiting for process to run...')

        # add button click events
         # Add button signal to  return_dir slot 
        self.button_choose_dir.clicked.connect(self.return_dir)
        self.button_ext_add.clicked.connect(self.print_ext_in_label)
        self.valueChanged.connect(self.on_value_changed)
        self.button_invoke_run.clicked.connect(self.on_clicked)
        self.button_open_dst_dir.clicked.connect(self.open_dst_file)
        #   Add lineedit signal to input_ext
        self.lineedit_ext_add.textChanged.connect(self.input_ext)
         
         # Create layout and add widgets to layout
        layout = QGridLayout()
        
         #布局内标签初始坐标设置（标签，格子0行，格子0列）默认标签大小显示
        layout.addWidget(self.label_dir,0,0)
        layout.addWidget(self.button_choose_dir,0,1)
        layout.addWidget(self.lineedit_ext_add,1,0)
        layout.addWidget(self.button_ext_add,1,1)
        layout.addWidget(self.label_ext_print,2,0,1,2)
         #文本框初始坐标设置（button，格子1行，格子0列，所占位置起始格子1，结束格子2）
        layout.addWidget(self.button_invoke_run,3,0)
        layout.addWidget(self.button_open_dst_dir,3,1)
        layout.addWidget(self.textedit_output_print,4,0,1,2)
        # Set widget layout
        self.setLayout(layout)
    def check_mk_txtdir(self):
        dirname='txt_file'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    def list_txt(self,txtfile,listname):
        filetxt=open(txtfile,'w',encoding='utf-8')
        for f in listname:
                filetxt.write(f)
                filetxt.write('\n')
        filetxt.close()
    def clear_txt(self,txt_path):
        """
        clear txt contents
        """
        f=open(txt_path,'w+',encoding='utf-8')
        f.truncate()
        f.close()

    def txt_list(self,txtfile,listname):
        with open(txtfile, 'r',encoding='utf-8') as fd:
            
            for line in fd.readlines():
                #去掉txt里的‘nan’
                if not line.strip()=='nan':
                    lin=line.strip()
                    listname.append(lin)
            return listname
    
    def input_ext(self,text):
        """ 
        ext input line:mobi;azw3
        """ 
        self.lineedit_output_list.append(text)
    def count_filtered_files_print(self,src_dir:str,dst_dir:str,extension_with_dot:list):
        """
        count files and print
        according to file extension cate
        """
        # create dst dir
       
        try:
            os.makedirs(dst_dir)
        except FileExistsError:
            pass
        ext_category=len(extension_with_dot)
        extension_with_dot_list=[]
        # use Counter()
        for _dirpath,_dirname,filelist in os.walk(src_dir):
            for afile in filelist:
                split_file_ext=os.path.splitext(afile)[-1]
                if split_file_ext in extension_with_dot:
                    extension_with_dot_list.append(split_file_ext)
        total_file_number=len(extension_with_dot_list)
        ext_cat_list=Counter(extension_with_dot_list).most_common(ext_category)
        ext_cat_str=""
        for (ext,num) in ext_cat_list:
            ext_cat_str+=ext+': '+str(num)+'\n'
        self.valueChanged.emit(f"""
        found files: {total_file_number} ,details as follows:
        {ext_cat_str}
        """)
                    
    def filter_ext_to_new_dir(self,src_dir:str,dst_dir:str,extension_with_dot:list):
        """
        match given file extension
        cp files to new dir
        """
        # create dst dir
       
        try:
            os.makedirs(dst_dir)
        except FileExistsError:
            pass
        for dirpath,_dirname,filelist in os.walk(src_dir):
            for afile in filelist:
                split_file_ext=os.path.splitext(afile)[-1]
                if split_file_ext in extension_with_dot:
                    try:
                        shutil.copy(os.path.join(dirpath,afile),os.path.join(dst_dir,afile))
                    except shutil.SameFileError:
                        continue
                    self.valueChanged.emit(f'copy {afile} to {os.path.join(dst_dir,afile)}')
        

    @pyqtSlot(str)
    def on_value_changed(self, value):
        self.textedit_output_print.append(f'{value}')
        
    @pyqtSlot()
    def on_clicked(self):
        
        t1=threading.Thread(target=self.run ,daemon=True)
        t1.start()
                

    def run(self):
        """
        run to filter given extension
        cp filtered files to new folder
        """
        # read chosen_dir_path and ext_str 
        # from txt files
        temp_dir_list=[]
        temp_ext_list=[]
        self.txt_list(self.txt_dir_path,temp_dir_list)
        self.txt_list(self.txt_ext_path,temp_ext_list)
        
        if temp_dir_list !=[] and temp_ext_list !=[]:
            # print dir and extensions
            self.valueChanged.emit('begin to run...')
            # set button bgcr to red when task running
            self.button_invoke_run.setText("running...")
            self.button_invoke_run.setStyleSheet("QPushButton{background: red}")

            dir_str=temp_dir_list[0]
            ext_str=temp_ext_list[0]
            self.valueChanged.emit(f"""
chosen dir is {dir_str}
input file extension(s) is(are) {ext_str}
""")

            # split ext_list: [mobi azw3] and add pre_dot
            ext_list=temp_ext_list[0].split(' ')
            ext_list_with_dot=['.'+i for i in ext_list]
            src_dir=temp_dir_list[0]
            # src and dst are in a same level
            dst_dir=os.path.join(os.path.dirname(src_dir),'filtered_dir')
            # write dst to txt
            dst_dir_list=[]
            dst_dir_list.append(dst_dir)
            self.list_txt(self.txt_dst_dir_path,dst_dir_list)
            
            self.count_filtered_files_print(src_dir,dst_dir,ext_list_with_dot)
            self.filter_ext_to_new_dir(src_dir,dst_dir,ext_list_with_dot)
            
            # set button bgcr to green when task done
            self.button_invoke_run.setText("job done!!!")
            self.button_invoke_run.setStyleSheet("QPushButton{background: green}")
            
             # set button bgcr to green that means
            # dst_file_foleder can be opened
            self.button_open_dst_dir.setText("已准备好，打开目标文件夹")
            self.button_open_dst_dir.setStyleSheet("QPushButton{background: green}")
        else:
            self.valueChanged.emit('dir_path or ext_str not found!!!')
            
            self.button_invoke_run.setText("未准备好，不能运行")
            self.button_invoke_run.setStyleSheet("QPushButton{background: red}")
        temp_ext_list.clear()
    def open_dst_file(self):
        """
        open dst folder from txt_file_path
        after fn fun was run
        """
        dst_path=[]
        if os.path.exists(self.txt_dst_dir_path):
            self.txt_list(self.txt_dst_dir_path,dst_path)
            if dst_path !=[]:
                dst_path_str=dst_path[-1]
                path = os.path.realpath(dst_path_str)
                os.startfile(path)
            else:
                self.button_open_dst_dir.setText("未准备好，不能打开目标文件夹")
                self.button_open_dst_dir.setStyleSheet("QPushButton{background: red}")
        else:
            self.button_open_dst_dir.setText("未准备好，不能打开目标文件夹")
            self.button_open_dst_dir.setStyleSheet("QPushButton{background: red}")
    def print_ext_in_label(self):
        if self.lineedit_output_list!=[]:
            last_lineedit_output=self.lineedit_output_list[-1]
            ext_label_str=''
            # split ext_str: jpg;png
            if last_lineedit_output!='':
                # put ext_str to txt
                temp_list=[]

                if ';' in last_lineedit_output:
                    split_last_lineedit_output=last_lineedit_output.split(';')
                    for ext in split_last_lineedit_output:
                        # [jpg,'']
                        if ext!='':
                            ext_label_str+=' '+ext
                    temp_list.append(ext_label_str)
                    self.label_ext_print.setText('<h3><font color=green>后缀格式：'+ext_label_str+'</h3>')
                else:
                    ext_label_str=last_lineedit_output
                    temp_list.append(ext_label_str)
                    self.label_ext_print.setText('<h3><font color=green>后缀格式：'+ext_label_str+'</h3>')
                # put ext_str to txt
                self.list_txt(self.txt_ext_path,temp_list)
        else:
            self.label_ext_print.setText('<h3><font color=red>未输入文件后缀，请输入一个或多个文件后缀</h3>')
            self.clear_txt(self.txt_ext_path)
        self.lineedit_output_list.clear()
    def return_dir(self):
        """
        choose dir
        display dir path in label
        """
        # get abs path dir by selete dir
        directory = QFileDialog.getExistingDirectory()
        # after button being clicked,
        # display dir path label
        self.dir_path_list.append(directory)
        last_dir_from_list=self.dir_path_list[-1]
        #put dir_path to txt file
        
        temp_list=[]
        temp_list.append(last_dir_from_list)
        self.list_txt(self.txt_dir_path,temp_list)

        if last_dir_from_list !='':
            self.label_dir.setText('<h3><font color=green>'+last_dir_from_list+'</h3>')
        else:
            # this is applied to that cancel from choose dir
            self.label_dir.setText('<h3><font color=red>请选择文件夹</h3>')
        self.dir_path_list.clear()
    def main(self):
        #clear contents of txts ext.txt dir_path.txt
        
        self.clear_txt(self.txt_dir_path)
        self.clear_txt(self.txt_ext_path)
        self.clear_txt(self.txt_dst_dir_path)
# set window bg cr
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(207, 165, 239))
        self.setPalette(palette) 

        self.show()
        