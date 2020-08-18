#!/bin/bash
RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
END='\e[0m'
PASSWORD='password'

checkStatus() {
    if [ $1 == 0 ]
    then
        printf "${GREEN}Succeed!${END}\n"
    else
        printf "${RED}Failed!${END}\n"
    fi
}

install_tools()
{
    sudo dnf install rpm-build rpmdevtools dnf-utils gdb -y
}

install_tools
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
