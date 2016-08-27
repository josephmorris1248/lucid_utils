from lucid_utils import data_api
from lucid_utils import blobbing
from lucid_utils.classification.lucid_algorithm import classify
import urllib2 as urllib
import numpy as np

def xycparse(lines):
	frame = np.zeros((256, 256))
	for line in lines:
		vals = line.split("\t")
		x = int(float(vals[0].strip()))
		y = int(float(vals[1].strip()))
		c = int(float(vals[2].strip()))

		frame[x][y] = c

	return frame

runs = [
    "2016-05-30",
    "2016-06-07",
    "2016-06-15",
    "2016-06-23",
    "2016-07-01",
    "2016-07-09",
    "2016-07-17",
    "2016-07-25",
    "2016-08-10",
    "2016-08-18"
]
count = 1
files= []
for run in runs:
    print "RUN STARTING", run
    files += data_api.get_data_files(run)

print files[269:271]
files = files[265:]

for df in files:
    print "ANALYSING FILE", count

    count += 1

    electron, proton = 0,0
    lat,lng = df['latitude'], df['longitude']
    num_frames = 1

    url = "http://starserver.thelangton.org.uk/lucid-data-browser/view/get/xyc?run=" + df['run'] + "&file_id=" + df['id'] + "&frame=1&channel=0"
    lines = urllib.urlopen(url).readlines()
    frames = [xycparse(lines)]

    print df['id']
    print url

    for frame in frames:
        ch = frame
        blobs = blobbing.find(ch)
        for blob in blobs:
            c = classify(blob)
            if c == "beta":
                electron += 1
            if c == "proton":
                proton += 1
    of = open("counts.txt", "a")
    of.write(str(lat) + "," + str(lng) + "," + str(num_frames) + "," + str(electron) + "," + str(proton) + "\n")
    of.close()
