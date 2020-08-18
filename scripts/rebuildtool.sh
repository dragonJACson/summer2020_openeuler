#!/bin/bash

# Modified from https://github.com/FZUG/repo/blob/master/repos/rebuildtool.sh
# Credits to FZUG

# You need the following line in /etc/sudoers
# builduser ALL=NOPASSWD: /usr/bin/yum-builddep, /usr/bin/dnf

function install_tools()
{
    sudo dnf install rpm-build rpmdevtools dnf-utils -y
}

function prepare_src()
{
    # spectool -g -R ${SPECPATH}
    find ./ -type f -not -iname "*.spec" -not -iname "*.md" -not -iname "*.yaml" -not -path '*/\.*' -exec cp {} ~/rpmbuild/SOURCES/ \;
    echo ${SPECDIR}
}

function rpm_build()
{
    log_path=$(echo ${SPECPATH} | sed 's/\//_/g' | sed 's/ /_/g')
    echo "* yum-builddep for ${PKGNAME}"
    sudo yum-builddep -y ${SPECPATH} >/dev/null
    echo "* rpmbuild for ${PKGNAME}"
    rpmbuild -ba ${SPECPATH} &> ${TOP_DIR}/${log_path}-FAILED.log
    if [ $?==0 ] ; then mv ${TOP_DIR}/${log_path}-FAILED.log ${TOP_DIR}/${log_path}-PASSED.log; fi
    pushd ~/rpmbuild/RPMS
    # Comment this line if you don't want to update the repo
    # createrepo_c --update ~/rpmbuild/RPMS
    popd
}

function traverse_build()
{
    TOP_DIR=$1
    for i in `find ${TOP_DIR} -type f -iname "*.spec"` ;
    do
        SPECPATH=$i
        SPECNAME=$(echo ${SPECPATH} | awk -F '/' '{print $NF}')
        SPECDIR=$(echo ${SPECPATH} | sed 's/${SPECNAME}//g')
        echo ${SPECDIR}
        PKGNAME=$(echo ${SPECNAME} | sed 's/.SPEC//g' | sed 's/.spec//g')
        if ! grep -q "${SPECPATH}" ${TOP_DIR}/list_done ; then
            echo "--------${PKGNAME} start--------"
            echo "${SPECPATH}" >> ${TOP_DIR}/list_done
            prepare_src
            rpm_build
            echo "--------${PKGNAME} finished--------"
        fi
    done
}

traverse_build $@


