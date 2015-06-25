import os
import shutil
import glob

pathtolog = "/opt/fhem/log/"
filepattern = "TempKeller"
searchstring_temp = "temperature:"
searchstring_hum = "humidity:"
threshold_temps = 1
threshold_hums = 2
buffer_lenght = 9

buffer = []
compare_temps = []
compare_hums = []
line_count = 1

try:
    inputfile = max(glob.iglob(pathtolog + '*' + filepattern + '*.log'), key=os.path.getctime)
except ValueError:
    print "Could not find File matching Pattern in specified Path, Exiting!"
    exit()

outputfile = inputfile + '.tmp'

input = open(inputfile, 'r')
output = open(outputfile, 'w')

for line in input:
  if len(buffer) < buffer_size:
    buffer.append(line)
    
  if len(buffer) == buffer_size:
    if len([s for s in buffer if searchstring_temp in s]) != 3 and len([s for s in buffer if searchstring_hum in s]) != 3:
      output.write(buffer[0])
      buffer.pop(0)
    else:
      for buffer_element in buffer:
        if searchstring_temp in buffer_element:
          compare_temps.append(float(((buffer_element.split(searchstring_temp,1)[1]).strip())))
        if searchstring_hum in buffer_element:
          compare_hums.append(int(((buffer_element.split(searchstring_hum,1)[1]).strip())))

      if len(compare_temps) == 3:
        if abs(compare_temps[1] - compare_temps[0]) >= threshold_temps and abs(compare_temps[1] - compare_temps[2]) >= threshold_temps:
          float_comma = compare_temps[1]
          if (float_comma).is_integer():
            float_comma = int(float_comma)
          buffer = [buffer_elements.replace(searchstring_temp + " " + str(float_comma), searchstring_temp + " " + str(round(((compare_temps[0] + compare_temps[2]) / 2), 1))) for buffer_elements in buffer]
      
      if len(compare_hums) == 3:
        if abs(compare_hums[1] - compare_hums[0]) >= threshold_hums and abs(compare_hums[1] - compare_hums[2]) >= threshold_hums:
          buffer = [buffer_elements.replace(searchstring_hum + " " + str(compare_hums[1]), searchstring_hum + " " + str((compare_hums[0] + compare_hums[2]) / 2)) for buffer_elements in buffer]
      
      compare_temps_new = []
      compare_hums_new = []
      compare_temps = compare_temps_new
      compare_hums = compare_hums_new
      del compare_temps_new[:]
      del compare_hums_new[:]
      output.write(buffer[0])
      buffer.pop(0)
  line_count += 1

for buffer_element in buffer:
  output.write(buffer_element)

input.close()
output.close()
shutil.copy(outputfile, inputfile)
os.remove(outputfile)
