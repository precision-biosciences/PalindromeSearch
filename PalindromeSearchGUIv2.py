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

        ### Our topmost frame is called myContainer1
        self.myContainer1 = Frame(parent) 
        self.myContainer1.pack(expand=YES, fill=BOTH)

        #------ constants for controlling layout ------
        button_width = 10

        button_padx = "2m"
        button_pady = "1m"

        buttons_frame_ipadx = "1m"
        # -------------- end constants ----------------

        # top frame
        self.top_frame = Frame(self.myContainer1, background = "LightSteelBlue3")
        self.top_frame.pack(side=TOP,
            fill=BOTH,
            expand=YES,
            )  

        # bottom frame
        self.bottom_frame = Frame(self.myContainer1,
            borderwidth=5,
            height=50,
            background="LightSteelBlue3",
            ) 
        self.bottom_frame.pack(side=TOP,fill=X)  


        # left_frame
        self.left_frame = Frame(self.top_frame, background="LightSteelBlue3",
            borderwidth=5,
            height=250,
            width=50,
            ) 
        self.left_frame.pack(side=LEFT,fill=Y,ipadx = buttons_frame_ipadx)  


        ### right_frame
        self.right_frame = Frame(self.top_frame, background="LightSteelBlue3",
            )
        self.right_frame.pack(side=RIGHT,
            fill=BOTH,
            expand=YES,
            padx = "2m",
            pady = "2m"
            )  
            
#        inside right frame
        self.topright_frame = Frame(self.right_frame,background = "white",
            borderwidth=5, relief=RIDGE, width = 350)
        self.topright_frame.pack(side=TOP,fill=BOTH, expand = YES)
        self.txtArea = ScrolledText.ScrolledText(master = self.topright_frame, wrap = "none", height = 5)
        self.txtArea.pack(fill=BOTH, expand = YES)
        self.bottomright_frame = Frame(self.right_frame,background = "white",
            borderwidth=5, relief=RIDGE, width = 350)
        self.bottomright_frame.pack(side=TOP,fill=BOTH, expand = YES)
        self.txtAreatwo = ScrolledText.ScrolledText(master = self.bottomright_frame, wrap = WORD, height = 5)
        self.txtAreatwo.pack(fill=BOTH, expand = YES)

        # now we add the buttons to the buttons_frame
        
        self.button3 = Button(self.left_frame, command=self.button3Click)
        self.button3.configure(text="Import Seq", background="light gray")
        self.button3.configure(
            width=button_width,  
            padx=button_padx,    
            pady=button_pady     
            )

        self.button3.pack(side=TOP)
        self.button3.bind("<Return>", self.button3Click_a)
        
        self.button4 = Button(self.left_frame, command=self.button4Click)
        self.button4.configure(text="Process", background="light gray")
        self.button4.configure(
            width=button_width,  
            padx=button_padx,    
            pady=button_pady     
            )

        self.button4.pack(side=TOP)
        self.button4.bind("<Return>", self.button4Click_a)
        
        self.button5 = Button(self.left_frame, command=self.button5Click)
        self.button5.configure(text="Save to File", background="light gray")
        self.button5.configure(
            width=button_width,  
            padx=button_padx,    
            pady=button_pady     
            )

        self.button5.pack(side=TOP)
        self.button5.bind("<Return>", self.button5Click_a)
        
        self.button6 = Button(self.left_frame, command=self.button6Click)
        self.button6.configure(text="Clear", background="light gray")
        self.button6.configure(
            width=button_width,  
            padx=button_padx,    
            pady=button_pady     
            )

        self.button6.pack(side=TOP)
        self.button6.bind("<Return>", self.button6Click_a)

        self.button2 = Button(self.left_frame, command=self.button2Click)
        self.button2.configure(text="Close", background="light gray")
        self.button2.configure(
            width=button_width,  
            padx=button_padx,    
            pady=button_pady     
            )

        self.button2.pack(side=TOP)
        self.button2.bind("<Return>", self.button2Click_a)

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
        hit_list_tuple = [(k,v) for k, v in hit_list.iteritems()]
        hit_list_tuple.sort(key=lambda x:x[1][1], reverse=True)
        header = "Start,     Sequence,     Score\n"
        self.txtAreatwo.insert(END,header)
        for start,hit in hit_list_tuple:
            position = str(start)
            if len(str(start))<len(str(len(text_upper))):
                spaces_to_add = len(str(len(text_upper)))-len(str(start))
                for i in range(spaces_to_add):
                    position += " "
            resultone = position+","+ str(hit[0])+ ","+ str(hit[1])+"\n"
            self.result = resultone.replace("[u'","").replace("']","")
            self.txtAreatwo.insert(END, self.result)
#        self.txtAreatwo.insert(END,hit_list_tuple)


    
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
        
        
root = Tk()
myapp = MyApp(root)
root.mainloop()