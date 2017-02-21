import requests, getpass
from lxml import html
import sys
import os.path

print "Enter your student number:"
student_num = raw_input()

print "Enter your moodle password:"
moodle_password = getpass.getpass()

def get_moodle_session():
	# Log into moodle
	S_moodle = requests.session()
	moodle_url = 'https://csmoodle.ucd.ie/moodle/login/index.php'
	S_moodle.get(moodle_url)
	moodle_session = S_moodle.cookies['MoodleSession']
	login_data = dict(MoodleSession=moodle_session, username=student_num, password=moodle_password)
	S_moodle.post(moodle_url, data=login_data, headers={"Referer": "https://csmoodle.ucd.ie/moodle/"})
	page = S_moodle.get('https://csmoodle.ucd.ie/moodle/')
	tree = html.fromstring(page.content)
	if tree.find(".//a[@class='loginurl']/") is not None:
		sys.exit("MOODLE LOGIN ERROR: Check username and password")

	return S_moodle

def get_module_list():
	# Creating a list of modules the user is registered to for the semester
	if not os.path.isfile('module_list.txt'):
		print "\nHow many modules are you doing this semester?"
		num_of_modules = raw_input()
		print "Enter your modules like so: <MODULE CODE> <MODULE TITLE>"
		print "Hint: Its much better if you just copy & paste the entire title from csmoodle"
		c_list = []
		for i in xrange(int(num_of_modules)):
			c_list.append(str(raw_input()))

		# Assuming input is in correct format
		module_list = open('module_list.txt', 'w')
		for module in c_list:
			module_name = module[10:]
			if not os.path.exists(module_name):
				os.makedirs(module_name)
				module_list.write("%s\n" % module)
		return c_list
	else:
		c_list = open("module_list.txt", 'r').read().splitlines()
		for module_name in c_list:
			if not os.path.isdir(module_name[10:]):
				os.makedirs(module_name[10:])
		return c_list

def download_file(download_url, filename, extension, module_name):
	# Need to go to the url first to get the file url
	result = S_moodle.get(download_url, stream=True)
	r = S_moodle.get(download_url, stream=True)
	filename = filename.replace("/", "")
	with open(module_name+'/'+filename+'.'+get_file_format(extension), 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				#f.flush()
		#print("Completed")


def get_file_format(extension):
	return {
        "archive" : "zip",
        "powerpoint" : "ppt",
        "document" : "docx",
        "spreadsheet" : "xslx",
    }.get(extension, "pdf")

def scrape_moodle(moodle_class_links):
	module_dict = {}
	# Collect urls
	for module in moodle_class_links:
		module_dict[module.text] = module.get("href")

	for module in module_dict.keys():
		module_url = module_dict[module]

		if module in class_list:
			module = module[10:]
			moodle_result = S_moodle.get(module_url, headers = dict(referer = module_url))
			tree = html.fromstring(moodle_result.content)
			file_div = tree.findall(".//div[@class='activityinstance']/")

			for a_tag in file_div:
				img_tag = a_tag[0] # last few characters of img src link tell what format file is
				span_tag = a_tag[1] # Name of the file
				acceptable_formats = ['powerpoint', 'pdf', 'archive', 'document', 'spreadsheet']		    
				
				for file_format in acceptable_formats:
					if file_format in img_tag.get("src"):
						# Check if file does not exist in folder
						if not os.path.isfile(module+'/'+span_tag.text+'.'+get_file_format(file_format)):
							print "Adding:\t" +span_tag.text+'.'+get_file_format(file_format)
							download_file(a_tag.get("href"), span_tag.text, file_format, module)

# Get Moodle session
S_moodle = get_moodle_session()

# Get list of classes for semester
class_list = get_module_list()

# Scrape for files on moodle
moodle_url = 'https://csmoodle.ucd.ie/moodle/'
moodle_result = S_moodle.get(moodle_url, headers = dict(referer = moodle_url))
tree = html.fromstring(moodle_result.content)
moodle_class_links = tree.findall(".//h3[@class='coursename']/")
scrape_moodle(moodle_class_links)

print "Files up to date"

