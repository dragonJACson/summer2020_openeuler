%global project_name FcitxQt5

Name:           fcitx-qt5
Version:        1.2.4
Release:        4%{?dist}
Summary:        Fcitx IM module for Qt5

# The entire source code is GPLv2+ except
# platforminputcontext/ which is BSD
License:        GPLv2+ and BSD
URL:            https://github.com/fcitx/fcitx-qt5
Source0:        http://download.fcitx-im.org/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  fcitx-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext-devel
# The author requests that fcitx-qt5 should be rebuilt for each minor version
# of qt5. qt5-qtbase-private-devel is not actually required for build, but
# left for Qt maintainer to tract this case.
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
%filter_provides_in %{_qt5_plugindir}/platforminputcontexts/libfcitxplatforminputcontextplugin.so
%filter_provides_in %{_libdir}/fcitx/qt/libfcitx-quickphrase-editor5.so
%filter_setup

%description
This package provides Fcitx Qt5 input context.

%package devel
Summary:        Development files for fcitx-qt5
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake

%description devel
The %{name}-devel package contains libraries and header files necessary for
developing programs using fcitx-qt5 libraries.

%prep
%setup -q

%build
mkdir -pv build
pushd build
%cmake ..
popd
make %{?_smp_mflags} -C build

%install
make install/fast DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" -C build
%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc README
%license COPYING COPYING.BSD
%{_libdir}/fcitx/libexec/%{name}-gui-wrapper
%{_libdir}/lib%{project_name}*.so.*
%{_libdir}/fcitx/qt/
%{_qt5_plugindir}/platforminputcontexts/libfcitxplatforminputcontextplugin.so

%files devel
%{_includedir}/%{project_name}
%{_libdir}/lib%{project_name}*.so
%{_libdir}/cmake/*


%changelog
* Mon Apr 06 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.2.4-4
- rebuild (qt5)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 1.2.4-2
- rebuild (qt5)

* Sun Dec  1 2019 Robin Lee <cheeselee@fedoraproject.org> - 1.2.4-1
- Release 1.2.4

* Wed Sep 25 2019 Jan Grulich <jgrulich@redhat.com> - 1.2.3-10
- rebuild (qt5)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Jan Grulich <jgrulich@redhat.com> - 1.2.3-8
- rebuild (qt5)

* Wed Jun 05 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.2.3-7
- rebuild (qt5)

* Sun Mar 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.2.3-6
- rebuild (qt5)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.2.3-4
- rebuild (qt5)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.2.3-2
- rebuild (qt5)

* Wed Jun  6 2018 Robin Lee <cheeselee@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3 (#1584926)

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.2.2-5
- rebuild (qt5)

* Mon Feb 19 2018 Robin Lee <cheeselee@fedoraproject.org> - 1.2.2-4
- rebuild (qt5)

* Wed Feb 14 2018 Robin Lee <cheeselee@fedoraproject.org> - 1.2.2-3
- BR: qt5-qtbase-private-devel

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2 (#1539217)

* Wed Dec 20 2017 Jan Grulich <jgrulich@redhat.com> - 1.2.1-2
- rebuild (qt5)

* Wed Dec 13 2017 Robin Lee <cheeselee@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1 (BZ#1511238)
- License changed to GPLv2+ and BSD

* Sun Nov 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-3
- rebuild (qt5)

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-2
- rebuild (qt5)

* Sun Sep 24 2017 Robin Lee <cheeselee@fedoraproject> - 1.1.1-1
- Update to 1.1.1 (BZ#1492079)

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.1.0-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-3
-  rebuild (qt5)

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.0-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri May 12 2017 Robin Lee <cheeselee@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Wed May 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.0.6-5
- rebuild (qt5)

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.0.6-4
- rebuild (qt5)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.6-2
- bump Release

* Thu Nov 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.6-1.2
- f24 branch rebuild (qt5)

* Fri Oct 21 2016 Robin Lee <cheeselee@fedoraproject.org> - 1.0.6-1
- Upate to 1.0.6 (BZ#1384262)

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-7
- use macro version of qt5 dep

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-6
- rebuild (qtbase)

* Thu Jun 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-5
- rebuild (qtbase)

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-4
- BR: qt5-qtbase-private-devel

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-3
- rebuild (Qt5)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Robin Lee <cheeselee@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Mon Dec 07 2015 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-4
- rebuild (qt5)

* Fri Oct 09 2015 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-3
- rebuild(qt5), tighten qt5 dep, .spec cosmetics

* Wed Sep 23 2015 Robin Lee <cheeselee@fedoraproject.org> - 1.0.4-2
- Requires a versioned qt5-qtbase

* Tue Sep 22 2015 Robin Lee <cheeselee@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun  1 2015 Robin Lee <cheeselee@fedoraproject.org> - 1.0.2-2
- Don't explicitly require fcitx

* Thu Apr 30 2015 Robin Lee <cheeselee@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- License tag revised
- BR: libxkbcommon-devel

* Thu Apr 16 2015 Robin Lee <cheeselee@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Fri Dec 12 2014 Robin Lee <cheeselee@fedoraproject.org> - 0.1.3-1
- Initial package
