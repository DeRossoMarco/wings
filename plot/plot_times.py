import os
import re
import matplotlib.pyplot as plt

def extract_time_from_log(file_path):
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        return None

    with open(file_path, 'r') as file:
        lines = file.readlines()[-30:]
    content = ''.join(lines)

    if 'snappyHexMesh' in file_path:
        pattern = r'Finished meshing in\s*=\s*(\d+(\.\d+)?)\s*s'
        group_index = 1
    else:
        pattern = r'total\s+:\s+avg\s+=\s+\d+(\.\d+)?,\s+min\s+=\s+\d+(\.\d+)?\s+\(proc\s+\d+\),\s+max\s+=\s+(\d+(\.\d+)?)\s+\(proc\s+\d+\)'
        group_index = 3

    match = re.search(pattern, content)
    if match:
        return float(match.group(group_index))

    print('Time not found:', file_path)
    return None

def save_plot_with_high_resolution(filename):
    plt.savefig(filename, dpi=600)

def main():
    log_files = ['log.snappyHexMesh', 'log.simpleFoam', 'log.pimpleFoam']
    processes_dir = 'one_wing/processes'
    
    mesh_times = []
    simple_times = []
    pimple_times = []
    process_counts = []

    for process in sorted(os.listdir(processes_dir), key=int):
        process_path = os.path.join(processes_dir, process)
        if os.path.isdir(process_path):
            process_counts.append(int(process))
            mesh_time = extract_time_from_log(os.path.join(process_path, 'log/log.snappyHexMesh'))
            simple_time = extract_time_from_log(os.path.join(process_path, 'log/log.simpleFoam'))
            pimple_time = extract_time_from_log(os.path.join(process_path, 'log/log.pimpleFoam'))
            
            mesh_times.append(mesh_time if mesh_time else 0)
            simple_times.append(simple_time if simple_time else 0)
            pimple_times.append(pimple_time if pimple_time else 0)

    total_times = [m + s + p for m, s, p in zip(mesh_times, simple_times, pimple_times)]

    plt.figure()
    plt.plot(process_counts, mesh_times, label='Mesh Time')
    for count in process_counts:
        plt.axvline(x=count, color='gray', linestyle='--', linewidth=0.5)
    for y in plt.yticks()[0]:
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel('Processes')
    plt.ylabel('Time (s)')
    plt.title('Mesh Time over Processes')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks(process_counts, process_counts)
    save_plot_with_high_resolution('mesh_time.png')

    plt.figure()
    plt.plot(process_counts, simple_times, label='SimpleFoam Time')
    plt.plot(process_counts, pimple_times, label='PimpleFoam Time')
    for count in process_counts:
        plt.axvline(x=count, color='gray', linestyle='--', linewidth=0.5)
    for y in plt.yticks()[0]:
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel('Processes')
    plt.ylabel('Time (s)')
    plt.title('SimpleFoam and PimpleFoam Time over Processes')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks(process_counts, process_counts)
    save_plot_with_high_resolution('simple_pimple_time.png')

    plt.figure()
    plt.plot(process_counts, total_times, label='Total Time')
    for count in process_counts:
        plt.axvline(x=count, color='gray', linestyle='--', linewidth=0.5)
    for y in plt.yticks()[0]:
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel('Processes')
    plt.ylabel('Time (s)')
    plt.title('Total Time over Processes')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks(process_counts, process_counts)
    save_plot_with_high_resolution('total_time.png')

    # Plot speedup and ideal scalability
    reference_time = total_times[process_counts.index(2)]
    speedup = [reference_time / t for t in total_times]
    ideal_speedup = [count / 2 for count in process_counts]

    plt.figure()
    plt.plot(process_counts, speedup, label='Speedup')
    plt.plot(process_counts, ideal_speedup, 'r--', label='Ideal Scalability')
    for count in process_counts:
        plt.axvline(x=count, color='gray', linestyle='--', linewidth=0.5)
    for y in plt.yticks()[0]:
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel('Processes')
    plt.ylabel('Speedup')
    plt.title('Speedup and Ideal Scalability over Processes')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks(process_counts, process_counts)
    save_plot_with_high_resolution('speedup.png')

if __name__ == '__main__':
    main()
