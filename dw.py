import yaml
import time
import sys
from mypytube import YouTube
import os 
from console_progressbar import ProgressBar

#function to log errors
def log(err):
    error_file = open("error_logs.txt" , "a")
    error_file.write("\n" + str(err))
    error_file.close()


#converting seconds to hours and minutes
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%dh %02dm %02ds" % (hour, minutes, seconds) 

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
s_downloaded = 0
failed = 0

#save directory
save_dirictory = settings[2]
save_dirictory = os.path.join(save_dirictory, "YouTubeDw")

#progress bar
progress = ProgressBar(total=100 ,prefix='Downloading', suffix='Completed', decimals=2, length=50, fill='#', zfill='-')


t0 = time.time()

#download all music
for i in urls:
    index = urls.index(i)
    try:
        audio = YouTube(i).streams.filter(only_audio=True).order_by('bitrate').desc().first()
        audio.download(save_dirictory, names[index])
        s_downloaded = s_downloaded + 1
    except Exception as err:
        log(str(err) + " : " + str(i))
        errors.append(i)
        failed = failed + 1

    downloaded = downloaded + 1

    #update progress bar
    progress.print_progress_bar(round((downloaded/n_to_download)*100, 2))
    
t1 = time.time()
time_elapsed = t1 - t0
time_elapsed = round(time_elapsed, 0)
time_elapsed = convert(time_elapsed)


print("Downloaded " + str(s_downloaded) + " tracks")
print("Failed to download " + str(failed) + " tracks")
print("Total time: " + str(time_elapsed))
print("Take a look at 'download_report.txt' the stats")
print("Will quit in 10s")


report_msg = "Downloaded " + str(s_downloaded) + " tracks\n"
report_msg = report_msg + "Failed to download " + str(failed) + " tracks\n"
report_msg = report_msg + "Total time: " + str(time_elapsed) + "\n"
report_msg = report_msg + "Failed to download:\n"

if len(errors) != 0:
    for i in errors:
        report_msg = report_msg + str(i) + "\n"

else:
    report_msg = report_msg + "None"


report = open("download_report.txt", "w+")
report.write(report_msg)
report.close()
time.sleep(10)






