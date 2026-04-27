from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import escape
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def build_statement_query(item_id: str) -> str:
    return f"""
SELECT ?property ?propertyLabel ?value ?valueLabel WHERE {{
  BIND(wd:{item_id} AS ?item)
  ?item ?p ?statement .
  ?property wikibase:claim ?p .
  ?statement ?ps ?value .
  ?property wikibase:statementProperty ?ps .

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],en\". }}
}}
ORDER BY ?propertyLabel
""".strip()


def fetch_sparql_bindings(query: str, endpoint: str = "https://query.wikidata.org/sparql"):
    params = urlencode({"query": query, "format": "json"})
    request_url = f"{endpoint}?{params}"
    request = Request(
        request_url,
        headers={
            "Accept": "application/sparql-results+json",
            "User-Agent": "bimprototpye02-quarto-site/1.0 (https://www.wikidata.org/wiki/Q138547468)",
        },
    )
    with urlopen(request) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("results", {}).get("bindings", [])


def properties_from_bindings(bindings):
    properties = defaultdict(list)
    for row in bindings:
        prop = row.get("propertyLabel", {}).get("value", "Unknown property")
        value_obj = row.get("value", {})
        value_type = value_obj.get("type", "literal")
        value_uri = value_obj.get("value", "")

        label = row.get("valueLabel", {}).get("value", value_uri)
        label = label if label else value_uri

        if value_type == "uri":
            properties[prop].append({"label": label, "url": value_uri, "kind": "entity"})
        else:
            properties[prop].append({"label": label, "url": "", "kind": "literal"})

    return properties


def property_frequency(properties):
    return Counter({k: len(v) for k, v in properties.items()})


def value_kind_breakdown(properties):
    counter = Counter()
    for values in properties.values():
        for v in values:
            counter[v.get("kind", "literal")] += 1
    return counter


def _bar_row(label: str, value: int, max_value: int, color: str) -> str:
    ratio = 0 if max_value == 0 else int((value / max_value) * 100)
    return (
        f'<div class="wd-bar-row">'
        f'<div class="wd-bar-label">{escape(label)}</div>'
        f'<div class="wd-bar-track"><div class="wd-bar-fill" style="width:{ratio}%;background:{color}"></div></div>'
        f'<div class="wd-bar-value">{value}</div>'
        f"</div>"
    )


def _property_chart_html(freq: Counter, top_n: int = 10) -> str:
    most_common = freq.most_common(top_n)
    if not most_common:
        return "<p>No properties found.</p>"

    max_value = max(v for _, v in most_common)
    rows = [
        _bar_row(label, value, max_value, "#1d4ed8")
        for label, value in most_common
    ]
    return "<div class=\"wd-bars\">" + "".join(rows) + "</div>"


def _kind_chart_html(kind_breakdown: Counter) -> str:
    entity_count = kind_breakdown.get("entity", 0)
    literal_count = kind_breakdown.get("literal", 0)
    total = entity_count + literal_count
    entity_pct = 0 if total == 0 else round((entity_count / total) * 100)
    literal_pct = 100 - entity_pct if total else 0

    return f"""
    <div class="wd-kind-wrap">
      <div class="wd-kind-bar">
        <div class="wd-kind-entity" style="width:{entity_pct}%"></div>
        <div class="wd-kind-literal" style="width:{literal_pct}%"></div>
      </div>
      <div class="wd-kind-legend">
        <span><span class="wd-kind-swatch" style="background:#1a1a18"></span><strong>{entity_count}</strong> Entity values</span>
        <span><span class="wd-kind-swatch" style="background:#c5a882"></span><strong>{literal_count}</strong> Literal values</span>
      </div>
    </div>
    """


def render_profile_html(item_id: str, properties) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    statement_count = sum(len(v) for v in properties.values())

    freq = property_frequency(properties)
    kind_breakdown = value_kind_breakdown(properties)

    cards = []
    for prop_name in sorted(properties.keys()):
        values_html = []
        for entry in properties[prop_name]:
            label = escape(entry["label"])
            if entry["url"]:
                url = escape(entry["url"])
                values_html.append(
                    f'<li><a href="{url}" target="_blank" rel="noopener">{label}</a></li>'
                )
            else:
                values_html.append(f"<li>{label}</li>")

        cards.append(
            f"""
            <section class=\"wd-card\">
              <h3>{escape(prop_name)}</h3>
              <ul>{''.join(values_html)}</ul>
            </section>
            """
        )

    return f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

  :root {{
    --paper: #f8f6f1;
    --ink: #1a1a18;
    --rule: #c8c4bb;
    --muted: #6b6760;
    --accent: #1a1a18;
    --highlight: #c5a882;
    --card-bg: #ffffff;
  }}

  .wd-shell {{
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    color: var(--ink);
    background: var(--paper);
    padding: 3rem 0 4rem;
    max-width: 960px;
    margin: 0 auto;
  }}

  /* ── Header ── */
  .wd-header {{
    border-top: 2px solid var(--ink);
    border-bottom: 1px solid var(--rule);
    padding: 1.5rem 0 1.25rem;
    margin-bottom: 2.5rem;
  }}
  .wd-header-eyebrow {{
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 0.5rem;
  }}
  .wd-header h2 {{
    font-family: 'EB Garamond', serif;
    font-size: 2.6rem;
    font-weight: 400;
    letter-spacing: -0.01em;
    margin: 0 0 0.75rem;
    line-height: 1.15;
  }}
  .wd-header-meta {{
    font-size: 0.8rem;
    color: var(--muted);
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    align-items: baseline;
  }}
  .wd-header-meta strong {{
    font-weight: 500;
    color: var(--ink);
  }}
  .wd-header-meta a {{
    color: var(--ink);
    text-decoration: underline;
    text-decoration-color: var(--rule);
    text-underline-offset: 3px;
  }}
  .wd-header-meta a:hover {{
    text-decoration-color: var(--ink);
  }}

  /* ── Catalogue numbers ── */
  .wd-stat-row {{
    display: flex;
    gap: 2.5rem;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid var(--rule);
    padding-bottom: 1.5rem;
  }}
  .wd-stat {{
    display: flex;
    flex-direction: column;
  }}
  .wd-stat-value {{
    font-family: 'EB Garamond', serif;
    font-size: 2rem;
    line-height: 1;
  }}
  .wd-stat-label {{
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.2rem;
  }}

  /* ── Insight panels ── */
  .wd-insights {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1px;
    background: var(--rule);
    border: 1px solid var(--rule);
    margin-bottom: 2.5rem;
  }}
  .wd-panel {{
    background: var(--card-bg);
    padding: 1.25rem 1.5rem;
  }}
  .wd-panel-title {{
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 1rem;
  }}

  /* ── Bar chart ── */
  .wd-bars {{
    display: grid;
    gap: 0.55rem;
  }}
  .wd-bar-row {{
    display: grid;
    grid-template-columns: minmax(100px, 1fr) 2fr 32px;
    gap: 0.6rem;
    align-items: center;
    font-size: 0.78rem;
  }}
  .wd-bar-label {{
    color: var(--ink);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .wd-bar-track {{
    height: 3px;
    background: #e5e2db;
    overflow: hidden;
  }}
  .wd-bar-fill {{
    height: 3px;
    background: var(--ink);
  }}
  .wd-bar-value {{
    font-size: 0.75rem;
    color: var(--muted);
    text-align: right;
  }}

  /* ── Kind breakdown ── */
  .wd-kind-wrap {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }}
  .wd-kind-bar {{
    display: flex;
    width: 100%;
    height: 4px;
    background: #e5e2db;
    overflow: hidden;
  }}
  .wd-kind-entity {{
    background: var(--ink);
  }}
  .wd-kind-literal {{
    background: var(--highlight);
  }}
  .wd-kind-legend {{
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    font-size: 0.78rem;
    color: var(--muted);
  }}
  .wd-kind-legend strong {{
    color: var(--ink);
    font-weight: 500;
  }}
  .wd-kind-swatch {{
    display: inline-block;
    width: 8px;
    height: 8px;
    margin-right: 4px;
    vertical-align: middle;
  }}

  /* ── Property grid ── */
  .wd-section-label {{
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--rule);
  }}
  .wd-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1px;
    background: var(--rule);
    border: 1px solid var(--rule);
  }}
  .wd-card {{
    background: var(--card-bg);
    padding: 1rem 1.25rem;
  }}
  .wd-card h3 {{
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 0.5rem;
  }}
  .wd-card ul {{
    margin: 0;
    padding: 0;
    list-style: none;
    color: var(--ink);
  }}
  .wd-card li {{
    font-family: 'EB Garamond', serif;
    font-size: 1rem;
    line-height: 1.5;
    padding: 0.15rem 0;
    border-bottom: 1px solid #f0ede8;
  }}
  .wd-card li:last-child {{
    border-bottom: none;
  }}
  .wd-card a {{
    color: var(--ink);
    text-decoration: underline;
    text-decoration-color: var(--rule);
    text-underline-offset: 2px;
  }}
  .wd-card a:hover {{
    text-decoration-color: var(--ink);
  }}
</style>

<div class="wd-shell">

  <header class="wd-header">
    <p class="wd-header-eyebrow">Catalogue Entry</p>
    <h2>Wikidata Statement Profile</h2>
    <div class="wd-header-meta">
      <span>Object ID&nbsp;<strong>{escape(item_id)}</strong></span>
      <span>Statements&nbsp;<strong>{statement_count}</strong></span>
      <span>Retrieved&nbsp;<strong>{generated_at}</strong></span>
      <span><a href="https://www.wikidata.org/wiki/{escape(item_id)}" target="_blank" rel="noopener">View source record ↗</a></span>
    </div>
  </header>

  <div class="wd-stat-row">
    <div class="wd-stat">
      <span class="wd-stat-value">{statement_count}</span>
      <span class="wd-stat-label">Statements</span>
    </div>
    <div class="wd-stat">
      <span class="wd-stat-value">{len(freq)}</span>
      <span class="wd-stat-label">Properties</span>
    </div>
    <div class="wd-stat">
      <span class="wd-stat-value">{kind_breakdown.get('entity', 0)}</span>
      <span class="wd-stat-label">Entity values</span>
    </div>
    <div class="wd-stat">
      <span class="wd-stat-value">{kind_breakdown.get('literal', 0)}</span>
      <span class="wd-stat-label">Literal values</span>
    </div>
  </div>

  <section class="wd-insights">
    <div class="wd-panel">
      <p class="wd-panel-title">Properties by statement count</p>
      {_property_chart_html(freq, top_n=10)}
    </div>
    <div class="wd-panel">
      <p class="wd-panel-title">Value type breakdown</p>
      {_kind_chart_html(kind_breakdown)}
    </div>
  </section>

  <p class="wd-section-label">All properties</p>
  <section class="wd-grid">
    {''.join(cards)}
  </section>

</div>
"""
