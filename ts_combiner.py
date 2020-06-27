import m3u8
import sys
import os
import subprocess
import requests as req
import shutil
from Crypto.Cipher import AES



def saveAndCombine(out_filename, file_count):
    #TODO: it wont work, use generic way to solve it!!
    subprocess.run(shlex.split('cat '+out_filename+'_temp_{0..'+str(file_count)+'}.ts>temp.ts'))
    #shutil.copyfile(out_filename+'_temp_{0..'+str(file_count)+'}.ts','temp.ts')
    subprocess.run(shlex.split('ffmpeg -i temp.ts -acodec copy -vcodec copy '+out_filename+'.mp4'))
    print("merge complete, deleting temprary files")
    subprocess.run(shlex.split('rm '+out_filename+'_temp_'+'{0..'+str(file_count)+'}.ts'))
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

    file_count = 0
    seg_filename = out_filename+"_temp_"
    #create a new directory for storing all ts files
    for seg in playlist.segments:
        r=req.get(prefix_link+seg.absolute_uri,stream=True)
        if key_link:
            data = cipher.decrypt(r.content)
        else:
            data = r.content
        with open(seg_filename+str(file_count)+".ts",'wb') as f:
            f.write(data)
        print("downloaded file: "+seg_filename+str(file_count)+".ts")
        file_count=file_count+1
        progress = str(format((file_count/seg_length)*100,'.3f'))
        print("current progress: "+progress+"%")
    file_count=file_count-1 #the file count would be added 1 more time, so minus 1
    print("all ts files have been downloaded, start combinining...")
    saveAndCombine(out_filename,file_count)

