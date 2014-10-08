#------------------------------------------------------box-maker.py----#
#
#                  BOX   MAKER
#
# 
# Copyright (c) 2014 Matteo Perini
# Copyright (c) 2014 Alessandro Navarini
#
# The original code is written in java 
# Copyright (c) 2002 Rahul Bhargava
# https://github.com/rahulbot/boxmaker
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#-----------------------------------------------------------------------


'''
Programma per la prgettazione di Box su file svg con interfaccia 
grafica per l'inserimento dati da parte dell'utente
'''

#Importo le librerie per l'interfaccia grafica
from Tkinter import *
from tkMessageBox import *

#Costante per convertire i millimetri in pixel
from_mm_to_pixel = 3.5433071

#Funzione che crea il file svg
def BoxMaker(width, height, depth, thickness, notchLength, cutwidth, autom, coper):
    
    #Verifico se le dimensioni delle tacche sono su automatiche e, se si, calcolo la lunghezza
    if autom == "True":
        notchLength = thickness*2.5
    
    #Funzione per approssimare il numero delle tacche
    def closestOddTo(numd):
        num= int(numd+0.5)
        if(num % 2 == 0): 
            return int(num-1)
        return int(num)
        
    #Funzione per disegnare le linee orizzontali nel file svg    
    def drawHorizontalLine(x0,y0,notchWidth,notchCount,notchHieght,cutwidth,flip,smallside,fil):
        x=x0
        y=y0 
        for step in range(notchCount):
            if(((step%2)==0) != flip):
                y=y0
            else:
                y=y0+notchHieght
            if(step==0):
                if(smallside):
                    #fil.write('    <line x1="'+str(x+notchHieght)+'" y1="'+str(y)+'" x2="'+str(x+notchWidth+cutwidth)+'" y2="'+str(y)+'"/>\n')
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x+notchHieght,y,x+notchWidth+cutwidth,y))
                else:
                    #fil.write('    <line x1="'+str(x)+'" y1="'+str(y)+'" x2="'+str(x+notchWidth)+'" y2="'+str(y)+'"/>\n')
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y,x+notchWidth+cutwidth,y))
            elif (step==(notchCount-1)):
                #fil.write('    <line x1="'+str(x-cutwidth)+'" y1="'+str(y)+'" x2="'+str(x+notchWidth-notchHieght)+'" y2="'+str(y)+'"/>\n')
                fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x-cutwidth,y,x+notchWidth-notchHieght,y))
            elif (step%2==0):
                #fil.write('    <line x1="'+str(x-cutwidth)+'" y1="'+str(y)+'" x2="'+str(x+notchWidth+cutwidth)+'" y2="'+str(y)+'"/>\n')
                fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x-cutwidth,y,x+notchWidth+cutwidth,y))
            else:
                #fil.write('    <line x1="'+str(x+cutwidth)+'" y1="'+str(y)+'" x2="'+str(x+notchWidth-cutwidth)+'" y2="'+str(y)+'"/>\n')
                fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x+cutwidth,y,x+notchWidth-cutwidth,y))
            if (step<(notchCount-1)):
                if (step%2==0):
                    #fil.write('    <line x1="'+str(x+notchWidth+cutwidth)+'" y1="'+str(y0+notchHieght)+'" x2="'+str(x+notchWidth+cutwidth)+'" y2="'+str(y0)+'"/>\n')
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x+notchWidth+cutwidth,y0+notchHieght,x+notchWidth+cutwidth,y0))
                else:
                    #fil.write('    <line x1="'+str(x+notchWidth-cutwidth)+'" y1="'+str(y0+notchHieght)+'" x2="'+str(x+notchWidth-cutwidth)+'" y2="'+str(y0)+'"/>\n')
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x+notchWidth-cutwidth,y0+notchHieght,x+notchWidth-cutwidth,y0))
            x=x+notchWidth
    
    #Funzione per disegnare e linee verticali nel file svg   
    def drawVerticalLine(x0,y0,stepLength,numSteps,mlength,cutwidth,flip,smallside,fil):
        x=x0
        y=y0
        for step in range(numSteps):
            if(((step%2)==0) != flip):
                x=x0
            else:
                x=x0+mlength
            if (step==0):
                if(smallside):
                    #drawLineByMm(x,y+mlength,x,y+stepLength+cutwidth)
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y+mlength,x,y+stepLength+cutwidth))
                else:
                    #drawLineByMm(x,y,x,y+stepLength+cutwidth)
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y,x,y+stepLength+cutwidth))
            elif(step==(numSteps-1)):
                #g.moveTo(x,y+cutwidth); g.lineTo(x,y+stepLength); g.stroke()
                if(smallside):
                    #drawLineByMm(x,y-cutwidth,x,y+stepLength-mlength)
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y-cutwidth,x,y+stepLength-mlength))
                else:
                    #drawLineByMm(x,y-cutwidth,x,y+stepLength)
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y-cutwidth,x,y+stepLength))
            elif (step%2==0):
                #drawLineByMm(x,y-cutwidth,x,y+stepLength+cutwidth)
                fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y-cutwidth,x,y+stepLength+cutwidth))
            else:
                #drawLineByMm(x,y+cutwidth,x,y+stepLength-cutwidth)
                fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x,y+cutwidth,x,y+stepLength-cutwidth))
            if (step<(numSteps-1)):
                if (step%2==0):
                    #drawLineByMm(x0+mlength,y+stepLength+cutwidth,x0,y+stepLength+cutwidth)
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x0+mlength,y+stepLength+cutwidth,x0,y+stepLength+cutwidth))
                else:
                    #drawLineByMm(x0+mlength,y+stepLength-cutwidth,x0,y+stepLength-cutwidth)
                    fil.write('    <line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>\n'%(x0+mlength,y+stepLength-cutwidth,x0,y+stepLength-cutwidth))
            y=y+stepLength
    
    #Aumento le dimensioni per compensare quelle perse a causa dello spessore del taglio
    width+=cutwidth
    height+=cutwidth
    depth+=cutwidth
    
    #Calcolo del numero di tacche per ogni dimensione (Altezza, lunghezza e profondita')
    numNotchesW = closestOddTo(width / notchLength)
    numNotchesH = closestOddTo(height / notchLength)
    numNotchesD = closestOddTo(depth / notchLength)
    
    #Calcolo dell'esatta lunghezza delle tacche
    notchLengthW = width / float(numNotchesW)
    notchLengthH = height / float(numNotchesH)
    notchLengthD = depth / float(numNotchesD)
    
    #and compute the new width based on that (should be a NO-OP)
    margin=10.0+cutwidth
    
    width = numNotchesW*notchLengthW
    height = numNotchesH*notchLengthH
    depth = numNotchesD*notchLengthD
    
    boxPiecesWidth = (depth*2+width)
    boxPiecesHeight = (height*2+depth*2)
    
    #Apertura del file
    out_file=open('Box.svg','w')
    out_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    out_file.write('<svg\n')
    out_file.write('   xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
    out_file.write('   xmlns:cc="http://creativecommons.org/ns#"\n')
    out_file.write('   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
    out_file.write('   xmlns:svg="http://www.w3.org/2000/svg"\n')
    out_file.write('   xmlns="http://www.w3.org/2000/svg"\n')
    out_file.write('   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n')
    out_file.write('   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n')
    out_file.write('   width="'+str(boxPiecesWidth+margin*4)+'"\n')
    out_file.write('   height="'+str(boxPiecesHeight+margin*5)+'"\n')
    out_file.write('   id="svg2"\n')
    out_file.write('   version="1.1"\n')
    out_file.write('   inkscape:version="0.48.4 r9939">\n')
    out_file.write('  <sodipodi:namedview\n')
    out_file.write('     id="base"\n')
    out_file.write('     pagecolor="#ffffff"\n')
    out_file.write('     bordercolor="#666666"\n')
    out_file.write('     borderopacity="1.0"\n')
    out_file.write('     inkscape:pageopacity="0.0"\n')
    out_file.write('     inkscape:pageshadow="2"\n')
    out_file.write('     inkscape:zoom="0.35"\n')
    out_file.write('     inkscape:cx="500"\n')
    out_file.write('     inkscape:cy="500"\n')
    out_file.write('     inkscape:document-units="px"\n')
    out_file.write('     inkscape:current-layer="layer1"\n')
    out_file.write('     />\n')
    #out_file.write('  <g\n')
    #out_file.write('     inkscape:label="Livello 1"\n')
    #out_file.write('     inkscape:groupmode="layer"\n')
    #out_file.write('     id="layer1"\n')
    #out_file.write('     transform="translate(500,500)"\n')
    #out_file.write('     >\n')
    # Embed gear in group to make animation easier:
    #  Translate group, Rotate path.
    
    #Variabili per le coordinate di x e di y
    xOrig = 0.0
    yOrig = 0.0
        
    # compensate for the cut width (in part) by increasing mwidth (eolson)
    # no, don't do that, because the cut widths cancel out. (eolson)
    #       mwidth+=cutwidth/2; 
    
    
    xOrig = depth + margin*2
    yOrig = margin
    
    
    out_file.write('    <g fill="none" stroke="black" stroke-width="0.07086614" >\n')
    
    
    #1. a W x H side (il retro)
    if coper=="True":
        #Se bisogna fare il coperchio faccio le tacche sul lato alto
        drawHorizontalLine(xOrig,yOrig,notchLengthW,numNotchesW,thickness,cutwidth/2.0,False,False,out_file)				#top
    else:
        #Altrimenti tiro una riga dritta
        drawHorizontalLine(xOrig,yOrig,width-thickness-cutwidth/2,1,thickness,cutwidth/2.0,False,False,out_file)
    drawHorizontalLine(xOrig,yOrig+height-thickness,notchLengthW,numNotchesW,thickness,cutwidth/2,True,False,out_file)	#bottom
    drawVerticalLine(xOrig,yOrig,notchLengthH,numNotchesH,thickness,cutwidth/2.0,False,False,out_file)					#left
    drawVerticalLine(xOrig+width-thickness,yOrig,notchLengthH,numNotchesH,thickness,-cutwidth/2,False,False,out_file)	#right
    out_file.write('    </g>\n')
    out_file.write('    <g fill="none" stroke="black" stroke-width="0.07086614" >\n')

    #2. a D x H side (Il lato sinistro)
    xOrig = margin;
    yOrig = height + margin*2;
    if coper=="True":
        drawHorizontalLine(xOrig,yOrig,notchLengthD,numNotchesD,thickness,cutwidth/2,False,False,out_file)					#top
    else:
        drawHorizontalLine(xOrig,yOrig,depth-thickness-cutwidth/2,1,thickness,cutwidth/2,False,False,out_file)
    drawHorizontalLine(xOrig,yOrig+height-thickness,notchLengthD,numNotchesD,thickness,cutwidth/2,True,False,out_file)	#bottom
    drawVerticalLine(xOrig,yOrig,notchLengthH,numNotchesH,thickness,cutwidth/2,False,False,out_file)					#left
    drawVerticalLine(xOrig+depth-thickness,yOrig,notchLengthH,numNotchesH,thickness,-cutwidth/2,False,False,out_file)	#right
    out_file.write('    </g>\n')
    out_file.write('    <g fill="none" stroke="black" stroke-width="0.07086614" >\n')

    #3. a W x D side (il fondo)
    xOrig = depth + margin*2
    yOrig = height + margin*2
    drawHorizontalLine(xOrig,yOrig,notchLengthW,numNotchesW,thickness,-cutwidth/2,True,True,out_file)					#top
    drawHorizontalLine(xOrig,yOrig+depth-thickness,notchLengthW,numNotchesW,thickness,-cutwidth/2,False,True,out_file)	#bottom
    drawVerticalLine(xOrig,yOrig,notchLengthD,numNotchesD,thickness,-cutwidth/2,True,True,out_file)						#left
    drawVerticalLine(xOrig+width-thickness,yOrig,notchLengthD,numNotchesD,thickness,-cutwidth/2,False,True,out_file)	#right
    out_file.write('    </g>\n')
    out_file.write('    <g fill="none" stroke="black" stroke-width="0.07086614" >\n')

    #4. a D x H side (il lato destro)
    xOrig = depth + width + margin*3
    yOrig = height + margin*2
    if coper=="True":
        drawHorizontalLine(xOrig,yOrig,notchLengthD,numNotchesD,thickness,cutwidth/2,False,False,out_file)					#top
    else:
        drawHorizontalLine(xOrig,yOrig,depth-thickness-cutwidth/2,1,thickness,cutwidth/2,False,False,out_file)
    drawHorizontalLine(xOrig,yOrig+height-thickness,notchLengthD,numNotchesD,thickness,cutwidth/2,True,False,out_file)	#bottom
    drawVerticalLine(xOrig,yOrig,notchLengthH,numNotchesH,thickness,cutwidth/2,False,False,out_file)					#left
    drawVerticalLine(xOrig+depth-thickness,yOrig,notchLengthH,numNotchesH,thickness,-cutwidth/2,False,False,out_file)	#right
    out_file.write('    </g>\n')
    out_file.write('    <g fill="none" stroke="black" stroke-width="0.07086614" >\n')

    #5. a W x H side (il davanti)
    xOrig = depth + margin*2
    yOrig = height + depth+ margin*3
    if coper=="True":
        drawHorizontalLine(xOrig,yOrig,notchLengthW,numNotchesW,thickness,cutwidth/2,False,False,out_file)					#top
    else:
        drawHorizontalLine(xOrig,yOrig,width-thickness-cutwidth/2,1,thickness,cutwidth/2,False,False,out_file)
    drawHorizontalLine(xOrig,yOrig+height-thickness,notchLengthW,numNotchesW,thickness,cutwidth/2,True,False,out_file)	#bottom
    drawVerticalLine(xOrig,yOrig,notchLengthH,numNotchesH,thickness,cutwidth/2,False,False,out_file)					#left
    drawVerticalLine(xOrig+width-thickness,yOrig,notchLengthH,numNotchesH,thickness,-cutwidth/2,False,False,out_file)	#right
    out_file.write('    </g>\n')
    out_file.write('    <g fill="none" stroke="black" stroke-width="0.07086614" >\n')

    #6. a W x D side (il coperchio)
    #Disegna il coperchio solamente se la checkbox nella finestra e' selezionata
    if coper=="True":
        xOrig = depth + margin*2
        yOrig = height*2 + depth + margin*4
        drawHorizontalLine(xOrig,yOrig,notchLengthW,numNotchesW,thickness,-cutwidth/2,True,True,out_file)					#top
        drawHorizontalLine(xOrig,yOrig+depth-thickness,notchLengthW,numNotchesW,thickness,-cutwidth/2,False,True,out_file)	#bottom
        drawVerticalLine(xOrig,yOrig,notchLengthD,numNotchesD,thickness,-cutwidth/2,True,True,out_file)						#left
        drawVerticalLine(xOrig+width-thickness,yOrig,notchLengthD,numNotchesD,thickness,-cutwidth/2,False,True,out_file)	#right
        
    
    #chiusura del file svg
    out_file.write('    </g>\n')
    ##t = 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')'
    ##g_attribs = {inkex.addNS('label','inkscape'):'Gear' + str( teeth ),
    ##             'transform':t }
    ##g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)
    
    # Create SVG Path for gear
    ##style = { 'stroke': '#000000', 'fill': 'none' }
    ##gear_attribs = {'style':simplestyle.formatStyle(style), 'd':path}
    ##gear = inkex.etree.SubElement(g, inkex.addNS('path','svg'), gear_attribs )
    
    #out_file.write('<path\n')
    #out_file.write('d="'+path+'"\n')
    #out_file.write('style="fill:none;stroke:#000000" />\n')
    
    #out_file.write('  </g>')
    out_file.write('</svg>')
    out_file.close()
    
    #Avviso l'utente che il file e' pronto
    showinfo("Avviso", "Il file svg e' stato creato correttamente")

#Funzione che cotrolla se il contenuto delle caselle di testo e' numerico
def controllo(Input):
    try:
        variabile = float(Input)
        return float(Input)
    except:
        showerror("Errore", "Non hai inserito un valore numerico, riprova.")
        return None
        
#Funzione collegata al pulsante "Disegna"
def pulsante():
    continua = True     #Si recuperano i valori dalle caselle di testo e dalle checkbox
    udmm = udm.get()    #Unita' di misura selezionata
    width_ = controllo(larghezza.get().replace(",", "."))   #Larghezza
    height_ = controllo(altezza.get().replace(",", "."))    #Altezza
    depth_ =  controllo(profondita.get().replace(",", "."))     #Profondita'
    thickness_ = controllo(spessore_materiale.get().replace(",", "."))      #Spessore del materiale
    #Controllo se la lunghezza delle tacche e' su automatica
    if str(bool(autom.get()))=="True":
        notchLength_ = 0        #Se e' automatica metto 0 nella variabile per non ricevere errori
    else:
        notchLength_ = controllo(tacche.get().replace(",", "."))    #Altrimenti eseguo i controlli
    cutwidth_ = controllo(spessore_taglio.get().replace(",", "."))      #Spessore del taglio
    autom_ = str(bool(autom.get()))     #Lunghezza delle tacche automatica
    coper_ = str(bool(coper.get()))     #Coperchio
    
    if (width_<>None and height_<>None and depth_<>None and thickness_<>None and notchLength_<>None and cutwidth_<>None):       #Controlla se il valore delle variabili e' valido
        
        #Conversione inch --> millimetri
        if udmm=="inch":
            width_*=25.4
            height_*=25.4
            depth_*=25.4
            thickness_*=25.4
            notchLength_*=25.4
            cutwidth_*=25.4
            
        #Conversione centimetri --> millimetri
        elif udmm=="centimetri":
            width_*=10
            height_*=10
            depth_*=10
            thickness_*=10
            notchLength_*=10
            cutwidth_*=10
                 
        #Inizio dei controlli sui valori inseriti dall'utente
        
        if thickness_>=width_ or thickness_>=height_ or thickness_>=depth_:
            showwarning("Attenzione", "Lo spessore del materiale non puo' essere maggiore delle dimensioni della scatola, riprova")
            continua = False
        if height_>1000 or width_>1000 or depth_>1000:
            showwarning("Attenzione", "Le dimensioni della scatola non possono essere maggiori di 1 metro, riprova")
            continua = False
        if thickness_<1:
            showwarning("Attenzione", "Lo spessore del materiale non puo' essere inferiore a 1 millimetro, riprova")
            continua = False
        if thickness_>=30:
            showwarning("Attenzione", "Lo spessore del materiale non puo' essere maggiore a 30 millimetri, riprova")
            continua = False
        if  autom_ == "False":
            if notchLength_<=thickness_:
                showwarning("Attenzione", "La lunghezza delle tacche non puo' essere inferiore allo spessore del materiale, riprova")
                continua = False
        if  autom_ == "False":
            if notchLength_>(height_/2) or notchLength_>(width_/2) or notchLength_>(depth_/2):
                showwarning("Attenzione", "La lunghezza delle tacche deve essere inferiore alla meta' delle dimensioni della scatola, riprova")
                continua = False
        if cutwidth_>1:
            showwarning("Attenzione", "Lo spessore del taglio non puo' essere superiore ad 1 millimetro, riprova")
            continua = False
        
        #Se i controlli non hanno rilevato problemi si procede con la creazione del file tramite la funzione BoxMaker
        
        if continua==True:
            
            #Conversione millimetri --> pixel
            width_*=from_mm_to_pixel
            height_*=from_mm_to_pixel
            depth_*=from_mm_to_pixel
            thickness_*=from_mm_to_pixel
            notchLength_*=from_mm_to_pixel
            cutwidth_*=from_mm_to_pixel
            
            BoxMaker(width_, height_, depth_, thickness_, notchLength_, cutwidth_, autom_, coper_)
            '''
            print "Larghezza:", width_, 'pixel'
            print "Altezza:", height_, 'pixel'
            print "Profondita':", depth_, 'pixel'
            print "Spessore del materiale:", thickness_, 'pixel'
            print "Lunghezza delle tacche:", notchLength_, 'pixel'
            print "Automatica:", autom_
            print "Coperchio:", coper_
            print "Spessore del taglio:", cutwidth_, 'pixel'
            '''

#Interfaccia grafica con Tkinter
#Le label vuote sono state posizionate per riempire gli spazi e mantenere allineate le righe
#Gli elementi della finestra sono disposti in tre frame verticali: sinistra, centro e destra

#Creo la finestra
main = Tk()
main.title("BoxMaker")

#Suddivido la finestra in tre frame
sinistra = Frame(main)
centro = Frame(main)
destra = Frame(main)
basso = Frame(main)

#Frame sinistra: descrizioni
l1=Label(sinistra, text="Unita' di misura").pack(pady=1)
l2=Label(sinistra, text="Larghezza").pack(pady=1)
l3=Label(sinistra, text="Altezza").pack(pady=1)
l4=Label(sinistra, text="Profondita'").pack(pady=1)
l5=Label(sinistra, text="Spessore materiale").pack(pady=1)
l6=Label(sinistra, text="Lunghezza tacche").pack(pady=1)
l7=Label(sinistra, text="").pack(pady=1)
l8=Label(sinistra, text="Spessore del taglio").pack(pady=1)
l9=Label(sinistra, text="").pack(pady=1)
l10=Label(sinistra, text="").pack(pady=1)
sinistra.pack(side=LEFT, fill=BOTH)

#Frame centro: raccolta input e pulsante
udm=Spinbox(centro, values=('millimetri', 'centimetri', 'inch'))
udm.pack()
larghezza = Entry(centro)
larghezza.pack()
altezza = Entry(centro)
altezza.pack()
profondita = Entry(centro)
profondita.pack()
spessore_materiale = Entry(centro)
spessore_materiale.pack()
tacche = Entry(centro, text="0")
#tacche.insert(0, "5")
tacche.pack()
l12=Label(centro, text="").pack(pady=1)
spessore_taglio = Entry(centro)
spessore_taglio.insert(0, "0")
spessore_taglio.pack()
l13=Label(centro, text="").pack(pady=1)
p = Button (centro, text="Disegna", command=pulsante)
p.pack()
centro.pack(side=LEFT, fill=BOTH)

#Frame destra: checkbox e suggerimenti
l20=Label(destra, text="").pack(pady=1)
l21=Label(destra, text="Dimensioni esterne").pack(pady=1)
l22=Label(destra, text="Dimensioni esterne").pack(pady=1)
l23=Label(destra, text="Dimensioni esterne").pack(pady=1)
l24=Label(destra, text="").pack(pady=1)
autom=BooleanVar()
w = Checkbutton (destra, text="Automatica", variable = autom, onvalue = True, offvalue = False)
w.select()
w.pack()
coper=BooleanVar()
x = Checkbutton (destra, text="Coperchio", variable = coper, onvalue = True, offvalue = False)
x.pack()
l26=Label(destra, text="").pack(pady=1)
l27=Label(destra, text="").pack(pady=1)
l28=Label(destra, text="").pack(pady=1)
destra.pack(side=LEFT, fill=BOTH)

#Frame basso: logo MUSE FabLab
logo = PhotoImage(file="FabLab.png")
immagine = Label()
immagine.configure(image=logo)
immagine.pack()
basso.pack()

#Apro la finestra
main.mainloop()
