---
title: 一组数据表练习Mysql查询
categories: 笔记
tags:
  - 数据库
date: 2023-10-14 15:56:32
---
# 一组数据表练习Mysql查询

## 数据表格式

![image-20231014154116950](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155457883160_747_image-20231014154116950.png)

数据库模式如下（分别为Department,Employee,Category,Project,Workson):

部门（部门号，部门名称，位置）

员工（员工号，姓名，年龄，性别，所在部门号）

项目种类（项目种类号，项目种类名）

项目（项目号，项目名称，预算，项目种类号）

员工工作情况（员工号，项目号，职责，开始日期）

下载地址：

https://github.com/Lunaticsky-tql/SQLQueryPractice

## 某年期末考试题

**一共10道，难度递增。**

1.给出职工中所有男性的所有信息（empid,empname,age,sex,edpid）

```sql
SELECT * FROM employee 
WHERE sex='男'
```

2.统计来自天津的“李”姓职工信息，按年龄降序排序（empid,empname,age,location）

```sql
SELECT empid,empname,age,location
FROM employee,department
WHERE employee.empname LIKE '李%' AND employee.depid =department.depid 
ORDER BY age DESC 
```

![image-20220424163426426](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155503258329_826_image-20220424163426426.png)

3.给出每位职员参与项目的最高预算和最低预算（empname，highestbudget，lowestbudget）

```sql
SELECT empname,MAX (budget) AS higestbudget, MIN (budget) AS lowestbudget
FROM employee ,workson ,project 
WHERE project.proid =workson.proid AND employee.empid=workson.empid
GROUP BY empname
```

![image-20220424163244361](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155506469724_414_image-20220424163244361.png)

4.给出所有项目超过一个的员工的id和参加的项目个数（empid, num）

```sql
select empid,count(proid) as num
from workson
having count(proid)>1
group by empid
```

![image-20220424163912198](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155511552514_152_image-20220424163912198.png)

5.给出项目种类号为“c2”且预算最多的项目。（proid，projectname，budget）

```sql
select proid,projectname,budget
from project
where budget>=all(select budget from project where catid ='c2') and catid='c2'
```

![image-20220424164944185](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155516353726_684_image-20220424164944185.png)

6.给出参加“产品推广”项目，但不担任职位的员工的员工信息，（empid,empname，age,sex.depid）

```sql
select empid,empname,age,sex,depid
from employee
where empid in(select empid from workson where proid=(select proid from project where projectname='产品推广') and job is null)
```

![image-20220424165835471](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155520977072_206_image-20220424165835471.png)

7.给出工号为“10102”的员工每类项目的参加总数，若没有参加过某类项目，则参加项目总数显示为0（catid，proNum）

```sql
select catid,count(workson.proid) as proNum
from project,workson
where empid=10102 and project.proid=workson.proid
group by catid
order by catid
```

![image-20220424172015697](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155524185316_831_image-20220424172015697.png)

但是随后发现这种方式并不能满足”若没有参加过某类项目，则参加项目总数显示为0“的要求。

修改如下：

```sql
select distinct category.catid ,isnull(subtable.subNum) as proNum
from category left join (select catid,count(workson.proid) as subNum
from project,workson
where empid=10211 and project.proid=workson.proid
group by catid) as subtable
on category.catid=subtable.catid
```

以10211为例进行了测试：成功。

![image-20220424212513530](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155528947182_726_image-20220424212513530.png)

[参考链接](https://blog.csdn.net/evasunny2008/article/details/52525196?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_default&utm_relevant_index=1)

> distinct操作往往比较耗费性能。

8.给出没有参与“软件类”项目女性职工的信息（empid,empname, age,sex,depid)

```sql
SELECT *
FROM employee
WHERE sex = '女'
	AND NOT EXISTS (
		SELECT *
		FROM workson
		WHERE empid = employee.empid
			AND proid IN (
				SELECT proid
				FROM project
				WHERE catid = (
					SELECT catid
					FROM category
					WHERE catname = '软件类'
				)
			)
	)
```

刚刚发现了格式化的功能。

![image-20220424214552653](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155533441829_214_image-20220424214552653.png)

9.给出有30岁以上男性员工的省份名称和该省男员工最大年龄，结果按最大年龄升序排序

```sql
SELECT location, MAX(age)
FROM department, employee
WHERE department.depid = employee.depid
	AND sex = '男'
GROUP BY location
HAVING MAX(age) > 30
ORDER BY MAX(age)
```

![image-20220424221636001](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155538165850_847_image-20220424221636001.png)

10.给出在广州工作的、参加“'产品推广'”项目的职员id、姓名及他们参加的项目个数（empid, empname, procnt）

```sql
SELECT employee.empid, empname, count(workson.proid) AS procnt
FROM project, employee, workson, department
WHERE location = '广州'
	AND projectname = '产品推广'
	AND department.depid = employee.depid
	AND workson.proid = project.proid
	AND employee.empid = workson.empid
GROUP BY employee.empid
```

![image-20220424223306078](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155542227505_244_image-20220424223306078.png)

---

## 补充题目

**根据数据库课程讲述内容和网上资料进行整理，往往是比较容易遗忘或犯错的地方，难度不一。标\*的题目有超出课程范围内容。**

1.隶属同一部门的员工对。(name1,name2)

```sql
select e1.empname as name1,e2.empname as name2
from employee e1,employee e2 where e1.depid=e2.depid and e1.empname<e2.empname
```

> 利用小于关系去重

![image-20231012203847118](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155547176726_653_image-20231012203847118.png)

2. 查找部门中只有一名员工的员工姓名(empname)

```sql
select empname
from employee e1
where not exists (select * from employee
where depid=e1.depid and empname<>e1.empname)
```

![image-20231012205231700](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155550880799_733_image-20231012205231700.png)

3. 2020年12月21日之后入职的员工所参与项目的平均预算（empid，avgngbudget）

```sql
select empid,avg(budget) as avgbudget
from workson,project
where workson.proid=project.proid 
and enterdate >'2020-12-21 00:00'
group by empid
```

![image-20231012212055411](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155555162156_749_image-20231012212055411.png)

4. 如果担任过职员的员工所参与的所有项目的平均预算大于110000则返回结果为职员的名字(empname)，与对应的平均项目预算值avg(budget)

```sql
select empname,avg(budget)
from employee natural join workson natural join project 
where empid in (select empid from workson where job='职员') 
group by empname
having avg(budget)>110000;
```

![image-20231012212759491](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155559791125_456_image-20231012212759491.png)

> 典型错误：
>
> ````sql
> select empname,avg(budget)
> from employee natural join workson natural join project 
> where job='职员'
> group by empname
> having avg(budget)>110000;
> ````
>
> ![image-20231012212955932](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155604301445_444_image-20231012212955932.png)
>
> 错误原因：这时候avg只计算了参与角色为职员的项目。

5. \*找出每个部门预算前两名的项目，前两名指**不同** 预算中 **排名前两名**，若部门少于两个项目，返回部门内所有项目。（catname,projectname,budget）。

```sql
   select catname,projectname,budget from project p1 join category c on p1.catid=c.catid
   where 
   2>(select count(distinct p2.budget)
   	from project p2 
   	where p1.budget<p2.budget and p1.catid=p2.catid)
```

![image-20231014141406527](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155607606479_529_image-20231014141406527.png)

> 注：这是经典的分组TopK问题。
>
> 分解子任务为在project表中找每个catid中排名前三的project。
>
> 对于这个子问题，用到了相关子查询的技巧。
>
> 将project表克隆一份，在原表上遍历，判断是否有大于两个部门的预算大于它。最后与category 连接即可。
>
> MySQL8之后可以使用窗口函数完成类似的功能，可以参见[这篇文章](https://www.zhihu.com/tardis/zm/art/92654574?source_id=1003)学习。

窗口函数的做法：

```sql
select catname,projectname,budget,
dense_rank() over(partition by c.catid order by budget desc)
from category c join project p on c.catid=p.catid
```

![image-20231014142403857](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155610257288_208_image-20231014142403857.png)

最终得到可行SQL语句：

```sql
select t.catname,t.projectname,t.budget from
(select catname,projectname,budget,
dense_rank() over(partition by c.catid order by budget desc) as rk
from category c join project p on c.catid=p.catid) t
where t.rk<=2
```

6. \*找出每个部门项目预算的中位数，若有两个中间数，返回两者而非取平均值。（catname,projectname,budget）。

本题目较容易理解的方法需要掌握上一个题目中提到的窗口函数。当然也有其他解法，但较繁琐或使用较多其他的内置函数。下面对使用窗口函数的方法进行讲解。

总的思路是利用中位数在排序中的位次关系求解。

```sql
select 
catname,projectname,budget,
row_number() over(partition by catid order by budget) as rk,
count(proid) over(partition by catid) as n
from category c natural join project p
```

使用`partion_by`分组统计每一部门的排名，并使用`count`得出该部门的部门数，方便后续筛选。

得到下面的中间结果。

![image-20231014150850190](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155615661381_775_image-20231014150850190.png)

作为中位数，其rank应位于`[n/2,n/2+1]`之间。

比较违反编程直觉的是，MySQL中除法是浮点数除法，例如有三个元素，区间为`[1.5,2.5]`,有四个元素，区间为`[2,3]`。可以看到奇数时包含一个元素，偶数时包含两个元素，符合题目要求。

最终得到可行SQL如下：

```sql
select catname,projectname,budget
from
(select 
catname,projectname,budget,
row_number() over(partition by catid order by budget) as rk,
count(proid) over(partition by catid) as n
from category c natural join project p
)t
where rk>=n/2 and rk<=n/2+1
```

![image-20231014152206322](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155619109089_940_image-20231014152206322.png)

7. 查找每个项目类别超过其内项目平均预算的项目？（catname，projectname)

有了TopK问题解法一的基础，就很容易想到用相关子查询来做了。

对于这个题来说，相当于先在x表内找到对应的项目类别，再在子查询中返回该类别中的项目平均预算，最后回到父查询得到该类别中大于平均预算的项目。类似于二重循环。

```sql
select catname,projectname
from project x natural join category c
where budget >=(select avg(budget)
                from project y
                where y.catid =x.catid 
               group by y.catid )
```

![image-20231014153658251](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155623802818_678_image-20231014153658251.png)

8. 参与过所有项目的员工的姓名（empname）。

```sql
select empname from employee
where not exists(select * from project 
                 where not exists (select * from workson
                                   where empid=employee.empid and proid=project.proid))
```

![image-20231014155355539](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%B8%80%E7%BB%84%E6%95%B0%E6%8D%AE%E8%A1%A8%E7%BB%83%E4%B9%A0Mysql%E6%9F%A5%E8%AF%A2/20231014155627876393_620_image-20231014155355539.png)
