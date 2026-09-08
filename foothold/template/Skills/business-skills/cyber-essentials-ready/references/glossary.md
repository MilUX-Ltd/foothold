# Plain-English glossary

Terms the `cyber-essentials-ready` skill uses, written for someone who isn't an IT specialist. If a user asks "what does that mean", check here before improvising.

## Admin account
A user account that can install software and change system settings. Cyber Essentials wants this to be a separate account from the one you use day to day.

## Antivirus
Software that watches for known bad programs and blocks them. On Mac the built-in version is called XProtect. On Windows it is called Microsoft Defender. Cyber Essentials accepts both.

## BitLocker
The built-in Windows feature that encrypts everything on your hard drive, so a lost or stolen laptop can't be read. The Mac equivalent is FileVault.

## Cyber Essentials
The UK Government's minimum cyber-security standard for organisations of all sizes. Five technical controls, assessed by a self-assessment questionnaire administered by IASME. See https://www.ncsc.gov.uk/cyberessentials/overview.

## Cyber Essentials Plus
The same five controls as Cyber Essentials, plus a hands-on test of your machines by an external assessor. This skill prepares you for Cyber Essentials. If you go on to Plus, the same configuration is the starting point.

## Auto-fail
A question where a wrong answer fails the whole assessment on its own, regardless of how well everything else scores. Danzell introduced the first of these: MFA on cloud services where it is available, and questions A6.4 and A6.5 on installing high-risk or critical updates within 14 days.

## Cloud service
Requirements v3.3 defines it as an on-demand, scalable service, hosted on shared infrastructure and reached over the internet, that you access through an account and that stores or processes your organisation's data. Microsoft 365, Google Workspace, Dropbox and your accounting software all count. Cloud services cannot be excluded from your Cyber Essentials scope.

## CVSS
The Common Vulnerability Scoring System, the industry scale for how serious a security flaw is. Cyber Essentials treats a CVSS v3 base score of 7 or above as high risk or critical, which puts the fix inside the 14-day window.

## Danzell
The name of the current version of the Cyber Essentials question set, in use for assessment accounts created after 26 April 2026. The question set is renamed roughly once a year, after a lighthouse (Beacon, Evendine, Montpellier, Willow, Danzell). The five technical controls stay the same; the phrasing of the questions and the marking evolve. Danzell pairs with the NCSC's Requirements for IT Infrastructure v3.3.

## Defender (Microsoft Defender)
Windows's built-in antivirus and security suite. Comes with every modern Windows install. Cyber Essentials accepts it as malware protection.

## FileVault
The Mac feature that encrypts everything on the drive. The Windows equivalent is BitLocker.

## Firewall
A filter between your computer and the network, which blocks unsolicited connections. Both Mac and Windows have one built in.

## Gatekeeper
A Mac feature that checks apps are from a trusted source before letting you open them. Default-on. Cyber Essentials counts it toward malware protection.

## IASME
The NCSC's delivery partner for Cyber Essentials. They publish the question set, license the certification bodies, and host the certificate search. See https://iasme.co.uk.

## MFA (multi-factor authentication)
Logging in with something you know (a password) plus something else (a code from your phone, a hardware key, a fingerprint). Cyber Essentials requires MFA on cloud services wherever it is available. Under the Danzell question set, not having it is an automatic fail of the whole assessment. This skill does not cover it, you'll do it for each service separately.

## NCSC
The UK's National Cyber Security Centre, part of GCHQ. Publishes the Cyber Essentials standard, the small business guide, and device platform guides. See https://www.ncsc.gov.uk.

## Passkey
A login that replaces the password with a key pair held by your device or a security key, unlocked by your fingerprint, face or PIN. Requirements v3.3 recognises passkeys, and treats a FIDO2 authenticator as multi-factor authentication in its own right.

## Passwordless authentication
Proving who you are with something other than a remembered secret. Passkeys, FIDO2 authenticators, biometrics, security keys or tokens, one-time codes, QR codes and push notifications all count. Requirements v3.3 gives this its own section and encourages it.

## Question set
The list of questions IASME asks you to confirm compliance with the five technical controls. The current set is Danzell. Free download at https://iasme.co.uk/cyber-essentials/free-download-of-self-assessment-questions/.

## Requirements for IT Infrastructure
The NCSC document that states what Cyber Essentials actually requires. The current version is v3.3, published April 2026. The question set asks you about what this document requires.

## Recovery key
A long string of letters and numbers that unlocks an encrypted drive if you lose your normal password. FileVault and BitLocker both give you one when you turn encryption on. You must store it somewhere outside the computer, your password manager is ideal.

## Restore Point (Windows System Restore Point)
A snapshot Windows takes of system files and settings. If a change breaks something, you can roll back to a Restore Point. We take one at the start of this skill as a safety net.

## SIP (System Integrity Protection)
A Mac feature that stops anything (including the user) modifying core operating-system files. Default-on. Cyber Essentials assumes it stays on.

## SmartScreen
A Microsoft feature that warns you before running a file or opening a site Windows thinks is suspicious.

## Standard user
A user account that can't install software or change system settings on its own. Has to authenticate as an admin to do that. Cyber Essentials wants your daily account to be this kind.

## Tamper Protection
A Microsoft Defender feature that prevents apps (including PowerShell) from disabling Defender. Must be on for Cyber Essentials. If a Defender change errors out with "access denied", Tamper Protection is the reason; the fix is to disable it temporarily through Windows Security, make the change, then turn it back on.

## Time Machine
The Mac's built-in backup tool. Cheap, reliable, runs in the background once set up. We take a snapshot at the start of this skill as a safety net.

## UAC (User Account Control)
The Windows prompt that asks for permission when a program tries to make a change requiring admin rights. Cyber Essentials wants it set to Always Notify.

## XProtect
The Mac's built-in anti-malware engine. Updates silently as part of macOS updates. Cyber Essentials accepts it as malware protection.
