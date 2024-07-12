# domain/services.py
import platform
import psutil
import GPUtil
from domain.models import CPU, Memory, Disk, GPU, SystemInfo
from infrastructure.utils import load_json_file, save_json_file
from domain.security import hash_password, authenticate_user

USER_CREDENTIALS_FILE = "user_credentials.json"

class SystemInfoService:
    def get_system_info(self) -> SystemInfo:
        cpu = CPU(
            model=platform.processor(),
            cores=psutil.cpu_count(logical=False),
            threads=psutil.cpu_count(logical=True),
            frequency=psutil.cpu_freq().current
        )
        memory = Memory(
            total=psutil.virtual_memory().total,
            available=psutil.virtual_memory().available
        )
        disk = Disk(
            total=psutil.disk_usage('/').total,
            free=psutil.disk_usage('/').free
        )
        gpus = GPUtil.getGPUs()
        gpu_list = [
            GPU(
                name=gpu.name,
                memory_total=gpu.memoryTotal,
                memory_free=gpu.memoryFree,
                memory_used=gpu.memoryUsed
            )
            for gpu in gpus
        ]
        return SystemInfo(cpu=cpu, memory=memory, disk=disk, gpu=gpu_list)

    def get_cpu_usage(self):
        return psutil.cpu_percent(percpu=True)

class UserService:
    def load_user_credentials(self) -> dict:
        return load_json_file(USER_CREDENTIALS_FILE, {"users": []})

    def save_user_credentials(self, data: dict):
        save_json_file(USER_CREDENTIALS_FILE, data)

    def change_password(self, users: dict, username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        for user in users["users"]:
            if user["username"] == username and user["password"] == hash_password(old_password):
                if len(new_password) < 8:
                    return False, "New password too short."
                user["password"] = hash_password(new_password)
                self.save_user_credentials(users)
                return True, "Password changed successfully."
        return False, "Old password is incorrect."
