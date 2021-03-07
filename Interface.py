import SudokuSolver
from tkinter import Tk,Button,Toplevel,Label,Entry,Frame
import os

class Display():
    def __init__(self):
        self.display = Tk()
        self.selectedNumber = " "

    def initDisplay(self):
        self.display.configure(bg='black')
        self.display.title("Sudoku Solver")
        self.display.geometry("400x375")
        self.frame = Frame(self.display, width=400, height=375,bg ='black')
        self.frame.bind("<Key>",self.key)
        self.frame.bind("<Button-1>", self.callback)
        self.frame.pack()
        self.selectedNumberText = Label(self.frame, text="Selected Number: ",bg='black',fg='white')
        self.selectedNumberText.place(x=25,y=25*14)

    def key(self,event):
        change = False
        if(event.char) == "0":
            num = " "
            change = True
        else:
            try:
                num = str(int(event.char))
                change = True
            except: pass
        if change:
            self.selectedNumberText.configure(text="Selected Number: {}".format(num))
            self.selectedNumber = "{}".format(num)

    def callback(self,event):
        self.frame.focus_set()

    def createButtons(self):
        self.createEnterButtons()
        self.createGridButtons()
        self.otherButtons()

    def otherButtons(self):
        self.OtherButtons = {}
        self.createOtherButtons()
        self.placeOtherButtons()

    def createOtherButtons(self):
        bWidth = 8
        self.OtherButtons["Solve"] = Button(self.display, text="Solve",width=bWidth,command= self.solvePress)
        self.OtherButtons["ClearButton"] = Button(self.display, text="Clear Grid",width=bWidth,command= self.clearButtonPress)
        self.OtherButtons["Save"] = Button(self.display, text="Save",width=bWidth,command= self.savePress)
        self.OtherButtons["Load"] = Button(self.display, text="Load",width=bWidth,command= self.loadPress)
        self.OtherButtons["Exit"] = Button(self.display, text="Exit",width=bWidth,command= self.display.destroy)
        #self.OtherButtons["ChangeSelection"] = Button(self.display, text="Change Selection Method",width=14,command= self.) # Add a way to change to click box and press key or button to enter

    def placeOtherButtons(self):
        xpos = 25*13
        self.OtherButtons["Solve"].place(x=xpos,y=75)
        self.OtherButtons["ClearButton"].place(x=25*13,y=100)
        self.OtherButtons["Save"].place(x=xpos,y=125)
        self.OtherButtons["Load"].place(x=xpos,y=150)
        self.OtherButtons["Exit"].place(x=xpos,y=175)

    def createGridButtons(self):
        k = 25
        self.gridButtons = {}
        for i in range(81):
            yval = int(i/9)*k
            xSpacing = k+(int((i%9)/3)*k)
            ySpacing = k+(int(i/27)*k)

            self.gridButtons["b{}".format(i)] = Button(self.display, text = " ",width = 2,command= lambda num = i: self.gridButtonPress(num))
            self.gridButtons["b{}".format(i)].place(x=xSpacing+((i%9)*k), y=ySpacing+yval)
    
    def createEnterButtons(self):
        self.enterButtons = {}
        self.enterButtons["b0"] = Button(self.display, text=" ",width = 2,command= lambda: self.enterButtonPress(" "))
        self.enterButtons["b0"].place(x=30,y=25*13)
        for i in range(1,10):
            self.enterButtons["b{}".format(i)] = Button(self.display, text="{}".format(i),width = 2,command= lambda num = i: self.enterButtonPress(num))
            self.enterButtons["b{}".format(i)].place(x=30+i*25,y=25*13)

    def solvePress(self):
        startGrid = []
        for _ in range(9):
            startGrid.append([])
        for i in range(81):
            if self.gridButtons["b{}".format(i)]['text'] == " ":
                startGrid[int(i/9)].append(None)
            else:
                startGrid[int(i/9)].append(int(self.gridButtons["b{}".format(i)]['text']))

        endGrid = SudokuSolver.solver(startGrid)
        self.checkForRecursion(endGrid[1])
        self.setSolvedGrid(endGrid[0])

    def clearButtonPress(self):
        for i in range(81):
            self.gridButtons["b{}".format(i)].configure(text=" ")
    
    def savePress(self):
        text = []

        getText = Toplevel(self.display,bg='black')
        getText.geometry("300x75")
        label = Label(getText,text="Enter the name you want to save the sudoku under:",bg='black',fg='white')
        textHolder = Entry(getText,width = 1000)
        button = Button(getText,text="Done",command=lambda:self.done(getText,textHolder,text))
        label.place(x=0)
        textHolder.place(y=25)
        button.place(x=0,y=50)

        self.display.wait_window(getText)
        try:
            saveFile = open("Saves/{}.txt".format(text[0]), "w")
            for i in range(81):
                saveFile.write(self.gridButtons["b{}".format(i)]['text'])
            saveFile.close()
        except:
            pass

    def done(self,getText,textHolder,text):
        text.append(textHolder.get())
        getText.destroy()

    def loadPress(self):
        getLoad = Toplevel(self.display,bg='black')
        label = Label(getLoad,text="Click the sudoku you want to load:",bg='black',fg='white')
        label.place(x=0,y=0)

        text = []
        buttons = {}
        deleteButtons = {}
        i=25
        for filename in os.listdir("Saves"):
            name = filename[:len(filename)-4]
            buttons[name] = Button(getLoad,text=name,command=lambda n = filename:self.loadFile(getLoad,n,text))
            buttons[name].place(x=0,y=i)
            i+=25
        i=25
        for filename in os.listdir("Saves"):
            name = filename[:len(filename)-4]
            data = (buttons,name,deleteButtons)
            deleteButtons[name] = Button(getLoad,text="Delete",command= lambda dataI=data:self.delFile(dataI))
            deleteButtons[name].place(x=150,y=i)
            i+=25
        getLoad.geometry("200x{}".format(i))
        self.display.wait_window(getLoad)
        try:
            self.setGrid(text[0])
        except:
            pass

    def delFile(self,data): # data[0] is list of buttons, data[1] is name of wanted button, data[2] is delete buttons
        confirm = Toplevel(self.display,bg='black')
        label= Label(confirm,text="Are you sure you want to delete {}?".format(data[1]),bg='black',fg='white')
        label.place(x=0,y=0)
        yesButton = Button(confirm,text="Yes",command= lambda data = data,confirm = confirm:self.checkDelete(data,confirm))
        noButton = Button(confirm,text ="No",command= lambda confirm = confirm:self.checkDont(confirm))
        yesButton.place(x=0,y=25)
        noButton.place(x=35,y=25)
        confirm.geometry("300x50")
        
    def checkDelete(self,data,confirm):
        os.remove("Saves/{}".format("{}.txt".format(data[1])))
        data[0][data[1]].destroy()
        data[2][data[1]].destroy()
        confirm.destroy()

    def checkDont(self,confirm):
        confirm.destroy()

    def loadFile(self,getLoad,name,text):
        readFile = open("Saves/{}".format(name),"r")
        text.append(readFile.read())
        getLoad.destroy()

    def setGrid(self,text):
        for i in range(81):
            self.gridButtons["b{}".format(i)].configure(text=text[i])

    def gridButtonPress(self,num):
        self.gridButtons["b{}".format(num)].configure(text="{}".format(self.selectedNumber))

    def enterButtonPress(self,num):
        self.selectedNumberText.configure(text="Selected Number: {}".format(num))
        self.selectedNumber = "{}".format(num)

    def checkForRecursion(self,did):
        if did:
            window = Toplevel(self.display,bg='black')
            window.title("Notice")
            label = Label(window,text="Had to use brute force to solve",bg='black',fg='white')
            window.geometry("250x25")
            label.place(x=0,y=0)

    def setSolvedGrid(self,solved):
        for i in range(81):
            self.gridButtons["b{}".format(i)].configure(text=solved[i])

    def run(self):
        self.display.mainloop()

d = Display()
d.initDisplay()
d.createButtons()
d.run()