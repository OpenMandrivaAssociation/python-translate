%define pname translate
%define oname %{pname}-toolkit
%define name python-%{pname}
%define version 1.7.0
%define release %mkrel 1

Summary: Software localization toolkit
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/translate/%{oname}-%{version}.tar.bz2
# (Fedora) add patch to fix crash with moz2po:
# https://bugzilla.redhat.com/show_bug.cgi?id=603597
Patch0:  translate-toolkit-1.7.0-moz2po_needs_output_dir.patch
# (Fedora) add patch to fix crash in virtaal:
# https://bugzilla.redhat.com/show_bug.cgi?id=600561
Patch1:  translate-toolkit-1.7.0-lang_zh_lamba.patch
License: GPLv2+
Group: Development/Python
Url: http://translate.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: python-lxml
Suggests: python-levenshtein
Suggests: python-psyco
Suggests: python-simplejson
Suggests: python-enchant
Suggests: python-vobject
Suggests: python-iniparse
Provides: %{oname} = %{version}-%{release}
%py_requires -d

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
%patch0 -p2 -b .moz2po_needs_output_dir
%patch1 -p2 -b .lang_zh_lamba

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
%{py_puresitedir}/*.egg-info
%{_mandir}/man1/*
