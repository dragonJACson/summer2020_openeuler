#
# spec file for package xcb-imdkit
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define _suffix 0
Name:           xcb-imdkit
Version:        0.1.0+git20200607.709ddd7
Release:        0
Summary:        An implementation of xim protocol in xcb
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
Url:            https://gitlab.com/fcitx/xcb-imdkit
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
xcb-imdkit is an implementation of xim protocol in xcb, comparing with the
implementation of IMDkit with Xlib, and xim inside Xlib, it has less memory
foot print, better performance, and safer on malformed client.

%package -n libxcb-imdkit%{_suffix}
Summary:        An implementation of xim protocol in xcb
Group:          System/Libraries

%description -n libxcb-imdkit%{_suffix}
xcb-imdkit is an implementation of xim protocol in xcb, comparing with the
implementation of IMDkit with Xlib, and xim inside Xlib, it has less memory
foot print, better performance, and safer on malformed client.

%package devel
Summary:        Development files for xcb-imdkit
Group:          Development/Libraries/C and C++
Requires:       libxcb-imdkit%{_suffix} = %{version}

%description devel
This package provides development files for xcb-imdkit.

%prep
%setup -q

%build
%cmake
make %{?_smp_mflags}

%install
%cmake_install

%post -n libxcb-imdkit%{_suffix} -p /sbin/ldconfig
%postun -n libxcb-imdkit%{_suffix} -p /sbin/ldconfig

%files -n libxcb-imdkit%{_suffix}
%defattr(-,root,root)
%doc LICENSE README.md
%{_libdir}/libxcb-imdkit.so.%{_suffix}
%{_libdir}/libxcb-imdkit.so.%{_suffix}.1

%files devel
%defattr(-,root,root)
%{_includedir}/xcb-imdkit
%{_libdir}/cmake/XCBImdkit
%{_libdir}/libxcb-imdkit.so
%{_libdir}/pkgconfig/xcb-imdkit.pc

%changelog

