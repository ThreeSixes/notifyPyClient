import netifaces as ni
import json
import urllib
import urllib2
from pprint import pprint

class notifyPyClient():
	def __init__(self, destination, token, appName):
		"""
		Notify API of events. Requires a destination URL and auth token.
		"""
		
		# Set token and destination host.
		self.__appName = appName
		self.__token = token
		self.__callDst = destination
	
	def sendNotify(self, payload):
		"""
		Send notification to receiver. Requires JSON data, returns a dict containing the response.
		"""
		# Set response data.
		respData = {}
		
		# Set blank response body.
		respBody = "{}"
		
		# Send our token _always_.
		payload.update({
			'authToken': self.__token,
			'appName': self.__appName
		})
		
		try:
			# Set headers and perform request.
			headers = {'content-type': 'application/json'}    
			req = urllib2.Request(self.__callDst, json.dumps(payload), headers)
			
			# Make the request and wait for the body to come back.
			response = urllib2.urlopen(req)
			respBody = response.read()
		
		except urllib2.HTTPError as httpErr:
			# See if we can get the HTTP error string.
			respData.update({'error': True, 'message': str(httpErr)})
		
		except:
			raise
		
		finally:
			try:
				# Try to tack on response data.
				respData.update(json.loads(respBody))
			
			except:
				raise
		
		return respData