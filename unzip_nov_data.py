import os
import py7zr

PATH_TO_UNZIPPED = os.path.join( 'data', 'Data','Data', 'nextbike')

for filename in os.listdir(PATH_TO_UNZIPPED):
    path = os.path.join(PATH_TO_UNZIPPED, filename)
    with py7zr.SevenZipFile(path, mode='r') as z:
        z.extractall(path=os.path.join("intermediate", filename))

previous_name = ""
previous_index = 0
for u in os.listdir("intermediate"):
    if os.path.isdir(os.path.join("intermediate", u)):
        for i in os.listdir(os.path.join("intermediate", u)):
            with open(os.path.join("intermediate", u, i),'r',encoding='utf-8-sig') as data_file:
                if u[0:10] != previous_name:
                    previous_index = 0
                for line in data_file:
                    data = line.split("<?xml")
                    data2 = ["<?xml" + d2 for d2 in data]
                    data_final = data2[1:-1]
                    for i2, d in enumerate(data_final):
                        with open(os.path.join("results3", u[0:10]+"-"+str(previous_index+i2)+".xml"), "w",encoding='utf-8-sig') as text:
                            text.write(d)

                previous_index = previous_index+i2+1
                previous_name = u[0:10]