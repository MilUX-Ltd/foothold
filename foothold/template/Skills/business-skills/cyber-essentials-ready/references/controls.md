# The five controls, in plain English

Cyber Essentials is built around five technical controls. The NCSC overview is the canonical statement of what each one means: https://www.ncsc.gov.uk/cyberessentials/overview. This file is the plain-English version the skill uses to explain each control to the user when it introduces it.

## 1. Firewalls

Block connections coming in from the network that you didn't ask for. Every Mac and every Windows machine has a software firewall built in. Job done is to confirm it's on for every network profile and, on Mac, that stealth mode is on too.

## 2. Secure configuration

Set the computer up so the obvious risks are closed off. In practice for a single personal machine this means: encrypt the disk, set the screen to lock when you walk away, turn off sharing services you don't use, remove default accounts (like Guest) that aren't needed, and disable old insecure protocols.

## 3. Security update management

Install security updates promptly. Cyber Essentials requires high-risk or critical updates and vulnerability fixes within 14 days of vendor release. The clock starts when the vendor publishes the fix, not when you notice it. "Critical" or "high risk" means the vendor said so, or the vulnerability scores 7 or above on CVSS v3, or the vendor gave no severity information at all.

Under Danzell this is an auto-fail in two places: question A6.4 for operating systems and router and firewall firmware, question A6.5 for applications including their associated files and extensions. Miss either and the whole assessment fails, whatever else you have done.

The practical way to meet this on one computer is to turn on automatic updates for the operating system and for any app that supports it, keep a manual list of the apps that don't, and prune browser extensions you no longer use.

## 4. User access control

Use a separate admin account for installing software and changing system settings. Run your daily work in a standard account. Have a strong password: at least 12 characters, or at least 8 characters with automatic blocking of common passwords, or MFA on the login. Don't reuse it anywhere else. Make sure the computer locks itself when you walk away.

Turn MFA on wherever it is available. Requirements v3.3 says authentication to cloud services must always use MFA. It also gives passwordless methods a section of their own: passkeys, FIDO2 authenticators, biometrics, security keys, push notifications and one-time codes are all recognised, and a FIDO2 authenticator counts as MFA in its own right.

## 5. Malware protection

Have anti-malware running. On Windows: Microsoft Defender with real-time protection, cloud protection, tamper protection and SmartScreen all on. On Mac: Gatekeeper, XProtect and System Integrity Protection all on (they are by default; the job is to confirm). On both: set the OS to only allow apps from trusted sources.

## What's out of scope today

The Cyber Essentials standard also covers:

- Mobile devices (iOS, iPadOS, Android phones and tablets) that you use for work.
- Multi-factor authentication on cloud services (Microsoft 365, Google Workspace, Slack, etc.).
- Network boundary controls (your home or office router/firewall).

This skill does not cover any of those today. They are real Cyber Essentials requirements and you will need to handle them separately before submitting your self-assessment.

Two warnings before you go further.

First, cloud MFA is now an automatic fail. Under the Danzell marking criteria, a cloud service that offers MFA and does not have it turned on fails the assessment outright, whatever state your laptop is in. Requirements v3.3 states that cloud services cannot be excluded from scope, so this cannot be scoped away.

Second, the 14-day update rules apply to everything in your scope, not just the machine in front of you. This skill gets this computer right. Any other device, router or firewall inside your scope is yours to handle.

NCSC's Small Business Guide and the IASME Knowledge Hub are the right starting points:

- https://www.ncsc.gov.uk/collection/small-business-guide
- https://ce-knowledge-hub.iasme.co.uk/

## What changed in Danzell (Requirements v3.3, April 2026)

The five controls are unchanged. What changed is the marking and the wording.

- Automatic fails arrive for the first time in the scheme: MFA on cloud services where it is available, and questions A6.4 and A6.5 on installing high-risk or critical updates within 14 days.
- Cloud services get a definition of their own, and cannot be excluded from scope. A cloud service is an on-demand, scalable service on shared infrastructure, reached over the internet through an account, that stores or processes your organisation's data.
- Passwordless authentication is expanded to name FIDO2 explicitly, alongside passkeys, biometrics, security keys, push notifications and one-time codes.
- Scope criteria no longer describe internet connections as "untrusted" or "user-initiated". Anything excluded from scope must be justified to the assessor, with an explanation of how it is segregated.
- The web applications section is now called software development, and points to the UK Government Software Security Code of Practice. Commercial web applications are in scope by default; bespoke and custom components are out.
- Backing up your data moves earlier in the requirements document. It is still not a technical requirement, and still recommended.
- "Point in time" is now defined as the date the certificate is issued, so your systems have to be supported on that date.

Sources: IASME, https://iasme.co.uk/articles/important-update-changes-to-cyber-essentials-for-april-2026/, and NCSC Requirements for IT Infrastructure v3.3.
