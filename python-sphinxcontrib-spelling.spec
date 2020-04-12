#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Sphinx spell checking extension
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do sprawdzania pisowni
Name:		python-sphinxcontrib-spelling
# keep 4.x here for python 2.x support
Version:	4.3.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-spelling/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-spelling/sphinxcontrib-spelling-%{version}.tar.gz
# Source0-md5:	363cd2f4c485db5e6a3f81572289a1e7
URL:		https://pypi.org/project/sphinxcontrib-spelling/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-fixtures >= 3.0.0
BuildRequires:	python-pyenchant >= 1.6.5
BuildRequires:	python-pytest
BuildRequires:	python-six
BuildRequires:	python-subunit >= 0.0.18
BuildRequires:	python-testrepository >= 0.0.18
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 1.4.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-pbr
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testrepository >= 0.0.18
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 1.4.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc} || %{with tests}
# en_US dict for enchant
BuildRequires:	aspell-en
BuildRequires:	enchant-aspell
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-2 >= 1.8.5
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-sphinxcontrib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains sphinxcontrib.spelling, a spelling checker for
Sphinx-based documentation. It uses PyEnchant to produce a report
showing misspelled words.

%description -l pl.UTF-8
Ten pakiet zawiera sphinxcontrib.spelling - rozszerzenie do
sprawdzania pisowni w dokumentacji opartej na Sphinksie. Wykorzystuje
PyEnchant do tworzenia raportu wskazującego błędnie napisane słowa.

%package -n python3-sphinxcontrib-spelling
Summary:	Sphinx spell checking extension
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do sprawdzania pisowni
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5
Requires:	python3-sphinxcontrib

%description -n python3-sphinxcontrib-spelling
This package contains sphinxcontrib.spelling, a spelling checker for
Sphinx-based documentation. It uses PyEnchant to produce a report
showing misspelled words.

%description -n python3-sphinxcontrib-spelling -l pl.UTF-8
Ten pakiet zawiera sphinxcontrib.spelling - rozszerzenie do
sprawdzania pisowni w dokumentacji opartej na Sphinksie. Wykorzystuje
PyEnchant do tworzenia raportu wskazującego błędnie napisane słowa.

%package apidocs
Summary:	API documentation for Python sphinxcontrib-spelling module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinxcontrib-spelling
Group:		Documentation

%description apidocs
API documentation for Python sphinxcontrib-spelling module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinxcontrib-spelling.

%prep
%setup -q -n sphinxcontrib-spelling-%{version}

# sphinxcontrib.spelling 4.2.1 supports Sphinx>=0.6, but doesn't work with Sphinx 1.8.x.
# sphinxcontrib.spelling 4.3.0, which still supports Python 2.7, officially
# requires Sphinx >= 2.0.0 (but Sphinx dropped Python 2 support before 2.0.0
# beta stage), but seems the only version working with python 2.7+Sphinx 1.8.5.
# Additionally verify this combo in tests and by building docs using
# python 2 + Sphinx 1.8.5 + spell checking enabled
%{__sed} -i -e '/Sphinx/ s/2\.0\.0/1.8.5/' requirements.txt

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with tests}
# clean after tests because python3 tests would fail with incompatible repository
%{__rm} -r .testrepository
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with tests}
%{__rm} -r .testrepository
%endif
%endif

%if %{with doc}
# force python2 and enable spell checking to additionally verify particular
# python+sphinx+sphinxcontrib.spelling combo
ENABLE_SPELLING=1 \
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINX_BUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README
%{py_sitescriptdir}/sphinxcontrib/spelling
%{py_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*.egg-info
%{py_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-sphinxcontrib-spelling
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README
%{py3_sitescriptdir}/sphinxcontrib/spelling
%{py3_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*.egg-info
%{py3_sitescriptdir}/sphinxcontrib_spelling-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
