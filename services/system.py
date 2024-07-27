import psutil

def cpu_info():
    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    