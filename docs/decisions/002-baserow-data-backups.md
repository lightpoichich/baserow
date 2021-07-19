# Baserow Data Backups

We need to be able to back-up all Baserow data for disaster recovery. There are a number
of ways to do this detailed below, followed by an explanation of why we picked the
chosen solution.

With a back-up solution ideally we are looking for:

* A consistent back-up
* A process that works on a running, production version of Baserow without impacting
  user performance
* A solution that can handle hundreds of thousands of tables (this is common in a large
  Baserow database) or ideally an arbitrary number of tables.
*

## Option 1: pg_dump the entire database at once

[pg_dump](https://www.postgresql.org/docs/11/app-pgdump.html) is the standard logical
back-up tool for Postgres. It essentially generates a big SQL script which when run
recreates the backed-up database.

To do this, pg_dump takes
an [ACCESS SHARE](https://www.postgresql.org/docs/11/explicit-locking.html)
table level lock on all tables it wants to dump, all at once. This is to guarantee it
will get a constant snapshot of the data across the tables. Unfortunately this means
that pg_dump will need to hold a lock per table all in the same transaction. Postgres
controls how many locks a single transaction can hold at once with the
(`max_locks_per_transaction`)[https://www.postgresql.org/docs/11/runtime-config-locks.html]
configuration parameter, which defaults to 64. Baserow creates an actual Postgres
database table per Baserow table resulting in a potentially huge number of tables in the
database, which will continue to grow over time. This means if we want to pg_dump the
entire database at once, we would need to set `max_locks_per_transaction` to at-least be
the number of tables in the database. This is unfeasible as we would need to set this to
a huge number, or be constantly updating it. Additionally, we would then need to
configure other related config parameters to ensure Postgresql has enough shared memory
to open that many locks at
once [1](https://stackoverflow.com/questions/59092696/can-max-locks-per-transaction-be-increased-to-a-very-large-amount)
, [2](https://dba.stackexchange.com/questions/77928/postgresql-complaining-about-shared-memory-but-shared-memory-seems-to-be-ok)
. This is undesirable as our back-up process would over time require an increasing
amount of shared memory.

Another problem with pg_dump taking out an ACCESS SHARE lock on all tables during the
back-up process is that during this time users cannot delete or alter tables and will
recieve database errors.

## Option 2: pg_dump in multiple separate runs

To avoid the `max_locks_per_transaction` issue encountered in Option 1 we could instead
use the various pg_dump parameters to only dump a smaller part of the database in each
run. This is essentially splitting the backup over multiple separate transactions. Also,
this method still has the problem of preventing users altering fields or deleting tables
over whatever subset we choose whilst each back-up runs.

One way of doing this would be using the `-t` pg_dump parameter and dumping each table
at once. However here we run into data consistency issues. What if we dump a through
relation table, then a user deletes a row referenced in that table before we are able to
dump the related table.

We could do something "smarter" by calculating all the connected tables and dumping them
in one transaction. However that seems overly complex, and you still result in a
database backup which isn't from a single snapshot in time. What if users are using
tables in a "related" fashion without using actual FK's, after a restore they could see
very odd results.

Finally, this method also means we could need to come up with our own custom script to
find all the tables/groups of tables to back-up, loop over them running pg_dump many
times, and then somehow combine the resulting SQL scripts and store them. It also means
we can't use pg_dump's built in non SQL script output formats it provides, like the
custom compressed format or the directory format, as we need to stitch together
different pg_dump result files.

## Option 3: pg_basebackup (Chosen solution)

[pg_basebackup](https://www.postgresql.org/docs/11/app-pgbasebackup.html) is another
built-in Postgres back-up tool which works at the file-system level and not logically
like pg_dump. As a result it does not need to open and hold any locks over tables, nor
does it affect clients who are connected and using the database.

Using pg_basebackup we essentially can generate a tarred, compressed snapshot of the
database's files which is also consistent. The resulting file is also self contained
(two separate tar's might be generated when using WAL streaming which we do need to use)
. This means we don't need any custom scripting to inspect the database and figure out
what tables we want to back-up or how to split up a back-up command into many. It'll
just be a nice simple single command line run followed by storing the resulting file 
somewhere safe!

The dis-advantages of this approach is that it is lower level than pg_dump, to restore
you can't just run a SQL file in a database. Instead, you need to extract the dumps
files, place them in the correct postgres folders and start up the cluster. But this
is a relatively simple problem to solve with a runbook or helper script.

We also need to be slightly more careful with how exactly we run pg_basebackup as
it is possible to create backups without transaction logs. If we did not have the 
transaction logs included (also known as WALs), it is almost certain that the backup
is corrupted and un-usable. See https://www.cybertec-postgresql.com/en/pg_basebackup-creating-self-sufficient-backups/
for more details. However as long as we properly understand what pg_basebackup is doing,
test the resulting command line script works and test it can be used to recover Baserow, 
we are fine.

Finally this method could potentially generate much larger archive sizes compared to
pg_dump as it includes everything in the database, the indexes etc, which instead 
pg_dump just stores as the command to create the index. However storage is cheap!







