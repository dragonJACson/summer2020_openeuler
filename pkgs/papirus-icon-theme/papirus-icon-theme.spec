#
# spec file for package papirus-icon-theme for fedora centos and redhat enterprise linux 7
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


Name:           papirus-icon-theme
Version:        20200702
Release:        1
License:        LGPLv3
Summary:        Papirus icon theme
Url:            https://github.com/PapirusDevelopmentTeam/papirus-icon-theme
Group:          User Interface/Desktops
Source:         https://github.com/PapirusDevelopmentTeam/%{name}/archive/%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Papirus is a free and open source SVG icon theme for Linux,
based on Paper Icon Set with a lot of new icons and a few
extras, like Hardcode-Tray support, KDE colorscheme support,
Folder Color support, and other.

This package contains the following icon themes:

 - ePapirus
 - Papirus
 - Papirus-Dark
 - Papirus-Light

%prep
%setup -q

%install
%make_install

%build

%post
for theme in \
    ePapirus \
    Papirus \
    Papirus-Dark \
    Papirus-Light 
do
    /bin/touch --no-create /usr/share/icons/${theme} &>/dev/null || :
    /usr/bin/gtk-update-icon-cache -q /usr/share/icons/${theme} || :
done

# Try to restore the color of folders from a config
if which papirus-folders &>/dev/null; then
  sudo papirus-folders -R || true
fi

%postun
if [ $1 -eq 0 ]; then
    for theme in \
        ePapirus \
        Papirus \
        Papirus-Dark \
        Papirus-Light 
    do
        /bin/touch --no-create /usr/share/icons/${theme} &>/dev/null || :
        /usr/bin/gtk-update-icon-cache -q /usr/share/icons/${theme} || :
    done
fi

%files
%defattr(-,root,root)
%doc LICENSE README.md
%{_datadir}/icons/ePapirus
%{_datadir}/icons/Papirus
%{_datadir}/icons/Papirus-Dark
%{_datadir}/icons/Papirus-Light
%ghost %{_datadir}/icons/ePapirus/icon-theme.cache
%ghost %{_datadir}/icons/Papirus/icon-theme.cache
%ghost %{_datadir}/icons/Papirus-Dark/icon-theme.cache
%ghost %{_datadir}/icons/Papirus-Light/icon-theme.cache

%changelog
* Thu Nov 9 2017 Sergei Eremenko <finalitik@gmail.com> - 20171102-1
- Addded Papirus-Adapta-Nokto
- Added papirus-folders (https://git.io/papirus-folders) support
* Sun Sep 17 2017 Dirk Davidis <davidis.dirk@gmail.com> - 20170916-1
- Addded Papirus Adapta
* Sun Feb 26 2017 Dirk Davidis <davidis.dirk@gmail.com> - 20170225-1
- Initial Build depending on the OBS Build provided by Konstantin Voinov for openSUSE
