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

echo -e "${YELLOW}======= Stage 1: Copy Package Files =======${END}"

status=0
echo ${PASSWORD} | sudo -S rsync -r ${SOURCE} ${DEST}
tmp=$?
status=$[tmp + status];
checkStatus $status

echo -e "${YELLOW}======== Stage 2: Regen Repo Info =========${END}"

status=0
echo ${PASSWORD} | sudo -S createrepo ${DEST}
tmp=$?
status=$[tmp + status];
checkStatus $status

echo -e "${YELLOW}======== Stage 3: Set Permissions =========${END}"

status=0
echo ${PASSWORD} | sudo -S chmod -R u+rwX,go+rX,go-w ${DEST}
tmp=$?
status=$[tmp + status];
checkStatus $status
