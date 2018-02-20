#!/usr/bin/python
import subprocess
class CheckVols(object):
    def __init__(self):
        self.retrieve_mount_points()
        print self.calc_md5sum()


    def retrieve_mount_points(self): # exclude the device(s) used for the root files system "/" and /boot..etc
        self.mps = subprocess.Popen("df -h | grep /dev/mapper | awk '{print $NF}'", shell=True, stdout=subprocess.PIPE).communicate()[0]
        self.mps = self.mps.strip().split('\n')



    def calc_md5sum(self):
        md5sum = [subprocess.Popen("md5sum {0}/*".format(x), shell=True, stdout=subprocess.PIPE).communicate()[0] for x in self.mps] # at this phase, only one file is written in each mounted volume
        md5sum = [x.split() for x in md5sum]
        return [x[0] for x in md5sum]


if __name__ == "__main__":
    CheckVols()