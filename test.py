# def clean(phase, result):
#     if phase == 4:
#         data = 0
#     elif phase == 5:
#         data = 1
#     else :
#         data = 2
#     with open("./static/js/test.js", "r") as f:
#         lines = f.readlines()
#     with open("./static/js/test.js", "w") as f:
#         for line in lines:
#             if not f"""dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);""" in line.strip("\n"):
#                 f.write(line)

#clean(5, 0)

# def checkdriver(phase, result):
#     if phase == "Phase 4":
#         phase = 4
#         data = 0
#     elif phase == "Phase 5":
#         phase = 5
#         data = 1
#     else :
#         phase = 9
#         data = 2
#     with open("./static/js/test.js", "r") as f:
#         lines = f.readlines()
#     with open("./static/js/test.js", "r") as f:
#         for line in lines:
#             print(phase)
#             print(data)
#             print(result)
#             if line.find(f"""dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);""") != -1:
#                 print("Found!")
#                 break
#             else:
#                 print("Not found!")
   
# checkdriver("Phase 5", 0)  

# def addtoshow(phase, result):
#     if phase == "Phase 4":
#         phase = 4
#         data = 0
#         line_insert = 28
#     elif phase == "Phase 5":
#         phase = 5
#         data = 1
#         line_insert = 36
#     else :
#         phase = 9
#         data = 2
#         line_insert = 45
#     with open("./static/js/test.js", "r") as f:
#         lines = f.readlines()
#     with open("./static/js/test.js", "w") as f:
#         lines[line_insert] =  f'\n dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);  \n'
#         a_file = open("./static/js/test.js", "w")
#         a_file.writelines(lines)
#         a_file.close()
        
# addtoshow("Phase 9", 6)         
