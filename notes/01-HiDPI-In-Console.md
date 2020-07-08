---
title: HiDPI In Console
date: 2020-07-08 08:50:34
---

## 提出问题

前天收到了暑期 2020 项目由 openEuler 社区寄来的 Raspberry Pi 4B，我也要开始着手准备进行 Xfce 的移植项目了。为了方便完成这个项目，我也购置了一台 4K 分辨率的显示器，使用自己的主机连接显示器时，Console 中的字体是比较大的，而连接 Raspberry Pi 到显示器时，可以主要到字体非常小，十分影响使用。

在网上查阅资料后，我注意到可以使用 `setfont` 来在 Console 中使用 16 × 32 的字体，以实现 HiDPI 的效果，可使用的字体在 openEuler 系统中位于 `/usr/lib/kbd/consolefonts`，在 Archlinux 中位于 `/usr/share/kbd/consolefonts`，但是我发现两个系统中都没有 16 × 32 的字体在对应位置，因此是无法使用 `setfont` 来达成的。那么是否可以通过安装 `terminus-font` 来使系统包含 16 × 32 的字体呢？事实上，Archlinux 没有安装该字体，也能做到在 Console 中实现 HiDPI 的效果，因此我们需要进一步查询资料。

## 解决问题

再经过一番查找后，我在 https://wiki.archlinux.org/index.php/Linux_console#Fonts 中注意到，内核选项 `CONFIG_FONT_TER16x32` 似乎可以将 16 × 32 的字体置入内核。查阅内核里的 `Kconfig` 后，我发现 openEuler 使用的 4.19 内核暂无该选项，那么我们现在有两个选择，第一是 upgrade 内核到主线，第二是 backport 该特性到 4.19。在 GitHub 上查看了一下实现该特性的提交，我注意到只有寥寥几个提交，那么，第二种方案则是较好的选择，因为紧跟主线内核十分麻烦，可能需要解决非常多的问题，而只 backport 该特性的话则不需要付出太多时间。

cherry-pick 下方几个提交到 openEuler 组织下的 raspberry-kernel 仓库中，在 `arch/arm64/configs/openeuler-raspi_defconfig` 中设置 `CONFIG_FONT_TER16x32=y` 以及 `CONFIG_FONTS=y`，然后再按照 https://gitee.com/openeuler/raspberrypi/blob/master/documents/交叉编译内核.md 中的教程进行交叉编译，并将编译好的内核替换，开机，就可以看到确实使用了 16 × 32 的字体，显著提升了在高分辨率显示器下的使用体验。

### 用到的提交

* https://github.com/torvalds/linux/commit/ac8b6f148fc97e9e10b48bd337ef571b1d1136aa

* https://github.com/torvalds/linux/commit/aa1d19f1f96764e72155235ece22461599d0e7ac

* https://github.com/torvalds/linux/commit/73a649d2b98e25f4960b8081080c78695fea8bc7

* https://github.com/torvalds/linux/commit/dfd19a5004eff03755967086aa04254c3d91b8ec

