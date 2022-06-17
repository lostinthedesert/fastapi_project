pgadmin learning dump:

table properties is where you can find the column settings/values. You can also add 'constraints' so when a column is 'not null?' in 
other words the user must provide a value, you can specify a default value. That way if the user doesn't enter anything, pgadmin will
assign it the value you specify in the constraints tab.

We set up a new server group in pgadmin called postgres, then a database called fastapi, and then created a table under schemas called 
'posts'. that's where we added columns and labeled each column and set a primary key. The primary key column is our id number for each
new post. we set pgadmin to assign a number to it of the type serial so that the posts are numbered in order from when they were
created. You can set one primary key column per table. We also created 'created_at' column and set the data type as time stamp
so that pgadmin/postgres automatically assingns it the time when the row was created.

Just a bit more about 'not null.' when it's turned on you're telling postgres not to accept an empty value for that column, so leaving
a field blank that is assigned to a not null column will throw an error. Unless you set a default in the constraints tab as discussed
above.

There's so many options in pgadmin it's kind of overwhelming but our use of it here is pretty narrow. after setting up the database and 
table on pgadmin, most of the other data will be added to the table by users through the app. But we can use pgadmin as the backend
terminal to view the database, change it's properties etc.