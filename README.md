# Xfce for openEuler (running on Raspberry Pi 4B)

- [项目结构](#项目结构)
- [相关下载](#相关下载)
- [软件包相关情况](#软件包相关情况)
- [项目状态](#项目状态)
- [相关文档](#相关文档)

## 项目结构

- [graphviz](./graphviz)：该文件夹包含了部分软件的依赖关系图。
- [notes](./notes)：该文件夹包含了参与该项目时，遇到问题及解决问题的相关记录，每周汇报，以及相关使用文档等等。
    - [文档](./notes/Documents.md)：其中是如何使用 Raspberry Pi 4B，以及安装桌面环境的部分文档。
- [repo](https://github.com/dragonjacson/raspi-repo)：该文件夹包含了同步项目软件包列表所需的 manifest 文件。
- [patches](./patches)：该文件夹包含了对内核等部分软件包所需要的 patch。
- [pkgs](./pkgs)：该文件夹包含了在完成项目的过程中，需要使用到，但 openEuler 源里暂时没有的软件包。
- [scripts](./scripts)：该文件夹包含了完成该项目中使用到的部分脚本。
    - [add\_repo.sh](./scripts/add_repo.sh)：添加 `repo` 文件到 `~/bin` 下，并将 `~/bin` 添加到 `PATH` 中（通过修改 `.zshrc` 和 `.bashrc` 的方式），同时将 `repo` 的下载源指定为清华的镜像源，使用 `source add_repo.sh` 来使 `REPO_URL` 生效。
    - [add\_source.sh](./scripts/add_source.sh)：创建 `~/sources` 目录，并根据 `https://github.com/dragonJACson/raspi-repo`
    中的 manifest，init 源仓库（需要提前配置 `git config --global user.name "Name"` 和 `git config --global user.email "Email"`）。
    - [build.sh](./scripts/build.sh)：进入有 SPEC 文件和源码包的文件夹后，使用 `build.sh` 来进行对某一个包的打包（例如 src-openEuler 中存储软件包 SPEC 的仓库，进入后，使用 build.sh 即可打包）。需要修改 `PASSWORD` 为管理员用户的密码，或者也可以修改脚本，以 `sudo` 来执行。
    - [buildall.sh](./scripts/buildall.sh)：与 `build.sh` 类似，搭配 `add_source.sh` 使用，同步完包仓库后，使用其对软件包进行批量打包，打包顺序按 `pkglist` 中的执行，建议按依赖顺序维护 `pkglist`。同时在打包完成的软件包文件夹下生成文件 `success.token`（目前判断打包是否完成是通过监测 `~/rpmbuild/RPMS` 下有无新增文件），在下次执行该脚本时，如监测到有该文件存在，则跳过打包该软件包。需要修改 `PASSWORD` 为管理员用户的密码，`RPMPATH` 为 `rpmbuild` 执行后，打包生成软件包的路径，`SRCPATH` 为各软件包文件夹的父目录，`PKGLIST` 为 `pkglist` 文件。也可以修改脚本，以 `sudo` 来执行。
    - [syncpack.sh](./scripts/syncpack.sh)：将软件包从 `rpmbuild` 执行后，打包生成软件包的路径，复制到目标路径，并给予正确的权限，方便自建网络源。需要修改 `PASSWORD` 为管理员用户的密码，`SOURCE` 为源路径，`DEST` 为目的路径。也可以修改脚本，以 `sudo` 来执行。
    - [tokens.sh](./scripts/token.sh)：监测目标目录下的 `*.token` 文件，默认输出所有该文件的路径，使用 `tokens.sh -d path/to/dir` 或者 `tokens.sh --delete path/to/dir` 来删除这些 `*.token` 文件。
- [raspberrypi](https://gitee.com/lukedyue/raspberrypi)：基于 https://gitee.com/openeuler/raspberrypi 中的脚本修改得到的，可以制作桌面镜像的脚本。

## 相关下载

- [Headless 镜像](https://github.com/dragonJACson/summer2020_openeuler/releases/download/v1.0/raspi-1.0-headless.img.xz)（构建于 2020-10-12）
- [Standard 镜像](https://github.com/dragonJACson/summer2020_openeuler/releases/download/v1.0/raspi-1.0-standard.img.xz)（构建于 2020-10-11）
- [Full 镜像](https://github.com/dragonJACson/summer2020_openeuler/releases/download/v1.0/raspi-1.0-full.img.xz)（构建于 2020-10-12）
- [相关 RPM 软件包](https://github.com/dragonJACson/summer2020_openeuler/releases/download/v1.0/rpms.tar.gz)

## 软件包相关情况

**openEuler 暂未建立仓库的包**

- midori（由于多次测试均有问题，暂未考虑向 src-openEuler 提交）
- neofetch（工具类软件，非必要，优先级较低）
- sysconftool（暂未提交 Pull Request，后面视情况提交）
- inkscape（工具类软件，非必要，优先级较低）
- materia-gtk-theme（主题类软件，非必要，优先级较低）
- papirus-icon-theme（主题类软件，非必要，优先级较低）
- google-roboto-fonts（字体，非必要，优先级较低）

**openEuler 已建立仓库但暂无提交的包**

- gparted（有社区提交的 [Pull Request](https://gitee.com/src-openeuler/gparted/pulls/1)，但暂未合并）
- lightdm-gtk（有我提交的 [Pull Request](https://gitee.com/src-openeuler/lightdm-gtk/pulls/1)，但暂未合并）
- ncdu（工具类软件，非必要，优先级较低）
- im-chooser（有社区提交的 [Pull Request](https://gitee.com/src-openeuler/im-chooser/pulls/1)，但暂未合并）
- fcitx-configtool（有社区提交的 [Pull Request](https://gitee.com/src-openeuler/fcitx-configtool/pulls/1)，但暂未合并）
- unique3（有社区提交的 [Pull Request](https://gitee.com/src-openeuler/unique3/pulls/1)，但暂未合并）
- gtk-murrine-engine（有社区提交的 [Pull Request](https://gitee.com/src-openeuler/gtk-murrine-engine/pulls/1)，但暂未合并）
- libgxim（有我提交的 [Pull Request](https://gitee.com/src-openeuler/libgxim/pulls/1)，但暂未合并）
- fcitx（有我提交的 [Pull Request](https://gitee.com/src-openeuler/fcitx/pulls/1)，但暂未合并）
- fcitx-qt5（有我提交的 [Pull Request](https://gitee.com/src-openeuler/fcitx-qt5/pulls/1)，但暂未合并）
- fcitx-libpinyin（有我提交的 [Pull Request](https://gitee.com/src-openeuler/fcitx-libpinyin/pulls/1)，但暂未合并）

**openEuler 仓库中有提交，但源里暂时未提供的软件包**

- htop
- imsettings
- libxfce4util
- xfconf
- libxfce4ui
- exo
- garcon
- xfwm4
- xfce4-panel
- xfce4-session
- Thunar
- xfdesktop
- thunar-archive-plugin
- thunar-media-tags-plugin
- thunar-vcs-plugin
- thunar-volman
- python-distutils-extra
- catfish
- tumbler
- ristretto
- mousepad
- Midori
- parole
- gigolo
- blueman
- libnma
- network-manager-applet
- xfce4-dev-tools
- xfburn
- xarchiver
- xfce4-appfinder
- xfce4-dict
- xfce4-notifyd
- xfce4-panel-profiles
- xfce4-power-manager
- xfce4-screensaver
- xfce4-screenshooter
- xfce4-settings
- xfce4-taskmanager
- xfce4-terminal
- xfce4-volumed-pulse
- xfce-polkit
- xfce-theme-manager
- xfdashboard
- xfce4-battery-plugin
- xfce4-calculator-plugin
- xfce4-clipman-plugin
- xfce4-cpugraph-plugin
- xfce4-datetime-plugin
- xfce4-diskperf-plugin
- xfce4-embed-plugin
- xfce4-eyes-plugin
- xfce4-fsguard-plugin
- xfce4-genmon-plugin
- gtkmm24
- libglademm24
- libgnomecanvasmm26
- xfce4-hardware-monitor-plugin
- xfce4-mailwatch-plugin
- xfce4-mount-plugin
- xfce4-mpc-plugin
- xfce4-netload-plugin
- xfce4-notes-plugin
- xfce4-places-plugin
- xfce4-pulseaudio-plugin
- xfce4-sensors-plugin
- xfce4-smartbookmark-plugin
- xfce4-statusnotifier-plugin
- xfce4-systemload-plugin
- xfce4-time-out-plugin
- xfce4-timer-plugin
- xfce4-verve-plugin
- xfce4-wavelan-plugin
- xfce4-weather-plugin
- xfce4-whiskermenu-plugin
- xfce4-xkb-plugin

## 项目状态

- 对于网络设置，连接无线网络，可以使用 `network-manager-applet`
- 对于蓝牙传输文件，可以使用 `blueman`
- 对于文件管理器，可以使用 Xfce 配套的 `Thunar`
- 对于浏览器，可以使用 Xfce 配套的 `midori` 或者 `firefox`（`midori` 只在访问部分网页时正常工作，请视情况使用）

## 相关文档

- 请参见
    - GitHub: https://github.com/dragonJACson/summer2020_openeuler/blob/master/notes/Documents.md
    - Gitee: https://gitee.com/lukedyue/summer2020/blob/master/notes/Documents.md
    - VuePress: https://ragondl.github.io/RaspberryPi/Documents.html
