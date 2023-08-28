---
title: 数据库系统期末工程作业设计
categories: 作业
date: 2022-6-30 10:00:00
tags: 数据库
abbrlink: 30344
---
### 期末工程作业



<p class="note note-info">本文暂只提供相关设计思路，不提供最终实现代码。实现方面前端flask或swing上手较为快速，也可尝试其他框架。后端使用mysql数据库，关于连接数据库方式网上很容易搜到，不再赘述。</p>

#### 1. 需求描述

疫情期间，学校的润美超市（虚构）需要对商品物资做更详细的管理。为防止供应链出现问题，对商品的供货商需要进行详细的记录，并对顾客的购买记录进行管理。当然，也需要对商品本身和超市内工作人员进行常规的管理。作为典型的数据库应用场景，引入合适的数据管理系统能够更好的落实疫情防控要求，并让超市具有更好的营业效果。

1.商品根据名称和供应商整理，通过编号标识，记录其价格。同时对于食品还需记录其保质期，以免过期未处理。

2.进货数据需要包含商品编号、进货价，进货时间等。

3.超市内有若干工作人员，需要对其个人信息和销售商品所得薪水进行储存。

4.需要对顾客信息进行储存。并对应购买时间和商品，形成销售日志。

#### 2.1 概念模型ER图

![image-20220919004148336](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%95%B0%E6%8D%AE%E5%BA%93%E7%B3%BB%E7%BB%9F%E6%9C%9F%E6%9C%AB%E5%B7%A5%E7%A8%8B%E4%BD%9C%E4%B8%9A%E8%AE%BE%E8%AE%A1/20230828211224660894_271_20220919004325018293_610_image-20220919004148336.png)

#### 2.2 关系模式转换

注：1.普通商品采用使用空值的方式，food与goods共用一张表

​		2.斜体代表外键

goods（<u>goods_id</u>, goods_name, supplier_id, price, good_num, *shelf_no*)

//food（<u>goods_id</u>, goods_name, supplier_id, price, shelf_life)

supplier（<u>sp_id</u>, sp_name, phone, address)

supply（<u>*sp_id*</u>, <u>*goods_id*</u>, enter_time, costs)

employee（<u>emp_no</u>, <u>emp_name</u>, salary)

customer（<u>cu_id</u>, cu_name)

buy(<u>*cu_id*</u>, <u>*goods_id*</u>, buy_time, buy_costs)

shelf(<u>shelf_id</u>, goods_num_on_shelf)

sell (<u>*emp_no*</u>, *<u>goods_id</u>*)



#### 2.3 SQL创建关系模式

```sql
create table goods 
(
   goods_id             integer                        not null,
   shelf_id             integer                        not null,
   goods_name           varchar(10)                    not null,
   price                integer                        not null,
   goods_num            integer                        not null,
   shell_life           timestamp                      null,
   constraint PK_GOODS primary key (goods_id)
);

alter table goods
   add constraint FK_GOODS_ON_SHELF foreign key (shelf_id)
      references shelf (shelf_id)
      on update restrict
      on delete restrict;

create table supplier 
(
   sp_id                integer                        not null,
   sp_name              varchar(10)                    not null,
   address              varchar(10)                    not null,
   phone                char(11)                       not null,
   constraint PK_SUPPLIER primary key (sp_id)
);

create table supply 
(
   goods_id             integer                        not null,
   sp_id                integer                        not null,
   enter_time           timestamp                      not null,
   costs                integer                        not null,
   constraint PK_SUPPLY primary key clustered (goods_id, sp_id)
);

create table customer 
(
   cu_id                integer                        not null,
   cu_name              varchar(4)                     not null,
   constraint PK_CUSTOMER primary key (cu_id)
);

create table shelf 
(
   shelf_id             integer                        not null,
   goods_num_on_shelf   integer                        not null,
   constraint PK_SHELF primary key (shelf_id)
);

create table employee 
(
   emp_name             varchar(4)                     not null,
   emp_no               integer                        not null,
   salary               integer                        null,
   constraint PK_EMPLOYEE primary key (emp_no)
);

create table buy 
(
   cu_id                integer                        not null,
   goods_id             integer                        not null,
   buy_time             timestamp                      null,
   buy_costs            integer                        null,
   constraint PK_BUY primary key clustered (cu_id, goods_id)
);

alter table buy
   add constraint FK_BUY_BUY_CUSTOMER foreign key (cu_id)
      references customer (cu_id)
      on update restrict
      on delete restrict;



create table sell 
(
   emp_no               integer                        not null,
   goods_id             integer                        not null,
   constraint PK_SELL primary key clustered (emp_no, goods_id)
);

alter table sell
   add constraint FK_SELL_SELL_EMPLOYEE foreign key (emp_no)
      references employee (emp_no)
      on update restrict
      on delete restrict;

alter table sell
   add constraint FK_SELL_SELL2_GOODS foreign key (goods_id)
      references goods (goods_id)
      on update restrict
      on delete restrict;
```

#### 2.4 查询语句样例

1.单表查询

查询单价为10元的商品名称

```sql
select goods_name 
from goods
where price=10
```

2.多表连接查询

查询每个厂商生产商品的平均价格

```SQL
select sp_id,avg(price)
from supply natural join goods
group by sp_id
```



3.4多表嵌套查询和exist查询

查询只有一种商品的货架，返回这种商品的名称和货架id

```sql
select goods_name,shelf_id
from goods,shelf
where goods.shelf_id=shelf.shelf_id and goods.goods_num=shelf.goods_num_on_shelf
```

也可以只在goods表中查

```sql
select goods_name
from goods g1
where not exists (select
*
from goods
where shelf.id=e1.shelf.id and
goods_name<>e1.goods_name);
```

5.聚合查询

有10种以上商品的货架，以及拥有的商品种类数

```sql
select shelf_id,count(*)
from goods
group by shef_id
having count(*)>10;
```



#### 3.1 PowerDesigner 绘制ER图





![image-20220415222750452](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%95%B0%E6%8D%AE%E5%BA%93%E7%B3%BB%E7%BB%9F%E6%9C%9F%E6%9C%AB%E5%B7%A5%E7%A8%8B%E4%BD%9C%E4%B8%9A%E8%AE%BE%E8%AE%A1/20230828211230228848_283_20220919004326633367_468_image-20220415222750452.png)

#### 3.2 转为关系模型

![image-20220415222820109](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%95%B0%E6%8D%AE%E5%BA%93%E7%B3%BB%E7%BB%9F%E6%9C%9F%E6%9C%AB%E5%B7%A5%E7%A8%8B%E4%BD%9C%E4%B8%9A%E8%AE%BE%E8%AE%A1/20230828211231407880_506_20220919004327928426_899_image-20220415222820109.png)

#### 3.3 生成SQL语句

```sql
/*==============================================================*/
/* DBMS name:      Sybase SQL Anywhere 12                       */
/* Created on:     2022/4/15 22:28:49                           */
/*==============================================================*/


if exists(select 1 from sys.sysforeignkey where role='FK_BUY_BUY_CUSTOMER') then
    alter table buy
       delete foreign key FK_BUY_BUY_CUSTOMER
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_BUY_BUY2_GOODS') then
    alter table buy
       delete foreign key FK_BUY_BUY2_GOODS
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_GOODS_ON_SHELF') then
    alter table goods
       delete foreign key FK_GOODS_ON_SHELF
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SELL_SELL_EMPLOYEE') then
    alter table sell
       delete foreign key FK_SELL_SELL_EMPLOYEE
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SELL_SELL2_GOODS') then
    alter table sell
       delete foreign key FK_SELL_SELL2_GOODS
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SUPPLY_SUPPLY_GOODS') then
    alter table supply
       delete foreign key FK_SUPPLY_SUPPLY_GOODS
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SUPPLY_SUPPLY2_SUPPLIER') then
    alter table supply
       delete foreign key FK_SUPPLY_SUPPLY2_SUPPLIER
end if;

drop index if exists buy.buy2_FK;

drop index if exists buy.buy_FK;

drop index if exists buy.buy_PK;

drop table if exists buy;

drop index if exists customer.customer_PK;

drop table if exists customer;

drop index if exists employee.emplyer_PK;

drop table if exists employee;

drop index if exists goods.on_FK;

drop index if exists goods.goods_PK;

drop table if exists goods;

drop index if exists sell.sell2_FK;

drop index if exists sell.sell_FK;

drop index if exists sell.sell_PK;

drop table if exists sell;

drop index if exists shelf.shelf_PK;

drop table if exists shelf;

drop index if exists supplier.supplier_PK;

drop table if exists supplier;

drop index if exists supply.supply2_FK;

drop index if exists supply.supply_FK;

drop index if exists supply.supply_PK;

drop table if exists supply;

/*==============================================================*/
/* Table: buy                                                   */
/*==============================================================*/
create table buy 
(
   cu_id                integer                        not null,
   goods_id             integer                        not null,
   buy_time             timestamp                      null,
   buy_costs            integer                        null,
   constraint PK_BUY primary key clustered (cu_id, goods_id)
);

/*==============================================================*/
/* Index: buy_PK                                                */
/*==============================================================*/
create unique clustered index buy_PK on buy (
cu_id ASC,
goods_id ASC
);

/*==============================================================*/
/* Index: buy_FK                                                */
/*==============================================================*/
create index buy_FK on buy (
cu_id ASC
);

/*==============================================================*/
/* Index: buy2_FK                                               */
/*==============================================================*/
create index buy2_FK on buy (
goods_id ASC
);

/*==============================================================*/
/* Table: customer                                              */
/*==============================================================*/
create table customer 
(
   cu_id                integer                        not null,
   cu_name              varchar(4)                     not null,
   constraint PK_CUSTOMER primary key (cu_id)
);

/*==============================================================*/
/* Index: customer_PK                                           */
/*==============================================================*/
create unique index customer_PK on customer (
cu_id ASC
);

/*==============================================================*/
/* Table: employee                                              */
/*==============================================================*/
create table employee 
(
   emp_name             varchar(4)                     not null,
   emp_no               integer                        not null,
   salary               integer                        null,
   constraint PK_EMPLOYEE primary key (emp_no)
);

/*==============================================================*/
/* Index: emplyer_PK                                            */
/*==============================================================*/
create unique index emplyer_PK on employee (
emp_no ASC
);

/*==============================================================*/
/* Table: goods                                                 */
/*==============================================================*/
create table goods 
(
   goods_id             integer                        not null,
   shelf_id             integer                        not null,
   goods_name           varchar(10)                    not null,
   price                integer                        not null,
   goods_num            integer                        not null,
   shell_life           timestamp                      null,
   constraint PK_GOODS primary key (goods_id)
);

/*==============================================================*/
/* Index: goods_PK                                              */
/*==============================================================*/
create unique index goods_PK on goods (
goods_id ASC
);

/*==============================================================*/
/* Index: on_FK                                                 */
/*==============================================================*/
create index on_FK on goods (
shelf_id ASC
);

/*==============================================================*/
/* Table: sell                                                  */
/*==============================================================*/
create table sell 
(
   emp_no               integer                        not null,
   goods_id             integer                        not null,
   constraint PK_SELL primary key clustered (emp_no, goods_id)
);

/*==============================================================*/
/* Index: sell_PK                                               */
/*==============================================================*/
create unique clustered index sell_PK on sell (
emp_no ASC,
goods_id ASC
);

/*==============================================================*/
/* Index: sell_FK                                               */
/*==============================================================*/
create index sell_FK on sell (
emp_no ASC
);

/*==============================================================*/
/* Index: sell2_FK                                              */
/*==============================================================*/
create index sell2_FK on sell (
goods_id ASC
);

/*==============================================================*/
/* Table: shelf                                                 */
/*==============================================================*/
create table shelf 
(
   shelf_id             integer                        not null,
   goods_num_on_shelf   integer                        not null,
   constraint PK_SHELF primary key (shelf_id)
);

/*==============================================================*/
/* Index: shelf_PK                                              */
/*==============================================================*/
create unique index shelf_PK on shelf (
shelf_id ASC
);

/*==============================================================*/
/* Table: supplier                                              */
/*==============================================================*/
create table supplier 
(
   sp_id                integer                        not null,
   sp_name              varchar(10)                    not null,
   address              varchar(10)                    not null,
   phone                char(11)                       not null,
   constraint PK_SUPPLIER primary key (sp_id)
);

/*==============================================================*/
/* Index: supplier_PK                                           */
/*==============================================================*/
create unique index supplier_PK on supplier (
sp_id ASC
);

/*==============================================================*/
/* Table: supply                                                */
/*==============================================================*/
create table supply 
(
   goods_id             integer                        not null,
   sp_id                integer                        not null,
   enter_time           timestamp                      not null,
   costs                integer                        not null,
   constraint PK_SUPPLY primary key clustered (goods_id, sp_id)
);

/*==============================================================*/
/* Index: supply_PK                                             */
/*==============================================================*/
create unique clustered index supply_PK on supply (
goods_id ASC,
sp_id ASC
);

/*==============================================================*/
/* Index: supply_FK                                             */
/*==============================================================*/
create index supply_FK on supply (
goods_id ASC
);

/*==============================================================*/
/* Index: supply2_FK                                            */
/*==============================================================*/
create index supply2_FK on supply (
sp_id ASC
);

alter table buy
   add constraint FK_BUY_BUY_CUSTOMER foreign key (cu_id)
      references customer (cu_id)
      on update restrict
      on delete restrict;

alter table buy
   add constraint FK_BUY_BUY2_GOODS foreign key (goods_id)
      references goods (goods_id)
      on update restrict
      on delete restrict;

alter table goods
   add constraint FK_GOODS_ON_SHELF foreign key (shelf_id)
      references shelf (shelf_id)
      on update restrict
      on delete restrict;

alter table sell
   add constraint FK_SELL_SELL_EMPLOYEE foreign key (emp_no)
      references employee (emp_no)
      on update restrict
      on delete restrict;

alter table sell
   add constraint FK_SELL_SELL2_GOODS foreign key (goods_id)
      references goods (goods_id)
      on update restrict
      on delete restrict;

alter table supply
   add constraint FK_SUPPLY_SUPPLY_GOODS foreign key (goods_id)
      references goods (goods_id)
      on update restrict
      on delete restrict;

alter table supply
   add constraint FK_SUPPLY_SUPPLY2_SUPPLIER foreign key (sp_id)
      references supplier (sp_id)
      on update restrict
      on delete restrict;


```



#### 4.1 分析差异

有差异。PowerDesigner会事先判断外键约束、索引以及表本身是否存在，若存在会删除。同时也会对表建立索引。但是基本逻辑是一致的，在总体的设计上不会造成影响。

#### 4.2 语句特点

从4.1的分析可以看出，PowerDesigner生成的语句更严谨。当然，语句顺序比如外键约束声明的位置也有不同。这些附加语句的作用是防止特殊情况的发生导致无法正常建立表。