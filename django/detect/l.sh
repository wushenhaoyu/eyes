cd /var/www/app/
nohup python -u nystagmus.py $1  > test.log 2>&1 &

#仅调用眼震视图部分代码