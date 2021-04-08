%define major 5
%define libname %mklibname KF5Completion %{major}
%define devname %mklibname KF5Completion -d
%define debug_package %{nil}
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name: kcompletion
Version:	5.81.0
Release:	2
Source0: http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
Summary: The KDE Frameworks 5 auto-completion library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF5Config)
BuildRequires: kconfig
BuildRequires: cmake(KF5WidgetsAddons)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: cmake(Qt5UiPlugin)
# For Python bindings
BuildRequires: cmake(PythonModuleGeneration)
BuildRequires: pkgconfig(python3)
BuildRequires: python-qt5-core
BuildRequires: python-qt5-gui
BuildRequires: python-qt5-widgets
# For QCH format docs
BuildRequires: doxygen
BuildRequires: qt5-assistant

%description
The KDE Frameworks 5 auto-completion library.

%package -n %{libname}
Summary: The KDE Frameworks 5 auto-completion library
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
The KDE Frameworks 5 auto-completion library.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n %{name}-devel-docs
Summary: Developer documentation for %{name} for use with Qt Assistant
Group: Documentation
Suggests: %{devname} = %{EVRD}

%description -n %{name}-devel-docs
Developer documentation for %{name} for use with Qt Assistant

%package -n python-%{name}
Summary: Python bindings for %{name}
Group: System/Libraries
Requires: %{libname} = %{EVRD}

%description -n python-%{name}
Python bindings for %{name}

%package designer
Summary: Qt Designer plugin for handling %{name} widgets
Group: Development/KDE and Qt
Requires: %{libname} = %{EVRD}

%description designer
Qt Designer plugin for handling %{name} widgets

%files designer
%{_libdir}/qt5/plugins/designer/*.so

%prep
%autosetup -p1
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

L="`pwd`/%{name}.lang"
cd %{buildroot}
for i in .%{_datadir}/locale/*/LC_MESSAGES/*.qm; do
	LNG=`echo $i |cut -d/ -f5`
	echo -n "%lang($LNG) " >>$L
	echo $i |cut -b2- >>$L
done

# Let's not ship py2 crap unless and until something still needs it...
rm -rf %{buildroot}%{_libdir}/python2*

[ -s %{buildroot}%{python_sitearch}/PyKF5/__init__.py ] || rm -f %{buildroot}%{python_sitearch}/PyKF5/__init__.py

%files -f %{name}.lang
%{_datadir}/qlogging-categories5/*.*categories

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Completion
%{_libdir}/qt5/mkspecs/modules/*.pri

%files -n %{name}-devel-docs
%{_docdir}/qt5/*.{tags,qch}

%files -n python-%{name}
%dir %{python_sitearch}/PyKF5
%{python_sitearch}/PyKF5/KCompletion.so
%dir %{_datadir}/sip/PyKF5
%{_datadir}/sip/PyKF5/KCompletion
