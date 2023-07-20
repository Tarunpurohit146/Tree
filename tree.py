#!/usr/bin/python3
import datetime
import os
import argparse
import shutil
import time
import sys
class tree:
    def __init__(self):
        self.ssize=int(shutil.get_terminal_size().columns)
        self.dir=self.file=0
        self.time_start=self.time_end=0
        self.find_file=self.find_dirt=self.flag=1
    def content(self,absolut):
        if os.path.isdir(absolut):
            self.dir+=1               
        else:
            self.file+=1
    def basic_structure(self,dirt,file=None,directory=None):
        try:
            self.time_start=time.time_ns()
            print(f"{dirt}\n".center(int(self.ssize)-5))
            for i in sorted(os.listdir(dirt)): 
                if os.path.isdir(os.path.join(dirt,i)):
                    self.dir+=1
                    print(f"\033[0;36m{os.path.getsize(os.path.join(dirt,i))}bytes \033[0;37m📂{i}__|".rjust(int(self.ssize/2)+11))
                    if directory==i:
                        print('\033[0;33m\nDirectory Found')
                        self.flag=0
                        break
                else:
                    self.file+=1
                    print("|__".rjust(int(self.ssize/2))+f"\033[0;37m{i} \033[0;36m{os.path.getsize(os.path.join(dirt,i))}bytes\033[0;37m")
                    if file == i:
                        print('\033[0;33m\nFile Found')
                        self.flag=0
                        break          
        except FileNotFoundError:
            print("\033[0;31mFile not found!")
    def adance_structure(self,dirt,prf=""):
        try:
            dir_list1=sorted([i for i in os.listdir(dirt)])
            for i in range(len(dir_list1)):
                abst=os.path.join(dirt,dir_list1[i])
                self.content(abst)
                if i == len(dir_list1)-1:
                    if os.path.isdir(abst):
                        print(f"{prf}└──{dir_list1[i]}📂 \033[0;33m{os.path.getsize(abst)}bytes\033[0;37m")
                        if self.find_dirt == dir_list1[i]:
                            print('\033[0;33m\ndirctory found')
                            self.basic_structure(abst)
                            self.find_file=self.find_dirt=0
                            break
                        self.adance_structure(abst,prf + "      ")
                    else:
                        print(f'{prf}└──{dir_list1[i]} \033[0;36m{os.path.getsize(abst)}bytes\033[0;37m')
                        if self.find_file == dir_list1[i]:
                            print('\033[0;33m\nfile found')
                            self.find_file=self.find_dirt=0
                            exit()
                        continue
                else:    
                    if os.path.isdir(abst):
                        print(f"{prf}└──{dir_list1[i]}📂 \033[0;33m{os.path.getsize(abst)}bytes\033[0;37m")
                        if self.find_dirt == dir_list1[i]:
                            print('\033[0;33m\ndirctory found')
                            self.basic_structure(abst)
                            self.find_file=self.find_dirt=0
                            break
                        self.adance_structure(abst,prf+"|    ")
                    else:
                        print(f'{prf}├──{dir_list1[i]} \033[0;36m{os.path.getsize(abst)}bytes\033[0;37m')
                        if self.find_file == dir_list1[i]:
                            print('\033[0;33m\nfile found')
                            self.find_file=self.find_dirt=0
                            exit()
                        continue
        except FileNotFoundError:
            print("\033[0;33mFile not found!")
    def extention(self,dirt_name):
        try:
            ext=[]
            for i in os.listdir(dirt_name):
                val=i.split('.')
                if os.path.isfile(dirt_name+"/"+i) and val[0] != "" and len(val)>1:
                    ext.append(val[-1])
            e=sorted(set(ext))
            for i in e:
                print("\033[4;36m"+i+"\033[0m")
                for j in os.listdir(dirt_name):
                    if j.split('.')[-1] == i and len(j.split('.'))>1:
                        print(f"\033[0;32m  ─── {j} \033[0;36m{os.path.getsize(os.path.join(dirt_name,j))}bytes\033[0;37m")
        except FileNotFoundError:
            print("\033[0;31mFile not found!")
    def meta(self,file_name,out_file=None):
        try:
            fname=f"File Name : {file_name}"
            meta=os.stat(file_name)
            fsize=f"File size : {meta.st_size}"
            gid=f"Group Id : {meta.st_gid}"
            uid=f"User Id : {meta.st_uid}"
            fpermission=f"File Permission : {oct(meta.st_mode)[-3:]}"
            laccessfile=f"last access time : {datetime.datetime.fromtimestamp(meta.st_atime)}"
            lmodifyfile=f"last modify time : {datetime.datetime.fromtimestamp(meta.st_mtime)}"
            if out_file!=None:
                with open(out_file,"a") as f:
                    f.write(f"{fname}\n{fsize}\n{gid}\n{uid}\n{fpermission}\n{laccessfile}\n{lmodifyfile}\n\n\n")
                print(f"\n{fname}\n{fsize}\n{gid}\n{uid}\n{fpermission}\n{laccessfile}\n{lmodifyfile}\n\n")
            else:
                print(f"\n{fname}\n{fsize}\n{gid}\n{uid}\n{fpermission}\n{laccessfile}\n{lmodifyfile}\n\n")
        except FileNotFoundError:
            print("\033[0;32m File not found!")
    def __del__(self):
        if self.dir:
            print(f"\033[0;32m\nTotal directrys:{self.dir}\nTotal files:{self.file}\nTime taken:{self.time_end-self.time_start}ns\n")
if __name__=="__main__":
    parse=argparse.ArgumentParser() 
    parse.add_argument("-b","--basic",metavar="directry_name",help="show's basic structure of the directory")
    parse.add_argument("-a","--advance",metavar="directry_name",help="show's addir_list1ance structure of the directory")
    parse.add_argument("-f","--file",metavar="file_name",help="find the file in the directory")
    parse.add_argument("-d","--directory",metavar="directory_name",help="find subdirectory in the directory")
    parse.add_argument("-e",metavar="directory_name",help="Segregate file based on Extension")
    parse.add_argument("-m",metavar="file_name",help="Shows metadata of the file")
    parse.add_argument("-o",metavar="file_name",help="Use the option with -e to save the meta information in a file")  
    arg=parse.parse_args()  
    tr=tree()
    if arg.o and (arg.basic or arg.advance or arg.file or arg.e or arg.directory):
        print('should use -o option with -m')
        exit()
    if arg.e and (arg.basic or arg.advance or arg.file or arg.directory or arg.m):
        print("option -e should not be used with any option")
        exit()
    elif arg.basic or arg.basic and arg.file or arg.basic and arg.directory:    
        tr.basic_structure(arg.basic,arg.file,arg.directory)
        tr.time_end=time.time_ns()
        if tr.flag == 1 and (arg.file or arg.directory):
            print('\033[0;33m\nnot found!')
    elif arg.m and (arg.basic or arg.advance or arg.file or arg.directory or arg.e):
        print("option -m can be used alone or can be used with option -o")
    elif arg.file and len(sys.argv) <= 3:
        print("should use -f option with -b or -a")
    elif arg.directory and len(sys.argv) <= 3:
        print("should use -d option with -b or -a")
    elif arg.advance:
        tr.time_start=time.time_ns()
        tr.find_file=arg.file
        tr.find_dirt=arg.directory
        print(arg.advance+'\n|')
        tr.adance_structure(arg.advance)
        tr.time_end=time.time_ns()
        if tr.find_dirt != 0 and arg.directory or tr.find_file !=0 and arg.file:
            print('\033[0;33m\nnot found!')
    elif arg.e:
        tr.extention(arg.e)
    elif arg.m and arg.o:
        tr.meta(arg.m,arg.o)
    elif arg.m:
        tr.meta(arg.m)
    elif arg.o:
        print('should use -o option with -m')
