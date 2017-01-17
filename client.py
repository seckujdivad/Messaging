#-*- coding: UTF-8 -*-
global end, s, output, messages, sendfield, root, shutdown, fullscreen, postit, external_connections, glob_font, window, game_thread_hasher, ciphers, colours
global buttonrelief, file_upload_packet_size, recieve_all
fullscreen = False #Don't change
ontop = False      #Don't change
postit = False
end = False
external_connections = []
server_output = True #Show side panel with connection log
glob_font = ('', 10) #Default is ('', 10) - this will rescale the UI and the default is when the UI looks best
game_thread_hasher = 1
file_upload_packet_size = 15 #Split on uploads

import tkinter as tk
import socket, threading, time, getpass, random, winsound, os, webbrowser, sys, base64
print('For those connecting to you:\nHost: ', end='')
print(socket.gethostname())

#Styling
buttonrelief = tk.FLAT
class colours:
    _theme_loc = open('theme.txt', 'r')
    theme = _theme_loc.read()
    _theme_loc.close()
    _theme_file = open(theme, 'r')
    _theme_contents = _theme_file.read()
    _theme_file.read()
    exec(_theme_contents)
print("Using theme '" + colours.theme + '"')
print("WARNING: On Windows and Macintosh, scrollbars can't have themes applied to them")

#Cipher
class ciphers:
    def encrypt(msg, key='sa.uh389d/hsj?34nm902'):
        try:
            out = ''
            chars = []
            for line in key:
                chars.extend(line)
            factor = 0
            for a in chars:
                factor = factor + ord(a)
            for i in msg:
                out = out + str((ord(i) * factor)) + '¬'
            return out
        except:
            print('Error encrypting')
            return 'Encryption error'
    def decrypt(msg, key='sa.uh389d/hsj?34nm902'):
        try:
            out = ''
            chars = []
            for line in key:
                chars.extend(line)
            factor = 0
            for a in chars:
                factor = factor + ord(a)
            for i in msg.split('¬'):
                if i == '':
                    ''
                else:
                    out = out + chr(int(int(i) / factor))
            return out
        except:
            print('Decryption error')
            return 'Decryption error'

#Threads
def show_games():
    global game_thread_hasher
    def game_thread():
        gamewindow = tk.Tk()
        def start_snake():
            file = open('sharefile.txt', 'w')
            file.write('0')
            file.close()
            for c in external_connections:
                c.server.send(bytes(ciphers.encrypt('gamestart~' + getpass.getuser() + ' just started a new game of Snake!'), 'UTF-8'))
            messages.insert(0, 'You just started a new game of Snake!')
            os.system('py snake.py')
            try:
                file = open('sharefile.txt', 'r')
                fc = file.read()
                file.close()
                messages.insert(0, 'You just scored ' + fc + ' on Snake!')
                for c in external_connections:
                    if fc == '0':
                        c.server.send(bytes(ciphers.encrypt('gamescore~' + getpass.getuser() + ' just scored 0 on Snake for attempting to cheat!'), 'UTF-8'))
                    else:
                        c.server.send(bytes(ciphers.encrypt('gamescore~' + getpass.getuser() + ' just scored ' + fc + ' on Snake!'), 'UTF-8'))
            except:
                print("Couldn't post data to chat")
        gamewindow.title('Games')
        gamewindow.configure(background=colours.superlight)
        snake_go = tk.Button(gamewindow, font=glob_font, text='Snake', command=start_snake, background=colours.light, relief=buttonrelief)
        snake_go.pack(fill=tk.X)
        gamewindow.mainloop()
    game_thread_t = threading.Thread(target=game_thread, name='Game window thread #' + str(game_thread_hasher), daemon=True)
    game_thread_t.start()
    game_thread_hasher = game_thread_hasher + 1

def relay():
    time.sleep(0.3)
    global s, c, end
    end = False
    class s:
        port = 8000
        host = socket.gethostname()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
    s.server.listen(0)
    def handler(clientsocket, address, thread_number):
        try:
            current_download = None
            while not end:
                data = ciphers.decrypt(recieve_all(clientsocket).decode())
                if current_download == None:
                    data = data.split('~')
                    if data[0] == 'chat' or data[0] == 'gamescore' or 'gamestart':
                        messages.insert(0, data[1])
                    if data[0] == 'weblink':
                        messages.insert(0, 'Web link from ' + data[1])
                        output.insert(0, address[0] + ' - ' + data[0] + ': ' + data[1])
                    if data[0] == 'file':
                        messages.insert(0, 'File from ' + data[1])
                        output.insert(0, address[0] + ' - ' + data[0] + ': ' + data[1])
                        current_download = data[1].split(' - ')[1]
                        file = open('Downloads/' + current_download, 'w')
                        file.write('')
                        file.close()
                else:
                    d = data
                    file = open('Downloads/' + current_download, 'a')
                    for x in range(0, len(d), file_upload_packet_size + 11):
                        _towrite = d[x:x+file_upload_packet_size + 11][11:]
                        if _towrite.startswith('§'):
                            print('end')
                            current_download = None
                            break
                        else:
                            towrite = ''
                            for x in _towrite:
                                if x == '§':
                                    print('end')
                                    current_download = None
                                    break
                                else:
                                    towrite = towrite + x
                            file.write(towrite)
                    file.close()
                    
        except SyntaxError:
            output.insert(0, address[0] + ' closed')
    threadhasher = 1
    while not end:
        output.insert(0, 'Ready for new connections')
        try:
            clientsocket, address = s.server.accept()
            handling_thread = threading.Thread(target=handler, args=(clientsocket, address, threadhasher), name='Handling thread #' + str(threadhasher))
            handling_thread.start()
            output.insert(0, 'Connection started as connection #' + str(threadhasher))
            threadhasher = threadhasher + 1
        except OSError: end = True
    print('Subrelay stopped')

def interactive_messages(messages):
    global end
    try:
        while not end:
            while messages.curselection() == (): time.sleep(0.2)
            curselection = messages.curselection()
            selection = messages.get(curselection[0])
            if selection.startswith('Web link from '):
                nselection = selection.split(' - ')
                print(nselection)
                webbrowser.open(nselection[1])
                try:
                    while selection == messages.get(messages.curselection()[0]): time.sleep(0.2)
                except IndexError:
                    pass
            if selection.startswith('File from ') and not selection.startswith('File from me'):
                nselection = selection.split(' - ')
                print(nselection)
                slash = '\ ' #Allows better use of \ - use slash[0]
                cmd = 'explorer.exe /select,"' + sys.path[0] + '\Downloads' + slash[0] + nselection[1] + '"'
                print(cmd)
                os.system(cmd)
                try:
                    while selection == messages.get(messages.curselection()[0]): time.sleep(0.2)
                except IndexError:
                    pass
            time.sleep(0.3)
    except tk.TclError or RuntimeError: end = True
    print('Interactive messages stopped')

#Functions
def create_new_connection(self=None):
    global external_connections, targetid
    try:
        crf = False
        class c:
            port = 8000
            host = targetid.get()
            if host == '': host = socket.gethostname()
        try:
            c.server = socket.create_connection((c.host, c.port))
        except ConnectionRefusedError:
            crf = True
            #cfgwindow.destroy()
        if not crf:
            external_connections.append(c)
            targetid.delete(0, tk.END)
    except socket.gaierror or ConnectionRefusedError:
        crf = True
    if crf:
        print("Couldn't find connection")
        noconnect = tk.Tk()
        noconnect.title("Couldn't connect")
        try:
            label = tk.Label(noconnect, text="Couldn't connect to " + targetid.get(), font=glob_font)
        except:
            label = tk.Label(noconnect, text="Couldn't connect to unknown host", font=glob_font)
        label.pack()
        noconnect.mainloop()

def recieve_all(socket):
    buffer = 4096 # 4 KB
    data = b""
    while True:
        part = socket.recv(buffer)
        data = data + part
        if len(part) < buffer:
            break
    return data

def send_msg(self=None):
    msg = sendfield.get()
    sendfield.delete(0, tk.END)
    if msg != '' and msg[0] == '@':
        msg = msg[1:]
        for c in external_connections:
            c.server.send(bytes(ciphers.encrypt('weblink~' + getpass.getuser() + ' - ' + msg), 'UTF-8'))
        messages.insert(0, 'Web link from me - ' + msg)
    elif msg != '':
        try:
            messages.insert(0, 'me - ' + msg)
            for c in external_connections:
                c.server.send(bytes(ciphers.encrypt('chat~' + getpass.getuser() + ' - ' + msg), 'UTF-8'))
        except NameError:
            print('Error sending message: please continue connection setup in the other window')

def send_file(field):
    file = field.get()
    field.delete(0, tk.END)
    print(file)
    flist = file.split('.')
    go = False
    if flist[len(flist)-1] == 'py' or flist[len(flist)-1] == 'txt' or flist[len(flist)-1] == 'bat': #Check extension
        print('Correct file')
        file_obj = open(file)
        file_c = file_obj.read()
        file_obj.close()
        messages.insert(0, 'File from me - ' + file)
        for c in external_connections:
            c.server.sendall(bytes(ciphers.encrypt('file~' + getpass.getuser() + ' - ' + file), 'UTF-8'))
            for x in range(0, len(file_c), file_upload_packet_size):#Split up big files
                tosend = 'cont_upload' + file_c[x:x+file_upload_packet_size]
                c.server.sendall(bytes(ciphers.encrypt(tosend), 'UTF-8'))
            c.server.sendall(bytes(ciphers.encrypt('§'), 'UTF-8'))
            time.sleep(0.05)
            

def shutdown():
    print('Closing...')
    try: s.server.close()
    except NameError: pass
    try: root.destroy()
    except tk.TclError: pass
    #exit()

def toggle_fullscreen():
    global fullscreen
    if fullscreen:
        fullscreen = False
        root.attributes('-fullscreen', False)
    else:
        fullscreen = True
        root.attributes('-fullscreen', True)

def toggle_ontop(ontop_arg):
    global ontop
    if ontop_arg:
        ontop = False
    else:
        ontop = True
    root.wm_attributes("-topmost", ontop)

root = tk.Tk()
root.title('Messaging')
root.configure(background=colours.superlight)
root.bind(sequence='<Return>', func=send_msg) #Not recommended


#

clientframe = tk.Frame(root, background=colours.superlight)
msgframe = tk.Frame(clientframe)
msgbar = tk.Scrollbar(msgframe, background=colours.superlight)
messages = tk.Listbox(msgframe, yscrollcommand=msgbar.set, width=70, height=38, font=glob_font, background=colours.superlight, relief=buttonrelief)
msgbar.config(command=messages.yview)
sendfield = tk.Entry(clientframe, width=60, font=glob_font, background=colours.superlight)
sendbutton = tk.Button(clientframe, text='Send', command=send_msg, font=glob_font, width=10, background=colours.light, relief=buttonrelief)

msgframe.pack(anchor='nw')
msgbar.pack(side=tk.RIGHT, fill=tk.Y)
messages.pack(side=tk.LEFT, fill=tk.BOTH)
sendfield.pack(side=tk.LEFT, fill=tk.X)
sendbutton.pack(side=tk.LEFT, fill=tk.X)

serverframe = tk.Frame(root, background=colours.superlight)
outframe = tk.Frame(serverframe, background=colours.superlight)
outputbar = tk.Scrollbar(outframe)
output = tk.Listbox(outframe, yscrollcommand=outputbar.set, width=40, height=20, font=glob_font, background=colours.superlight, relief=buttonrelief)
outputbar.config(command=output.yview)
shutbutton = tk.Button(serverframe, text='Shut down', command=shutdown, font=glob_font, background=colours.light, relief=buttonrelief)
addrlabel = tk.Label(serverframe, text='Your hostname: ' + socket.gethostname(), font=glob_font, background=colours.superlight)
togglefullscreenbutton = tk.Button(serverframe, text='Toggle fullscreen', command=toggle_fullscreen, font=glob_font, background=colours.light, relief=buttonrelief)
games = tk.Button(serverframe, text='More', font=glob_font, command=show_games, background=colours.light, relief=buttonrelief)
toggleontopbutton = tk.Button(serverframe, text='Toggle always on top', command=lambda: toggle_ontop(ontop), font=glob_font, background=colours.light, relief=buttonrelief)
upload_frame = tk.Frame(serverframe, background=colours.superlight)
upload_label = tk.Label(upload_frame, text='File', background=colours.superlight, relief=buttonrelief, font=glob_font)
upload_name = tk.Entry(upload_frame, background=colours.superlight, font=glob_font)
upload_button = tk.Button(upload_frame, background=colours.light, relief=buttonrelief, font=glob_font, text='Upload', command=lambda: send_file(upload_name), width=6)

notif_frame = tk.Frame(serverframe, background=colours.superlight)
notif_list_bar = tk.Scrollbar(notif_frame, background=colours.superlight)
notif_list = tk.Listbox(notif_frame, yscrollcommand=notif_list_bar.set, font=glob_font, width=40, height=9, background=colours.superlight, relief=buttonrelief)
notif_list_bar.config(command=notif_list.yview)

outframe.pack(anchor='nw', fill=tk.BOTH)
if server_output:
    outputbar.pack(side=tk.RIGHT, fill=tk.Y)
    output.pack(side=tk.RIGHT, fill=tk.BOTH)
addrlabel.pack(side=tk.BOTTOM, fill=tk.X)
shutbutton.pack(side=tk.BOTTOM, fill=tk.X)
togglefullscreenbutton.pack(side=tk.BOTTOM, fill=tk.X)
toggleontopbutton.pack(side=tk.BOTTOM, fill=tk.X)
games.pack(side=tk.BOTTOM, fill=tk.BOTH)
upload_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
upload_button.pack(side=tk.RIGHT)
upload_name.pack(side=tk.RIGHT, fill=tk.X)
upload_label.pack(side=tk.RIGHT)

notif_frame.pack(fill=tk.BOTH)
notif_list_bar.pack(side=tk.RIGHT, fill=tk.Y)
notif_list.pack(side=tk.RIGHT, fill=tk.BOTH)

#                                                           Or to here on the first line
#48 characters max per line                     That's to the first "T"
notifs = '''Fix for embedded gaming - embedded gaming
now works on the default Python install

File sharing! Just type the name of the file
(must be in the same folder as this program to
send it. Add the appropriate extension (ie .py
for Python files, .txt for Plain text files to
make sure it sends. The only restriction is that
you can't use the "§" symbol - but who does?
If you recieve a file, just click on it in chat.
Supported:
.txt
.py
.bat

Themes! Edit the reference in themes.txt to load
custom colours for the GUI - templates in the
Themes/ folder

Links! Try sending @www.google.com
Click on links in chat to open them

Multiple message support

Key-based cipher added

New integrated external games - click on the
"More" button
Only one game so far - Snake'''
notifs = notifs.split('\n')
for msg in notifs:
    notif_list.insert(tk.END, msg)

#Connection config
cfgwindow = tk.Frame(serverframe, background=colours.superlight)
leftframe = tk.Frame(cfgwindow)
rightframe = tk.Frame(cfgwindow)
targetidlabel = tk.Label(leftframe, text='Target hostname', font=glob_font, background=colours.superlight)
targetid = tk.Entry(rightframe, font=glob_font, background=colours.superlight)
targetidlabel.pack(anchor='nw')
targetid.pack(anchor='nw')
leftframe.pack(side=tk.LEFT)
rightframe.pack(side=tk.LEFT) #I know! It's for styling
start = tk.Button(cfgwindow, text='Submit', command=create_new_connection, font=glob_font, background=colours.light, relief=buttonrelief, width=6)
start.pack(anchor='s', fill=tk.X)
cfgwindow.pack(side=tk.LEFT)

#

clientframe.pack(side=tk.LEFT)
serverframe.pack(side=tk.RIGHT)

#

relay_thread = threading.Thread(target=relay, name='Relay Thread')
relay_thread.start()

interactive_messages_thread = threading.Thread(target=lambda: interactive_messages(messages), name='Interactive messages thread')
interactive_messages_thread.start()

#

root.mainloop()
print('Window closed')
shutdown()
