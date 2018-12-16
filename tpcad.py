### tpcad.py
#
# Update TPC News Address
#
# 1997.02.09  Jim Tittsler Jim.Tittsler@tokyopc.bbs.net
#

import os
import regex
from httplib import HTTP

hostname = "www.dtinet.or.jp"
url = "/~tpc/address.htm"

print "TPC News Address Updater   1997.02.10 23:20JST  7j1ajh@amsat.org"
print "Making connection to http://%s%s..." % (hostname,url)
h = HTTP(hostname)
h.putrequest('GET', url)
h.putheader('Accept', 'text/html')
h.putheader('Accept', 'text/plain')
h.endheaders()
errcode, errmsg, headers = h.getreply()
if errcode != 200:
    print "Unable to connect"

print "Reading current address..."
f = h.getfile()
cahtml = f.readlines()
f.close()
print " ",cahtml[1]

windir = "C:\WINDOWS"
if os.environ.has_key("windir"):
    windir = os.environ["windir"]

print "Updating %s\HOSTS..." % (windir)
fin = open("%s\HOSTS" % (windir) , "r")
hosts = fin.readlines()
fin.close()

prog = regex.compile("news\.tokyopc\.bbs\.net", regex.casefold)
fout = open("%s/HOSTS.NEW" % (windir), "w")

updated = 0
for host in hosts:
    if (prog.search(host) != -1):
        fout.write(cahtml[1])
        updated = 1
    else:
        fout.write(host)

if (updated == 0):
    fout.write(cahtml[1])
fout.close()

try:
    os.unlink("%s/HOSTS.BAK" % (windir))
except os.error:
    pass

try:
    os.rename("%s/HOSTS" % (windir), "%s/HOSTS.BAK" % (windir))
except os.error:
    pass

os.rename("%s/HOSTS.NEW" % (windir), "%s/HOSTS" % (windir))

print "Ready to read news!"
