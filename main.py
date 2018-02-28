
# main.py to create bobst.py from modules
fin = open("modules/app_init.py", "r")
app_init = fin.read()
fin.close()

fin = open("modules/common.py", "r")
common = fin.read()
fin.close()

fin = open("modules/app_run.py", "r")
app_run = fin.read()
fin.close()

combined_file = app_init + common + app_run
fout = open("bobst.py", "w")

fout.write(combined_file)
fout.close()

