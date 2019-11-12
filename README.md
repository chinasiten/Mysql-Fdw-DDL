# Mysql-Fdw-DDL
generate ddl for mysql_fdw


when i use mysql_fdw ,i find create foreign table is pretty annoying,especially when your mysql table have more than ten columns or you need to create foreign table in your program.so i wrote this simple script to help  generate ddl ~


Installation
------------
```bash

pip install mysql-fdw-ddl
```

Usage
-----

```python

   from mysql_fdw_ddl import MysqlFdwDDL
   m=MysqlFdwDDL(url='mysql+pymysql://xxx:xxx@xxxx/xxxxx?charset=utf8', #sqlalchemy url,
   	             table_name='dl_tag', #table name,
   	             server_name='tidb',  #the fdw server you created,
   	             dbname='loandb'      #mysql database name 
   	             )
   print(m.get_create_statment())
```

will generate 


```sql
CREATE FOREIGN TABLE loandb.dl_tag (
	id integer, 
	name varchar, 
	value varchar, 
	type integer) server tidb OPTIONS (dbname 'loandb', table_name 'dl_tag');
```

which orignal ddl is:
```sql
CREATE TABLE `dl_tag` (
  `id` tinyint(2) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '标签名称',
  `value` varchar(64) DEFAULT NULL,
  `type` tinyint(2) NOT NULL COMMENT '1:单选 2:多选',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8
```

