Summary:	TeX to XML translator
Summary(pl):	Konwerter z TeXa do XML
Name:		tex4ht
Version:	20030211
Release:	1
License:	LaTeX Project Public License
Group:		Applications/Publishing/TeX
Source0:	http://www.ctan.org/tex-archive/support/TeX4ht/%{name}-mn.zip
# Source0-md5:	c62ac8170b319602f88f1ed4016119b2
Patch0:		%{name}-env-giftrans.patch
Requires:	ghostscript >= 4.03
Requires:	giftrans
Requires:	netpbm-progs
Requires:	tetex-dvips >= 0.4
Requires:	tetex-latex >= 0.4
# latex2html is required for pstoimg script, that is provided by it
# see Patch0
Requires:	latex2html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Program to convert (la)tex documents to xml, using (La)TeX to process
images and equations.

%description -l pl
Program do konwertowania dokumentów TeXa do formatu XML.

%prep
%setup -q -c %{name}-%{version}
unzip -q %{name}.zip
%patch0 -p0

%build
cd temp
%{__cc} %{rpmldflags} %{rpmcflags} -o tex4ht tex4ht.c -DHAVE_DIRENT_H
%{__cc} %{rpmldflags} %{rpmcflags} -o t4ht t4ht.c -DHAVE_DIRENT_H
%{__cc} %{rpmldflags} %{rpmcflags} -o htcmd htcmd.c -DHAVE_DIRENT_H

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_bindir}}

install temp/{tex4ht,t4ht,htcmd} $RPM_BUILD_ROOT%{_bindir}
for f in bin/unix/* ; do
	cat $f | sed -e 's!~/tex4ht\.dir!%{_datadir}!' |\
	sed -e 's! -i!-e%{_datadir}/texmf/tex4ht/base/tex4ht.env -i!'  |\
	sed -e 's!## -d.*$!-e%{_datadir}/texmf/tex4ht/base/tex4ht.env!' >$f.tmp

	mv $f.tmp $f
done
install bin/unix/*  $RPM_BUILD_ROOT%{_bindir}

mkdir docs
mv *.html *.css *.gif docs

cp -r texmf  $RPM_BUILD_ROOT%{_datadir}
cd $RPM_BUILD_ROOT%{_datadir}/texmf/tex4ht/base/

cat unix/tex4ht.env | sed -e 's!~/tex4ht\.dir!%{_datadir}!' | \
	sed -e 's!path/tex!%{_datadir}!' >./tex4ht.env
rm -r win32
rm -r unix

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p %{_bindir}/mktexlsr
%postun -p %{_bindir}/mktexlsr

%files
%defattr(644,root,root,755)
%doc docs/*

%attr(755,root,root) %{_bindir}/*

%{_datadir}/texmf/tex4ht

%dir %{_datadir}/texmf/tex/generic/tex4ht
%{_datadir}/texmf/tex/generic/tex4ht/*.4ht
%{_datadir}/texmf/tex/generic/tex4ht/tex4ht.sty
