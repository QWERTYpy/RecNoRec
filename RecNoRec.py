"""
Скрипт проверяет запись с камер в Beward Record Center
"""
import os
os.system("") #Костыль для вывода цвета
import datetime
now_date = datetime.datetime.today().strftime("%Y-%m-%d")
#now_date = "2022-01-24"

def serv_mount(upath,ipcam,name=None,pwd=None):
    """
    Функция, которая монтирует сетевую папку в виде диска, и работает в нем
    """
    if name == None:
        if os.system('net use h: "'+upath+'"') == 0:
            print("\033[32m"+upath+" - Подключен \033[37m")
    else:
        if os.system('net use h: "'+upath+'" /USER:'+name+" "+pwd) == 0:
            print("\033[32m"+upath+" - Подключен \033[37m")
    os.chdir("H:/")
    if os.path.exists(now_date):
        print("\033[32m   Актуальный каталог "+now_date+" - Существует \033[37m")
        find_cam("H:",ipcam)
    else:
        print("\033[31m   Актуальный каталог "+now_date+" - Отсутствует \033[37m") 

    
    os.chdir("C:/")
    os.system("net use h: /delete")

def find_cam(upath,ipcam_str):
    """
    Функиця поиска присутсвует ли запись по камерам
    """
    spis_cam=[]
    for dir_cam in os.listdir(path=upath+'\\'+now_date):
        if '(' in dir_cam[10:13]:
            if '(' in dir_cam[10:12]:
                spis_cam.append(int(dir_cam[10:11]))
            else:
                spis_cam.append(int(dir_cam[10:12]))
        else:
            spis_cam.append(int(dir_cam[10:13]))
    ipcam = list(ipcam_str.split(','))
    for cam in ipcam:
        if int(cam) in spis_cam: 
            print("\033[32m  "+str(cam)+" \033[37m", end=" ")
        else:
            print("\033[31m  "+str(cam)+" \033[37m", end=" ")

def serv_path(upath,ipcam):
    """
    Функия работает с расшаренными сетевыми папками
    """
    try:
        if now_date in os.listdir(path=upath):
            print("\033[32m"+upath+" - Подключен \033[37m\n\033[32m  Актуальный каталог "+now_date+" - Существует \033[37m")
            find_cam(upath,ipcam)
        else:
            print("\033[32m"+upath+" - Подключен \033[37m\n\033[31m   Актуальный каталог "+now_date+" - Отсутствует \033[37m")
    except:
       print("\033[31m"+upath+" - Подключение отсутсвует \033[37m")
    print('\n')
    
print ('Добро пожаловать. Идет анализ системы ...\n'+'='*50)

def serv(line_spl):
    if line_spl[3].strip() == "0":
        serv_path(line_spl[0],line_spl[1])
    else:
        serv_mount(line_spl[0],line_spl[1],line_spl[2],line_spl[3])
        
file_ip = open('ip.conf','r')
for line in file_ip:
    line_spl = line.split(';')
    serv(line_spl)
file_ip.close()
input ('\n\nДля завершения нажмите ввод')


