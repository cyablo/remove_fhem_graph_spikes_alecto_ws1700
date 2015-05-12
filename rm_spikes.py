inputfile  = "C:/temp/temp.txt"
outputfile = "C:/temp/new_temp.txt"
searchstring_temp = "temperature:"
searchstring_hum = "humidity:"
threshold = 2

buffer = []
compare_temps = []
compare_hums = []
line_count = 1

input = open(inputfile, 'r')
output = open(outputfile, 'w')

for line in input:
  if len(buffer) < 7:
    buffer.append(line)
    
  if len(buffer) == 7:
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
        if abs(compare_temps[1] - compare_temps[0]) >= threshold and abs(compare_temps[1] - compare_temps[2]) >= threshold:
          float_comma = compare_temps[1]
          if (float_comma).is_integer():
            float_comma = int(float_comma)
          buffer = [buffer_elements.replace(str(float_comma), str(round(((compare_temps[0] + compare_temps[2]) / 2), 1))) for buffer_elements in buffer]
      
      if len(compare_hums) == 3:
        if abs(compare_hums[1] - compare_hums[0]) >= threshold and abs(compare_hums[1] - compare_hums[2]) >= threshold:
          buffer = [buffer_elements.replace(str(compare_hums[1]), str((compare_hums[0] + compare_hums[2]) / 2)) for buffer_elements in buffer]
      
      compare_temps_new = []
      compare_hums_new = []
      compare_temps = compare_temps_new
      compare_hums = compare_hums_new
      del compare_temps_new[:]
      del compare_hums_new[:]
      output.write(buffer[0])
      buffer.pop(0)
  line_count += 1  
