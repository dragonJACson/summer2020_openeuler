#
# spec file for package fcitx5-gtk
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


Name:           fcitx5-gtk
Version:        4.99.0+git20200607.fc335f1
Release:        0
Summary:        Gtk im module for fcitx5 and glib based dbus client library
License:        LGPL-2.1-or-later
Group:          System/I18n/Chinese
Url:            https://gitlab.com/fcitx/fcitx5-gtk
Source:         %{name}-%{version}.tar.gz
Source99:       baselibs.conf
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  fcitx5-devel
BuildRequires:  gobject-introspection-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Gtk im module for fcitx5 and glib based dbus client library.

%package -n libFcitx5GClient-devel
Summary:        Development files for libFcitx5GClient
Group:          Development/Libraries/C and C++
Requires:       libFcitx5GClient1 = %{version}

%description -n libFcitx5GClient-devel
This package provides development files for libFcitx5GClient.

%package -n libFcitx5GClient1
Summary:        GClient library for fcitx5
Group:          System/Libraries

%description -n libFcitx5GClient1
This package provides GClient library for fcitx5.

%package -n fcitx5-gtk2
Summary:        GTK+ 2.0 im module for fcitx5
Group:          System/I18n/Chinese
%gtk2_immodule_requires
Provides:       fcitx-gtk2 = %{version}
Obsoletes:      fcitx-gtk2 <= 4.2.9.6

%description -n fcitx5-gtk2
This package provides GTK+ 2.0 im module for fcitx5.

%package -n fcitx5-gtk3
Summary:        GTK+ 3.0 im module for fcitx5
Group:          System/I18n/Chinese
%gtk3_immodule_requires
Provides:       fcitx-gtk3 = %{version}
Obsoletes:      fcitx-gtk3 <= 4.2.9.6

%description -n fcitx5-gtk3
This package provides GTK+ 3.0 im module for fcitx5.

%package -n typelib-1_0-FcitxG-1_0
Summary:        Introspection bindings for fcitx5
Group:          System/Libraries
Provides:       typelib-1_0-Fcitx-1_0 = %{version}
Obsoletes:      typelib-1_0-Fcitx-1_0 <= 4.2.9.6

%description -n typelib-1_0-FcitxG-1_0
This package provides the GObject Introspection bindings for fcitx5.

%prep
%setup -q

%build
%cmake
make %{?_smp_mflags}

%install
%cmake_install

%post -n libFcitx5GClient1 -p /sbin/ldconfig
%post -n fcitx5-gtk2
%gtk2_immodule_post
%post -n fcitx5-gtk3
%gtk3_immodule_post
%postun -n libFcitx5GClient1 -p /sbin/ldconfig
%postun -n fcitx5-gtk2
%gtk2_immodule_postun
%postun -n fcitx5-gtk3
%gtk3_immodule_postun

%files -n libFcitx5GClient-devel
%defattr(-,root,root)
%doc README.md
%{_libdir}/cmake/Fcitx5GClient
%{_libdir}/libFcitx5GClient.so
%{_libdir}/pkgconfig/Fcitx5GClient.pc

%files -n typelib-1_0-FcitxG-1_0
%defattr(-,root,root)
%{_libdir}/girepository-1.0/FcitxG-1.0.typelib
%{_datadir}/gir-1.0/FcitxG-1.0.gir

%files -n libFcitx5GClient1
%defattr(-,root,root)
%{_libdir}/libFcitx5GClient.so.1
%{_libdir}/libFcitx5GClient.so.1.0

%files -n fcitx5-gtk2
%defattr(-,root,root)
%{_libdir}/gtk-2.0/2.10.0/immodules/im-fcitx5.so

%files -n fcitx5-gtk3
%defattr(-,root,root)
%{_libdir}/gtk-3.0/3.0.0/immodules/im-fcitx5.so

%changelog

