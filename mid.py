from subprocess import check_output,DEVNULL
from hashlib import sha256
from uuid import getnode


def get_hardware_ids(command, key_name):
    """通过WMIC命令获取硬件信息"""
    try:
        output = check_output(
            command,
            shell=True,
            stderr=DEVNULL,
            text=True,
            encoding='utf-8'
        )
        values = [value.strip() for line in output.splitlines() if line.startswith(f"{key_name}=")
                  for _, value in (line.split('=', 1),)]
        return ''.join(values)
    except Exception:
        return ''


def generate_mid():
    """生成基于硬件信息的机器码"""
    hardware_components = [
        ('CPU', 'wmic cpu get ProcessorId /value', 'ProcessorId'),
        ('Disk', 'wmic diskdrive get SerialNumber /value', 'SerialNumber'),
        ('Motherboard', 'wmic baseboard get SerialNumber /value', 'SerialNumber')
    ]

    combined = ''.join(get_hardware_ids(component[0], component[2]) for component in hardware_components)
    combined += hex(getnode())[2:]

    if combined:
        # 使用SHA-256生成哈希值
        hash_object = sha256(combined.encode('utf-8'))
        full_hash = hash_object.hexdigest().upper()

        # 截取前22个字符
        machine_code = full_hash[:22]

        # 按照1-9-5-7格式分割
        formatted_code = '-'.join([
            machine_code[0:1],
            machine_code[1:10],
            machine_code[10:15],
            machine_code[15:22]
        ])

        return formatted_code
    else:
        return None
if __name__ == "__main__":
    print(generate_mid())
