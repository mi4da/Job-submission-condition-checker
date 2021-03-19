# Job submission condition checker
 Auto-checks a class's homeworks.
# Befor use:
you should check your envrionment like this:
 python3.6+
 mysql5.6+
 pymysql
# and befor ro use. You must verify your mysql serve were OPOENED.
## How to use
- In your Terminal enter this to merge 2 tables(on universal case, your classmates aren't all in one lesson, 
so, I should find which students both in my class and in this lesson. then this command well create a table in your mysql-database):
python main.py --merge \[lessonlist_filepath\] \[classlist_filepath\]
>>>merge begin!
>>>merge end!

- In your Terminal enter this to get names who don't submits homeworks to you.(Must verify your Mysql-database already has a null-table to check)
python main.py --check \[Already_Submits_list_filepath\] 
>>> check begin!
>>> (name1,name2)
>>> check end!



