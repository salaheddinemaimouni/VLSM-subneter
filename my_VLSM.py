import copy
L,l=[],[] #list de 2**i et de i=[0....32]
for i in range(1,33):
	L.append(2**i)
	l.append(i)
#print(l,L)
	
def ntobin(n,X): # entier to list binaire
    r=n%2
    X.insert(0,r)
    n=n//2
    if n==0: return [0]*(8-len(X))+X
    else: return ntobin(n,X)


def binlistto4x8oct(L): #list binaire to 8 octet dcml
    x=[]
    for i in range(0,32,8):
    	n,j=0,0
    	for e in L[i:i+8]:
    		n=n+e*(2**(7-j))
    		j=j+1
    	x.append(n)
    return x

def twobinlistproduct(L1,L2):
	x=[]
	for a,b in zip(L1,L2):
		x.append(a*b)
	return x

def bintodcml(bin):
    n=0
    for e,i in zip(bin,range(len(bin)-1,0,-1)):
    	n=n+e*(2**i)
    return n


def diffusionip(x):
        
    if x[3]==0:
        x[3]=255
        x[2]=x[2]-1
        if x[2]==-1:
            x[2]=255
            x[1]=x[1]-1
            if x[1]==-1:
                x[1]=255
                x[0]=x[0]-1
                if x[0]==-1:
                    print("erreur///")
    else:
        x[3]=x[3]-1 
    return x

class ipv4:
    
    def __init__(self,octs,mask):
        self.octs=octs
        self.mask=mask

    def ipv4bin(self):
        Y=[]
        for n in self.octs:
            X=[]
            for e in ntobin(n,X):
                Y.append(e)
        return Y

    def ipv4networkclass(self):
        if self.octs[0]<=126: return "A"
        elif self.octs[0]>126 and self.octs[0]<=191: return "B"
        elif self.octs[0]>191 and self.octs[0]<=223: return "C"
        elif self.octs[0]>223 and self.octs[0]<=239: return "D"
        elif self.octs[0]>239 and self.octs[0]<=254: return "E"
    
    def ipv4binmask(self):
        return ([1]*self.mask)+([0]*(32-self.mask))

    def ipv4subnetmask(self):
        return binlistto4x8oct(self.ipv4binmask())

    def ipv4firstadresse(self):
        x=twobinlistproduct(self.ipv4bin(),self.ipv4binmask())
        return binlistto4x8oct(x)

    def ipv4diffusion(self):
        x=twobinlistproduct(self.ipv4bin(),self.ipv4binmask())
        for b in range(len(x)-1,0,-1):
            if x[b]==0:
                x[b]=1
            else: break
        return binlistto4x8oct(x)

    def ipv4avaliablehosts(self):
        return (2**(32-self.mask))-2

 

class vlsm(ipv4):
    
    def __init__(self,octs,mask,hts):
        ipv4.__init__(self,octs,mask)
        self.hts=hts
        
    def masks(self):
        global L
        global l
        masque,i,j=[],0,0
        while i<len(self.hts):
            if self.hts[i]+2<=L[j]:
                masque.append(32-l[j])
                i,j=i+1,0
            else:
                j=j+1
        return masque

    def pas(self):
        ps=[]
        for msk in self.masks():
            ps.append(2**(32-msk))
        return ps

    def octet(self):
        global L
        x=[]
        for e in self.pas():
            if e <=L[7]:
                x.append(4)
            elif e>L[7] and e<=L[15]:
                x.append(3)
            elif e>L[15] and e<=L[23]:
                x.append(2)
            elif e>L[23] and e<=L[-1]:
                x.append(1)
        return x

    def moderedpas(self):
            ps=[]
            for e,c in zip(self.masks(),self.octet()):
                    if c==4:
                            ps.append(2**(32-e))
                    elif c==3:
                            ps.append(2**(32-e)//(2**8))
                    elif c==2:
                            ps.append(2**(32-e)//(2**16))
                    elif c==1:
                            ps.append(2**(32-e)//(2**24))
            return ps

    

    def network_adresses(self):
        networks=[binlistto4x8oct(twobinlistproduct(self.ipv4bin(),([1]*self.mask)+([0]*(32-self.mask))))]

        broadcasts=[]
        for octa,ps,i in zip(self.octet(),self.moderedpas(),range(len(self.octet()))):
            if octa==1 and networks[i][0]+ps<255:
                x=copy.copy(networks[i])
                x[0]=x[0]+ps
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
            elif octa==1 and networks[i][0]+ps>255:
                print("no more")
                break
            elif octa==2 and networks[i][1]+ps<255:
                x=copy.copy(networks[i])
                x[1]=x[1]+ps
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
            elif octa==2 and networks[i][1]+ps>255:
                x=copy.copy(networks[i])
                x[0]=x[0]+(ps//255)+1
                x[1],x[2],x[3]=0,0,0
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
            elif octa== 3 and networks[i][2]+ps<255:
                x=copy.copy(networks[i])
                x[2]=x[2]+ps
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
            elif octa==3 and networks[i][2]+ps>255:
                x=copy.copy(networks[i])
                x[1]=x[1]+(ps//255)+1
                x[2],x[3]=0,0
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
            elif octa==4 and networks[i][3]+ps<255:
                x=copy.copy(networks[i])
                x[3]=x[3]+ps
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
            elif octa==4 and networks[i][3]+ps>255:
                x=copy.copy(networks[i])
                x[2]=x[2]+(ps//255)+1
                x[3]=0
                networks.append(x)
                y=copy.copy(x)
                broadcasts.append(diffusionip(y))
        return [networks,broadcasts]


                        
                    
            
#print(vlsm([192,168,7,1],20,[1000,1000,100,100,50,50,10,10,4]).network_adresses())




from tkinter import *



root = Tk()
root.title("ipv4 vlsm subneting")

def checkOct(n):
   if type(n)==int and n<=255 and n>=0: return "good oct"
   elif type(n)==int and n>255 : return "oct>255"
   elif type(n)==int and n<0 : return "oct<0"
   else: return "not good oct"

def checkmask(msk):
   if type(msk)==int and msk>=0 and msk<=32: return "good mask"
   else: return "not good mask"
   
   
class GUIvlsm(Frame):
   
   def __init__(self,master=None):
      Frame.__init__(self,master)
      self.grid()
      self.createWidgets()
      
   def createWidgets(self):
      fieldWith=7
      clmspm=1
      #row 0
      self.inputTextAdresse = Label(self)
      self.inputTextAdresse["text"] = "input adresse ip :"
      self.inputTextAdresse.grid(row=0, column=0)

      self.inputFieldOct1 = Entry(self)
      self.inputFieldOct1["width"] = fieldWith
      self.inputFieldOct1.grid(row=0, column=1)

      self.point1 = Label(self)
      self.point1["text"] = "."
      self.point1.grid(row=0, column=2)

      self.inputFieldOct2 = Entry(self)
      self.inputFieldOct2["width"] = fieldWith
      self.inputFieldOct2.grid(row=0, column=3)

      self.point2 = Label(self)
      self.point2["text"] = "."
      self.point2.grid(row=0, column=4)

      self.inputFieldOct3 = Entry(self)
      self.inputFieldOct3["width"] = fieldWith
      self.inputFieldOct3.grid(row=0, column=5)

      self.point3 = Label(self)
      self.point3["text"] = "."
      self.point3.grid(row=0, column=6)

      self.inputFieldOct4 = Entry(self)
      self.inputFieldOct4["width"] = fieldWith
      self.inputFieldOct4.grid(row=0, column=7)

      self.slash = Label(self)
      self.slash["text"] = "/"
      self.slash.grid(row=0, column=8)

      self.mask = Entry(self)
      self.mask["width"] = fieldWith
      self.mask.grid(row=0, column=9)



      
      
      #row 1
      

      self.inputTextHosts = Label(self)
      self.inputTextHosts["text"] = "input hosts separated by coma ',' :"
      self.inputTextHosts.grid(row=2, column=0)

      self.inputhosts = Entry(self)
      self.inputhosts["width"] = 20
      self.inputhosts.grid(row=2, column=2,columnspan =7)
      




#row 10
      self.subnet = Button(self)
      self.subnet["text"] = "Subnet"
      self.subnet.grid(row=10, column=0,columnspan =10)
      self.subnet["command"] = self.subnetcommande

      #self.save = Button(self)
      #self.save["text"] = "save"
      #self.save.grid(row=10, column=5,columnspan =3)


#row 20

      self.notification = Label(self)
      self.notification["text"]="alertes"
      self.notification.grid(row=20, column=0,columnspan =10)


#row 31
      self.listout =  Listbox(self)
      self.listout["width"]=65
      self.listout .grid(row=31, column=0,columnspan =10)

   def subnetcommande(self):
      self.notification["text"]="alerts"
      self.listout.delete(0,END)
      try:
         oct1 = int(self.inputFieldOct1.get() )
         oct2 = int(self.inputFieldOct2.get())
         oct3 = int(self.inputFieldOct3.get())
         oct4 = int(self.inputFieldOct4.get())
         mask = int(self.mask.get())
         hosts = self.inputhosts.get()
         hosts = hosts.split(",")
         hats=[]
         for char in hosts:
            hats.append(int(char))
         hats.sort()
         hats.reverse()
         if checkOct(oct1)=="good oct" and checkOct(oct2)=="good oct" and checkOct(oct3)=="good oct" and checkOct(oct4)=="good oct" and checkmask(mask)=="good mask":
            objet = vlsm([oct1,oct2,oct3,oct4],mask,hats)
            self.listout.insert(END,"la classe du reseau est la classe "+objet.ipv4networkclass())
            self.insertinlistout(objet.network_adresses(),objet.masks(),hats)
         else:
            self.notification["text"] = "one value or more of octs or mask can't be coded in 8 bits"
         
      except ValueError:
         if self.inputFieldOct1.get()=="" or self.inputFieldOct2.get() =="" or self.inputFieldOct3.get()=="" or self.inputFieldOct4.get()=="" or self.mask.get()=="" or self.inputhosts.get()=="":
            self.notification["text"] = "there is an empty fieald"
         else:
            self.notification["text"] = "one or more of octs or mask or hosts is not an'integer "
            
   def insertinlistout(self,obj,mask,hosts):
   
      net,dif,lignes=obj[0],obj[1],[]
      for adresse,a,msk,diff,hts in zip(net,range(len(net)),mask,dif,hosts):
         ligne=".".join(str(v) for v in adresse)
         sligne=".".join(str(v) for v in diff)
         lignes.append("reseau de "+str(hts)+" htosts ; network :"+ligne+"/"+str(msk)+" broadcast :"+sligne)
      for ligne,i in zip(lignes,range(len(lignes))):
         self.listout.insert(i,ligne)
         


      

   


app = GUIvlsm(master=root)
root.resizable(0,0)

app.mainloop()




            
        


            
        
            

        

