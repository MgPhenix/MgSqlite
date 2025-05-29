from tkinter import Tk, Frame, Button, Label, ttk, Entry, StringVar,PhotoImage


class TableViewer(Tk):
    def __init__(self, table : object) -> None:
        super().__init__()
        self.geometry("600x400")
        self.title("MgSqlite Viewer")
        self.iconphoto(False,PhotoImage(file="MgSqlite/ressource/MgSqliteLogo.png"))
        self.table = table
        self.stringVar = StringVar()
        self.__createWidget()
        self.__loadData()

    def __createWidget(self):
        reaserchFrame = Frame(self,)
        reaserchFrame.pack(side="top",fill="x",pady=10)

        #Create the line for the reaserch
        label = Label(reaserchFrame, text = "🔍 Research : ")
        label.pack(side="left")
        self.entry = Entry(reaserchFrame,textvariable=self.stringVar)
        self.entry.pack(side="left",padx = 5)
        button = Button(reaserchFrame,text="Research",command = self.__searchVal)
        button.pack(side="left")


        #The fucking table (absolutely no idea how i'm gonna do that)
        tableView = Frame(self)
        tableView.pack(side="top",fill="both",expand=True)

        self.tree = ttk.Treeview(tableView, columns=self.table.columns,show = "headings")
        for col in self.table.columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=150)
        self.tree.pack(side = "top",fill="both",expand=True)
        

    def __loadData(self, keyword=""):
        if keyword:
            value = []
            for column in self.table.columns:
                value.append((column,keyword))
            rows = self.table._selectValuesOR(self.table.columns,value)
        else:
            rows = self.table.selectAll()
        print(rows)
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for row in rows:
            self.tree.insert("","end", values=row)

    def __searchVal(self):
        keyword = self.entry.get()
        self.__loadData(keyword)
