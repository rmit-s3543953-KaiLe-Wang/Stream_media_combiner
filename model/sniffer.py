'''
Created on 30 Jun 2020

@author: kai
'''

import pychrome
import subprocess
import time
from model.ts_combiner import Ts_combiner

heads={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6,ja;q=0.5','Cache-Control':'max-age=0','Connection': 'keep-alive',}

class Sniffer:
    def __init__(self,target_uri,**options):
        self.target_uri=target_uri
        self.requests=[]
        if 'wait_time' in options:
            self.wait_time = int(options.get('wait_time'))
        else:
            self.wait_time = 10
        if 'keyword' in options:
            self.keyword = str(options.get('keyword'))
        else:
            self.keyword = '.m3u8'
    
    def request_will_be_sent(self,**kwargs):
        #print("loading: %s" % kwargs.get('request').get('url'))
        #print("with headers: %s" % kwargs.get('request').get('headers'))
        request = kwargs.get('request').get('url')
        self.requests.append(str(request))
    
    def search_resuest(self):
        self.target_list=[]
        for link in self.requests:
            if(self.keyword in link):
                self.target_list.append(link)
        return self.target_list.copy()
    
    def start(self):
        pid =subprocess.Popen(["chrome","--headless","--disable-gpu","--remote-debugging-port=9222"])
        time.sleep(3)
        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tab = browser.new_tab()
        tab.Network.requestWillBeSent = self.request_will_be_sent
        tab.start()
        tab.Network.enable()
        #tab.Network.setExtraHTTPHeaders(headers=heads)
        tab.Page.navigate(url=self.target_uri, _timeout=5)
        tab.wait(self.wait_time)
        self.tab_name=tab.id
        tab.stop()
        browser.close_tab(tab)
        subprocess.Popen.terminate(pid)
        
    def read_list (self):
        messages=[]
        self.uri_list=[]
        for link in self.target_list:
            target=Ts_combiner(link,"")
            info_list = target.get_info()
            info_list.pop(0)
            if target.get_info()[0]=="Master:T":
                messages.append("found a master list:")
                for info in info_list:
                    messages.append("["+str(len(self.uri_list))+"] "+ info[0])
                    self.uri_list.append(info[0])
                    messages.append("stream info:"+ info[1])
                messages.append("----------------------------------")
            elif target.get_info()[0]=="Master:F":
                for uri in info_list:
                    messages.append("["+str(len(self.uri_list))+"] "+ uri)
                    self.uri_list.append(uri)
            else:
                messages.append("ERROR")
        return messages
    def download(self,selection,*output_filename):
        if None in output_filename:
            filename = self.tab_name
        else:
            filename = output_filename[0]
        target = Ts_combiner(self.uri_list[int(selection)],str(filename))
        target.download()
        target.combine_and_save()
        
    def set_keyword(self,keyword):
        self.keyword= keyword
    
def main():
    flag = False
    while not flag:
        # register callback if you want
        input_uri = input("please input video uri\n").replace("\n","")
        sniffer = Sniffer(input_uri)
        sniffer.start()
        print("time out, sniffer terminate, search for target request\n")
        target_list=sniffer.search_resuest()
        while None in target_list:
            option = input("none m3u8 link found, search requests from a different link?\n")
            if option == "Y" or option =="y":
                sniffer.set_keyword(option)
                target_list = sniffer.search_resuest()
            else:
                exit(0)
        message_list=sniffer.read_list()
        for info in message_list:
            print(info)
        selection = input("please select a link to download\n").replace("\n","")
        try:
            out_filename = input("please type output filename\n")
        except SyntaxError:
            out_filename = None
        sniffer.download(selection,out_filename)
        redo = input("another video?   Y/N\n").replace("\n","")
        if redo =="N" or redo =="n":
            flag = True
if __name__=="__main__":
    main()