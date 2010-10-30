%define pname translate
%define oname %{pname}-toolkit
%define name python-%{pname}
%define version 1.8.0
%define release %mkrel 1

Summary: Software localization toolkit
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
License: GPLv2+
Group: Development/Python
Url: http://translate.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: python-devel
# (Fedoar) those are needed for mange page generation
BuildRequires: python-lxml
BuildRequires: python-simplejson
Requires: python-lxml
Requires: python-levenshtein
Requires: python-simplejson
Requires: python-enchant
Requires: python-vobject
Requires: python-iniparse
# for sub2po and po2sub
Requires: python-aeidon
# python-pysco is only available for i586
%ifarch %{ix86}
Requires: python-psyco
%endif
Provides: %{oname} = %{version}-%{release}

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
various localization storage formats: DTD, properties, OpenOffice.org
GSI/SDF, CSV and of course PO.  And scripts to convert between these
formats.

Also part of the Toolkit are Python programs to create word counts,
merge translations and perform various checks on PO files.

%prep
%setup -q -n %{oname}-%{version}

%build
./setup.py build

%install
rm -rf %{buildroot}
./setup.py install --root=%{buildroot}

# (Fedora) create manpages
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
for program in $RPM_BUILD_ROOT/%{_bindir}/*; do
    case $(basename $program) in
      pocompendium|poen|pomigrate2|popuretext|poreencode|posplit|\
      pocount|poglossary|lookupclient.py|tmserver|build_tmdb|\
      junitmsgfmt)
       ;;
      *)
        LC_ALL=C PYTHONPATH=. $program --manpage \
          >  $RPM_BUILD_ROOT/%{_mandir}/man1/$(basename $program).1 \
          || rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/$(basename $program).1
          ;;
    esac
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{pname}/README
%{_bindir}/*
%{py_puresitedir}/%{pname}
%{py_puresitedir}/translate_toolkit-%{version}-py%{pyver}.egg-info
%{_mandir}/man1/*
