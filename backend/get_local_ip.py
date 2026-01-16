"""
获取本机IP地址并写入前端配置文件
用于手机访问提示
"""
import socket
import subprocess
import platform
import json
import os
import re


def get_local_ip_addresses():
    """
    获取本机的所有本地IP地址列表

    Returns:
        List[str]: 本地IP地址列表，排除127.0.0.1
    """
    ip_addresses = []

    try:
        # 方法1: 通过连接到外部地址获取本地IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            if primary_ip and not primary_ip.startswith("127."):
                ip_addresses.append(primary_ip)

        # 方法2: Windows特定方法 - 使用ipconfig
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["ipconfig"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                output = result.stdout

                # 匹配IPv4地址
                ipv4_pattern = r'IPv4 Address[^\d]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                matches = re.findall(ipv4_pattern, output)

                for match in matches:
                    if match and not match.startswith("127.") and match not in ip_addresses:
                        ip_addresses.append(match)

                # 也尝试中文版ipconfig
                ipv4_pattern_cn = r'IPv4 地址[^\d]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                matches_cn = re.findall(ipv4_pattern_cn, output)
                for match in matches_cn:
                    if match and not match.startswith("127.") and match not in ip_addresses:
                        ip_addresses.append(match)
            except Exception:
                pass

        # 方法3: Linux/Mac特定方法
        else:
            try:
                result = subprocess.run(
                    ["ifconfig"] if platform.system() != "Linux" else ["ip", "addr"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                output = result.stdout

                inet_pattern = r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                matches = re.findall(inet_pattern, output)

                for match in matches:
                    if match and not match.startswith("127.") and match not in ip_addresses:
                        ip_addresses.append(match)
            except Exception:
                pass

    except Exception as e:
        print(f"获取IP地址时出错: {e}")

    # 去重并返回（保持顺序，优先主IP）
    seen = set()
    unique_ips = []
    for ip in ip_addresses:
        if ip not in seen:
            seen.add(ip)
            unique_ips.append(ip)

    return unique_ips


def main():
    """主函数：获取IP并写入配置文件"""

    # 获取IP地址列表
    ip_list = get_local_ip_addresses()

    if not ip_list:
        print("警告: 未能获取到本地IP地址")
        ip_list = ["localhost"]

    # 获取脚本所在目录的上级目录（项目根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # 前端public目录
    public_dir = os.path.join(project_root, "frontend", "public")

    # 确保目录存在
    os.makedirs(public_dir, exist_ok=True)

    # 配置文件路径
    config_file = os.path.join(public_dir, "ip-config.json")

    # 准备配置数据
    config_data = {
        "ips": ip_list,
        "primary_ip": ip_list[0] if ip_list else "localhost",
        "hostname": socket.gethostname(),
        "port": 5173,
        "timestamp": __import__('time').time()
    }

    # 写入配置文件
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        print(f"IP配置已写入: {config_file}")
        print(f"主要IP: {config_data['primary_ip']}")
        if len(ip_list) > 1:
            print(f"其他可用IP: {', '.join(ip_list[1:])}")

        return 0
    except Exception as e:
        print(f"写入配置文件失败: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
