import yaml
import time
import sys
from pytube import YouTube
import os 
from console_progressbar import ProgressBar

#disctionary values

#function to log errors
def log(err):
    error_file = open("error_logs.txt" , "a")
    error_file.write("\n" + str(err))
    error_file.close()

#try reading the config file
try:
    with open("config.yml") as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        d_settings = yaml.load(file, Loader=yaml.FullLoader)
except Exception as err:
    log(err)
    print("An error occured while openning the config file")
    print("Chek the 'error_logs.txt' to see the error")
    print("Quitting in 5s")
    time.sleep(5)
    sys.exit()

#create an ordered settings array
settings = [d_settings["urls_path"], d_settings["name_path"], d_settings["save_dir"]]


#try reading the url file
try:
    url_file = open(settings[0])
    urls = url_file.readlines()
    
    #remove any empty spaces
    urls = [i for i in urls if i != "\n"]

    #remove any extra spaces
    urls = [x.strip() for x in urls]
    
except Exception as err:
    log(err)
    print("An error occured while reading the file contaning names")
    print("Chek the 'error_logs.txt' to see the error")
    print("Quitting in 5s")
    time.sleep(5)
    sys.exit()


#try reading the url file
try:
    name_file = open(settings[1])
    names = name_file.readlines()
    
    #remove any empty spaces
    names = [i for i in names if i != "\n"]

    #remove any extra spaces
    names = [x.strip() for x in names]
    
except Exception as err:
    log(err)
    print("An error occured while reading the file containing names")
    print("Chek the 'error_logs.txt' to see the error")
    print("Quitting in 5s")
    time.sleep(5)
    sys.exit()


#check if there are enough names for all urls
if len(urls) > len(names):
    diff = len(urls)-len(names)

    #if not enough names add some
    c = 1
    for i in range (diff):
        names.append("UnnamedSong_" + str(c))
        c = c + 1

n_to_download = len(urls)
downloaded = 0
errors = []

#save directory
save_dirictory = settings[2]
save_dirictory = os.path.join(save_dirictory, "YouTubeDw")

#progress bar
progress = ProgressBar(total=100 ,prefix='Downloading', suffix='Completed', decimals=2, length=50, fill='#', zfill='-')



#download all music
for i in urls:
    index = urls.index(i)
    try:
        audio = YouTube(i).streams.filter(only_audio=True).order_by('bitrate').desc().first()
        audio.download(save_dirictory, names[index])
    except Exception as err:
        log(err)
        errors.append(i)

    downloaded = downloaded + 1

    #update progress bar
    progress.print_progress_bar(round((downloaded/n_to_download)*100, 2))
    


#if any failed to download display which one failed
if len(errors) != 0:
    print("Couldn't download the folowing:")
    for i in errors:
        print(i)

    print("Check 'error_logs.txt' for more info")



