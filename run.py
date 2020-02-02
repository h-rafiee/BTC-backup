from subprocess import Popen, PIPE
import sys, getopt, shlex, datetime
import zipfile , ftplib , shutil
import glob, os

rpcUser = '*****'
rpcPassword = '*************'
key = '*************'
ftpServer = '*.*.*.*' #192.168.1.1
ftpUser = 'btc1001'
ftpPass = 'btc2002'
ftpPath = '/.btc/'
ftpEnable = True

def main(argv):
    method = 'full'
    path = '/var/backup/.btc'
    try:
        opts, args = getopt.getopt(argv,"h",['help','method=','path=','rpc-user=','rpc-password=','ftp-server=','ftp-user=','ftp-pass=', 'ftp-path=','ftp-disable'])
    except getopt.GetoptError :
        print('run.py --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print("Backup version 1.0.0.1 by Hossein Rafiee - [help]\n")
            print('run.py --method=<full|wallet|privateKeys> --path=<optional: path>')
            print("-------------------------------------")
            print("• default method: full")
            print("• default path: /var/backup/.btc\n")
            print("--rpc-user=*****\n\t for set rpc connection")
            print("--rpc-password=******\n\t for set rpc connection")
            print("--ftp-server=*.*.*.*\n\t for set ftp server to upload")
            print("--ftp-user=usr\n\t for set ftp username")
            print("--ftp-pass=val\n\t for set ftp password")
            print("--ftp-path=val\n\t for set ftp path upload")
            print("--ftp-disable\n\t for disable ftp")
            sys.exit(2)
        elif opt == '-m' or opt == '--method':
            if arg in ['full','wallet','privateKeys']:
                method = arg
            else :
                print('run.py -method=<full|wallet|privateKeys> --path=<optional: path>')
                sys.exit(2)
        elif opt == '--path':
            path = arg
        elif opt == '--rpc-user':
            global rpcUser
            rpcUser = arg
        elif opt == '--rpc-password':
            global rpcPassword
            rpcPassword = arg
        elif opt == '--ftp-server':
            global ftpServer
            ftpServer = arg
        elif opt == '--ftp-user':
            global ftpUser
            ftpUser = arg
        elif opt == '--ftp-pass':
            global ftpPass
            ftpPass = arg
        elif opt == '--ftp-path':
            global ftpPath
            ftpPath = arg
        elif opt == '--ftp-disable':
            global ftpEnable
            ftpEnable = False
    backup(method, path)

def backup(method , rootPath):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    path = rootPath + '/' + now
    if os.path.isdir(path) is not True :
        os.makedirs(path)
    status = True

    if method in ['full', 'wallet'] and status == True:
        print("Start backup wallet ...")
        status = backupwallet(path)

    if method in ['full', 'privateKey'] and status == True:
        print("Start dump wallet keys ...")
        status = dumpWallet(path)
    
    if status == True :
        print("Start compress files ...")
        status = zipKeep(path)

    if status == True :
        print("Start FTP stuff ...")
        status = sendByFTP(path)

    if status == False :
        print("An Error has occurred  : [errCode = -1]")
        sys.exit(2)
    print("Job Done. :)")
    sys.exit(2)
    
    

def backupwallet(path):
    global rpcUser, rpcPassword
    path = path + "/wallet.back.dat"
    command = "bitcoin-cli -rpcuser={0} -rpcpassword={1} backupwallet {2}".format(rpcUser , rpcPassword, path)
    try:
        args = shlex.split(command)
        process = Popen(args, stdout=PIPE)
        stdout = process.communicate()
        print(stdout)
    except :
        return False
    return True

def dumpWallet(path):
    global rpcUser, rpcPassword
    path = path + "/dump.wallet"
    command = "bitcoin-cli -rpcuser={0} -rpcpassword={1} dumpwallet {2}".format(rpcUser , rpcPassword, path)
    try:
        args = shlex.split(command)
        process = Popen(args, stdout=PIPE)
        stdout = process.communicate()
        print(stdout)
    except :
        return False
    return True

def zipKeep(path):
    command="zip -9 -r -j -e -P {0} {1} {2}".format(key, path+'.zip', path)
    try:
        args = shlex.split(command)
        process = Popen(args, stdout=PIPE)
        stdout = process.communicate()
        print(stdout)
        shutil.rmtree(path)
    except :
        return False
    return True

def sendByFTP(path):
    global ftpEnable
    if ftpEnable == False:
        return True
    global ftpServer, ftpUser, ftpPass , ftpPath
    try:
        filepath = path+'.zip'
        basename = os.path.basename(filepath)
        session = ftplib.FTP(ftpServer,ftpUser,ftpPass)
        session.cwd(ftpPath)
        file = open(filepath,'rb')# file to send
        session.storbinary('STOR '+basename, file)     # send the file
        file.close()                                    # close file and FTP
        session.quit()
    except :
        print('Ftp occurred an error')
        return False
    return True

if __name__ == "__main__":
    main(sys.argv[1:])
