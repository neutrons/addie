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

    input_file_old_format = 'los.txt'
    input_file_new_format = 'los.csv'
    
    def __init__(self, folder=None):
        self.folder = folder
        
    def create_sum_inp_file(self):
        
        # try new output first
        full_input_file_name_new_format = os.path.join(self.folder, self.input_file_new_format)
        if os.path.isfile(full_input_file_name_new_format):
            self.create_sum_inp_file_from_new_format(full_input_file_name_new_format)
        else:
            full_input_file_name_old_format = os.path.join(self.folder, self.input_file_old_format)
            if os.path.isfile(full_input_file_name_old_format):
                self.create_sum_inp_file_from_old_format(full_input_file_name_old_format)
        #else:
        #        raise IOError("lost.* file does not exist!")

    def create_sum_inp_file_from_new_format(self,  full_input_file_name):
        
        print("[LOG] Reading %s" %full_input_file_name)
        name_list = []
        run_nums = defaultdict(list)
        
        with open(full_input_file_name, "r") as myfile:
            data = myfile.readlines()
                  
        for i in range(len(data)):
            if len(data[i].split(',')) == 8:
                if 'scan' in data[i].split(',') [6]:
                    word = data[i].split(',')[6]
                    run_num = int(data[i].split(',')[0])

                    temp_range = data[i].split(',')[7].replace("K", "").split('to')
                    from_temp = round(float(temp_range[0]))
                    temp_name = str(from_temp).replace(".0", "")
  
                    word = word.replace("(","")
                    word = word.replace(")","_")
                    word = word.replace(" ", "_")
                    word = word + "_" + temp_name + "K"
                    if word in name_list:
                        run_nums[word].append(run_num)
                    else:
                        name_list.append(word)
                        run_nums[word].append(run_num)
    
        full_output_file_name = os.path.join(self.folder, "auto_sum.inp")        
    
        outfile = open(full_output_file_name, "w")
        outfile.write("background \n")
    
        #print(">creating file %s" %full_output_file_name)
        for key in sorted(run_nums.iterkeys()):
            outbit = str(run_nums[key])
            outbit = outbit.replace("[","")
            outbit = outbit.replace("]","")
            outbit = outbit.replace(" ","")
            outfile.write(key + " " + outbit+"\n")
    
        outfile.close()


    def create_sum_inp_file_from_old_format(self, full_input_file_name):

        print("[LOG] Reading %s" %full_input_file_name)
        name_list=[]
        run_nums=defaultdict(list)
        
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
        
        #print(">creating file %s" %full_output_file_name)
        for key in sorted(run_nums.iterkeys()):
            outbit = str(run_nums[key])
            outbit = outbit.replace("[","")
            outbit = outbit.replace("]","")
            outbit = outbit.replace(" ","")
            outfile.write(key + " " + outbit+"\n")

        outfile.close()