import json
import os
import csv
 
# Get the list of all files and directories
path = "json_files"
files = os.listdir(path)
 
print("Files and directories in '", path, "' :",files)

songs=0
header=['title','uri','name','playcount','trackNumber','duration','artist','other artist']
rows=[]
track=[]
for file in files:
    title=file.split('.')[0]
    print('--->'+file)
    print('--->TITLE',title)
    f = open(path+'/'+file)
    jsonObj=json.load(f)
    # print(jsonObj)
    # print(type(jsonObj))
    for i,items in enumerate(jsonObj['data']['album']['tracks']['items']):
        
        print(' --> track',i)
        print('  -> title',title)
        track.append(title)
        for val in items['track']:
            if val in ['uri','name','playcount','trackNumber','duration','artists']:
                
                if val=='duration':
                    print('  ->',val,items['track'][val]['totalMilliseconds'])
                    track.append(items['track'][val]['totalMilliseconds'])
                elif val=='artists':
                    if len(items['track'][val]['items'])==1: #only rosalia
                        print('  ->artist  ',items['track'][val]['items'][0]['profile']['name'])
                        print('  -> other artists  ',None)
                        track.append(items['track'][val]['items'][0]['profile']['name'])
                        track.append(None)
                    else:
                        print('  ->artist  ',items['track'][val]['items'][0]['profile']['name'])
                        track.append(items['track'][val]['items'][0]['profile']['name'])
                        others=[]
                        for a,artist in enumerate( items['track'][val]['items'][1:]):
                            print('  -> other artist  ',a,artist['profile']['name'])
                            others.append(artist['profile']['name'])
                        track.append((','.join(others)))
                else: 
                    print('  ->',val,items['track'][val])
                    track.append(items['track'][val])
        songs+=1
        print(track)
        rows.append(track)
        track=[]

print('total songs',songs)
print('data len',len(rows))

with open('spotify_data.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(header)
    write.writerows(rows)

# print(','.join(['hola','adios'])    )
        

        


    
