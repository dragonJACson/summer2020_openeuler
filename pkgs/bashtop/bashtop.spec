Name:           bashtop
Version:        0.9.24
Release:        1%{?dist}
Summary:        Linux resource monitor

License:        ASL 2.0
URL:            https://github.com/aristocratos/bashtop
Source0:        %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz
Patch0:         dontcheckupdates.patch

Requires: bash >= 4.4
Requires: gawk
Requires: coreutils
Requires: grep
Requires: procps-ng
Requires: sed
Requires: python3-psutil

Recommends: lm-sensors
Recommends: curl
Recommends: sysstat

BuildArch: noarch

%description
Resource monitor written in Bash that shows usage and stats for processor, 
memory, disks, network and processes.

%prep
%autosetup

%build
# None required

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}/themes
install -p -m 755 bashtop %{buildroot}%{_bindir}
install -p -m 644 themes/* %{buildroot}%{_datadir}/%{name}/themes

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Thu Jul 16 2020 Germano Massullo <germano.massullo@gmail.com> - 0.9.24-1
- 0.9.24 release

* Sun Jul 05 2020 Germano Massullo <germano.massullo@gmail.com> - 0.9.19-3
- Added Requires: python3-psutil

* Wed Jul 01 2020 Alessio <alciregi@fedoraproject.org> - 0.9.19-1
- 0.9.19 release

* Wed Jun 17 2020 Alessio <alciregi@fedoraproject.org> - 0.9.11-1
- 0.9.11 release

* Mon Jun 01 2020 Alessio <alciregi@fedoraproject.org> - 0.9.7-1
- 0.9.7 release

* Mon May 25 2020 Alessio <alciregi@fedoraproject.org> - 0.9.3-1
- 0.9.3 release

* Wed May 13 2020 Alessio <alciregi@fedoraproject.org> - 0.8.30-1
- 0.8.30 release
- Disable updates check

* Sat May 09 2020 Alessio <alciregi@fedoraproject.org> - 0.8.27-2
- 0.8.27 release

* Sun May 03 2020 Germano Massullo <germano.massullo@gmail.com> - 0.8.22-1
- 0.8.22 release

* Sat May 02 2020 Alessio <alciregi@fedoraproject.org> - 0.8.20-2
- Revert to unnoticed comaintainer changes

* Sat May 02 2020 Alessio <alciregi@fedoraproject.org> - 0.8.20-1
- Update to 0.8.20

* Fri May 01 2020 Germano Massullo <germano.massullo@gmail.com> - 0.8.19-1
- 0.8.19 release
- Added Recommends: sysstat

* Fri May 01 2020 Germano Massullo <germano.massullo@gmail.com> - 0.8.18-2
- Added bash minimum version requirement
- Removed EPEL7 macros since Bash 4.4 is not available, so the package cannot work on this branch

* Fri May 01 2020 Germano Massullo <germano.massullo@gmail.com> - 0.8.18-1
- 0.8.18 release

* Fri May 01 2020 Germano Massullo <germano.massullo@gmail.com> - 0.8.17-2
- Disabled weak dependencies on EPEL7, since Recommends is not supported

* Thu Apr 30 2020 Alessio <alciregi@fedoraproject.org> - 0.8.17-1
- Update to 0.8.17

* Wed Apr 29 2020 Alessio <alciregi@fedoraproject.org> - 0.8.16-1
- Initial package

