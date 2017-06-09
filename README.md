# Veebiportaali Kreutzwaldi sajand pildifailide ja -info _scraper_
Kirjutasin programmi Tartu Ülikooli veebipõhise programmeerimiskursuse [Programmeerimise alused II](https://courses.cs.ut.ee/2017/eprogalused2/) projektina.


## Programmi eesmärk
Tegelen ajalooliste piltide ühisloome korras kaardistamise platvormi [Ajapaik.ee](https://ajapaik.ee) arendamisega (projektijuhi, mitte programmeerijana) ning sellega seoses tunnen huvi ka igasugu muude pildilist kultuuripärandit sisaldavate veebirakenduste vastu. Juba ammu olen mõlgutanud mõtteid mitmest allikast andmete _scrape_'imisest ning nüüd otsustasin siinse kursuse raames teha midagi, mis juba hangiks mulle huvipakkuvat infot. 

Esialgu pidasin silmas ühte teist veebiplatvormi, aga lõpuks otsustasin kätt proovida Eesti Kirjandusmuuseumi kultuuriloolise veebiportaaliga [**Kreutzwaldi sajand**](http://kreutzwald.kirmus.ee/). Portaalis on eraldi **kogude** alajaotus, milles omakorda [**fotode** rubriik](http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?table=Scans). Rubriik on pagineeritud 25 pildi kaupa, aga nupust *Vaata kõiki* kuvatakse [kogu fotokogu korraga](http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?table=Scans&page=all).

Uurisin nii loendilehekülje kui ka üksikpiltide lehekülgede ([üks näide](http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?item_id=4105&page_start=&table=Scans)) html-koodi, et tuvastada, milliste html-täägide vahel on piltide kohta käivad erinevad infoüksused (pildi pealkiri, muuseumi kogunumber, allikaviide) ning kus asuvad pildifailid. Tegin kindlaks, et kui fotokogu lehekülgedelt saan kätte pildiobjektide identifikaatorid, siis enim pildiinfot leidub moodalaknana üksikpildi lehel avanevast aknast, mis avaneb ka [oma urlilt](http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?image_id=4105&action=scan&hide_template=1).

Esmase eurimise käigus oli suurimaks avastuseks, et Kreutzwaldi sajandi veebilehel on kaustade sisu (nn _directory listing_) avalik ning et kõik rohkem kui 10000 pildifaili on [**ühes kaustas**](http://krzwlive.kirmus.ee/scans/) nähtavad. See tegi lihtsamaks piltide salvestamise ning edasi sain tegeleda piltide info kogumise küsimusega. Olgu öeldud ka, et andsin portaali tegijatele teada, et mõistlik oleks kaustade sisu kuvamine siiski kinni keerata.

## Valminud _scraper'_i lühikirjeldus
1. Programm küsib Easygui-kasutajaliidese abil kasutajalt ühte fotokogu sirvimise lehekülge (nt [123. lehekülg](http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?table=Scans&page=123)).
2. Saadud url on esimese funktsiooni sisendiks, mis käib veebilehe ridahaaval läbi, kirjutab leitud identifikaatorid järjendisse ja väljastab selle.
3. Saadud järjend on 3. funktsiooni sisendiks, mis omakorda käivitab iga id-ga 2. funktsiooni, mis kogub iga pildi kohta info kokku ennikusse, milles on pealkiri, kogunumber, pildi välisallika url (kui see on olemas, kui mitte, kirjutatakse tühi string), pildifaili url ning pildifaili mõõdud, mis kirjutatakse omakorda eraldi 3 elemendiga ennikusse, milles on pildifaili laius, kõrgus ning viimasena pildi orientatsioon, mis arvutatakse laiuse-kõrguse suhtest. Olles saanud vastavad andmed 2. funktsioonilt, kirjutab 3. funktsioon kõigi piltide andmed sõnastikku, milles on võtmeks piltide id-d ning väärtuseks andmetega ennik.
4. Programm küsib kasutajalt, millisesse kausta soovib kasutaja salvestada kogutud andmetega CSV-faili ning kirjutab 3. funktsiooni tagastatud sõnastiku CSV-faili.

## Ülevaade tööprotsessist
Esmalt kirjeldasin ära, milliseid funktsioone programmis vaja oleks ning otsisin html-koodist välja, kus kohas html-koodis asuvad vajalikud infoühikud.

Suurimaks õppimiskohaks oli tutvumine _regex_-i ehk regulaaravaldiste teemaga, mida siinne kursus otseselt ei käsitlenud, aga millega olin esmatutvuse teinud [SoloLearn veebiõppekeskkonna pythoni kursusel](https://www.sololearn.com/Play/Python).

Kui sain regex-avaldise esimeses funktsioonis tööle, siis läks 2. funktsiooni avaldistega juba lihtsamalt, kuigi nuputamiskohti jagus piisavalt. Väga praktilise leidsin olevat regulaaravaldise alamosadele grupinime omistamine, mille abil sain hiljem tervest kontrollavaldisest mugavalt kätte mind huvitava infokillu.

Suurima probleemi põhjustas avastus, et piltide _h2_-täägide vahel olevate pealkirjade puhul oli osadel juhtudel lõpetav tääg rea lõpus, osadel juhtumitel aga uuel real. Lõpuks lahendasin selle nii, et lisasin hiljem tingimuslausesse veel regulaaravaldise meetodi _sub_, mis, juhul kui leitud väärtuse lõpus oli h2-tääg, jättis selle sealt ära, kui polnud, siis ei teinud midagi.

Viimase osa programmist moodustab kasutajalt Easygui-ga kausta küsimine, kuhu salvestada andmetega CSV-fail, ning CSV-faili genereerimine. Praegu kirjutatakse CSV-faili igale reale pildi id ning andmetega ennik. Edasiarendusena võiks programm muidugi kõik ennikus olevad infoühikud eraldi veergudesse kirjutada, aga see jäi praegu tegemata.

Testimiseks kasutasin konsooli printimist, samuti oli mugav, et piltide loend oli 25 pildi kaupa pagineeritud, nii sain katsetada eri lehekülgi, sel moel tuvastasin ka kirjeldatud anomaalia h2-täägide asukohtade puhul.

Ajakulu arvestamiseks kasutasin [**Toggl**](https://toggl.com)'i. Reaalsele programmeerimisele kulus umbes 7,5 h, osa Kreutzwaldi sajandi platvormiga tutvumise aega jäi algul ka träkkimata.

##Kokkuvõte
Kui tundus, et programm 25 pildiga saab hakkama, siis andsin programmile ette ka [kogu fotokogu urli](http://krzwlive.kirmus.ee/et/lisamaterjalid/ajatelje_materjalid?table=Scans&page=all). Kulus üle poole tunni, aga tulemuseks sain kätte CSV-faili, milles ligi 11 000 rida andmeid, mis tegi tuju heaks, sest olin saavutanud tulemuse, mida soovisin.
