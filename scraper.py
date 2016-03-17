#!/usr/bin/env python

#  Wayback Scraper
#
#  Description:
#      This script enumerates all archives for a particular domain (or subdomain)
#      and outputs them to a text file that begins with the supplied domain.
#
#  Notes:
#      The results are not all-inclusive of each individual subdomain on the
#      given domain. For example, earching for example.com may also include
#      archived results for some.example.com, but searching explicitly for
#      some.example.com will provide many more results.
#
#
#  0x30797263

import urllib2
import re
import sys

# A newline at the beginning to make everything pretty. <3
print

# Output instructions.
if len(sys.argv) != 2:
    print "Wayback Scraper\n"
    print "Description:"
    print "    Retrieves all archived pages for a specified"
    print "    domain and outputs them to [sub].domain.tld.txt\n"
    print "Usage:"
    print "    python %s [sub.]domain.tld\n" % sys.argv[0]
    print "Examples:"
    print "    python %s kali.org" % sys.argv[0]
    print "    python %s www.bypro.xyz" % sys.argv[0]
    print "    python %s you.get.the.point\n" % sys.argv[0]
    exit()

domain = sys.argv[1]
print "Fetching archives...\n"

# 403 indicates that robots.txt is present.
try:
    result = urllib2.urlopen("http://web.archive.org/web/*/http://%s/*" % domain)
except urllib2.HTTPError as e:
    if e.code == 403:
        print "That site's robots.txt says no. =(\n"
        exit()

print "Parsing results...\n"

# Eliminate any issues with Unicode chars.
try:
    data = result.read().encode("ascii", "ignore")
except:
    print "No archived pages were found. =(\n"
    exit()

# Grab all archived pages.
matches = re.findall(r">(.*%s.*)<" % domain, data)
total_matches = len(matches)

print "Found %d archived pages!\n" % total_matches
file = open("%s.txt" % domain, "w+")

for i in range(0, total_matches):
    percent = int(float(i+1) / total_matches * 100)
    file.write("%s\n" % matches[i].replace("&amp;", "&"))
    # Eliminate needless re-printing and re-flushing.
    try:
        if percent == progress:
            continue
    except:
        pass
    progress = percent
    sys.stdout.write("\rFetching links... %d%%" % progress)
    sys.stdout.flush()

print "\n\nAll archived pages saved to %s.txt.\n" % domain
file.close()
