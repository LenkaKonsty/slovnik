# -*- coding: utf-8 -*-
from tkinter import *
from pathlib import Path
from random import randrange
#import pyttsx3
import os

#  TODO: součást NASTAVENÍ - uložit/načítat v txt -> možnost změny adresáře v aplikaci
adresar = "c://SLOVNIK//"
#  TODO: součást NASTAVENÍ - uložit/načítat v txt -> možnost změny adresáře v aplikaci

# slovník s daty, které se využívají na různých m ístech programu, takto jsou stále dostupné
data = {"adresar" : "",
        "osoby" : [], # seznam všech osob - uživatelů, co mohou procvičovat
        "osoba" : "",    #aktuální osoba - druhá položka z dvojice v seznamu osob(=bez diakritiky)
        "nazev_aktualni_lekce" : "",  # název lekce - řetězec = odpovídá názvu souboru.txt
        "pocet_test_slovicek" : 0,
        "slovicek_celkem" : 0,
        "spravne" : 0,
        "uspesnost" : 0,
        "seznam_uspesnosti" : [],
        "testuj_celkem_proc_slov": 75,
        "testuj_celkem_slov": 0,
        "speak_language": 0,

        }

def nacti_nastaveni_ze_souboru():
    konec_osob = False

    with open(adresar + "nastaveni.txt", encoding="utf-8") as text_soubor:
        for radek in text_soubor:
            if radek.strip() != "*****" and konec_osob == False:   #začátek souboru, kde jsou osoby
                osoba_text = radek.strip().split("-")
                osoba_dvojice = (osoba_text[0].strip(), osoba_text[1].strip())
                data["osoby"].append(osoba_dvojice)
                print(osoba_dvojice)
            elif radek.strip() == "*****":
                konec_osob = True
                poradi_udaju = 2  # konec seznamu osob a pokračuje se dalšími údaji v txt souboru
            elif poradi_udaju == 2:
                data["adresar"] = radek.strip()
                poradi_udaju +=1
            elif poradi_udaju == 3:
                blbost = radek.strip()
                poradi_udaju +=1
        print(data["adresar"], data["osoby"], data ["speak_language"], "BLBOST ", blbost)
    return

# k hodnostě k danému klíči se dostanu: moje_data["osoba"])

def aktualni_cas():
    import datetime
    now = datetime.datetime.now()
    return str(now.year)+ "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute)

def najdi_lekci(adresar): # vrátí seznam lekci z dostupných txt slovníků/souborů v odpovídajícím adresáři
    data["osoba"] = aktualni_osoba.get()
    cesta = adresar + "lekce_"  + data["osoba"]
    seznam_lekci = []

    for c in Path(cesta).iterdir():
        soubor = Path(c).name
        if ".txt" in soubor:
            seznam_lekci.append(soubor.replace(".txt",""))

    listbox.delete(0, END)  # před vložením nového seznamu pro danou osobu se předchozí seznam lekcí smaže
    for lekce in seznam_lekci:
        listbox.insert(END, lekce)
        # listbox.bind("<<ListboxSelect>>", vyber_lekci)  # metoda se volá až po uvolnění myši
        # items = map(int, list.curselection())
    return seznam_lekci

def vyber_lekci(event):  # zjistí aktuálně vybranou lekci
    index = listbox.curselection()[0]  # uloží pozici vybrané položky
    s_lekci = najdi_lekci(adresar)
    print("AKTUAL VYBER LEKCI:", data["nazev_aktualni_lekce"])
    data["nazev_aktualni_lekce"] = s_lekci[index]
    return

def nacti_lekci(lekce_soubor):  #  načte slovíčka z daného txt souboru  vybrané lekce(=nazev_aktualni_lekce)
    lekce = []
    index = listbox.curselection()[0]  # uloží pozici vybrané položky
    s_lekci = najdi_lekci(adresar)
    data["nazev_aktualni_lekce"] = s_lekci[index]

    with open(lekce_soubor + data['nazev_aktualni_lekce'] + ".txt", encoding="utf-8") as text_soubor:
        for radek in text_soubor:
            slovo = radek.split("\t")
            cz = slovo[0].replace("\ufeff","")
            aj = slovo[1]
            slovicko = cz.replace("\n",""), aj.replace("\n","")
            lekce.append(slovicko)



    return lekce

def vypis_slovicka():   # vypíše obsah lekce do nového podokna, jako Text
    aktualni_lekce = nacti_lekci(adresar + "lekce_" + data['osoba'] + "//")
    okno_slovicka = Toplevel()
    okno_slovicka.title("LEKCE: " + data['nazev_aktualni_lekce'])
    slovicka = Text(okno_slovicka)
    slovicka.grid(row=0)
    slovicka.insert(END, "Slovíčka lekce: " + data['nazev_aktualni_lekce'] )
    slovicka.insert(END, "\n")
    slovicka.insert(END,"*****************************")
    slovicka.insert(END, "\n")
    for slovo in aktualni_lekce:
        slovicka.insert(END, slovo[0] + " = " + slovo[1] )
        slovicka.insert(END, "\n")
    slovicka.insert(END,"*****************************")
    slovicka.insert(END, "\n")
    slovicka.insert(END,"Počet slovíček v lekci:" + str(len(aktualni_lekce)))
    slovicka.insert(END, "\n")
    Button(okno_slovicka, text="KONEC", fg="red", width=15,command=okno_slovicka.destroy).grid(row=3, column=0,columnspan=2, sticky=N, pady=5)
    return

def priprav_novy_test():
    # smazat po každém testu obsah oken... ale aby byl vidět výsledek...
    vypis.config(state=NORMAL)  # nastavit na "zápis", aby se tam zapsalo co je třeba
    vypis.delete(1.0, END)  # smaže celý obsah okna
    vypis.insert(INSERT, "Lekce má " + str(data["slovicek_celkem"]) + " slovíček, otestuješ si " + str(data["testuj_celkem_slov"]) +" slovíček! \n")
    vypis.insert(INSERT, "****************************************************\n")
    vypis.config(state=DISABLED)  # nastavit na "jen pro čtení", aby tam nemohl psát uživatel
    return




def procvic_slovicka(): #  do nového podokna
    global aktualni_lekce
    aktualni_lekce = nacti_lekci(adresar + "lekce_" + data['osoba'] + "//")
    data['seznam_uspesnosti'] = []
    data["slovicek_celkem"] = len(aktualni_lekce)
    data["testuj_celkem_slov"] = data["slovicek_celkem"] * data["testuj_celkem_proc_slov"]//100

    w = Toplevel()
    w.title("Procvičování slovíček")

    tlacitka = LabelFrame(w, text="", padx=5, pady=15)
    tlacitka.grid(row=2, column=3, sticky=N)

    Label(w, text="česky:", font=("Arial", 10)).grid(row=0, column=0, pady=10)
    Label(w, text="přelož:", font=("Arial", 10)).grid(row=0, column=1, pady=10)

    global slovo
    slovo = Label(w, text=aktualni_lekce[0][0], font=("Arial Bold", 14), fg="blue")
    slovo.grid(row=1, column=0)
    slovo.config(text=aktualni_lekce[index_slova][0])  # první slovíčko při spuštění lekce

    global zadano
    zadano = Entry(w, width = 25, font=("Arial Bold", 16))
    zadano.bind("<Return>", dalsi_slovo)
    zadano.grid(row=1, column=1)

    global vypis

    vypis_pole = LabelFrame(w, text="...", padx=10, pady=10)
    vypis_pole.grid(row=2, column=0, columnspan=2, pady = 5, padx = 5, sticky=N)

    scrollbar = Scrollbar(vypis_pole, orient=VERTICAL)
    vypis = Text(vypis_pole, yscrollcommand=scrollbar.set)
    scrollbar.config(command=vypis.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    vypis.pack(side=RIGHT)
        #tlačítka akcí pro procvičovací okno
    Button(tlacitka, text="Nový test", width=15, command = priprav_novy_test).grid(row=0, column=3, pady = 8, padx = 15)
    #Button(tlacitka, text="Ulož testy", width=15, command = uloz_test).grid(row=1, column=3, pady = 8)
    Button(tlacitka, text="Ulož statistiku", width=15, command = uloz_statistiku).grid(row=2,column=3, pady = 8)
    Button(tlacitka, text="Konec", width=15,command=w.destroy).grid(row=3, column=3, pady=8)
    priprav_novy_test()
    return





def dalsi_slovo(event, data=data):  # po stisku ENTER se zkontroluje překlad a zadá nové slovíčko
    global index_slova
    data["pocet_test_slovicek"] = data["pocet_test_slovicek"] + 1
    if aktualni_lekce[index_slova][1] == zadano.get():
        kontrola = "OK"
        data["spravne"] = data["spravne"] + 1
    else:
        kontrola = "CHYBA {" + aktualni_lekce[index_slova][1] + "}"
    #zkontroluj.configure(text = kontrola)
    vypis.config(state=NORMAL)  # nastavit na "zápis", aby se tam zapsalo co je třeba
    vypis.insert(3.0, str(data["pocet_test_slovicek"]) + "." + aktualni_lekce[index_slova][0] + " = " + zadano.get() + " ... " + kontrola + "\n")
    vypis.config(state=DISABLED)  # nastavit na "jen pro čtení", aby tam nemohl psát uživatel
    #engine = pyttsx3.init()
    #engine.say(aktualni_lekce[index_slova][1])
    #engine.runAndWait()

    #print("OTESTOVANO", data["pocet_test_slovicek"], "SLOVICEK CELKEM", data["slovicek_celkem"], data["testuj_celkem_slov"])

    if data["testuj_celkem_slov"] == data["pocet_test_slovicek"]:
        # print("KONEC TESTOVANI")
        vyhodnot_test()
        uloz_test()

        return
    zadano.delete(0, END) #vymaže obsah pole pro zadávání slovíček
    index_slova = randrange(0,len(aktualni_lekce)) #náhodný výběr pro další slovíčko ze slovíček dané lekce
    slovo.config(text=aktualni_lekce[index_slova][0]) #přepíše další slovo ????
    return

def uloz_test(): # TODO: tisk do souboru
    nazev_souboru = data['osoba'] + "_" + aktualni_cas() + ".txt"
    with open(adresar + "//vystupy//" + nazev_souboru, "a", encoding="utf-8") as soubor:
        print(f"Lekce: {data['nazev_aktualni_lekce']}", file=soubor)   # do souboru název lekce
        print("=======================", file=soubor)   # do souboru název lekce
        print(vypis.get(1.0, END), end="", file=soubor)   # do souboru uloží kompletní výpis, co je aktuálně v okně


def uloz_statistiku(): # TODO: tisk do souboru
    nazev_souboru = "statistika.txt"
    with open(adresar + "//vystupy//" + nazev_souboru, "a", encoding="utf-8") as soubor:
        print(data['osoba'].upper(), ":", aktualni_cas(), ":", data['nazev_aktualni_lekce'], end=" --> ", file=soubor)   # do souboru uloží kompletní výpis, co je aktuálně v okně
        print("ÚSPĚŠNOST: ", data['seznam_uspesnosti'], "%", end="\n", file=soubor)

def vyhodnot_test(): # TODO: tisk do souboru
    data["uspesnost"] = round(data["spravne"] / data["pocet_test_slovicek"] * 100,1)
    data["slovicek_celkem"] = len(aktualni_lekce)

    vypis.config(state=NORMAL) # nastavit na "zápis", aby se tam zapsalo co je třeba
    vypis.insert(3.0, "*****************************************************************\n")
    vypis.insert(4.0, f"Testováno: {data['pocet_test_slovicek']} z {data['slovicek_celkem']} slovíček --> úspěšnost {data['uspesnost']}%\n", "vyrazne")
    vypis.insert(5.0, "*****************************************************************\n")
    vypis.tag_config("vyrazne", foreground="red", font="Arial 12")
    vypis.config(state=DISABLED) # nastavit na "jen pro čtení", aby tam nemohl psát uživatel
    data['seznam_uspesnosti'].append(data['uspesnost'])
    data['uspesnost'] = 0
    data['pocet_test_slovicek'] = 0
    data['spravne'] = 0
    data['otestovano'] = 0

def otevri_okno_nastaveni():
    with open("nastaveni.txt","a", encoding="utf-8") as soubor:
         print("zakládám soubor pro nastavení", file=soubor)   # vytvoří soubor nastaveni.txt
    okno_nastav = Tk()
    okno_nastav.title("Nastavení aplikace SLOVNÍČEK - Zatím nefunguje")
    Label(okno_nastav, text="Adresář s daty:", font=("Arial", 10)).grid(row=0, column=0, pady=10)
    Label(okno_nastav, text="Seznam osob:", font=("Arial", 10)).grid(row=1, column=0, pady=10)
    Button(okno_nastav, text="Ulož nastavení",command=uloz_nastaveni).grid(row=2, column=0, pady=10)  # když na tebe někdo kliken zavolá metodu odezamkni
    adresar = StringVar()
    Entry(okno_nastav, textvariable=adresar).grid(row=0, column=1, pady=10)
    return

def uloz_nastaveni():
    print("???", adresar, "to je blbe")



#*********************************************************************
# *****HLAVNÍ PROGRAM ********
#*********************************************************************

if os.path.exists("nastaveni.txt"):
    nacti_nastaveni_ze_souboru()
    nastaveni_ok = True
else:
    nastaveni_ok = False

hlavni_okno = Tk()
hlavni_okno.title("Slovník")

if nastaveni_ok:
    aktualni_osoba = StringVar()
    aktualni_osoba.set(data["osoby"][0][1])

    Label(hlavni_okno, text="Vyber lekci k procvičení", font="Arial 18").grid(row=0, columnspan=2, padx=50, pady=10)
    kdo = LabelFrame(hlavni_okno, text="Kdo jsi", padx=10, pady=15)
    kdo.grid(row=1, column=0, sticky=N)
    # naplnění dat pro výběr osob z RadioButton
    for text, osoba in data["osoby"]:
        Radiobutton(kdo, text=text, variable=aktualni_osoba, value=osoba, command=lambda: najdi_lekci(adresar)).pack(anchor=W)
        data["osoba"] = aktualni_osoba.get()
    lekce = LabelFrame(hlavni_okno, text="Seznam lekcí", padx=10, pady=10)
    lekce.grid(row=1, column=1, sticky=N)

    scrollbar = Scrollbar(lekce, orient=VERTICAL)
    listbox = Listbox(lekce, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=RIGHT)

    # prvotní naplnění seznamu
    najdi_lekci(adresar)
    akce = Frame(hlavni_okno)
    akce.grid(row=1, column=2, sticky=N)
    Button(akce, text="Vypiš slovíčka", width=15, command=vypis_slovicka).grid(row=1, column=3, sticky=N, padx=10, pady=10)
    Button(akce, text="Procvič slovíčka", width=15, command=procvic_slovicka).grid(row=2, column=3, sticky=N, padx=10, pady=10)
    Button(akce, text="Nastavení - zatím NE", width=15, command=otevri_okno_nastaveni).grid(row=0, column=3, sticky=N, padx=10, pady=10)
    Button(akce, text="Konec", width=15,command=hlavni_okno.destroy).grid(row=3, column=3, sticky=N, pady=10)
else:
    akce = Frame(hlavni_okno)
    akce.grid(row=1, column=0, sticky=N)
    Label(hlavni_okno, text="Nemáš nastavení aplikace, proveď nastavení:", font="Arial 8").grid(row=0, column=0, padx=10, pady=10)
    Button(akce, text="Nastavení", width=15, command=otevri_okno_nastaveni).grid(row=1, column=0, sticky=N, padx=10, pady=10)
    Button(akce, text="Konec", width=15,command=hlavni_okno.destroy).grid(row=2, column=0, sticky=N, pady=10)

#pocet_slovicek = 0  # TODO: nulovat po ukončení testovní lekce
#pocet_test_slovicek = 0
index_slova = 1
#spravne = 0

mainloop()