# Mac steps

Per-control reference for the `cyber-essentials-ready` skill. Claude reads this during a walkthrough on macOS. Each control maps to a Cyber Essentials question set theme. Source of truth for each setting is Apple's Platform Security guide (https://support.apple.com/guide/security/welcome/web) and NCSC's macOS configuration pack (https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs/tree/main/Apple/macOS).

The wording in each "Say:" block is a starting point. Adapt to the user's pace and prior answers. Do not use em dashes. British English throughout.

System Settings paths are written for macOS 14 (Sonoma) and 15 (Sequoia). On older supported releases the labels are similar but may sit under "System Preferences" rather than "System Settings". If the user is on macOS 12 or earlier, stop and tell them the OS itself is end-of-support territory.

---

## Control 1. Software firewall

**Maps to:** Firewalls.

**Why it matters:** Blocks unsolicited connections from the network to the computer.

**Where to find it:** Apple menu, System Settings, Network, Firewall.

**Check current state**
- Walk-through mode: look at the Firewall toggle in System Settings, Network, Firewall. Note the state.
- Commands mode: `defaults read /Library/Preferences/com.apple.alf globalstate`. `0` is off, `1` is on, `2` is on with all incoming connections blocked.

**Apply**
- Walk-through: turn the Firewall toggle on. Click Options. Tick "Enable stealth mode". Leave "Block all incoming connections" off unless the user has no reason to accept any inbound traffic (most personal users do not need it on).
- Commands: stage on clipboard, the user pastes into Terminal:
  ```
  sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
  sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on
  sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setloggingmode on
  ```
- Do-it-for-me: open System Settings to the Firewall page, click the toggle on, click Options, tick stealth mode, click OK.

**Verify**
- `defaults read /Library/Preferences/com.apple.alf globalstate` should return `1` or `2`.
- `defaults read /Library/Preferences/com.apple.alf stealthenabled` should return `1`.

**Revert:** turn the Firewall toggle off in the same place. Or `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off`.

**Say:** "The firewall blocks incoming connections you didn't ask for. Cyber Essentials needs it on. Stealth mode means your Mac doesn't even reply to things probing it from the network, which is the recommended setting for a personal laptop."

---

## Control 2. FileVault (full-disk encryption)

**Maps to:** Secure configuration.

**Why it matters:** If the computer is lost or stolen, the data on the disk stays unreadable without the user's password or the recovery key.

**Where to find it:** Apple menu, System Settings, Privacy & Security, FileVault.

**Check current state**
- Walk-through: look at the FileVault section. It will say "FileVault is on for the disk" or "FileVault is off".
- Commands: `fdesetup status`.

**Apply (if off)**
- Walk-through: click "Turn On". Choose between "iCloud account" recovery (convenient for solo users with iCloud) or "Recovery key" (a long code the user writes down or saves to their password manager). Recommend the recovery-key option for users with a password manager. The computer encrypts in the background; it can take an hour or more on a busy machine.
- Commands: not recommended for the personal-computer audience. FileVault should be enabled through the UI so the user is in control of the recovery key.
- Do-it-for-me: drive the UI. Stop and hand back to the user when the recovery-key choice appears; that decision must be theirs and the key must end up somewhere they control.

**Verify**
- `fdesetup status` should say "FileVault is On."

**Revert:** Apple menu, System Settings, Privacy & Security, FileVault, Turn Off. Requires the user's login password.

**Say:** "FileVault encrypts everything on the disk. If your laptop is ever lost or stolen, this is what keeps your work confidential. You'll get a recovery key when you turn it on, you'll need somewhere safe to store that, your password manager is the best bet."

---

## Control 3. Automatic updates (macOS and apps)

**Maps to:** Security update management.

**Why it matters:** Cyber Essentials requires security updates to be installed within 14 days of release. Auto-updates are the practical way to meet that on a single machine.

**Where to find it:** Apple menu, System Settings, General, Software Update. Click the small "i" button next to "Automatic updates".

**Check current state**
- Walk-through: open the Automatic updates panel. Note which of the four toggles are on.
- Commands: `defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled` and the related keys. Documented in NCSC's macOS configuration pack.

**Apply**
- Walk-through: in the Automatic updates panel, turn all four toggles on:
  - Check for updates
  - Download new updates when available
  - Install macOS updates
  - Install Security Responses and system files
  Then in App Store settings (System Settings, App Store), set "Install application updates from the App Store" on.
- Commands: prefer the UI for these. The defaults keys exist but the System Settings UI is the cleanest path on a personal machine.

**Verify**
- All four Automatic updates toggles are on.
- App Store's "App updates" toggle is on.

**Revert:** turn the relevant toggle off in the same place.

**Say:** "Cyber Essentials needs security updates installed within 14 days. The simplest way to be confident about that on one laptop is to let the Mac handle it automatically. We turn all four toggles on, and the App Store one for your apps."

**Note on third-party apps:** Apps not from the Mac App Store update through their own mechanism (Sparkle, vendor auto-update, etc.). The user needs to confirm, separately, that any business-critical third-party apps are set to auto-update or are checked manually within 14 days of a release. Capture this in the evidence pack as a manual check item.

---

## Control 4. Account separation (separate admin account)

**Maps to:** User access control.

**Why it matters:** Cyber Essentials requires that admin accounts are not used for everyday work. The user signs in to a standard account for daily use and only switches to or elevates as the admin account when they install software or change system settings.

**Where to find it:** Apple menu, System Settings, Users & Groups.

**Check current state**
- Walk-through: open Users & Groups. List the accounts. Note which are "Admin" and which are "Standard". Note which is the user's daily account.
- Commands: `dscl . list /Users | grep -v '^_'` then `dscl . -read /Groups/admin GroupMembership` to see who has admin.

**Preconditions before any change**
- If only one admin account exists, the first action is to create a second admin. Skip to "Create a second admin" below before doing anything else.
- The second admin account must have a strong, known password (12+ characters), stored in the user's password manager.
- The user must successfully log out of their daily account and log in to the second admin account at least once before we demote the daily account. This proves the admin password works.

**Create a second admin (only if needed)**
- Walk-through: in Users & Groups, click "Add Account..." (or "Add User..." on older macOS). Authenticate. Choose "Administrator" as the account type. Use a descriptive name like "Mac Admin" (not the user's own name). Generate a strong password in their password manager and paste it in. Click Create User.
- Commands: not recommended for this step. Use the UI.

**Demote the daily account to Standard**
- This step only runs after the precondition is confirmed.
- Log out of the daily account. Log in to the new admin account. Open System Settings, Users & Groups, click the small "i" next to the daily account. Toggle off "Allow this user to administer this computer". Click OK. Log out of the admin account. Log back in to the daily account.

**Verify**
- In Users & Groups, the daily account shows as "Standard". The other account shows as "Admin".
- Try a quick admin-only action from the daily account, e.g. open System Settings, Users & Groups, click the lock. The user should be prompted for the admin account's username and password, not their own.

**Revert:** log in as the admin account, toggle "Allow this user to administer this computer" back on for the daily account.

**Say:** "Cyber Essentials wants your daily account to be a standard user, with a separate admin account that only gets used when you install software or change a system setting. We need to make sure that second admin works perfectly before we change anything about your daily account, otherwise you can lock yourself out."

**Critical:** if the user cannot confirm the second admin works (cannot log in to it, password not stored), stop. Do not demote. Tell the user the risk plainly: with no working second admin and no admin rights on the daily account, they cannot install software or change system settings.

---

## Control 5. Lock screen and password on wake

**Maps to:** Secure configuration, User access control.

**Why it matters:** A computer left unattended is a computer anyone walking past can use.

**Where to find it:** Apple menu, System Settings, Lock Screen.

**Check current state**
- Walk-through: read the "Require password after screen saver begins or display is turned off" setting and the inactivity timer.

**Apply**
- Walk-through: set "Start Screen Saver when inactive" to 10 minutes or less. Set "Require password after screen saver begins or display is turned off" to "Immediately" (or "After 5 seconds" if the user finds Immediately too aggressive in practice; Cyber Essentials wants this to be short).
- Commands: stage on clipboard:
  ```
  defaults write com.apple.screensaver idleTime -int 600
  defaults write com.apple.screensaver askForPassword -int 1
  defaults write com.apple.screensaver askForPasswordDelay -int 0
  ```

**Verify**
- Settings show 10 minutes or less, password Immediately.

**Revert:** set the slider back to the user's preferred longer interval.

**Say:** "If you walk away from the laptop for a few minutes and someone wanders past, the screen should already be locked. We'll set it to lock after 10 minutes of inactivity and ask for the password immediately."

---

## Control 6. Account password strength

**Maps to:** User access control.

**Why it matters:** Cyber Essentials requires either a 12+ character password, or 8+ with a blocklist and throttling, or MFA on the device login. On macOS the practical path is "use a strong passphrase the user actually remembers".

**Check current state**
- The user knows whether their password is strong. There is no way to read the current password length. Ask honestly: "How long is the password you use to log in to this Mac, and is it the same password you use anywhere else?"

**Apply**
- Walk-through: if the password is shorter than 12 characters or reused anywhere else, walk the user through changing it. System Settings, Touch ID & Password (or Users & Groups, Change Password), Change Password. Recommend a memorable passphrase of four random words plus a number, or whatever their password manager generates.
- Commands: not appropriate. Password changes go through the UI so the keychain is updated correctly.

**Verify**
- The user logs out, logs back in with the new password. The change worked.

**Revert:** change it back through the same UI.

**Say:** "Your Mac password is the front door. Cyber Essentials wants it to be at least 12 characters and not reused anywhere else. A passphrase like four random words and a number is both stronger and easier to remember than something with random symbols."

**Caveat for the audit:** for the evidence pack, record the date the password was last changed and whether it has been confirmed unique to this device. Do not record the password itself.

---

## Control 7. Built-in malware protection (Gatekeeper, XProtect, SIP)

**Maps to:** Malware protection.

**Why it matters:** macOS ships with built-in protection: Gatekeeper checks app signatures, XProtect blocks known malware, System Integrity Protection (SIP) stops malware tampering with the OS. Cyber Essentials accepts these as malware protection on macOS, so the job is to confirm they are all on.

**Check current state**
- Commands:
  - `spctl --status` should say "assessments enabled".
  - `csrutil status` should say "System Integrity Protection status: enabled".
  - XProtect updates are part of normal Software Update; if Control 3 is satisfied, XProtect is updating.

**Apply (only if any check fails)**
- Gatekeeper off: rare on a personal Mac. If `spctl --status` says "assessments disabled", `sudo spctl --master-enable` re-enables it.
- SIP disabled: very rare. Requires booting to Recovery to fix. If the user shows SIP disabled, stop and tell them they need to boot to Recovery (Apple menu, Restart, hold the power button on Apple silicon or Command-R on Intel) and run `csrutil enable` from the Recovery Terminal. Walk through carefully.

**Verify**
- Re-run the two commands above.

**Revert:** the secure state is the default. There is no legitimate need to revert.

**Say:** "macOS has malware protection built in. We just need to confirm it's switched on. There are three pieces: Gatekeeper, which checks that apps you open are from a trusted source; XProtect, which is Apple's malware database; and System Integrity Protection, which stops anything tampering with the operating system itself. All three should be on out of the box."

---

## Control 8. Sharing services off

**Maps to:** Secure configuration.

**Why it matters:** Each sharing service is a potential way in. Cyber Essentials wants only the services the user actively needs to be on.

**Where to find it:** Apple menu, System Settings, General, Sharing.

**Check current state**
- Walk-through: open Sharing. Read the state of each toggle.

**Apply**
- Walk-through: turn the following off unless the user has a stated reason to need them on:
  - Screen Sharing
  - File Sharing
  - Media Sharing
  - Printer Sharing
  - Remote Login (this is SSH)
  - Remote Management (this is Apple Remote Desktop)
  - Bluetooth Sharing
  - Internet Sharing
  - AirPlay Receiver (or set to "Current User" if they use AirPlay to their own Mac)
  - Content Caching
- For AirDrop: System Settings, General, AirDrop & Handoff, set AirDrop to "Contacts Only" or "Receiving Off".

**Verify**
- All toggles in Sharing are off (or set as recorded above).

**Revert:** turn the specific toggle on if the user later finds they need that service.

**Say:** "Each of these is a way for another computer to reach into yours. The recommended setting for a personal laptop is to have all of them off, and only turn one on when you actually need it that day."

---

## Control 9. Guest user off

**Maps to:** User access control.

**Where to find it:** Apple menu, System Settings, Users & Groups, Guest User.

**Apply**
- Walk-through: click the "i" next to Guest User, turn "Allow guests to log in to this computer" off. Click OK.

**Verify**
- Users & Groups list shows Guest User as off.

**Revert:** turn it back on if the user wants it.

**Say:** "The Guest account lets anyone log in to your Mac as a one-off. Cyber Essentials wants this off."

---

## Control 10. App installation source

**Maps to:** Secure configuration, Malware protection.

**Where to find it:** Apple menu, System Settings, Privacy & Security, "Allow applications downloaded from".

**Apply**
- Walk-through: set this to "App Store" if the user installs everything from the App Store. If they use direct-download apps (Zoom, Adobe, browsers, dev tools), set this to "App Store & Known Developers". Do not advise leaving this on "Anywhere"; macOS 13+ does not even offer "Anywhere" in the UI without a Terminal override.

**Say:** "macOS only lets you install apps from sources it can verify. Keep this set to App Store, or App Store and Known Developers if you install things like Zoom or Adobe directly."

---

## Control 11. NCSC reference cross-check (optional advanced step)

For users who want to compare what we have just done against the canonical NCSC recommendation, point them at:

- NCSC macOS configurations (CSV and Markdown), https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs/tree/main/Apple/macOS
- NCSC's macOS Platform Guide, https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/macos

These are written for enterprise IT teams, not solo users, but the per-setting recommendations are the same. If a difference exists, note it in the evidence pack and let the user decide whether to apply the stricter NCSC variant.

---

## End-of-run checklist

Before generating the evidence pack, confirm with the user:

- All ten controls above have a status recorded (Applied, Already compliant, Skipped).
- Recovery key for FileVault is stored somewhere outside the computer.
- Second admin account credentials are stored in the user's password manager.
- A Time Machine backup ran or is running.
- The user can still log in to both the daily standard account and the second admin account.

If any of those is "no", flag it and resolve before finishing.
