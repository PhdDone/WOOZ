
BACKUP=/home/yzhdong/mobvoi/wooz/WOOZ/db/backups/$(date +%F--%T) 
mkdir $BACKUP
mongodump --out $BACKUP
