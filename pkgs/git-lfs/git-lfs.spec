%bcond_without check

# https://github.com/git-lfs/git-lfs
%global goipath         github.com/git-lfs/git-lfs
Version:                2.11.0

%gometa

%global common_description %{expand:
Git extension for versioning large files.}

%global golicenses      LICENSE.md
%global godocs          docs CHANGELOG.md CODE-OF-CONDUCT.md\\\
                        CONTRIBUTING.md README.md

Name:           git-lfs
Release:        1%{?dist}
Summary:        Git extension for versioning large files

License:        MIT
URL:            https://git-lfs.github.io/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  golang(github.com/dpotapov/go-spnego)
BuildRequires:  golang(github.com/git-lfs/gitobj) >= 1.4.1
BuildRequires:  golang(github.com/git-lfs/gitobj/errors) >= 1.4.1
BuildRequires:  golang(github.com/git-lfs/go-netrc/netrc) >= 0-0.1.20180827gite0e9ca4
BuildRequires:  golang(github.com/git-lfs/go-ntlm/ntlm)
BuildRequires:  golang(github.com/git-lfs/wildmatch) >= 1.0.4
BuildRequires:  golang(github.com/mattn/go-isatty) >= 0.0.4
BuildRequires:  golang(github.com/olekukonko/ts)
BuildRequires:  golang(github.com/pkg/errors)
BuildRequires:  golang(github.com/rubyist/tracerx)
BuildRequires:  golang(github.com/spf13/cobra) >= 0.0.3
BuildRequires:  golang(github.com/ssgelm/cookiejarparser) >= 1.0.1
BuildRequires:  golang(golang.org/x/net/http2)
BuildRequires:  golang(golang.org/x/sync/semaphore)

# Generate man pages
BuildRequires:  /usr/bin/ronn

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert) >= 1.5.1
BuildRequires:  golang(github.com/stretchr/testify/require) >= 1.5.1
BuildRequires:  golang(github.com/xeipuuv/gojsonschema)
BuildRequires:  perl-Digest-SHA
BuildRequires:  perl-Test-Harness
# Tests require full git suite, but not generally needed.
BuildRequires:  git >= 1.8.5
%endif

Requires:       git-core >= 1.8.5

%description
Git Large File Storage (LFS) replaces large files such as audio samples,
videos, datasets, and graphics with text pointers inside Git, while
storing the file contents on a remote server.


%gopkg


%prep
%goprep

# Modify Makefile so that it expects binaries where we build them.
sed -i -e 's!\.\./bin/!/%{gobuilddir}/bin/!g' t/Makefile


%build
# Build manpages first (some embedding in the executable is done.)
pushd docs
ronn --roff man/*.ronn
%gobuild -o %{gobuilddir}/bin/mangen man/mangen.go
%{gobuilddir}/bin/mangen
popd

LDFLAGS="-X 'github.com/git-lfs/git-lfs/config.Vendor=Fedora %{fedora}' " \
%gobuild -o %{gobuilddir}/bin/git-lfs %{goipath}

# Build test executables
for cmd in t/cmd/*.go; do
    %gobuild -o "%{gobuilddir}/bin/$(basename $cmd .go)" "$cmd"
done
%gobuild -o "%{gobuilddir}/bin/git-lfs-test-server-api" t/git-lfs-test-server-api/*.go


%install
%gopkginstall
install -Dpm0755 %{gobuilddir}/bin/git-lfs %{buildroot}%{_bindir}/%{name}
install -d -p %{buildroot}%{_mandir}/man1/
install -Dpm0644 docs/man/*.1 %{buildroot}%{_mandir}/man1/
install -d -p %{buildroot}%{_mandir}/man5/
install -Dpm0644 docs/man/*.5 %{buildroot}%{_mandir}/man5/


%post
%{_bindir}/%{name} install --system --skip-repo

%preun
if [ $1 -eq 0 ]; then
    %{_bindir}/%{name} uninstall --system --skip-repo
fi
exit 0


%if %{with check}
%check
%gocheck
PATH=%{buildroot}%{_bindir}:%{gobuilddir}/bin:$PATH \
    make -C t PROVE_EXTRA_ARGS="-j$(getconf _NPROCESSORS_ONLN)"
%endif


%files
%doc README.md CHANGELOG.md docs
%license LICENSE.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/%{name}*.5*

%gopkgfiles


%changelog
* Sun May 10 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.11.0-1
- Update to latest version

* Thu Feb 20 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.10.0-1
- Update to latest version

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.9.2-1
- Update to latest version

* Wed Jan 01 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.9.0-1
- Update to latest version

* Fri Aug 30 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.8.0-4
- Customize vendor information in version

* Fri Aug 30 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.8.0-3
- Update to latest version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.7.2-2
- Update to latest Go macros

* Wed Apr 24 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.7.2-1
- Update to latest version

* Wed Feb 27 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.7.1-1
- Update to latest version

* Thu Feb 21 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.7.0-1
- Update to latest version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.6.1-1
- Update to latest version

* Mon Jan 14 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.2-4
- Rebuilt for dependencies

* Tue Oct 23 2018 Nicolas Mailhot <nim@fedoraproject.org>
- 2.5.2-3
- redhat-rpm-config-123 triggers bugs in gosetup, remove it from Go spec files as it’s just an alias
- https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/RWD5YATAYAFWKIDZBB7EB6N5DAO4ZKFM/

* Fri Oct 12 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.2-2
- rebuilt

* Wed Oct 10 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.2-1
- Update to latest version

* Tue Sep 04 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.1-1
- Update to latest version

* Mon Sep 03 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.0-1
- Update to 2.5.0

* Wed Aug 29 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.4.2-1
- Update to 2.4.2

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 2.4.1-3
- Rebuild with fixed binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.4.1-1
- Update to latest release

* Mon May 21 2018 Carl George <carl@george.computer> - 2.4.0-3
- Fix %%preun to correctly remove the lfs filter on uninstall (rhbz#1580357)

* Mon Mar 12 2018 Carl George <carl@george.computer> - 2.4.0-2
- Add %%go_arches fallback to work around Koji issues

* Sun Mar 04 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.4.0-1
- Update to latest release.

* Thu Feb 08 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.3.4-6
- Add patches to build with Go 1.10.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Carl George <carl@george.computer> - 2.3.4-4
- Use vendored libraries on RHEL
- Skip test on RHEL
- Don't build man pages on RHEL due to missing ronn
- Don't build html versions of man pages

* Fri Dec 01 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.3.4-3
- Require git-core instead of git.

* Fri Nov 03 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.3.4-2
- Patch tests to work on slow systems like arm and aarch builders.
- Fix "git lfs help" command.

* Fri Nov 03 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.3.4-1
- Update to latest release.
- Run all tests during build.

* Fri Sep 01 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.1-3
- Remove redundant doc tag on manpages.
- Use path macros in %%post/%%postun.

* Thu Aug 31 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.1-2
- Disable unnecessary subpackages.

* Sun Jul 30 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.1-1
- Update to latest version.

* Wed Apr 19 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.2-2
- Patch up to build with Go 1.7

* Wed Apr 19 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.2-1
- Update to latest release
- Add some requested macros

* Tue Mar 14 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.1-1
- Update to latest release
- Don't disable git-lfs globally during upgrade

* Mon Mar 06 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.0.0-1
- Update to latest release

* Sun Feb 12 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.5.5-1
- Update to latest release
- Add -devel and -unit-test-devel subpackages
- Add post/preun scriptlets for global enablement

* Sun May 15 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.2.0-1
- Initial package
