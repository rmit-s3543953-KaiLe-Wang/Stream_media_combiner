'''
Created on 30 Jun 2020

@author: kai
'''

import pychrome
import subprocess
import time
from model.ts_combiner import Ts_combiner

def request_will_be_sent(**kwargs):
    #print("loading: %s" % kwargs.get('request').get('url'))
    #for debug purpose
    #request_list.append(kwargs.get('request').get('url'))
    request = kwargs.get('request').get('url')
    if('.m3u8' in request):
        m3u8_links.append(request)
        #print("possible candidates: "+'\n'.join(map(str, m3u8_links)))

pid =subprocess.Popen(["chrome","--headless","--disable-gpu","--remote-debugging-port=9222"])
time.sleep(3)
browser = pychrome.Browser(url="http://127.0.0.1:9222")
flag = False
while not flag:
    # create a tab
    tab = browser.new_tab()
    m3u8_links=[]
    request_list=[]
    # register callback if you want
    input_uri = input("please input video uri\n")

    tab.Network.requestWillBeSent = request_will_be_sent

    # start the tab 
    tab.start()

    # call method
    tab.Network.enable()
    # call method with timeout
    tab.Page.navigate(url=input_uri, _timeout=5)
    
    tabname = tab.id
    # wait for loading
    tab.wait(10)

    # stop the tab (stop handle events and stop recv message from chrome)
    tab.stop()
    print("time out, sniffer terminate\n")
    # close tab
    browser.close_tab(tab)
    uri_list =[]
    for link in m3u8_links:
        target=Ts_combiner(link,"out.mp4")
        info_list = target.get_info()
        info_list.pop(0)
        if target.get_info()[0]=="Master:T":
            print("it is a master list:")
            for info in info_list:
                print("["+str(len(uri_list))+"] "+ info[0])
                uri_list.append(info[0])
                print("stream info:"+ info[1])
        elif target.get_info()[0]=="Master:F":
            for uri in info_list:
                print("["+str(len(uri_list))+"] "+ uri)
                uri_list.append(uri)
        else:
            print("ERROR")
    selection = input("please select a link to download\n")
    try:
        out_filename = input("please type output filename\n")
    except SyntaxError:
        out_filename = None
    if out_filename != None or out_filename !="\n":
        output_filename =out_filename
    else:
        output_filename = tabname
    target = Ts_combiner(uri_list[int(selection)],output_filename)
    target.download()
    target.combine_and_save()
    redo = input("another video?   Y/N\n")
    if redo =="N" or redo =="n":
        flag = True
        subprocess.Popen.terminate(pid)
