import numpy as np
import sys
import time
import csv


FILE_INPUT_NAME = "hw3dataset/graph_6.txt"
ERROR_TOLERANCE = 0.1
OUTPUT_HITS_RESULT_NAME = "HITS_RESULT.csv"

pages_arr = [] 
file_list = [] 

inp = open(FILE_INPUT_NAME) 
for row in inp.readlines():
    source, target = row.split(',')
    file_list.append([int(source),int(target)])
    if int(source) not in pages_arr:
        pages_arr.append(int(source)) 
    if int(target) not in pages_arr:
        pages_arr.append(int(target)) 
inp.close() 

page_num = max(pages_arr) 
graph = np.zeros((page_num,page_num)) 
for row in file_list: 
    graph[row[0]-1][row[1]-1] = 1
    
hub = np.full((page_num),1.0) 
aut = np.full((page_num),1.0) 
error = sys.maxsize
start_time = time.time()
while error > ERROR_TOLERANCE:
    new_hub = np.full((page_num),0.0)
    new_aut = np.full((page_num),0.0)
    max_hub = 0.0
    max_aut = 0.0
    error = 0.0
    
    for x in range(0,page_num): 
        for y in range(0,page_num):
            if graph[x][y] == 1:
                new_hub[x] += aut[y]
                new_aut[y] += hub[x]            

    for z in range(0,page_num): 
        if new_hub[z] > max_hub:
            max_hub = new_hub[z]
        if new_aut[z] > max_aut:
            max_aut = new_aut[z]
    
    for s in range(0,page_num): 
        new_hub[s] = new_hub[s]/max_hub
        new_aut[s] = new_aut[s]/max_aut
        error += (abs(new_hub[s] - hub[s])+abs(new_aut[s] - aut[s]))
        hub[s] = new_hub[s]
        aut[s] = new_aut[s]

print("--- Excution time %s seconds ---" % (time.time() - start_time))

output_data = [] 
print("Write result to csv file...")
for i in range(0,page_num):
    output_data.append([i+1,aut[i],hub[i]])
out_put_file = open(OUTPUT_HITS_RESULT_NAME, 'w', newline='')
with out_put_file:
    writer = csv.writer(out_put_file)
    writer.writerows(output_data)
print("done!")
