# Supify — Project Guide

**The business problem, the domain model, the platform architecture, and every user workflow.**

This document is about *what Supify is and why it exists*. It deliberately says almost nothing about
React. If you want hooks, routing and component patterns, read the companion document
`REACT_CONCEPTS_DEEP_DIVE.md` instead — the two are meant to be read separately and neither repeats
the other.

Everything below was written by reading the code in this repository, not the pitch. Where the
implementation falls short of the design intent, it says so. A guide that hides the gaps is useless
in a viva, because the gaps are exactly what you get asked about.

**Stack:** Vite 8 · React 19.2 · react-router-dom 6.30 · Tailwind CSS 3.4 · JSON fixtures over HTTP.
No backend. No database. Not yet.

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [The problem: the asymmetry of trust](#2-the-problem-the-asymmetry-of-trust)
3. [The Supify solution and its domain invariants](#3-the-supify-solution-and-its-domain-invariants)
4. [Data and architecture](#4-data-and-architecture)
5. [Complete user workflows](#5-complete-user-workflows)
6. [The tactile visual design system](#6-the-tactile-visual-design-system)
7. [Built vs. stubbed: an honest inventory](#7-built-vs-stubbed-an-honest-inventory)
8. [Running it, and where everything lives](#8-running-it-and-where-everything-lives)

---

## 1. Executive summary

Supify is a B2B supplier discovery and verification platform. A buyer — think a procurement lead at
a manufacturer who needs 80,000 fasteners a month from someone who will still exist in six months —
comes to Supify to find suppliers and, more importantly, to find out whether those suppliers are what
they say they are.

The one-line version of the product thesis, taken from `docs/CLAUDE.md`:

> A buyer cannot cheaply observe whether a supplier is what they claim to be.

Every feature in the codebase has to reduce either the cost of **finding** a supplier or the cost of
**trusting** one. The project calls this the **Asymmetry Razor**, and it is used as a scope-control
test: if a proposed feature does neither, it gets cut.

What makes Supify different from every other supplier directory is a single design decision that
propagates everywhere. Most platforms render trust as a green tick. Supify refuses to. A green tick
compresses three separate facts — *what* we concluded, *how* we checked, and *when* we last looked —
into one bit, and two of those three facts are the ones a buyer actually needs. So Supify renders all
three, on every claim, every time. A supplier profile doesn't tell you "verified." It tells you
"Verified — registry check, 4 days ago, valid until 15 Nov 2026," and then lets you open the evidence
that produced that conclusion.

The application ships four surfaces:

| Surface | Who it's for | What it does |
| --- | --- | --- |
| **Landing** (`/`) | Everyone | Explains the thesis; the hero is itself a rendered claim ledger |
| **Solutions / Discovery** (`/search`) | Buyers | Multi-attribute search with all filter state held in the URL |
| **Supplier profile** (`/suppliers/:id`) | Buyers | Facts, the claim ledger, the trust panel, evidence inspector |
| **Comparison** (`/compare`) | Buyers | Side-by-side table; the comparison set is a shareable URL |
| **Verification engine** (`/verification`) | Buyers + verifiers | Live audit run, D&B financials, EcoVadis ESG, sanctions screen, evidence queue |
| **Supplier workspace** (`/supplier/onboarding`) | Suppliers | Four-step listing wizard with local draft autosave |

Data comes from two JSON fixtures in `public/`, fetched over HTTP through a repository class that
simulates 200 ms of network latency. Five suppliers, five verification tasks. They were written to be
hostile to the UI rather than flattering to it, which is covered in §4.

---

## 2. The problem: the asymmetry of trust

### 2.1 It's an information asymmetry, and that has consequences

A supplier knows whether their ISO certificate is current, whether that factory photo is their
factory, and whether they can actually hit 80,000 units a month. The buyer knows none of this. The
seller holds private information about quality that the buyer cannot verify before committing.

This is Akerlof's market for lemons, in industrial procurement. When buyers can't distinguish good
suppliers from bad ones, they price for the average. Good suppliers — who invested real money in real
certification — get paid the average price, so eventually they stop bothering, and the average drops
again. The asymmetry doesn't just inconvenience buyers. It actively punishes the honest supplier.

So the problem isn't "buyers need a directory." Directories are everywhere and they're free. The
problem is that **verification is expensive and its results are not portable**.

### 2.2 Why the existing instruments fail

**Static PDF certificates.** A PDF is a photograph of a fact, taken at an unknown moment, by an
unknown party, potentially of somebody else's fact. It has no issuer signature the buyer can check,
no expiry the interface enforces, and nothing stopping it from being edited in a text editor. A buyer
receiving a PDF has learned that a supplier is willing to send a PDF.

**Point-in-time audits.** An audit is genuinely informative on the day it happens. Then it starts
decaying, silently, at a rate nobody publishes. An eighteen-month-old audit is displayed with exactly
the same visual weight as a three-day-old one — usually as a badge with no date on it at all. Decay is
invisible, so buyers implicitly treat all audits as current, which is precisely when they're most
dangerous.

**Binary checkmarks.** The worst of the three, because it's the one that looks like a solution. A
boolean `isVerified: true` cannot express *by what method*, *how recently*, or *until when*. It can't
distinguish "a government registry API confirmed this identifier four days ago" from "somebody typed
it into a form." Both render as the same green tick. And because there's nowhere to put an expiry,
the tick stays lit after the underlying attestation lapses. Trust expires; the checkmark doesn't.

The codebase has this as a hard rule — invariant 1 in `docs/CLAUDE.md`:

> **Never add a boolean verification flag.** No `isVerified`, `hasGST`, `isTrusted`. Verification
> state is always `{ method, verifiedAt, validUntil, attestor, evidence }`. A boolean cannot express
> *how*, *when*, or *until when*, and those are the entire point.

### 2.3 What it costs both sides

**Buyers** run the same background check everybody else already ran — company registry lookups,
sanctions screening, reference calls, certificate chasing, sometimes a physical site visit — and then
throw the result away in a spreadsheet nobody else can see. Weeks of work, repeated across every buyer
evaluating the same supplier, with no shared memory of the result.

**Suppliers** experience the mirror image. A legitimate manufacturer re-proves the same facts to every
prospect, in whatever format each one demands, and still loses to a competitor with a better
photograph. There's no way to accumulate credibility. Effort spent proving yourself to buyer A is
worth nothing when buyer B arrives.

Both sides burn money producing the same knowledge over and over and then discarding it. That waste
*is* the market opportunity.

### 2.4 The honest caveat

Supify does not abolish verification cost. Somebody still has to call the registry, read the
certificate, and walk the factory floor. What the platform does is make the result **portable,
inspectable, and honestly dated**, so the cost is paid once and the conclusion is auditable by
everybody afterwards. That's a real improvement, and it is a narrower claim than "we eliminate
supplier risk." The UI is careful not to overstate it — see the Decision Safeguard copy in
`VerificationDashboard.jsx:414`.

---

## 3. The Supify solution and its domain invariants

### 3.1 The Trust Triple: state + method + recency

This is the single most important idea in the product, and it's enforced structurally rather than by
convention. Trust is never one value. It is always three, travelling together:

| Component | Question it answers | Example |
| --- | --- | --- |
| **State** | What did we conclude? | `verified` |
| **Method** | How did we reach that? | `third_party_api` → "Registry check" |
| **Recency** | When, and until when? | checked 4 days ago · valid until 15 Nov 2026 |

Drop any one of the three and you get a lie of omission. State alone is the green tick. State plus
method with no date is an audit badge that never ages. State plus date without method can't
distinguish a registry sync from a self-declaration.

The shape is created at the API boundary in `src/entities/supplier/model/adapter.js:39-49` and there
is nowhere in the UI to construct a trust object without it:

```js
trust: {
  band: wire.trust?.band || 'unverified',
  method: wire.trust?.method || 'self_declared',
  methodLabel: wire.trust?.method_label || methodLabels[wire.trust?.method] || 'Self-declared',
  verifiedAt: wire.trust?.verified_at || null,
  validUntil: wire.trust?.valid_until || null,
  lastChecked: wire.trust?.last_checked || 'Pending check',
  overallScore: wire.trust?.overall_score || 0,
  pillars: (wire.trust?.pillars || []).map(([name, score]) => ({ name, score })),
  gatesApplied: wire.trust?.gates_applied || [],
},
```

Look at the defaults. Missing band becomes `'unverified'`, not blank. Missing method becomes
`'self_declared'`, not blank. Missing date becomes `'Pending check'`, not an empty string. That is
invariant 4 — *never render an unknown state as neutral* — implemented at the boundary rather than
left to each component to remember. An empty field reads to a human as tacit approval, so the domain
model doesn't permit an empty field.

And the renderer refuses to show a band without its method and date.
`src/entities/trust/ui/TrustBand.jsx:55-61`:

```jsx
{showMethod && (
  <div className="text-xs text-on-surface-variant flex items-center gap-1">
    <span>{trust.methodLabel || 'Self-declared'}</span>
    <span className="opacity-60">·</span>
    <span>{trust.lastChecked || 'Recently checked'}</span>
  </div>
)}
```

**Methods recognised by the system** (`adapter.js:1-10`) — note that these are labels for *how a human
or a machine established something*, and they are ordered by strength:

`self_declared` → "Self-declared" · `document_review` → "Document review" ·
`third_party_api` → "Registry check" · `human_audit` → "Human audit" · `site_audit` → "Site audit" ·
`site_visit` → "Site visit" · `registry_and_audit` → "Registry check & audit" ·
`comprehensive_audit` → "Comprehensive audit & API sync"

### 3.2 Bands, and the gates that override them

A **band** is the headline standing of a supplier. Four exist, defined in
`src/entities/trust/ui/TrustBand.jsx:1-26`:

| Band | Label shown | Icon | Meaning |
| --- | --- | --- | --- |
| `unverified` | Unverified | `error_outline` | Nothing independently established |
| `basic` | Basic Standing | `hourglass_empty` | Some claims checked, coverage incomplete |
| `verified` | Verified | `verified` | Core claims independently established and current |
| `audited` | Audited & High Trust | `verified_user` | Includes human audit evidence |

Each band carries an icon *and* text *and* colour, never colour alone. That's invariant 5, and it's
both an accessibility requirement (WCAG 1.4.1) and an information-integrity one — a colour-blind buyer
and a screen-reader user must get the same three facts as everyone else.

A **gate** is a caveat that sits on top of the band and contradicts it. Gates are the mechanism that
stops a band from quietly overstating a supplier. `src/entities/trust/ui/TrustPanel.jsx:60-68` renders
them in warning peach, above the fold, not hidden in a tooltip:

```jsx
{trust.gatesApplied && trust.gatesApplied.length > 0 && (
  <div className="bg-brand-peach text-primary p-3 rounded-lg flex items-start gap-2 border border-primary/20">
    <span className="material-symbols-outlined text-base text-primary mt-0.5">warning</span>
    <div className="flex flex-col gap-0.5 text-xs">
      <strong className="font-semibold">Trust Gate Applied</strong>
      <span>{trust.gatesApplied.join(' · ')}</span>
    </div>
  </div>
)}
```

Three gates appear in the fixture data: `"Quality evidence is incomplete"`,
`"Identity has not been independently established"`, and `"A prior attestation has lapsed"`.

### 3.3 The four trust pillars

Band is the headline; **pillars** are the decomposition. Rather than one opaque score, trust is broken
into four axes so a buyer can see *where* the confidence comes from and where it doesn't.

| Pillar | What it covers |
| --- | --- |
| **Identity** | Is this a real, traceable legal entity? Registry presence, tax identifiers. |
| **Legal** | Registration standing, sanctions exposure, corporate good standing. |
| **Quality** | Certifications, quality management systems, audit outcomes. |
| **Capability** | Can they actually produce what they claim? Capacity, throughput, lead time. |

The brief's example numbers — Identity 92, Legal 86, Quality 68, Capability 58 — are real. They belong
to `aravind-fasteners`, the strongest supplier in the fixture set. Here is every supplier, so you can
see the spread the UI has to render:

| Supplier | Band | Identity | Legal | Quality | Capability | Derived score | Gate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Aravind Fasteners | `verified` | 92 | 86 | 68 | 58 | **76** | — |
| Monarch Industrial | `basic` | 74 | 57 | 18 | 26 | **44** | Quality evidence is incomplete |
| Kalyani Textiles | `basic` | 66 | 58 | 34 | 20 | **45** | A prior attestation has lapsed |
| Narmada Fabrication | `unverified` | 12 | 0 | 15 | 22 | **12** | Identity not independently established |
| Deccan Polymers | `unverified` | 8 | 0 | 0 | 12 | **5** | Identity not independently established |

Notice Aravind: 92 on Identity but 58 on Capability. A single blended number would hide that. The
decomposition tells a buyer something actionable — *this company definitely exists and is legally
clean, but nobody has independently confirmed it can hit the volume it advertises.* That's a
different procurement decision from "76% trustworthy."

Pillars render as labelled bars with the numeric value beside them
(`TrustPanel.jsx:43-56`), never as a bar alone:

```jsx
{(trust.pillars || []).map((pillar) => (
  <div key={pillar.name} className="flex flex-col gap-1">
    <div className="flex justify-between text-xs">
      <span className="text-white/90 font-medium">{pillar.name}</span>
      <span className="text-brand-mint font-semibold">{pillar.score}%</span>
    </div>
    <div className="w-full bg-white/20 rounded-full h-1.5 overflow-hidden">
      <div className="bg-brand-mint h-1.5 rounded-full transition-all duration-500"
           style={{ width: `${pillar.score}%` }} />
    </div>
  </div>
))}
```

> ⚠️ **An honest note on the derived score.** `docs/CLAUDE.md` invariant 2 says *never compute a trust
> score on the client* — the server computes, the client renders, because a score computed in the
> browser is a score that can be reverse-engineered and forged. The fixtures carry no `overall_score`
> field, so both `SupplierCard.jsx:25-27` and `VerificationDashboard.jsx:84-86` currently fall back to
> averaging the pillars in the browser. This is a genuine invariant violation. It is survivable only
> because there is no backend yet; the moment one exists, `overall_score` must come down the wire and
> the client-side average must be deleted. If an examiner asks you to name a flaw in this codebase,
> this is the best answer you have.

### 3.4 The Verifiable Claim Ledger

A **claim** is one assertion a supplier makes about itself. Not a profile field — an assertion, with
provenance attached. Every claim in the system carries the same envelope
(`adapter.js:50-67`):

```js
claims: (wire.claims || []).map((claim) => ({
  key: claim.key,
  label: claim.label,
  value: claim.value,
  state: claim.state,
  method: claim.method,
  methodLabel: claim.method_label || methodLabels[claim.method] || 'Self-declared',
  verifiedAt: claim.verified_at,
  validUntil: claim.valid_until,
  evidenceCount: claim.evidence_count || (claim.evidence ? claim.evidence.length : 0),
  evidence: (claim.evidence || []).map((item) => ({
    kind: item.kind,
    kindLabel: evidenceKindLabels[item.kind] || item.kind,
    label: item.label,
    issuedOn: item.issued_on,
  })),
})),
```

Six claim states exist, each with its own icon, badge text and colour treatment
(`src/entities/claim/ui/ClaimRow.jsx:19-50`):

| State | Badge | Meaning |
| --- | --- | --- |
| `verified` | Verified | A verifier established this against evidence |
| `under_review` | Under Review | Submitted, a verifier is working it |
| `needs_more_info` | Needs Info | Verifier bounced it back to the supplier |
| `submitted` | Submitted | In the queue, untouched |
| `revoked` | Revoked | Was established, then withdrawn |
| `expired` | Expired | Attestation lapsed and was not renewed |

`revoked` and `expired` matter more than the happy path. Most platforms delete a revoked claim.
Supify renders it, in error colours, with the word "Revoked" on it — because the *fact that a claim was
withdrawn* is the single most informative thing on the page. Deccan Polymers has a revoked quality
management claim in the fixtures specifically to force this path to exist.

**Evidence kinds** (`adapter.js:12-18`): `document` · `photo` · `registry_response` → "Registry check"
· `audit_report` · `reference_contact` → "Reference call".

**Expiry is computed and rendered, not assumed.** `ClaimRow.jsx:15-17` and `:83-86`:

```js
const validity = claim.validUntil
  ? `Attestation ${new Date(claim.validUntil).getTime() < Date.now() ? 'lapsed' : 'valid until'} ${formatDate(claim.validUntil)}`
  : null
```

The same date that reads "valid until 15 Nov 2026" today will read "lapsed 15 Nov 2026" on 16 Nov,
in red, automatically, with no human intervention and no cron job. The interface ages honestly
because the comparison is against `Date.now()` at render time. This is the single cheapest and most
valuable line in the trust model.

**The evidence inspector and the SHA-256 record.** Clicking "Inspect" on any claim opens a modal
(`src/features/supplier-profile/ui/SupplierProfile.jsx:237-297`) showing the asserted value, the
verification method, the evidence count, and a ledger hash:

```jsx
<div className="p-3 bg-brand-mint/20 rounded-lg border border-brand-teal/30 text-xs text-brand-teal flex flex-col gap-1">
  <div className="flex items-center gap-1 font-bold">
    <span className="material-symbols-outlined text-sm">enhanced_encryption</span>
    <span>SHA-256 Ledger Record</span>
  </div>
  <span className="font-mono text-[10px] break-all opacity-80">
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  </span>
</div>
```

The *intent* is content-addressed evidence: hash the artifact on ingest, store the hash in an
append-only ledger, and let anyone re-hash the file to prove it wasn't swapped. The *implementation*
is presently a hardcoded constant — and as it happens, `e3b0c442...b855` is the SHA-256 of the empty
string, which is a nicely appropriate placeholder. Real hashing belongs on the server when one exists.
Know this before you're asked.

### 3.5 The twelve invariants, and where each one lives in code

These come from `docs/CLAUDE.md`. They're the rules that are easiest to break by accident, which is
exactly why they're written down.

| # | Invariant | Where you can see it |
| --- | --- | --- |
| 1 | Never add a boolean verification flag | `adapter.js:39-49` — trust is an object, never a bool |
| 2 | Never compute a trust score on the client | ⚠️ **currently violated** — `SupplierCard.jsx:25-27` |
| 3 | Never render trust without method and date | `TrustBand.jsx:55-61` |
| 4 | Never render unknown as neutral | `adapter.js:41-45` — explicit fallbacks |
| 5 | Never convey trust by colour alone | `TrustBand.jsx:1-26` — icon + label + colour on every band |
| 6 | Supplier code paths never write attestation state | `OnboardingScreen.jsx` writes drafts only |
| 7 | Never hardcode a claim type | `ClaimRow.jsx:19-52` — lookup map, no `switch` |
| 8 | Never import across features | verified: no `features/*` imports another `features/*` |
| 9 | Never render trust outside entity components | `entities/trust/*`, `entities/claim/*` |
| 10 | Never consume wire shapes in the UI | `adapter.js` — snake_case in, camelCase out |
| 11 | Anything shareable belongs in the URL | `SearchScreen.jsx:42-54`, `ComparisonScreen.jsx:50-58` |
| 12 | Never lose a supplier's work | `OnboardingScreen.jsx:35-40` — autosave on every keystroke |

Invariant 7 deserves a moment. There is no `switch (claimType)` anywhere in this codebase. Claim
rendering is driven by a lookup object keyed on state, so adding a new certification type is a data
change in JSON, not a code change in JSX. That's what stops the UI from accumulating a 40-branch
conditional as the registry grows.

---

## 4. Data and architecture

### 4.1 Feature-Sliced Design, dependencies pointing one way

```
  app        shell, routing, providers, cross-feature wiring
   ↓
  features   landing · discovery · supplier-profile · comparison
             verification-dashboard · verification-review · supplier-onboarding
   ↓
  entities   supplier · claim · trust · user
   ↓
  shared     ui primitives · api client
```

Dependencies point **downward only**. Never upward, never sideways between features. If
`features/discovery` needs something from `features/verification-review`, that's not a shared
component — that's a signal it belongs in `entities/` or the wiring belongs in `app/`.

The decision procedure from `docs/CLAUDE.md`, which is worth memorising because it answers 90% of
"where does this file go" arguments:

- Used by more than one feature, knows nothing about the domain → `shared/ui`
- Used by more than one feature, *does* know about the domain → `entities/<thing>`
- Used by exactly one feature → that feature
- Wires two features together → `app`

Concretely: `Modal` and `Toast` know nothing about suppliers, so they're in `shared/ui`. `TrustBand`
knows what a band is, so it's in `entities/trust`. `SearchScreen` is discovery and nothing else, so
it's in `features/discovery`. The toast state that any feature might trigger lives in `app/App.jsx`.

### 4.2 The wire/domain boundary

The backend doesn't exist, so its shapes *will* change. The defence is a hard boundary: exactly one
module knows what the server's JSON looks like, and it's `adapter.js`.

Wire side is snake_case, nullable, and full of holes: `legal_name`, `trade_name`, `lead_time`,
`verified_at`, `trust.pillars` as an array of `[name, score]` tuples.

Domain side is camelCase, total, and safe to render: `legalName`, `tradeName`, `leadTime`,
`verifiedAt`, `trust.pillars` as `{ name, score }` objects.

```js
pillars: (wire.trust?.pillars || []).map(([name, score]) => ({ name, score })),
```

That one line is the entire reason `TrustPanel` can write `pillar.name` instead of `pillar[0]`. If the
backend later sends objects instead of tuples, one line changes and no component notices. This is
invariant 10, and it's the cheapest insurance in the codebase.

### 4.3 The repository pattern

`src/shared/api/contract.js` defines an abstract class whose every method throws:

```js
export class SupplierRepository {
  async search(_filters) {
    throw new Error('SupplierRepository.search must be implemented')
  }
  async getById(_supplierId) { /* ... */ }
  async getVerificationQueue() { /* ... */ }
  async getVerificationTask(_taskId) { /* ... */ }
}
```

`src/shared/api/supplierRepository.js` extends it with `FixtureSupplierRepository`, which fetches the
JSON files, filters and sorts in memory, and maps through the adapter. The whole application imports
one singleton:

```js
export const supplierRepository = new FixtureSupplierRepository()
```

Swapping fixtures for a real API later means writing `HttpSupplierRepository extends
SupplierRepository` and changing one export line. Not one component changes. That's the point of
declaring the contract separately from the implementation — in a language with no interfaces, a
throwing base class is how you write one down.

Every call also pays a deliberate 200 ms tax (`supplierRepository.js:6, 12-19`):

```js
const SIMULATED_LATENCY_MS = 200

async function fetchJson(url) {
  await delay(SIMULATED_LATENCY_MS)
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status} for ${url}`)
  }
  return response.json()
}
```

That delay is a feature. Instant local fixtures let you build a UI with no loading state at all, and
then it falls apart the first time it meets a real network. Forcing the latency means every screen had
to grow a real loading state during development.

### 4.4 Adversarial fixtures

From `docs/CLAUDE.md`:

> Fixtures must be **adversarial toward our own UI**. Seed data full of tidy happy paths is how a demo
> passes and the real product breaks.

Five suppliers, deliberately awkward:

| Supplier | What it's there to break |
| --- | --- |
| **Aravind Fasteners** | The happy path — `verified`, registry-checked, current until 15 Nov 2026 |
| **Monarch Industrial** | `basic` with a gate; last checked *7 weeks ago*; tests stale-but-not-expired |
| **Kalyani Textiles** | Attestation **lapsed 10 Aug 2026**; 72-char legal name; tests the expiry path |
| **Narmada Fabrication** | **87-character legal name**; `unverified`; tests every layout that assumed names are short |
| **Deccan Polymers** | Nothing ever checked; a **revoked** claim; tests the floor |

And five verification tasks covering every queue state — `in_review`, `awaiting_supplier`, `queued`,
`escalated` — including `VT-1090`, which has **11 evidence items and `requires_dual: true`**
(dual-control review), and `VT-1088`, which is escalated and *overdue by 2 days*. The task
`VT-1081` deliberately omits `evidence_count` entirely, so the adapter's `|| 0` fallback gets
exercised.

That 87-character name is not a typo. It's `Narmada Advanced Custom Fabrication and Integrated
Industrial Solutions Private Limited`, and it exists purely to break `text-overflow` assumptions. This
is why `SupplierCard` uses `line-clamp-1` and `truncate` in specific places rather than trusting
content to behave.

---

## 5. Complete user workflows

### 5.0 The actual route table

Straight from `src/app/App.jsx:41-122`. Note the aliases — several paths intentionally resolve to the
same screen so that older links and differently-worded nav items all land somewhere sensible:

| Path | Screen | Notes |
| --- | --- | --- |
| `/` | `LandingScreen` | |
| `/search` · `/solutions` · `/discovery` | `SearchScreen` | three aliases, one component |
| `/compare` | `ComparisonScreen` | reads `?ids=a,b,c` |
| `/suppliers/:supplierId` | `SupplierProfile` | dynamic segment |
| `/verification` · `/verify` · `/verifier/queue` | `VerificationDashboard` | reads `?supplier=` |
| `/verifier/task/:taskId` | `VerificationTaskDetail` | |
| `/supplier` · `/supplier/onboarding` | `OnboardingScreen` | |
| `*` | `NotFound` | catch-all, must be last |

### 5.1 Discovery — search that lives in the URL

**Route:** `/search` (or `/solutions`, or `/discovery`) · **File:**
`src/features/discovery/ui/SearchScreen.jsx`

A buyer arrives and needs to narrow five thousand suppliers to five. Supify gives them five
simultaneous filters:

1. **Free-text query** — matched against legal name, trade name, category, location, description,
   region, *and the text of every claim*. That last part matters: searching "ISO 9001" finds suppliers
   whose claims mention it, not just ones with it in the company name.
2. **Trust band** — All / Verified / Audited / Basic / Unverified, as a segmented control
3. **Region** — North America / Europe / Asia Pacific / India
4. **Industry** — Textiles / Packaging / Electronics / Machining / Industrial Fasteners / Sheet-metal
5. **Sort** — Relevance / Rating / Lead Time / MOQ

The defining architectural decision here is that **none of that is component state**. All of it lives
in the query string, because of invariant 11: *if a user might bookmark it, send it to a colleague, or
reach it with the back button, it is URL state.*

```jsx
const [searchParams, setSearchParams] = useSearchParams()

const query = searchParams.get('q') || ''
const band = searchParams.get('band') || ''
const region = searchParams.get('region') || 'All Regions'
const industry = searchParams.get('industry') || 'All Industries'
const sortBy = searchParams.get('sort') || 'relevance'
```

Writing back is centralised in one function (`SearchScreen.jsx:42-54`) that keeps the URL clean by
deleting any parameter set to its default:

```jsx
function updateParams(next) {
  const updated = new URLSearchParams(searchParams)
  updated.delete('prompt')
  Object.entries(next).forEach(([key, value]) => {
    if (value && value !== 'All Regions' && value !== 'All Industries' && value !== 'relevance') {
      updated.set(key, value)
    } else {
      updated.delete(key)
    }
  })
  setSearchParams(updated)
}
```

So `/search?q=fasteners&band=verified` is a complete, shareable description of a search. Paste it into
Slack and your colleague sees exactly your results. Hit back and you get your previous filter set,
because each change pushed a history entry. You didn't write any of that behaviour — the URL gave it
to you free.

**Results** render in a three-column responsive grid, with all three states handled: a spinner while
loading, the grid when populated, and a designed empty state with a "Clear All Filters" escape hatch
when nothing matches (`SearchScreen.jsx:276-301`). The empty state is not an afterthought; zero-result
searches are listed in the definition of done.

Two extra client-side filter chips sit outside the URL — **ISO 9001** and **Lead Time < 14 days** —
held in ordinary component state (`extraFilter`). These are arguably an invariant-11 violation: they're
shareable-looking filters that don't survive a page reload. Small, but worth knowing.

> ⚠️ **Two real bugs in this screen, verified against the fixtures.**
>
> 1. **The region filter always returns zero results.** All five suppliers are Indian, but their
>    locations are written `"Ludhiana, Punjab, IN"` and none of them has the optional `region` field.
>    The matcher (`supplierRepository.js:40`) tests `supplier.region === region ||
>    supplier.location.toLowerCase().includes(region.toLowerCase())` — and `"ludhiana, punjab, in"`
>    does not contain the substring `"india"`. Every one of the four region options yields nothing.
> 2. **The industry dropdown is half fictional.** Only *Textiles*, *Industrial fasteners* and
>    *Sheet-metal fabrication* match anything. *Packaging*, *Electronics* and *Machining* return zero,
>    because the fixture categories are `Precision machined parts` and `Injection moulded components`
>    — "Machining" is not a substring of "Precision machined parts".
>
> Also, the "Apply Filters" button is `onClick={() => {}}` — a genuine no-op. Filtering is already
> live-on-change, so the button is decorative. Either wire it or delete it.

### 5.2 Supplier profile — the ledger, the panel, the inspector

**Route:** `/suppliers/:supplierId` · **File:**
`src/features/supplier-profile/ui/SupplierProfile.jsx`

The profile is a two-column layout. Left: identity header, a four-up quick-facts card (capacity, MOQ,
lead time, rating), the facility description, and then the claim ledger. Right: the `TrustPanel` and
the Asymmetry Razor guarantee note.

The ledger is the centrepiece, and its section heading states the contract explicitly — *"Every claim
shows method, date, and evidence."* Each claim renders through `ClaimRow`, which is in `entities/`
because invariant 9 says trust is rendered in exactly one place and nowhere else.

**Claim inspection is deep-linkable.** Opening a claim writes to the URL, not to state
(`SupplierProfile.jsx:79-87`):

```jsx
const handleToggleClaim = (claimKey) => {
  const updated = new URLSearchParams(searchParams)
  if (activeClaimKey === claimKey) {
    updated.delete('claim')
  } else {
    updated.set('claim', claimKey)
  }
  setSearchParams(updated)
}
```

So `/suppliers/kalyani-textiles?claim=gst_registration` opens that page *with that claim already
expanded*. A buyer can send a colleague a link to one specific piece of evidence. The back button
closes the claim rather than leaving the page, which is exactly what a user expects and almost never
gets.

**Shortlisting** persists to `localStorage` under `supify-shortlist`, read lazily on mount
(`SupplierProfile.jsx:9-15, 26`) and written on every toggle, with `try/catch` around both because
storage throws in private-browsing modes.

### 5.3 Comparison — a shareable decision table

**Route:** `/compare?ids=a,b,c` · **File:** `src/features/comparison/ui/ComparisonScreen.jsx`

Pick suppliers with checkboxes on the left; a table appears on the right comparing trust band,
location, category, capacity, MOQ, lead time, and established-claim count. The comparison set is
serialised into the URL as a comma-separated list, so the entire comparison is one link. The hero copy
says it outright: *"The comparison set lives in the URL, so you can send it to a colleague."*

The "established claims" row is a nice piece of honesty — it renders `"2 of 3"` rather than a
percentage, because the denominator is the informative part:

```js
{ label: 'Established claims',
  render: (s) => `${s.claims.filter((c) => c.state === 'verified').length} of ${s.claims.length}` },
```

The table's column count is driven off the selection with an inline grid template
(`ComparisonScreen.jsx:77`), and this screen is also the only one with a real **error state** plus a
retry button, and the only one that cancels in-flight requests on unmount.

> ⚠️ This screen is styled with class names — `.page`, `.queue-card`, `.filter-panel`, `.empty-state`,
> `.radio-row` — that **do not exist anywhere in the project's CSS**. `styles.css` never defines them
> and Tailwind doesn't generate them. It renders as unstyled HTML. Same applies to `NotFound`,
> `VerificationQueue`, `VerificationTaskDetail` and `ProtectedRoute`. These screens were written
> against an earlier hand-written stylesheet that the Tailwind redesign replaced, and they never got
> ported. The logic is sound; the paint is missing.

### 5.4 The verification engine

**Route:** `/verification?supplier=<id>` · **File:**
`src/features/verification-dashboard/ui/VerificationDashboard.jsx`

Two tabs, switched by local state because a tab is arguably ephemeral (though invariant 11 would
prefer it in the URL too).

**Tab 1 — Live Verification Run.** A four-stage progress stepper across the top:

| Stage | Status in fixture |
| --- | --- |
| 1. Identity Check | 100% Complete ✓ |
| 2. Sanctions & Watchlist | 0 Hits · Cleared ✓ |
| 3. Financial Health | In Review (D&B) — *in progress* |
| 4. ESG Compliance | EcoVadis Sync — *pending* |

Stage 3 is the interesting one. It's rendered in ochre with an hourglass, and it is neither "done" nor
"failed" nor "loading". `docs/CLAUDE.md` has a name for this: **pending-external**.

> "Pending-external" is specific to this product: a third-party check in flight is neither loading nor
> complete. Rendering it as either one is inaccurate.

Below the stepper, a bento grid:

- **Overall Trust Score** (saturated teal, `md:col-span-1`) — the score out of 100 plus band standing.
- **Financial Stability** — Dun & Bradstreet integration. Credit risk class derived from the score:
  ≥70 → "Low Risk (Class 2)", ≥40 → "Moderate Risk (Class 3)", else "Review Required". Payment
  promptness shows "98% On-Time" above 60 and "Data Pending" below, which is the right instinct —
  don't invent a number you don't have.
- **ESG Compliance** — EcoVadis sync: carbon Scope 1 & 2 reported ✓, labour rights audit passed ✓,
  conflict minerals declaration still under review.
- **Global Sanctions & Watchlists** (peach, spans two columns) — "0 Hits Found (Clean Standing)",
  checked against 1,200+ databases, naming OFAC (US Treasury), the UN Security Council, and the EU
  Consolidated list.

Actions: **Switch Supplier**, **Download PDF** (calls `window.print()`), and **Approve Supplier**,
which flips `approvedState`, disables the button, and toasts *"...approved and appended to immutable
ledger!"*

> ⚠️ The financial risk bar is inverted: `style={{ width: \`${Math.min(100 - overallScore, 100)}%\` }}`
> at `VerificationDashboard.jsx:273`. A supplier scoring 76 gets a 24%-wide bar. If the bar is meant to
> read as "risk", the label above it says "Credit Risk Class" and it's arguably correct; if it's meant
> to mirror the trust score, it's backwards. The ambiguity itself is the bug — nothing on screen tells
> the user which reading is intended.

**Tab 2 — Evidence Queue.** The verifier-facing side. A table of tasks with supplier, claim, evidence
count, state, assignee and SLA. Non-approved tasks get a "Review" button that opens a modal showing
the asserted claim, the evidence with its SHA-256 status, the priority and the SLA target. Approving
issues an attestation and updates the row.

The footer of this tab carries the **Decision Safeguard Axiom**, and it's the most important sentence
in the verifier console:

> Attestations are never issued optimistically. A submitted decision remains pending until the verifier
> confirms document integrity against registry check logs.

That's invariant 6 restated for humans: the supplier asserts, the platform attests, and the platform
does not attest hopefully.

### 5.5 The Solutions-first verification guard

This is the workflow most worth understanding in detail, because it's a navigation guard implemented
across two screens with a handoff through the URL.

**The problem.** "Verification" is a top-level nav item (`Header.jsx:9`), so a user can click it
cold. But a verification run is *about a specific supplier*. There is no meaningful
`/verification` without one. Rendering an empty dashboard would be a dead end, and silently bouncing
to search would be baffling.

**The guard.** `VerificationDashboard.jsx:24-49`:

```jsx
useEffect(() => {
  if (!supplierIdParam) {
    onShowToast?.('Please select a supplier from Solutions first to verify.', 'info')
    navigate('/search?prompt=select_to_verify', { replace: true })
    return
  }

  setSupplierLoading(true)
  supplierRepository
    .getById(supplierIdParam)
    .then((data) => {
      if (!data) {
        onShowToast?.('Selected supplier not found in registry.', 'error')
        navigate('/search', { replace: true })
        return
      }
      setVerifySupplier(data)
      setSupplierLoading(false)
      setApprovedState(false)
      setActiveStep(2)
    })
    .catch(() => {
      setSupplierLoading(false)
      navigate('/search', { replace: true })
    })
}, [supplierIdParam, navigate])
```

Three branches, and all three are handled: no supplier selected, supplier selected but not in the
registry, and the fetch itself failing. Each redirects with an explanation rather than leaving a blank
screen.

`{ replace: true }` is doing real work here. Without it, the bounce pushes a history entry, and the
user pressing Back lands on `/verification` — which immediately bounces them forward again. A history
trap. `replace` swaps the entry instead of stacking it, so Back goes where the user expects.

**The handoff.** The redirect doesn't just dump the user on search. It carries a flag,
`?prompt=select_to_verify`, which `SearchScreen` reads (`:16`) and turns into a banner (`:66-88`):

```jsx
{isSelectToVerifyPrompt && (
  <div className="bg-brand-mint/25 border-2 border-brand-teal/30 rounded-2xl p-4 md:p-5 ...">
    <h3 className="...">Select a Supplier to Run Verification</h3>
    <p className="text-xs text-on-surface-variant">
      Browse our verified partner solutions below and click
      <strong className="text-brand-teal font-bold">"Verify"</strong> on any card to view their live audit run.
    </p>
    <button onClick={() => updateParams({})}>✕</button>
  </div>
)}
```

The banner self-clears: `updateParams` deletes `prompt` on *any* filter interaction (`:45`), so the
moment the user starts working, the instruction disappears. That's a genuinely thoughtful detail —
the hint is present exactly as long as it's useful.

**The full sequence:**

```
User clicks "Verification" in the header
  → navigates to /verification  (no ?supplier=)
  → VerificationDashboard mounts, effect runs, supplierIdParam is null
  → toast: "Please select a supplier from Solutions first to verify."
  → navigate('/search?prompt=select_to_verify', { replace: true })
  → SearchScreen mounts, reads prompt=select_to_verify
  → mint banner explains what to do
  → user clicks "Verify" on a SupplierCard
  → Link to /verification?supplier=aravind-fasteners
  → effect runs again, param present, supplier fetched, dossier renders
```

The entry point for step six is on every card — `SupplierCard.jsx:113-119` — so the loop closes
in one click from wherever the user ended up.

### 5.6 Supplier workspace onboarding

**Route:** `/supplier/onboarding` (or `/supplier`) · **File:**
`src/features/supplier-onboarding/ui/OnboardingScreen.jsx`

Four steps, with a clickable stepper on the left so a supplier can jump around rather than being
marched forward:

1. **Organisation** — trade name, full legal name, operating city/region, website
2. **Capabilities** — primary category, monthly capacity, MOQ, lead time
3. **Claims & Evidence** — tax/registry identifier (GSTIN, VAT, D-U-N-S), certification upload
4. **Review & Publish** — read-only summary, then submit into the verifier queue

The upload affordance states the hashing contract up front: *"PDF, PNG, JPG up to 25MB (SHA-256 hashed
on ingest)."*

**Autosave is the feature that matters.** Invariant 12 — *never lose a supplier's work* — because
onboarding spans days, on unreliable connections, often on a phone in a factory. Two halves:

Lazy read on mount (`:14-31`), so the expensive parse runs once rather than on every render:

```jsx
const [formData, setFormData] = useState(() => {
  try {
    const saved = localStorage.getItem('supify_supplier_onboarding_draft')
    if (saved) return JSON.parse(saved)
  } catch (e) {}
  return { /* seeded defaults */ }
})
```

Write on every change (`:35-40`):

```jsx
useEffect(() => {
  try {
    localStorage.setItem('supify_supplier_onboarding_draft', JSON.stringify(formData))
    setSavedStatus('Draft saved locally just now')
  } catch (e) {}
}, [formData])
```

Because the dependency is the whole `formData` object and every edit produces a new object via
`setFormData((prev) => ({ ...prev, [field]: val }))`, the effect fires on **every keystroke**. Type
one character, refresh the page, it's still there. The footer shows a live "Draft saved locally just
now" indicator so the supplier can *see* that nothing is being lost — reassurance is part of the
feature, not decoration.

Both storage calls are wrapped in `try/catch` because `localStorage` throws in Safari private mode and
when the quota is full. Losing the draft is bad; crashing the whole form because you couldn't save the
draft is worse.

Note also that this screen only ever writes to `formData` and `localStorage`. It cannot touch
attestation state — invariant 6 — because the supplier asserts and the platform attests, and those are
different write paths by construction.

### 5.7 The 404

**Route:** `*` · **File:** `src/app/NotFound.jsx`

The catch-all is the last route in the list, which is not stylistic — React Router v6 ranks routes by
specificity, and `path="*"` is the lowest-ranked pattern, so it only matches when nothing else does.
It offers a designed way out rather than a dead end:

```jsx
export function NotFound() {
  return (
    <main className="page">
      <div className="empty-state">
        <span aria-hidden="true">⊘</span>
        <h2>Page not found</h2>
        <p>This address does not match anything in Supify.</p>
        <Link className="button" to="/search">Go to discovery</Link>
      </div>
    </main>
  )
}
```

The same "not found" treatment exists one level deeper too: an unknown `:supplierId` doesn't 404 the
route (the route matched fine) — it renders a *"Supplier Record Not Found"* state inside the profile
with a route back to search (`SupplierProfile.jsx:53-64`). Route-not-found and record-not-found are
different failures and get different screens.

> ⚠️ Two internal links currently land on this 404. `VerificationQueue.jsx:87` links to
> `/verify/tasks/${task.id}` and `VerificationTaskDetail.jsx:64, 75` link to `/verify/queue` — but the
> registered routes are `/verifier/task/:taskId` and `/verifier/queue`. Both are leftovers from the
> pre-redesign route table. `VerificationQueue` isn't routed at all, so only the second pair is
> reachable, but it's reachable and it's broken.

---

## 6. The tactile visual design system

The full specification lives in `docs/design.md`. What follows is the implemented subset, with the
gaps marked.

### 6.1 Atmosphere

Most supply-chain software is cold: white or grey, blue accents, dense grids, the visual language of a
spreadsheet that grew a UI. Supify goes the other way deliberately. The page floor is a
**cream-tinted white** — `#fffaf0` — warm enough to read as paper rather than screen. Type is near-black
ink. Feature cards are fully saturated colour with hard black strokes and offset shadows, so they
read as physical objects sitting on that paper.

`docs/design.md` describes the ink as "dark navy/black"; the actual token is `#0a0a0a`, which is
effectively near-black with a touch of warmth. If asked, quote the hex, not the adjective.

### 6.2 The palette

All tokens from `tailwind.config.js`. Seven brand hues are defined, not six:

| Token | Hex | Role |
| --- | --- | --- |
| `background` / `canvas` | `#fffaf0` | The page floor. Cream-tinted white. |
| `primary` | `#0a0a0a` | Ink type, primary CTAs, the 2px card stroke |
| `brand-teal` | `#1a3a3a` | Verified / high-trust. Deep forest-teal. |
| `brand-pink` | `#ff4d8b` | Discovery and matching |
| `brand-lavender` | `#b8a4ed` | Compliance, ESG, regulatory |
| `brand-peach` | `#ffb084` | Watchlists, sanctions, trust-gate warnings |
| `brand-ochre` | `#e8b94a` | In-review, pending, expiring |
| `brand-mint` | `#a4d4c5` | Accent on trust badges, pillar bars, verified marks |
| `brand-coral` | `#ff6b5a` | Highlights, active indicators, destructive accents |
| `surface-card` | `#f5f0e0` | Card fill, one step warmer than canvas |
| `surface-strong` | `#ebe6d6` | Table headers, filter pills |
| `hairline` | `#e5e5e5` | Every 1px border in the app |
| `body-muted` | `#6a6a6a` | Secondary text |
| `error` | `#ba1a1a` | Revoked, expired, lapsed |

`docs/design.md` §12 names the "6-colour saturated feature card palette" as pink, teal, lavender,
peach, ochre and *cream* `surface-card` — mint and coral are accent colours rather than card fills.
The brief's list substitutes mint for cream. Both mint and coral exist as tokens; if an examiner asks
for six, give them pink/teal/lavender/peach/ochre/cream and note that mint and coral are accents.

Colour assignment is never computed from a string — `SupplierCard.jsx:4-20` uses explicit lookup maps,
because Tailwind's compiler scans source text for class names and a template literal like
`bg-${color}` produces a class that gets purged from the build.

> ⚠️ No supplier in `suppliers.json` carries a `theme_color` field, so `adapter.js:36` falls through to
> `'brand-teal'` for all five and every card in the grid is teal. The six-colour card system is fully
> built and entirely unexercised by the data. Add `"theme_color": "brand-pink"` to one fixture and it
> lights up immediately.

### 6.3 Typography

Two families, split by job — display versus data.

**Rubik** (weights 500–600) for display sizes. Rounded terminals, slightly geometric, friendly at
scale. Used with negative letter-spacing that tightens as the size grows.

**Inter** (400–700) for everything else: body, navigation, buttons, labels, and every data table,
audit log and claim ledger in the app. Inter is designed for exactly this — dense tabular data at
small sizes.

| Token | Size | Weight | Tracking | Family | Used for |
| --- | --- | --- | --- | --- | --- |
| `display-xl` | 72px | 500 | −2.5px | Rubik | Landing h1 — "Source with confidence." |
| `display-lg` | 56px | 500 | −2px | Rubik | Section heads |
| `display-md` | 40px | 500 | −1px | Rubik | Page h1s |
| `display-sm` | 32px | 500 | −0.5px | Rubik | Brand mark, stat figures |
| `display-xl-mobile` | 36px | 500 | −1px | Rubik | Mobile hero |
| `title-lg` | 24px | 600 | −0.3px | Inter | Card titles, modal headings |
| `title-md` | 18px | 600 | — | Inter | Sub-headings, claim labels |
| `body-md` | 16px | 400 | — | Inter | Default body |
| `body-sm` | 14px | 400 | — | Inter | Secondary text |
| `button` | 14px | 600 | — | Inter | All controls |
| `label-uppercase` | 12px | 600 | +1.5px | Inter | Eyebrow labels |

Note the tracking direction flips with size: big display type gets *negative* tracking so letters knit
together, and 12px uppercase eyebrows get *+1.5px* because uppercase at small sizes needs air. That's
not a Supify invention, it's standard practice, but the scale actually implements it.

`styles.css:25-27` sets `h1, h2, h3` to Rubik globally, so headings are correct even where a component
forgets the utility class.

### 6.4 The tactile card

The signature treatment. A hard offset shadow with no blur, plus a 2px black stroke — a card that
looks die-cut and lifted rather than softly floating.

```css
.tactile-card {
  box-shadow: 4px 4px 0px 0px rgba(0, 0, 0, 1);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.tactile-card:hover {
  transform: translateY(-2px);
  box-shadow: 6px 6px 0px 0px rgba(0, 0, 0, 1);
}
```

On hover the card rises 2px *and* the shadow grows to 6px — the offset increasing as the object lifts
is what sells the physicality. The easing curve `cubic-bezier(0.16, 1, 0.3, 1)` is a sharp
decelerate: fast out of the gate, long settle. It feels like a physical object coming to rest.

> ⚠️ `.tactile-card` and `.tactile-card-subtle` are defined in `styles.css:77-95` and **used nowhere in
> `src/`**. The landing page's feature cards achieve the identical effect with inline Tailwind
> arbitrary values instead (`LandingScreen.jsx:192`):
>
> ```jsx
> className="bg-brand-pink text-on-primary rounded-xl p-xl ...
>   shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1
>   hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] transition-all duration-200
>   border-2 border-primary group cursor-pointer h-full"
> ```
>
> Same visual result, duplicated four times. The CSS class is the better home; the components never
> got switched over.

The best example of the language is the landing hero (`LandingScreen.jsx:92-174`) — a mint backing
card rotated −3° behind a white card rotated +1°, both with 2px strokes, the front one carrying a 6px
hard shadow. It's a paper mock-up of a trust ledger, and it's rendered in the product's own components
rather than being a stock illustration. The hero *is* the pitch: four claim rows, each showing method
and recency, one expiring, one openly marked self-declared, and a coverage strip reading "3 of 4
independently checked" rather than a made-up percentage.

### 6.5 Spacing, radius, motion, icons

**Spacing** is a named 4px scale — `base` 4, `xs` 8, `sm` 12, `md` 16, `lg` 24, `xl` 32, `xxl` 48,
`section` 96 — plus `container-max` at 1280px, which every page uses via `max-w-container-max mx-auto`.

**Radius** — `sm` 4px, `md` 12px, `lg` 16px, `xl` 24px, `full`. Buttons sit at `md`/`lg`, cards at
`xl`/`2xl`. Nothing is sharp-cornered; the roundness is part of the friendliness.

**Motion** — two keyframes are defined, `float` (6s, ±15px vertical, the hero card) and `pulseGlow`
(4s opacity). Crucially, `styles.css:68-74` honours the OS accessibility setting:

```css
@media (prefers-reduced-motion: reduce) {
  .animate-float,
  .animate-pulseGlow,
  .animate-ping {
    animation: none !important;
  }
}
```

A user who has asked their operating system to stop moving things gets a static page. This costs six
lines and is skipped by most production apps.

**Icons** are Google Material Symbols, loaded as a variable font from the CDN
(`index.html:11`), with a CSS custom-property trick for the fill axis (`styles.css:62-65`):

```css
.material-symbols-outlined[data-fill="true"] {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
```

So `<span className="material-symbols-outlined" data-fill="true">verified</span>` gives a solid icon
and omitting the attribute gives an outline — one font file, two weights of meaning. Filled is used
for established facts, outline for pending ones, which is a third redundant channel alongside colour
and text.

### 6.6 Accessibility posture

Worth listing because it's better than average and it's the kind of thing viva examiners like:

- **Never colour alone** — every trust state pairs colour with an icon and a text label
- **`prefers-reduced-motion`** honoured for all decorative animation
- **Decorative glyphs** carry `aria-hidden="true"` (`NotFound.jsx:7`, `ComparisonScreen.jsx:111`)
- **The hero card** is `role="img"` with a 58-word `aria-label` that reads out the entire ledger
  (`LandingScreen.jsx:18-22, 103-104`) — a screen-reader user gets the actual claims, not "decorative
  image"
- **`aria-live="polite"`** on the verifier decision confirmation (`VerificationTaskDetail.jsx:100`)
- **`.sr-only`** utility defined for visually-hidden text
- **Semantic landmarks** — `<main>`, `<header>`, `<nav>`, `<article>`, `<fieldset>`/`<legend>`
- **`aria-label`** on the mobile menu toggle

> ⚠️ Gaps: the evidence and task modals don't trap focus or close on `Escape`, and nothing returns
> focus to the trigger on close. The definition of done in `docs/CLAUDE.md` requires full keyboard
> operability, so this is unfinished work rather than an accepted trade-off. Also, `animate-fadeIn`
> (used in seven files) and `animate-bounce-short` (used in `Toast.jsx:19`) are **not defined** in
> either `tailwind.config.js` or `styles.css` — those elements appear instantly with no animation. The
> classes are inert.

---

## 7. Built vs. stubbed: an honest inventory

If you only memorise one section for a viva, make it this one. "What doesn't work yet, and why?" is
the question that separates someone who wrote the code from someone who watched it get written.

### Fully working

| Feature | Notes |
| --- | --- |
| Search with URL-synchronised filters | Query, band, sort all work and survive reload/back |
| Trust triple rendering | State + method + recency, everywhere, through entity components |
| Claim ledger with evidence inspection | Deep-linkable via `?claim=` |
| Expiry computed at render time | Lapsed attestations self-declare in red |
| Comparison set in the URL | Shareable, with error + retry + request cancellation |
| Onboarding autosave | Every keystroke, `try/catch`-guarded, with a live indicator |
| Verification guard + banner handoff | All three failure branches covered, `replace: true` correct |
| 404 + record-not-found | Two distinct, designed states |
| Reduced-motion support | Honoured for all decorative animation |

### Built but not wired

| Thing | Status |
| --- | --- |
| `ProtectedRoute.jsx` | Written, correct, **never imported**. No route uses it. |
| `UserRoleContext` | Provider mounted in `main.jsx:11`; only consumer is the unrouted `ProtectedRoute`. Effectively dead. |
| `VerificationQueue.jsx` | Complete screen, **not routed**. Superseded by the dashboard's Queue tab. |
| `OnboardingStep.jsx` | Needs `useOutletContext` and a parent `<Outlet>` route that doesn't exist. |
| `steps.js` | Only consumed by the unrouted `OnboardingStep`. |
| `.tactile-card` CSS | Defined, never used. Components inline the same values. |
| Six-colour card system | Fully built; no fixture sets `theme_color`, so every card is teal. |
| `@tailwindcss/forms`, `container-queries` | In `devDependencies`; `tailwind.config.js` has `plugins: []`. Not loaded. |
| `darkMode: "class"` | Configured; `index.html` hardcodes `class="light"` and no `dark:` variants exist. |

The README describes role-protected consoles and routes like `/verify/queue` and
`/supplier/onboarding/organisation`. Those were real in an earlier version. The tactile redesign
(commits `a2fbc28` and `fe0ac48`) rebuilt the router and left the old screens orphaned in the tree.
**The README is out of date relative to `App.jsx`** — trust the code.

### Simulated, not implemented

| Thing | Reality |
| --- | --- |
| SHA-256 ledger record | Hardcoded constant — and it's the hash of the empty string |
| D&B financial ratings | Static copy; risk class derived from the local score |
| EcoVadis ESG sync | Static copy, three hardcoded line items |
| Sanctions screening | Always "0 Hits Found"; the 1,200+ database count is copy |
| "Download PDF" | Calls `window.print()` |
| Auth modal | Accepts any credentials, closes, toasts a welcome |
| Approve / attest | Local state only; nothing persists past a reload |

None of this is dishonest — it's a frontend built against a contract with no backend, which is exactly
what `docs/CLAUDE.md` says the scope is. But you should be able to name every item on this list.

### Known bugs

1. **Region filter returns zero for all four options** — no `region` field in fixtures and
   `"Ludhiana, Punjab, IN"` doesn't contain `"india"`.
2. **Three of six industry options match nothing** — Packaging, Electronics, Machining.
3. **"Apply Filters" is `onClick={() => {}}`** — a no-op button.
4. **Client-side trust score** — violates invariant 2.
5. **`animate-fadeIn` / `animate-bounce-short` undefined** — inert classes in eight places.
6. **Five screens reference undefined CSS classes** — `.page`, `.empty-state`, `.button`, etc. render
   unstyled.
7. **Toast timer has no cleanup** — `App.jsx:21-26` never clears the previous `setTimeout`, so a second
   toast within 4s gets dismissed early by the first toast's timer.
8. **Broken internal links** — `/verify/queue` and `/verify/tasks/:id` don't match any route.
9. **Financial risk bar renders `100 - score`** — ambiguous direction, unlabelled.
10. **Modals don't trap focus or close on Escape.**

---

## 8. Running it, and where everything lives

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build to dist/
npm run preview  # serve the build
```

A tour worth taking in order:

1. `/` — read the hero card. Every row shows method and recency; one is expiring; one is openly
   self-declared.
2. `/search?q=fasteners&band=verified` — paste that URL cold and land on a filtered result set.
3. `/suppliers/aravind-fasteners` — trust panel, four pillars, validity window.
4. `/suppliers/kalyani-textiles` — a lapsed attestation, rendered as lapsed.
5. `/suppliers/deccan-polymers` — a revoked claim, rendered rather than hidden.
6. `/suppliers/narmada-fabrication` — the 87-character legal name. Check the layout holds.
7. `/verification` with no query string — watch the guard bounce you to Solutions with a banner.
8. `/supplier/onboarding` — type one character, refresh, confirm it survived.
9. `/nonsense` — the 404.

### File map

```
index.html                    fonts, theme-color, #root
tailwind.config.js            all design tokens
vite.config.js                React plugin, nothing else
public/data/
  suppliers.json              5 adversarial supplier records
  verification-tasks.json     5 queue tasks covering every state
src/
  main.jsx                    createRoot · StrictMode · BrowserRouter · UserRoleProvider
  app/
    App.jsx                   Header + <Routes> + global Toast + auth Modal
    ProtectedRoute.jsx        role guard — written, not wired
    NotFound.jsx              404
    styles.css                Tailwind directives, tokens, tactile classes, a11y
  shared/
    api/contract.js           abstract SupplierRepository
    api/supplierRepository.js fixture implementation + 200ms latency
    ui/Header.jsx             sticky nav + mobile drawer
    ui/Modal.jsx              generic overlay via children
    ui/Toast.jsx              transient notification
  entities/
    supplier/model/adapter.js wire → domain mapping (the boundary)
    supplier/ui/SupplierCard.jsx
    trust/ui/TrustBand.jsx    the only place a band renders
    trust/ui/TrustPanel.jsx   pillars + validity + gates
    claim/ui/ClaimRow.jsx     the only place a claim renders
    user/model/UserRoleContext.jsx
  features/
    landing/ui/LandingScreen.jsx
    discovery/ui/SearchScreen.jsx
    supplier-profile/ui/SupplierProfile.jsx
    comparison/ui/ComparisonScreen.jsx
    verification-dashboard/ui/VerificationDashboard.jsx
    verification-review/ui/VerificationQueue.jsx         (not routed)
    verification-review/ui/VerificationTaskDetail.jsx
    supplier-onboarding/ui/OnboardingScreen.jsx
    supplier-onboarding/ui/OnboardingStep.jsx            (not routed)
    supplier-onboarding/model/steps.js
docs/
  CLAUDE.md                   working agreement + the twelve invariants
  understanding.md            problem framing, axioms, domain model (1355 lines)
  architecture.md             frontend architecture (797 lines)
  design.md                   the visual system spec
  contract/supplier-api.md    the API the frontend is built against
```

---

### One closing thought

The thing to carry out of this document is that Supify's central idea is a *refusal*. It refuses to
compress trust into one bit. Everything else — the adapter's explicit fallbacks, the invariant against
boolean flags, the four pillars, the render-time expiry check, the gate that contradicts its own band,
the "3 of 4 independently checked" instead of "94%" — is downstream of that one refusal.

The product is not "a directory with verification." It's a bet that showing your working is more
valuable than showing a checkmark, and that buyers will pay for the difference.

---

*For the React architecture, hooks, and routing behind all of this, see `REACT_CONCEPTS_DEEP_DIVE.md`.*
