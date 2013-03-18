import urllib2
import types
import json
import md5
from uritemplate import expand

def md5(s):
	return md5.new(s).hexdigest()

class ParameterBuilder(object):
	"""dict to str"""
	def __init__(self, params):
		super(ParameterBuilder, self).__init__()
		self.params = params

	def get_url_params(self):
		plist = []
		for k in self.params:
			plist.append("%s=%s"%(k, self.params[k]))

		return "&".join(plist)
		
	def get_params_with_url(self, surl):
		return ("%s?%s"%(surl, self.get_url_params()))

class RestClient(object):
	"""Simple RestClient"""
	def __init__(self, baseUrl):
		super(RestClient, self).__init__()
		self.baseUrl = baseUrl
	
	def __build_url(self, path, path_params):
		return ("%s%s"%(self.baseUrl, (None == path_params and path or expand(path, path_params))))

	def __parse_params(self, url_params):
		params = ""
		if None != url_params:
			if type(url_params) == types.DictType:
				pbuilder = ParameterBuilder(url_params)
				params = pbuilder.get_url_params()
			else:
				params = url_params
		return params

	def __build_request_and_do(self, method, url, params, headers):
		data = self.__parse_params(params)
		if "GET" == method:
			url = "%s?%s"%(url, data)
			data = None
		if None == headers:
			headers = {}
		req = urllib2.Request(url, data)
		req.get_method = lambda: method
		for k in headers:
			req.add_header(k, headers[k])
		resp = urllib2.urlopen(req)
		return json.loads(resp.read())

	def __do_request(self, method, path, path_params, url_params, headers):
		req_url = self.__build_url(path, path_params)
		return self.__build_request_and_do(method, req_url, url_params, headers)

	def do_get(self, path, path_params, url_params, headers):
		return self.__do_request("GET", path, path_params, url_params, headers)

	def do_post(self, path, path_params, url_params, headers):
		return self.__do_request("POST", path, path_params, url_params, headers)