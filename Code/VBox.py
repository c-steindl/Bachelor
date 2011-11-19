"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

from vboxapi import VirtualBoxManager
import os
import time
import sys

"""
    Script to run VM from terminal an start "client.py".
"""
def main(name, path, port, ip):
    
    # Username and password of VM hardcoded
    user = 'bachelor'
    password = 'bachelor'
    
    try:
        mgr = VirtualBoxManager(None, None)
        vbox = mgr.vbox
        mach = vbox.findMachine(name)
        session = mgr.mgr.getSessionObject(vbox)
        progress = mach.launchVMProcess(session, 'headless', '')
        progress.waitForCompletion(-1)
        print 'VM started!', name
        
        # Waits for the guestcontrol execution to be ready.
        time.sleep(20)
    except Exception:
        print 'VM ' + name + ' not started. Probably it is already started'
        pass

    try:
        command = 'VBoxManage guestcontrol "' + name + '" exec --image "/usr/bin/python" --username ' + user + ' --password ' + password + ' --wait-exit --wait-stdout --wait-stderr -- ' + path + '/client.py' + ' ' + str(port) + ' ' + ip
        print 'Execution of:', command
        # Runs the client.py script at defined location.
        os.system('VBoxManage guestcontrol "ubuntu4" exec --image "/usr/bin/python" --username bachelor --password bachelor --wait-exit --wait-stdout --wait-stderr -- /home/bachelor/Dropbox/Bachelorarbeit/Code/client.py 50007 192.168.56.1')
    except Exception:
        print 'Could not run "' + command + '"'
        pass

def usage():
    print 'USAGE: python VBox.py <Name of VM> <Path to client.py> <Port to connect> <Server IP>'
    
if __name__ == "__main__":
    if len(sys.argv) == 5:
        name = str(sys.argv[1])
        path = str(sys.argv[2])
        port = int(sys.argv[3])
        ip = str(sys.argv[4])
        
        main(name, path, port, ip)
        
    elif len(sys.argv) == 3:
        name = str(sys.argv[1])
        path = str(sys.argv[2])
        port = 50007
        ip = socket.gethostbyname(socket.gethostname())
        
        main(name, path, port, ip)
        
    else: usage()