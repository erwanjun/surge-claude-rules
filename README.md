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

## Design decisions

- Anthropic-owned suffixes are used instead of duplicating every subdomain. For example, `DOMAIN-SUFFIX,anthropic.com` already covers `api.anthropic.com`, `mcp-proxy.anthropic.com`, and `assets-proxy.anthropic.com`.
- Broad `DOMAIN-KEYWORD,datadog`, `DOMAIN-KEYWORD,sentry`, and `DOMAIN-KEYWORD,sift` rules are included in the complete list for conservative coverage. Exact known telemetry hosts remain listed as documentation and fallback coverage. These keyword rules can capture unrelated services across the entire device; the core list avoids them.
- NTP is intentionally excluded. NTP distributes UTC time, not the operating system timezone, and a destination-only Claude rule should not redirect every application's UDP/123 traffic.
- The IP fallbacks use Anthropic's documented inbound client destinations (`160.79.104.0/23` and `2607:6bc0::/48`). The broader `160.79.104.0/21` documented by Anthropic is an outbound source range and is not used as a client destination fallback.
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
