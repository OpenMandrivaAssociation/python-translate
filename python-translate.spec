%define pname translate
%define oname %{pname}-toolkit

Summary:	Software localization toolkit
Name:		python-%{pname}
Version:	1.9.0
Release:	5
License:	GPLv2+
Group:		Development/Python
Url:		http://translate.sourceforge.net/
Source0:	http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
BuildArch:	noarch
# (Fedoar) those are needed for mange page generation
BuildRequires:	python-lxml
BuildRequires:	python-simplejson
BuildRequires:	pkgconfig(python)
Requires:	python-lxml
Requires:	python-levenshtein
Requires:	python-simplejson
Requires:	python-enchant
Requires:	python-vobject
Requires:	python-iniparse
# for sub2po and po2sub
Requires:	python-aeidon
# python-pysco is only available for i586
%ifarch %{ix86}
Requires:	python-psyco
%endif
Provides:	%{oname} = %{version}-%{release}

%description
The Translate Toolkit is a set of software and documentation designed
to help make the lives of localizers both more productive and less
frustrating.  The Toolkit is part of the translate.sourceforge.net
project, hosted at http://translate.sourceforge.net/

The software includes programs to covert localization formats to the
common PO format and programs to check and manage PO files.  The
documentation includes guides on using the tools, running a
localization project and how to localize various projects from
OpenOffice.org to Mozilla.

At its core the software contains a set of classes for handling
various localization storage formats:	DTD, properties, OpenOffice.org
GSI/SDF, CSV and of course PO.  And scripts to convert between these
formats.

Also part of the Toolkit are Python programs to create word counts,
merge translations and perform various checks on PO files.

%prep
%setup -qn %{oname}-%{version}

%build
./setup.py build

%install
./setup.py install --root=%{buildroot}

# (Fedora) create manpages
mkdir -p %{buildroot}/%{_mandir}/man1
for program in %{buildroot}/%{_bindir}/*; do
    case $(basename $program) in
      pocompendium|poen|pomigrate2|popuretext|poreencode|posplit|\
      pocount|poglossary|lookupclient.py|tmserver|build_tmdb|\
      junitmsgfmt)
       ;;
      *)
        LC_ALL=C PYTHONPATH=. $program --manpage \
          >  %{buildroot}/%{_mandir}/man1/$(basename $program).1 \
          || rm -f %{buildroot}/%{_mandir}/man1/$(basename $program).1
          ;;
    esac
done

# Drop shebang from non-executable scripts to make rpmlint happy
find %{buildroot}%{py_puresitedir} -name "*py" -perm 644 -exec sed -i '/#!\/usr\/bin\/env python/d' {} \;

%files
%doc %{pname}/README
%{_bindir}/*
%{py_puresitedir}/%{pname}
%{py_puresitedir}/translate_toolkit-%{version}-py%{py_ver}.egg-info
%{_mandir}/man1/*

