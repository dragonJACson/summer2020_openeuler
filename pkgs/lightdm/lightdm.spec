# FIXME: most tests currently fail
%bcond_with tests

%global glib2_version	%(pkg-config --modversion glib-2.0 2>/dev/null || echo "2.44")
%global giturl		https://github.com/CanonicalLtd/lightdm

Name:		lightdm
Summary:	A cross-desktop Display Manager
Version:	1.30.0
Release:	7

# library/bindings are LGPLv2 or LGPLv3, the rest GPLv3+
License:	(LGPLv2 or LGPLv3) and GPLv3+
URL:		https://www.freedesktop.org/wiki/Software/LightDM/
Source0:	%{giturl}/archive/%{version}/lightdm-%{version}.tar.gz

Source10:	lightdm.pam
Source11:	lightdm-autologin.pam
Source12:	lightdm-tmpfiles.conf
Source13:	lightdm.service
Source14:	lightdm.logrotate
Source15:	lightdm.rules


# .conf snippets
Source20:	50-backup-logs.conf
Source21:	50-minimum-vt.conf
Source22:	50-session-wrapper.conf
Source23:	50-user-authority-in-system-dir.conf
Source24:	50-xserver-command.conf
Source25:	50-disable-guest.conf
Source26:	50-remove-wayland-session.conf
Source27:	50-run-directory.conf

# X session wrapper
Source30:	Xsession

# Upstreamed:
Patch0:		%{giturl}/pull/5.patch#/lightdm-1.25.1-disable_dmrc.patch

# Upstream commits

BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gtk-doc itstool
BuildRequires:	intltool
BuildRequires:	libgcrypt-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(audit)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0) >= 2.26
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-export-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(Qt5Core) pkgconfig(Qt5DBus) pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	systemd
BuildRequires:	vala

Requires:	%{name}-gobject%{?_isa} = %{version}-%{release}
Requires:	accountsservice
Requires:	dbus-x11
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:	polkit-js-engine
%endif
Requires:	systemd
Requires:	xorg-x11-xinit

#Requires:   (lightdm-greeter = 1.2 if xorg-x11-server-Xorg)

%{?systemd_requires}

Requires(pre):	shadow-utils
Requires(post):	psmisc

# needed for anaconda to boot into runlevel 5 after install
Provides:	service(graphical-login) = lightdm

%description
Lightdm is a display manager that:
* Is cross-desktop - supports different desktops
* Supports different display technologies
* Is lightweight - low memory usage and fast performance


%package gobject
Summary:	LightDM GObject client library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	glib2%{?_isa} >= %{glib2_version}
%description gobject
This package contains a GObject based library for LightDM clients to use to
interface with LightDM.


%package gobject-devel
Summary:	Development files for %{name}-gobject
Requires:	%{name}-gobject%{?_isa} = %{version}-%{release}
%description gobject-devel
%{summary}.

%if 0%{?_with_qt4}
%package qt
Summary: LightDM Qt4 client library
Requires:	%{name}%{?_isa} = %{version}-%{release}
%{?_qt4_version:Requires:	qt4%{?_isa} >= %{_qt4_version}}
%description qt
This package contains a Qt4-based library for LightDM clients to use to interface
with LightDM.

%package qt-devel
Summary:	Development files for %{name}-qt
Requires:	%{name}-qt%{?_isa} = %{version}-%{release}
%description qt-devel
%{summary}.
%endif

%package qt5
Summary:	LightDM Qt5 client library
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description qt5
This package contains a Qt5-based library for LightDM clients to use to interface
with LightDM.


%package qt5-devel
Summary:	Development files for %{name}-qt5
Requires:	%{name}-qt5%{?_isa} = %{version}-%{release}
%description qt5-devel
%{summary}.


%prep
%autosetup -p 1


%build
# Make libtoolize happy.
%{__cat} %{_datadir}/aclocal/intltool.m4 > aclocal.m4
# Bootstrap
NOCONFIGURE=1 ./autogen.sh

%configure					\
	--disable-dmrc				\
	--disable-silent-rules			\
	--disable-static			\
	--enable-gtk-doc			\
	--enable-libaudit			\
	%{?_with_qt4:--enable-liblightdm-qt}			\
	--enable-liblightdm-qt5			\
	--enable-introspection			\
%if %{with tests}
	--enable-tests				\
%else
	--disable-tests				\
%endif
	--enable-vala				\
	--with-greeter-user=lightdm		\
	--with-greeter-session=lightdm-greeter

%make_build


%install
%make_install

# We need to own these
%{__mkdir_p} %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/		\
		%{buildroot}%{_datadir}/dbus-1/interfaces		\
		%{buildroot}%{_datadir}/dbus-1/system.d			\
		%{buildroot}%{_datadir}/lightdm/lightdm.conf.d/		\
		%{buildroot}%{_datadir}/lightdm/remote-sessions/	\
		%{buildroot}%{_datadir}/xgreeters/			\
		%{buildroot}%{_localstatedir}/cache/lightdm/		\
		%{buildroot}%{_rundir}/lightdm/		\
		%{buildroot}%{_localstatedir}/log/lightdm/		\
		%{buildroot}%{_localstatedir}/lib/lightdm/		\
		%{buildroot}%{_localstatedir}/lib/lightdm-data/

# libtool cruft
rm -fv %{buildroot}%{_libdir}/lib*.la

# We don't ship AppAmor
%{__rm} -rfv %{buildroot}%{_sysconfdir}/apparmor.d/

# omit upstart support
%{__rm} -rfv %{buildroot}%{_sysconfdir}/init

# install pam file
%{__install} -Dpm 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/lightdm
%{__install} -Dpm 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/lightdm-autologin
%{__install} -Dpm 0644 %{SOURCE12} %{buildroot}%{_prefix}/lib/tmpfiles.d/lightdm.conf
%{__install} -Dpm 0644 %{SOURCE13} %{buildroot}%{_unitdir}/lightdm.service
%{__install} -Dpm 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/logrotate.d/lightdm
%{__install} -Dpm 0644 %{SOURCE15} %{buildroot}%{_datadir}/polkit-1/rules.d/lightdm.rules
%{__install} -pm 0644 %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}	\
	%{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27} %{buildroot}%{_datadir}/lightdm/lightdm.conf.d/

# Install Xsession file
%{__install} -pm 0755 %{SOURCE30} %{buildroot}%{_sysconfdir}/lightdm/Xsession

# Move DBus config to proper location.
# why is this needed? -- rex
%{__mv} -f %{buildroot}%{_sysconfdir}/dbus-1/system.d/*.conf		\
	%{buildroot}%{_datadir}/dbus-1/system.d

%find_lang lightdm --with-gnome


%if %{with tests}
%check
%make_build check ||:
%endif


%pre
%{_bindir}/getent group lightdm >/dev/null || %{_sbindir}/groupadd -r lightdm
%{_bindir}/getent passwd lightdm >/dev/null || %{_sbindir}/useradd -g lightdm \
	-M -d /var/lib/lightdm -s /sbin/nologin -r lightdm
exit 0

%post
# todo: document need/purpose for this snippet
if [ $1 = 1 ] ; then
	%{_bindir}/killall -HUP dbus-daemon 2>&1 > /dev/null
fi
%{?systemd_post:%systemd_post lightdm.service}

%preun
%{?systemd_preun:%systemd_preun lightdm.service}

%postun
%{?systemd_postun}

%files -f lightdm.lang
%license COPYING.GPL3
%doc NEWS
%dir %{_sysconfdir}/lightdm/
%dir %{_sysconfdir}/lightdm/lightdm.conf.d
%{_sysconfdir}/lightdm/Xsession
%config(noreplace) %{_sysconfdir}/pam.d/lightdm*
%config(noreplace) %{_sysconfdir}/lightdm/keys.conf
%config(noreplace) %{_sysconfdir}/lightdm/lightdm.conf
%config(noreplace) %{_sysconfdir}/lightdm/users.conf
%dir %{_sysconfdir}/logrotate.d/
%{_sysconfdir}/logrotate.d/lightdm
%dir %attr(-,lightdm,lightdm) %{_localstatedir}/cache/lightdm/
%dir %attr(-,lightdm,lightdm) %{_localstatedir}/lib/lightdm/
%dir %attr(-,lightdm,lightdm) %{_localstatedir}/lib/lightdm-data/
%dir %attr(-,lightdm,lightdm) %{_localstatedir}/log/lightdm/
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%dir %{_datadir}/xgreeters/
%ghost %dir %{_rundir}/lightdm
%{_bindir}/dm-tool
%{_sbindir}/lightdm
%{_libexecdir}/lightdm-guest-session
%{_datadir}/lightdm/
%{_libdir}/girepository-1.0/LightDM-1.typelib
%{_mandir}/man1/dm-tool.1*
%{_mandir}/man1/lightdm*
%{_unitdir}/lightdm.service
%{_datadir}/accountsservice
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/polkit-1/rules.d/lightdm.rules
%{_datadir}/polkit-1/actions/org.freedesktop.DisplayManager.AccountsService.policy
%{_datadir}/bash-completion/completions/dm-tool
%{_datadir}/bash-completion/completions/lightdm
%{_prefix}/lib/tmpfiles.d/lightdm.conf

%ldconfig_scriptlets gobject

%files gobject
%license COPYING.LGPL2 COPYING.LGPL3
%{_libdir}/liblightdm-gobject-1.so.0*

%files gobject-devel
%doc %{_datadir}/gtk-doc/html/lightdm-gobject-1/
%{_includedir}/lightdm-gobject-1/
%{_libdir}/liblightdm-gobject-1.so
%{_libdir}/pkgconfig/liblightdm-gobject-1.pc
%{_datadir}/gir-1.0/LightDM-1.gir
%{_datadir}/vala/vapi/liblightdm-gobject-1.*

%if 0%{?_with_qt4}
%ldconfig_scriptlets qt

%files qt
%license COPYING.LGPL2 COPYING.LGPL3
%{_libdir}/liblightdm-qt-3.so.0*

%files qt-devel
%{_includedir}/lightdm-qt-3/
%{_libdir}/liblightdm-qt-3.so
%{_libdir}/pkgconfig/liblightdm-qt-3.pc
%endif

%ldconfig_scriptlets qt5

%files qt5
%license COPYING.LGPL2 COPYING.LGPL3
%{_libdir}/liblightdm-qt5-3.so.0*

%files qt5-devel
%{_includedir}/lightdm-qt5-3/
%{_libdir}/liblightdm-qt5-3.so
%{_libdir}/pkgconfig/liblightdm-qt5-3.pc


%changelog
* Tue Aug 04 2020 Luke Yue <lukedyue@gmail.com> - 1.30.0-7
- Add Xsession Wrapper for lightdm

* Thu Jul 09 2020 douyan <douyan@kylinos.cn> - 1.30.0-6
- Package init for openEuler
