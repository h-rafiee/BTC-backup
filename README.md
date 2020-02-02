# BTC Backup Script
_powered by **Python v 3**_ :snake:

## Get started
just run by below command :

```python3 run.py```

### Help
you can use `-h` parameter to get help about script.

### Options

arguments | description
---| ---
--rpc-user | for set user on rpc coneection
--rpc-password | for set password on rpc connection
--method | for set method backup `full|wallet|privateKey`
--path | for set path for keep backups
--ftp-server | host of ftp backup must be push
--ftp-user | user of ftp connection
--ftp-pass | password of ftp connection
--ftp-path | set path to upload
--ftp-disable | for disable push to ftp usage `--ftp-disable` doesn't need value

### Default Values
arguments | value
--- | ---
--rpc-user | earth
--rpc-password | YANoPHjXzgkDv*******
--method | full
--path | /var/backup/.btc
--ftp-server | 78.***.***.159
--ftp-user | btc1001
--ftp-pass | btc****
--ftp-path | /.btc/

## Hint

> for upload you have to create a specific directory with account owner because root of ftp is not safe place.

##### Best regards 
###### _Hossein Rafiee_ - 2018 oct
