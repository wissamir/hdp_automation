#!/usr/bin/python
import re
import json
import subprocess

# return a json from each node about its own mapping
# but hwo to unify all returned output in the main playbook?... need to manipulate the returned output


class Mapper(object):
    def __init__(self):
        self.os_device = self.retrieve_os_device()
        self.host_name = self.retrieve_host_name()
        self.map_list = self.set_map_list()
        self.map_dic = self.set_map_dic()

    def retrieve_os_device(self): # exclude the device(s) used for the root files system "/" and /boot..etc
        df = subprocess.Popen('df -h', shell=True, stdout=subprocess.PIPE).communicate()[0]
        df = df.strip().split('\n')
        reg = re.compile("\/\Z|\/boot\Z") # matching lines that either ends with "/" or "/boot"
        df = [x for x in df if reg.findall(x) != []]
        assert df != [] # information about root file system must be founded! if len(df) == 2 that means that /boot is on its dedicated partition
        return [x.split()[0][:-1] for x in df]  # extract basic device name "such /dev/sdbq" by removing partition number and other partition info


    def retrieve_host_name(self):
        return subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE).communicate()[0].strip()


    def set_map_list(self): # map scsi id to device names .. do it presuming multipath is installed.. so analyze the multipath -ll output
               # rather than lssci -i output (longer way)... you can presume multipath is there and works
        scsiid_re = re.compile("\(.*\)")
        device_re = re.compile('sd.*\s+')
        mpath_re = re.compile('mpath')
        multipaths = subprocess.Popen('multipath -ll', shell=True, stdout=subprocess.PIPE).communicate()[0]
        devices = mpath_re.findall(multipaths)
        # The following assertions are necessary checks in order to insure correct text processing at the end of this method
        assert devices != []
        # Following assertion should be true before defining the blacklists
        # assert len(devices) == 34 #find a way to give this as an input const

        # expect device names to be in their original form, i.e. without aliasing
        # i.e. something like "mpathk (35000cca01a4e7360) dm-6 HITACHI ,HUS723030ALS640"
        # rather than "alias-name (35000cca01a4e7360) dm-6 HITACHI ,HUS723030ALS640"
        multipaths = multipaths.split('mpath')
        for x in multipaths:
            if x.strip().split() != []:
                devices = device_re.findall(x)
                assert (devices != [] and len(devices) == 2 and scsiid_re.findall(x) != [])  # two traditional device names should be mapped to this device mapper name

        '''
            scsiid_re.findall(x)[0][1:-1] - to retrieve scsi_id such "(35000c50062815bb3)" removing the parentheses
            "mpath" + x.split()[0] to reconstruct device mapper device name (mpathr, mpathe, mpathq, mpathah..etc)
            [y.split()[0] for y in device_re.findall(x)] - to match os device names, remove unnecessary info keeping only device name (by split()[0])
        '''
        multipaths = [[scsiid_re.findall(x)[0][1:-1], "mpath" + x.split()[0], [y.split()[0] for y in device_re.findall(x)]] for x in
         multipaths if x.strip().split() != []]
        # The following assertion should be true before defining the blacklists
        # assert len(multipaths) == 34
        return multipaths


    def set_map_dic(self):
        d = dict()
        for x in self.map_list:
            d[x[0]] = {self.host_name: x[1:]}
        return d

    def get_map_list(self):
        return self.map_list

    def get_map_dic(self):
        return self.map_dic

    def get_map_json(self):
        return json.dumps(self.map_dic)

'''
from opnstk3
>>> print multipaths
[['35000c50062815bb3', 'mpathr', ['sdv', 'sdbd']], ['35000c5007f578bd7', 'mpathe', ['sdq', 'sday']], ['35000c50062815d6f', 'mpathq', ['sdu', 'sdbc']], ['35000cca01a9ae9b4', 'mpathd', ['sdp', 'sdax']], ['35000c50063735907', 'mpathp', ['sdn', 'sdav']], ['35000cca01a9a9c18', 'mpathc', ['sdo', 'sdaw']], ['35000cca01a4deb00', 'mpathah', ['sde', 'sdal']], ['35000cca01a3f71d0', 'mpatho', ['sdm', 'sdau']], ['35000cca01a4deafc', 'mpathb', ['sdf', 'sdam']], ['35000cca01a4df76c', 'mpathag', ['sdd', 'sdak']], ['35000cca01a9aec88', 'mpathn', ['sdl', 'sdat']], ['35000cca01a9ae97c', 'mpatha', ['sda', 'sdao']], ['35000cca01a4dfad4', 'mpathz', ['sdz', 'sdbh']], ['35000cca01a9a6584', 'mpathaf', ['sdc', 'sdaj']], ['35000cca01a9a9c3c', 'mpathm', ['sdk', 'sdas']], ['35000c50062806a63', 'mpathy', ['sdy', 'sdbg']], ['35000cca01a9a2260', 'mpathae', ['sdb', 'sdai']], ['35000cca01a4dfad0', 'mpathl', ['sdj', 'sdar']], ['35000cca01a4e89c4', 'mpathx', ['sdx', 'sdbf']], ['35000cca01a4debc0', 'mpathad', ['sdad', 'sdbl']], ['35000cca01a4e7360', 'mpathk', ['sdi', 'sdaq']], ['35000cca01a9a2c44', 'mpathw', ['sdw', 'sdbe']], ['35000cca01a4dfa38', 'mpathac', ['sdac', 'sdbk']], ['35000cca01a9acc7c', 'mpathj', ['sdh', 'sdap']], ['35000cca01a9a1a00', 'mpathv', ['sdah', 'sdbp']], ['35000c50062806bbb', 'mpathab', ['sdab', 'sdbj']], ['35000cca01a4e86b0', 'mpathi', ['sdg', 'sdan']], ['35000cca01a4e72b8', 'mpathu', ['sdag', 'sdbo']], ['35000cca01a4dcf2c', 'mpathaa', ['sdaa', 'sdbi']], ['35000c50062800e7b', 'mpathh', ['sdt', 'sdbb']], ['35000cca01a9acc80', 'mpatht', ['sdaf', 'sdbn']], ['35000cca01a4dfae4', 'mpathg', ['sds', 'sdba']], ['35000cca01a4e875c', 'mpaths', ['sdae', 'sdbm']], ['35000cca01a4e7710', 'mpathf', ['sdr', 'sdaz']]]
>>> print multipaths[10]
['35000cca01a9aec88', 'mpathn', ['sdl', 'sdat']]
>>> m1 = multipaths
# bringing the other lists from opnstk4, opnstk5, opnstk6 machines and unifying everything in one dictionary of the structure:


		{uuid1:
		    {node1: [/dev/yyy, /dev/xxx]
		     node2: [....]
		     node3: [....]
		     node4: [....]
		   },
		uuid2:
		    {node1: [/dev/yyy, /dev/xxx]
		     node2: [....]
		     node3: [....]
		     node4: [....]
		   },
		...
		...
		...
		}


>>> m2 = [['35000c50062815bb3', 'mpathr', ['sdab', 'sdal']], ['35000c5007f578bd7', 'mpathe', ['sdu', 'sdj']], ['35000c50062815d6f', 'mpathq', ['sdz', 'sdag']], ['35000cca01a9ae9b4', 'mpathd', ['sdt', 'sdd']], ['35000c50063735907', 'mpathp', ['sdr', 'sdbh']], ['35000cca01a9a9c18', 'mpathc', ['sds', 'sdbi']], ['35000cca01a4deb00', 'mpathah', ['sdg', 'sdau']], ['35000cca01a3f71d0', 'mpatho', ['sdq', 'sdbf']], ['35000cca01a4deafc', 'mpathb', ['sdh', 'sdaw']], ['35000cca01a4df76c', 'mpathag', ['sdf', 'sdat']], ['35000cca01a9aec88', 'mpathn', ['sdo', 'sdbe']], ['35000cca01a9ae97c', 'mpatha', ['sdb', 'sday']], ['35000cca01a4dfad4', 'mpathz', ['sdaf', 'sdbg']], ['35000cca01a9a6584', 'mpathaf', ['sde', 'sdas']], ['35000cca01a9a9c3c', 'mpathm', ['sdn', 'sdbd']], ['35000c50062806a63', 'mpathy', ['sdae', 'sdba']], ['35000cca01a9a2260', 'mpathae', ['sdc', 'sdar']], ['35000cca01a4dfad0', 'mpathl', ['sdm', 'sdbc']], ['35000cca01a4e89c4', 'mpathx', ['sdad', 'sdav']], ['35000cca01a4debc0', 'mpathad', ['sdak', 'sdbm']], ['35000cca01a4e7360', 'mpathk', ['sdl', 'sdbb']], ['35000cca01a9a2c44', 'mpathw', ['sdac', 'sdaq']], ['35000cca01a4dfa38', 'mpathac', ['sdaj', 'sdbl']], ['35000cca01a9acc7c', 'mpathj', ['sdk', 'sdaz']], ['35000cca01a9a1a00', 'mpathv', ['sdap', 'sdbq']], ['35000c50062806bbb', 'mpathab', ['sdai', 'sdbk']], ['35000cca01a4e86b0', 'mpathi', ['sdi', 'sdax']], ['35000cca01a4e72b8', 'mpathu', ['sdao', 'sdbp']], ['35000cca01a4dcf2c', 'mpathaa', ['sdah', 'sdbj']], ['35000c50062800e7b', 'mpathh', ['sdy', 'sdaa']], ['35000cca01a9acc80', 'mpatht', ['sdan', 'sdbo']], ['35000cca01a4dfae4', 'mpathg', ['sdx', 'sdv']], ['35000cca01a4e875c', 'mpaths', ['sdam', 'sdbn']], ['35000cca01a4e7710', 'mpathf', ['sdw', 'sdp']]]
>>> m3 = [['35000c50062815bb3', 'mpathr', ['sdbe', 'sdw']], ['35000c5007f578bd7', 'mpathe', ['sdr', 'sdaz']], ['35000c50062815d6f', 'mpathq', ['sdv', 'sdbd']], ['35000cca01a9ae9b4', 'mpathd', ['sdq', 'sday']], ['35000c50063735907', 'mpathp', ['sdo', 'sdaw']], ['35000cca01a9a9c18', 'mpathc', ['sdp', 'sdax']], ['35000cca01a3f71d0', 'mpatho', ['sdn', 'sdav']], ['35000cca01a4deb00', 'mpathah', ['sdf', 'sdam']], ['35000cca01a4deafc', 'mpathb', ['sdg', 'sdan']], ['35000cca01a9aec88', 'mpathn', ['sdm', 'sdau']], ['35000cca01a4df76c', 'mpathag', ['sde', 'sdal']], ['35000cca01a9ae97c', 'mpatha', ['sdb', 'sdap']], ['35000cca01a4dfad4', 'mpathz', ['sdaa', 'sdbi']], ['35000cca01a9a9c3c', 'mpathm', ['sdl', 'sdat']], ['35000cca01a9a6584', 'mpathaf', ['sdd', 'sdak']], ['35000c50062806a63', 'mpathy', ['sdbh', 'sdz']], ['35000cca01a4dfad0', 'mpathl', ['sdk', 'sdas']], ['35000cca01a9a2260', 'mpathae', ['sdc', 'sdaj']], ['35000cca01a4e89c4', 'mpathx', ['sdbg', 'sdy']], ['35000cca01a4debc0', 'mpathad', ['sdae', 'sdbm']], ['35000cca01a4e7360', 'mpathk', ['sdj', 'sdar']], ['35000cca01a9a2c44', 'mpathw', ['sdbf', 'sdx']], ['35000cca01a4dfa38', 'mpathac', ['sdad', 'sdbl']], ['35000cca01a9acc7c', 'mpathj', ['sdi', 'sdaq']], ['35000cca01a9a1a00', 'mpathv', ['sdai', 'sdbq']], ['35000c50062806bbb', 'mpathab', ['sdac', 'sdbk']], ['35000cca01a4e86b0', 'mpathi', ['sdh', 'sdao']], ['35000cca01a4e72b8', 'mpathu', ['sdah', 'sdbp']], ['35000cca01a4dcf2c', 'mpathaa', ['sdab', 'sdbj']], ['35000c50062800e7b', 'mpathh', ['sdu', 'sdbc']], ['35000cca01a9acc80', 'mpatht', ['sdag', 'sdbo']], ['35000cca01a4dfae4', 'mpathg', ['sdt', 'sdbb']], ['35000cca01a4e875c', 'mpaths', ['sdaf', 'sdbn']], ['35000cca01a4e7710', 'mpathf', ['sds', 'sdba']]]
>>> m4 = [['35000c50062815bb3', 'mpathr', ['sdv', 'sdbd']], ['35000c5007f578bd7', 'mpathe', ['sdq', 'sday']], ['35000c50062815d6f', 'mpathq', ['sdu', 'sdbc']], ['35000cca01a9ae9b4', 'mpathd', ['sdp', 'sdax']], ['35000c50063735907', 'mpathp', ['sdn', 'sdav']], ['35000cca01a9a9c18', 'mpathc', ['sdo', 'sdaw']], ['35000cca01a4deb00', 'mpathah', ['sde', 'sdal']], ['35000cca01a3f71d0', 'mpatho', ['sdm', 'sdau']], ['35000cca01a4deafc', 'mpathb', ['sdf', 'sdam']], ['35000cca01a4df76c', 'mpathag', ['sdd', 'sdak']], ['35000cca01a9aec88', 'mpathn', ['sdl', 'sdat']], ['35000cca01a9ae97c', 'mpatha', ['sda', 'sdao']], ['35000cca01a4dfad4', 'mpathz', ['sdz', 'sdbh']], ['35000cca01a9a6584', 'mpathaf', ['sdc', 'sdaj']], ['35000cca01a9a9c3c', 'mpathm', ['sdk', 'sdas']], ['35000c50062806a63', 'mpathy', ['sdy', 'sdbg']], ['35000cca01a9a2260', 'mpathae', ['sdb', 'sdai']], ['35000cca01a4dfad0', 'mpathl', ['sdj', 'sdar']], ['35000cca01a4e89c4', 'mpathx', ['sdx', 'sdbf']], ['35000cca01a4debc0', 'mpathad', ['sdad', 'sdbl']], ['35000cca01a4e7360', 'mpathk', ['sdi', 'sdaq']], ['35000cca01a9a2c44', 'mpathw', ['sdw', 'sdbe']], ['35000cca01a4dfa38', 'mpathac', ['sdac', 'sdbk']], ['35000cca01a9acc7c', 'mpathj', ['sdh', 'sdap']], ['35000cca01a9a1a00', 'mpathv', ['sdah', 'sdbp']], ['35000c50062806bbb', 'mpathab', ['sdab', 'sdbj']], ['35000cca01a4e86b0', 'mpathi', ['sdg', 'sdan']], ['35000cca01a4e72b8', 'mpathu', ['sdag', 'sdbo']], ['35000cca01a4dcf2c', 'mpathaa', ['sdaa', 'sdbi']], ['35000c50062800e7b', 'mpathh', ['sdt', 'sdbb']], ['35000cca01a9acc80', 'mpatht', ['sdaf', 'sdbn']], ['35000cca01a4dfae4', 'mpathg', ['sds', 'sdba']], ['35000cca01a4e875c', 'mpaths', ['sdae', 'sdbm']], ['35000cca01a4e7710', 'mpathf', ['sdr', 'sdaz']]]
>>> d = dict()
>>> for x in m1:
...   d[x[0]] = {"opnstk1": x[2]}
...
>>> d
{'35000c50062815bb3': {'opnstk1': ['sdv', 'sdbd']}, '35000cca01a4e72b8': {'opnstk1': ['sdag', 'sdbo']}, '35000cca01a4e875c': {'opnstk1': ['sdae', 'sdbm']}, '35000c50062800e7b': {'opnstk1': ['sdt', 'sdbb']}, '35000cca01a4debc0': {'opnstk1': ['sdad', 'sdbl']}, '35000cca01a3f71d0': {'opnstk1': ['sdm', 'sdau']}, '35000cca01a4dfae4': {'opnstk1': ['sds', 'sdba']}, '35000c50062806bbb': {'opnstk1': ['sdab', 'sdbj']}, '35000cca01a9acc80': {'opnstk1': ['sdaf', 'sdbn']}, '35000cca01a4dcf2c': {'opnstk1': ['sdaa', 'sdbi']}, '35000c50062815d6f': {'opnstk1': ['sdu', 'sdbc']}, '35000cca01a4deafc': {'opnstk1': ['sdf', 'sdam']}, '35000cca01a4e86b0': {'opnstk1': ['sdg', 'sdan']}, '35000cca01a9acc7c': {'opnstk1': ['sdh', 'sdap']}, '35000cca01a9a9c18': {'opnstk1': ['sdo', 'sdaw']}, '35000cca01a9a1a00': {'opnstk1': ['sdah', 'sdbp']}, '35000cca01a9aec88': {'opnstk1': ['sdl', 'sdat']}, '35000cca01a4e7360': {'opnstk1': ['sdi', 'sdaq']}, '35000cca01a4e7710': {'opnstk1': ['sdr', 'sdaz']}, '35000cca01a4deb00': {'opnstk1': ['sde', 'sdal']}, '35000cca01a9ae9b4': {'opnstk1': ['sdp', 'sdax']}, '35000cca01a4dfad4': {'opnstk1': ['sdz', 'sdbh']}, '35000cca01a9a6584': {'opnstk1': ['sdc', 'sdaj']}, '35000cca01a4dfad0': {'opnstk1': ['sdj', 'sdar']}, '35000cca01a4e89c4': {'opnstk1': ['sdx', 'sdbf']}, '35000cca01a9a2260': {'opnstk1': ['sdb', 'sdai']}, '35000c5007f578bd7': {'opnstk1': ['sdq', 'sday']}, '35000c50062806a63': {'opnstk1': ['sdy', 'sdbg']}, '35000cca01a9ae97c': {'opnstk1': ['sda', 'sdao']}, '35000cca01a4dfa38': {'opnstk1': ['sdac', 'sdbk']}, '35000cca01a9a2c44': {'opnstk1': ['sdw', 'sdbe']}, '35000cca01a9a9c3c': {'opnstk1': ['sdk', 'sdas']}, '35000cca01a4df76c': {'opnstk1': ['sdd', 'sdak']}, '35000c50063735907': {'opnstk1': ['sdn', 'sdav']}}
>>> for x in m2:
...   d[x[0]]['opnstk2'] = x[2]
...
>>> d
{'35000c50062815bb3': {'opnstk2': ['sdab', 'sdal'], 'opnstk1': ['sdv', 'sdbd']}, '35000cca01a4e72b8': {'opnstk2': ['sdao', 'sdbp'], 'opnstk1': ['sdag', 'sdbo']}, '35000cca01a4e875c': {'opnstk2': ['sdam', 'sdbn'], 'opnstk1': ['sdae', 'sdbm']}, '35000c50062800e7b': {'opnstk2': ['sdy', 'sdaa'], 'opnstk1': ['sdt', 'sdbb']}, '35000cca01a4debc0': {'opnstk2': ['sdak', 'sdbm'], 'opnstk1': ['sdad', 'sdbl']}, '35000cca01a3f71d0': {'opnstk2': ['sdq', 'sdbf'], 'opnstk1': ['sdm', 'sdau']}, '35000cca01a4dfae4': {'opnstk2': ['sdx', 'sdv'], 'opnstk1': ['sds', 'sdba']}, '35000c50062806bbb': {'opnstk2': ['sdai', 'sdbk'], 'opnstk1': ['sdab', 'sdbj']}, '35000cca01a9acc80': {'opnstk2': ['sdan', 'sdbo'], 'opnstk1': ['sdaf', 'sdbn']}, '35000cca01a4dcf2c': {'opnstk2': ['sdah', 'sdbj'], 'opnstk1': ['sdaa', 'sdbi']}, '35000c50062815d6f': {'opnstk2': ['sdz', 'sdag'], 'opnstk1': ['sdu', 'sdbc']}, '35000cca01a4deafc': {'opnstk2': ['sdh', 'sdaw'], 'opnstk1': ['sdf', 'sdam']}, '35000cca01a4e86b0': {'opnstk2': ['sdi', 'sdax'], 'opnstk1': ['sdg', 'sdan']}, '35000cca01a9acc7c': {'opnstk2': ['sdk', 'sdaz'], 'opnstk1': ['sdh', 'sdap']}, '35000cca01a9a9c18': {'opnstk2': ['sds', 'sdbi'], 'opnstk1': ['sdo', 'sdaw']}, '35000cca01a9a1a00': {'opnstk2': ['sdap', 'sdbq'], 'opnstk1': ['sdah', 'sdbp']}, '35000cca01a9aec88': {'opnstk2': ['sdo', 'sdbe'], 'opnstk1': ['sdl', 'sdat']}, '35000cca01a4e7360': {'opnstk2': ['sdl', 'sdbb'], 'opnstk1': ['sdi', 'sdaq']}, '35000cca01a4e7710': {'opnstk2': ['sdw', 'sdp'], 'opnstk1': ['sdr', 'sdaz']}, '35000cca01a4deb00': {'opnstk2': ['sdg', 'sdau'], 'opnstk1': ['sde', 'sdal']}, '35000cca01a9ae9b4': {'opnstk2': ['sdt', 'sdd'], 'opnstk1': ['sdp', 'sdax']}, '35000cca01a4dfad4': {'opnstk2': ['sdaf', 'sdbg'], 'opnstk1': ['sdz', 'sdbh']}, '35000cca01a9a6584': {'opnstk2': ['sde', 'sdas'], 'opnstk1': ['sdc', 'sdaj']}, '35000cca01a4dfad0': {'opnstk2': ['sdm', 'sdbc'], 'opnstk1': ['sdj', 'sdar']}, '35000cca01a4e89c4': {'opnstk2': ['sdad', 'sdav'], 'opnstk1': ['sdx', 'sdbf']}, '35000cca01a9a2260': {'opnstk2': ['sdc', 'sdar'], 'opnstk1': ['sdb', 'sdai']}, '35000c5007f578bd7': {'opnstk2': ['sdu', 'sdj'], 'opnstk1': ['sdq', 'sday']}, '35000c50062806a63': {'opnstk2': ['sdae', 'sdba'], 'opnstk1': ['sdy', 'sdbg']}, '35000cca01a9ae97c': {'opnstk2': ['sdb', 'sday'], 'opnstk1': ['sda', 'sdao']}, '35000cca01a4dfa38': {'opnstk2': ['sdaj', 'sdbl'], 'opnstk1': ['sdac', 'sdbk']}, '35000cca01a9a2c44': {'opnstk2': ['sdac', 'sdaq'], 'opnstk1': ['sdw', 'sdbe']}, '35000cca01a9a9c3c': {'opnstk2': ['sdn', 'sdbd'], 'opnstk1': ['sdk', 'sdas']}, '35000cca01a4df76c': {'opnstk2': ['sdf', 'sdat'], 'opnstk1': ['sdd', 'sdak']}, '35000c50063735907': {'opnstk2': ['sdr', 'sdbh'], 'opnstk1': ['sdn', 'sdav']}}
>>> for x in m3:
...   d[x[0]]['opnstk3'] = x[2]
...
>>> for x in m4:
...   d[x[0]]['opnstk4'] = x[2]
...
>>> d
{'35000c50062815bb3': {'opnstk2': ['sdab', 'sdal'], 'opnstk3': ['sdbe', 'sdw'], 'opnstk1': ['sdv', 'sdbd'], 'opnstk4': ['sdv', 'sdbd']}, '35000cca01a4e72b8': {'opnstk2': ['sdao', 'sdbp'], 'opnstk3': ['sdah', 'sdbp'], 'opnstk1': ['sdag', 'sdbo'], 'opnstk4': ['sdag', 'sdbo']}, '35000cca01a4e875c': {'opnstk2': ['sdam', 'sdbn'], 'opnstk3': ['sdaf', 'sdbn'], 'opnstk1': ['sdae', 'sdbm'], 'opnstk4': ['sdae', 'sdbm']}, '35000c50062800e7b': {'opnstk2': ['sdy', 'sdaa'], 'opnstk3': ['sdu', 'sdbc'], 'opnstk1': ['sdt', 'sdbb'], 'opnstk4': ['sdt', 'sdbb']}, '35000cca01a4debc0': {'opnstk2': ['sdak', 'sdbm'], 'opnstk3': ['sdae', 'sdbm'], 'opnstk1': ['sdad', 'sdbl'], 'opnstk4': ['sdad', 'sdbl']}, '35000cca01a3f71d0': {'opnstk2': ['sdq', 'sdbf'], 'opnstk3': ['sdn', 'sdav'], 'opnstk1': ['sdm', 'sdau'], 'opnstk4': ['sdm', 'sdau']}, '35000cca01a4dfae4': {'opnstk2': ['sdx', 'sdv'], 'opnstk3': ['sdt', 'sdbb'], 'opnstk1': ['sds', 'sdba'], 'opnstk4': ['sds', 'sdba']}, '35000c50062806bbb': {'opnstk2': ['sdai', 'sdbk'], 'opnstk3': ['sdac', 'sdbk'], 'opnstk1': ['sdab', 'sdbj'], 'opnstk4': ['sdab', 'sdbj']}, '35000cca01a9acc80': {'opnstk2': ['sdan', 'sdbo'], 'opnstk3': ['sdag', 'sdbo'], 'opnstk1': ['sdaf', 'sdbn'], 'opnstk4': ['sdaf', 'sdbn']}, '35000cca01a4dcf2c': {'opnstk2': ['sdah', 'sdbj'], 'opnstk3': ['sdab', 'sdbj'], 'opnstk1': ['sdaa', 'sdbi'], 'opnstk4': ['sdaa', 'sdbi']}, '35000c50062815d6f': {'opnstk2': ['sdz', 'sdag'], 'opnstk3': ['sdv', 'sdbd'], 'opnstk1': ['sdu', 'sdbc'], 'opnstk4': ['sdu', 'sdbc']}, '35000cca01a4deafc': {'opnstk2': ['sdh', 'sdaw'], 'opnstk3': ['sdg', 'sdan'], 'opnstk1': ['sdf', 'sdam'], 'opnstk4': ['sdf', 'sdam']}, '35000cca01a4e86b0': {'opnstk2': ['sdi', 'sdax'], 'opnstk3': ['sdh', 'sdao'], 'opnstk1': ['sdg', 'sdan'], 'opnstk4': ['sdg', 'sdan']}, '35000cca01a9acc7c': {'opnstk2': ['sdk', 'sdaz'], 'opnstk3': ['sdi', 'sdaq'], 'opnstk1': ['sdh', 'sdap'], 'opnstk4': ['sdh', 'sdap']}, '35000cca01a9a9c18': {'opnstk2': ['sds', 'sdbi'], 'opnstk3': ['sdp', 'sdax'], 'opnstk1': ['sdo', 'sdaw'], 'opnstk4': ['sdo', 'sdaw']}, '35000cca01a9a1a00': {'opnstk2': ['sdap', 'sdbq'], 'opnstk3': ['sdai', 'sdbq'], 'opnstk1': ['sdah', 'sdbp'], 'opnstk4': ['sdah', 'sdbp']}, '35000cca01a9aec88': {'opnstk2': ['sdo', 'sdbe'], 'opnstk3': ['sdm', 'sdau'], 'opnstk1': ['sdl', 'sdat'], 'opnstk4': ['sdl', 'sdat']}, '35000cca01a4e7360': {'opnstk2': ['sdl', 'sdbb'], 'opnstk3': ['sdj', 'sdar'], 'opnstk1': ['sdi', 'sdaq'], 'opnstk4': ['sdi', 'sdaq']}, '35000cca01a4e7710': {'opnstk2': ['sdw', 'sdp'], 'opnstk3': ['sds', 'sdba'], 'opnstk1': ['sdr', 'sdaz'], 'opnstk4': ['sdr', 'sdaz']}, '35000cca01a4deb00': {'opnstk2': ['sdg', 'sdau'], 'opnstk3': ['sdf', 'sdam'], 'opnstk1': ['sde', 'sdal'], 'opnstk4': ['sde', 'sdal']}, '35000cca01a9ae9b4': {'opnstk2': ['sdt', 'sdd'], 'opnstk3': ['sdq', 'sday'], 'opnstk1': ['sdp', 'sdax'], 'opnstk4': ['sdp', 'sdax']}, '35000cca01a4dfad4': {'opnstk2': ['sdaf', 'sdbg'], 'opnstk3': ['sdaa', 'sdbi'], 'opnstk1': ['sdz', 'sdbh'], 'opnstk4': ['sdz', 'sdbh']}, '35000cca01a9a6584': {'opnstk2': ['sde', 'sdas'], 'opnstk3': ['sdd', 'sdak'], 'opnstk1': ['sdc', 'sdaj'], 'opnstk4': ['sdc', 'sdaj']}, '35000cca01a4dfad0': {'opnstk2': ['sdm', 'sdbc'], 'opnstk3': ['sdk', 'sdas'], 'opnstk1': ['sdj', 'sdar'], 'opnstk4': ['sdj', 'sdar']}, '35000cca01a4e89c4': {'opnstk2': ['sdad', 'sdav'], 'opnstk3': ['sdbg', 'sdy'], 'opnstk1': ['sdx', 'sdbf'], 'opnstk4': ['sdx', 'sdbf']}, '35000cca01a9a2260': {'opnstk2': ['sdc', 'sdar'], 'opnstk3': ['sdc', 'sdaj'], 'opnstk1': ['sdb', 'sdai'], 'opnstk4': ['sdb', 'sdai']}, '35000c5007f578bd7': {'opnstk2': ['sdu', 'sdj'], 'opnstk3': ['sdr', 'sdaz'], 'opnstk1': ['sdq', 'sday'], 'opnstk4': ['sdq', 'sday']}, '35000c50062806a63': {'opnstk2': ['sdae', 'sdba'], 'opnstk3': ['sdbh', 'sdz'], 'opnstk1': ['sdy', 'sdbg'], 'opnstk4': ['sdy', 'sdbg']}, '35000cca01a9ae97c': {'opnstk2': ['sdb', 'sday'], 'opnstk3': ['sdb', 'sdap'], 'opnstk1': ['sda', 'sdao'], 'opnstk4': ['sda', 'sdao']}, '35000cca01a4dfa38': {'opnstk2': ['sdaj', 'sdbl'], 'opnstk3': ['sdad', 'sdbl'], 'opnstk1': ['sdac', 'sdbk'], 'opnstk4': ['sdac', 'sdbk']}, '35000cca01a9a2c44': {'opnstk2': ['sdac', 'sdaq'], 'opnstk3': ['sdbf', 'sdx'], 'opnstk1': ['sdw', 'sdbe'], 'opnstk4': ['sdw', 'sdbe']}, '35000cca01a9a9c3c': {'opnstk2': ['sdn', 'sdbd'], 'opnstk3': ['sdl', 'sdat'], 'opnstk1': ['sdk', 'sdas'], 'opnstk4': ['sdk', 'sdas']}, '35000cca01a4df76c': {'opnstk2': ['sdf', 'sdat'], 'opnstk3': ['sde', 'sdal'], 'opnstk1': ['sdd', 'sdak'], 'opnstk4': ['sdd', 'sdak']}, '35000c50063735907': {'opnstk2': ['sdr', 'sdbh'], 'opnstk3': ['sdo', 'sdaw'], 'opnstk1': ['sdn', 'sdav'], 'opnstk4': ['sdn', 'sdav']}}
>>> d.keys()
['35000c50062815bb3', '35000cca01a4e72b8', '35000cca01a4e875c', '35000c50062800e7b', '35000cca01a4debc0', '35000cca01a3f71d0', '35000cca01a4dfae4', '35000c50062806bbb', '35000cca01a9acc80', '35000cca01a4dcf2c', '35000c50062815d6f', '35000cca01a4deafc', '35000cca01a4e86b0', '35000cca01a9acc7c', '35000cca01a9a9c18', '35000cca01a9a1a00', '35000cca01a9aec88', '35000cca01a4e7360', '35000cca01a4e7710', '35000cca01a4deb00', '35000cca01a9ae9b4', '35000cca01a4dfad4', '35000cca01a9a6584', '35000cca01a4dfad0', '35000cca01a4e89c4', '35000cca01a9a2260', '35000c5007f578bd7', '35000c50062806a63', '35000cca01a9ae97c', '35000cca01a4dfa38', '35000cca01a9a2c44', '35000cca01a9a9c3c', '35000cca01a4df76c', '35000c50063735907']
>>> len(d.keys())
34

'''
























'''
per il TdC
il discorso delle blacklist pare funzionare...  qualche dubbio ancora sulla gestione delle partizioni per come vengono
viste dal device mapper.. e questo mi lo chiarisco con Simone
sto anche automatizzando la creazione delle blacklist nei vari nodi con un numero configurabile a piacimento dei dischi
per ciascun nodo.. cosa essenziale per prove con HDP.. e questo automatismo consintera pure di testare al 100% tutti i device mappaer
e tutti i mount point e accertare ceh le blacklist siano corrette.. che non ci sia una sovrapposizione
 - per il momento blacklist semplici statici e montando alcuni (non tutti) i device a mano in 2 dei nodi, pare funzionare.. quindi
 testato solo parzialmente

'''

if __name__ == "__main__":
    # Note that it is not sufficient to call the target method (Mapper().get_map_dic()), but need also to output it to standard output (print Mapper().get_map_dic())
    # in order to be able from the ansible controller machine to capture the output
    # What you still need to understand is Local Facts! in https://www.safaribooksonline.com/library/view/ansible-up-and/9781491915318/ch04.html
    # they state that one way to fix local facts is through An executable that takes no arguments and outputs JSON on standard out
    # which lets think that from the ansible playbook side you do not need to register the output in order to get the new facts
    #  You tried it.. (i.e just to print Mapper().get_map_json() here without registering the fact from the ansible playbook)
    # but you did not get the new facts! So, anyway it seems to you you have to register the fact yourself!
    # print Mapper().get_map_list()
    print Mapper().get_map_dic()
    # print Mapper().get_map_json()

    # If you want to get rid from the print and just return values and get them recognized as ansible facts, the way to go
    # seems to be is to transform this script into ansible module, then to return a dictionary that contains ansible_facts
    # as a key! see https://www.safaribooksonline.com/library/view/ansible-up-and/9781491915318/ch04.html#setup_module_output
    # Any Module Can Return Facts.. ansible facts in the return value is an ansible idiom! if a module returns a dictionary that contains
    # ansible_facts as a key, then ansible will create a variable names in the environment with thous values and associate
    # them with the active host.. for modules that return facts, there is no need to register variables, since ansible will
    # create these variables for you automatically