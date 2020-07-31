#
# spec file for package fcitx5
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
%global debug_package %{nil}

Name:           fcitx5
Version:        4.99.0+git20200730.297308b
Release:        1
Summary:        Next generation of fcitx
License:        LGPL-2.1-or-later
Group:          System/I18n/Chinese
Url:            https://gitlab.com/fcitx/fcitx5
Source:         %{name}-%{version}.tar.gz
Source1:        en_dict-20121020.tar.gz
Source2:        https://raw.githubusercontent.com/fcitx/fcitx-artwork/master/logo/Fcitx.svg
Source3:        xim.d-fcitx5
Source4:        macros.fcitx5
Source99:       baselibs.conf

BuildRequires:  cldr-emoji-annotation-devel
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  xcb-imdkit-devel
BuildRequires:  enchant-devel
BuildRequires:  systemd-devel
BuildRequires:  dbus-devel
BuildRequires:  libevent-devel
BuildRequires:  json-c-devel
BuildRequires:  libuuid-devel
BuildRequires:  fmt-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  iso-codes-devel
BuildRequires:  expat-devel
BuildRequires:  xkeyboard-config
BuildRequires:  xkeyboard-config-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  pango-devel
BuildRequires:  cairo-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  librsvg2
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  fdupes
Requires:       libFcitx5Config5 = %{version}
Requires:       libFcitx5Core5 = %{version}
Requires:       libFcitx5Utils1 = %{version}
Recommends:     fcitx5-gtk2
Recommends:     fcitx5-gtk3
Recommends:     fcitx5-qt4
Recommends:     fcitx5-qt5
Provides:       fcitx = %{version}
Obsoletes:      fcitx <= 4.2.9.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Fcitx 5 is a generic input method framework.

%package devel
Summary:    Development files for fcitx5
Group:      Development/Libraries/C and C++
Requires:   fcitx5 = %{version}

%description devel
This package provides development files for fcitx5.

%package -n libFcitx5Config5
Summary:    Configuration library for fcitx5
Group:      System/Libraries

%description -n libFcitx5Config5
This package provides configuration libraries for fcitx5.

%package -n libFcitx5Core5
Summary:    Core library for fcitx5
Group:      System/Libraries
Provides:   libfcitx-4_2_9 = %{version}
Obsoletes:  libfcitx-4_2_9 <= 4.2.9.6

%description -n libFcitx5Core5
This package provides core libraries for fcitx5.

%package -n libFcitx5Utils1
Summary:    Utility library for fcitx5
Group:      System/Libraries

%description -n libFcitx5Utils1
This package provides utility libraries for fcitx5.

%prep
%setup -q
%patch -p1
ln -s %{SOURCE1} src/modules/spell/dict/

%build
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_LIBDIR=/usr/lib64 .
%make_build

%install
%make_install

# create autostart
mkdir -p %{buildroot}%{_sysconfdir}/X11/xim.d/
install -m 644 %{S:3} %{buildroot}%{_sysconfdir}/X11/xim.d/fcitx

priority=30
pushd  %{buildroot}%{_sysconfdir}/X11/xim.d/
    for lang in am ar as bn el fa gu he hi hr ja ka kk kn ko lo ml my \
                pa ru sk vi zh_TW zh_CN zh_HK zh_SG \
                de fr it es nl cs pl da nn nb fi en sv ; do
        mkdir $lang
        pushd $lang
            ln -s ../fcitx $priority-fcitx
        popd
    done
popd

# install icons
for i in 16 22 24 32 48 512; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
  rsvg-convert -h $i -w $i %{S:2} -o %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/fcitx.png
done
install -D -m 0644 %{S:2} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/fcitx.svg

desktop-file-install                                    \
        --delete-original                               \
        --dir %{buildroot}%{_datadir}/applications      \
        %{buildroot}%{_datadir}/applications/fcitx5.desktop

desktop-file-install                                    \
        --delete-original                               \
        --dir %{buildroot}%{_datadir}/applications      \
        %{buildroot}%{_datadir}/applications/fcitx5-configtool.desktop

# own directories
mkdir -p %{buildroot}%{_datadir}/fcitx5/inputmethod
mkdir -p %{buildroot}%{_libdir}/fcitx5/qt5

# install macros.fcitx5
install -Dm 0755 %{S:4} %{buildroot}%{_sysconfdir}/rpm/macros.fcitx5

%find_lang fcitx5
%fdupes %{buildroot}

%post -p /sbin/ldconfig
%post -n libFcitx5Config5 -p /sbin/ldconfig
%post -n libFcitx5Core5 -p /sbin/ldconfig
%post -n libFcitx5Utils1 -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%postun -n libFcitx5Config5 -p /sbin/ldconfig
%postun -n libFcitx5Core5 -p /sbin/ldconfig
%postun -n libFcitx5Utils1 -p /sbin/ldconfig

%files -f fcitx5.lang
%defattr(-,root,root)
%doc README.md LICENSES/LGPL-2.1-or-later.txt
%config %{_sysconfdir}/X11/xim.d/
%{_bindir}/fcitx5
%{_bindir}/fcitx5-configtool
%{_bindir}/fcitx5-remote
%{_libdir}/fcitx5
%{_datadir}/applications/fcitx5.desktop
%{_datadir}/applications/fcitx5-configtool.desktop
%{_datadir}/fcitx5
%{_datadir}/icons/hicolor/*/apps/fcitx.*

%files devel
%defattr(-,root,root)
%{_sysconfdir}/rpm/macros.fcitx5
%{_includedir}/Fcitx5
%{_libdir}/cmake/Fcitx5*
%{_libdir}/libFcitx5Config.so
%{_libdir}/libFcitx5Core.so
%{_libdir}/libFcitx5Utils.so
%{_libdir}/pkgconfig/Fcitx5*.pc

%files -n libFcitx5Config5
%defattr(-,root,root)
%{_libdir}/libFcitx5Config.so.5
%{_libdir}/libFcitx5Config.so.5.0

%files -n libFcitx5Core5
%defattr(-,root,root)
%{_libdir}/libFcitx5Core.so.5
%{_libdir}/libFcitx5Core.so.5.0

%files -n libFcitx5Utils1
%defattr(-,root,root)
%{_libdir}/libFcitx5Utils.so.1
%{_libdir}/libFcitx5Utils.so.1.0

%changelog
