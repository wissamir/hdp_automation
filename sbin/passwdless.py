#!/usr/bin/python
import pexpect
import sys
import os

ssh_newkey = 'Are you sure you want to continue connecting'
SSH = 'ssh '
SCP = 'scp '
CAT = 'cat '
RM = 'rm -rf '
#ToDo
# 1. make a class
# 2. create _main_ function
# 3. create _init_ function to instantiate the class and all other constants
# 4. user try/catch - wrap pexpect exceptions with your ones! and handle different errors for example requiring to create a passwordless for a non-existing user! (with pexpect exceptions you got an error on timeout with further explanations)
# 5. child.expect(pexpect.EOF) e' importante per portare a buon fine il comando
# 6. print child.before - solo se si vuole tracciare l'output dei comandi.. si puo' eliminare
if len(sys.argv) != 4:
   print "usage: createPasswordless <user> <password> <machines file>"
   print "machines file must list all machines in group one per line"
   sys.exit(1)

USER = sys.argv[1] 
PASSWORD = sys.argv[2]
filePath = sys.argv[3]
machinesFile = open(filePath,"r") 
machines = machinesFile.readlines() 

#preparing commands
#COMMAND1 is for deleting previously created kesy to avoid handling the overwriting questions
if (USER == 'root'): 
    COMMAND1 = ' rm -rf /root/.ssh/id_rsa*'
    PATH1 = ':/root/.ssh/'
else:
    COMMAND1 = ' rm -rf /home/'+USER+'/.ssh/id_rsa*'
    PATH1 = ':/home/'+USER+'/.ssh/'

KEY = PATH1+'id_rsa.pub'
PATH2 = ' /tmp/id_rsa'
KEYS = ' /tmp/authorized_keys'

COMMAND2 = ' ssh-keygen -t rsa'


for i in range(len(machines)):
      # clearing line feeds read from input file
      machines[i] = machines[i].rstrip('\n') 
      #print "i = " + str(i)
      #print "USER = "+USER
      #print "PASSWORD = "+PASSWORD
      #print "machines[i] = "+machines[i]
      child = pexpect.spawn(SSH+USER+'@'+machines[i]+COMMAND1)
      j = child.expect([ssh_newkey,'password:','Password:',pexpect.EOF])
      #print "responseeeeeeeee = " + str(response)
      if j == 0:
         child.sendline('yes')
         #i = child.expect([ssh_newkey,'password:','Password:',pexpect.EOF]) 
         j = child.expect([ssh_newkey,'password:','Password:',pexpect.EOF]) 
      if j == 1 or j == 2:
         child.sendline(PASSWORD)
         child.expect(pexpect.EOF)
         #print child.before
      if j == 3:
         print "error encounterd..check connections to machine " + machines[i]
         print "trying to continue without " + machines[i]
#print child.before

for i in range(len(machines)):
      child = pexpect.spawn(SSH+USER+'@'+machines[i]+COMMAND2)
      #child.expect('password')
      j = child.expect(['password','Password:'])
      if j == 0 or j == 1:
         child.sendline(PASSWORD)
         child.expect("Enter .*: ")
         child.sendline('\r')
         child.expect("Enter .*: ")
         child.sendline('\r')
         child.expect("Enter .*: ")
         child.sendline('\r')
         child.expect(pexpect.EOF)
         print child.before

os.popen(RM + KEYS)
for i in range(len(machines)):
      child = pexpect.spawn(SCP+USER+'@'+machines[i]+KEY+PATH2+str(i))
      #print "command is: " + SCP+USER+'@'+machines[i]+KEY+PATH2+str(i)
#      child.expect('password:')
#      child.expect('Password:')
      j = child.expect(['password','Password:'])
      if j == 0 or j == 1:
         child.sendline(PASSWORD)
         child.expect(pexpect.EOF)
         os.popen(CAT + PATH2 + str(i) + ">> " + KEYS)
         print child.before

for i in range(len(machines)):
      child = pexpect.spawn(SCP + KEYS + " " + USER+'@'+machines[i]+PATH1)
#      child.expect('password:')
#      child.expect('Password:')
      j = child.expect(['password','Password:'])
      if j == 0 or j == 1:
        child.sendline(PASSWORD)
        child.expect(pexpect.EOF)
        print child.before

os.popen(RM + KEYS)
os.popen(RM + PATH2 + '*')
