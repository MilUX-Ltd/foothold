# Vault Viewer

**v1.0.0**

A single HTML file that reads a folder of Markdown notes like a website. No install, no cloud, no account. Point it at a folder and read it, with wikilinks, search and backlinks all working. It understands Obsidian-style links and embeds, but Obsidian is not required and nor is anything else.

Built for the case where someone needs to read a Foothold vault, or any Markdown folder, on a machine that does not have Obsidian.

## How to use it

1. Download `vault-viewer.html`.
2. Open it in Chrome, Edge or Brave. Double-clicking may open your default browser, so if that is Safari or Firefox, open the file from within a Chromium browser instead.
3. Click "Open a vault folder" and choose the folder you want to read.

That is the whole setup. The folder picker is the browser's File System Access API, which exists in Chromium browsers and not in Safari or Firefox.

## What it does

- Renders Markdown: headings, lists, tables, task lists, code blocks, quotes, images and frontmatter.
- Resolves `[[wikilinks]]`, aliases, heading links and `![[embeds]]` for images and notes, plus standard Markdown links with spaces in the filename.
- Full-text search across the vault, with Cmd/Ctrl-K to focus it.
- A backlinks panel and an outgoing-links list for the open note.
- A file tree that starts fully collapsed and reveals a folder only when you open a note inside it.
- Light and dark themes, following the system by default with a manual toggle that is remembered.
- Resizable side columns: drag the inner edge of either panel, double-click to reset. Widths are remembered.
- An opt-in edit mode. The viewer is read-only until you click Edit, at which point the browser asks once for write permission. Saving writes back to the real file. There is an unsaved-changes indicator and a prompt before you navigate away or close with unsaved edits.

## Privacy

The file makes no network requests. It was audited for `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, web workers, analytics, external scripts, stylesheets, iframes and font imports. None are present. The brand fonts are embedded in the file as base64, so they render offline with nothing to download.

Two things depend on the content of the notes themselves, not on the viewer:

- A link in a note to a website opens that site when you click it. That is a deliberate action.
- A note that embeds an image by remote URL (`![](https://...)`) causes the browser to load that image when the note is rendered. Local images stay offline. Most vaults only use local images.

The file contains no vault data. You are sharing the viewer, not any notes.

## Edit mode and your files

Edit mode writes to your actual files in place. It has no version history of its own, so it relies on whatever you already use, such as Obsidian Sync or Git. Treat editing here with the same care as editing the files directly. The viewer stays read-only until you choose to edit.

## Browser support

Works in Chrome, Edge, Brave and other Chromium browsers. Safari and Firefox do not support the folder picker the viewer relies on.

## Fonts and licences

The embedded fonts are open-source and redistributable: Manrope and Bai Jamjuree under the SIL Open Font License 1.1, and Roboto Mono under Apache License 2.0.

## Version history

### 1.0.0, 2026-06-23

First release. Single-file offline viewer with Markdown rendering, Obsidian-style wikilinks, embeds and backlinks, full-text search, a collapsible file tree, light and dark themes, resizable columns, and opt-in editing that writes back to disk. MilUX brand fonts embedded for fully offline use.

## Help

Email matt@milux.co.uk or open an issue at https://github.com/MilUX-Ltd/foothold/issues.
