import paramiko
import tarfile,os,sys

host = 'ec2-54-152-135-221.compute-1.amazonaws.com'
path_me = r'C:\Users\Pan\Google Drive\Study\kaggle\revelent\aws'
#path_me = os.path.dirname(os.path.realpath(sys.argv[0]))

class psh():
    def __init__(self, host,ssh =None, username = 'ubuntu'):
        if ssh ==None:
            self.ssh=paramiko.SSHClient()
        else:
            self.ssh = ssh
        self.pkeypair = 'd:\data\keywin.pem'
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=username, password='passwd',key_filename = self.pkeypair)
    def cmd(self, ccmd):
        #will stuck when stdin
        stdin, stdout, stderr = self.ssh.exec_command(ccmd)
        try:
            print stderr.readlines()
        except Exception:
            pass
        print stdout.readlines()
    def putfolder(self,source,name,target):
        #source dir, source name, target dir w/o name
        tar = tarfile.open("temp.tar.gz", "w:gz")
        tar.add(source+r'/'+name, arcname=name)
        tar.close()
        sftp = self.ssh.open_sftp()
        sftp.put(source+r'/temp.tar.gz',target+'/temp.tar.gz') 
        self.cmd('sudo tar -C ' + target + ' -xzf '+target+'/temp.tar.gz')
    def getfolder(self,source, name, target):
        self.cmd('sudo tar cjf '+source +'/temp1.tar.gz -C '+source+'/'+name+ ' .')
        sftp = self.ssh.open_sftp()
        sftp.get(source+r'/temp1.tar.gz',target+'/temp1.tar.gz')        
        tar = tarfile.open(target+"/temp1.tar.gz", "r")
        tar.extractall(target+'/'+name)
    def close():
        pass

ps1 = psh(host)
ps1.cmd('mkdir -p data')
ps1.cmd('mkdir -p script')
#ps1.putfolder(path_me,'data','/home/ubuntu')
ps1.getfolder('/home/ubuntu','data',path_me)
'''
psh.put(pdata + '', data)
psh.put(pdata + '', script)
'''