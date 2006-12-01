Summary:	TeX to XML translator
Summary(pl):	Konwerter z TeXa do XML-a
Name:		tex4ht
Version:	20050228
Release:	0.1
License:	LaTeX Project Public License
Group:		Applications/Publishing/TeX
Source0:	http://www.ctan.org/tex-archive/support/TeX4ht/%{name}-all.zip
# Source0-md5:	26eb8df2d6631794b3df0d6fb87a0219
Patch0:		%{name}-env-giftrans.patch
BuildRequires:	unzip
Requires:	ghostscript >= 4.03
Requires:	giftrans
Requires:	netpbm-progs
Requires:	tetex-dvips >= 0.4
Requires:	tetex-latex >= 0.4
# latex2html is required for pstoimg script, that is provided by it
# see Patch0
#Requires:	latex2html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Program to convert (La)TeX documents to XML, using (La)TeX to process
images and equations.

%description -l pl
Program do konwertowania dokumentów (La)TeXa do formatu XML przy
u¿yciu (La)TeXa do przetwarzania obrazów i równañ.

%prep
%setup -q -c
unzip -q %{name}.zip
#%patch0 -p0

%build
cd src
%{__cc} %{rpmldflags} %{rpmcflags} -o tex4ht tex4ht.c -DHAVE_DIRENT_H
%{__cc} %{rpmldflags} %{rpmcflags} -o t4ht t4ht.c -DHAVE_DIRENT_H
%{__cc} %{rpmldflags} %{rpmcflags} -o htcmd htcmd.c -DHAVE_DIRENT_H

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_bindir}}

install src/{tex4ht,t4ht,htcmd} $RPM_BUILD_ROOT%{_bindir}
for f in bin/unix/* ; do
	cat $f | sed -e 's!~/tex4ht\.dir!%{_datadir}!' |\
	sed -e 's! -i! -e%{_datadir}/texmf/tex4ht/base/tex4ht.env -i!' |\
	sed -e 's!## -d.*$!-e%{_datadir}/texmf/tex4ht/base/tex4ht.env!' >$f.tmp

	mv $f.tmp $f
done
for f in bin/unix/oo* ; do
	sed -e 's!t4ht -f/$1 $4 -coo!t4ht -f/$1 $4 -coo -e%{_datadir}/texmf/tex4ht/base/tex4ht.env!' -i $f;
done

install bin/unix/* $RPM_BUILD_ROOT%{_bindir}

mkdir docs
mv *.html *.css *.png docs

cp -r texmf $RPM_BUILD_ROOT%{_datadir}
cd $RPM_BUILD_ROOT%{_datadir}/texmf/tex4ht/base

cat unix/tex4ht.env | sed -e 's!~/tex4ht\.dir!%{_datadir}!' | \
	sed -e 's!path/tex!%{_datadir}!' >./tex4ht.env
rm -r win32
rm -r unix

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p %{_bindir}/mktexlsr
%postun -p %{_bindir}/mktexlsr

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/texmf/tex/generic/tex4ht
%{_datadir}/texmf/tex/generic/tex4ht/*.4ht
%{_datadir}/texmf/tex/generic/tex4ht/tex4ht.sty
%{_datadir}/texmf/tex4ht
