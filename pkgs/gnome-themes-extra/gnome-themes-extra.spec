Name:           gnome-themes-extra
Version:        3.28
Release:        7%{?dist}
Summary:        GNOME Extra Themes

License:        LGPLv2+
URL:            https://gitlab.gnome.org/GNOME/gnome-themes-extra
Source0:        https://download.gnome.org/sources/%{name}/3.28/%{name}-%{version}.tar.xz
Source1:        gtkrc

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  /usr/bin/gtk-update-icon-cache

Recommends: adwaita-gtk2-theme = %{version}-%{release}
Requires: adwaita-icon-theme

# Renamed in F28
Obsoletes: gnome-themes-standard < 3.28
Provides: gnome-themes-standard = %{version}-%{release}
Provides: gnome-themes-standard%{_isa} = %{version}-%{release}

%description
This module houses themes and theme-y tidbits that don’t really fit in anywhere
else, or deserve their own module. At the moment this consists of:

 * The GTK+ 2 version of Adwaita
 * Adwaita-dark as a separate theme, along with its GTK+ 2 equivalent
 * GTK+ 2 versions of the HighContrast themes
 * The legacy HighContrast icon theme
 * Index files needed for Adwaita to be used outside of GNOME

Once named gnome-themes-standard, this module used to contain various
components of the default GNOME 3 theme. However, at this point, most it has
moved elsewhere. The GTK+ 3 versions of the Adwaita and HighContrast themes are
now part of GTK+ 3 itself, and the HighContrastInverse and LowConstrast themes
have been discontinued.

Not to be confused with gnome-themes-extras.

%package -n adwaita-gtk2-theme
Summary: Adwaita gtk2 theme
Requires: gtk2%{_isa}

%description -n adwaita-gtk2-theme
The adwaita-gtk2-theme package contains a gtk2 theme for presenting widgets
with a GNOME look and feel.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/HighContrast/icon-theme.cache
touch $RPM_BUILD_ROOT%{_datadir}/icons/HighContrast/icon-theme.cache

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-2.0
cp -a $RPM_SOURCE_DIR/gtkrc $RPM_BUILD_ROOT%{_datadir}/gtk-2.0/gtkrc

%transfiletriggerin -- %{_datadir}/icons/HighContrast
gtk-update-icon-cache --force %{_datadir}/icons/HighContrast &>/dev/null || :

%transfiletriggerpostun -- %{_datadir}/icons/HighContrast
gtk-update-icon-cache --force %{_datadir}/icons/HighContrast &>/dev/null || :

%files
%license LICENSE
%doc NEWS README.md
%dir %{_datadir}/icons/HighContrast
%{_datadir}/icons/HighContrast/16x16/
%{_datadir}/icons/HighContrast/22x22/
%{_datadir}/icons/HighContrast/24x24/
%{_datadir}/icons/HighContrast/32x32/
%{_datadir}/icons/HighContrast/48x48/
%{_datadir}/icons/HighContrast/256x256/
%{_datadir}/icons/HighContrast/scalable/
%{_datadir}/icons/HighContrast/index.theme
%ghost %{_datadir}/icons/HighContrast/icon-theme.cache
%{_datadir}/themes/Adwaita/gtk-3.0/
%{_datadir}/themes/Adwaita-dark/gtk-3.0/
%{_datadir}/themes/HighContrast/gtk-3.0/

%files -n adwaita-gtk2-theme
%license LICENSE
%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.so
%{_datadir}/gtk-2.0/gtkrc
%dir %{_datadir}/themes/Adwaita
%{_datadir}/themes/Adwaita/gtk-2.0/
%{_datadir}/themes/Adwaita/index.theme
%dir %{_datadir}/themes/Adwaita-dark
%{_datadir}/themes/Adwaita-dark/gtk-2.0/
%{_datadir}/themes/Adwaita-dark/index.theme
%dir %{_datadir}/themes/HighContrast
%{_datadir}/themes/HighContrast/gtk-2.0/
%{_datadir}/themes/HighContrast/index.theme

%changelog
* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 3.28-5
- Rebuilt against fixed atk (#1626575)

* Tue Feb 19 2019 Pete Walter <pwalter@fedoraproject.org> - 3.28-4
- Drop font requires

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 13 2018 Pete Walter <pwalter@fedoraproject.org> - 3.28-1
- Rename gnome-themes-standard to gnome-themes-extra
