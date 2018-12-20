import numpy as np
import sys
import random
import time
import csv


FILE_INPUT_NAME = "hw3dataset/graph_6.txt"
ERROR_TOLERANCE = 0.1
OUTPUT_PAGERANK_RESULT_NAME = "PAGERANK_RESULT.csv"

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

pr_vector = np.full((page_num),1.0) 

temp1, temp2 = np.unique(graph, return_counts=True) 
link_num = temp2[1]

for i in range(0,page_num): 
    for j in range(0,page_num):
        if graph[i][j] == 1.0:
            graph[i][j] = graph[i][j] / link_num
            
graph = graph.T 

page_ranks_i = np.full((page_num,page_num),0.0)
page_ranks_j = np.full((page_num,page_num),0.0)
start_time = time.time()
for i in range(0,page_num): 
    for j in range(0,page_num):
        DAMP_FACTOR =  0.15 
        page_ranks_j[i][j] = (1.0-DAMP_FACTOR)/page_num
        page_ranks_i[i][j] = (DAMP_FACTOR * graph[i][j]) + page_ranks_j[i][j]
        
error = sys.maxsize
new_pr_vector = np.full((page_num),1.0)

while error > ERROR_TOLERANCE:
    error = 0.0
    for i in range(0,page_num):
        temp = 0.0
        for j in range(0,page_num):
            temp += page_ranks_i[i][j] * pr_vector[j]
        new_pr_vector[i] = temp
        
    for i in range(0,page_num):
        error += abs(new_pr_vector[i] - pr_vector[i])
        pr_vector[i] = new_pr_vector[i]

print("--- Excution time %s seconds ---" % (time.time() - start_time))

output_data = [] 
print("Write result to csv file...")
for i in range(0,page_num):
    output_data.append([i+1,pr_vector[i]])
out_put_file = open(OUTPUT_PAGERANK_RESULT_NAME, 'w', newline='')
with out_put_file:
    writer = csv.writer(out_put_file)
    writer.writerows(output_data)
print("done!")
