#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Smart Food Tracker - Environment Check Script
验证Python、Node.js、依赖包状态
"""
import sys
import os
import subprocess
import socket
from typing import List, Tuple

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(title: str):
    """打印标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_ok(text: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text: str):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def print_info(text: str):
    """打印信息"""
    print(f"{Colors.CYAN}○{Colors.RESET} {text}")


def check_python_version() -> Tuple[bool, str]:
    """检查Python版本"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 8:
        return True, version_str
    else:
        return False, version_str


def check_node_version() -> Tuple[bool, str]:
    """检查Node.js版本"""
    try:
        result = subprocess.run(
            ['node', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_str = result.stdout.strip()
            # Extract version number (v16.14.0 -> 16.14.0)
            version_num = version_str.lstrip('v')
            major = int(version_num.split('.')[0])
            if major >= 14:
                return True, version_str
            else:
                return False, version_str
        return False, "Not found"
    except Exception:
        return False, "Not found"


def check_python_packages() -> List[str]:
    """检查Python依赖包"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'python-dotenv',
        'httpx'
    ]

    missing_packages = []
    installed_packages = []

    for package in required_packages:
        try:
            __import__(package)
            installed_packages.append(package)
        except ImportError:
            missing_packages.append(package)

    return missing_packages, installed_packages


def check_npm_packages() -> bool:
    """检查npm依赖包"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    node_modules_dir = os.path.join(frontend_dir, 'node_modules')

    if os.path.exists(node_modules_dir):
        # Check if it's not empty
        if os.listdir(node_modules_dir):
            return True

    return False


def check_port_in_use(port: int) -> Tuple[bool, str]:
    """检查端口是否被占用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()

    if result == 0:
        return True, "Port is in use"
    else:
        return False, "Port is available"


def get_local_ip() -> str:
    """获取本机IP地址"""
    try:
        # Create a socket connection to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════╗")
    print("║      Smart Food Tracker - Environment Check      ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    all_passed = True

    # ============================================
    # Check Python
    # ============================================
    print_header("1. Python Environment Check")

    python_ok, python_version = check_python_version()
    if python_ok:
        print_ok(f"Python version: {python_version}")
    else:
        print_error(f"Python version: {python_version} (requires 3.8+)")
        print_info("Please install Python 3.8 or higher")
        all_passed = False

    # ============================================
    # Check Node.js
    # ============================================
    print_header("2. Node.js Environment Check")

    node_ok, node_version = check_node_version()
    if node_ok:
        print_ok(f"Node.js version: {node_version}")
    else:
        print_error(f"Node.js: {node_version} (requires 14+)")
        print_info("Please install Node.js 14 or higher")
        all_passed = False

    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_ok(f"npm version: {result.stdout.strip()}")
        else:
            print_warning("npm not found")
    except Exception:
        print_warning("npm not found")

    # ============================================
    # Check Python Packages
    # ============================================
    print_header("3. Python Dependencies Check")

    missing, installed = check_python_packages()

    if installed:
        print_ok(f"Installed packages: {len(installed)}/{len(instired) + len(missing)}")
        for pkg in installed:
            print(f"  - {pkg}")

    if missing:
        print_error(f"Missing packages: {len(missing)}")
        for pkg in missing:
            print(f"  - {pkg}")
        print_info("Run: pip install -r requirements.txt")
        all_passed = False
    else:
        print_ok("All required Python packages are installed")

    # ============================================
    # Check npm Packages
    # ============================================
    print_header("4. Frontend Dependencies Check")

    npm_ok = check_npm_packages()
    if npm_ok:
        print_ok("Frontend dependencies are installed (node_modules exists)")
    else:
        print_error("Frontend dependencies not installed")
        print_info("Run: cd frontend && npm install")
        all_passed = False

    # ============================================
    # Check Ports
    # ============================================
    print_header("5. Port Availability Check")

    port_8000_in_use, _ = check_port_in_use(8000)
    if port_8000_in_use:
        print_warning("Port 8000 is in use (backend)")
        print_info("Backend service may fail to start")
    else:
        print_ok("Port 8000 is available (backend)")

    port_5173_in_use, _ = check_port_in_use(5173)
    if port_5173_in_use:
        print_warning("Port 5173 is in use (frontend)")
        print_info("Frontend service may fail to start")
    else:
        print_ok("Port 5173 is available (frontend)")

    # ============================================
    # Get Local IP
    # ============================================
    print_header("6. Network Information")

    local_ip = get_local_ip()
    print_ok(f"Local IP address: {local_ip}")
    print_info(f"For mobile access: http://{local_ip}:5173")

    # ============================================
    # Check Backend Files
    # ============================================
    print_header("7. Project Files Check")

    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')

    required_backend_files = [
        'app/main.py',
        'app/api/meal.py',
        'app/data/extended_food_database.py',
        'init_extended_database.py'
    ]

    required_frontend_files = [
        'src/api/index.ts',
        'src/views/Record.vue',
        'src/views/Home.vue',
        'package.json'
    ]

    backend_files_ok = True
    for file_path in required_backend_files:
        full_path = os.path.join(backend_dir, file_path)
        if os.path.exists(full_path):
            print_ok(f"backend/{file_path}")
        else:
            print_error(f"backend/{file_path} - Not found")
            backend_files_ok = False

    frontend_files_ok = True
    for file_path in required_frontend_files:
        full_path = os.path.join(frontend_dir, file_path)
        if os.path.exists(full_path):
            print_ok(f"frontend/{file_path}")
        else:
            print_error(f"frontend/{file_path} - Not found")
            frontend_files_ok = False

    if not backend_files_ok or not frontend_files_ok:
        all_passed = False

    # Check .env file
    env_file = os.path.join(backend_dir, '.env')
    if os.path.exists(env_file):
        print_ok("backend/.env exists")
        # Check if GLM_API_KEY is set
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'your_glm_api_key_here' in content or 'GLM_API_KEY=' not in content:
                print_warning("GLM_API_KEY is not configured in .env")
            else:
                print_ok("GLM_API_KEY is configured")
    else:
        print_warning("backend/.env not found (will be created automatically)")

    # ============================================
    # Summary
    # ============================================
    print_header("Check Summary")

    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed! Environment is ready.{Colors.RESET}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.RESET}")
        print(f"  1. Run: start_local.bat (Windows)")
        print(f"     or: ./start_local.sh (macOS/Linux)")
        print(f"  2. Or run: start_simple.bat (quick start)")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please fix the issues above.{Colors.RESET}")
        print(f"\n{Colors.BOLD}Common fixes:{Colors.RESET}")
        print(f"  1. Install Python 3.8+: https://www.python.org/downloads/")
        print(f"  2. Install Node.js 14+: https://nodejs.org/")
        print(f"  3. Install Python dependencies:")
        print(f"     cd backend")
        print(f"     pip install -r requirements.txt")
        print(f"  4. Install frontend dependencies:")
        print(f"     cd frontend")
        print(f"     npm install")
        print(f"\n{Colors.CYAN}For detailed help, see: MANUAL_INSTALL_GUIDE.md{Colors.RESET}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
