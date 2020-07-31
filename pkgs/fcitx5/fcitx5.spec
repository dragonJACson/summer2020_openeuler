%global commit 327912d9c855f906d823f7c70c188b7faf2c268e
%global endictver 20121020

Name:           fcitx5
Summary:        Next generation of fcitx
Version:        0.0.0.20200728
Release:        1
License:        GPL
Source0:        https://github.com/fcitx/fcitx5/archive/${commit}/fcitx5-${commit}.tar.gz
Source1:        https://download.fcitx-im.org/data/en_dict-${endictver}.tar.gz
URL:            https://github.com/fcitx/fcitx5

BuildRequires:  tar, gcc-g++, cmake
BuildRequires:  extra-cmake-modules
Requires:       fontpackages-filesystem

Provides: fcitx

%description
Next generation of fcitx.

%prep
%setup -q -n fcitx5-${commit} -c
ln -s en_dict-$_endictver.tar.gz ./src/modules/spell/dict

%build
cd fcitx5-${commit}

cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_LIBDIR=/usr/lib .
%make_build

%if %{with tests}
%check
make test
%endif

%install
%make_install
