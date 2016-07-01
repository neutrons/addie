# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:47:21 2015

reads in a los.txt file, writes out auto_sum.inp file 

@author: Dan Olds
"""
from collections import defaultdict
import sys
import os.path

class GenerateSumthing(object):

    input_file = 'los.txt'
    
    def __init__(self, folder=None):
        self.folder = folder
        
    def create_sum_inp_file(self):
        full_input_file_name = os.path.join(self.folder, self.input_file)

        name_list=[]
        run_nums=defaultdict(list)
        
        if not os.path.isfile(full_input_file_name):
            raise IOError("File does not exist!")
        
        with open(full_input_file_name, "r") as myfile:
            data = myfile.readlines()
        
        for i in range(0,len(data)):
            if len(data[i].split()) == 9:
                if data[i].split()[7] == "scan":
                    word = data[i].split()[6]
                    run_num = int(data[i].split()[0])
                    temp_name = round(float(data[i].split()[8].replace("K","")))
                    temp_name = str(temp_name).replace(".0","")
                    word = word.replace("(","")
                    word = word.replace(")","_")
                    word = word+"_"+temp_name+"K"
                    if word in name_list:
                        run_nums[word].append(run_num)
                    else:
                        name_list.append(word)
                        run_nums[word].append(run_num)
        
        full_output_file_name = os.path.join(self.folder, "auto_sum.inp")        
        
        outfile = open(full_output_file_name, "w")
        outfile.write("background \n")
        
        print(">creating file %s" %full_output_file_name)
        for key in sorted(run_nums.iterkeys()):
            outbit = str(run_nums[key])
            outbit = outbit.replace("[","")
            outbit = outbit.replace("]","")
            outbit = outbit.replace(" ","")
            outfile.write(key + " " + outbit+"\n")

        outfile.close()