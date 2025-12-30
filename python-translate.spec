%define pname translate
%define oname %{pname}-toolkit

Summary:	Software localization toolkit
Name:		python-%{pname}
Version:	3.6.1
Release:	2
License:	GPLv2+
Group:		Development/Python
Url:		https://translate.sourceforge.net/
Source0:	https://files.pythonhosted.org/packages/source/t/translate/%{pname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-lxml
BuildRequires:	python-simplejson
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(pip)
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
%autosetup -p1 -n %{pname}-%{version}

%build
%py_build

%install
%py_install

%files
%{_bindir}/*
%{py_puresitedir}/%{pname}
%{py_puresitedir}/translate-%{version}-py%{py_ver}.egg-info
