---
title: Create Your Own Yum Repo
date: 2020-07-27 15:07:28
---

## 提出问题

树莓派 4B 的性能在编译较大的项目时捉襟见肘，使用服务器进行打包无疑是更好的选择，但是服务器打出来的包怎么传到树莓派上呢？直接下载到本地不失为一种选择，但是这样做非常不方便，尤其是在处理依赖的时候，那么，什么样的方法才是相对优解呢？

## 解决问题

其实解决问题也很简单，openEuler 的包是从哪里下载的？从源里下载的。那么，我们自建一个 yum 源，就能完美的解决问题了。对于 openEuler 自己的包来说，由于数量较大，通常会使用自动化 / 持续集成工具进行批量构建和检测，但是我们自己构建的包目前还不多，而且很多包都需要手动验证，因此这里暂时用不到自动化工具。随着包的数量逐渐增加，我们也可以使用 [Copr](https://pagure.io/copr/copr/tree/master) 来自动化构建，并根据你所有的包直接生成一个可用的源（这一点也是其和 OBS 不同之处），但是目前其暂不支持为 openEuler 构建包，可在 [mock](https://github.com/rpm-software-management/mock) 查看相关支持情况。下面开始介绍如何自建 yum 源。

首先我们需要安装 `rpm-build` 和 `createrepo` 这两个包，其中 `rpm-build` 包含了打包所需要的工具，`createrepo` 则包含了创建软件源所需要的工具

```bash
$ sudo dnf install rpm-build createrepo
```

然后创建你想存放 RPM 软件包的文件夹，并将 RPM 包存入其中

```bash
$ sudo mkdir /path/to/rpmrepo && sudo mv /path/to/rpms/* /path/to/rpmrepo
```

现在执行 `createrepo` 命令，生成 repodata

```bash
$ sudo createrepo /path/to/rpmrepo
```

注意，每次我们往该文件夹中添加或者删除或者改变一个包，我们都需要重新执行一次 `createrepo` 命令，这个包才会被（重新）索引。
别忘了给包和文件夹正确的权限（文件夹为 755，文件为 644），否则我们无法访问它。

```bash
$ sudo chmod -R u+rwX,go+rX,go-w /path/to/rpmrepo
```

最后，我们只需要在 `/etc/yum.repo.d/custom.repo` 里添加对应的信息即可大功告成。

```text
[yarepo]
name=Yet Another Repository
baseurl=http://url.to/yourrepo
enabled=1
gpgcheck=0
```
