import m3u8
import sys
import os
import subprocess
import requests as req
import shutil
import shlex
from Crypto.Cipher import AES



def saveAndCombine(seg_filename,out_filename,dir_name,file_count):
    #concatenate all files together
    for file_num in range(file_count+1):
        seg_filename_complete = seg_filename+str(file_num)+'.ts'
        with open('./'+dir_name+'/'+seg_filename_complete,'rb') as sample:
            print("combining process, reading file: "+seg_filename_complete)
            with open('./'+dir_name+'/temp.ts','ab') as out:
                out.write(sample.read())
    subprocess.run(shlex.split('ffmpeg -i '+'./'+dir_name+'/temp.ts -acodec copy -vcodec copy '+'./'+dir_name+'/'+out_filename+'.mp4'))
    #print("merge complete, deleting temprary files")
    
    print("all complete, program exit")

#argv[1] = link for m3u8 file
if(len(sys.argv)==3):
    out_filename = str(sys.argv[1]).replace(".mp4","")
    m3u8_link = str(sys.argv[2])
    playlist = m3u8.load(m3u8_link)
    print("getting m3u8 file from:"+m3u8_link)
    if playlist.keys[0]:
        key_link = playlist.keys[0].absolute_uri
    else:
        key_link = ''
    prefix_link =''
    
#argv[2] = offset link => link prefix for download .ts file, also sometimes the m3u8 file contains part of the link for the password.
#argv[3] = "y" or "n" => does password need the prefix link too? default is no. 
elif(len(sys.argv)==4 or len(sys.argv)==5):
    out_filename = str(sys.argv[1]).replace("mp4","")
    m3u8_link = str(sys.argv[2])
    playlist = m3u8.load(m3u8_link)
    prefix_link = str(sys.argv[3])
    if(len(sys.argv)==5):
        if(str(sys.argv)=="y"):
            key_link = prefix_link+playlist.keys[0].absolute_uri
    else:
        key_link=playlist.keys[0].absolute_uri

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
        print("downloaded file: "+seg_filename+str(file_count)+".ts")
        file_count=file_count+1
        progress = str(format((file_count/seg_length)*100,'.3f'))
        print("current progress: "+progress+"%")
    file_count=file_count-1 #the file count would be added 1 more time, so minus 1
    print("all ts files have been downloaded, start combinining...")
    saveAndCombine(seg_filename,out_filename,dir_name,file_count)

