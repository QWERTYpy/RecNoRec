"""
Скрипт проверяет запись с камер в Beward Record Center
"""
import os
os.system("") #Костыль для вывода цвета
import datetime
import configparser


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
    print(upath)
    print(os.listdir(path="\\\\10.64.130.249\SkladTMC"))
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

def securos(config):
    dict_const = {'servers': [str_serv.strip() for str_serv in config["servers"]["servers"].split(',')]}
    for serv in dict_const['servers']:
        # print(serv)
        dict_const[serv] = [config[serv]["ip_serv"],
                            [str_fold.strip() for str_fold in config[serv]["ip_fold"].split(',')],
                            config[serv]["folder"], [str_ip.strip() for str_ip in config[serv]["ip_cam"].split(',')]]
        # print(os.listdir(path="\\\\10.64.130.249\SkladTMC"))
        try:
            dir_cam = os.listdir(f"\\\\{dict_const[serv][0]}\{dict_const[serv][1][0]}")
            print("\033[32m" + dict_const[serv][0] + " - Подключен \033[37m")
        except:
            print("\033[31m" + dict_const[serv][0] + " - Подключение отсутсвует \033[37m")
        date_cam = {}
        for ind in dict_const[serv][1]:
            dir_cam = os.listdir(f"\\\\{dict_const[serv][0]}\{ind}")
            for dir_cam_n in range(1, int(dict_const[serv][2]) + 1):
                if f"CAM_{dir_cam_n}" in dir_cam:
                    date_cam_dir = os.listdir(f"\\\\{dict_const[serv][0]}\{ind}\CAM_{dir_cam_n}")
                    if f"CAM_{dir_cam_n}" in date_cam:
                        date_cam[f"CAM_{dir_cam_n}"].append(date_cam_dir[len(date_cam_dir) - 1][:10])
                    else:
                        date_cam[f"CAM_{dir_cam_n}"] = [date_cam_dir[len(date_cam_dir) - 1][:10]]
                    # print(f"CAM_{dir_cam_n}","->",date_cam_dir[len(date_cam_dir)-1][:10],"->",now_date)
        for dir_cam_n in range(1, int(dict_const[serv][2]) + 1):
            if now_date in date_cam[f"CAM_{dir_cam_n}"]:
                print("\033[32m  " + dict_const[serv][3][dir_cam_n - 1] + " \033[37m", end=" ")
            else:
                print("\033[31m  " + dict_const[serv][3][dir_cam_n - 1] + " \033[37m", end=" ")

        print("")
# Инициализация основных переменных
config = configparser.ConfigParser()
config.read("securos.ini", encoding="utf-8")

file_ip = open('ip.conf','r')
for line in file_ip:
    line_spl = line.split(';')
    serv(line_spl)
file_ip.close()
securos(config)


print("Анализ серверов SecurOS:")

    # print(date_cam)

# dict_const['ping_device'] = int(config["ping_time"]["ping_device"])
# dict_const['time_out'] = int(config["ping_time"]["time_out"])
# print(dict_const)
# input ('\n\nДля завершения нажмите ввод')


