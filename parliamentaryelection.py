import copy  # mv_hesabla fonksiyonunda deepcopy methodundan kullanmak icin fonksiyonu import ettim

def verileri_al(secim_dosyasi, il_say,parti_say):  #Dosyadan ilin plakasi,kontenjan ve puanlari alan fonksiyon
    # il_say = 0
    kontenjan_list = []  #kontenjan degerleri icin liste
    plaka_list = []   # ilin plaka numaralari icin liste
    plaka_no = secim_dosyasi.readline()
    oylar = [] #her ilin oy verileri icin liste
    while plaka_no != '':
        plaka_list.append(int(plaka_no))
        kontenjan = int(secim_dosyasi.readline())
        kontenjan_list.append(kontenjan)
        il_say += 1  #secimlerin yapildigi il sayisi
        oy_list = []
        for say in range (parti_say):    
            oy_sayi = int(secim_dosyasi.readline())
            oy_list.append(oy_sayi)
        oylar.append(oy_list)  #Tum oylari bir listede topladim
        plaka_no = secim_dosyasi.readline()   
    return il_say,plaka_list,kontenjan_list,oylar

def mv_hesablama(il_say,kontenjan_list,parti_say,oylar): # İllerin milletvekili kontenjanlarının partilere dağıtılmasınin hesablanmasi
    mv = []  # milletvekili kontenjanlari
    top_oylar = copy.deepcopy(oylar) #oylar uzerinde islem yapilacagi zaman liste degisecegi icin kopyaladim
    for il in range(il_say):
        mv_say = [0]*parti_say
        for say in range (kontenjan_list[il]):   
            max_oy = max(top_oylar[il])
            max_oy_parti = top_oylar[il].index(max_oy)
            mv_say[max_oy_parti] += 1         #her ilin kontenjani dolana kadar o ilde max oyu toplayan partiye 1 milletvekili verilir
            top_oylar[il][max_oy_parti] = top_oylar[il][max_oy_parti] // 2  #sonra max oy 2 ye bolunur ve kontenjan dolana kadar tekrarlanir
        mv.append(mv_say)
    return mv      

def il_istatistikleri(il_say,plaka_list,kontenjan_list,top_oylar,parti_say,mv_say):   # her il istatistiklerin ekrana yazdirilmasi icin fonksiyon
    for il in range(il_say):
        print('Il Plaka Kodu: ',plaka_list[il])
        print('Milletvekili Kontenjani: ',kontenjan_list[il]) 
        print('Gecerli Oy Sayisi: ',sum(top_oylar[il]),'\n') 
        print('Pusula Sira      Oy Say        Oy Yuzde       MV Say')
        print('-----------     --------       ---------     --------')
        for say in range(parti_say):
            print(format(say+1,"11d"),end = '')
            print(format(top_oylar[il][say],"12d"),end='        ' )
            # oy toplamlarinin 0 olmasi halinde sifira bolunme hatasini onlemek icin
            try:
                print(' %',format(top_oylar[il][say]*100/sum(top_oylar[il]),"6.2f"),end = '  ')
            except ZeroDivisionError:
                print(format(0.00,"6.2f"),end = '  ')   
            print(format(mv_say[il][say],'11d'),'\n')  
        print('**************************************************************','\n')     

def ulke_istatistikleri(il_say,plaka_list,kontenjan_list,top_oylar,parti_say,mv_say): #tum ulke geneli istatistiklerin ekrana yazdirilmasi icin fonksiyon
    print('Türkiye Geneli:')
    print('Pusula Sira       Oy Say          Oy Yuzde          MV Say          MV Yuzde       0 MV Il Say' )      
    print('-----------     --------         ---------         -------          --------       ------------')
    for say in range(parti_say):
        print(format(say+1,"11d"),end = '  ')
        top_parti_puan = 0  #her partinin oylarinin tum illerde toplami 
        toplam_oy = 0       # verilen tum oylar
        for i in top_oylar:
            top_parti_puan += i[say]  
            toplam_oy += sum(i)   
        print(format(top_parti_puan,"11d"),end = '          ')
         # oy toplamlarinin 0 olmasi halinde sifira bolunme hatasini onlemek icin
        try:
            print(' %',format((top_parti_puan*100/toplam_oy),"5.2f"),end = '      ')
        except ZeroDivisionError: 
            print(format(0.00,"5.2f"),end = '      ')     
        top_mv_il = 0   # partiye tum illerden verilen toplam milletvekilleri
        sifir_mv = 0
        for i in mv_say:
            top_mv_il += i[say]
            if i[say] == 0:   #partilerin hiç milletvekili çıkaramadıkları il sayıları
                sifir_mv += 1   
        print(format(top_mv_il,'10d'),end = '          ')
        top_mv_ulke = sum(kontenjan_list)   #toplam milletvekilleri sayi
        # oy toplamlarinin 0 olmasi halinde sifira bolunme hatasini onlemek icin
        try:
            print(' %',format((top_mv_il*100/top_mv_ulke),"5.2f"),end = '  ')
        except ZeroDivisionError: 
            print(format(0.00,"5.2f"),end = '  ')     
        print(format(sifir_mv,'16d'))

def main(): #tum fonksiyonlar buradan cagriliyor
    try:
        secim_dosyasi = open('secim.txt','r')
        parti_say = int(secim_dosyasi.readline())
        il_say = 0
        il_say,plaka_list,kontenjan_list,oylar = verileri_al(secim_dosyasi,il_say,parti_say)
        mv_say = mv_hesablama(il_say,kontenjan_list,parti_say,oylar)
        il_istatistikleri(il_say,plaka_list,kontenjan_list,oylar,parti_say,mv_say)
        ulke_istatistikleri(il_say,plaka_list,kontenjan_list,oylar,parti_say,mv_say)
        secim_dosyasi.close()
    # isim hatasini onlemek ici    
    except IOError:
        print("Veri dosyası açılamadı")

main()
