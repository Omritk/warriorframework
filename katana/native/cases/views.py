"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
import os, sys, glob, copy 
from collections import OrderedDict
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from xml.sax.saxutils import escape, unescape
import xml.dom.minidom 
import xmltodict
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library
import json
from utils.navigator_util import Navigator
from katana_utils import *
import scanfiles


navigator = Navigator();
path_to_src_python_file = navigator.get_katana_dir() + os.sep + "config.json"
All_case_action_details = py_file_details(json.loads(open(path_to_src_python_file).read())['pythonsrcdir']);
			



def index(request):
	path_to_config_file = navigator.get_katana_dir() + os.sep + "config.json"
	x= json.loads(open(path_to_config_file).read());
	path_to_testcases = x['xmldir'];
	template = loader.get_template("listAllCases.html")
	fpath = path_to_testcases ;

	jtree = navigator.get_dir_tree_json(fpath)
	jtree['state']= { 'opened': True };

	context = { 
		'title' : 'List of Cases',	
		'dirpath' : path_to_testcases,
		'treejs': jtree,
	}
	return HttpResponse(template.render(context, request))




##
## This is very costly imho. 
##
## If we keep this information on file on disk then we'll be left behind 
## if more actions/keywords are added to the dispalys. 
## On the other hand getting this information on every call is absurd. 
## However, the spaghetti code in the py_file_details is too hairy to untangle
## before the demo and is left alone. 
##
def getListOfActions(request):
	"""
	Returns a list of all the actions and their details using config.json.
	"""
	path_to_pythonsrc = json.loads(open(path_to_src_python_file).read())['pythonsrcdir'] ;                 
	jsr = scanfiles.fetch_action_file_names(path_to_pythonsrc,'driver','all');
	actions = [ os.path.basename(fn)[:-3] for fn in jsr['ProductDrivers']];
	return JsonResponse({'actions': actions , 'filesinfo' : All_case_action_details })


##
## If we keep this information on file on disk then we'll be left behind 
## if more actions/keywords are added to the dispalys. 
## On the other hand getting this information on every call is absurd. 
## However, the spaghetti code in the py_file_details is too hairy to untangle
## before the demo and is left alone. 
##
def getListOfKeywords(request):
	if 0: 
			path_to_src_python_file = navigator.get_katana_dir() + os.sep + "config.json"
			x= json.loads(open(path_to_src_python_file).read());
			path_to_pythonsrc = x['pythonsrcdir']; 
			details = py_file_details(path_to_pythonsrc);
	else:
			details = All_case_action_details;
			
	driver = request.GET.get('driver');
	print dir(details);
	print driver
	#print details[driver][0]
	print len(details[driver][0])
	responseBack = { 'keywords': [] }
	for item in details[driver][0]: 
		print item
		responseBack['keywords'].append(item['fn']);
	return JsonResponse(responseBack)

##
## This is very costly imho. 
##
## If we keep this information on file on disk then we'll be left behind 
## if more actions/keywords are added to the dispalys. 
## On the other hand getting this information on every call is absurd. 
## However, the spaghetti code in the py_file_details is too hairy to untangle
## before the demo and is left alone. 
##
def getListOfComments(request):
	"""
	Return infomration about the driver and keyword in the incoming POST request.
	"""
	if 0: 
			path_to_src_python_file = navigator.get_katana_dir() + os.sep + "config.json"
			x= json.loads(open(path_to_src_python_file).read());
			path_to_pythonsrc = x['pythonsrcdir']; 
			details = py_file_details(path_to_pythonsrc);
	else:
			details = All_case_action_details;
			
	driver  = request.GET.get('driver');
	keyword = request.GET.get('keyword');
	responseBack = { 'fields': [] }
	
	for item in details[driver][0]: 
		if item['fn'] == keyword: 
			print item
			responseBack['fields'].append(item);

	return JsonResponse(responseBack)


def editCase(request):
	""" 
	Set up JSON object for editing a suites file. 
	"""
	path_to_config_file = navigator.get_katana_dir() + os.sep + "config.json"
	x= json.loads(open(path_to_config_file).read());
	path_to_testcases = x['xmldir'];
	template = loader.get_template("editCase.html")
	filename = request.GET.get('fname')

	# Open the XML file and get it's dictionary...
	# Make exceptions for missing or badly formatted files. 
	
	# Set up defaults for an xml_r object

	xml_r = {}
	xml_r["Testcase"] = {}
	xml_r["Testcase"]["Details"] = {}
	xml_r["Testcase"]["Details"]["Name"] = ""
	xml_r["Testcase"]["Details"]["Title"] = ""
	xml_r["Testcase"]["Details"]["Category"] = ""
	xml_r["Testcase"]["Details"]["Engineer"] = ""
	xml_r["Testcase"]["Details"]["Date"] = ""
	xml_r["Testcase"]["Details"]["Time"] = ""
	xml_r["Testcase"]["Details"]["State"] = ""
	xml_r["Testcase"]["Details"]["InputDataFile"] = ""
	xml_r["Testcase"]["Details"]["Datatype"] = ""
	xml_r["Testcase"]["Details"]["default_onError"] = ""
	xml_r["Testcase"]["Details"]["Logsdir"] = ""
	xml_r["Testcase"]["Details"]["Resultsdir"] = ""
	xml_r["Testcase"]["Details"]["ExpectedResults"] = 	""
	xml_r["Testcase"]["Requirements"] = {} 
	xml_r["Testcase"]["Steps"] = {} 
	

	if filename == 'NEW':
		subdir = path_to_testcases 
		filename = 'new.xml'
		fn = 'new.xml'
		xml_d = copy.deepcopy(xml_r)
	else: 
		xlines = open(filename).read()
		xml_d = xmltodict.parse(xlines);
		subdir = os.path.split(filename)[0]
		fn = 'save_' + os.path.split(filename)[1]
	# Map the input to the response collector
	for xstr in ["Name", "Title", "Category", "Date", "Time", "InputDataFile", "Engineer", \
		"Datatype", "default_onError", "Logsdir", "Resultsdir", "ExpectedResults"]:
		try:
			if not xml_r["Testcase"]["Details"].has_key(xstr): xml_r["Testcase"]["Details"][xstr]="";
			xml_r["Testcase"]["Details"][xstr] = copy.copy(xml_d["Testcase"]["Details"].get(xstr, ""))
			
		except:
			pass

	caseStateOptions_str = ['New','Draft','In Review','Released']

	try:
		xml_r['Testcase']['Steps'] = copy.deepcopy(xml_d['Testcase']['Steps']);
	except:
		xml_r["Testcase"]["Steps"] = {}

	try:
		xml_r['Testcase']['Requirements'] = copy.deepcopy(xml_d['Testcase']['Requirements']);
	except:
		xml_r["Testcase"]["Requirements"] = {}

	context = { 
		'myfile': filename,
		'savefilename': fn,
		'savesubdir': subdir,
		'docSpec': 'caseSpec',
		'caseName': xml_r["Testcase"]["Details"]["Name"],
		'caseTitle': xml_r["Testcase"]["Details"]["Title"],
		'caseEngineer': xml_r["Testcase"]["Details"]["Engineer"],
		'caseCategory': xml_r["Testcase"]["Details"]["Category"],
		'caseDate': xml_r["Testcase"]["Details"]["Date"],
		'caseTime': xml_r["Testcase"]["Details"]["Time"],
		'caseState': xml_r["Testcase"]["Details"]["State"],
		'caseStateOptions': caseStateOptions_str, 
		'caseDatatype': xml_r["Testcase"]["Details"]["Datatype"],
		'caseInputDataFile': xml_r["Testcase"]["Details"]["InputDataFile"],
		'casedefault_onError': xml_r["Testcase"]["Details"]["default_onError"],
		'caseLogsdir': xml_r["Testcase"]["Details"]["Logsdir"],
		'caseResultsdir': xml_r["Testcase"]["Details"]["Resultsdir"],
		'caseExpectedResults': xml_r["Testcase"]["Details"]["ExpectedResults"],
		'caseSteps': xml_r["Testcase"]["Steps"],
		'caseRequirements': xml_r['Testcase']['Requirements'],
		'fulljson': xml_r['Testcase']
	}

	return HttpResponse(template.render(context, request))

def getCaseDataBack(request):
	"""
	Return edited case data back as JSON and a file name to write to.
	Use the config.json file to get the path to the testcases directory and
	the savesubdir parameter to save to the (sub)directory under the main 
	directory. 
	"""
	path_to_config_file = navigator.get_katana_dir() + os.sep + "config.json"
	x= json.loads(open(path_to_config_file).read());
	path_to_testcases = x['xmldir'];
	ijs = request.POST.get(u'json')
	fn = request.POST.get(u'filetosave')
	sb = request.POST.get(u'savesubdir')
	fname = sb + os.sep + fn;  
	print "save case to ", fname 
 
	xml = xmltodict.unparse(json.loads(ijs), pretty=True)	
	fd = open(fname,'w');
	fd.write(xml);
	fd.close();
	return redirect(request.META['HTTP_REFERER'])