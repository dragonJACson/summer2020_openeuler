#!/bin/bash
RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
END='\e[0m'
PASSWORD='password'
RPMPATH='~/rpmbuild/RPMS'
SRCPATH='~/sources/src-openeuler/pkgs'
PKGLIST='./pkglist'

checkStatus() {
    if [ $1 == 0 ]
    then
        printf "${GREEN}Succeed!${END}\n"
    else
        printf "${RED}Failed!${END}\n"
    fi
}

install_tools() {
    echo ${PASSWORD} | sudo -S dnf install createrepo rpm-build rpmdevtools dnf-utils gdb -y
}

add_repo() {
    echo -e "[xfce-repo]\nname=xfce-repo\nbaseurl=file://${RPMPATH}\nenabled=1\ngpgcheck=0" | sudo tee /etc/yum.repos.d/xfce.repo
    createrepo ${RPMPATH}
}

install_tools
add_repo
while read pkgname;
do
    cd ${SRCPATH}/${pkgname}
    echo -e "${YELLOW}======= Stage 1: Copy Build Files =======${END}"

    status=0
    find ./ -type f -not -iname "*.spec" -not -iname "*.md" -not -iname "*.yaml" -not -path '*/\.*' -exec cp {} ~/rpmbuild/SOURCES/ \;
    cp *.spec ~/rpmbuild/SPECS/
    tmp=$?
    status=$[tmp + status];
    rm ~/rpmbuild/SOURCES/*.spec ~/rpmbuild/SOURCES/*.md
    tmp=$?
    status=$[tmp + status];
    checkStatus $status

    echo -e "${YELLOW}========== Stage 2: Build Deps ==========${END}"

    status=0
    echo ${PASSWORD} | sudo -S dnf -y builddep *.spec --refresh
    status=$[tmp + status];
    checkStatus $status

    echo -e "${YELLOW}======== Stage 3: Build Package =========${END}"

    status=0
    rpmbuild -ba *.spec
    tmp=$?
    status=$[tmp + status];
    checkStatus $status

    echo -e "${YELLOW}======= Stage 4: Regen database =========${END}"
    createrepo ${RPMPATH}
done < ${PKGLIST}
