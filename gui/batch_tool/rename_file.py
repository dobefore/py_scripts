from os.path import isfile, split, splitext
from typing import Set
from PyQt5.QtWidgets import (QPushButton,
QGridLayout,QWidget,QFileDialog,QLabel,QLineEdit,
QTextEdit)
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from PyQt5.QtGui import QPalette,QColor
import threading,os
from file_oprate import txt_list,list_txt,clear_txt


class RenameFileWindow(QWidget):
    valueChanged = pyqtSignal(str)
    def __init__(self, parent=None):
        super(RenameFileWindow, self).__init__(parent)
        self.resize(700,500)
        #创建窗口标题
        self.setWindowTitle('重命名文件')
        
        self.dir_path_list=[]
        self.lineedit_output_list=[]
        self.txt_dir_path=r'txt_file\dir_path.txt'
        self.txt_str_repl_path=r'txt_file\str_repl.txt'
        # create widgets

         # create Label 
        self.label_dir=QLabel('<h3><font color=red>请选择文件夹</h3>') 
        self.label_str_replaced_show=QLabel('<h3><font color=red>请输入待替换的文本</h3>') 
        #create lineedit for input replace str
        self.lineedit_str_replaced=QLineEdit()
        self.lineedit_str_replaced.setText('局部替换（abc;123）全部替换（abc）')
         #   Add lineedit signal to input_
        self.lineedit_str_replaced.textChanged.connect(self.return_str_replaced)
        
        self.valueChanged.connect(self.on_value_changed)

        # create textedit for print process output
        self.textedit_output_print=QTextEdit()
        self.textedit_output_print.setPlainText('waiting for process to run...')
        #  create button
        self.button_choose_dir = QPushButton()
        self.button_str_replaced_confirm = QPushButton()
        self.button_trigger_run = QPushButton()
        self.button_open_dst_folder = QPushButton()
         # add button attributes
        self.button_choose_dir.setText("选择源文件夹")
        self.button_choose_dir.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
        self.button_str_replaced_confirm.setText("确认添加替换文本")
        self.button_str_replaced_confirm.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        
        self.button_trigger_run.setText("开始运行")
        self.button_trigger_run.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")

        self.button_open_dst_folder.setText("打开目标文件夹")
        self.button_open_dst_folder.setStyleSheet("QPushButton::hover{background : lightgreen;}\
            QPushButton{background: transparent}")
        # add button click events
        self.button_choose_dir.clicked.connect(self.choose_display_dir)
        self.button_str_replaced_confirm.clicked.connect(self.str_replaced_show_label)
        self.button_trigger_run.clicked.connect(self.on_clicked)
        self.button_open_dst_folder.clicked.connect(self.open_dst_file)
        
         # Create layout and add widgets to layout
        layout = QGridLayout()

         #布局内标签初始坐标设置（标签，格子0行，格子0列）默认标签大小显示
        layout.addWidget(self.label_dir,0,0)
        layout.addWidget(self.button_choose_dir,0,1)
        layout.addWidget(self.lineedit_str_replaced,1,0)
        layout.addWidget(self.button_str_replaced_confirm,1,1)
        layout.addWidget(self.label_str_replaced_show,2,0,1,2)
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
    def on_value_changed(self,value):
        self.textedit_output_print.append(value)
    def print_str_repl(self,str_repl:str):
        if ';' in str_repl:
            split_str=str_repl.split(';')
            return split_str[0]+'->'+split_str[-1]+' 局部替换'
        else:
            return str_repl+' 全部替换'
    def rename_info(self,src_path:str,repl_str:str):
        file_list=[i for i in os.listdir(src_path) if os.path.isfile(os.path.join(src_path,i))]
        # print file info 
        total_file_num=len(file_list)
        matched_file_list=[]
        if ';' in repl_str:
            src_str=repl_str.split(';')[0]
            matched_file_list=[i for i in file_list if src_str in i]
        else:
            matched_file_list=file_list
        non_matched_file_list=list(set(file_list)-set(matched_file_list))
        self.valueChanged.emit(f"""
chosen dir is {src_path}
replace_str is {self.print_str_repl(repl_str)}
found files: {total_file_num}
matched_file_number is {len(matched_file_list)}
non_matched_file_number is {len(non_matched_file_list)}        
""")

        # rename file
        n=0
        for fn in matched_file_list:
            n+=1 
            src_file_path=os.path.join(src_path,fn)
            dst_file_path=''
            new_file_name=''
            if ';' in repl_str:
                split_str_l=repl_str.split(';')
                src_str=split_str_l[0]
                dst_str=split_str_l[-1]
                new_file_name=fn.replace(src_str,dst_str)
                dst_file_path=os.path.join(src_path,new_file_name)
            else:
                file_suffix_ext=os.path.splitext(fn)[-1]
                file_prefix_str=repl_str+str(n)
                new_file_name=file_prefix_str+file_suffix_ext
                dst_file_path=os.path.join(src_path,new_file_name)
            os.rename(src_file_path,dst_file_path)
            self.valueChanged.emit(f'rename file from {fn} to {new_file_name}')

    def run(self):

        # get src_dir from txt 
        src_dirl=[]
        txt_list(self.txt_dir_path,src_dirl)
        # get replaced_str from txt
        tempt_str_repl_li=[]
        txt_list(self.txt_str_repl_path,tempt_str_repl_li)
        # check if src  path or str_repl_li  
        # is empty
        if src_dirl==['']:
            src_dirl.pop(0)
        if src_dirl and tempt_str_repl_li  !=[]:
            print(src_dirl)
            # set button bgcr to red when task running
            self.button_trigger_run.setText("running...")
            self.button_trigger_run.setStyleSheet("QPushButton{background: red}")
            # not empty
            # get dst and src path 
            src_dir=src_dirl[-1] 
            # read str_repl from list
            str_repl=tempt_str_repl_li[-1]
            self.rename_info(src_dir,str_repl)

            # set button bgcr to green when task done
            self.button_trigger_run.setText("job done!!!")
            self.button_trigger_run.setStyleSheet("QPushButton{background: green}")
            # set button bgcr to green that means
            # dst_file_foleder can be opened
            self.button_open_dst_folder.setText("已准备好，打开目标文件夹")
            self.button_open_dst_folder.setStyleSheet("QPushButton{background: green}")
            
        else:
            # empty
            self.valueChanged.emit('dir_path or str_repl  not found!!!')
            self.button_trigger_run.setText("未准备好，不能运行")
            self.button_trigger_run.setStyleSheet("QPushButton{background: red}")
        # clear contents
        src_dirl.clear()      

    def str_replaced_show_label(self):
        """
        display last lineedit input in label
        after button being clicked
        """
        if self.lineedit_output_list!=[]:
            last_lineedit_output=self.lineedit_output_list[-1]
            # write str-repl to txt
            temp_str_repl_li=[]
            temp_str_repl_li.append(last_lineedit_output)
            list_txt(self.txt_str_repl_path,temp_str_repl_li)
            if ';' in last_lineedit_output:
                split_str=last_lineedit_output.split(';')
                src_str=split_str[0]
                dst_str=split_str[-1]
                self.label_str_replaced_show.setText('<h3><font color=green>替换文本：'+src_str+'->'+dst_str+'</h3>')
            else:
                self.label_str_replaced_show.setText('<h3><font color=green>替换文本：'+last_lineedit_output+'</h3>')

        else:
            self.label_str_replaced_show.setText('<h3><font color=red>未输入替换文本</h3>')
    def open_dst_file(self):
        """
        open dst folder from txt_file_path
        after fn fun was run
        """
        dst_path=[]
        if os.path.exists(self.txt_dir_path):
            txt_list(self.txt_dir_path,dst_path)
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
        choose dir
        display dir path in label
        """
        # get abs path dir by selete dir
        directory = QFileDialog.getExistingDirectory()
        self.dir_path_list.append(directory)
        last_dir_from_list=self.dir_path_list[-1]
        #put dir_path to txt file
        temp_list=[]
        temp_list.append(last_dir_from_list)
        list_txt(self.txt_dir_path,temp_list)

        if last_dir_from_list !='':
            self.label_dir.setText('<h3><font color=green>'+last_dir_from_list+'</h3>')
        else:
            # this is applied to that cancel from choose dir
            self.label_dir.setText('<h3><font color=red>请选择文件夹</h3>')
        self.dir_path_list.clear()
    def return_str_replaced(self,text):
        """
        return str_repl_list after lineedit input
        """
        self.lineedit_output_list.append(text)

    def main(self):
        clear_txt(self.txt_str_repl_path)
        clear_txt(self.txt_dir_path)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('#a2eeeb'))
        self.setPalette(palette) 
        self.show()