from django.shortcuts import render
from soz_analizi import *
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
# Create your views here.
from django.http import HttpResponse
from .forms import NameForm,TextForm,SozForm, SignUpForm, UserLoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import UserLoginForm
def index(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm
    if request.method == 'POST':

        if request.POST['action'] == 'soz':
            return soz_analiz(request)
        if request.POST['action'] == 'metn':
            return stem_metn(request)
        if request.POST['action'] == 'morf':
            return morf(request)


    return render(request,'index.html', {'form': soz_class,'cumle':cumle_class,'morf':morf_class})

def morf(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm
    temp=request.POST.get('soz', '')
    k=deqiq_olsun(duzelt(temp))
    txt=[]
    if len(k)==0:
        txt.append(temp+' sözü tapılmadı\n')

    txt.append(str(' '+temp+' sözünü '+str(len(k))+' cür təhlil etmək mümkündür '))
    for i in range(0,len(k)):
        txt.append(' '+str(i+1)+' ci yol ')
        txt.append(' '+str(k[i].kok)+' -sözün başlanğıc formasıdır. Nitqi hissəsi isə '+ str(k[i].nitq)+'dir.')
        for sh in k[i].shekilciler:
            if sh.stat=='-':
                txt.append(str(sh.adi)+' : '+str(sh.secilmis[-1:]))
            else:
                txt.append(str(sh.adi)+' : '+str(sh.secilmis))

        txt.append('\n Hecalara isə bu yol ilə ayırmaq olar : '+k[0].hecaya_bol()+' ')



    return render(request,'morf.html', {'form': soz_class,'cumle':cumle_class,'morf':morf_class,'morf_t':txt})

def stem_metn(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm
    porter = PorterStemmer()
    lancaster = LancasterStemmer()
    k=request.POST.get('metn', '')
    alqo=request.POST.get('alqo', '')
    txt=k
    if alqo=='Bizim Alqoritm':
        txt=metn_oxu(k)
    elif alqo=='Porter Alqoritmi':
        txt=porter.stem(txt)
    elif alqo=='Lancaster Alqoritmi':
        txt=lancaster.stem(txt)
    elif alqo=='WordNet Alqoritmi':
        wordnet_lemmatizer = WordNetLemmatizer()
        txt=metn_oxu(wordnet_lemmatizer.stem(k))

    return render(request,'metn.html', {'form': soz_class,'cumle':cumle_class,'morf':morf_class,'txt':txt})


def soz_analiz(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm

    k=sz(request.POST.get('soz', ''))
    k.nitq(request.POST.get('nitq', ''))
    k.Kateqoriya(request.POST.get('Kateqoriya',''))

    z=[]

    for a in k.yarat():

        if(a.ozu[-3:]=="ıda"):
            a.ozu=a.ozu[:-3]+"ında"
        elif (a.ozu[-4:] == "ıdan"):
            a.ozu = a.ozu[:-4] + "ından"
        elif(a.ozu[-3:] == "idə"):
            a.ozu=a.ozu[:-3] +"ində"
        elif (a.ozu[-4:] == "idən"):
            a.ozu = a.ozu[:-4] + "indən"
        elif (a.ozu[-3:] == "üdə"):
            a.ozu = a.ozu[:-3] + "ündə"
        elif(a.ozu[-4:]=="üdən"):
            a.ozu=a.ozu[:-4]+"ündən"
        elif (a.ozu[-3:] == "uda"):
            a.ozu = a.ozu[:-3] + "unda"
        elif(a.ozu[-4:]=="udan"):
            a.ozu=a.ozu[:-4]+"undan"
        elif(a.ozu[-5:])=="ıdakı":
            a.ozu=a.ozu[:-5]+"ındakı"
        elif (a.ozu[-5:]) == "idəki":
            a.ozu = a.ozu[:-5] + "indəki"


        z.append(a)

        form = soz_class(data=request.POST)


    data=z
    pho=k.ozu
    return render(request,'yarat.html', {'data':data,'pho':pho,'form': soz_class,'morf':morf_class,'cumle':cumle_class})

def about(request):
        return render(request,'team.html', {})


def contact(request):
        return render(request,'contact.html', {})

def work(request):
        return render(request, 'work.html', {})

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
    return render(request, "login.html",{"form":form, "title":title})


def morf_view(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm
    if request.method == 'POST':
        if request.POST['action'] == 'morf':
            return morf(request)


    return render(request,'morf.html', {'form': soz_class,'cumle':cumle_class,'morf':morf_class})

def yarat_view(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm
    if request.method == 'POST':

        if request.POST['action'] == 'soz':
            return soz_analiz(request)


    return render(request,'yarat.html', {'form': soz_class,'cumle':cumle_class,'morf':morf_class})

def metn_view(request):
    soz_class = NameForm
    cumle_class = TextForm
    morf_class=SozForm
    if request.method == 'POST':
        if request.POST['action'] == 'metn':
            return stem_metn(request)
    return render(request,'metn.html', {'form': soz_class,'cumle':cumle_class,'morf':morf_class})

def cnv(n):
    if(n in dey_isim):
        return 'Isim'
    if(n in dey_feil):
        return 'Feil'
    if(n in dey_evez):
        return 'Əvəzlik'
    if(n in dey_sif):
        return 'Sifət'
    if(n in dey_say):
        return 'Say'
    if(n in dey_zerf):
        return 'Zərf'
    return n
def l_v(request):
    morf_class=SozForm
    temp=request.POST.get('soz', '')
    koko=lug()
    za=yuxari(temp)
    sozder=koko.de(za[:3])
    cv=[]
    for kl in sozder:
        if kl.startswith(za)==True:
            soz=kl.split('\t')[0]
            nitqler=kl.split('\t')[1].split(';')[:-1]
            for ni in nitqler:
                cv.append([soz,cnv(ni)])

    if(len(za)<3):
        for zaaz in koko.dic.keys():
            if zaaz.startswith(za)==True:
                for kl in koko.de(zaaz):
                    soz=kl.split('\t')[0]
                    #print(kl)
                    nitqler=kl.split('\t')[1].split(';')[:-1]
                    for ni in nitqler:
                        cv.append([soz,cnv(ni)])

    return render(request,'luget.html', {'morf':morf_class,'morf_t':cv})


def luget_view(request):
    morf_class=SozForm
    if request.method == 'POST':
        if request.POST['action'] == 'morf':
            return l_v(request)
    return render(request,'luget.html', {'morf':morf_class})
