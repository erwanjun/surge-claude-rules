# Surge Rules for Claude

Maintained Surge rule sets for Claude, Claude Code, Claude web apps, and related Anthropic services.

The project was created as a documented replacement for older Claude lists that only covered a few domains. The rules are based on Anthropic's current network documentation and the domain inventory published by [Net.Coffee](https://ip.net.coffee/claude/site.html), with several safety corrections described below.

## Recommended configuration

Add the complete list before broad regional, AI-service, or final rules:

```ini
RULE-SET,https://raw.githubusercontent.com/erwanjun/surge-claude-rules/main/Surge/Claude.list,Claude-Policy,update-interval=86400
```

Replace `Claude-Policy` with the name of the Surge policy group that should carry Claude traffic.

For a smaller list that avoids shared third-party infrastructure, use:

```ini
RULE-SET,https://raw.githubusercontent.com/erwanjun/surge-claude-rules/main/Surge/Claude-Core.list,Claude-Policy,update-interval=86400
```

## Rule sets

| File | Purpose |
| --- | --- |
| `Surge/Claude.list` | Recommended complete list, including Claude Code downloads, telemetry, support widgets, and Anthropic network fallbacks. |
| `Surge/Claude-Core.list` | Low-collateral list limited to Anthropic/Claude domains, uniquely branded infrastructure, and Anthropic network fallbacks. |

The complete list includes shared hosts such as `raw.githubusercontent.com`, `storage.googleapis.com`, Sentry, Statsig, Intercom, and Datadog intake endpoints. It also includes broad `datadog`, `sentry`, and `sift` keyword matches. Surge rules are destination-based, so unrelated applications using matching hosts will also use the selected policy. Use the core list if that is undesirable.

Both lists cover `claude.app` and its subdomains, including the dynamically generated live preview hosts used by Claude Desktop. [Claude Desktop network requirements](https://code.claude.com/docs/en/desktop#network-access-requirements)

## Optional network dependencies

Use your existing network policy for these shared destinations, or add an individual rule when you want the corresponding feature to use your Claude policy.

| Destination | When Claude uses it |
| --- | --- |
| `github.com` | Cloning GitHub-hosted Claude Code plugin marketplaces and plugins. |
| `registry.npmjs.org` | Installing npm-based plugins and their dependencies, running `npx` MCP servers, and installing Claude Code with npm or Bun. |
| `withpersona.com` and its subdomains | Completing identity verification when Claude prompts for it. |

Add only the lines you need to your Surge `[Rule]` section, above any broader rules for those destinations. Replace `Claude-Policy` with your policy group. Each line applies to all matching traffic, including traffic from other apps.

```ini
DOMAIN,github.com,Claude-Policy
DOMAIN,registry.npmjs.org,Claude-Policy
DOMAIN-SUFFIX,withpersona.com,Claude-Policy
```

[Claude Code network requirements](https://code.claude.com/docs/en/corporate-proxy#network-access-requirements) · [Claude identity verification](https://support.claude.com/en/articles/14328960-identity-verification-on-claude) · [Persona network allowlist](https://docs.withpersona.com/security#standard-domains-for-allowlisting)

## Design decisions

- Anthropic-owned suffixes are used instead of duplicating every subdomain. For example, `DOMAIN-SUFFIX,anthropic.com` already covers `api.anthropic.com`, `mcp-proxy.anthropic.com`, and `assets-proxy.anthropic.com`.
- Broad `DOMAIN-KEYWORD,datadog`, `DOMAIN-KEYWORD,sentry`, and `DOMAIN-KEYWORD,sift` rules are included in the complete list for conservative coverage. Exact known telemetry hosts remain listed as documentation and fallback coverage. These keyword rules can capture unrelated services across the entire device; the core list avoids them.
- NTP is intentionally excluded. NTP distributes UTC time, not the operating system timezone, and a destination-only Claude rule should not redirect every application's UDP/123 traffic.
- The IP fallbacks use Anthropic's documented inbound destinations (`160.79.104.0/23`, `153.61.224.0/22`, and `2607:6bc0::/48`).
- For server-side allowlists, Anthropic publishes `160.79.104.0/21` and `153.61.208.0/20` as outbound source ranges for requests such as MCP tool calls.
- IP and ASN rules follow domain rules and use `no-resolve`.

## Sources

- [Anthropic: Enterprise network configuration for Claude Code](https://code.claude.com/docs/en/corporate-proxy)
- [Anthropic: API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses)
- [Net.Coffee: Claude domain routing inventory](https://ip.net.coffee/claude/site.html)
- [Previous Blackmatrix7 Claude list](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Surge/Claude)

## Validation

Run:

```bash
python3 scripts/validate_rules.py
```

The validator checks rule types, domains, IP networks, ASN syntax, duplicates, and that the complete list remains a superset of the core list.

## Scope

These files only select network destinations. They do not change account identity, browser fingerprints, device identifiers, system timezone, or Anthropic account eligibility.

## License

MIT
