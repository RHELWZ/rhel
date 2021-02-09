#!/usr/local/bin/python3
def shend_icmp_packet(ip_address,times):
    try:
        response = os.popen('ping -c ' + str(times) + ' '+ ip_address).read()
        print(response)
        # 取出丢包率
        lost = response[response.rindex(',',0,response.index("%"))+1:response.index("%")].strip()
        #取出指定的延时字符串
        res = list(response)
        index = 0
        count = 0
        for r in res:
            count += 1
            if r == "=" :
                index = count
        response = response[index + 1:-4]

        # 取出执行的延迟
        i = 0
        j = []
        res1 = list(response)
        for r in res1:
            i += 1
            if r == "/" :
                j.append(i)

        min = response[:j[0]-1]
        avg = response[j[0]:j[1]-1]
        max = response[j[1]:j[2]-1]
        return min,avg,max,lost
    except Exception as e:
        print("ping exec error",e)
postgres操作
		云pg添加权限
			select control_extension('create', 'pg_trgm');
		清除wal日志：pg_archivecleanup /home/pgsql_arch 00000002000000320000005F	（10.4版本的大多在pg_wal下，此命令会删掉此之前的所有数据）
					 若数据库起不来可用命令恢复：pg_resetwal /home/pgsql_data
		给vrp用户授权表的读权限
			grant select on 表 to vrp
		
		数据库重命名
			alter database [] rename to []
			
		备份恢复单表,到处表结构 加-s参数
			备份：pg_dump -h 10.1.13.48 -U postgres -t TABLE_NAME -f 备份文件 gitlabhq_production
			恢复：psql -h 10.1.13.48 -U postgres -d gitlabhq_production -f 备份文件
			
		备份数据库
			备份：pg_dump -h 10.1.13.48 -U postgres -f /postgres.sql  postgres(数据库名)
			恢复：psql -h 10.1.13.48 -U postgres -f /postgres.sql postgres
            
            1、登录数据库
```
/* 切换到数据库用户 */
su - postgres

/* 登录 */
psql
```
登录成功显示如下：
```
bash-4.2$ psql
psql (9.3.17)
Type "help" for help.

postgres=> 
```
2、切换数据库
```
/* 登录指定数据库 */
psql -U user -d dbname

/* 列举数据库 */
\l

/* 切换数据库 */
\c dbname
```
3、用户管理
```
/* 创建用户 */
CREATE ROLE rolename;
CREATE USER username WITH PASSWORD '*****';

/* 显示所有用户 */
\du

/* 修改用户权限 */
ALTER ROLE username WITH privileges;
/* 赋给用户表的所有权限 */
GRANT ALL ON tablename TO user; 
/* 赋给用户数据库的所有权限 */
GRANT ALL PRIVILEGES ON DATABASE dbname TO dbuser;

/* 撤销用户权限 */
REVOKE privileges ON tablename FROM user;


/* 撤销用户权限 */
```
4、数据库操作
```
/* 创建数据库 */
create database dbname; 

/* 删除数据库 */
drop database dbname;  
```
5、表操作
```
/* 增加让主键自增的权限 */
grant all on sequence tablename_keyname_seq to webuser;

 /* 重命名一个表 */
alter table [表名A] rename to [表名B]; 

/* 删除一个表 */
drop table [表名]; 

/* 在已有的表里添加字段 */
alter table [表名] add column [字段名] [类型]; 

/* 删除表中的字段 */
alter table [表名] drop column [字段名]; 

/* 重命名一个字段 */
alter table [表名] rename column [字段名A] to [字段名B]; 

/* 给一个字段设置缺省值 */
alter table [表名] alter column [字段名] set default [新的默认值];

/* 去除缺省值 */
alter table [表名] alter column [字段名] drop default; 

/* 插入数据 */
insert into 表名 ([字段名m],[字段名n],......) values ([列m的值],[列n的值],......); 

/* 修改数据 */
update [表名] set [目标字段名]=[目标值] where ...; 

/* 删除数据 */
delete from [表名] where ...; 

/* 删除表 */
delete from [表名];

/* 查询 */
SELECT * FROM dbname WHERE ...;

/* 创建表 */
create table (
    [字段名1] [类型1] primary key,
    [字段名2] [类型2],
    ......,
    [字段名n] [字段名n] )
```
6、退出
```
\q
quit
```
