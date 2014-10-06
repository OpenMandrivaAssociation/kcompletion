%define major 5
%define libname %mklibname KF5Completion %{major}
%define devname %mklibname KF5Completion -d
%define debug_package %{nil}

Name: kcompletion
Version: 5.3.0
Release: 1
Source0: http://ftp5.gwdg.de/pub/linux/kde/stable/frameworks/%{version}/%{name}-%{version}.tar.xz
Summary: The KDE Frameworks 5 auto-completion library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(KF5Config) kconfig
BuildRequires: cmake(KF5WidgetsAddons)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: qmake5
BuildRequires: extra-cmake-modules5
BuildRequires: ninja
Requires: %{libname} = %{EVRD}

%description
The KDE Frameworks 5 auto-completion library.

%package -n %{libname}
Summary: The KDE Frameworks 5 auto-completion library
Group: System/Libraries

%description -n %{libname}
The KDE Frameworks 5 auto-completion library.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -q
%cmake

%build
%make -C build

%install
%makeinstall_std -C build
mkdir -p %{buildroot}%{_libdir}/qt5
mv %{buildroot}%{_prefix}/mkspecs %{buildroot}%{_libdir}/qt5

L="`pwd`/%{name}.lang"
cd %{buildroot}
for i in .%{_datadir}/locale/*/LC_MESSAGES/*.qm; do
	LNG=`echo $i |cut -d/ -f5`
	echo -n "%lang($LNG) " >>$L
	echo $i |cut -b2- >>$L
done

%files -f %{name}.lang

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Completion
%{_libdir}/qt5/mkspecs/modules/*.pri
