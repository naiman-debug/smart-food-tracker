"""
系统信息 API - 提供系统级别的信息接口
"""
from fastapi import APIRouter, HTTPException
import socket
import subprocess
import platform
from typing import List

router = APIRouter(prefix="/api/system", tags=["system"])


def get_local_ip_addresses() -> List[str]:
    """
    获取本机的所有本地IP地址列表

    Returns:
        List[str]: 本地IP地址列表，排除127.0.0.1
    """
    ip_addresses = []

    try:
        # 方法1: 通过连接到外部地址获取本地IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # 不实际发送数据，只是获取本机用于连接外部地址的IP
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            if primary_ip and not primary_ip.startswith("127."):
                ip_addresses.append(primary_ip)

        # 方法2: 获取主机名对应的所有IP
        hostname = socket.gethostname()
        try:
            # 获取完整主机名（可能在某些网络环境下更有用）
            full_hostname = socket.getfqdn()
            addr_info = socket.getaddrinfo(full_hostname, None)
            for info in addr_info:
                ip = info[4][0]
                if ip and not ip.startswith("127.") and ip not in ip_addresses:
                    # 只保留IPv4地址
                    if ":" not in ip:
                        ip_addresses.append(ip)
        except Exception:
            pass

        # 方法3: Windows特定方法 - 使用ipconfig
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
                import re
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

        # 方法4: Linux/Mac特定方法
        else:
            try:
                result = subprocess.run(
                    ["ifconfig"] if platform.system() != "Linux" else ["ip", "addr"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                output = result.stdout

                import re
                # 匹配inet地址（排除127.0.0.1）
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


@router.get("/local-ip")
async def get_local_ip():
    """
    获取服务器的本机IP地址列表

    返回本机所有可用的局域网IP地址，用于手机访问提示。

    Returns:
        {
            "ips": ["192.168.1.100", "192.168.0.5"],  // IP地址列表
            "primary_ip": "192.168.1.100",              // 主要IP（第一个）
            "hostname": "DESKTOP-ABC123"                 // 主机名
        }
    """
    try:
        ip_list = get_local_ip_addresses()

        # 获取主机名
        hostname = socket.gethostname()

        return {
            "ips": ip_list,
            "primary_ip": ip_list[0] if ip_list else "localhost",
            "hostname": hostname,
            "count": len(ip_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取IP地址失败: {str(e)}")


@router.get("/info")
async def get_system_info():
    """
    获取系统基本信息

    Returns:
        {
            "platform": "Windows",
            "hostname": "DESKTOP-ABC123",
            "port": 8000
        }
    """
    return {
        "platform": platform.system(),
        "hostname": socket.gethostname(),
        "port": 8000
    }
