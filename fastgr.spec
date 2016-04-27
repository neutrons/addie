%global summary Gui to create Gr from SQ
%global srcname fastgr

Name:           python-%{srcname}
Version:        0.0.1
Release:        1%{?dist}
Summary:        %{summary}

License:        MIT
URL:            http://github.com/neutrons/FastGR
#Source0:        https://github.com/neutrons/FastGR/archive/v%{version}.tar.gz
Source0:        fastgr-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
Description goes here

%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       numpy
Conflicts:      python3-%{srcname}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Description goes here

%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-numpy
Conflicts:      python2-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Description goes here

%prep
%autosetup -n fastgr-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files -n python2-%{srcname}
#%license LICENSE
#%doc README.md
%{_bindir}/fastgr
%{python2_sitelib}/*

%files -n python3-%{srcname}
#%license LICENSE
#%doc README.md
%{_bindir}/fastgr
%{python3_sitelib}/*


%changelog
