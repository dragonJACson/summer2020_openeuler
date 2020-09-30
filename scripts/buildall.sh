#!/bin/bash
RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
END='\e[0m'
PASSWORD='password'
RPMPATH='/rpmbuild/RPMS'
SRCPATH='/sources/src-openeuler/pkgs'
PKGLIST='/pkglist'

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

print_info() {
    echo -e "${GREEN}$succ package(s) built successfully.\n${END}"
    echo -e "${YELLOW}$skip package(s) were skipped.\n${END}"
    echo -e "${RED}$fail package(s) built unsuccessfully.\n${END}"
    echo -e "For detailed info, please check ${SRCPATH}/build-log.txt"
    exit
}

prepare()
{
    mkdir -p ~/rpmbuild/RPMS
    mkdir -p ~/rpmbuild/SPECS
    mkdir -p ~/rpmbuild/SOURCES
}

install_tools
add_repo
prepare
succ=0
fail=0
skip=0
rm ${SRCPATH}/build-log.txt
trap print_info INT

while read pkgname;
do
    cd ${SRCPATH}/${pkgname}
    count1=`find ${RPMPATH}/aarch64/ -type f | wc -l`
    count1=$[count1 + `find ${RPMPATH}/noarch/ -type f | wc -l`]
    if [ ! -f ${SRCPATH}/${pkgname}/success.token ]; then
        echo -e "${YELLOW}======= Stage 1: Copy Build Files =======${END}"

        status=0
        find ./ -type f -not -iname "*.spec" -not -iname "*.md" -not -iname "*.yaml" -not -path '*/\.*' -exec cp {} ~/rpmbuild/SOURCES/ \;
        cp *.spec ~/rpmbuild/SPECS/
        tmp=$?
        status=$[tmp + status];
        rm ~/rpmbuild/SOURCES/*.spec ~/rpmbuild/SOURCES/*.md
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
        count2=`find ${RPMPATH}/aarch64/ -type f | wc -l`
        count2=$[count2 + `find ${RPMPATH}/noarch/ -type f | wc -l`]
        if [ count2 -gt count1 ]; then
            echo "${PWD##*/} OK!" >> ${SRCPATH}/build-log.txt
            succ=$[succ + 1]
            touch ${SRCPATH}/${pkgname}/success.token
        else
            echo "${PWD##*/} Failed!" >> ${SRCPATH}/build-log.txt
            fail=$[fail + 1]
        fi
    else
        skip=$[skip + 1]
    fi
done < ${PKGLIST}

trap print_info EXIT
