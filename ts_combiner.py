import m3u8
import sys
import os
import requests as req
import time
from ffmpy import FFmpeg
from Crypto.Cipher import AES


def combine_and_save(seg_filename,out_filename,dir_name,file_count):
    #concatenate all files together
    for file_num in range(file_count+1):
        seg_filename_complete = seg_filename+str(file_num)+'.ts'
        with open('./'+dir_name+'/'+seg_filename_complete,'rb') as sample:
            print("combining process, reading file: "+seg_filename_complete)
            with open('./'+dir_name+'/temp.ts','ab') as out:
                out.write(sample.read())
    #format convertion
    ff = FFmpeg(
            inputs = {'./'+dir_name+'/temp.ts':None},
            outputs ={'./'+dir_name+'/'+out_filename+'.mp4':None}
            )
    print("generated command: "+ff.cmd)
    ff.run()
    print("merge complete, deleting temprary files") 
    try:
        for file_num in range(file_count+1):
            seg_filename_complete = seg_filename+str(file_num)+'.ts'
            os.remove('./'+dir_name+'/'+seg_filename_complete)
        os.remove('./'+dir_name+'/temp.ts')
    except OSError as e:
        print("Error: %s - %s." %(e.filename, e.strerror))
    
    
heads={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}

#main()
start_time = time.time()
#argv[1] = link for m3u8 file
if(len(sys.argv)==3):
    out_filename = str(sys.argv[1]).replace(".mp4","")
    m3u8_link = str(sys.argv[2])
    playlist = m3u8.load(m3u8_link,headers=heads)
    print("getting m3u8 file from:"+m3u8_link)
    if playlist.keys[0]:
        key_link = playlist.keys[0].absolute_uri
    else:
        key_link = ''
    prefix_link =''
    
#argv[2] = offset link => link prefix for download .ts file, also sometimes the m3u8 file contains part of the link for the password.
#argv[3] = "y" or "n" => does password need the prefix link too? default is no. 
elif(len(sys.argv)==4 or len(sys.argv)==5):
    out_filename = str(sys.argv[1]).replace(".mp4","")
    m3u8_link = str(sys.argv[2])
    print("got m3u8 link:"+m3u8_link)
    playlist = m3u8.load(m3u8_link,headers=heads)
    prefix_link = str(sys.argv[3])
    print(playlist.keys)
    if not None in playlist.keys:
        if(len(sys.argv)==5):
            if(str(sys.argv)=="y"):
                key_link = prefix_link+playlist.keys[0].absolute_uri
        else:
            key_link=playlist.keys[0].absolute_uri
    else:
        key_link=''

seg_length = int(len(playlist.segments))
#print(playlist.segments)
#print(playlist.target_duration)
#print(key_link)
print("found "+str(len(playlist.segments))+" segments")
print("loading complete, start gathering files")

#TODO:fix key function, currently it only support 1 key.
if key_link:
    for key in playlist.keys:
        if key:  # First one could be None
            print(str(key.uri))
            print(str(key.method))
            print(str(key.iv))
            if(str(key.iv)=="None"):
                iv = '0000000000000000'
            else:
                iv = str(key.iv)
key = ''
data =''
with req.session() as req:
    if key_link:
        r = req.get(key_link,stream = True)
        key = r.text
        print("got key:")
        print(key)
        print("key length:"+str(len(key)))
        cipher = AES.new(key,AES.MODE_CBC,iv)
    dir_name = out_filename.replace(".mp4","")
    try:
        os.mkdir(dir_name)
    except OSError:
        print("creation of the directory %s failed" % dir_name)
        print("exists dir with the same name?")
        exit(-1)
    else:
        print("directory "+dir_name+" created")

    file_count = 0
    seg_filename = out_filename+"_temp_"
    #create a new directory for storing all ts files
    for seg in playlist.segments:
        r=req.get(prefix_link+seg.absolute_uri,stream=True)
        if key_link:
            data = cipher.decrypt(r.content)
        else:
            data = r.content
        with open("./"+dir_name+"/"+seg_filename+str(file_count)+".ts",'wb') as f:
            f.write(data)
        print("downloaded file: "+prefix_link+seg.absolute_uri+", saved as"+seg_filename+str(file_count)+".ts")
        file_count=file_count+1
        progress = str(format((file_count/seg_length)*100,'.3f'))
        print("current progress: "+progress+"%")
    file_count=file_count-1 #the file count would be added 1 more time, so minus 1
    print("all ts files have been downloaded, start combinining...")
    combine_and_save(seg_filename,out_filename,dir_name,file_count)
    print("all complete, program exit")
    print("time spent: "+str(format(time.time()-start_time,'.3f'))+" seconds")
    exit(0)
