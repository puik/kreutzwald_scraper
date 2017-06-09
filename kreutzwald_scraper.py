from easygui import *
import re, urllib.request, csv


def id_sortimine(url):

    # regex-fraasis annan id-osale grupinime, et hiljem see kiirelt kätte saada
    # fraasi lõpp on kontrolli-tingimusega (?=...
    id_fraas = r"item_id=(?P<id>\d+)(?=&amp;page_start=&amp;table=Scans)"

    # tühi järjend id-de kogumiseks
    id_jarj = []

    # avame kasutajalt küsitud urli, loeme, dekodeerime, jagame ridadeks
    with urllib.request.urlopen(url) as loend:
        for rida in loend.read().decode().splitlines():
            # otsin igalt realt id-ga fraasi, kui leian, kirjutan järjendisse
            tulemus = re.search(id_fraas, rida)
            if tulemus:
                id_jarj += [tulemus.group('id')]

    # print(id_jarj)            
    return id_jarj
    

def lisaandmed(id):

    # otsitavate pildiandmete regex-kirjeldused
    pealkiri_html = r"<h2>(?P<pealkiri>.+)" # avastasin, et paljudel on lõpu </h2> eraldi real, selle koristan hiljem
    kogunr_html = r"<span>(?P<kogunr>.+)</span>"
    välisurl = r'target="_blank">(?P<exturl>(.*))</a>' # võib ka tühi olla

    pildifail_html = '="(?P<pildiurl>http://krzwlive.kirmus.ee/scans/(?P<failinr>.+\.\w{3}))'
    # NB! ei ole raw string nagu teised, pärast punkti 3täheline laiend
    # NB! kaks gruppi (kogu urlile ja pildifailile eraldi), neist üks teise sees

    laius = r'data-width="(?P<laius>\d+)' 
    kõrgus = r'data-height="(?P<korgus>\d+)'

    # sisestame id piltide detailiinfo vaate urli
    url = "http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?image_id={0}&action=scan&hide_template=1".format(id)

    # loome tühja järjendi, kuhu kogume väljasõelutava info
    andmed = []

    # eraldi järjendi pildifaili mõõtude jaoks, kuhu 3. elemendina läheb pildi orientatsioon
    mõõdud = []

    with urllib.request.urlopen(url) as info:

        for rida in info.read().decode().splitlines():

            # pealkirja otsimine
            pk = re.search(pealkiri_html, rida)
            p = re.compile('</h2>')
            if pk:
                # sub-iga võtan lõpust ära </h2>, kui see seal on
                andmed += [p.sub('', pk.group('pealkiri'))]

            #kogunumber
            knr = re.search(kogunr_html, rida)
            if knr:
                andmed += [knr.group('kogunr')]


            # välisallika url (lingid samale pildile muudes keskkondades)
            vurl = re.search(välisurl, rida)
            if vurl:
                andmed += [vurl.group('exturl')]

            # pildifaili url
            f = re.search(pildifail_html, rida)
            if f:
                andmed += [f.group('pildiurl')]

            # pildi mõõdud
            la = re.search(laius, rida)
            if la:
                mõõdud += [int(la.group('laius'))]

            ko = re.search(kõrgus, rida)
            if ko:
                mõõdud += [int(ko.group('korgus'))]

                # kirjutame välja ka pildi orientatsiooni
                # ruudukujulist eraldi ei erista, see läheb siis ka P alla
                # võimaldab hiljem pilte sortida orientatsiooni järgi
                if len(mõõdud) == 2:
                    if mõõdud[0] > mõõdud[1]:
                        mõõdud += 'L'
                    else:
                        mõõdud += 'P'
                    andmed += [tuple(mõõdud)]

    # print(tuple(andmed))
    return tuple(andmed)

def andmed_sõnastikku(idloend):
    andmesõnastik = {}
    for id in idloend:
        id_kirje = lisaandmed(id)
        andmesõnastik[id] = id_kirje
        
    # print(andmesõnastik)
    return andmesõnastik
      
# Üksikpildi andmete kogumise testimiseks küsisin eraldi konkreetse pildi id-d
# testid = enterbox("Sisestage Kreutzwaldi sajandi pildi id:")
# lisaandmed(testid)

# küsime kasutajalt pildiloendi lehekülje urli
krzurl = enterbox("Sisestage Kreutzwaldi sajandi kogude loendi url:")

# loome sõnastiku, 3. funktsiooni sisendiks on 1. funktsiooni väljund, 1. omakorda jooksutab 2. fn-i
sõnastik = andmed_sõnastikku(id_sortimine(krzurl))

# küsime, kas ja kuhu kasutaja tahab tulemustega CSV-faili salvestada
if ccbox("Määrake tulemuste faili salvestamiseks kaust:"):

    # kasutaja valib arvutis kausta
    kaustavalik = diropenbox()

    with open(kaustavalik + '/kreutzwald.csv', 'w', newline='', encoding='utf-8') as csvfile:
        tulemused = csv.writer(csvfile)

        # CSV-faili kirjutatakse sõnastiku ID ja siis andmed, mis jäävad ennikusse
        # tulevikus tuleks andmete ennik laiali jaotada, aga praegu seda ei jõua
        for id, andmed in sõnastik.items():
            tulemused.writerow([id, andmed])
    
else:
    sys.exit(0)



