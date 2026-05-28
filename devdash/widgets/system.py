"""System stats widget — CPU, memory, disk."""
from __future__ import annotations
import shutil
import subprocess
import platform
from dataclasses import dataclass


@dataclass
class SystemStats:
    cpu_percent: float
    mem_used_gb: float
    mem_total_gb: float
    mem_percent: float
    disk_used_gb: float
    disk_total_gb: float
    disk_percent: float
    platform: str


def _bar(pct: float, width: int = 20) -> str:
    filled = int(width * pct / 100)
    return "█" * filled + "░" * (width - filled)


def get_system_stats() -> SystemStats:
    """Collect system stats using stdlib only (no psutil required)."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return SystemStats(
            cpu_percent=cpu,
            mem_used_gb=mem.used / 1e9,
            mem_total_gb=mem.total / 1e9,
            mem_percent=mem.percent,
            disk_used_gb=disk.used / 1e9,
            disk_total_gb=disk.total / 1e9,
            disk_percent=disk.percent,
            platform=platform.system(),
        )
    except ImportError:
        pass

    # Fallback: parse /proc (Linux) or use vm_stat (macOS)
    sys = platform.system()
    cpu = 0.0
    mem_used = mem_total = 0.0
    mem_pct = 0.0

    if sys == "Darwin":
        try:
            out = subprocess.check_output(["vm_stat"], text=True)
            lines = dict(
                l.split(":") for l in out.strip().splitlines() if ":" in l
            )
            page = 4096
            free = int(lines.get(" Pages free", "0").strip().rstrip(".")) * page
            active = int(lines.get(" Pages active", "0").strip().rstrip(".")) * page
            wire = int(lines.get(" Pages wired down", "0").strip().rstrip(".")) * page
            mem_used = (active + wire) / 1e9
            mem_total = (free + active + wire) / 1e9
            mem_pct = (mem_used / mem_total * 100) if mem_total else 0.0
        except Exception:
            pass
    elif sys == "Linux":
        try:
            with open("/proc/meminfo") as f:
                mi = {l.split(":")[0]: int(l.split(":")[1].strip().split()[0]) * 1024
                      for l in f if ":" in l}
            mem_total = mi.get("MemTotal", 0) / 1e9
            mem_free = mi.get("MemAvailable", mi.get("MemFree", 0)) / 1e9
            mem_used = mem_total - mem_free
            mem_pct = (mem_used / mem_total * 100) if mem_total else 0.0
        except Exception:
            pass

    disk = shutil.disk_usage("/")
    return SystemStats(
        cpu_percent=cpu,
        mem_used_gb=mem_used,
        mem_total_gb=mem_total,
        mem_percent=mem_pct,
        disk_used_gb=disk.used / 1e9,
        disk_total_gb=disk.total / 1e9,
        disk_percent=disk.used / disk.total * 100 if disk.total else 0,
        platform=sys,
    )


def format_stats(s: SystemStats) -> list[str]:
    lines = [
        f"CPU    {_bar(s.cpu_percent)} {s.cpu_percent:4.0f}%",
        f"RAM    {_bar(s.mem_percent)} {s.mem_percent:4.0f}%  {s.mem_used_gb:.1f}/{s.mem_total_gb:.1f} GB",
        f"Disk   {_bar(s.disk_percent)} {s.disk_percent:4.0f}%  {s.disk_used_gb:.0f}/{s.disk_total_gb:.0f} GB",
    ]
    return lines
