# Marriage Covenant

## Tagline
Marriage covenants with your AI: your own vows, a Bible verse, twelve designs, a PDF to sign

## Description
Marriage Covenant makes a marriage covenant with your AI assistant: both names, the date and place, each person's own vow, a Bible verse and the witnesses, in one of twelve painted or drawn designs, typeset by Doksi as a one-page PDF to sign and frame. It is a keepsake, not a civil marriage certificate.

It is a hosted server with a Streamable HTTP endpoint at https://marriage.publifye.com/mcp, so there is nothing to install. The first time, you sign in from your browser with a Publifye account. It handles marriage covenants only; every covenant is typeset by Doksi, and other documents are made with Doksi itself.

It is for couples, and for the pastors, officiants and wedding arrangers who make covenants with them. Designing, checking the wording and a watermarked preview are free; the print-ready covenant needs a 7-day marriage pass, a Doksi credit or a Doksi plan.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Productivity

## Use Cases
Marriage covenants, wedding vows, wedding keepsakes, Christian marriage covenants, Jewish marriage covenants, covenant PDFs to frame, collecting witness signatures, QR code signing

## Features
- Marriage covenants only: anything else is refused with a pointer to Doksi
- `covenant_requirements` returns the fields, the full JSON schema and complete examples in English and Norwegian, including the 1662 Book of Common Prayer vows
- Twelve designs: seven watercolour paintings, four fine-line drawings and Star & Blossom for a Jewish marriage, plus a plain frame, a laurel frame or your own artwork
- Each person writes their own vow
- A Bible verse, Ecclesiastes 4:12 by default, can be replaced by one to three others or switched off
- A4, or A3 for framing; the covenant is made in English or Norwegian
- `covenant_validate` reports every problem at once, with the JSON path to each
- Free watermarked preview with `covenant_preview`, valid for one hour and never kept
- `covenant_access_status` says before composing whether the account gets a print-ready covenant
- `covenant_compose` takes a `request_id`, so a retry never charges twice
- Kept covenants with private names, a trash and restore within 7 days
- Temporary share links, link rotation and revocation, and email to the account's own verified address only
- Signing by personal link or QR code; signers need no account
- Every covenant says at its foot that it is not a civil marriage certificate
- 19 customer tools

## Getting Started
- "Make a marriage covenant for Anna and Erik, who marry on 19 June 2027 in Bergen, with the Champagne Butterfly design. Ask me for our vows and our witnesses, then show me a preview."
- "Which designs are there, and which one is made for a Jewish marriage?"
- "Use Ruth 1:16 instead of the default verse and check the covenant again"
- "Can my account make the print-ready covenant yet?"
- "Send signing links to both witnesses"
- Tool: covenant_requirements — the fields, schema, examples and what is free or paid
- Tool: covenant_designs — the twelve designs, with preview images and sample PDFs
- Tool: covenant_validate — every problem at once, with the JSON path to each
- Tool: covenant_preview — a free, watermarked preview, not kept
- Tool: covenant_compose — the print-ready covenant, kept on the account
- Tool: covenant_sign_request — personal signing links and QR pages for the couple and witnesses

## Tags
marriage, wedding, covenant, vows, pdf, keepsake, bible, christian, jewish, signatures, qr-code, typesetting, ceremony, document-generation, norwegian

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/marriage

## Health Check URL
https://marriage.publifye.com/health
