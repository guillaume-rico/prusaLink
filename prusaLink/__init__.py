#!/usr/bin/python

import requests
import json

class prusaLink:
    """Wrapper for the PrusaLink API.
    https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/master/lib/WUI/link_content/basic_gets.cpp
    """
    
    def __init__(self, host: str, api_key: str, port=80) -> None:
        """Initialize the prusaLink class."""
        self.host = host
        self.port = str(port)
        self.api_key = api_key
        self.headers = {'X-Api-Key': api_key}
        
    def get_version(self) :
        """Get the version."""
        r = requests.get('http://' + self.host + ':' + self.port + '/api/version', headers=self.headers)
        return r
        
    def get_printer(self) :
        """Get the printer."""
        r = requests.get('http://' + self.host + ':' + self.port + '/api/printer', headers=self.headers)
        return r
        
    def get_job(self) :
        """Get the job."""
        r = requests.get('http://' + self.host + ':' + self.port + '/api/job', headers=self.headers)
        return r
        
    def get_files(self, remoteDir = '/USB/') :
        """
        List files on USB Drive.
        
        Test code :
        import prusaLink
        prusaMini = prusaLink.prusaLink("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.get_files().json()
        
        r = requests.get('http://192.168.1.211/api/files', headers=headers)
        
        """
        # was : r = requests.get('http://' + self.host + ':' + self.port + '/api/files?recursive=true', headers=self.headers)
        r = requests.get('http://' + self.host + ':' + self.port + '/api/files' + remoteDir, headers=self.headers)
        return r
        
    def post_gcode(self, filePathLocal) :
        """
        Send a file on USB Drive.
        
        Test code :
        import prusaLink
        prusaMini = prusaLink.prusaLink("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.post_gcode('C:/SLF/Perso/brio/_exportUSB/MTN/DEBOUCHAGE.gcode')
        
        files.json()['refs']['resource']
        
        """
        fileContentBinary = {'file': open(filePathLocal,'rb')}
        # Marche aussi avec 
        #r = requests.post('http://' + self.host + ':' + self.port + '/api/files/usb/', headers=self.headers, files=fileContentBinary )
        r = requests.post('http://' + self.host + ':' + self.port + '/api/files/local/', headers=self.headers, files=fileContentBinary )
        return r
        
    def post_print_gcode(self, remotePath) :
        """
        Print on USB Drive.
        
        Test code :
        import prusaLink
        prusaMini = prusaLink.prusaLink("192.168.1.211", "44Da9wHhThmzFFJ")
        files = prusaMini.post_print_gcode('/usb/DEBOUC~1.GCO')
        
        """
        payload = {'command': 'start'}
        r = requests.post('http://' + self.host + ':' + self.port + '/api/files' + remotePath, headers=self.headers, data=json.dumps(payload))
        return r
        
        
    def delete_gcode(self, filePathRemote) :
        """
            Delete gcode on USB drive
            
            Test code :
            import prusaLink
            prusaMini = prusaLink.prusaLink("192.168.1.211", "44Da9wHhThmzFFJ")
            ret = prusaMini.delete_gcode('/usb/DEBOUC~1.GCO').json()
        """
        r = requests.delete('http://' + self.host + ':' + self.port + '/api/files' + filePathRemote, headers=self.headers)
        return r
        
        
# Utilisation :
# import prusaLink
# prusaMini = prusaLink.prusaLink("192.168.0.123", "8ojHKHGNuAHA2bM", port=8017)
# prusaMini = prusaLink.prusaLink("192.168.1.211", "44Da9wHhThmzFFJ")
# obj = prusaMini.get_version()