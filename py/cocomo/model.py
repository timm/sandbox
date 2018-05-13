def estimate():
  months=pm()
  timE=tdev()
  staff = months/timE
  return report(months,timE,staff) 

def size():
  return (1+(revl()/100)) * (newKsloc()+equivalentKsloc())

def equivalentKsloc():
  return adaptedKsloc()*aam()*(1-(at()/100))

def aam():
  f = aaf();
  if f <=50:
    return (aa()+f*(1+(0.02*su()*unfm())))/100
  return ((aa()+f+(su()*unfm()))/100)

def aaf():
  return 0.4*dm()+0.3*cm()+0.3*im()

def tdev():
 return (c()*(pmNs()**f()))*scedPercent()/100

ScedPercents = dict(vl=75, l=85, n=100, h=130, vh=160)

def scedPercent(): 
  return ScedPercents[sced()]

def f():
  return d()+0.2*(e()-b())

def pm():
  return pmNs()*sced()+pmAuto()

def pmNs():
  return a()    * (size()**e())   *          \
 	 rely() * data() * cplx() * ruse() *  \
	 docu() * time() * stor() *            \
	 pvol() * acap() * pcap() *             \
	 pcon() * apex() * plex() *              \
	 ltex() * tool() * site() 

def e():
  return b() + 0.01*(prec() + flex() + resl() + team() + pmat()) 

def pmAuto():
  return ((adaptedKsloc()*(at()/100))/atKProd())

def a(): return 2.5  if (cocomo()==1983) else 2.94
def b(): return 0.91 if (cocomo()==2000) else 1.01
def c(): return 3.0  if (cocomo()==1983) else 3.67
def d(): return 0.28 if (cocomo()==2000) else 0.33

#=head2 Factors & Multipliers

 BEGIN {if(ScaleEffortFile)
   readtable(ScaleEffortFile,ScaleEffort);
 }

 function readtable(file,a,   i,f,line,n,tab) {
   while ((getline line < file) > 0) {
     n=split(line,f,/,/);
     for(i=1;i<=n;i++) f[i]=trim(f[i]);
     if (match(f[1],/^=/)) {
       tab=rhs(f[1]);
       for(i=1;i<n;i++) label[i]=f[i+1];
     } else {
       for(i=1;i<n;i++) a[tab,f[1],label[i]]=f[i+1]}}
 }

