#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kldap
Summary:	LDAP access API for KDE
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	00178a3ba0c799e21789853d8dc600a6
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Keychain-devel >= 0.12.0
BuildRequires:	Qt6Test-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	cyrus-sasl-devel
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kldap - an LDAP access API for KDE.

%description -l pl.UTF-8
kldap - API do dostępu do usług LDAP dla KDE.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{ko,sr}
%find_lang %{kaname}_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}_qt.lang
%defattr(644,root,root,755)
%{_libdir}/libKPim6LdapCore.so.*.*
%ghost %{_libdir}/libKPim6LdapCore.so.6
%{_libdir}/libKPim6LdapWidgets.so.*.*
%ghost %{_libdir}/libKPim6LdapWidgets.so.6
%{_libdir}/qt6/plugins/kf6/kio/ldap.so
%{_datadir}/qlogging-categories6/kldap.categories
%{_datadir}/qlogging-categories6/kldap.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/KLDAPCore
%{_includedir}/KPim6/KLDAPWidgets
%{_libdir}/cmake/KPim6LdapCore
%{_libdir}/cmake/KPim6LdapWidgets
%{_libdir}/libKPim6LdapCore.so
%{_libdir}/libKPim6LdapWidgets.so
