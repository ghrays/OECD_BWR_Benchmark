import sys, os
path = os.getcwd() 
for file in os.listdir(path):
 if file.endswith(".xlsx"):
    print(file)