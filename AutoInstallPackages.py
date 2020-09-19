import os
try:
    os.system("pip install PIL")
    os.system("pip install scipy")
    os.system("pip install numpy")
    input("Installed packages successfully.")
except:
    input("Failed installing packages successfully.")
