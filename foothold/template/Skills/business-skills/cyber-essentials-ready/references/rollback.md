# Rollback guide

If anything done by the `cyber-essentials-ready` skill caused a problem on your machine, this file tells you how to undo each control. Use it alongside the evidence pack the skill produced, that file records exactly what was changed and when.

The default position is: do not revert security controls just because something inconvenient happened. Try the inconvenience first, ask the helper for support, then revert as a last resort. If you do revert, you have stepped away from the Cyber Essentials baseline and you should record that in your evidence pack.

If something is genuinely broken, the safest first move is to restore from the backup taken at the start of the run (Time Machine on Mac, System Restore Point on Windows).

## Mac

### Firewall

Apple menu, System Settings, Network, Firewall. Toggle off.

Or, in Terminal: `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off`.

### FileVault

Apple menu, System Settings, Privacy & Security, FileVault, Turn Off. Requires your login password. Decryption takes time and runs in the background.

### Automatic updates

Apple menu, System Settings, General, Software Update. Click the small "i" next to "Automatic updates" and turn off the toggles you want to revert.

### Account demotion

Important: only do this signed in as the second admin account. Apple menu, System Settings, Users & Groups, click the "i" next to the daily account, toggle "Allow this user to administer this computer" back on.

### Lock screen timeout

Apple menu, System Settings, Lock Screen. Set the "Start Screen Saver when inactive" slider back to your preferred interval, and "Require password after screen saver begins or display is turned off" to a longer delay.

### Sharing services

Apple menu, System Settings, General, Sharing. Turn the specific service back on.

### Guest user

Apple menu, System Settings, Users & Groups, Guest User, turn "Allow guests to log in to this computer" back on.

### App installation source

Apple menu, System Settings, Privacy & Security, set "Allow applications downloaded from" back to your preferred value.

### Gatekeeper / SIP

These are macOS defaults. There is no legitimate reason to turn them off. If you are sure you need to, search Apple's documentation for the correct procedure (SIP requires booting to Recovery), and document that you have stepped away from the baseline.

## Windows

### Windows Defender Firewall

Settings, Privacy & security, Windows Security, Firewall & network protection. Toggle off the specific profile.

Or, elevated PowerShell: `Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False`.

### BitLocker

Control Panel, BitLocker Drive Encryption, Turn Off BitLocker on the drive. Decryption takes time and runs in the background.

### Windows Update

Settings, Windows Update, Advanced options. Turn the specific toggle off.

### Account demotion

Important: only do this signed in as the second admin account. Settings, Accounts, Other users / Family & other users, click the daily account, Change account type, set back to Administrator.

Or elevated PowerShell, as the second admin: `Add-LocalGroupMember -Group "Administrators" -Member "<dailyUsername>"`.

### UAC

Control Panel, User Accounts, Change User Account Control settings. Move the slider down to your preferred level.

### Screen timeout

Settings, System, Power & battery, Screen and sleep. Set timeouts back to your preferred values.

Or `powercfg /change monitor-timeout-ac 30` (and `-dc`).

### Password policy

Pro / Enterprise: secpol.msc, Local Policies, Account Policies, Password Policy. Set values back to defaults.

Home or Pro: `net accounts /minpwlen:0 /lockoutthreshold:0`.

### Microsoft Defender

Settings, Privacy & security, Windows Security, Virus & threat protection. Toggle the specific protection off. Tamper Protection prevents this from PowerShell.

### SmartScreen

Settings, Privacy & security, Windows Security, App & browser control, Reputation-based protection settings. Toggle the specific check off.

### Remote Desktop

Settings, System, Remote Desktop. Toggle on.

### AutoPlay

Settings, Bluetooth & devices, AutoPlay. Toggle on.

### SMBv1

Elevated PowerShell: `Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol`. Reboot.

There is no legitimate reason on a current Windows machine to re-enable SMBv1.

## When the rollback isn't enough

If the machine has a problem the rollback above does not solve, use the backup taken at the start of the run:

- **Mac:** boot to Recovery (hold the power button on Apple silicon, Command-R on Intel). Use Migration Assistant or Time Machine restore.
- **Windows:** open System Properties, System Protection, System Restore, choose the restore point taken on the date the skill was run.

If you are not comfortable doing that, stop and ask a Cyber Advisor or a trusted IT helper. NCSC keeps an assured list at https://www.ncsc.gov.uk/schemes/cyber-advisor/introduction.
