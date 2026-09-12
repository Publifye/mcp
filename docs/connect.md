# Connecting a client

All three servers speak **Streamable HTTP** at a single endpoint and are authenticated. There is
nothing to install.

| Service | MCP endpoint |
|---|---|
| Darash | `https://darash-api.publifye.com/mcp` |
| Junifye | `https://junifye.publifye.com/mcp` |
| Lexifye | `https://lexifye.publifye.com/mcp` |

## Discovery

An unauthenticated request returns `401` with an RFC 9728 pointer, which is what a conformant client
follows automatically:

```console
$ curl -i -X POST https://darash-api.publifye.com/mcp \
    -H 'Content-Type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

HTTP/2 401
www-authenticate: Bearer resource_metadata="https://darash-api.publifye.com/.well-known/oauth-protected-resource"
```

```console
$ curl -s https://darash-api.publifye.com/.well-known/oauth-protected-resource
{
  "resource": "https://darash-api.publifye.com/mcp",
  "authorization_servers": ["https://lighthouse.publifye.pro"],
  "bearer_methods_supported": ["header"],
  "scopes_supported": ["darash-service:read", "darash-service:write", "darash-service:admin"]
}
```

## Authorisation server

`https://lighthouse.publifye.pro`, advertised at
`/.well-known/oauth-authorization-server` (RFC 8414):

| | |
|---|---|
| `authorization_endpoint` | `https://lighthouse.publifye.pro/oauth/authorize` |
| `token_endpoint` | `https://lighthouse.publifye.pro/oauth/token` |
| `registration_endpoint` | `https://lighthouse.publifye.pro/oauth/register` |
| `code_challenge_methods_supported` | `S256` |

PKCE is **required**, and Dynamic Client Registration (RFC 7591) is open — so a client that has
never seen these servers before can register itself and complete a login without anyone issuing it
credentials by hand. That is what makes them usable as a custom connector.

## Claude Desktop / Claude Code

Add as a remote MCP server (a custom connector). The OAuth flow runs in the browser on first use;
there is no key to paste.

```jsonc
{
  "mcpServers": {
    "darash": {
      "type": "http",
      "url": "https://darash-api.publifye.com/mcp"
    }
  }
}
```

## API key instead of OAuth

Every endpoint also accepts a personal API key in an `X-API-Key` header, for scripts, CI and clients
that do not implement OAuth. Keys are issued from your account on the product site.

```console
$ curl -s -X POST https://darash-api.publifye.com/mcp \
    -H 'Content-Type: application/json' \
    -H "X-API-Key: $DARASH_KEY" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Tool annotations

Every tool on every server carries `title`, `readOnlyHint`, `destructiveHint`, `idempotentHint` and
`openWorldHint`. These are **derived from each tool's declared access level**, not written by hand,
so a newly added tool cannot ship unannotated.

`openWorldHint: true` is set on exactly the tools that leave our estate — nothing else. Darash's
corpus is closed and fixed: a lookup returns the same answer tomorrow, and the hints say so, which
lets a client run reads in parallel without confirmation prompts.

Annotations are hints for clients, never a security boundary. Authorisation is enforced server-side.

## A longer walkthrough

[How to connect Claude, ChatGPT or Cursor to Darash, Junifye and Lexifye — MCP and DCR explained](https://blog.publifye.com/p/how-your-ai-connects-to-darash-junifye-and-lexifye-mcp-and-dcr)
covers every route in, including what actually happens when your assistant registers itself.
Also in Norwegian, Spanish, Chinese and Korean.
