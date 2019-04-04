# Program: news_analysis.py 
Author: Perry Brandiezs
Date: April 4, 2019


This program will analyse the news database to answer three questions:

*   Question 1: What are the most popular three articles of all time?
*   Question 2: Who are the most popular article authors of all time?
*   Question 3: On which days did more than 1% of requests lead to errors?

## Installation 
This program requires Virtualbox and Vagrant to be installed.

### System Preparation
These procedures document the setup on an HP laptop running WIN 10 Pro.

#### BIOS setup
*Reboot the system to access the BIOS setup, by pressing F10 as the system powers-up
*Move to the settings screen
*Enable Virtualization Technologies
*Save the change and continue the system boot
#### Disable hyper-v
If previously enabled, it is necessary to disable hyper-v to run Ubuntu 64 bit in Virtual-box.
*Select Windows logo
*Type Control Panel
*Select Programs
*Turn Windows features on or off
*Make sure Hyper-V, and it's options are not selected
*Click OK
### Virtualbox Installation
Download and install VirtualBox following the procedures here:
https://www.virtualbox.org/wiki/Downloads

This program was tested with the most recent version of VirtualBox Version 6.0.4 r128413 (Qt5.6.2)
### Virtualbox Extension Pack Installation
Download and install Virtual Box Extension Pack following the procedures here:
https://www.virtualbox.org/wiki/Downloads
### Vagrant Installation
Download and install Vagrant following the procedures here:
https://www.vagrantup.com/downloads.html

This program was tested with the most recent version Vagrant 2.2.4
### Vagrant VM Installation
*Download, uncompress, and install the Vagrant VM from this link:
https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip
*Change into the vagrant directory: **cd vagrant**
*Start the VM, this may take a few minutes: **vagrant up**
*Connect to the VM: **vagrant ssh**
*ctrl-d to exit from Vagrant
### Data Load Procedures
*Download and unzip the data from this link:
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
*Place the newsdata.sql file into the vagrant directory
*Connect to the VM: **vagrant ssh**
*cd to the shared vagrant directory: **cd /vagrant**
*Install the data into the database: **psql -d news -f newsdata.sql**
*ctrl-d to exit from Vagrant
### Create view tables
*Connect to the VM: **vagrant ssh**
*cd to the shared vagrant directory: **cd /vagrant**
*Install the data into the database: **psql -d news**
*Run these sql commands to create the two views:
```
CREATE VIEW daily_error AS
    SELECT to_char(date_trunc('day', time), 'YYYY-MM-DD') as date,
        COUNT(*) AS error_count
        FROM log
        WHERE status <> '200 OK'
        GROUP BY date_trunc('day', time);

CREATE VIEW daily_count AS
    SELECT to_char(date_trunc('day', time), 'YYYY-MM-DD') as date,
        COUNT(*) as day_count
        FROM log
        GROUP BY date_trunc('day', time);
```
*ctrl-d to exit from psql
*ctrl-d to exit from Vagrant
### Moving news_analysis.py to the vagrant VM
*Move this program news_analysis.py to the vagrant directory
## Usage
*cd to the vagrant directory
*Connect to the VM: **vagrant ssh**
*cd to the VM's vagrant directory: **cd /vagrant**
*Execute the program: **python news_analysis.py**
*ctrl-d to exit from Vagrant
*vagrant halt to shutdown the vagrant VM (restart again with vagrant up)
## Expected Output

```
vagrant@vagrant:/vagrant$ python news_analysis.py


Analysis of news database results:


Question 1: What are the most popular three articles of all time?


"Candidate is jerk, alleges rival" -- 338647 views
"Bears love berries, alleges bear" -- 253801 views
"Bad things gone, say good people" -- 170098 views

==========

Question 2: Who are the most popular article authors of all time?


Ursula La Multa -- 507594 views
Rudolf von Treppenwitz -- 423457 views
Anonymous Contributor -- 170098 views
Markoff Chaney -- 84557 views

==========

Question 3: On which days did more
than 1% of requests lead to errors?


July 17, 2016 -- 2.26% errors

==========

```