# Windows steps

Per-control reference for the `cyber-essentials-ready` skill. Claude reads this during a walkthrough on Windows 10 or Windows 11. Each control maps to a Cyber Essentials question set theme. Source of truth for each setting is Microsoft's documentation at https://learn.microsoft.com/ and NCSC's Windows configuration pack (https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs/tree/main/Microsoft/Windows). The NCSC pack is written for Intune-managed estates; we are adapting the same controls for a single personally-owned machine.

The wording in each "Say:" block is a starting point. Adapt to the user's pace and prior answers. Do not use em dashes. British English throughout.

Settings paths are written for Windows 11. Where Windows 10 differs, the Windows 10 path is noted alongside.

Important up front: ask the user which edition they're on, Home, Pro or Enterprise. Some controls (Group Policy, BitLocker via Control Panel, password complexity via secpol) are not available on Home and we use registry equivalents instead.

To check edition: `winver` (run from Start menu), or Settings, System, About, Windows specifications.

---

## Control 1. Windows Defender Firewall

**Maps to:** Firewalls.

**Why it matters:** Blocks unsolicited connections from the network to the computer.

**Where to find it:** Settings, Privacy & security, Windows Security, Firewall & network protection.

**Check current state**
- Walk-through: open Firewall & network protection. Three profiles are listed, Domain, Private, Public. Each should say "Firewall is on".
- Commands (elevated PowerShell): `Get-NetFirewallProfile | Select-Object Name, Enabled`. All three should show `Enabled : True`.

**Apply**
- Walk-through: for each profile that shows off, click it and toggle the firewall on. Leave inbound rules at default (block) and outbound at default (allow).
- Commands (elevated PowerShell, staged on clipboard):
  ```
  Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
  ```

**Verify**
- Re-run `Get-NetFirewallProfile | Select-Object Name, Enabled`. All three `True`.

**Revert:** `Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False` (not recommended).

**Say:** "Windows Defender Firewall blocks incoming connections you didn't ask for. Cyber Essentials needs it on for all three profiles, Domain, Private and Public."

---

## Control 2. Device encryption (BitLocker)

**Maps to:** Secure configuration.

**Why it matters:** If the laptop is lost or stolen, the data on the disk stays unreadable.

**Where to find it:**
- Windows 11 Home, Pro and Enterprise: Settings, Privacy & security, Device encryption (Home) or Settings, System, Storage, Advanced storage settings, Disks & volumes, BitLocker (Pro / Enterprise).
- Windows 10 Pro and Enterprise: Control Panel, BitLocker Drive Encryption.
- Windows 10 Home: limited to "Device encryption" via Settings, Update & Security, Device encryption, if the device supports it.

**Hardware precondition:** BitLocker requires a TPM 2.0 chip. Most machines made in the last five years have one. To check: open Device Security in Windows Security, look for "Security processor". If it says "Standard hardware security not supported", BitLocker is unlikely to work without group policy changes that are beyond the scope of this skill. Note this in the evidence pack as a hardware blocker and move on.

**Check current state**
- Walk-through: open the BitLocker page. The C: drive should say "BitLocker on" or "Device encryption on".
- Commands (elevated PowerShell): `Get-BitLockerVolume -MountPoint C:`. `ProtectionStatus` should be `On`.

**Apply (if off and hardware supports it)**
- Walk-through: open the BitLocker page, click "Turn on BitLocker" for the C: drive. Choose how to back up the recovery key. Recommend "Save to a file" then store that file in the user's password manager or somewhere offline they control, OR "Print the recovery key" and keep the printout somewhere safe. Do NOT choose "Save to your Microsoft account" as the only option, because if the account is lost so is the key. Choose "Encrypt entire drive" (slower, safer than "Used disk space only" for an existing machine). Choose "New encryption mode". Start encrypting. The user can keep working, encryption runs in the background.
- Commands: BitLocker setup is safer through the UI than PowerShell for non-IT users, because the recovery key handling is the single most error-prone step.

**Verify**
- Re-run `Get-BitLockerVolume -MountPoint C:`. `ProtectionStatus : On`.

**Revert:** Control Panel, BitLocker Drive Encryption, Turn Off BitLocker. Takes hours; the disk decrypts in the background.

**Say:** "BitLocker encrypts the contents of your hard drive. If the laptop is ever lost or stolen, this is what stops anyone reading what's on it. We need to be careful with the recovery key, that's what unlocks the drive if anything goes wrong, so we'll save it somewhere you control."

---

## Control 3. Windows Update

**Maps to:** Security update management.

**Why it matters:** Cyber Essentials requires security updates installed within 14 days of release.

**Where to find it:** Settings, Windows Update.

**Check current state**
- Walk-through: look at the top of the Windows Update page. It should say "You're up to date" or similar. If it says updates are available, install them now.
- Then click Advanced options. Confirm:
  - "Receive updates for other Microsoft products" is on.
  - "Get the latest updates as soon as they're available" is on (this opts in to the Last-Cumulative-Update fast-ring; recommended for Cyber Essentials's 14-day window).
  - Active hours are configured so updates can install when the user isn't using the laptop.
  - "Pause updates" is NOT enabled.

**Apply**
- Walk-through: click Check for updates. Install everything offered. Reboot if asked. After reboot, run "Check for updates" again. Repeat until "You're up to date" sticks.
- Commands (elevated PowerShell): `Get-WindowsUpdate; Install-WindowsUpdate -AcceptAll -AutoReboot` (requires the `PSWindowsUpdate` module). Not recommended for non-IT users; the UI is safer.

**Verify**
- Windows Update page says "You're up to date".
- Advanced options shows the right settings.

**Revert:** turn the specific advanced-options toggle off.

**Say:** "Windows needs to install security updates promptly. We'll let it check now, install anything pending, and confirm it's set to keep doing that automatically. Active hours just tell Windows when not to reboot you mid-workday."

---

## Control 4. Account separation (separate admin account)

**Maps to:** User access control.

**Why it matters:** Cyber Essentials requires that admin accounts are not used for everyday work. The user signs in to a standard account for daily use and only authenticates as the admin account when they install software or change system settings.

**Where to find it:** Settings, Accounts, Other users (Windows 11) or Settings, Accounts, Family & other users (Windows 10).

**Check current state**
- Walk-through: open Other users / Family & other users. Note any existing accounts. Then open Settings, Accounts, Your info, this shows whether the user's daily account is Administrator or Standard.
- Commands (elevated PowerShell):
  ```
  Get-LocalUser
  Get-LocalGroupMember -Group "Administrators"
  ```

**Preconditions before any change**
- Same as macOS, do not demote the only admin. The second admin account must exist, must have a strong known password (12+ chars in the user's password manager), and the user must have successfully logged in to it at least once before we touch the daily account.

**Create a second admin (only if needed)**
- Walk-through: Settings, Accounts, Other users, "Add account". Click "I don't have this person's sign-in information", then "Add a user without a Microsoft account". Use a descriptive name like "Win Admin". Set a strong password (no security questions for a local admin if avoidable; Windows may insist on three, just use throwaway answers stored in the password manager). Once created, click the new account in the list, click "Change account type", set to Administrator.
- Commands (elevated PowerShell):
  ```
  $pw = Read-Host -AsSecureString
  New-LocalUser -Name "WinAdmin" -Password $pw -FullName "Win Admin"
  Add-LocalGroupMember -Group "Administrators" -Member "WinAdmin"
  ```
  Then sign out of the daily account and sign in to WinAdmin to confirm it works.

**Demote the daily account to Standard**
- Sign in as the new admin (WinAdmin). Settings, Accounts, Other users, click the daily account, Change account type, Standard user. Or PowerShell, signed in as WinAdmin:
  ```
  Remove-LocalGroupMember -Group "Administrators" -Member "<dailyUsername>"
  ```
- Sign out of the admin account, sign back in to the daily account.

**Verify**
- Settings, Accounts, Your info shows "Standard user" on the daily account.
- Open Settings as the daily account and try to access "Add account" under Other users. Windows should prompt for the admin account's credentials.
- `Get-LocalGroupMember -Group "Administrators"` lists the admin account and any built-in admins, but not the daily account.

**Revert:** sign in as the admin, change the daily account back to Administrator.

**Say:** "Cyber Essentials wants your daily account to be a Standard user, with a separate admin account that you only authenticate as when you install software. We need to make sure that admin works perfectly before we change anything about your daily account, otherwise you can lock yourself out."

**Critical safety check:** if the user cannot confirm the second admin works, stop. Do not demote.

---

## Control 5. User Account Control (UAC)

**Maps to:** User access control.

**Why it matters:** UAC is the prompt that asks for permission when a program tries to make changes that require admin rights. Cyber Essentials expects it to be on, and at the strict setting.

**Where to find it:** Control Panel, search for "UAC", "Change User Account Control settings". Or Settings search bar, type "UAC".

**Check current state**
- Walk-through: open the UAC settings dialog. There's a slider with four positions.

**Apply**
- Walk-through: drag the slider to the top, "Always notify". Click OK.
- Commands (elevated PowerShell):
  ```
  Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 2
  Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA" -Value 1
  Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "PromptOnSecureDesktop" -Value 1
  ```

**Verify**
- UAC slider is at the top.
- `(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System").EnableLUA` returns 1.

**Revert:** move the slider down. Not recommended.

**Say:** "User Account Control is the prompt that pops up when something tries to change your computer. Setting it to Always Notify is what Cyber Essentials expects, so any change has to go through that prompt and you can see who's asking."

---

## Control 6. Lock screen and screen timeout

**Maps to:** Secure configuration, User access control.

**Where to find it:** Settings, Personalization, Lock screen, Screen timeout. And Settings, Accounts, Sign-in options, "If you've been away, when should Windows require you to sign in again".

**Apply**
- Walk-through: set the screen timeout for "On battery, turn off my screen after" and "When plugged in, turn off my screen after" both to 10 minutes or less. Then under Sign-in options, set "If you've been away..." to "When PC wakes up from sleep" (or, on Windows 11, set the lock to occur when the screensaver kicks in).
- Commands (elevated PowerShell, staged):
  ```
  powercfg /change monitor-timeout-ac 10
  powercfg /change monitor-timeout-dc 10
  ```

**Verify**
- Settings show the new timeout.

**Revert:** set the slider longer.

**Say:** "If you walk away for a few minutes, the screen should lock itself. We'll set it to 10 minutes, with a password required on wake."

---

## Control 7. Password policy

**Maps to:** User access control.

**Why it matters:** Cyber Essentials Montpellier requires either 12+ character minimum, or 8+ with throttling and a common-password blocklist, or MFA on the device login. On a personal Windows machine, the simplest evidenceable path is to set the minimum length policy to 12 and tell the user to pick a strong passphrase.

**Where to find it:**
- Pro and Enterprise: Run, `secpol.msc`, Local Policies, Account Policies, Password Policy.
- Home: Group Policy is not available. Use registry, see below.

**Check current state (Pro/Enterprise)**
- Walk-through: open `secpol.msc`. Go to Password Policy. Note "Minimum password length", "Account lockout threshold" (in Account Lockout Policy).
- Commands (elevated PowerShell):
  ```
  secedit /export /cfg C:\temp\secpol.cfg
  Get-Content C:\temp\secpol.cfg | Select-String "MinimumPasswordLength|LockoutBadCount"
  ```

**Apply (Pro/Enterprise)**
- Walk-through: in `secpol.msc`, set:
  - Minimum password length: 12.
  - Account lockout threshold: 10 invalid logon attempts.
  - Account lockout duration: 15 minutes.
  - Reset account lockout counter after: 15 minutes.
- Commands (elevated PowerShell, staged):
  ```
  net accounts /minpwlen:12 /lockoutthreshold:10 /lockoutduration:15 /lockoutwindow:15
  ```

**Apply (Home)**
- `net accounts` works on Home as well. Stage the same command. Group Policy editor does not exist but the underlying policy settings are still respected by Windows.

**Verify**
- `net accounts` shows the new values.

**Revert:** `net accounts /minpwlen:0 /lockoutthreshold:0`.

**Say:** "Cyber Essentials wants passwords at least 12 characters, and accounts to lock out after 10 wrong attempts. We'll set both, and you'll need to pick a passphrase that's at least 12 characters and not used anywhere else."

**Caveat:** Microsoft accounts (sign in with your @outlook.com or @hotmail.com) bypass local policy because the password is managed by Microsoft. For Microsoft accounts, the user's job is to make sure the account password is strong (12+ chars) and that 2-step verification is on at https://account.microsoft.com/security. Record this as a manual check in the evidence pack.

---

## Control 8. Microsoft Defender Antivirus

**Maps to:** Malware protection.

**Where to find it:** Settings, Privacy & security, Windows Security, Virus & threat protection.

**Check current state**
- Walk-through: open Virus & threat protection. Confirm:
  - Real-time protection is On.
  - Cloud-delivered protection is On.
  - Automatic sample submission is On.
  - Tamper Protection is On.
  - Definitions are up to date (date shown in the Threat history area).
- Commands (elevated PowerShell):
  ```
  Get-MpComputerStatus | Select-Object AMServiceEnabled, AntispywareEnabled, AntivirusEnabled, RealTimeProtectionEnabled, IsTamperProtected, AntivirusSignatureLastUpdated
  ```

**Apply (if anything is off)**
- Walk-through: toggle the offending switch on.
- Commands (staged): `Set-MpPreference -DisableRealtimeMonitoring $false` (and similar per setting).

**Important Tamper Protection note:** Tamper Protection prevents some PowerShell-driven changes to Defender. If a `Set-MpPreference` command fails with access denied, that is why. The user can temporarily disable Tamper Protection (Settings, Virus & threat protection, Manage settings) to apply the change, then turn it back on. Walk through that carefully and re-enable Tamper Protection at the end.

**Verify**
- `Get-MpComputerStatus` shows all the relevant flags `True`.

**Say:** "Microsoft Defender is the built-in antivirus on Windows. Cyber Essentials accepts it as malware protection. We just need to confirm real-time protection, cloud protection and tamper protection are all on, and that the malware definitions are up to date."

---

## Control 9. SmartScreen

**Maps to:** Malware protection, Secure configuration.

**Where to find it:** Settings, Privacy & security, Windows Security, App & browser control, Reputation-based protection settings.

**Apply**
- Walk-through: turn on:
  - Check apps and files
  - SmartScreen for Microsoft Edge
  - Potentially unwanted app blocking
  - SmartScreen for Microsoft Store apps

**Say:** "SmartScreen warns you when you try to run a file or open a site Windows has reason to think is suspicious. Cyber Essentials wants these warnings on."

---

## Control 10. Remote Desktop

**Maps to:** Secure configuration.

**Where to find it:** Settings, System, Remote Desktop.

**Apply**
- Walk-through: set Remote Desktop to Off, unless the user specifically uses it (sole traders usually do not). If they do use it, that is fine for CE provided RDP is locked down with strong passwords and not exposed to the public internet.

**Say:** "Remote Desktop lets you log in to your computer from another computer. If you don't actively use it, Cyber Essentials wants it off."

---

## Control 11. AutoPlay

**Maps to:** Secure configuration.

**Where to find it:** Settings, Bluetooth & devices, AutoPlay.

**Apply**
- Walk-through: turn "Use AutoPlay for all media and devices" off. Or set every individual default to "Take no action".

**Say:** "AutoPlay is what makes a CD or USB stick open automatically when you plug it in. Cyber Essentials wants this off so a dodgy USB can't run anything on its own."

---

## Control 12. Guest account confirmation

**Maps to:** User access control.

**Apply**
- Commands (elevated PowerShell):
  ```
  Get-LocalUser -Name "Guest"
  ```
- If `Enabled` is `True`, disable it:
  ```
  Disable-LocalUser -Name "Guest"
  ```
- On modern Windows the Guest account is disabled by default; this is a verify-only check for most users.

**Say:** "The Guest account is disabled by default on modern Windows. We're just confirming it's still off."

---

## Control 13. SMBv1

**Maps to:** Secure configuration.

**Why it matters:** SMBv1 is an old file-sharing protocol with serious known vulnerabilities. Cyber Essentials wants insecure protocols disabled.

**Check current state**
- Commands (elevated PowerShell):
  ```
  Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
  ```

**Apply (if enabled)**
- Commands (staged):
  ```
  Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart
  ```
- Reboot when convenient.

**Say:** "SMBv1 is an old file-sharing protocol from before modern security. It's been exploited in big ransomware campaigns. We turn it off."

---

## Control 14. NCSC reference cross-check (optional advanced step)

For users who want to compare what we have just done against the canonical NCSC recommendation, point them at:

- NCSC Windows configurations (CSV and Markdown), https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs/tree/main/Microsoft/Windows/MDM/Configurations
- NCSC Windows Platform Guide, https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/windows

These are written for organisations using Microsoft Intune, but the per-setting recommendations are the same. Where applicable to a single machine, the user can apply the stricter NCSC variant via Group Policy or registry. Capture any divergence in the evidence pack.

---

## End-of-run checklist

Before generating the evidence pack, confirm with the user:

- All applicable controls above have a status recorded (Applied, Already compliant, Skipped, Hardware blocker).
- BitLocker recovery key is saved somewhere the user controls and is NOT only stored in the Microsoft cloud.
- Second admin account credentials are stored in the user's password manager.
- A System Restore Point is in place for today.
- The user can still log in to both the daily standard account and the second admin account.
- Microsoft account password is strong and 2-step verification is on (if they sign in with a Microsoft account).

If any of those is "no", flag it and resolve before finishing.
