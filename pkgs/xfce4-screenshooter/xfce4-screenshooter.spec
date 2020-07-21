# Review at https://bugzilla.redhat.com/show_bug.cgi?id=478659
# Successor of the xfce4-screenshooter-plugin, which was reviewed at
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=179202

%global minorversion 1.9
%global xfceversion 4.14

Name:           xfce4-screenshooter
Version:        1.9.7
Release:        1%{?dist}
Summary:        Screenshot utility for the Xfce desktop

License:        GPLv2+
URL:            http://goodies.xfce.org/projects/applications/%{name}
Source0:        http://archive.xfce.org/src/apps/%{name}/%{minorversion}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires:  exo-devel
BuildRequires:  libxfce4ui-devel >= %{xfceversion}
BuildRequires:  xfce4-panel-devel >= %{xfceversion}
BuildRequires:  libsoup-devel >= 2.26.0
BuildRequires:  libXext-devel >= 1.0.0
BuildRequires:  libXfixes-devel >= 4.0.0
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
The Xfce Screenshooter utility allows you to capture the entire screen, the 
active window or a selected region. You can set the delay that elapses before 
the screenshot is taken and the action that will be done with the screenshot: 
save it to a PNG file, copy it to the clipboard, or open it using another 
application.

%package        plugin
Summary:        Screenshot utility for the Xfce panel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xfce4-panel >= %{xfceversion}

%description    plugin
The Xfce Screenshooter plugin allows you to take screenshots from the Xfce 
panel.


%prep
%autosetup

# KDE and GNOME have their own screenshot utils
echo "NotShowIn=KDE;GNOME;" >> src/xfce4-screenshooter.desktop.in.in

%build
%configure --disable-static
%make_build


%install
%make_install

# remove la file
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# make sure debuginfo is generated properly
chmod -c +x %{buildroot}%{_libdir}/xfce4/panel/plugins/*.so

%find_lang %{name}

desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        --delete-original \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/*.appdata.xml

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/applets-screenshooter.png
%{_datadir}/icons/hicolor/scalable/apps/applets-screenshooter.svg
%{_datadir}/metainfo/xfce4-screenshooter.appdata.xml
%{_mandir}/man1/*.1.*


%files plugin
%{_libdir}/xfce4/panel/plugins/*.so
%{_datadir}/xfce4/panel/plugins/*.desktop


%changelog
* Sun Nov 03 2019 Kevin Fenzi <kevin@scrye.com> - 1.9.7-1
- Update to 1.9.7

* Sun Aug 25 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.6-1
- Update to 1.9.6

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 31 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.5-1
- Update to 1.9.5

* Sat Mar 09 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.4-1
- Update to 1.9.4

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Aug 11 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.3-20
- Rebuild for xfce version 4.13

* Sat Aug 11 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat May 05 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2

* Wed Mar 28 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1

* Thu Feb 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.8.2-11
- Spec cleanup / modernization

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 05 2015 Kevin Fenzi <kevin@scrye.com> 1.8.2-4
- Rebuild again for Xfce 4.12

* Sat Feb 28 2015 Kevin Fenzi <kevin@scrye.com> 1.8.2-3
- Rebuild for Xfce 4.12

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.8.2-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Jan 25 2015 Kevin Fenzi <kevin@scrye.com> 1.8.2-1
- Update to 1.8.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.8.1-4
- Fix FTBFS with automake-1.14 (#1107271)
- Cleanup spec

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 19 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1 (fixes #895968)
- Upstream build fixes: Build plugin as module, no versioned libs,
  only export needed symbols
- Add aarch64 support (#926787)
- Increase transparency of selection background (bugzilla.xfce.org #9592)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 15 2012 Kevin Fenzi <kevin@scrye.com> - 1.8.0-6
- Rebuild for Xfce 4.10(pre2)

* Fri Apr 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.8.0-5
- Update manpage (#809491)

* Thu Apr 05 2012 Kevin Fenzi <kevin@scrye.com> - 1.8.0-4
- Rebuild for Xfce 4.10

* Tue Feb 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.8.0-3
- Bring back the dsofix patch
- Rebuild for new libpng

* Wed Aug 03 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.8.0-2
- Drop dsofix patch, no longer needed

* Mon Aug 01 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0
- No longer require xfce4-doc but own %%{_datadir}/xfce4/doc/ (#721291)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.9-3
- Rebuild for xfce4-panel 4.7

* Tue May 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.9-2
- Add patch to fix DSO linking (#564819)

* Sun Feb 07 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9 (RC for 1.8.0)
- Include NEWS and TODO

* Thu Jul 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Wed Feb 25 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1
- Built for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0 on Xfce 4.5.93.

* Fri Jan 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.90.0-1
- Update to 1.4.90.0
- Split package into standalone app and panel plugin

* Thu Nov 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Wed Aug 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Wed Aug 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Fri Jul 18 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Jul 16 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Thu Jul 03 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
- Include new xfce4-screenshooter manpage

* Sat Jun 21 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0
- BR gettext

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-7
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-6
- Change license tag to GPLv2+

* Sat Apr 28 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-5
- Rebuild for Xfce 4.4.1

* Sun Jan 28 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-4
- Rebuild for XFCE 4.4.

* Thu Oct 05 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-3
- Bump release for devel checkin.

* Wed Sep 13 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-2
- Rebuild for XFCE 4.3.99.1.
- BR perl(XML::Parser).

* Mon Sep 04 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 on XFCE 4.3.90.2.

* Mon Sep 04 2006 Christoph Wickert <cwickert@fedoraproject.org> - 0.0.8-4
- Mass rebuild for Fedora Core 6.

* Tue Apr 11 2006 Christoph Wickert <fedora.wickert@arcor.de> - 0.0.8-3
- Require xfce4-panel.

* Thu Feb 16 2006 Christoph Wickert <fedora.wickert@arcor.de> - 0.0.8-2
- Rebuild for Fedora Extras 5.

* Sat Jan 21 2006 Christoph Wickert <fedora.wickert@arcor.de> - 0.0.8-1
- Initial Fedora Extras version.
