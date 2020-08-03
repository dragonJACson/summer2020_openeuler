# openEuler for Raspberry Pi 4B

**注意**：本文档中使用系统为 openEuler，使用硬件为 Raspberry Pi 4B with 4 GiB RAM。本文仅保证，截止本文最后更新，文中操作可以在作者处正确执行，一切请以实际情况为准，如有问题，请开 Issue 或者 Pull Request。

## 安装桌面环境之前

众所周知，在 Linux 下使用桌面环境时，一般是不建议使用 `root` 用户进行登录的，因此，我们在这里需要配置多用户环境。

### 安装 `sudo`

首先，如果我们想要其他用户可以用自己的密码提升权限（即达到 `root` 用户的权限），或者使用 `root` 用户，但模拟其他用户的权限来执行命令，则我们需要使用 `sudo` 这一软件

```bash
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

```bash
# useradd -m -G your_group -s login_shell your_username
```

其中 `-m` 选项是指为该用户创建 `/home/your_username` 文件夹，`-G` 选项是指将用户添加进某一用户组（一般 wheel 是管理员用户组），`-s` 选项可以指定用户的登录 Shell，比如 `/bin/bash`，`/bin/zsh` 等等（zsh 需要额外安装），`your_username` 即你想要的用户名。如果你想使用 `bash` 进行登录，创建 `/home/your_username`，并且不将用户添加至其他用户组，你也可以使用下述命令进行用户添加

```bash
# adduser your_username
```

注意添加完以后别忘了给用户设置一个密码

```bash
# passwd your_username
```

#### 如何切换用户

从 `root` 用户切换至其他用户可以使用

```bash
# su your_username
```

从其他用户切换至 `root` 用户可以使用如下命令，但需要输入 `root` 用户的密码

```bash
# su
```

从管理员（已添加至 `sudoers`）用户切换至 `root` 用户可以使用如下命令，但需要输入用户自己的密码

```bash
# sudo su
```

好了，现在你已经创建好了你的用户，可以开始尝试安装桌面环境了，后面的内容，我们将会用管理员用户的身份来执行命令，并使用用户自己的密码来提升权限。

## 如何在树莓派 4B 上安装桌面环境

**注意**：如前文所说，对于这里的内容，我们将会用管理员用户的身份来执行命令，并使用用户自己的密码来提升权限。
如果你没有设置管理员，对于添加了 `sudo` 的命令，请直接使用 `root` 用户执行去掉 `sudo` 的部分，对于没有添加 `sudo` 的命令，请使用普通用户执行。

### 安装 Xorg 驱动

首先我们需要安装 `xorg-x11-drv-fbdev`，其提供了树莓派所需的 Xorg 驱动。

```bash
$ sudo dnf install xorg-x11-drv-fbdev
```

### 安装显示管理器

然后我们需要安装一个 Display Manager，也即中文所说的显示管理器，用于登录用户，启动各种桌面 Session 等。由于树莓派的性能并不是很高，我们一般选择 `lightdm` 进行安装。由于 `lightdm` 没有自带 greeter（greeter 是提示用户输入密码的 GUI 界面），除非配置了自动登录，一般情况下我们都需要安装一个 greeter。这里我们使用常见的 `lightdm-gtk`。

```bash
$ sudo dnf install lightdm lightdm-gtk
```

### 安装桌面环境

接下来就是安装桌面环境了，同样地，由于树莓派性能较差，我们不推荐安装常见的 GNOME，KDE Plasma 等桌面环境，而推荐使用 LXQt，MATE，Xfce 等轻量级的桌面环境，这里我们使用的是 Xfce。

