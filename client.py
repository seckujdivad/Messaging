#-*- coding: UTF-8 -*-
#Specify encoding

print('''Messaging program by David

TODO:
Reciprocating connections - only one person needs to connect to the other and you are fine
Add anti-spam etc
''')

global end, s, output, messages, sendfield, root, shutdown, fullscreen, postit, external_connections, glob_font, window, game_thread_hasher, ciphers, colours #All the global variables
global buttonrelief, file_upload_packet_size, recieve_all, flags, connect_to_host, spec_char, send_txt
fullscreen = False #Don't change
ontop = False      #Don't change
postit = False
end = False
external_connections = []
server_output = True #Show side panel with connection log
glob_font = ('', 10) #Default is ('', 10) - this will rescale the UI and the default is when the UI looks best
game_thread_hasher = 1
file_upload_packet_size = 15 #Split on uploads
spec_char = chr(167) #Symbol to separate uploads

import tkinter as tk
from tkinter import filedialog
import socket, threading, time, getpass, random, winsound, os, webbrowser, sys, base64
print('For those connecting to you:\nHost: ', end='') #Show hostname
print(socket.gethostname())

#Flags
flags = {'username':getpass.getuser(), #Default flag values in case they aren't in the file
         'rcmd':False, #A remote aid tool. Even if on, commands need to be approved
         'theme':'Themes/snow.py',
         'port_incoming':8000,
         'port_outgoing':8000,
         'contacts':[]}

try:
    file = open('flags.py', 'r')
    contents = eval(file.read())
    file.close()
    flags.update(contents)
except IOError:
    print('Error with flags - make sure file exists and you have the correct permissions')
except: #bad practice, but there could be any sort of error with the file
    print('Error with flags - check that it is error free - it should be a Python dictionary')

#Styling
buttonrelief = tk.FLAT #Self explanatory - flatten buttons
try:
    class colours: #Theming data
        theme = flags['theme']
        _theme_file = open(theme, 'r')
        _theme_contents = _theme_file.read()
        _theme_file.read()
        exec(_theme_contents) #Run code from theme
except: #bad practice, but running unknown code so I'm not doing too well anyway
    print("Couldn't load theme")
    while True:
        time.sleep(1) #would use pass, but it loops too fast and drains cpu checking condition
print("Using theme '" + colours.theme + '"')
print("WARNING: On Windows and Macintosh, scrollbars can't have themes applied to them") #Maybe this isn't true, but it isn't my top priority

#Cipher
class ciphers: #a simple ciphering tool from another program I wrote
    def encrypt(msg, key='sa.uh389d/hsj?34nm902'): #random string for key - don't change it
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
def show_games(): #Give list of games
    global game_thread_hasher
    def game_thread():
        gamewindow = tk.Tk()
        def start_snake(): #Run the snake program
            file = open('sharefile.txt', 'w')
            file.write('0')
            file.close()
            send_txt('gamestart~' + flags['username'] + ' just started a new game of Snake!')
            messages.insert(0, 'You just started a new game of Snake!')
            os.system('snake.vbs') #Run program
            time.sleep(2)
            cont = False
            while not cont:
                file = open('sharefile.txt')
                if not file.read() == 'No score':
                    cont = True
                file.close()
            try:
                file = open('sharefile.txt', 'r')
                fc = file.read()
                file.close()
                messages.insert(0, 'You just scored ' + fc + ' on Snake!')
                if fc == '0':
                    send_txt('gamescore~' + flags['username'] + ' just scored 0 on Snake for attempting to cheat!') #Pretty dumb filter, but it's better than nothing - cheating is seriously easy
                else:
                    send_txt('gamescore~' + flags['username'] + ' just scored ' + fc + ' on Snake!')
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

def relay(): #Recieve incoming connections
    time.sleep(0.3)
    global s, c, end
    end = False
    class s:
        port = flags['port_incoming']
        host = socket.gethostname()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
    s.server.listen(0)
    def handler(clientsocket, address, thread_number): #handle connections
        try:
            current_download = None
            while not end:
                data = ciphers.decrypt(recieve_all(clientsocket).decode())
                if current_download == None: #Post everything to chat - not very complicated
                    data = data.split('~')
                    if data[0] == 'chat' or data[0] == 'gamescore' or 'gamestart':
                        messages.insert(0, data[1])
                        output.insert(0, address[0] + ' - ' + data[0] + ': ' + data[1])
                    if data[0] == 'weblink':
                        messages.insert(0, 'Web link from ' + data[1])
                        output.insert(0, address[0] + ' - ' + data[0] + ': ' + data[1])
                    if data[0] == 'file':
                        output.insert(0, address[0] + ' - ' + data[0] + ': ' + data[1])
                        current_download = data[1].split(' - ')[1]
                        current_download = current_download.split('/')
                        current_download = current_download[len(current_download)-1]
                        messages.insert(0, 'File from ' + data[1].split(' - ')[0] + ' - ' + current_download)
                        file = open('Downloads/' + current_download, 'w')
                        file.write('')
                        file.close()
                    if data[0] == 'cmd_result':
                        messages.insert(0, 'Command result from ' + data[1])
                        output.insert(0, address[0] + ' - ' + data[0] + ': ' + data[1])
                    if data[0] == 'cmd': #handle remote python code execution
                        output.insert(0, 'Command from ' + address[0] + ' - ' + data[1])
                        inp = data[1].split('&')
                        if len(inp) == 2:
                            if flags['rcmd']:
                                messages.insert(0, 'Command request - go to IDLE/command prompt') #Will hang on input()
                                choice = ''
                                print(address[0] + ' wants to run the command ' + inp[0][1:] + ' -  allow? [y/N]:')
                                while not choice in ['y', 'n']: #Confirm/deny incoming commands
                                    choice = input('').lower()
                                if choice == 'y':
                                    print('Request approved')
                                    try:
                                        result = eval(inp[0][1:])
                                    except:
                                        result = 'Error with code'
                                    send = str(result)
                                else:
                                    print('Request denied')
                                    send = 'rCmd request was denied'
                            else:
                                send = 'rCmd is turned off on the target'
                            send_to = None
                            for c in external_connections:
                                if c.server.getsockname()[0] == inp[1]:
                                    send_to = c
                                    break
                            if send_to == None:
                                print("Couldn't return data")
                            else:
                                try:
                                    send_to.server.send(bytes(ciphers.encrypt('cmd_result~' + flags['username'] + ' - ' + send), 'UTF-8'))
                                except:
                                    print("Couldn't return data")
                        else:
                            output.insert(0, 'Command faulty')
                else: #Mid way through download
                    d = data
                    file = open('Downloads/' + current_download, 'a')
                    for x in range(0, len(d), file_upload_packet_size + 11):
                        _towrite = d[x:x+file_upload_packet_size + 11][11:]
                        if _towrite.startswith(spec_char):
                            print('end')
                            current_download = None
                            break
                        else:
                            towrite = ''
                            for x in _towrite:
                                if x == spec_char:
                                    print('end')
                                    current_download = None
                                    break
                                else:
                                    towrite = towrite + x
                            file.write(towrite)
                    file.close()
        except ValueError:
            output.insert(0, address[0] + ' closed')
    threadhasher = 1
    while not end: #allow all connections
        output.insert(0, 'Ready for new connections')
        try:
            clientsocket, address = s.server.accept()
            handling_thread = threading.Thread(target=handler, args=(clientsocket, address, threadhasher), name='Handling thread #' + str(threadhasher))
            handling_thread.start()
            output.insert(0, 'Connection started to ' + address[0] + ' #' + str(threadhasher))
            threadhasher = threadhasher + 1
        except OSError: end = True
    print('Subrelay stopped')

def interactive_messages(messages): #Clicking on files and weblinks
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
    except tk.TclError or RuntimeError:
        end = True
    print('Interactive messages stopped')

#Functions
def create_new_connection(self=None): #Relay for host chooser
    global external_connections, targetid
    choice = targetid.get()
    def contactslist():
        menu = tk.Tk()
        menu.title('Contacts')
        li = tk.Listbox(menu)
        liscroll = tk.Scrollbar(menu, background=colours.superlight)
        li = tk.Listbox(menu, yscrollcommand=liscroll.set, width=30, height=13, font=glob_font, background=colours.superlight, relief=buttonrelief)
        liscroll.config(command=li.yview)
        li.pack(side=tk.RIGHT, fill=tk.X)
        liscroll.pack(side=tk.RIGHT, fill=tk.Y)
        for entry in flags['contacts']:
            li.insert(tk.END, entry[0] + ' - ' + entry[1])
        menu.mainloop()
    if choice == '':
        thread = threading.Thread(target=contactslist, daemon=True)
        thread.start()
    else:
        output = connect_to_host(choice)
        if output:
            targetid.delete(0, tk.END)

def connect_to_host(chosen_host): #Add new connection
    global external_connections
    try:
        crf = False
        class c:
            port = flags['port_outgoing']
            host = chosen_host
            if host == '':
                host = socket.gethostname()
        try:
            c.server = socket.create_connection((c.host, c.port))
        except ConnectionRefusedError:
            crf = True
            #cfgwindow.destroy()
        if not crf:
            external_connections.append(c)
    except socket.gaierror or ConnectionRefusedError: #Client isn't running on port
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
        return False #Give status
    return True

def recieve_all(socket): #Downloader
    buffer = 4096 #4 KB
    data = b""
    while True:
        part = socket.recv(buffer)
        data = data + part
        if len(part) < buffer:
            break
    return data

def send_msg(self=None): #'send a cheeky message' - self is the event when bound to return
    'Send normal or weblink-style messages'
    msg = sendfield.get()
    sendfield.delete(0, tk.END)
    if msg != '' and msg[0] == '@':
        msg = msg[1:]
        send_txt('weblink~' + flags['username'] + ' - ' + msg)
        messages.insert(0, 'Web link from me - ' + msg)
    elif msg != '' and msg[0] == '$':
        try:
            msg = msg.split('>')
            if len(msg) == 3:
                messages.insert(0, 'me - ' + msg[0] + '>' + msg[1] + '>' + msg[2])
                send_txt('cmd~' + msg[0] + '&' + msg[2], spec_ip=msg[1])
            else:
                output.insert(0, 'rCmd is $cmd>address>return')
        except NameError:
            print('Error sending message: please continue connection setup in the other window')
    elif msg != '':
        try:
            messages.insert(0, 'me - ' + msg)
            send_txt('chat~' + flags['username'] + ' - ' + msg)
        except NameError:
            print('Error sending message: please continue connection setup in the other window')

def send_file():
    'send file - field is the text entry'
    file = filedialog.askopenfilename()
    if not file == '':
        print(file)
        flist = file.split('.')
        go = False
        if flist[len(flist)-1] == 'py' or flist[len(flist)-1] == 'txt' or flist[len(flist)-1] == 'bat': #Check/limit extension
            print('Correct file')
            file_obj = open(file)
            file_c = file_obj.read()
            file_obj.close()
            messages.insert(0, 'You sent a file: ' + file)
            for c in external_connections: #legacy sending method because i don't really need to update it
                try:
                    c.server.sendall(bytes(ciphers.encrypt('file~' + getpass.getuser() + ' - ' + file), 'UTF-8'))
                    for x in range(0, len(file_c), file_upload_packet_size):#Split up big files
                        tosend = file_c[x:x+file_upload_packet_size]
                        c.server.sendall(bytes(ciphers.encrypt('cont_upload' + tosend), 'UTF-8'))
                    c.server.sendall(bytes(ciphers.encrypt(spec_char), 'UTF-8'))
                    time.sleep(0.05)
                except socket.error:
                    print("[Error] A connection was closed, couldn't send file")

def send_txt(text, spec_ip=None): #Drastic simplification and unification of previous method
    'Send any text to all connections'
    for c in external_connections: #Send to all clients
        try:
            if spec_ip == None:
                c.server.send(bytes(ciphers.encrypt(text), 'UTF-8'))
            elif spec_ip == c.server.getpeername()[0]:
                c.server.send(bytes(ciphers.encrypt(text), 'UTF-8'))
            else:
                print(c.server.getpeername()[0], 'was rejected by the filter')
        except socket.error:
            output.insert(0, "Couldn't send text")
            print("[Error] A connection was closed, couldn't send text")

def shutdown():
    'Close all connections and window'
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
root.iconphoto(True, tk.PhotoImage(file='icon.gif'))
root.configure(background=colours.superlight)
root.bind(sequence='<Return>', func=send_msg) #Not recommended

#pack everything - so scratch made you think that UIs were simple?

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
#upload_name = tk.Entry(upload_frame, background=colours.superlight, font=glob_font)
upload_button = tk.Button(upload_frame, background=colours.light, relief=buttonrelief, font=glob_font, text='Upload', command=send_file, width=6)

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
upload_button.pack(side=tk.RIGHT, fill=tk.X)
#upload_name.pack(side=tk.RIGHT, fill=tk.X)
upload_label.pack(side=tk.RIGHT)

notif_frame.pack(fill=tk.BOTH)
notif_list_bar.pack(side=tk.RIGHT, fill=tk.Y)
notif_list.pack(side=tk.RIGHT, fill=tk.BOTH)

#                                                           Or to here on the first line
#48 characters max per line                     That's to the first "T"
notifs = '''Contacts list - leave the target blank and
sumbit to see a list of contacts. Edit the entry
in the flags.py file to add more.

New file sharing GUI - only works when running
in IDLE.

rCmd - remote aid tool. Send help through
messages - syntax:
$python code>target IP>your IP
eg. $1+1>192.168.137.1>192.168.137.1
IP not hostname!

Some core changes to program - any issues
please report to 113169@combertonvc.org along
with what you were doing at the time.

Fix for embedded gaming - embedded gaming
now works on the default Python install

File sharing! Just type the name of the file
(must be in the same folder as this program to
send it. Add the appropriate extension (ie .py
for Python files, .txt for Plain text files to
make sure it sends. The only restriction is that
you can't use the "''' + spec_char + '''" symbol - but who does?
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

#Finally - no more UI
#Start multithreading

relay_thread = threading.Thread(target=relay, name='Relay Thread')
relay_thread.start()

interactive_messages_thread = threading.Thread(target=lambda: interactive_messages(messages), name='Interactive messages thread')
interactive_messages_thread.start()

#

root.mainloop()
print('Window closed')
shutdown()
