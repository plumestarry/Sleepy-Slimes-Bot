
import psutil
import platform
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment

def server_data(message_dict, message_text):
    
    # 获取操作系统类型
    os_type = platform.system().lower()
    
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    count = 0
    cpu_usage_total = 0
    for usage in cpu_usage:
        if usage:
            cpu_usage_total += usage
            count += 1
    cpu = f"CPU: {cpu_usage_total / count:.2f} % 不准确，仅供参考\n"

    # 获取最大内存
    max_memory = psutil.virtual_memory().total / (1024**3)  # 将字节转换为GB
    used_memory = psutil.virtual_memory().used / (1024**3)
    memory = f"内存：{used_memory:.2f} GB / {max_memory:.2f} GB\n"

    # 获取磁盘存储空间
    disk_info = ""
    disk_partitions = psutil.disk_partitions()
    if os_type == "windows":
        for partition in disk_partitions:
            if "c:" in partition.device.lower():     # Windows系统下的C盘
                disk_space = psutil.disk_usage(partition.mountpoint)
                total_disk_space = disk_space.total / (1024**3)  # 将字节转换为GB
                used_disk_space = disk_space.used / (1024**3)    # 将字节转换为GB
                disk_info += f"C 盘：{used_disk_space:.2f} GB / {total_disk_space:.2f} GB\n"
            if "d:" in partition.device.lower():     # Windows系统下的D盘
                disk_space = psutil.disk_usage(partition.mountpoint)
                total_disk_space = disk_space.total / (1024**3)  # 将字节转换为GB
                used_disk_space = disk_space.used / (1024**3)    # 将字节转换为GB
                disk_info += f"D 盘：{used_disk_space:.2f} GB / {total_disk_space:.2f} GB\n"
    elif os_type == "linux":
        for partition in disk_partitions:
            if "/" == partition.mountpoint:     # Ubuntu系统下的根目录
                disk_space = psutil.disk_usage(partition.mountpoint)
                total_disk_space = disk_space.total / (1024**3)  # 将字节转换为GB
                used_disk_space = disk_space.used / (1024**3)    # 将字节转换为GB
                disk_info += f"根目录：{used_disk_space:.2f} GB / {total_disk_space:.2f} GB\n"
            if "/home" == partition.mountpoint:     # Ubuntu系统下的home目录
                disk_space = psutil.disk_usage(partition.mountpoint)
                total_disk_space = disk_space.total / (1024**3)  # 将字节转换为GB
                used_disk_space = disk_space.used / (1024**3)    # 将字节转换为GB
                disk_info += f"Home 目录：{used_disk_space:.2f} GB / {total_disk_space:.2f} GB\n"
    
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.normal_message(f"{message_text}：\n" + cpu + memory + disk_info)

    