#from django.shortcuts import render
from django.http import JsonResponse
import platform
import psutil
from cpuinfo import get_cpu_info
from subprocess import check_output
import datetime
import uptime

def default(request):
    return JsonResponse({"message": "Welcome to task manager api"})

def cpu_constants(request):
    processor = platform.processor()
    processor_qty = len(processor) if (isinstance(processor, list)) else 1
    physical_cores = psutil.cpu_count(logical=False)
    threads_qty = psutil.cpu_count(logical=True)
    (bits, linkage) = platform.architecture()
    base_speed = round(psutil.cpu_freq().max/1000, 3)
    l1_cache_size = 0
    l2_cache_size = 0
    l3_cache_size = 0
    flags = []
    virtualization = False
    for key, value in get_cpu_info().items():
        print('{}: {}'.format(key,value))
        if key == 'l1_cache_size':
            l1_cache_size = value
        elif key == 'l2_cache_size':
            l2_cache_size = value
        elif key == 'l3_cache_size':
            l3_cache_size = value
        elif key == 'flags':
            flags = value

    for flag in flags:
        if flag == 'svm' or flag == 'vmx':
            virtualization = True

    virtualization = bool(check_output(["powershell", "(Get-ComputerInfo).HyperVisorPresent"]).decode("utf-8").strip()) if not virtualization else False
    l3_l2_diff = l3_cache_size - l2_cache_size
    l1_cache_size = round((l3_l2_diff + l3_l2_diff * 0.83)/10000) if l1_cache_size == 0 else l1_cache_size
    return JsonResponse({
        "processor": processor,
        "processor_qty": processor_qty,
        "physical_cores": physical_cores,
        "threads": threads_qty,
        "data_bus": bits,
        "virtualization": virtualization,
        "base_speed": base_speed,
        "l1_cache": '{} KB'.format(l1_cache_size),
        "l2_cache": '{} MB'.format(round(l2_cache_size/1000000, 1)),
        "l3_cache": '{} MB'.format(round(l3_cache_size/1000000, 1))
    })

def cpu_variables(request):
    cpu_usage = psutil.cpu_percent(interval=60)
    speed = psutil.cpu_freq().current / 1000
    process_qty = len(psutil.pids())
    sub_process_qty = 0
    handles_qty = 0
    uptime_seconds = uptime.uptime()
    for process in psutil.process_iter():
        try:
            sub_process_qty += process.num_threads()
            handles_qty += process.num_handles()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return JsonResponse({
        "cpu_usage": cpu_usage,
        "speed": speed,
        "process_qty": process_qty,
        "sub_process_qty": sub_process_qty,
        "uptime": uptime_seconds
    })

""" def next(request):
    processor = platform.processor()
    physical_cores = psutil.cpu_count(logical=False)
    threads_qty = psutil.cpu_count(logical=True)
    (bits, linkage) = platform.architecture()
    total_ram_memory_bytes = round(psutil.virtual_memory().total/(1027**3), 2)
    free_ram_memory_bytes = round(psutil.virtual_memory().free/(1027**3), 2)
    total_ram_memory_gb = round(total_ram_memory_bytes/(1024**3), 2)
    psutil.virt
    return JsonResponse({
        "processor": processor,
        "physical_cores": physical_cores,
        "threads": threads_qty,
        "data_bus": bits,
        "total_memory": total_ram_memory_gb
    }) """