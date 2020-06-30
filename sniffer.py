'''
Created on 30 Jun 2020

@author: kai
'''

import pychrome
import subprocess
import time
def request_will_be_sent(**kwargs):
    #print("loading: %s" % kwargs.get('request').get('url'))
    #for debug purpose
    #request_list.append(kwargs.get('request').get('url'))
    request = kwargs.get('request').get('url')
    if('.m3u8' in request):
        m3u8_links.append(request)
        print("possible candidates: "+'\n'.join(map(str, m3u8_links)))

pid =subprocess.Popen(["google-chrome","--headless","--disable-gpu","--remote-debugging-port=9222"])
time.sleep(3)
browser = pychrome.Browser(url="http://127.0.0.1:9222")
# create a tab
tab = browser.new_tab()
m3u8_links=[]
request_list=[]
# register callback if you want


tab.Network.requestWillBeSent = request_will_be_sent

# start the tab 
tab.start()

# call method
tab.Network.enable()
# call method with timeout
tab.Page.navigate(url="", _timeout=5)

# wait for loading
tab.wait(10)

# stop the tab (stop handle events and stop recv message from chrome)
tab.stop()
print("time out, program terminate")
# close tab
browser.close_tab(tab)
subprocess.Popen.terminate(pid)
exit(0)
