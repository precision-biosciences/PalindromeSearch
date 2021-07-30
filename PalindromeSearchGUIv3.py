# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 09:03:50 2014

@author: jlape
"""

from Tkinter import *
import ScrolledText
import tkFileDialog 

class MyApp:
    def __init__(self, parent):

        self.myParent = parent
        self.myParent.geometry("640x400")
        self.limit = None

#-----------------------Define topmost frame----------------------------------------------
        self.myContainer1 = Frame(parent) 
        self.myContainer1.pack(expand=YES, fill=BOTH)

#------------------------- constants for controlling layout ------------------------------
        button_width = 10

        button_padx = "2m"
        button_pady = "1        m"

        buttons_frame_ipadx = "1m"
        width_right_frame = 350
# ------------------------------------ end constants ------------------------------------

        # top frame
        self.top_frame = Frame(self.myContainer1, background = "LightSteelBlue3")
        self.top_frame.pack(side=TOP,fill=BOTH,expand=YES)  

        # bottom frame
        self.bottom_frame = Frame(self.myContainer1,borderwidth=5,height=50,
            background="LightSteelBlue3") 
        self.bottom_frame.pack(side=TOP,fill=X)  

        # left_frame
        self.left_frame = Frame(self.top_frame, background="LightSteelBlue3",
            borderwidth=5,height=250,width=50) 
        self.left_frame.pack(side=LEFT,fill=Y,ipadx = buttons_frame_ipadx)  

        # right_frame
        self.right_frame = Frame(self.top_frame, background="LightSteelBlue3",)
        self.right_frame.pack(side=RIGHT,fill=BOTH,expand=YES,padx = "2m",pady = "2m")  
            
        # inside right frame
        # top right frame
        self.topright_frame = Frame(self.right_frame,background = "white",
            borderwidth=5, relief=RIDGE, width = width_right_frame)
        self.topright_frame.pack(side=TOP,fill=BOTH, expand = YES)
        self.txtArea = ScrolledText.ScrolledText(master = self.topright_frame, wrap = "none", height = 5)
        self.txtArea.pack(fill=BOTH, expand = YES)
        self.txtArea.bind("<Tab>", self.OnTextTab)
        # bottom right frame
        self.bottomright_frame = Frame(self.right_frame,background = "white",
            borderwidth=5, relief=RIDGE, width = width_right_frame)
        self.bottomright_frame.pack(side=TOP,fill=BOTH, expand = YES)
        self.txtAreatwo = ScrolledText.ScrolledText(master = self.bottomright_frame, wrap = WORD, height = 5)
        self.txtAreatwo.pack(fill=BOTH, expand = YES)
        self.txtAreatwo.bind("<Tab>",self.OnTextTab)
        
        # inside left_frame
        # top left frame
        self.topleft_frame = Frame(self.left_frame,background = "LightSteelBlue3")
        self.topleft_frame.pack(side=TOP,fill=X,expand=NO,pady="3m") 
        # bottome left frame
        self.bottomleft_frame = Frame(self.left_frame,background = "LightSteelBlue3")
        self.bottomleft_frame.pack(side=TOP,fill=BOTH,expand=YES) 
        

        # now we add the buttons to the buttons_frame
        
        self.button3 = Button(self.topleft_frame, command=self.button3Click)
        self.button3.configure(text="Import Seq", background="light gray")
        self.button3.configure(width=button_width,padx=button_padx,pady=button_pady)

        self.button3.pack(side=TOP)
        self.button3.focus_force()
        self.button3.bind("<Return>", self.button3Click_a)
        
        self.button4 = Button(self.topleft_frame, command=self.button4Click)
        self.button4.configure(text="Process", background="light gray")
        self.button4.configure(width=button_width,padx=button_padx,pady=button_pady)
        
        self.button4.pack(side=TOP)
        self.button4.bind("<Return>", self.button4Click_a)
        
        self.button5 = Button(self.topleft_frame, command=self.button5Click)
        self.button5.configure(text="Save to File", background="light gray")
        self.button5.configure(width=button_width,padx=button_padx,pady=button_pady)

        self.button5.pack(side=TOP)
        self.button5.bind("<Return>", self.button5Click_a)

        self.button7 = Button(self.topleft_frame, command=self.button7Click)
        self.button7.configure(text="Clear Top", background="light gray")
        self.button7.configure(width=button_width,padx=button_padx,pady=button_pady)

        self.button7.pack(side=TOP)
        self.button7.bind("<Return>", self.button7Click_a)    
        
        self.button8 = Button(self.topleft_frame, command=self.button8Click)
        self.button8.configure(text="Clear Bottom", background="light gray")
        self.button8.configure(width=button_width,padx=button_padx,pady=button_pady)

        self.button8.pack(side=TOP)
        self.button8.bind("<Return>", self.button8Click_a)
        
        self.button6 = Button(self.topleft_frame, command=self.button6Click)
        self.button6.configure(text="Clear Both", background="light gray")
        self.button6.configure(width=button_width,padx=button_padx,pady=button_pady)

        self.button6.pack(side=TOP)
        self.button6.bind("<Return>", self.button6Click_a)

        self.button2 = Button(self.topleft_frame, command=self.button2Click)
        self.button2.configure(text="Close", background="light gray")
        self.button2.configure(width=button_width,padx=button_padx,pady=button_pady)

        self.button2.pack(side=TOP)
        self.button2.bind("<Return>", self.button2Click_a)
        
        # add combo box to bottom left frame
        choices = ['13','12','11','10','9','8','7','6','5','4','3','2','1']
        var = StringVar()
        var.set('0')
        self.OptionLabel = Label(self.bottomleft_frame, text="Set Lower Score Limit:")
        self.OptionLabel.configure(background="LightSteelBlue3")
        self.OptionLabel.pack(side=TOP)
        self.option = OptionMenu(self.bottomleft_frame,var,*choices,command = self.optionmenu)
        self.option.pack(side=TOP)
        
#---------------------define button actions-------------------------------------------
    def button2Click(self):
        '''Close'''
        self.myParent.destroy()
        
    def button3Click(self):
        '''Open, read, and clean a sequence file'''
        ftypes = [('Text Files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(master=self.topright_frame, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            dna_string = text.replace('\n','').replace('\r','').replace(" ","")
            self.dna_done = filter(lambda c: not c.isdigit(), dna_string)
            istart = 0
            for i in range(0,len(self.dna_done),100):
                if i>0:
                    dna_break = self.dna_done[istart:i]+"\n"
                    istart = i
                    self.txtArea.insert(END, dna_break)
            
    def button4Click(self):
        '''Process the sequence in the top window'''
        #Split the dna into a dictionary of start positions and kmers of the length given
        text = self.txtArea.get('1.0', END)
        text_clean = text.replace('\n','').replace('\r','').replace(" ","")
        text_done = filter(lambda c: not c.isdigit(),text_clean)
        text_upper = text_done.upper()
        kmers = self.split_dna_dict(text_upper,34)

        #Filter the kmers for those that have a TA at string positions 16 and 17
        kmer_filter = {start:kmer for start, kmer in kmers.iteritems() if kmer[0][16]=="T" and kmer[0][17]=="A"}

        #Create a dictionary of start positions: list of kmers and scores
        hit_list = self.output(kmer_filter)
        #Make the dictionary into a tuple to sort it by palindrome score
        hit_list_tuple = [(k,v) for k, v in hit_list.iteritems()]
        hit_list_tuple.sort(key=lambda x:x[1][1], reverse=True)
        if self.limit == None:
            self.limit = "0"
        hit_list_done = filter(lambda x:x[1][1] >= int(self.limit), hit_list_tuple)
        #Format the printout of the hit list tuple
        header = "Start,     Sequence,     Score\n"
        self.txtAreatwo.insert(END,header)
        for start,hit in hit_list_done:
            position = str(start)
            # Normalize the length of the starting position string so sequences line up
            if len(str(start))<len(str(len(text_upper))):
                spaces_to_add = len(str(len(text_upper)))-len(str(start))
                for i in range(spaces_to_add):
                    position += " "
            resultone = position+","+ str(hit[0])+ ","+ str(hit[1])+"\n"
            self.result = resultone.replace("[u'","").replace("']","")
            self.txtAreatwo.insert(END, self.result)
#        self.txtAreatwo.insert(END,self.limit)
#        self.txtAreatwo.insert(END,hit_list_done)
    
    def button5Click(self):
        '''Save the items in the bottom window'''
        f = tkFileDialog.asksaveasfile(mode="w",defaultextension=".txt")
        if f is None:
            return
        text2save = self.txtAreatwo.get('1.0',END)
        f.write(text2save)
        f.close()
        
    def button6Click(self):
        self.txtArea.delete('1.0',END)
        self.txtAreatwo.delete('1.0',END)
        
    def optionmenu(self, choice):
        self.limit = choice
        
    def button7Click(self):
        self.txtArea.delete('1.0',END)
    
    def button8Click(self):
        self.txtAreatwo.delete('1.0',END)
#-------------------------------map Return key binding for buttons----------------------
    def button2Click_a(self, event):
        self.button2Click()
        
    def button3Click_a(self, event):
        self.button3Click()
    
    def button4Click_a(self, event):
        self.button4Click()
        
    def button5Click_a(self, event):
        self.button5Click()
        
    def button6Click_a(self, event):
        self.button6Click()
        
    def button7Click_a(self, event):
        self.button6Click()
        
    def button8Click_a(self, event):
        self.button6Click()
#------------------------------fix tab order through text boxes-------------------------
    def _focusNext(self, widget):
        '''Return the next widget in tab order'''
        widget = self.myParent.call('tk_focusNext', widget._w)
        if not widget: return None
        return self.myParent.nametowidget(widget.string)

    def OnTextTab(self, event):
        '''Move focus to next widget'''
        widget = event.widget
        next = self._focusNext(widget)
        next.focus()
        return "break"
#------------------------------functions------------------------------------------------        
    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text
        
    def writeFile(self,filename,result):
        f = open(filename,"w")
        f.write(result)
        f.close()

    def calc_complement(self,my_dna):
        '''Calculates the complement of a dna sequence'''
        complement = ""
        for i in range(len(my_dna)):
            if my_dna[i] == "A":
                complement += "T"
            elif my_dna[i] == "T":
                complement += "A"
            elif my_dna[i] == "C":
                complement += "G"
            elif my_dna[i] == "G":
                complement += "C"
        return complement
    
        
    def split_dna_dict(self,dna, kmer_size):
        '''Splits the dna into a dictionary of start positions:kmers of kmer_size
        then returns the dictionary'''
        kmers = {}
        for start in range(0,len(dna)-(kmer_size-1),1):
            kmer = dna[start:start+kmer_size]
            try:
                kmers[start].append(kmer)
            except KeyError:
                kmers[start] = [kmer]
        return kmers
        
    def palindrome_score(self,string, score = 0):
        '''Counts the number of bases that are palindromic'''
        if len(string) <=1:
            return score
        else:
            if string[0] == string[-1]:
                score += 1
            return  self.palindrome_score(string[1:-1],score)
    
    def output(self,kmer_filter):
        '''Runs through a dictionary of start:kmer and appends the palindrome
        score onto the kmer value as a list'''
        output = {}
        for start, kmer in kmer_filter.iteritems():
            rev_kmer = self.calc_complement(kmer[0][21:])
            score = self.palindrome_score(kmer[0][:13]+rev_kmer)
            try:
                output[start+1].append([kmer,score])
            except KeyError:
                output[start+1] = [kmer,score]
        return output
#----------------------------------run GUI----------------------------------------------        
        
root = Tk()
myapp = MyApp(root)
root.mainloop()