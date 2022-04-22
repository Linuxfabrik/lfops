# The MariaDB sys schema

from https://github.com/good-dba/mariadb-sys



## Comment

This schema was written by getting an idea from The MySQL sys schema (https://github.com/mysql/mysql-sys).

But all scripts have been written by myself, it did not use The MySQL sys schema.

A collection of views to help MariaDB administrators get insight in to MariaDB Database usage.

There are install files available for over MariaDB 10.0.x. To load these, you must position yourself within the directory that you downloaded to.

* Caution

The most of views are for any users, but the views of the suffix "_kr" are only for Korean users.

## Installation

The objects should all be created as the root user (but run with the privileges of the invoker).

For instance if you download to /tmp/mariadb-sys/, and want to install the schema you should:

```
cd /tmp/mariadb-sys/
mysql -u root -p < ./mariadb_sys_install.sql
```

Or if you would like to log in to the client, and install the schema:

```
cd /tmp/mariadb-sys/
mysql -u root -p
SOURCE ./mariadb_sys_install.sql
```

## Overview of objects

### db_all_objects

#### Description

List of all objects within all schemas

#### Structures

```
MariaDB [(none)]> desc sys.db_all_objects;
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| schema_name | varchar(64)  | NO   |     |         |       |
| object_type | varchar(64)  | YES  |     | NULL    |       |
| object_name | varchar(130) | YES  |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+
```

#### Example

```
MariaDB [sys]> select * from db_all_objects;
+--------------------+-------------+---------------------------------------+
| schema_name        | object_type | object_name                           |
+--------------------+-------------+---------------------------------------+
| information_schema | SYSTEM VIEW | ALL_PLUGINS                           |
| information_schema | SYSTEM VIEW | APPLICABLE_ROLES                      |
...
| sys                | INDEX(BTREE) | PRIMARY(workload_sql_text)           |
| sys                | PROCEDURE    | workload_proc_run_snapshot           |
| sys                | EVENT        | workload_event_schedule              |
+--------------------+-------------+---------------------------------------+
```

### db_user_privileges

#### Description

List of all user's privileges

#### Structures

```
MariaDB [(none)]> desc sys.db_user_privileges;
+----------------+--------------+------+-----+---------+-------+
| Field          | Type         | Null | Key | Default | Extra |
+----------------+--------------+------+-----+---------+-------+
| table_catalog  | varchar(512) | NO   |     |         |       |
| table_schema   | varchar(64)  | NO   |     |         |       |
| table_name     | varchar(64)  | NO   |     |         |       |
| table_type     | varchar(64)  | NO   |     |         |       |
| grantee        | varchar(190) | NO   |     |         |       |
| privilege_type | varchar(64)  | NO   |     |         |       |
| is_grantable   | varchar(3)   | NO   |     |         |       |
+----------------+--------------+------+-----+---------+-------+
```

#### Example

```
MariaDB [sys]> select * from db_user_privileges;
+---------------+--------------+---------------------------+------------+--------------------+----------------+--------------+
| table_catalog | table_schema | table_name                | table_type | grantee            | privilege_type | is_grantable |
+---------------+--------------+---------------------------+------------+--------------------+----------------+--------------+
| def           | sys          | db_all_objects            | VIEW       | 'root'@'localhost' | SELECT         | YES          |
| def           | sys          | db_user_privileges        | VIEW       | 'root'@'localhost' | SELECT         | YES          |
...
| def           | sys          | v$threads                 | VIEW       | 'root'@'localhost' | SELECT         | YES          |
+---------------+--------------+---------------------------+------------+--------------------+----------------+--------------+
```

### v$db_health_check

#### Description

MariaDB health check - Key Item

This view for everyone but the "description_kr" is only for Korean.

#### Structures

```
MariaDB [(none)]> desc sys.v$db_health_check;
+-----------------+--------------+------+-----+---------+-------+
| Field           | Type         | Null | Key | Default | Extra |
+-----------------+--------------+------+-----+---------+-------+
| category        | varchar(15)  | NO   |     |         |       |
| division        | varchar(29)  | NO   |     |         |       |
| current_percent | double(18,1) | YES  |     | NULL    |       |
| state           | varchar(8)   | YES  |     | NULL    |       |
| description_kr  | varchar(109) | NO   |     |         |       |
+-----------------+--------------+------+-----+---------+-------+
```

#### Example

```
MariaDB [sys]> select * from v$db_health_check;
+-----------------+-------------------------------+-----------------+----------+---------------------------------------------------------+
| category        | division                      | current_percent | state    | description_kr                                          |
+-----------------+-------------------------------+-----------------+----------+---------------------------------------------------------+
| Connection      | Refued Connection             |            99.8 | Critical | 연결 실패 비율                                          |
| Connection      | Connection Usage              |            44.8 | NULL     | 동시 접속이 가능한 최대 수치 대비 연결된 Thread의 비율  |
...
| Open Files      | Open Files Ratio              |             0.2 | NULL     | 파일 오픈 비율                                          |
+-----------------+-------------------------------+-----------------+----------+---------------------------------------------------------+
```

### v$global_status_kr

#### Description

Same as information_schema.global_status but include Korean description.

#### Structures

```
MariaDB [(none)]> desc sys.v$global_status_kr;
+------------------+---------------+------+-----+---------+-------+
| Field            | Type          | Null | Key | Default | Extra |
+------------------+---------------+------+-----+---------+-------+
| variable_name    | varchar(64)   | NO   |     |         |       |
| variable_value   | varchar(1024) | YES  |     | NULL    |       |
| variable_desc_kr | varchar(131)  | YES  |     | NULL    |       |
+------------------+---------------+------+-----+---------+-------+
```

#### Example

```
MariaDB [sys]> select * from v$global_status_kr;
+-------------------+----------------+------------------------------------------------------------------------------+
| variable_name     | variable_value | variable_desc_kr                                                             |
+-------------------+----------------+------------------------------------------------------------------------------+
| ABORTED_CLIENTS   | 69             | 연결을 닫지 않고 클라이언트가 죽어서 중지된 연결의 수                        |
| ABORTED_CONNECTS  | 303382         | MySQL 서버에 연결 실패한 횟수                                                |
...
| COM_INSERT_SELECT | 22305          | INSERT ... SELECT ... 쿼리 실행횟수                                          |
| COM_LOAD          | 0              | LOAD 쿼리 실행횟수                                                           |
+-------------------+----------------+------------------------------------------------------------------------------+
```

### v$innodb_lock ★

#### Description

Current InnoDB row level lock

If you want to kill thread, you can referenced the "kill_thread" column.

Only the top-level lock is displayed as the holder. The rest threads are displayed as waiters.

If kill the top-level lock, the top-level lock in the rest threads will become the holder.

#### Structures

```
MariaDB [(none)]> desc sys.v$innodb_lock;
+---------------------------+---------------------+------+-----+---------------------+-------+
| Field                     | Type                | Null | Key | Default             | Extra |
+---------------------------+---------------------+------+-----+---------------------+-------+
| thread_id                 | varchar(25)         | YES  |     | NULL                |       |
| thread_status             | varchar(16)         | NO   |     |                     |       |
| trx_state                 | varchar(13)         | NO   |     |                     |       |
| trx_started               | datetime            | NO   |     | 0000-00-00 00:00:00 |       |
| trx_wait_started          | datetime            | YES  |     | NULL                |       |
| wait_secs                 | bigint(21)          | YES  |     | NULL                |       |
| lock_type                 | varchar(67)         | YES  |     | NULL                |       |
| lock_table                | varchar(1024)       | YES  |     |                     |       |
| lock_index                | varchar(1024)       | YES  |     | NULL                |       |
| trx_query                 | varchar(1024)       | YES  |     | NULL                |       |
| trx_operation_state       | varchar(64)         | YES  |     | NULL                |       |
| waiting_trx_rows_locked   | bigint(21) unsigned | NO   |     | 0                   |       |
| waiting_trx_rows_modified | bigint(21) unsigned | NO   |     | 0                   |       |
| trx_lock_memory_bytes     | bigint(21) unsigned | NO   |     | 0                   |       |
| kill_thread               | varchar(26)         | YES  |     | NULL                |       |
+---------------------------+---------------------+------+-----+---------------------+-------+
```

#### Example

### v$meta_lock ★

#### Description

Current Metadata lock info

If you want to kill thread, you can referenced the "kill_thread" column.

#### Structures

```
MariaDB [(none)]> desc sys.v$meta_lock;
+--------------------+--------------+------+-----+---------+-------+
| Field              | Type         | Null | Key | Default | Extra |
+--------------------+--------------+------+-----+---------+-------+
| schema_name        | varchar(64)  | YES  |     | NULL    |       |
| object_name        | varchar(64)  | YES  |     | NULL    |       |
| meta_lock_type     | varchar(30)  | YES  |     | NULL    |       |
| meta_lock_mode     | varchar(24)  | YES  |     | NULL    |       |
| meta_lock_duration | varchar(30)  | YES  |     | NULL    |       |
| thread_id          | bigint(4)    | YES  |     | 0       |       |
| user               | varchar(193) | YES  |     | NULL    |       |
| thread_status      | varchar(16)  | YES  |     |         |       |
| thread_time_sec    | int(7)       | YES  |     | 0       |       |
| thread_info        | longtext     | YES  |     | NULL    |       |
| kill_thread        | varchar(25)  | YES  |     | NULL    |       |
+--------------------+--------------+------+-----+---------+-------+
```

#### Example

```
MariaDB [sys]> select * from v$meta_lock;
+-------------+-------------------+-----------------+------------------+--------------------+-----------+--------------------+---------------+-----------------+---------------------------+-------------+
| schema_name | object_name       | meta_lock_type  | meta_lock_mode   | meta_lock_duration | thread_id | user               | thread_status | thread_time_sec | thread_info               | kill_thread |
+-------------+-------------------+-----------------+------------------+--------------------+-----------+--------------------+---------------+-----------------+---------------------------+-------------+
| sys         | v$meta_lock       | Table           | MDL_SHARED_READ  | MDL_TRANSACTION    |    303860 | root@localhost     | Query         |               0 | select * from v$meta_lock | KILL 303860 |
+-------------+-------------------+-----------------+------------------+--------------------+-----------+--------------------+---------------+-----------------+---------------------------+-------------+
```

### v$threads ★

#### Description

Current all threads

#### Structures

```
MariaDB [(none)]> desc sys.v$threads;
+-------------------+---------------------+------+-----+---------+-------+
| Field             | Type                | Null | Key | Default | Extra |
+-------------------+---------------------+------+-----+---------+-------+
| thread_id         | bigint(4)           | NO   |     | 0       |       |
| user              | varchar(197)        | YES  |     | NULL    |       |
| schema_name       | varchar(64)         | YES  |     | NULL    |       |
| thread_status     | varchar(16)         | NO   |     |         |       |
| thread_sec        | int(7)              | NO   |     | 0       |       |
| memory_used       | int(7)              | NO   |     | 0       |       |
| thread_state      | varchar(64)         | YES  |     | NULL    |       |
| thread_info       | longtext            | YES  |     | NULL    |       |
| trx_existence     | varchar(3)          | NO   |     |         |       |
| trx_id            | varchar(18)         | YES  |     |         |       |
| trx_rows_modified | bigint(21) unsigned | YES  |     | 0       |       |
| lock_wait_sec     | bigint(21)          | YES  |     | NULL    |       |
| lock_table        | varchar(1024)       | YES  |     |         |       |
| lock_index        | varchar(1024)       | YES  |     | NULL    |       |
| lock_type         | varchar(32)         | YES  |     |         |       |
+-------------------+---------------------+------+-----+---------+-------+
```

#### Example

```
MariaDB [sys]> select * from v$threads;
+-----------+-------------------------------+-------------+---------------+------------+-------------+-----------------------------+-------------------------+---------------+--------+-------------------+---------------+------------+------------+-----------+
| thread_id | user                          | schema_name | thread_status | thread_sec | memory_used | thread_state                | thread_info             | trx_existence | trx_id | trx_rows_modified | lock_wait_sec | lock_table | lock_index | lock_type |
+-----------+-------------------------------+-------------+---------------+------------+-------------+-----------------------------+-------------------------+---------------+--------+-------------------+---------------+------------+------------+-----------+
|       368 | `root`@`localhost`            | sys         | Query         |          0 |      844672 | Filling schema table        | select * from v$threads | NO            | NULL   |              NULL |          NULL | NULL       | NULL       | NULL      |
...
|         2 | `event_scheduler`@`localhost` | NULL        | Daemon        |        149 |       44280 | Waiting for next activation | NULL                    | NO            | NULL   |              NULL |          NULL | NULL       | NULL       | NULL      |
+-----------+-------------------------------+-------------+---------------+------------+-------------+-----------------------------+-------------------------+---------------+--------+-------------------+---------------+------------+------------+-----------+
```

---

# The MariaDB sys schema

## 비고

이 스키마는 MySQL sys 스키마에서 아이디어를 얻어서 작성됐지만, 모두 제가 직접 작성한 것 입니다.

이 스키마는 MariaDB 10.0.x 이상에서 사용 가능하며, 설치할 때는 소스가 위치한 경로에서 설치를 실행해야 합니다.

* 주의

접미어가 "_kr"인 뷰는 한국인만을 위한 뷰입니다.

## 설치

오브젝트들은 root 사용자로 생성되어야 합니다. (단, 실행할 때는 invoker 권한을 사용합니다.)

설치 방법은 영문설명의 Installation 부분을 참고합니다.

## 오브젝트 개요

각 오브젝트의 구조 및 샘플은 상단의 영문 설명을 참고 하십시오.

### db_all_objects

#### 설명

DB에 있는 모든 오브젝트 목록

### db_user_privileges

#### 설명

모든 사용자의 권한 현황

### v$db_health_check

#### 설명

MariaDB 주요 헬스체크

### v$global_status_kr

#### 설명

information_schema.global_status와 동일한데, 한국어 설명을 추가한 것입니다.

### v$innodb_lock ★

#### 설명

InnoDB에 있는 row level lock 현황

모든 잠금이 계단식으로 표현되는 것은 아니며, 가장 최상위 잠금만 holder로 표시됩니다.

만약 최상위 잠금을 죽이고, 다음 최상위 잠금이 holder로 바뀝니다.

### v$meta_lock ★

#### 설명

메타데이터 잠금 현황

### v$threads ★

#### 설명

모든 쓰레드 현황
