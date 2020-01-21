import subprocess
import os

# Split pcap

print('Starting PCAP Splitting Script, please make sure you run this from the directory which contain your PCAP files!!!\n\n')
print(f'Current Directory: {os.getcwd()}')
directory = os.getcwd()

num = 0
for file in os.listdir(directory):
    if file.endswith(".pcap"):
        print(file)
        out_file_name = f'out_put_test_{num}_pcap'
        subprocess.run(["tcpdump", "-r", file, "-w", out_file_name, "-C", "100"]) #  tcpdump -r bigpcap3.pcap -w out_put_file -C 100
        num += 1


# Now we convert PCAP to .json to send to ElasticSearch
# tshark -r out_put_test_{num}_pcap -T ek -w out_put_json_{num2}_json
#
num = 0

for file in os.listdir(directory):
    if file.endswith("_pcap"):
        print(file)
        json_out_file = f'json_out_file_{num}_json'
        subprocess.run(["tshark", "-Q", "-r", file, "-T", "ek", ">", json_out_file])
        num += 1
