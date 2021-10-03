import json
import subprocess

from datetime import datetime
from collections import Counter, defaultdict

process_dct = defaultdict(dict)
process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

for proc in process.split('\n')[1:-1]:
    process_list = proc.split()
    pid = int(process_list[1])
    user = process_list[0]
    cpu = float(process_list[2])
    mem = float(process_list[3])
    command = process_list[10]

    process_dct[pid]["user"] = user
    process_dct[pid]["cpu"] = cpu
    process_dct[pid]["mem"] = mem
    process_dct[pid]["command"] = user

counter_proc_by_name = Counter([value["user"] for _, value in process_dct.items()])
filename = datetime.now().strftime('%d-%m-%Y-%H:%M-scan.txt')

with open(filename, 'w', encoding="utf-8") as file:
    result = {
        "System_users": list(counter_proc_by_name),
        "Processes_started": len(process_dct),
        "Users_processes": [{user: count} for user, count in counter_proc_by_name.items()],
        "Total_memory_used": round(sum(value['mem'] for key, value in process_dct.items()), 2),
        "Total_CPU_used": f"{round(sum(v['cpu'] for k, v in process_dct.items()), 2)} %",
        "Most_memory_uses": max(process_dct.items(), key=lambda x: x[1]['mem'])[1]['command'],
        "Most_CPU_uses": max(process_dct.items(), key=lambda x: x[1]['cpu'])[1]['command']
    }
    result_dumps = json.dumps(result, indent=4)
    print(result_dumps)
    file.write(result_dumps)