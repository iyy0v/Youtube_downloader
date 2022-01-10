import re
from pytube import YouTube 

# functions used in the script
def filterData(data,j,type):
	global choices
	i = 0
	while i < len(data):
		if(data[i][j] != type):
			data.pop(i)
		else:
			i += 1
	choices = [[],[],[]]
	for d in data:
		choices = addChoices(d[1],d[2],d[3],choices)

	return data

def addChoices(Type,Format,Res,choices):
	if(Type not in choices[0]):
		choices[0].append(Type)
	if(Format not in choices[1]):
		choices[1].append(Format)
	if(Res not in choices[2]):
		choices[2].append(Res)
	return choices

def choicesMenu(i,word):
	global choices
	choice = "0"
	while(int(choice) < 1 or int(choice) > len(choices[i])):
		print("\n\n Choose a " + word + " :")
		
		n = 1
		for c in choices[i]:
			print("\n [" + str(n) +"] " + c)
			n += 1

		choice = input("\n Enter a number : ")
		if (int(choice) > 0 and int(choice) <= len(choices[i])):
			uVar = choices[i][int(choice)-1]
		else:
			print("\n Unknown choice ! Please enter a number again.")
	return uVar
#####################################################

# Script:

url = input("\n Enter the video link/url : ")

yt = YouTube(url)

Streams = yt.streams.filter(res=None)

# extract all available specs for the given video
data = []
choices = [[],[],[]]
for strm in Streams:
	strm = str(strm)
	vTag = re.findall(".* itag=\"(\d+)\".*",strm)[0]
	vType = re.findall(".* type=\"([^\"]+)\".*",strm)[0]
	vFormat = re.findall(".*/([^\"]+)\".*",strm)[0]
	if(vType == "video"):
		vRes = re.findall(".* res=\"([^\"]+)\".*",strm)[0]
	else:
		vRes = re.findall(".* abr=\"([^\"]+)\".*",strm)[0]
	data.append((vTag,vType,vFormat,vRes))
	choices = addChoices(vType,vFormat,vRes,choices)

# choose media specs to download
uType = choicesMenu(0,"media type")

data = filterData(data,1,uType)

uFormat = choicesMenu(1,"format")

data = filterData(data,2,uFormat)

if(uType == "video"):
	uRes = choicesMenu(2,"video resolution")
else:
	uRes = choicesMenu(2,"audio bitrate")

data = filterData(data,3,uRes)

# Download the media
uTag = int(data[0][0])

strmolution = yt.streams.get_by_itag(uTag)

path = input('\n Enter the path for download : ')

print("\n Downloading " + yt.title + "...")

strmolution.download(output_path=path)

print("\n Your video is downloaded !")