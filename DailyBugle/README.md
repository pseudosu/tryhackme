# DailyBugle

# IP ADDR: 10.10.242.106

# NMAP RESULTS

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 68:ed:7b:19:7f:ed:14:e6:18:98:6d:c5:88:30:aa:e9 (RSA)
|   256 5c:d6:82:da:b2:19:e3:37:99:fb:96:82:08:70:ee:9d (ECDSA)
|_  256 d2:a9:75:cf:2f:1e:f5:44:4f:0b:13:c2:0f:d7:37:cc (ED25519)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.6.40)
|_http-generator: Joomla! - Open Source Content Management
| http-robots.txt: 15 disallowed entries 
| /joomla/administrator/ /administrator/ /bin/ /cache/ 
| /cli/ /components/ /includes/ /installation/ /language/ 
|_/layouts/ /libraries/ /logs/ /modules/ /plugins/ /tmp/
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.6.40
|_http-title: Home
3306/tcp open  mysql   MariaDB (unauthorized)
```

# Joomla v3.7.0 is vulnerable to a SQL injection attack
# Used a script: https://github.com/stefanlucas/Exploit-Joomla
# Dumped the user database.
```
 [-] Fetching CSRF token
 [-] Testing SQLi
  -  Found table: fb9j5_users
  -  Extracting users from fb9j5_users
 [$] Found user ['811', 'Super User', 'jonah', 'jonah@tryhackme.com', '$2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm', '', '']
  -  Extracting sessions from fb9j5_session
```
# Username: jonah
# Email: jonak@tryhackme.com
# Password hash: $2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm

# Let's try crack station

# didn't work. Hash is bycrypt. Threw the hash into john the ripper and got the password
# spiderman123
eec3d53292b1821868266858d7fa6f79
# used joomla exploit to put a php reverse shell in the index template.

# ran linpeas on target box.

# username of non-default user is jjameson

# root running python?
    root       948  0.0  1.7 574200 17416 ?        Ssl  16:58   0:01 /usr/bin/python2 -Es /usr/sbin/tuned -l -P
    /.autorelabel  
    nv5uz9r3ZEDzVjNu

# we can run yum as root with no password...
## hmmmmmmmm
# gtfo bins has an exploit for this!

# exploit ran and we have root.

