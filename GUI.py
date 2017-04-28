from Tkinter import *
from ttk import *
import glob
import MySQLdb

#count = 0
db = MySQLdb.connect(host="localhost", user="root",passwd="123", db="Member")
cur = db.cursor()
#cur.execute("SELECT *FROM `Login`")
#db.commit()
class App(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
	
    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('DataTime','User')
	tv.heading("#0", text='item', anchor='w')
        tv.column("#0", anchor="w" )
	tv.heading('DataTime', text='DataTime')
        tv.column('DataTime', anchor="center",width=200)
        tv.heading('User', text='User')
        tv.column('User', anchor='center', width=200)
        
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self):
	
	self.treeview.delete(*self.treeview.get_children())
	#for _ in map(self.treeview.delete,self.treeview.get_children("")):
	#	pass
	count=0
	cur.execute("SELECT *FROM `Login`")
	db.commit()
    	for row in cur.fetchall():   
	    count+=1	    
	    self.treeview.insert('', 'end',text=count, values=(row[0],
                             row[1], ))
	



	#self.update()
	self.after(1000,self.LoadTable)   
	
def main():
    root = Tk()
    root.title("RFID Query ")
    App(root)
    
    root.mainloop()
   
if __name__ == '__main__':
    main()
