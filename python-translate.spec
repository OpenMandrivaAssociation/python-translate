%define pname translate
%define oname %{pname}-toolkit

Summary: Software localization toolkit
Name:    python-%{pname}
Version: 1.9.0
Release: 3
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
%defattr(-,root,root)
%doc %{pname}/README
%{_bindir}/*
%{py_puresitedir}/%{pname}
%{py_puresitedir}/translate_toolkit-%{version}-py%{py_ver}.egg-info
%{_mandir}/man1/*


%changelog
* Tue Sep 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.9.0-0.1
- 1.9.0

* Wed Feb 23 2011 Michael Scherer <misc@mandriva.org> 1.8.1-1mdv2011.0
+ Revision: 639460
- upgrade to 1.8.1

* Sat Oct 30 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.8.0-1mdv2011.0
+ Revision: 590594
- update to 1.8.0
- drop patches 0 and 1, merged upstream
- sync spec with Fedora:
  o change some suggests into requires
  o add BR, python-lxml and python-simplejson to generate the man pages
  o as python-psyco is only available for i586, make it only required for %%ix86
- drop obsolete python macro
- use %%pyver macro in the file list

* Tue Jul 27 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.7.0-1mdv2011.0
+ Revision: 560894
- update to 1.7.0
- add two patches from Fedora
- create manpages (Fedora)

* Tue Feb 02 2010 Frederik Himpe <fhimpe@mandriva.org> 1.5.3-1mdv2010.1
+ Revision: 499750
- update to new version 1.5.3

* Tue Jan 12 2010 Jérôme Brenier <incubusss@mandriva.org> 1.5.2-1mdv2010.1
+ Revision: 490100
- new version 1.5.2

* Wed Dec 09 2009 Jérôme Brenier <incubusss@mandriva.org> 1.5.1-2mdv2010.1
+ Revision: 475714
- Suggests : python-psyco python-simplejson python-enchant python-vobject
  python-iniparse (spotted by Alaa Abd el Fattah #56308)

* Wed Dec 09 2009 Jérôme Brenier <incubusss@mandriva.org> 1.5.1-1mdv2010.1
+ Revision: 475602
- new version 1.5.1

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.1-1mdv2010.1
+ Revision: 462187
- update to new version 1.4.1

* Tue Aug 11 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.0-1mdv2010.0
+ Revision: 415157
- update to new version 1.4.0

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add a suggests on 'python-levenshtein'

* Sat May 23 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.3.0-2mdv2010.0
+ Revision: 378867
- add dependency on python-lxml (required by at least pretranslate..)

* Fri Feb 13 2009 Frederik Himpe <fhimpe@mandriva.org> 1.3.0-1mdv2009.1
+ Revision: 340122
- update to new version 1.3.0

* Wed Jan 14 2009 Funda Wang <fwang@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 329483
- add provides
- New version 1.2.1

* Sun Dec 28 2008 Funda Wang <fwang@mandriva.org> 1.2.0-2mdv2009.1
+ Revision: 320351
- rebuild for new python

* Mon Oct 20 2008 Funda Wang <fwang@mandriva.org> 1.2.0-1mdv2009.1
+ Revision: 295683
- New version 1.2.0

* Mon Oct 20 2008 Funda Wang <fwang@mandriva.org> 1.0.1-5mdv2009.1
+ Revision: 295682
- should use --root rather than --prefix

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1.0.1-4mdv2009.0
+ Revision: 259837
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.0.1-3mdv2009.0
+ Revision: 247701
- rebuild

* Thu Jan 17 2008 Olivier Blin <oblin@mandriva.com> 1.0.1-1mdv2008.1
+ Revision: 154232
- 1.0.1

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.10.1-1mdv2008.1
+ Revision: 140738
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Jan 12 2007 Olivier Blin <oblin@mandriva.com> 0.10.1-1mdv2007.0
+ Revision: 107921
- buildrequires python-devel
- initial python-translate release
- Create python-translate

