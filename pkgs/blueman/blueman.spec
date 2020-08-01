Name:		blueman
Summary:	GTK+ Bluetooth Manager
License:	GPLv2+

Epoch:		1
Version:	2.1.3
Release:	1%{?dist}

URL:		https://github.com/blueman-project/blueman
Source0:	%{URL}/releases/download/%{version}/blueman-%{version}.tar.gz

BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(python3)
BuildRequires:	desktop-file-utils
BuildRequires:	intltool >= 0.35.0
BuildRequires:  iproute
BuildRequires:	python3-Cython >= 0.21
BuildRequires:  python3-dbus
BuildRequires:	systemd

%{?systemd_requires}
Requires:	python3-gobject-base
Requires:	bluez
Requires:	bluez-obexd
Requires:       dconf
Requires:	dbus
Requires:       iproute
Requires:	python3-dbus
Requires:	pulseaudio-libs-glib2
Requires:	pulseaudio-module-bluetooth

Provides:	dbus-bluez-pin-helper
Obsoletes:	blueman-nautilus

%description
Blueman is a tool to use Bluetooth devices. It is designed to provide simple,
yet effective means for controlling BlueZ API and simplifying bluetooth tasks
such as:
- Connecting to 3G/EDGE/GPRS via dial-up
- Connecting to/Creating bluetooth networks
- Connecting to input devices
- Connecting to audio devices
- Sending/Receiving files via OBEX
- Pairing


%prep
%setup -q
sed -e 's|/usr/sbin/bluetoothd|%{_libexecdir}/bluetooth/bluetoothd|g' -i apps/blueman-report.in

%build
export PYTHON=%{_bindir}/python3

# Override the "_configure" macro - the name of the script
# in this repo is ./autogen.sh, not ./configure
%global _configure ./autogen.sh
%configure --disable-static \
           --enable-thunar-sendto=no \
           --disable-schemas-compile \
           --disable-appindicator
make %{?_smp_mflags}


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm -rf %{buildroot}%{_datadir}/doc/blueman/

%find_lang blueman

# we need to own this, not only because of SELinux
mkdir -p %{buildroot}%{_sharedstatedir}/blueman
touch %{buildroot}%{_sharedstatedir}/blueman/network.state


%check
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/blueman.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/blueman-*.desktop


%post
%systemd_post blueman-mechanism.service
%systemd_user_post blueman-applet.service

%postun
%systemd_postun_with_restart blueman-mechanism.service

%preun
%systemd_preun blueman-mechanism.service
%systemd_user_preun blueman-applet.service


%files -f blueman.lang
%doc CHANGELOG.md FAQ README.md
%license COPYING
%{_bindir}/*
%{python3_sitelib}/blueman/
%{python3_sitearch}/*.so
%{_libexecdir}/blueman-*
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.blueman.Mechanism.conf
%{_sysconfdir}/xdg/autostart/blueman.desktop
%{_datadir}/applications/blueman-*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/blueman/
%{_datadir}/blueman/
%{_datadir}/dbus-1/services/org.blueman.Applet.service
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/polkit-1/actions/org.blueman.policy
%{_datadir}/polkit-1/rules.d/blueman.rules
%{_mandir}/man1/*
%{_unitdir}/blueman-mechanism.service
%{_userunitdir}/blueman-applet.service
%dir %{_sharedstatedir}/blueman
%ghost %attr(0644,root,root) %{_sharedstatedir}/blueman/network.state


%changelog
* Fri May 08 2020 Artur Iwicki <fedora@svgames.pl> - 1:2.1.3-1
- Update to latest upstream release (2.1.3)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Artur Iwicki <fedora@svgames.pl> - 1:2.1.2-1
- Update to latest upstream release (2.1.2)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.1.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.1.1-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Artur Iwicki <fedora@svgames.pl> - 1:2.1.1-1
- Update to latest upstream release (2.1.1)

* Mon Jun 10 2019 Artur Iwicki <fedora@svgames.pl> - 1:2.1-1
- Update to latest upstream release (2.1)
- Drop Patch0 and Patch1 (they were backports from today's release)

* Sat Jun 08 2019 Artur Iwicki <fedora@svgames.pl> - 1:2.1-0.17.beta1
- Add two upstream patches for crashes and IO issues

* Mon May 06 2019 Artur Iwicki <fedora@svgames.pl> - 1:2.1-0.16.beta1
- Upgrade to new upstream pre-release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-0.15.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 27 2018 Artur Iwicki <fedora@svgames.pl> - 1:2.1-0.14.alpha3
- Upgrade to new upstream pre-release
- Remove the Group: tag (no longer used in Fedora)

* Tue Sep 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.1-0.13.alpha2
- pygobject3 → python3-gobject-base

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-0.12.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:2.1-0.11.alpha2
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-0.10.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.1-0.9.alpha2
- Remove obsolete scriptlets

* Mon Dec 11 2017 Pete Walter <pwalter@fedoraproject.org> - 1:2.1-0.8.alpha2
- Update to 2.1 alpha2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-0.7.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-0.6.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-0.5.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1:2.1-0.4.alpha1
- Rebuild for Python 3.6

* Wed Sep 21 2016 Peter Walter <pwalter@fedoraproject.org> - 1:2.1-0.3.alpha1
- Fix obexd dependencies (#1377640)

* Tue Sep 20 2016 Peter Walter <pwalter@fedoraproject.org> - 1:2.1-0.2.alpha1
- Enable polkit support
- Validate desktop files

* Mon Sep 19 2016 Peter Walter <pwalter@fedoraproject.org> - 1:2.1-0.1.alpha1
- Update to 2.1 alpha1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed May 18 2016 Leigh Scott <leigh123linux@googlemail.com> - 1:2.0.4-2
- patch to try and fix some of the dbus exceptions

* Sun Apr 03 2016 Leigh Scott <leigh123linux@googlemail.com> - 1:2.0.4-1
- update to 2.0.4 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.8.gita0408c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.7.gita0408c1
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.1-0.6.gita0408c1
- update to latest git

* Fri Oct 30 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.1-0.5.git608efb8
- update to latest git

* Fri Sep 18 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.1-0.4.git2a812a8
- update to latest git

* Wed Sep 16 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.1-0.3.git7a2e20e
- build against python3

* Mon Aug 24 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.1-0.2.git7a2e20e
- update to latest git

* Wed Aug 12 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.1-0.1.git0a5defd
- update to git

* Mon Jul 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-11
- add requires dconf (bz 1246995)

* Mon Jul 13 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-10
- remove requires desktop-notification-daemon and PolicyKit-authentication-agent
- patch for gi and pyobject changes

* Mon Jun 22 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-9
- add upstream fix for bz 1233237

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-7
- remove appindicator support

* Fri Jun 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-6
- add requires bluez (bz 1228488)

* Thu May 28 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-5
- add requires pulseaudio-libs-glib2

* Thu May 28 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-4
- remove browse feature (upstream patch)
- ammend description
- rename service file (upstream patch)
- clean up requires and buildrequires
- update scriptlets
- clean up spec file

* Wed May 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-3
- add requires dbus-python
- add requires pulseaudio-module-bluetooth for audio

* Wed May 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-2
- fix bluetoothd path for report tool

* Tue May 26 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.0-1
- update to 2.0 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-5
- Require pulseaudio-libs-glib2 (#856270)

* Sat Oct 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-4
- No longer require gnome-session
- Require gvfs-obexftp, needed when launching file managers from blueman

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-2
- Own /var/lib/blueman and /var/lib/blueman/network.state (#818528)

* Thu Apr 26 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-1
- Update to 1.23
- Drop upstreamed PulseAudio patch
- Fix statusicon
- Autostart blueman not only in GNOME but also in Xfce and LXDE
- Enhance description

