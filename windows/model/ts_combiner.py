import m3u8
import sys
import os
import requests
import time

from Crypto.Cipher import AES

class Ts_combiner:
    file_count=0 #how many files in the m3u8 list
    keys=[] #key list same as playlist.keys
    keys_location =[]#for indicating which key is needed for corresponding segment, e.g. [1,5,6] means segment 1,5 and 6 requires keys[0],keys[1],keys[2] to decrypt. 
    data=''
    heads={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6,ja;q=0.5',
           'Cache-Control':'max-age=0',
           'Connection': 'keep-alive',
           }
    def __init__(self,m3u8_link,out_filename,**kwargs):
        self.m3u8_link=m3u8_link
        if 'prefix' in kwargs:
            self.prefix=kwargs.get("prefix")
        else:
            self.prefix=''
        print("prefix:" +self.prefix)
        self.out_filename = out_filename.replace('.mp4','')
    #combine all input .ts files into a mp4 file with defined output filename    
    def combine_and_save(self):
        #concatenate all files together
        for file_num in range(self.file_count):
            with open(self.input_filename.replace('.ts', '')+str(file_num)+'.ts','rb') as sample:
                print("combining process, reading file: "+self.input_filename+str(file_num)+'.ts')
                with open(self.out_filename+'_temp.ts','ab') as out:
                    out.write(sample.read())
        import ffmpeg
        (
            ffmpeg
            .input(self.out_filename+'_temp.ts')
            .output(self.out_filename+'.mp4')
            .global_args('-map', '0')
            .global_args('-c','copy')
            .global_args('-y')
            .run()
         )
        print("merge complete, deleting temporary files") 
        try:
            for file_num in range(self.file_count):
                os.remove(self.input_filename+str(file_num)+'.ts')
            os.remove(self.input_filename+'_temp.ts')
        except OSError as e:
            print("Error: %s - %s." %(e.filename, e.strerror))
        print("combiner terminate")
    #get all .ts files
    def download(self):
        playlist=m3u8.load(self.m3u8_link,headers=self.heads)
        print("loading complete, start gathering files")
        self.input_filename=self.out_filename
        self.get_info()
        with requests.session() as re:
            dir_name = os.path.dirname(self.out_filename)
            try:
                os.mkdir(dir_name)
            except :
                print("creation of the directory %s failed" % dir_name)
                print("exists dir with the same name?")
            else:
                print("directory "+dir_name+" created")
            #create a new directory for storing all ts files
            local_count=0
            for seg in playlist.segments:
                r=re.get(self.prefix+seg.absolute_uri,stream=True)
                if (None in self.keys) or (not self.keys):
                    data = r.content
                else:
                    data=self.decrypt(r.content,local_count,re)
                temp_filename =self.input_filename+str(local_count)+'.ts' 
                with open(temp_filename,'wb') as f:
                    f.write(data)
                    print("downloaded file: "+self.prefix+seg.absolute_uri+", saved as:"+self.input_filename+str(local_count)+'.ts')
                    local_count=local_count+1
                    progress = str(format((local_count/self.file_count)*100,'.3f'))
                    print("current progress: "+progress+"%")
    def decrypt(self,content,local_count,re):
        corresponding_index=0
        if len(self.keys_location)!=1:
            temp = [x-local_count for x in self.keys_location] 
            # for example, if we have keys_location of [5, 7, 10] and a current pointer of segement = 6
            #we minus 6 at each element, which temp= [-1,1,4], use the minimal but greater than 0 element in the list. so, key[1] in this case has been selected.
            print(temp)
            corresponding_index = temp.index(min(x for x in temp if x>=0))
            if corresponding_index==-1:
                corresponding_index = temp.index(max(self.keys_location))
        current_key = self.keys[corresponding_index]
        r=re.get(self.prefix+current_key.absolute_uri,stream=True)
        key = r.text
        if(str(current_key.iv)=="None"):
            iv = '0000000000000000'
        else:
            iv = str(current_key.iv)
        crypt = AES.new(key,AES.MODE_CBC,iv)
        data = crypt.decrypt(content)
        return data
    #get m3u8 info
    def get_info(self):
        playlist=m3u8.load(self.m3u8_link,headers=self.heads)
        self.file_count = int(len(playlist.segments))
        #print(playlist.segments)
        #print(playlist.target_duration)\
        num_of_keys=0
        if playlist.keys:
            self.keys=playlist.keys
            if not None in self.keys:
                #print("found "+str(len(playlist.keys))+" keys")
                #num_of_keys = len(playlist.keys)
                self.get_key_location(playlist)    
                print(str(num_of_keys)+" key(s) have found")
        #print("found "+str(self.file_count)+" segments")
        # return bandwidth, additional info
        if playlist.is_variant:
            master_list_info=["Master:T"]
            for eachplaylist in playlist.playlists:
                sublist_info=[]
                sublist_info.append(eachplaylist.absolute_uri)
                if not None in eachplaylist.stream_info.resolution:
                    sublist_info.append("Resolution: "+str(eachplaylist.stream_info.resolution).replace(",","*"))
                else:
                    sublist_info.append(str(eachplaylist.stream_info))
                master_list_info.append(sublist_info)
            return master_list_info
        else:
            list_info = ["Master:F"]
            list_info.append(self.m3u8_link)
            return list_info
    
    def get_key_location(self,playlist):
        #first, counting EXTINF
        seg_count=0
        line = playlist.dumps().split("\n")
        #print(line)
        for word in line:
            if '#EXTINF' in word:
                seg_count=seg_count+1
            elif '#EXT-X-KEY' in word:
                print("key at seg: "+str(seg_count))
                self.keys_location.append(seg_count)#add segment location into it
#main()
def main():    
    start_time = time.time()
    #argv[1] = link for m3u8 file
    if(len(sys.argv)==3):
        out_filename = str(sys.argv[1])
        m3u8_link = str(sys.argv[2])
        target=Ts_combiner(m3u8_link,out_filename)
    #argv[2] = offset link => link prefix for download .ts file, also sometimes the m3u8 file contains part of the link for the password.
    elif(len(sys.argv)==4):
        out_filename = str(sys.argv[1])
        m3u8_link = str(sys.argv[2])
        prefix_link = str(sys.argv[3])
        target = Ts_combiner(m3u8_link,out_filename,prefix=prefix_link)
    #target.get_info()
    target.download()
    print("all ts files have been downloaded, start combinining...")
    target.combine_and_save()
    print("all complete, program exit")
    print("time spent: "+str(format(time.time()-start_time,'.3f'))+" seconds")
    exit(0)

if __name__ =="__main__":
    main()
