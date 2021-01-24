import os


def list_txt(txtfile:str,alist:list):
        filetxt=open(txtfile,'w',encoding='utf-8')
        for f in alist:
                filetxt.write(f)
                filetxt.write('\n')
        filetxt.close()

def txt_list(txtfile,listname):
        with open(txtfile, 'r',encoding='utf-8') as fd:
            for line in fd.readlines():
                #去掉txt里的‘nan’
                if not line.strip()=='nan':
                    lin=line.strip()
                    listname.append(lin)
            return listname
def clear_txt(txtname):
        f=open(txtname, 'w+')
        f.truncate()