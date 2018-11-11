import socket
import threading
import struct
import pickle
import os

class Command:
    command = ""
    payload = ""

def loadSongDict():
    rawData = {'0':'default'}
    f = open("songList.txt", 'r')
    lines = f.readlines()
    for line in lines:
        if line != '\n':
            line = line.strip('\n')
            rawData[line.split(',')[0]] = line.split(',')[1]
    return rawData

def saveSongDict(songDict):#convert every pairs of ID and songname to a line (string) and save them in a txt file
    f = open("songList.txt", 'w')
    for key in songDict:
        f.write(key+','+songDict[key]+'\n')
    f.close()

def loadListDict():#read the txt file and convert each line in it as a pair of ID and name in a dict varaiable
    rawData = {'0':'default'}
    f = open("playLists.txt", 'r')
    lines = f.readlines()
    for line in lines:
        if line != '\n':
            line = line.strip('\n')
            rawData[line.split(',')[0]] = line.split(',')[1]
    return rawData

def saveListDict(listDict):
    f = open("playLists.txt", 'w')
    for key in listDict:
        f.write(key+','+listDict[key]+'\n')
    f.close()

def loadIndex1(songDict):
    temp = 0
    for key in songDict:
        if int(key)>temp:
            temp = int(key)
    return temp + 1   
    
def loadIndex2(listDict):
    temp = 0
    for key in listDict:
        if int(key)>temp:
            temp = int(key)
    return temp + 1

def delete(songID,listID,listDict):
    temp = [listDict[listID]]
    f = open(listID +"_playlist.txt",'r')
    lines = f.readlines()
    for line in lines: 
        if (line.split(',')[0] !=songID) & (line.strip('\n') != listDict[listID]):
            line = line.strip('\n')
            temp.append(line)
    f.close()
    f = open(listID +"_playlist.txt",'w')
    for elem in temp:
        f.write(elem + '\n')
    f.close    
  
    

# This is my thread class.  It inherits from threading.Thread

class SocketThread(threading.Thread):
    
    def __init__(self, socketInstance):
        threading.Thread.__init__(self)   
        global songDict #2 global dict varaiables for store song and list name and number
        global listDict
        global index1#2 global int varaiables for song and list numeber generation 
        global index2
        self.mySocket = socketInstance


    
    def run(self):
        global songDict
        global listDict
        global index1
        global index2        
        try:
            while (True):
                print("Reading initial length")
                a = self.mySocket.recv(4)
                print("Wanted 4 bytes got " + str(len(a)) + " bytes")

                if len(a) < 4:
                    raise Exception("Client closed socket, ending client thread")

                messageLength = struct.unpack('i', a)[0]
                print("Message Length: ", messageLength)
                data = bytearray()
                while messageLength > len(data):
                    data += self.mySocket.recv(messageLength - len(data))

                newCommand = pickle.loads(data)
                print("Command is: ", newCommand.command)
                # check the type of getting command
                if newCommand.command.split(',')[0] == "GetSong":
                    #a.	Command = SONGDATA
                    #b.Payload = <binary MP3 file data>
                    print("Sending song")
                    replyCommand = Command()            
                    replyCommand.command = "SongData"
                    if newCommand.command.split(',')[1] not in songDict:
                        raise Exception("File not found")
                    f = open(newCommand.command.split(',')[1] + ".mp3", 'rb')  # Open the file, read it in, and use it as the payload
                    print("Sending file")
                    replyCommand.payload = f.read()
                    f.close()
                    
                elif newCommand.command == "GetSongList":
                    print("Sending song list")
                    replyCommand = Command()
                    replyCommand.command = "SongList"
                    replyCommand.payload = songDict
                    
                elif newCommand.command.split(',')[0] == "AddSong":
                    #a.	Command = SONGADDED <songID number>
                    #b.	Payload = empty
                    try:
                        print ("Adding song")
                        replyCommand = Command()
                        replyCommand.command = "SongAdded, songID: "+ str(index1)
                        f = open(str(index1)+ ".mp3", 'wb')
                        f.write(newCommand.payload)
                        f.close()
                        songDict[str(index1)]= newCommand.command.split(',')[1]#convert the index1 to a string as key in dict
                        index1 += 1
                        saveSongDict(songDict)
                        print("The song:",newCommand.command.split(',')[1], " is added.")
                    except Exception as e:
                        print("Error occured: ", e)
                        
                elif newCommand.command.split(',')[0] == "CreatePlaylist":
                    #a.	Command = PLAYLISTCREATED <playlistID number>
                    #b.	Payload = empty
                    try:
                        print ("Creating playlist")
                        replyCommand = Command()
                        replyCommand.command = "PlaylistCreated, PlaylistID: "+ str(index2)
                        f = open(str(index2)+"_playlist.txt", 'w')#create a new playlist with the playlist number in a .txt file
                        f.write(newCommand.command.split(',')[1]+"\n")
                        f.close()
                        listDict[str(index2)]= newCommand.command.split(',')[1]#save the list's name and ID pair in listDict
                        index2 += 1
                        saveListDict(listDict)#update playLists.txt
                        print("The playlist :",newCommand.command.split(',')[1], " is created")
                    except Exception as e:
                        print("Error occured: ", e)
                        
                elif newCommand.command == "GetAllPlaylists":
                    #a.	Command = ALLPLAYLISTSLIST
                    #b.	Payload = Python list containing all playlistID/playlist name pairs, from the file playlists.txt
                    try:
                        print ("Sending all playlists")
                        replyCommand = Command()
                        replyCommand.command = "AllPlaylistList"
                        plist = ["playlists"] # create a list object and use it as payload
                        f = open("playLists.txt", 'r') # open the file
                        lines = f.readlines() # read all lines of it
                        for line in lines:
                            if line != '\n': # ignore the empty line duirng file reading
                                line = line.strip('\n')
                                plist.append(line) # update the plist, save each line as an element of plist (added in the end of list) 
                        f.close()
                        plist.remove("playlists")
                        replyCommand.payload = plist
                    except Exception as e:
                        print("Error occured: ", e)
                        
                elif newCommand.command.split(',')[0] == "GetPlaylist":
                    #a.	Command = PLAYLISTLIST
                    #b.	Payload = Python list containing all songID/song name pairs, from the file <playlistID>.txt
                    try:
                        print("Sending playlist")
                        replyCommand = Command()            
                        replyCommand.command = "PlayList"
                        if newCommand.command.split(',')[1] not in listDict:
                            raise Exception("File not found")
                        slist = [newCommand.command.split(',')[1]+"_playlist"] # create a list object and use it as payload
                        f = open(newCommand.command.split(',')[1] + "_playlist.txt", 'r') # open the file
                        lines = f.readlines() # read all lines of it
                        for line in lines: 
                            if line != '\n': # ignore the empty line duirng file reading
                                line = line.strip('\n')
                                slist.append(line) # update the slist, save each line as an element of slist (added in the end of list)                       
                        f.close()
                        replyCommand.payload = slist
                    except Exception as e:
                        print("Error occured: ", e)                        

                elif newCommand.command.split(',')[0] == "AddSongToList":
                    #a.	Command = SONGADDED
                    try:
                        print ("Adding target song to list")
                        replyCommand = Command()
                        songID = newCommand.command.split(',')[1]
                        listID = newCommand.command.split(',')[2]
                        if songID not in songDict:
                            raise Exception("Song not found")
                        elif listID not in listDict:
                            raise Exception ("Playlist not found")
                        else:
                            f = open(listID+"_playlist.txt",'a')#open the target _playlist.txt file
                            f.write(songID +","+ songDict[songID]+"\n")#write the pair of songID and name to the end of this file
                            f.close()
                            replyCommand.command = "SongAdded"
                    except Exception as e:
                        print("Error occured: ", e)
                        
                elif newCommand.command.split(',')[0] == "RemoveSongFromList":
                    try:
                        print ("Remove target song from list")
                        replyCommand = Command()
                        songID = newCommand.command.split(',')[1]
                        listID = newCommand.command.split(',')[2]
                        if listID not in listDict:
                            raise Exception ("Playlist not found")
                        else:
                            delete(songID,listID,listDict)
                            replyCommand.command = "SongRemoved"
                    except Exception as e:
                        print("Error occured: ", e)
                        
                elif newCommand.command.split(',')[0] == "RemoveSong":
                    try:
                        print ("Remove target song")
                        replyCommand = Command()
                        songID = newCommand.command.split(',')[1]
                        if songID not in songDict:
                            raise Exception("Song not found")
                        else:
                            os.remove(songID + ".mp3") # delete the song file in server
                            songDict.pop(songID) # delete the songID and songName pair in songDict
                            saveSongDict(songDict) # save the updated songDict into file
                            for key in listDict: # delete all entries with songID in all playlists
                                delete(songID, key, listDict)    
                            replyCommand.command = "SongRemovedOK"
                        saveSongDict(songDict)
                    except Exception as e:
                        print("Error occured: ", e)
                        
                else:
                    print("Unknown Command")
                    raise Exception("Unknown Command")

                packedData = pickle.dumps((replyCommand))               # Serialize the class to a binary array
                self.mySocket.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
                self.mySocket.sendall(packedData)

        except Exception as e:
            print("Closing socket")
            print(e)
            self.mySocket.close()
            saveSongDict(songDict) # let's save it here before we exit the thread
            saveListDict(listDict)


host = "localhost"
port = 4567

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(1)


print("Listening...")
songDict = loadSongDict()
print(songDict)
listDict = loadListDict()
print(listDict)
index1 = loadIndex1(songDict)
print(index1)
index2 = loadIndex2(listDict)
print(index2)


while True:
    (clientSocket, address) = serverSocket.accept()
    print("Got incoming connection")
    newThread = SocketThread(clientSocket)        # make a new instance of our thread class to handle requests
    newThread.start()                             # start the thread running....
