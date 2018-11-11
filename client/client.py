import socket
import struct
import pickle
import tkinter as tk
import tkinter.messagebox
import playsound

host = "localhost"
port = 4567

def getSong(songID, s):#this songID is a string
    #a.	Command = GETSONG <songID>
    #b.	b.	Payload = none
    try:
        getCommand = Command()
        getCommand.command = "GetSong,"+ songID
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        print("Reply: ",replyCommand.command)
        f = open(songID+".mp3", "wb")
        f.write(replyCommand.payload)
        f.close()
        
    except Exception as e:
        print("Error occured: ", e)

def getSongList(s):
    getCommand = Command()
    getCommand.command = "GetSongList"
    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)

    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    data = bytearray()
    while (replyLen > len(data)):
        data += s.recv(replyLen - len(data))
    replyCommand = pickle.loads(data)
    print("Reply: ",replyCommand.command)
    print("Song List is: ", replyCommand.payload)
    return replyCommand.payload

def addSong(songName,s):
    
    #a.	Command = ADDSONG <song name>
    #b.	Payload = <binary .mp3 file data>
    getCommand = Command()
    getCommand.command = "AddSong,"+ songName
    f = open( songName + ".mp3", 'rb')  # Open the file, read it in, and use it as the payload
    getCommand.payload = f.read()
    f.close()
    print("Sending file: ", songName)

    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)
        
    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    data = bytearray()
    while (replyLen > len(data)):
        data += s.recv(replyLen - len(data))

    replyCommand = pickle.loads(data)
    print("Reply: ", replyCommand.command)


def createPlaylist(listName, s):
    #a.	Command = CREATEPLAYLIST <playlist name>
    #b.	Payload = none
    try:
        getCommand = Command()
        getCommand.command = "CreatePlaylist,"+ listName
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        print("Reply: ",replyCommand.command)
        
    except Exception as e:
        print("Error occured: ", e)

def getAllPlaylists(s):
    #a.	Command = GETALLPLAYLISTS
    #b.	Payload = none
    getCommand = Command()
    getCommand.command = "GetAllPlaylists"
    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)

    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    data = bytearray()
    while (replyLen > len(data)):
        data += s.recv(replyLen - len(data))
    replyCommand = pickle.loads(data)
    print("Reply: ",replyCommand.command)
    print("Playlists: ", replyCommand.payload)
    return replyCommand.payload

def getPlaylist(listID, s):
    #a.	Command = GETPLAYLIST <playlistID>
    #b.	Payload = none
    getCommand = Command()
    getCommand.command = "GetPlaylist,"+listID
    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)

    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    data = bytearray()
    while (replyLen > len(data)):
        data += s.recv(replyLen - len(data))
    replyCommand = pickle.loads(data)
    print("Reply: ",replyCommand.command)
    print("Playlist:", replyCommand.payload)
    return replyCommand.payload
    
def addSongToList(songID,listID,s):
    #a.	Command = ADDSONGTOLIST/REMOVESONGFROMLIST <songID> <listID>
    #b.	Payload = none
    try:
        getCommand = Command()
        getCommand.command = "AddSongToList,"+songID+","+ listID
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        print("Reply: ",replyCommand.command)
        
    except Exception as e:
        print("Error occured: ", e)

def removeSongFromList(songID,listID,s):
    try:
        getCommand = Command()
        getCommand.command = "RemoveSongFromList,"+ songID +','+listID
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        print("Reply: ",replyCommand.command)
        return replyCommand.command
    
    except Exception as e:
        print("Error occured: ", e)

def removeSong(songID,s):
    try:
        getCommand = Command()
        getCommand.command = "RemoveSong,"+ songID
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        print("Reply: ",replyCommand.command)
        
    except Exception as e:
        print("Error occured: ", e)
        
class Command:
    command = ""
    payload = ""

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        global s
        
        #frm1 _ all available songs
        self.frm1 = tk.Frame(self)
        self.frm1_1 = tk.Frame(self.frm1)
        self.title1 = tk.Label(self.frm1_1, text = "All available songs",fg = "red")
        self.title1.pack(side = "left")
        self.playButton1 = tk.Button(self.frm1_1, text = "Play")
        self.playButton1.pack(side = "right")
        self.frm1_1.pack(side = "top")
        self.songList = tk.Listbox(self.frm1, height = "10")
        self.slist = getSongList(s)
        for item in self.slist.keys():
            self.songList.insert("end", item + ","+ self.slist[item])
        self.songList.pack(side = "left")
        self.scrl1 = tk.Scrollbar(self.frm1)
        self.scrl1.pack(side = "right",fill = "y")
        self.songList['yscrollcommand'] = self.scrl1.set
        self.scrl1['command'] = self.songList.yview
        self.frm1.pack(side = "left")
        
        
        #frm2 _ main body
        self.frm2 = tk.Frame(self)
        self.title2 = tk.Label(self.frm2, text = "My Song Player",fg = "red",padx = 100)
        self.title2.pack(side = "top")
        
        #frm2_1 (for add song with songName and create playlist with list name)
        self.frm2_1 = tk.Frame(self.frm2)
        
        #frm2_1_1 (add song)
        self.frm2_1_1 = tk.Frame(self.frm2_1)
        self.songEntry = tk.Entry(self.frm2_1_1,width = "8")
        self.songEntry.pack(side = "left")
        self.nameLabel1 = tk.Label(self.frm2_1_1,text = "-songName")
        self.nameLabel1.pack(side = "left")
        self.addButton1 = tk.Button(self.frm2_1_1, text = "Add",command = self.clickAdd) 
        self.addButton1.pack(side = "right")
        self.frm2_1_1.pack(side = "top")
        
        #frm2_1_2 (create playlist)
        self.frm2_1_2 = tk.Frame(self.frm2_1)
        self.listEntry = tk.Entry(self.frm2_1_2,width = "8")
        self.listEntry.pack(side = "left")
        self.nameLabel2 = tk.Label(self.frm2_1_2,text = "-listName")
        self.nameLabel2.pack(side = "left")
        self.createButton = tk.Button(self.frm2_1_2, text = "Create", command = self.clickCreate) 
        self.createButton.pack(side = "right")        
        self.frm2_1_2.pack(side = "bottom")
        
        self.frm2_1.pack()

        #(for other operations) 
        #frm2_2 
        self.frm2_2 = tk.Frame(self.frm2)
        
        #frm2_2_1 (entries)
        self.frm2_2_1 = tk.Frame(self.frm2_2)
        self.songLabel = tk.Label(self.frm2_2_1,text = "songID:")
        self.songLabel.pack(side = "left")
        self.songIDEntry = tk.Entry(self.frm2_2_1,width = "4")
        self.songIDEntry.pack(side = "left")
        self.listLabel = tk.Label(self.frm2_2_1,text = "listID:")
        self.listLabel.pack(side = "left")
        self.listIDEntry = tk.Entry(self.frm2_2_1,width = "4")
        self.listIDEntry.pack(side = "right")    
        self.frm2_2_1.pack()

        #(for other operations) 
        self.deleteButton1 = tk.Button(self.frm2_2, text = "Delete Song", command = self.clickDelete) 
        self.deleteButton1.pack()
        self.addButton2 = tk.Button(self.frm2_2, text = "Add Song to Playlist", command = self.clickATP) 
        self.addButton2.pack()
        self.deleteButton2 = tk.Button(self.frm2_2, text = "Delete Song from Playlist", command = self.clickDFP)
        self.deleteButton2.pack()
        self.frm2_2.pack(side = "top")

        #EXIT 
        self.QUIT = tk.Button(self.frm2, text="QUIT", fg="red", command=root.destroy) 
        self.QUIT.pack(side = "bottom")
        self.frm2.pack(side = "left")
        
        #frm3 _ playlists
        self.frm3 = tk.Frame(self)
        self.frm3_1 = tk.Frame(self.frm3)
        self.title3 = tk.Label(self.frm3_1, text = "All PlayLists",fg = "red")
        self.title3.pack(side = "left")
        self.openButton = tk.Button(self.frm3_1, text = "Open", command = self.clickOpen) 
        self.openButton.pack(side = "right")
        self.frm3_1.pack(side = "top")
        self.playlists = tk.Listbox(self.frm3)
        self.plist = getAllPlaylists(s)
        for item in self.plist:
            self.playlists.insert("end", item)
        self.playlists.pack(side = "left")
        self.scrl3 = tk.Scrollbar(self.frm3)
        self.scrl3.pack(side = "right",fill = "y")
        self.playlists['yscrollcommand'] = self.scrl3.set
        self.scrl3['command'] = self.playlists.yview
        self.frm3.pack(side = "left")

        #frm4 _ songs in playlist
        self.frm4 = tk.Frame(self)
        self.frm4_1 = tk.Frame(self.frm4)
        self.title4 = tk.Label(self.frm4_1, text ="playlist...", fg = "red")
        self.title4.pack(side = "left")
        self.playButton2 = tk.Button(self.frm4_1, text = "Play")
        self.playButton2.pack(side = "right")
        self.frm4_1.pack(side = "top")
        self.playlist = tk.Listbox(self.frm4)
        self.playlist.pack(side = "left")
        self.scrl4 = tk.Scrollbar(self.frm4)
        self.scrl4.pack(side = "right",fill = "y")
        self.playlist['yscrollcommand'] = self.scrl4.set
        self.scrl4['command'] = self.playlist.yview
        self.frm4.pack(side = "right")

    def clickOpen(self): # associated with "open" button
        global s
        self.playlist.delete(0,"end") # clear the self.playlist
        listID = self.playlists.get(self.playlists.curselection()).split(',')[0]
        self.newlist = getPlaylist(listID,s)
        del self.newlist[0]
        for item in self.newlist:
            self.playlist.insert("end", item)
            
        
        
    def clickAdd(self): # associated with "add" button
        global s
        try:
            addSong(self.songEntry.get(),s)
            self.songList.delete(0,"end") # get updated self.songList
            self.slist = getSongList(s)
            for item in self.slist.keys():
                self.songList.insert("end", item + ","+ self.slist[item])
            self.playlist.delete(0,"end") # clear the self.playlist
        except Exception as e:
            tkinter.messagebox.showinfo(title = "ERROR", message = "Song is not found")

    def clickCreate(self): # associated with "create" button
        global s
        b = True
        test = self.listEntry.get()
        for item in self.plist:
            if item.split(',')[1] == test:
                b = False
        if b == False:
            tkinter.messagebox.showinfo(title = "ERROR", message = "Playlist is existed")
        else:
            createPlaylist(test,s)
            self.playlists.delete(0,"end") # get upated self.playlists
            self.plist = getAllPlaylists(s)
            for item in self.plist:
                self.playlists.insert("end", item)
            self.playlist.delete(0,"end") # clear the self.playlist
            
    def clickDelete(self): # associated with "Delete" button
        global s
        b = False
        test = self.songIDEntry.get()
        for item in self.slist:
            if item.split(',')[0] == test:
                b = True
        if b == False:
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target song")
        else:
            removeSong(test,s)
            self.songList.delete(0,"end") # get updated self.songList
            self.slist = getSongList(s)
            for item in self.slist.keys():
                self.songList.insert("end", item + ','+self.slist[item])
            self.playlist.delete(0,"end") # clear the self.playlist
            
    def clickATP(self):  # associated with "Add Song to Playlist" button
        global s
        b = False
        c = False
        songID = self.songIDEntry.get()
        listID = self.listIDEntry.get()
        for song in self.slist.keys():
            if song == songID:
                b = True
        for item in self.plist:
            if item.split(',')[0] == listID:
                c = True
        if (b == False)&(c == False):
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target song and playlist")
        elif (b == False):
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target song")
        elif(c == False):
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target playlist")
        else:
            addSongToList(songID,listID,s)
            self.playlist.delete(0,"end") # clear the self.playlist
            tkinter.messagebox.showinfo(title = "Done", message = "Target playlist updated")
            
    def clickDFP(self): # associated with "Delete Song from Playlist" button
        global s
        b = False
        c = False
        songID = self.songIDEntry.get()
        listID = self.listIDEntry.get()
        for song in self.slist.keys():
            if song == songID:
                b = True
        for item in self.plist:
            if item.split(',')[0] == listID:
                c = True
        if (b == False)&(c == False):
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target song and playlist")
        elif (b == False):
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target song")
        elif(c == False):
            tkinter.messagebox.showinfo(title = "ERROR", message = "No target playlist")
        else:
            check = removeSongFromList(songID,listID,s)
            self.playlist.delete(0,"end") # clear the self.playlist
            if check == "":
                tkinter.messagebox.showinfo(title = "ERROR", message = "No target in target playlist")
            else:
                tkinter.messagebox.showinfo(title = "Done", message = "Target playlist updated")

# to use this, you have to install this library first: pip install playsound
# this is kind of a hacky sound library.  There's no way to stop a song after it starts.

    def playSong1(self):
        global s
        for item in self.songList.keys():
            getSong(item, s)
            playsound.playsound(item+".mp3")
            
    def playSong2(self):
        global s
        temp = self.newlist.remove(self.newlist[0])
        for item in temp:
            getSong(item.split(',')[0],s)
            playsound.playsound(item+".mp3")
            
#this is my main driver script
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# GUI begining
root = tk.Tk()
app = Application(master=root)
app.mainloop()

#close the socket
s.close() 
