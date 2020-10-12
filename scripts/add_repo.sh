#!/bin/bash

mkdir ~/bin
curl https://mirrors.tuna.tsinghua.edu.cn/git/git-repo -o ~/bin/repo
chmod +x ~/bin/repo
if [ -f ~/.zshrc ]; then
    echo "PATH=\$PATH:~/bin/" >> ~/.zshrc
    echo "export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo'" >> ~/.zshrc
elif [ -f ~/.bashrc ]; then
    echo "PATH=\$PATH:~/bin/" >> ~/.bashrc
    echo "export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo'" >> ~/.bashrc
fi
export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo'
