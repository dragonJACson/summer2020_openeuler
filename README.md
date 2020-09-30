# Xfce for openEuler (running on Raspberry Pi 4B)

## 项目结构

- [graphviz](./graphviz)：该文件夹包含了部分软件的依赖关系图。
- [notes](./notes)：该文件夹包含了参与该项目时，遇到问题及解决问题的相关记录，每周汇报，以及相关使用文档等等。
    - [文档](./notes/Documents.md)：其中是如何使用 Raspberry Pi 4B，以及安装桌面环境的部分文档。
- [repo](https://github.com/dragonjacson/raspi-repo)：该文件夹包含了同步项目软件包列表所需的 manifest 文件。
- [patches](./patches)：该文件夹包含了对内核等部分软件包所需要的 patch。
- [pkgs](./pkgs)：该文件夹包含了在完成项目的过程中，需要使用到，但 openEuler 源里暂时没有的软件包。
- [scripts](./scripts)：该文件夹包含了完成该项目中使用到的部分脚本。
    - [add\_repo.sh](./scripts/add_repo.sh)：添加 `repo` 文件到 `~/bin` 下，并将 `~/bin` 添加到环境变量中（通过修改 `.zshrc` 和 `.bashrc` 的方式），同时将 `repo` 的下载源指定为清华的镜像源。
    - [add\_source.sh](./scripts/add_source.sh)：创建 `~/sources` 目录，并根据 `https://github.com/dragonJACson/raspi-repo`
    中的 manifest，init 源仓库（需要提前配置 `git config --global user.name "Name"` 和 `git config --global user.email "Email"`）。
    - [build.sh](./scripts/build.sh)：进入有 SPEC 文件和源码包的文件夹后，使用 `build.sh` 来进行对某一个包的打包（例如 src-openEuler 中存储软件包 SPEC 的仓库，进入后，使用 build.sh 即可打包）。需要修改 `PASSWORD` 为管理员用户的密码，或者也可以修改脚本，以 `sudo` 来执行。
