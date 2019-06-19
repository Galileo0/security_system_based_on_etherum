import subprocess
import os

print('City Security System Controller | CMD Version')
print ('---------------------------------------------')
while True:
    command = input('Command -> ')
    if command == 'Run_Gate':
        os.system('cd /media/galilio/06A04621A0461797/Ahmed/Dev/GP/imp/Auth/;python3 Gate_BC.py')
    elif command == 'Run_Resdent_server':
        os.system('cd /media/galilio/06A04621A0461797/Ahmed/Dev/GP/imp/resdent/;python3 init_visiting.py')
    elif command == 'Run_Tracking':
        os.system('cd /media/galilio/06A04621A0461797/Ahmed/Dev/GP/imp/Track_RF/;python3 Track.1.py;python3 Track.py')
    elif command == 'Run_Montering':
        os.system('cd /media/galilio/06A04621A0461797/Ahmed/Dev/GP/imp/SecurityB/;python3 montering.py')
    elif command == 'Help':
        print('''
        ------ Commands ------
        1- Run_Gate
        2- Run_Resdent_server
        3- Run_Tracking
        4- Run_Montering
        5- Help
        ''')
    else :
        print('Command Not Found')
