# Photo

**Which photo goes on the CV, and who sees it?** 4 Vitae MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://vitae.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`photo_get`](#photo_get) | read | Read the profile photo back: {cv_id, include_bytes?}. Owner only.   Without include_byte… |
| [`photo_set`](#photo_set) | write | Upload the profile photo: {cv_id, image_base64, content_type?}. Replaces any existing on… |
| [`photo_clear`](#photo_clear) | write | Remove the profile photo: {cv_id}. The file is destroyed, not hidden.   THIS IS NOT THE … |
| [`photo_visibility_set`](#photo_visibility_set) | write | Show or hide the profile photo to READERS, per language edition: {cv_id, show, lang?}.  … |

---

## `photo_get`

**Photo Get** — read-only, idempotent, closed-world · access: `read`.

Read the profile photo back: {cv_id, include_bytes?}. Owner only.
  Without include_bytes it reports what is stored — type, size, dimensions, when it was set. With include_bytes it returns the file itself, base64.
  IT EXISTS SO AN AGENT CAN DO WHAT AN OWNER CAN (rule 4) AND SO EXPORT IS NEVER WITHHELD (spec principle 5): a photo you can upload and never retrieve would be data of yours we hold and do not hand back. cv_export returns the JSON Resume document; this returns the one artifact that is not inside it.
  A stranger and a CV that does not exist get the same answer, and so does an impersonating admin.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `include_bytes` | boolean | no | return the image itself, base64. Default false. |

## `photo_set`

**Photo Set** — writes, closed-world · access: `write`.

Upload the profile photo: {cv_id, image_base64, content_type?}. Replaces any existing one.
  UPLOADING IS NOT PUBLISHING. A photo stored by this tool is shown to YOU and to nobody else until you say otherwise: no published page, no redacted PDF, no non-owner export. Publish it per language edition with photo_visibility_set — and hide it again with the same tool, which is NOT the same as photo_clear: hiding keeps the file, clearing destroys it.
  REPLACING A PHOTO DOES NOT REPUBLISH IT ANYWHERE NEW. The editions you had already published it in keep showing the new one; the ones you had not are untouched.
  JPEG AND PNG ONLY, and the format is decided by DECODING the bytes — the content type you declare and the name of the file you read it from are both ignored for that decision, and a content_type that disagrees with the bytes is an ERROR rather than a silent correction. SVG is refused outright: it is a script document, not a photograph.
  THE IMAGE IS RE-ENCODED, which is how the EXIF goes. GPS coordinates in a profile photo are a home-address disclosure, and camera serials and timestamps are not yours to publish either. What gets stored is the re-encoded file; your original bytes are never written anywhere.
  REFUSED, NEVER REPAIRED: over 5 MB, under 64px on a side, over 8000px on a side or over 16 megapixels. Nothing is downscaled or converted on your behalf — a photo you did not choose is not your photo. Resize it and send it again.
  SIZE NOTE FOR SHELL CALLERS: base64 of a photo is usually 100 KB-2 MB, which is past the ~128 KB argv limit of a command line. Call this over the HTTP MCP endpoint, not by pasting the argument into a shell.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_type` | string | no | optional. "image/jpeg" or "image/png". If supplied it must MATCH what the bytes decode as. |
| `cv_id` | string | yes |  |
| `image_base64` | string | yes | the image file, base64 (standard or URL-safe alphabet, padding optional). A data: URL prefix is refused, not stripped. |

## `photo_clear`

**Photo Clear** — writes, closed-world · access: `write`.

Remove the profile photo: {cv_id}. The file is destroyed, not hidden.
  THIS IS NOT THE SAME AS HIDING IT. To stop showing a photo while keeping it, use photo_visibility_set(show=false) — the file stays and you can publish it again later. This tool destroys the file: there is no trash and no undo, because a stored photograph of a person is not something to keep a copy of after they asked for it to go.
  The published-in list is cleared too, so a photo uploaded afterwards starts hidden again rather than inheriting where the old one was shown.
  Your CV, its editions and its history are untouched: the photo is platform metadata, not document content, so removing it consumes no version.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |

## `photo_visibility_set`

**Photo Visibility Set** — writes, closed-world · access: `write`.

Show or hide the profile photo to READERS, per language edition: {cv_id, show, lang?}.
  PER EDITION, and that is the point rather than a detail. Photo norms differ by country: a Norwegian CV commonly carries a photograph, and a US-facing English edition commonly must not. So `photo_visibility_set(lang="no", show=true)` and `photo_visibility_set(lang="en", show=false)` is a normal, correct configuration — the one thing that is SUPPOSED to differ between editions of a CV that is otherwise held in parity. parity_check does not complain about it.
  OMIT `lang` to set every edition at once. Unlike basics_set, that is NOT the recommended default here — it is the one field where writing all editions the same way is usually the wrong answer.
  HIDING IS NOT DELETING. show=false stops readers seeing it and keeps the file; you can show it again later without re-uploading. photo_clear destroys the file.
  THE DEFAULT IS HIDDEN. A newly uploaded photo is shown to nobody until this tool says otherwise, and a CV with no photo cannot be set to show one — there would be nothing behind the frame.
  WHAT SHOWING IT MEANS, EXACTLY: readers of that edition's page see it, that edition's redacted PDF embeds it, and its image URL answers to anyone the PAGE would answer to — no wider. An unpublished CV shows nothing to anyone whatever this is set to, because the whole document is refused first.
  It changes no document content and consumes no version of your history: this is platform metadata, like visibility and the slug.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `lang` | string | no | one language edition, e.g. "no". OMIT to set every edition — rarely what you want for this field. |
| `show` | boolean | yes | true publishes the photo to readers of the edition(s); false hides it and keeps the file. |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-24, version 0.2.63. Regenerate rather than edit by hand.*
