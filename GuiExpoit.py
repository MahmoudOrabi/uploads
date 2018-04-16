import os, hashlib, re
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
import tkinter.font as tkFont
from collections import OrderedDict, defaultdict

win = tk.Tk()

class Tools():
    class Proxy():
        class HTTP():
            def Start(SESSION, PORTL):
                pass


class SESSIONS():
    def ID(l1, l2):
        for l1_id in l1:
            up = 0
            for l2_id in l2:
                if re.search(str(l1_id), str(l2_id)):
                    up = 1
            if up == 0:
                return (hashlib.md5(str(l1_id).encode()).hexdigest())

    def START(ID):
        pass

    def STOP(ID):
        pass

    def EXIT(ID):
        print('Exit ', ID)
        pass


class toolsGui():
    class TextEdit():
        def Set(Frame,Id,Code,Click, width, height, Line):
            class TextEdit(tk.Frame):
                def __init__(self,Id,Code,Click, x=179, y=10, l=80, *args, **kwargs):
                    tk.Frame.__init__(self, *args, **kwargs)
                    self.text = self.CustomText(self, width=x, height=y)
                    self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
                    self.text.configure(yscrollcommand=self.vsb.set)
                    self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
                    self.linenumbers = self.TextLineNumbers(self, width=l, height=10)
                    self.linenumbers.attach(self.text)

                    self.vsb.pack(side="right", fill="y")
                    self.linenumbers.pack(side="left", fill="y")
                    self.text.pack(side="right", fill="both", expand=True)

                    self.text.bind("<<Change>>", self._on_change)
                    self.text.bind("<Configure>", self._on_change)

                def _on_change(self, event):
                    self.linenumbers.redraw()

                class TextLineNumbers(tk.Canvas):
                    def __init__(self, *args, **kwargs):
                        tk.Canvas.__init__(self, *args, **kwargs)
                        self.textwidget = None

                    def attach(self, text_widget):
                        self.textwidget = text_widget

                    def redraw(self, *args):
                        '''redraw line numbers'''
                        self.delete("all")

                        i = self.textwidget.index("@0,0")
                        while True:
                            dline = self.textwidget.dlineinfo(i)
                            if dline is None: break
                            y = dline[1]
                            linenum = str(i).split(".")[0]
                            self.create_text(2, y, anchor="nw", text=linenum)
                            i = self.textwidget.index("%s+1line" % i)

                class CustomText(tk.Text):

                    def __init__(self, *args, **kwargs):
                        tk.scrolledtext.Text.__init__(self, *args, **kwargs)
                        self.tk.eval('''
                            proc widget_proxy {widget widget_command args} {

                                # call the real tk widget command with the real args
                                set result [uplevel [linsert $args 0 $widget_command]]

                                # generate the event for certain types of commands
                                if {([lindex $args 0] in {insert replace delete}) ||
                                    ([lrange $args 0 2] == {mark set insert}) || 
                                    ([lrange $args 0 1] == {xview moveto}) ||
                                    ([lrange $args 0 1] == {xview scroll}) ||
                                    ([lrange $args 0 1] == {yview moveto}) ||
                                    ([lrange $args 0 1] == {yview scroll})} {

                                    event generate  $widget <<Change>> -when tail
                                }

                                # return the result from the real widget command
                                return $result
                            }
                            ''')
                        self.tk.eval('''
                            rename {widget} _{widget}
                            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
                        '''.format(widget=str(self)))

            PACK = TextEdit(Id,Code,Click,width, Line, height, Frame)
            PACK.pack(side="top", fill="both", expand=True)
            return PACK

    class treeListBox():
        def Set(WIN,Id,Code,Click, element_header, element_list, Line,v=0):


            class treeListBox(object):
                def __init__(self, WIN,Id,Code,Clickto, element_header, element_list, height=10):
                    self.WIN = WIN
                    self.Id = Id
                    self.Code = Code
                    self.Clickto = Clickto
                    self.element_header = element_header
                    self.element_list = element_list
                    self.X = height
                    self.tree = None
                    self._setup_widgets()
                    self._build_tree()



                def OnDoubleClick(self, event):
                    try:
                        item = self.tree.selection()[0]
                        self.Clickto.Click('OnDoubleClick on',self.Id,self.Code,(self.tree.item(item, "text"),self.tree.item(item, "values")))
                    except:
                        pass
                def Click(self, event):
                    try:
                        item = self.tree.selection()[0]
                        self.Clickto.Click('clicked on',self.Id,self.Code,(self.tree.item(item, "text"),self.tree.item(item, "values")))
                    except:
                        pass
                def _setup_widgets(self):
                    container = ttk.Frame(self.WIN)

                    container.pack(fill='both', expand=True)
                    self.tree = ttk.Treeview(container, columns=self.element_header, show="headings",
                                             selectmode="extended")
                    vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
                    hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)

                    self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=self.X)
                    self.tree.grid(column=0, row=0, sticky='nsew', in_=container)

                    vsb.grid(column=1, row=0, sticky='ns', in_=container)
                    hsb.grid(column=0, row=1, sticky='ew', in_=container)
                    container.grid_columnconfigure(0, weight=1)
                    container.grid_rowconfigure(0, weight=1)

                def _build_tree(self):
                    def isnumeric(s):
                        """test if a string is numeric"""
                        for c in s:
                            if c in "1234567890-.":
                                numeric = True
                            else:
                                return False
                        return numeric

                    def change_numeric(data):
                        """if the data to be sorted is numeric change to float"""
                        new_data = []
                        try:
                            if isnumeric(data[0][0]):
                                # change child to a float
                                for child, col in data:
                                    new_data.append((float(child), col))
                                return new_data
                            return data
                        except:
                            pass

                    def sortby(tree, col, descending):
                        try:
                            """sort tree contents when a column header is clicked on"""
                            # grab values to sort
                            data = [(tree.set(child, col), child) for child in tree.get_children('')]
                            # if the data to be sorted is numeric change to float
                            data = change_numeric(data)
                            # now sort the data in place
                            data.sort(reverse=descending)
                            for ix, item in enumerate(data):
                                tree.move(item[1], '', ix)
                            # switch the heading so that it will sort in the opposite direction
                            tree.heading(col,command=lambda col=col: sortby(tree, col, int(not descending)))
                        except:
                            pass
                    for col in self.element_header:
                        try:
                            self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
                            self.tree.column(col, width=tkFont.Font().measure(col.title()))
                        except:
                            pass
                    self.tree.bind("<Double-1>", self.OnDoubleClick)
                    self.tree.bind("<<TreeviewSelect>>", self.Click)

                    for item in self.element_list:
                        self.tree.insert('', 'end', values=item, text=0)

                        for ix, val in enumerate(item):
                            col_w = tkFont.Font().measure(val)
                            if self.tree.column(self.element_header[ix], width=None) < col_w:
                                self.tree.column(self.element_header[ix], width=col_w)

            return treeListBox(WIN,Id,Code,Click, element_header, element_list, Line)

    class ButtonNotebook():
        imgdir = os.path.join(os.path.dirname(__file__), 'img')
        i1 = tk.PhotoImage("img_close", file=os.path.join(imgdir, '/usr/share/oscanner/cqure/repeng/icons/info.gif'))
        i2 = tk.PhotoImage("img_closeactive", file=os.path.join(imgdir,
                                                                '/usr/share/beef-xss/extensions/admin_ui/media/images/default/layout/tab-close-on.gif'))
        i3 = tk.PhotoImage("img_closepressed", file=os.path.join(imgdir,
                                                                 '/usr/share/beef-xss/extensions/admin_ui/media/images/default/layout/tab-close-on.gif'))
        style = ttk.Style()

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')

        style.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
        style.layout("ButtonNotebook.Tab", [
            ("ButtonNotebook.tab", {"sticky": "nswe", "children":
                [("ButtonNotebook.padding", {"side": "top", "sticky": "nswe",
                                             "children":
                                                 [("ButtonNotebook.focus", {"side": "top", "sticky": "nswe",
                                                                            "children":
                                                                                [("ButtonNotebook.label",
                                                                                  {"side": "left", "sticky": ''}),
                                                                                 ("ButtonNotebook.close",
                                                                                  {"side": "left", "sticky": ''})]
                                                                            })]
                                             })]
                                    })]
                     )

        def btn_press(event):
            try:
                x, y, widget = event.x, event.y, event.widget
                elem = widget.identify(x, y)
                index = widget.index("@%d,%d" % (x, y))

                if "close" in elem:
                    widget.state(['pressed'])
                    widget.pressed_index = index
            except:
                pass

        def btn_release(event):
            x, y, widget = event.x, event.y, event.widget

            if not widget.instate(['pressed']):
                return

            elem = widget.identify(x, y)
            index = widget.index("@%d,%d" % (x, y))

            if "close" in elem and widget.pressed_index == index:
                lid_up = widget.tabs()
                widget.forget(index)
                widget.event_generate("<<NotebookClosedTab>>")
                lid_back = widget.tabs()
                SESSIONS.EXIT(SESSIONS.ID(lid_up, lid_back))

            widget.state(["!pressed"])
            widget.pressed_index = None

        win.bind_class("TNotebook", "<ButtonPress-1>", btn_press, True)
        win.bind_class("TNotebook", "<ButtonRelease-1>", btn_release)

    class ScrollbarFrame():
        def on_configureScrollbar(event, canvas):
            # update scrollregion after starting 'mainloop'
            # when all widgets are in canvas
            canvas.configure(scrollregion=canvas.bbox('all'))

        def Set(WIN,width,height):
            canvas = tk.Canvas(WIN, width=width, height=height)
            scrollbar = tk.Scrollbar(WIN, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill='y')
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar = tk.Scrollbar(WIN, command=canvas.xview, orient=tk.HORIZONTAL)
            scrollbar.pack(side=tk.BOTTOM, fill='x')
            canvas.pack()
            canvas.configure(xscrollcommand=scrollbar.set)
            frame = tk.Frame(canvas)
            frame.bind('<Configure>',
                       lambda evant, canvas=canvas: toolsGui.ScrollbarFrame.on_configureScrollbar(evant, canvas))
            canvas.create_window((0, 0), window=frame, anchor='nw')
            return frame


element_header = ['Type                 ', 'Domain                         ', 'phat                 ', 'Param Name   ',
                  'Param Value   ', 'Header Name          ', 'Header Value          ', 'Data                   ',
                  'Ip              ', 'Port      ', 'SSL     ']
element_list = []


#ScrollbarFrame = toolsGui.ScrollbarFrame.Set(win)
# TextEdits = toolsGui.TextEdit.Set(ScrollbarFrame,10,100,10)
# treeListBox = toolsGui.treeListBox.Set(ScrollbarFrame,element_header,element_list,10)
# TextEdits.text.delete(1.0, 'end')
# treeListBox.tree.insert('', 1000000000, 1, text='Proxy_HTTP_History_Request_Headers_',values=[1])

class Tap():
    def ExitWin(WIN):
        tabContorl = ttk.Notebook(WIN, style='ButtonNotebook')
        tabs = ttk.Frame(tabContorl)
        return tabContorl

    def RootWin(WIN):
        tabContorl = ttk.Notebook(WIN)

        tabs = ttk.Frame(tabContorl)
        return tabContorl

    def New(WIN, Name):
        tabs = ttk.Frame(WIN)
        WIN.add(tabs, sticky='nw', text=str(Name))
        WIN.pack(expand=True, fill='both')
        return tabs
    def makeNew(Code,Id,Index,backIndex,RootIndex,Name):
        add = Tap.New(RootIndex, str(Name))
        Routeng(Code + 'New' + '>', hashlib.md5(str(add).encode()).hexdigest(), add, backIndex)
        return add
    def SetWindo(WIN, Dict, Codeback='', Type='Root'):
        if Type.upper() == 'Exit'.upper():
            RootWin = Tap.ExitWin(WIN)
        else:
            RootWin = Tap.RootWin(WIN)
        LIST = {}
        LIST['ID'] = hashlib.md5(str(RootWin).encode()).hexdigest()
        for Root in Dict.keys():
            Code = Codeback + Root
            if type(Dict[Root]) == list:
                index = Tap.New(RootWin, Root)
                NewTap = Tap.RootWin(index)
                for mkTap in Dict[Root]:
                    CodeDone = Code + '>' + mkTap + '>'
                    Index = Tap.New(NewTap, mkTap)
                    LIST[str(CodeDone)] = Index
                    if Type.upper() == 'Exit'.upper():
                        Routeng(CodeDone, hashlib.md5(str(Index).encode()).hexdigest(), Index,NewTap)
                    else:
                        Routeng(CodeDone, hashlib.md5(str(RootWin).encode()).hexdigest(), Index,NewTap)

            else:
                CodeDone = Code + '>'
                Index = Tap.New(RootWin, Root)
                LIST[str(CodeDone)] = Index
                if Type.upper() == 'Exit'.upper():
                    Routeng(CodeDone, hashlib.md5(str(Index).encode()).hexdigest(), Index,RootWin)
                else:
                    Routeng(CodeDone, hashlib.md5(str(RootWin).encode()).hexdigest(), Index,RootWin)
        return (RootWin,LIST)


class System_Desktop():
    class Linux():
        class TOP():
            def MINU(Code, Id, Index,backIndex):
                def CMD_NEW_MENU():
                    Tap.makeNew(Code, Id, Index, backIndex, RootIndex,'New')

                monty = ttk.LabelFrame(Index, text=' Mony Pythons ')
                monty.grid(column=0, row=0, padx=3, pady=10, sticky='nW')
                ttk.Button(monty, text='New Tab', command=CMD_NEW_MENU).grid(column=0, row=0)

                monty = ttk.Label(Index, text=' Mony Python ')
                monty.grid(column=0, row=1, padx=0, pady=0, sticky='nW')
                RootIndex = Tap.SetWindo(monty, {'Video': 0}, Code, 'exit')[0]
        class Video():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)
        class New():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)
                pass




    class Windows():
        class TOP():
            def MINU(Code, Id, Index,backIndex):
                def CMD_NEW_MENU():
                    Tap.makeNew(Code, Id, Index, backIndex, RootIndex,'New')

                monty = ttk.LabelFrame(Index, text=' Mony Pythons ')
                monty.grid(column=0, row=0, padx=3, pady=10, sticky='nW')
                ttk.Button(monty, text='New Tab', command=CMD_NEW_MENU).grid(column=0, row=0)

                monty = ttk.Label(Index, text=' Mony Python ')
                monty.grid(column=0, row=1, padx=0, pady=0, sticky='nW')
                RootIndex = Tap.SetWindo(monty, {'Video': 0}, Code, 'exit')[0]
        class Video():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)
        class New():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)

    class Android():
        class TOP():
            def MINU(Code, Id, Index,backIndex):
                def CMD_NEW_MENU():
                    Tap.makeNew(Code, Id, Index, backIndex, RootIndex,'New')

                monty = ttk.LabelFrame(Index, text=' Mony Pythons ')
                monty.grid(column=0, row=0, padx=3, pady=10, sticky='nW')
                ttk.Button(monty, text='New Tab', command=CMD_NEW_MENU).grid(column=0, row=0)

                monty = ttk.Label(Index, text=' Mony Python ')
                monty.grid(column=0, row=1, padx=0, pady=0, sticky='nW')
                RootIndex = Tap.SetWindo(monty, {'Video': 0}, Code, 'exit')[0]
        class Video():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)
        class New():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)

    class Mac_os():
        class TOP():
            def MINU(Code, Id, Index,backIndex):
                def CMD_NEW_MENU():

                    Tap.makeNew(Code, Id, Index, backIndex, RootIndex,'New')

                monty = ttk.LabelFrame(Index, text=' Mony Pythons ')
                monty.grid(column=0, row=0, padx=3, pady=10, sticky='nW')
                ttk.Button(monty, text='New Tab', command=CMD_NEW_MENU).grid(column=0, row=0)

                monty = ttk.Label(Index, text=' Mony Python ')
                monty.grid(column=0, row=1, padx=0, pady=0, sticky='nW')
                RootIndex = Tap.SetWindo(monty, {'Video': 0}, Code, 'exit')[0]

        class Video():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)

        class New():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Information'] = '0'
                MENU['Scanners'] = '0'
                MENU['Vulnerable'] = '0'
                MENU['Attacks'] = '0'
                MENU['Payloads'] = '0'
                Tap.SetWindo(Index, MENU,Code)
class Proxy():
    class HTTP():
        class TOP():
            def MINU(Code, Id, Index,backIndex):
                def CMD_NEW_MENU():

                    Tap.makeNew(Code, Id, Index, backIndex, RootIndex,'New')

                monty = ttk.LabelFrame(Index, text=' Mony Pythons ')
                monty.grid(column=0, row=0, padx=3, pady=10, sticky='nW')
                ttk.Button(monty, text='New Tab', command=CMD_NEW_MENU).grid(column=0, row=0)

                monty = ttk.Label(Index, text=' Mony Python ')
                monty.grid(column=0, row=1, padx=0, pady=0, sticky='nW')
                RootIndex = Tap.SetWindo(monty, {'Video': 0}, Code, 'exit')[0]

        class Video():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Intercept'] = '0'
                MENU['HTTP history'] = '0'
                MENU['IF COMMAND'] = ['Drop & Forward', 'Replace']
                MENU['Options'] = '0'
                Tap.SetWindo(Index, MENU,Code)

        class New():
            def MINU(Code, Id, Index,backIndex):
                MENU = OrderedDict()
                MENU['Intercept'] = '0'
                MENU['HTTP history'] = '0'
                MENU['IF COMMAND'] = '0'
                MENU['Options'] = '0'
                Tap.SetWindo(Index, MENU,Code)

            class Intercept():
                def Click(self,Type,Id,Code,value):
                    pass
                def MINU(Code, Id, Index,backIndex):
                    element_header = ['#        ','Masseg               ', 'Host               ', 'Method',
                                      'URL                ', 'Params  ', 'Edited  ', 'Status  ', 'Length  ',
                                      'MIME type  ', 'User-Agent           ', 'LHOST             ', 'Server      ',
                                      'RHOST           ', 'SSL  ']
                    element_list = []

                    globals()[str(Id) + str(Code)] = toolsGui.treeListBox.Set(Index,Id,Code,Proxy.HTTP.New.Intercept(), element_header, element_list,10)
                    MENU = OrderedDict()
                    MENU['Response'] = ['Raw', 'Headers', 'Data']
                    MENU['Request'] = ['Raw', 'Headers', 'Data']
                    MENU['If Drop & Forward'] = 0

                    TAP = Tap.SetWindo(Index, MENU, Code)


                    montys = ttk.LabelFrame(TAP[1][str(Code) + 'If Drop & Forward>'], text='Response')
                    montys.grid(column=0, row=0, padx=0, pady=0)

                    montys = ttk.Label(montys)
                    montys.grid(column=0, row=0, padx=0, pady=0)

                    monty = ttk.Label(montys)
                    monty.grid(column=0, row=0, padx=0, pady=0)
                    element_header = ['method                                ',
                                      'phat                                  ',
                                      'version                                 ']

                    element_list = []
                    globals()[str(Id) + str(Code) + 'If Drop & Forward>Response>Status'] = toolsGui.treeListBox.Set(monty,Id,str(Code + 'If Drop & Forward>Response>Status'),Proxy.HTTP.New.Intercept(),element_header,element_list,1)

                    montys = ttk.Label(montys)
                    montys.grid(column=0, row=1, padx=0, pady=0)

                    monty = ttk.Label(montys)
                    monty.grid(column=0, row=0, padx=0, pady=0)
                    element_header = ['Name                                                       ',
                                      'Value                                                        ']

                    element_list = []
                    globals()[str(Id) + str(Code) + 'If Drop & Forward>Response>Header'] = toolsGui.treeListBox.Set(monty,Id,str(Code + 'If Drop & Forward>Response>Header'),Proxy.HTTP.New.Intercept(),element_header,element_list,9)

                    montys = ttk.LabelFrame(TAP[1][str(Code) + 'If Drop & Forward>'], text='Request')
                    montys.grid(column=1, row=0, padx=0, pady=0)

                    montys = ttk.Label(montys)
                    montys.grid(column=0, row=0, padx=0, pady=0)

                    monty = ttk.Label(montys)
                    monty.grid(column=0, row=0, padx=0, pady=0)
                    element_header = ['method                                ',
                                      'phat                                  ',
                                      'version                                 ']
                    globals()[str(Id) + str(Code) + 'If Drop & Forward>Request>Status'] = toolsGui.treeListBox.Set(monty, Id, str(Code + 'If Drop & Forward>Request>Status'), Proxy.HTTP.New.Intercept(),
                                             element_header, element_list, 1)

                    montys = ttk.Label(montys)
                    montys.grid(column=0, row=1, padx=0, pady=0)

                    monty = ttk.Label(montys)
                    monty.grid(column=0, row=0, padx=0, pady=0)
                    element_header = ['Name                                                       ',
                                      'Value                                                         ']

                    element_list = []
                    globals()[str(Id) + str(Code) + 'If Drop & Forward>Request>Header'] = toolsGui.treeListBox.Set(monty, Id, str(Code + 'If Drop & Forward>Request>Header'), Proxy.HTTP.New.Intercept(),
                                             element_header, element_list, 9)

                    globals()[str(Id) + str(Code) + 'Response>Raw>'] = toolsGui.TextEdit.Set(TAP[1][str(Code) + 'Response>Raw>'],Id,str(Code + 'Response>Raw>'),Proxy.HTTP.New.Intercept(),182,50,15)
                    globals()[str(Id) + str(Code) + 'Request>Raw>'] = toolsGui.TextEdit.Set(TAP[1][str(Code) + 'Request>Raw>'],Id,str(Code + 'Request>Raw>'),Proxy.HTTP.New.Intercept(), 182, 50, 15)

                    element_header = ['Name                                                       ',
                                      'Value                                                      ',
                                      'Name Replace                                               ',
                                      'Value Replace                                             ']
                    element_list = []

                    globals()[str(Id) + str(Code) + 'Response>Headers>'] = toolsGui.treeListBox.Set(TAP[1][str(Code) + 'Response>Headers>'],Id,str(Code + 'Response>Headers>'),Proxy.HTTP.New.Intercept(),element_header,element_list,11)
                    globals()[str(Id) + str(Code) + 'Request>Headers>'] = toolsGui.treeListBox.Set(TAP[1][str(Code) + 'Request>Headers>'],Id,str(Code + 'Request>Headers>'),Proxy.HTTP.New.Intercept(), element_header, element_list,11)

                    Data = ttk.LabelFrame(TAP[1][str(Code) + 'Response>Data>'], text=' Text 2560KB')
                    Data.grid(column=0, row=0, padx=0, pady=0)
                    DataReplcae = ttk.LabelFrame(TAP[1][str(Code) + 'Response>Data>'], text=' Replace ')
                    DataReplcae.grid(column=0, row=1, padx=0, pady=0)
                    globals()[str(Id) + str(Code) + 'Response>Data>Data'] = toolsGui.TextEdit.Set(Data,Id,str(Code + 'Response>Data>Data'),Proxy.HTTP.New.Intercept(), 181, 50, 7)
                    globals()[str(Id) + str(Code) + 'Response>Data>DataReplcae'] = toolsGui.TextEdit.Set(DataReplcae,Id,str(Code + 'Response>Data>DataReplcae'),Proxy.HTTP.New.Intercept(), 181, 50, 7)

                    Data = ttk.LabelFrame(TAP[1][str(Code) + 'Request>Data>'], text=' Text ')
                    Data.grid(column=0, row=0, padx=0, pady=0)
                    DataReplcae = ttk.LabelFrame(TAP[1][str(Code) + 'Request>Data>'], text=' Replace ')
                    DataReplcae.grid(column=0, row=1, padx=0, pady=0)
                    globals()[str(Id) + str(Code) + 'Request>Data>Data'] = toolsGui.TextEdit.Set(Data,Id,str(Code + 'Request>Data>Data'),Proxy.HTTP.New.Intercept(), 181, 50, 7)
                    globals()[str(Id) + str(Code) + 'Request>Data>DataReplcae'] = toolsGui.TextEdit.Set(DataReplcae,Id,str(Code + 'Request>Data>DataReplcae'),Proxy.HTTP.New.Intercept(), 181, 50, 7)
                    # globals()[str(Id) + str(Code) + 'If Drop & Forward>Response>Status']
                    # globals()[str(Id) + str(Code) + 'If Drop & Forward>Response>Header']
                    # globals()[str(Id) + str(Code) + 'If Drop & Forward>Request>Status']
                    # globals()[str(Id) + str(Code) + 'If Drop & Forward>Request>Header']
                    # globals()[str(Id) + str(Code) + 'Response>Raw>']
                    #globals()[str(Id) + str(Code) + 'Response>Raw>'].text.insert("end", 'Test')

                    #globals()[str(Id) + str(Code) + 'Response>Raw>']
                    # globals()[str(Id) + str(Code) + 'Request>Raw>']
                    # globals()[str(Id) + str(Code) + 'Response>Headers>']
                    # globals()[str(Id) + str(Code) + 'Request>Headers>']
                    # globals()[str(Id) + str(Code) + 'Response>Data>Data']
                    # globals()[str(Id) + str(Code) + 'Response>Data>DataReplcae']
                    # globals()[str(Id) + str(Code) + 'Request>Data>Data']
                    # globals()[str(Id) + str(Code) + 'Request>Data>DataReplcae']
                    pass
            class HTTP_history():
                def Click(self,Type,Id,Code,value):
                    pass
                def MINU(Code, Id, Index,backIndex):
                    element_header = ['#        ', 'Host               ', 'Method',
                                      'URL                       ', 'Params  ', 'Edited  ', 'Status  ', 'Length  ',
                                      'MIME type  ', 'User-Agent           ', 'LHOST             ', 'Server      ',
                                      'RHOST                ', 'SSL  ']
                    element_list = []

                    globals()[str(Id) + str(Code)] = toolsGui.treeListBox.Set(Index,Id,Code,Proxy.HTTP.New.HTTP_history(), element_header, element_list,10)
                    MENU = OrderedDict()
                    MENU['Response'] = ['Raw', 'Headers', 'Data']
                    MENU['Request'] = ['Raw', 'Headers', 'Data']
                    TAP = Tap.SetWindo(Index, MENU, Code)
                    globals()[str(Id) + str(Code) + 'Response>Raw>'] = toolsGui.TextEdit.Set(TAP[1][str(Code) + 'Response>Raw>'],Id,str(Code + 'Response>Headers>'),Proxy.HTTP.New.HTTP_history(),182,50,15)
                    globals()[str(Id) + str(Code) + 'Request>Raw>'] = toolsGui.TextEdit.Set(TAP[1][str(Code) + 'Request>Raw>'],Id,str(Code + 'Response>Headers>'),Proxy.HTTP.New.HTTP_history(), 182, 50, 15)

                    element_header = ['Name                                                       ',
                                      'Value                                                      ',
                                      'Name Replace                                               ',
                                      'Value Replace                                             ']
                    element_list = []
                    globals()[str(Id) + str(Code) + 'Response>Headers>'] = toolsGui.treeListBox.Set(TAP[1][str(Code) + 'Response>Headers>'],Id,str(Code + 'Response>Headers>'),Proxy.HTTP.New.HTTP_history(),element_header,element_list,11)
                    globals()[str(Id) + str(Code) + 'Request>Headers>'] = toolsGui.treeListBox.Set(TAP[1][str(Code) + 'Request>Headers>'],Id,str(Code + 'Request>Headers>'),Proxy.HTTP.New.HTTP_history(), element_header, element_list,11)

                    Data = ttk.LabelFrame(TAP[1][str(Code) + 'Response>Data>'], text=' Text 2560KB')
                    Data.grid(column=0, row=0, padx=0, pady=0)
                    DataReplcae = ttk.LabelFrame(TAP[1][str(Code) + 'Response>Data>'], text=' Replace ')
                    DataReplcae.grid(column=0, row=1, padx=0, pady=0)
                    globals()[str(Id) + str(Code) + 'Response>Data>Data'] = toolsGui.TextEdit.Set(Data,Id,str(Code + 'Response>Data>Data'),Proxy.HTTP.New.HTTP_history(), 181, 50, 7)
                    globals()[str(Id) + str(Code) + 'Response>Data>DataReplcae'] = toolsGui.TextEdit.Set(DataReplcae,Id,str(Code + 'Response>Data>DataReplcae'),Proxy.HTTP.New.HTTP_history(), 181, 50, 7)

                    Data = ttk.LabelFrame(TAP[1][str(Code) + 'Request>Data>'], text=' Text ')
                    Data.grid(column=0, row=0, padx=0, pady=0)
                    DataReplcae = ttk.LabelFrame(TAP[1][str(Code) + 'Request>Data>'], text=' Replace ')
                    DataReplcae.grid(column=0, row=1, padx=0, pady=0)
                    globals()[str(Id) + str(Code) + 'Request>Data>Data'] = toolsGui.TextEdit.Set(Data,Id,str(Code + 'Request>Data>Data'),Proxy.HTTP.New.HTTP_history(), 181, 50, 7)
                    globals()[str(Id) + str(Code) + 'Request>Data>DataReplcae'] = toolsGui.TextEdit.Set(DataReplcae,Id,str(Code + 'Request>Data>DataReplcae'),Proxy.HTTP.New.HTTP_history(), 181, 50, 7)
                    #globals()[str(Id) + str(Code) + 'Response>Raw>']
                    #globals()[str(Id) + str(Code) + 'Request>Raw>']
                    #globals()[str(Id) + str(Code) + 'Response>Headers>']
                    #globals()[str(Id) + str(Code) + 'Request>Headers>']
                    #globals()[str(Id) + str(Code) + 'Response>Data>Data']
                    #globals()[str(Id) + str(Code) + 'Response>Data>DataReplcae']
                    pass
            class IF_COMMAND():
                def Click(self,Type,Id,Code,value):
                    print(Type,Id,Code,value)
                def MINU(Code, Id, Index,backIndex):
                    pass
            class Options():
                def Click(self,Type,Id,Code,value):
                    print(Type,Id,Code,value)
                def MINU(Code, Id, Index,backIndex):
                    IFDrop = {}
                    IFDrops = {}
                    IFDrop['Header'] = [(b'User-Agent', b':',
                                         b'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                                         b'\r\n')]
                    IFDrop['IFHeaderNum'] = [1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                    IFDrop['COMMAND'] = 'Forward'
                    IFDrop['RequestsCOMMAND'] = 'IF'

                    IFDrops['Header'] = [(b'Server', b':',
                                         True,
                                          b'\r\n')]
                    IFDrops['IFHeaderNum'] = [1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                    IFDrops['COMMAND'] = 'Forward'


                    globals()[str(Id) + str('HttpProxy_ResponseIFDrop')] = []
                    globals()[str(Id) + str('HttpProxy_ResponseIFDrop')].append(IFDrop)

                    globals()[str(Id) + str('HttpProxy_RequestsIFDrop')] = []
                    globals()[str(Id) + str('HttpProxy_RequestsIFDrop')].append(IFDrops)

                    IFReplace = {}

                    IFReplace['Header'] = [(b'User-Agent', b':', True, b'\r\n'), (b'Server', b':', True, b'\r\n'),
                                           (b'Transfer-Encoding', b':', True, b'\r\n'), (b'Host', b':', True, b'\r\n'),
                                           (b'Date', b':', True, b'\r\n')]
                    IFReplace['IFHeaderNum'] = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                    IFReplace['COMMAND'] = 'ReplaceLine'
                    IFReplace['ReplaceFile'] = ['/root/Desktop/list']
                    IFReplace['ReplaceLine'] = [(b'Etisalat - web dashboard', b'PASS', 'BASE64'),(b'01122588618', b'01122588611', 'BASE64')]

                    IFReplace['Encode'] = 'auto'
                    IFReplace['ReplaceHeader'] = [(b'Server', b'Server', True, b'Apache/1.1.11 (Debian)'),(b'User-Agent', b'User-Agent', True, b'Firefox/1.1')]
                    IFReplace['IFAppendHeader'] = []
                    IFReplace['DeleteHeader'] = []

                    globals()[str(Id) + str('HttpProxy_ResponseIFReplace')] = []
                    globals()[str(Id) + str('HttpProxy_ResponseIFReplace')].append(IFReplace)

                    globals()[str(Id) + str('HttpProxy_RequestsIFReplace')] = []
                    globals()[str(Id) + str('HttpProxy_RequestsIFReplace')].append(IFReplace)
                    from threading import Thread
                    background_thread = Thread(target=Tools.Proxy.HTTP.Start, args=([Id,'8083']))
                    background_thread.start()



def Routeng(Code, winfo_id, Index,backIndex):
    print(Code,winfo_id)
    if Code == 'System Desktop>Linux>':
        System_Desktop.Linux.TOP.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Linux>Video>':
        System_Desktop.Linux.Video.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Linux>New>':
        System_Desktop.Linux.New.MINU(Code, winfo_id, Index,backIndex)

    if Code == 'Proxy>HTTP>':
        Proxy.HTTP.TOP.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'Proxy>HTTP>Video>':
        Proxy.HTTP.Video.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'Proxy>HTTP>New>':
        Proxy.HTTP.New.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'Proxy>HTTP>New>Intercept>':
        Proxy.HTTP.New.Intercept.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'Proxy>HTTP>New>HTTP history>':
        Proxy.HTTP.New.HTTP_history.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'Proxy>HTTP>New>IF_COMMAND>':
        Proxy.HTTP.New.IF_COMMAND.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'Proxy>HTTP>New>Options>':
        Proxy.HTTP.New.Options.MINU(Code, winfo_id, Index,backIndex)

    elif Code == 'System Desktop>Windows>':
        System_Desktop.Windows.TOP.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Windows>Video>':
        System_Desktop.Windows.Video.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Windows>New>':
        System_Desktop.Windows.New.MINU(Code, winfo_id, Index,backIndex)

    elif Code == 'System Desktop>Android>':
        System_Desktop.Android.TOP.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Android>Video>':
        System_Desktop.Android.Video.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Android>New>':
        System_Desktop.Android.New.MINU(Code, winfo_id, Index, backIndex)

    elif Code == 'System Desktop>Mac os>':
        System_Desktop.Mac_os.TOP.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Mac os>Video>':
        System_Desktop.Mac_os.Video.MINU(Code, winfo_id, Index,backIndex)
    elif Code == 'System Desktop>Mac os>New>':
        System_Desktop.Mac_os.New.MINU(Code, winfo_id, Index,backIndex)


dbs = OrderedDict()
dbs['System Desktop'] = ['Linux', 'Windows', 'Android', 'Mac os']
dbs['Network'] = ['Ethernet interface', '802.11 Wireless', 'Bluetooth', 'RFID NFC']
dbs['Web Application'] = '0'
dbs['Proxy'] = ['HTTP', 'FTP', 'Socks']
dbs['Data'] = ['Network', 'System', 'File', 'Text']
dbs['Social Engineering'] = ['System Desktop', 'Network', 'Web Application']
Index = toolsGui.ScrollbarFrame.Set(win, 8000, 8000)

Tap.SetWindo(Index, dbs)

win.mainloop()
