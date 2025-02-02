
import psutil
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment

def server_data(message_dict, message_text):
    
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
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        if "c:" in partition.device.lower():     # Windows系统下的C盘
            disk_space = psutil.disk_usage(partition.mountpoint)
            total_disk_space = disk_space.total / (1024**3)  # 将字节转换为GB
            used_disk_space = disk_space.used / (1024**3)    # 将字节转换为GB
            c_disk = f"C 盘：{used_disk_space:.2f} GB / {total_disk_space:.2f} GB\n"
        if "d:" in partition.device.lower():     # Windows系统下的D盘
            disk_space = psutil.disk_usage(partition.mountpoint)
            total_disk_space = disk_space.total / (1024**3)  # 将字节转换为GB
            used_disk_space = disk_space.used / (1024**3)    # 将字节转换为GB
            d_disk = f"D 盘：{used_disk_space:.2f} GB / {total_disk_space:.2f} GB"
    
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.normal_message(f"{message_text}：\n" + cpu + memory + c_disk + d_disk)

    