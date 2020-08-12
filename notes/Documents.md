# openEuler for Raspberry Pi 4B

**注意**：本文档中使用系统为 openEuler，使用硬件为 Raspberry Pi 4B with 4 GiB RAM。本文仅保证，截止本文最后更新，文中操作可以在作者处正确执行，一切请以实际情况为准，如有问题，请开 Issue 或者 Pull Request。

## 安装桌面环境之前

众所周知，在 Linux 下使用桌面环境时，一般是不建议使用 `root` 用户进行登录的，因此，我们在这里需要配置多用户环境。

### 安装 `sudo`

首先，如果我们想要其他用户可以用自己的密码提升权限（即达到 `root` 用户的权限），或者使用 `root` 用户，但模拟其他用户的权限来执行命令，则我们需要使用 `sudo` 这一软件

```text
# dnf install sudo
```

当然，就算一时没有上述需求，也可以安装上 `sudo`，并不会影响太多。接下来的内容只有需要使用 `sudo` 的用户需要查看，否则请跳至创建新用户部分。

#### 修改 `sudoers`

这里我们提前简单地提一下如何修改 `sudoers` 文件。并不是所有用户都能使用 `sudo` 命令来提升自己的权限，因此，我们需要将有这一需求的用户 / 用户组添加至 `sudoers` 文件中。
直接使用 `visudo` 命令打开 `sudoers` 文件，这里使用的是 `vim` 编辑器，我们可以使用 hjkl 或者方向键来进行上下左右移动光标的操作，将光标移动至
```text
root    ALL=(ALL)       ALL
```
这一行，按下 `i` 进行编辑，然后新建一行，或者直接按下 `o` 新建一行并开始编辑，将你想要使用 `sudo` 的用户按同样的方式添加到新的一行
```text
your_username    ALL=(ALL)       ALL
```
或者，你可以将用户添加至 wheel 用户组，然后将
```text
%wheel  ALL=(ALL)       ALL
```
这一行最前面的百分号删除。
编辑结束后，按下 `Esc`，输入英文冒号，w，q，也即 `:wq`，按下回车，即可保存并退出。

### 创建新用户

接下来就可以创建新用户了

```text
# useradd -m -G your_group -s login_shell your_username
```

其中 `-m` 选项是指为该用户创建 `/home/your_username` 文件夹，`-G` 选项是指将用户添加进某一用户组（一般 wheel 是管理员用户组），`-s` 选项可以指定用户的登录 Shell，比如 `/bin/bash`，`/bin/zsh` 等等（zsh 需要额外安装），`your_username` 即你想要的用户名。如果你想使用 `bash` 进行登录，创建 `/home/your_username`，并且不将用户添加至其他用户组，你也可以使用下述命令进行用户添加

```text
# adduser your_username
```

注意添加完以后别忘了给用户设置一个密码

```text
# passwd your_username
```

#### 如何切换用户

从 `root` 用户切换至其他用户可以使用

```text
# su your_username
```

从其他用户切换至 `root` 用户可以使用如下命令，但需要输入 `root` 用户的密码

```text
# su
```

从管理员（已添加至 `sudoers`）用户切换至 `root` 用户可以使用如下命令，但需要输入用户自己的密码

```text
# sudo su
```

好了，现在你已经创建好了你的用户，可以开始尝试安装桌面环境了，后面的内容，我们将会用管理员用户的身份来执行命令，并使用用户自己的密码来提升权限。

## 如何在树莓派 4B 上安装桌面环境

**注意**：如前文所说，对于这里的内容，我们将会用管理员用户的身份来执行命令，并使用用户自己的密码来提升权限。
如果你没有设置管理员，对于添加了 `sudo` 的命令，请直接使用 `root` 用户执行去掉 `sudo` 的部分，对于没有添加 `sudo` 的命令，请使用普通用户执行。

### 安装 Xorg 驱动

首先我们需要安装 `xorg-x11-drv-fbdev`，其提供了树莓派所需的 Xorg 驱动。

```text
$ sudo dnf install xorg-x11-drv-fbdev
```

### 安装显示管理器

然后我们需要安装一个 Display Manager，也即中文所说的显示管理器，用于登录用户，启动各种桌面 Session 等。由于树莓派的性能并不是很高，我们一般选择 `lightdm` 进行安装。由于 `lightdm` 没有自带 greeter（greeter 是提示用户输入密码的 GUI 界面），除非配置了自动登录，一般情况下我们都需要安装一个 greeter。这里我们使用常见的 `lightdm-gtk`。

```text
$ sudo dnf install lightdm lightdm-gtk
```

### 安装桌面环境

接下来就是安装桌面环境了，同样地，由于树莓派性能较差，我们不推荐安装常见的 GNOME，KDE Plasma 等桌面环境，而推荐使用 LXQt，MATE，Xfce 等轻量级的桌面环境，这里我们使用的是 Xfce。

```text
$ sudo dnf install xfce4-session xfwm4
```

注意，请在 `/etc/selinux/config` 中关闭 SELinux，或者你可以修改 `/etc/selinux/config` 中的对应选项并安装相应的规则来避免报错，但目前测试即使安装了 SELinux 对应规则也会有无法启动等问题，建议直接关闭。
在 openEuler 中，`lightdm.service` 会被自动 enable，因此安装完毕后，直接重启，就可以看到进入了 `lightdm` 的界面，在右上角选择合适的语言，并选中 Xfce Session，输入用户的密码即可进入 Xfce 桌面了。
如果发现图形界面与显示器边框之间有较大边框，请尝试编辑 `/boot/config.txt`，并取消 `disable_overscan=1` 的注释，如果仍有问题，请手动调整下面的 `overscan_left`，`overscan_right` 等数值。

### 安装配套软件

此时的 Xfce 仅仅只是一个单独的桌面，没有配套软件，对此，我们可以按需安装各种软件，下面将给出介绍。

- `Thunar`，Xfce 桌面的文件管理器。
    - `thunar-vcs-plugin`，整合部分 SVN 和 Git 操作到 Thunar 中。
    - `thunar-media-tags-plugin`，给 Thunar 增加媒体信息显示，并让用户能修改媒体标签。
    - `thunar-archive-plugin`，让用户能在 Thunar 内创建或解压压缩文件。
- `gigolo`，Xfce 桌面的远程文件系统管理器，方便让用户连接诸如 FTP / SAMBA 等远程文件服务。
- `parole`，Xfce 桌面的媒体播放器。
- `xfce4-terminal`，Xfce 桌面的终端模拟器。
- `xfburn`，Xfce 桌面的光碟烧录软件。
- `Midori`，Xfce 桌面的网页浏览器。
- `catfish`，Xfce 桌面的文件搜索器。
- `ristretto`，Xfce 桌面的图片浏览器。
- `xarchiver`，Xfce 桌面的压缩文件管理器。
- `xfdesktop`，`xfce-theme-manager`，Xfce 桌面、主题相关。
- `xfce4-settings`，Xfce 桌面的各种设置项。
- `xfce4-power-manager`，Xfce 桌面的电源管理。
- `xfce4-screenshooter`，Xfce 桌面的截图软件。
- `xfce4-screensaver`，Xfce 桌面的锁屏管理软件。
- `xfce4-panel-profiles`，让用户可以对 Xfce panel 的样式进行备份、管理和恢复。
- `xfce4-notifyd`，Xfce 桌面的通知管理器。
- `xfce4-dict`，Xfce 桌面的词典。
- `xfce4-taskmanager`，Xfce 桌面的任务管理器。
- `xfdashboard`，提供类似 GNOME Shell 的多工作空间管理和应用搜索界面。
- `xfce4-appfinder`，让用户可以搜索已安装的应用，或是使用快捷键等方式快速启动应用。
- `xfce4-volumed-pulse`，用于在 Xfce 桌面使用键盘快捷键调节音量
- `network-manager-applet`，用于在 Xfce 桌面连接网络。
- `blueman`，用于在 Xfce 桌面连接蓝牙设备。
- `fcitx`，一个常用的输入法框架，我们可以用其搭配输入法模块来使用各种输入法。
    - `fcitx-qt5`，`fcitx-qt4`，`fcitx-gtk3`，`fcitx-gtk2` 提供对各类应用的支持。
    - `fcitx-libpinyin`，提供拼音输入法。
    - `fcitx-configtool`，提供 `fcitx` 的 GUI 配置界面。
- `openEuler-logos`，提供 openEuler 社区的桌面壁纸。
- `gnome-font-viewer` 和 `font-manager` 提供字体管理。
- `google-noto-cjk-fonts`，提供中日韩字型，包括黑体和宋体以及等宽字体。如果觉得体积太大，可仅安装下述中文部分。如不安装，则中文字体可能会显示为方块或者不显示。
    - `google-noto-sans-cjk-sc-fonts`，提供中文字型，黑体。
    - `google-noto-serif-cjk-sc-fonts`，提供中文字型，宋体。
    - `google-noto-sans-mono-cjk-sc-fonts`，提供中文字型，等宽字体。
- `mousepad`、`geany` 和 `gedit` 是轻量的，基于 GTK 的文本编辑器。

使用 `imsettings-list` 可以看到输入法默认选择的是 `fcitx`，如果不是，可以使用 `imsettings-switch` 来进行切换。

`xfce4-panel` 提供了绝大多数 Xfce 桌面的功能，例如原本的应用启动器、开始菜单、工作空间切换等，其有非常多的插件可以进行安装，列表如下：
- `xfce4-battery-plugin`，电池电量监控。
- `xfce4-calculator-plugin`，计算器。
- `xfce4-clipman-plugin`，剪贴板管理器。
- `xfce4-cpugraph-plugin`，显示 CPU 支持和被使用的频率信息。
- `xfce4-datetime-plugin`，显示日期和时间，单击可以显示日历。
- `xfce4-diskperf-plugin`，显示实时硬盘 / 分区性能。
- `xfce4-embed-plugin`，将任意应用的窗口固定到 panel。
- `xfce4-eyes-plugin`，一双眼睛。
- `xfce4-fsguard-plugin`，监控挂载点并在达到限额时警告。
- `xfce4-genmon-plugin`，使用脚本监控各项数据并显示在 panel 上。
- `xfce4-hardware-monitor-plugin`，监控各项硬件数据（CPU 占用，网络吞吐量等）。
- `xfce4-mailwatch-plugin`，监控邮箱是否有新邮件。
- `xfce4-mount-plugin`，快捷挂载 / 取消挂载分区或移动存储等。
- `xfce4-mpc-plugin`，一个 MPD 的 GUI 控制器。
- `xfce4-netload-plugin`，显示当前选中网络设备的负载。
- `xfce4-notes-plugin`，提供笔记功能。
- `xfce4-places-plugin`，提供一个快速访问某些文件夹的目录。
- `xfce4-pulseaudio-plugin`，调节麦克风、扬声器的音量。
- `xfce4-sensors-plugin`，支持显示硬件传感器的温度。
- `xfce4-smartbookmark-plugin`，快捷使用各种搜索引擎进行搜索。
- `xfce4-statusnotifier-plugin`，支持让应用显示自己的状态，并与用户进行互动。
- `xfce4-stopwatch-plugin`，秒表。
- `xfce4-systemload-plugin`，系统负载监视器，显示 CPU 负载，交换空间占用及在线时间等。
- `xfce4-timer-plugin`，闹钟。
- `xfce4-time-out-plugin`，定时锁定计算机以让用户休息。
- `xfce4-verve-plugin`，快速执行命令，打开 URL 等，支持补全。
- `xfce4-wavelan-plugin`，显示无线网络的信号、状态、SSID 等。
- `xfce4-weather-plugin`，显示当前的天气状态以及天气预报。
- `xfce4-whiskermenu-plugin`，一个开始菜单替代，可以列出收藏、最近使用的应用，也可以配置关机使用的命令等。
- `xfce4-xkb-plugin`，设置、选择键盘布局。

未完待续
