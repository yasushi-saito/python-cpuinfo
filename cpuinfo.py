import re
import collections
from typing import List, NamedTuple, Tuple

"""
Parse /proc/cpuinfo in Linux.
"""

class CPU(object):
    def __init__(self) -> None:
        self.processor = 0
        self.vendor_id = ''
        self.cpu_family = -1
        self.model = -1
        self.model_name = ''
        self.stepping = -1
        self.microcode = -1
        self.cpu_mhz = -1.0
        self.cache_size = -1
        self.physical_id = -1
        self.siblings = -1
        self.core_id = -1
        self.cpu_cores = -1
        self.apicid = -1
        self.initial_apicid = -1
        self.fpu = False
        self.fpu_exception = False
        self.cpuid_level = -1
        self.wp = False
        self.flags: List[str] = []
        self.bogomips = -1.0
        self.clflush_size = -1
        self.cache_alignment = -1
        self.address_sizes = (0, 0)  # physical-addr bits, virt-addr bits.

    def __str__(self):
        return ('processor=%s vendor_id=%s cpu_family=%s '
                'model=%s model_name=%s stepping=%s microcode=%s '
                'cpu_mhz=%s cache_size=%s physical_id=%s siblings=%s '
                'core_id=%s cpu_cores=%s apicid=%s initial_apicid=%s '
                'fpu=%s fpu_exception=%s cpuid_level=%s '
                'wp=%s flags=%s bogomips=%s '
                'clflush_size=%s cache_alignment=%s address_size=%s' % (
            self.processor,
            self.vendor_id,
            self.cpu_family,
            self.model,
            self.model_name,
            self.stepping,
            self.microcode,
            self.cpu_mhz,
            self.cache_size,
            self.physical_id,
            self.siblings,
            self.core_id,
            self.cpu_cores,
            self.apicid,
            self.initial_apicid,
            self.fpu,
            self.fpu_exception,
            self.cpuid_level,
            self.wp,
            self.flags,
            self.bogomips,
            self.clflush_size,
            self.cache_alignment,
            self.address_sizes))

def get_cpuinfo() -> List[CPU]:
    cpus: List[CPU] = []
    cur_cpu: CPU = None
    with open('/proc/cpuinfo') as f:
        for line in f.readlines():
            m = re.match(r'processor\s+: (\d+)', line)
            if m:
                print("m", m)
                if cur_cpu:
                    cpus.append(cur_cpu)
                cur_cpu = CPU()
                cur_cpu.processor=int(m.group(1))
            m = re.match(r'vendor_id\s+: (.*)', line)
            if m:
                cur_cpu.vendor_id = m.group(1)
            m = re.match(r'physical id\s+: (.*)', line)
            if m:
                cur_cpu.physical_id = int(m.group(1))
            m = re.match(r'siblings\s+: (.*)', line)
            if m:
                cur_cpu.siblings = int(m.group(1))
            m = re.match(r'core id\s+: (.*)', line)
            if m:
                cur_cpu.core_id = int(m.group(1))
            m = re.match(r'cpu cores\s+: (.*)', line)
            if m:
                cur_cpu.cpu_cores = int(m.group(1))
            m = re.match(r'apicid\s+: (.*)', line)
            if m:
                cur_cpu.apicid = int(m.group(1))
    if cur_cpu:
        cpus.append(cur_cpu)
    return cpus
