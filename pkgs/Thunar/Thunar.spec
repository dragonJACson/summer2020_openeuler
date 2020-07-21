%global _hardened_build 1
%global minorversion 1.8
%global xfceversion 4.14

Name:           Thunar
Version:        1.8.15
Release:        1%{?dist}
Summary:        Thunar File Manager

License:        GPLv2+
URL:            http://thunar.xfce.org/
#VCS git:git://git.xfce.org/xfce/thunar
Source0:        http://archive.xfce.org/src/xfce/thunar/%{minorversion}/thunar-%{version}.tar.bz2
Source1:        thunar-sendto-gnome-bluetooth.desktop
Source2:        thunar-sendto-audacious-playlist.desktop
Source3:        thunar-sendto-quodlibet-playlist.desktop
Source4:        thunar-sendto-blueman.desktop

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.34
BuildRequires:  pkgconfig(exo-1) >= 0.12.0
BuildRequires:  pkgconfig(gudev-1.0) >= 145
BuildRequires:  pkgconfig(libexif) >= 0.6.0
BuildRequires:  pkgconfig(libpcre) >= 6.0
BuildRequires:  pkgconfig(libstartup-notification-1.0) >= 0.4
BuildRequires:  pkgconfig(libnotify) >= 0.4.0
BuildRequires:  pkgconfig(libxfce4ui-1) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfce4panel-1.0) >= %{xfceversion}
BuildRequires:  libSM-devel
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel >= 2:1.2.2-16
BuildRequires:  libICE-devel
BuildRequires:  pkgconfig
BuildRequires:  intltool gettext
BuildRequires:  desktop-file-utils >= 0.7
BuildRequires:  libappstream-glib
BuildRequires:  gobject-introspection-devel
Requires:       shared-mime-info
Requires:       dbus-x11

# obsolete xffm to allow for smooth upgrades
Provides:       xffm = 4.2.4
Obsoletes:      xffm <= 4.2.3-5.fc6

# thunar-shares-plugin isn't in F15
Provides:       thunar-shares-plugin = 0.2.0-4
Obsoletes:      thunar-shares-plugin <= 0.2.0-3.fc15

# Provide lowercase name to help people find the package. 
Provides:       thunar = %{version}-%{release}

%description
Thunar is a new modern file manager for the Xfce Desktop Environment. It has 
been designed from the ground up to be fast and easy-to-use. Its user interface 
is clean and intuitive, and does not include any confusing or useless options. 
Thunar is fast and responsive with a good start up time and directory load time.

%package devel
Summary: Development tools for Thunar file manager
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: exo-devel

%description devel
libraries and header files for the Thunar file manager.

%package docs
Summary: GTK docs for Thunar file manager
Requires: %{name} = %{version}-%{release}

%description docs
Thunarx GTK documentation files for the Thunar file manager.

%prep
%autosetup -n thunar-%{version}

# fix icon in thunar-sendto-email.desktop
sed -i 's!internet-mail!mail-message-new!' \
        plugins/thunar-sendto-email/thunar-sendto-email.desktop.in.in

%build
%configure --enable-dbus
# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH="`pwd`/thunarx/.libs"
%make_build


%install
%make_install

# fixes wrong library permissions
chmod 755 %{buildroot}/%{_libdir}/*.so

make -C examples distclean

# 2 of the example files need to not be executable 
# so they don't pull in dependencies. 
chmod 644 examples/thunar-file-manager.py
chmod 644 examples/xfce-file-manager.py

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang thunar

desktop-file-install --delete-original          \
        --dir %{buildroot}/%{_datadir}/applications         \
        %{buildroot}/%{_datadir}/applications/thunar-settings.desktop

desktop-file-install --delete-original          \
        --dir %{buildroot}/%{_datadir}/applications          \
        %{buildroot}/%{_datadir}/applications/thunar-bulk-rename.desktop

#desktop-file-install --delete-original          \
#        --dir %{buildroot}/%{_datadir}/applications         \
#        --remove-mime-type x-directory/gnome-default-handler    \
#        --remove-mime-type x-directory/normal                   \
#        %{buildroot}/%{_datadir}/applications/thunar-folder-handler.desktop

desktop-file-install --delete-original          \
        --dir %{buildroot}/%{_datadir}/applications         \
        %{buildroot}/%{_datadir}/applications/thunar.desktop

# install additional sendto helpers
for source in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} ; do
    desktop-file-install --vendor "" \
            --dir %{buildroot}%{_datadir}/Thunar/sendto \
            $source
done

# appdata
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml


%pre
for target in %{_defaultdocdir}/Thunar/html/*/images
do
       if [ -d $target ]
       then
               rm -rf $target
       fi
done

%ldconfig_scriptlets

%files -f thunar.lang
%license COPYING
%doc README TODO ChangeLog NEWS INSTALL AUTHORS HACKING THANKS
%doc docs/README.gtkrc
# exclude docs that we have moved to the above
%exclude %{_datadir}/doc/thunar/README.gtkrc
%{_bindir}/Thunar
%{_bindir}/thunar
%{_bindir}/thunar-settings
%{_libdir}/libthunar*.so.*
%dir %{_libdir}/thunarx-*/
%{_libdir}/thunarx-*/thunar*.so
%dir %{_libdir}/Thunar/
%{_libdir}/Thunar/ThunarBulkRename
%{_libdir}/Thunar/thunar-sendto-email
%dir %{_datadir}/Thunar/
%dir %{_datadir}/Thunar/sendto/
%{_datadir}/Thunar/sendto/*.desktop
%{_datadir}/polkit-1/actions/org.xfce.thunar.policy
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.xfce.Thunar.FileManager1.service
%{_datadir}/dbus-1/services/org.xfce.FileManager.service
%{_datadir}/dbus-1/services/org.xfce.Thunar.service
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/Thunar/
%{_datadir}/xfce4/panel/plugins/thunar-tpa.desktop
%{_metainfodir}/org.xfce.thunar.appdata.xml
%{_libdir}/xfce4/panel/plugins/libthunar-tpa.so
%{_libdir}/girepository-1.0/*.0.typelib
%{_mandir}/man1/Thunar.1*
%dir %{_sysconfdir}/xdg/Thunar
%config(noreplace) %{_sysconfdir}/xdg/Thunar/uca.xml
%{_userunitdir}/thunar.service

%files devel
%doc examples
%{_includedir}/thunarx-*/
%{_libdir}/libthunar*.so
%{_libdir}/pkgconfig/thunarx-*.pc
%{_datadir}/gir-1.0/*.gir

%files docs
%dir %{_datadir}/gtk-doc/html/thunarx
%{_datadir}/gtk-doc/html/thunarx/*

%changelog
* Sun May 24 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.15-1
- Update to 1.8.15

* Wed Mar 25 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.14-1
- Update to 1.8.14

* Tue Mar 24 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.13-1
- Update to 1.8.13

* Thu Jan 30 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.12-1
- Update to 1.8.12

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Kevin Fenzi <kevin@scrye.com> - 1.8.11-1
- Update to 1.8.11. Fixes bug #1775329

* Wed Aug 28 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.9-2
- Enable session management support

* Mon Aug 12 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.9-1
- Update to 1.8.9

* Tue Jul 30 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 1.8.8-4
- rebuild for xfce 4.14pre3

* Mon Jul 29 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 1.8.8-3
- rebuild for xfce 4.14pre3

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.8-1
- Update to 1.8.8

* Mon Jul 01 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7

* Sat May 18 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.6-1
- Update to 1.8.6

* Sat May 18 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.5-1
- Update to 1.8.5
- Drop patches no longer needed

* Wed Apr 24 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.4-5
- Add newer patch to fix tree view behavior

* Mon Apr 22 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 1.8.4-4
- Add patch to fix tree view weirdness

* Sat Apr 13 2019 Kevin Fenzi <kevin@scrye.com> - 1.8.4-3
- Add gobject introspection files. Fixes bug #1698267

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.4-1
- Update to 1.8.4

* Thu Jan 24 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.3-1
- Update to 1.8.3

* Wed Sep 26 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2 (bugfix update)

* Sat Aug 11 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.1-20
- rebuild for xfce version 4.13

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.1-3
- Add -docs subpackage

* Thu Jun 14 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.1-2
- Fix appdata file installation issues
- Add BR:libappstream-glib

* Thu Jun 14 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1
- Minor spec cleanup

* Thu Apr 05 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.6.15-1
- Update to 1.6.15

* Sat Mar 10 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.14-2
- Add BR:gcc-c++

* Thu Feb 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.6.14-1
- Update to 1.6.14

* Thu Feb 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.6.13-3
- Spec cleanup / modernization

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 26 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.13-1
- Update to 1.6.13
- bugfix update

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Kevin Fenzi <kevin@scrye.com> - 1.6.12-1
- Update to 1.6.12. Fixes bug #1468764

* Mon Feb 13 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.11-1
- Update to 1.6.11
- Dropped upstreamed patches

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 19 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.10-6
- Fix typo in patching

* Thu May 19 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.10-5
- Mitigate move and rename crashes - patches added from upstream

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1.6.10-3
- Remove no longer required AppData file

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.10-1
- Update to 1.6.10 - bugfix update

* Sun May 17 2015 Kevin Fenzi <kevin@scrye.com> 1.6.9-1
- Update to 1.6.9. Drop gtk-docs they are no longer supported upstream.

* Tue May 05 2015 Kevin Fenzi <kevin@scrye.com> 1.6.8-1
- Update to 1.6.8.

* Mon Apr 20 2015 Kevin Fenzi <kevin@scrye.com> 1.6.7-1
- Update to 1.6.7. Fixes bug #1183644

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.6.6-2
- Add an AppData file for the software center

* Sat Feb 28 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.6-1
- Update to 1.6.6

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.6.5-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 19 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.6.5-1
- Update to 1.6.5
- Moved COPYING file to license directory
- Thunar-tpa desktop file moved to ..xfce4/panel/plugins/..

* Sun Jan 04 2015 Kevin Fenzi <kevin@scrye.com> 1.6.4-1
- Update to 1.6.4

* Sun Dec 21 2014 Kevin Fenzi <kevin@scrye.com> 1.6.3-6
- Add patch for glib2 open with ordering. Fixes bug #1175867

* Tue Nov 11 2014 Kevin Fenzi <kevin@scrye.com> 1.6.3-5
- Add appdata. Fixes bug #1161931

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 05 2013 Kevin Fenzi <kevin@scrye.com> 1.6.3-1
- Update to 1.6.3

* Fri Feb 22 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.2-3
- Remove --vendor from desktop-file-install https://fedorahosted.org/fesco/ticket/1077

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Kevin Fenzi <kevin@scrye.com> 1.6.2-1
- Update to 1.6.2
- Clean up changelog

* Sun Dec 09 2012 Kevin Fenzi <kevin@scrye.com> 1.6.1-1
- Update to 1.6.1

* Tue Dec 04 2012 Kevin Fenzi <kevin@scrye.com> 1.6.0-1
- Update to 1.6.0. 
- See http://git.xfce.org/xfce/thunar/tree/NEWS?id=781395f339e13f4da7c69ac63caefeec451b6dea

* Sat Oct 13 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.0-3
- Show 'Send to' menu entries based on filetypes
- Add blueman-sendto to the 'Sent to' menu

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 1.4.0 (Xfce 4.10 final)
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 1.3.2-1
- Update to 1.3.2 (Xfce 4.10pre2)

* Mon Apr 02 2012 Kevin Fenzi <kevin@scrye.com> - 1.3.1-1
- Update to 1.3.1

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.3.0-7
- Rebuild against PCRE 8.30

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-5
- Own %%{_libdir}/Thunar/

* Thu Apr 21 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-4
- Fix format string flaw CVE-2011-1588 (#698290)

* Tue Mar 15 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-3
- Add missing BRs: libexif-devel, libICE-devel and libnotify-devel

* Tue Mar 08 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-2
- Obsolete old plugins (#682491)
- Add sendto helper for quodlibet

* Mon Feb 14 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Kevin Fenzi <kevin@tummy.com> - 1.2.1-1
- Update to 1.2.1

* Sat Jan 22 2011 Kevin Fenzi <kevin@tummy.com> - 1.2.0-2
- Add hack for upgrades (works around bug #670210)

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 1.2.0-1
- Update to 1.2.0

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.6-1
- Update to 1.1.6

* Sun Dec 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4
- Drop obsolete build requirements: GConf2-devel, fam-devel, hal-devel, 
  libjpeg-devel, libxslt-devel.
- Remove old patches

* Mon Nov 01 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.2-4
- Add patch for trash icon. (#647734)

* Sat Oct 16 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.2-3
- Add patch for Drag and drop issue. (#633171)

* Thu Jun 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.2-2
- Fix conditional requirement for hal-storage-addon

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.2-1
- Update to 1.0.2

* Fri Apr 30 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.1-7
- Require hal-storage-addon
- Remove obsolete mime types (#587256)
- Update icon-cache scriptlets

* Thu Apr 15 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.1-6
- Bump release

* Thu Apr 15 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.1-5
- Add patch to fix directory umask issue. Fixes bug #579087

* Sat Feb 13 2010 Kevin Fenzi <kevin@tummy.com> - 1.0.1-4
- Add patch for DSO linking. Fixes bug #564714

* Thu Sep 10 2009 Kevin Fenzi <kevin@tummy.com> - 1.0.1-3
- Require dbus-x11 (#505499)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 1.0.1-1
- Update to 1.0.1

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 1.0.0-1
- Update to 1.0.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 0.9.99.1-1
- Update to 0.9.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 0.9.93-1
- Update to 0.9.93

* Fri Dec 26 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.92-1
- Update to 0.9.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3
- Respect xdg user directory paths (#457740)
- Don't spawn zombies (bugzilla.xfce.org #2983)
- Add additional sendto helpers for bluethooth and audaciuos (#450784)

* Sat Feb 23 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.0-4
- Remove requires on xfce-icon-theme. See bug 433152

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 0.9.0-3
- Rebuild for gcc43

* Mon Dec  3 2007 Kevin Fenzi <kevin@tummy.com> - 0.9.0-2
- Add thunar-vfs patch. 

* Sun Dec  2 2007 Kevin Fenzi <kevin@tummy.com> - 0.9.0-1
- Update to 0.9.0

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 0.8.0-3
- Update License tag

* Mon Jul  9 2007 Kevin Fenzi <kevin@tummy.com> - 0.8.0-2
- Add provides for lowercase name

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 0.8.0-1
- Upgrade to 0.8.0

* Mon Dec 18 2006 Kevin Fenzi <kevin@tummy.com> - 0.5.0-0.3.rc2
- Own the thunarx-1 directory

* Sat Nov 11 2006 Kevin Fenzi <kevin@tummy.com> - 0.5.0-0.2.rc2
- Increase exo version 

* Thu Nov 09 2006 Kevin Fenzi <kevin@tummy.com> - 0.5.0-0.1.rc2
- Upgrade to 0.5.0rc2

* Mon Oct 09 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.11.rc1
- Add shared-mime-info and xfce4-icon-theme as Requires (fixes #209592)

* Fri Oct 06 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.10.rc1
- Tweak Obsoletes versions

* Fri Oct 06 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.9.rc1
- Obsolete xffm for now. 

* Thu Oct 05 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.8.rc1
- Really re-enable the trash plugin. 

* Thu Oct 05 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.7.rc1
- Re-enable trash plugin in Xfce 4.4rc1

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 0.4.0-0.6.rc1
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.5.rc1
- Remove duplicate thunar-sendto-email.desktop entry from files. 

* Fri Sep 15 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.4.rc1
- Added Requires: exo-devel >= 0.3.1.10 to devel. 
- exclude docs moved from datadir to docs
- Fixed datdir including files twice

* Thu Sep 14 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.3.rc1
- Cleaned up BuildRequires some more
- Disabled tpa plugin and desktop for now
- Moved some files from doc/Thunar to be %%doc
- Changed man to use wildcard in files
- Added examples to devel subpackage
- Made sure some examples are not executable. 

* Tue Sep 12 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.2.rc1
- Added some BuildRequires
- Added --with-gtkdoc and gtkdoc files to devel

* Wed Sep  6 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.1.rc1
- Inital package for fedora extras

