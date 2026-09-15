# React Concepts — Deep Dive (Supify)

**Every React concept in this codebase, explained through the actual code that implements it.**

This document is strictly about React: the mental model, components, props, state, hooks,
composition, and React Router v6. It says almost nothing about supplier verification as a business
problem — for that, read `SUPIFY_PROJECT_GUIDE.md`. The two documents are meant to stand alone.

Every topic follows the same four beats:

1. **The analogy** — plain English, no jargon
2. **The code** — a real snippet from this repository, with its file path
3. **Why we did it this way** — the engineering reasoning, including where we got it wrong
4. **Viva question** — the thing you'll actually get asked, with a two-sentence answer to say out loud

Where a curriculum topic isn't present in the codebase, this document says so plainly and shows where
it *would* go. Claiming a `useRef` that doesn't exist is how vivas go badly.

**Versions:** React 19.2.8 · react-router-dom 6.30.6 · Vite 8.2.1

---

## Hook census — what's actually in this codebase

Counted across `src/`, so you can't be caught out:

| Hook | Uses | Where |
| --- | ---: | --- |
| `useState` | 41 | Everywhere |
| `useEffect` | 15 | Data fetching, autosave, the verification guard |
| `useSearchParams` | 10 | Search, comparison, profile, dashboard, queue |
| `useNavigate` | 10 | App shell, guard redirects, wizard completion |
| `useParams` | 6 | Supplier profile, task detail, onboarding step |
| `useMemo` | 3 | `ComparisonScreen` only |
| `useCallback` | 2 | `ComparisonScreen` only |
| `useLocation` | 2 | `App.jsx`, for active-nav highlighting |
| `useContext` | 2 | `ProtectedRoute` only (and that file isn't routed) |
| `useOutletContext` | 2 | `OnboardingStep` only (and that file isn't routed) |
| **`useRef`** | **0** | **Not used anywhere — see §5.5** |
| **Custom hooks** | **0** | **None defined — see §5.6** |
| `useReducer`, `React.memo`, `useLayoutEffect`, `useId` | 0 | Not used |

---

## Table of contents

1. [React architecture and the mental model](#1-react-architecture-and-the-mental-model)
2. [Components, props and state](#2-components-props-and-state)
3. [List rendering and keys](#3-list-rendering-and-keys)
4. [Conditional rendering](#4-conditional-rendering)
5. [The React hooks toolkit](#5-the-react-hooks-toolkit)
6. [Component communication and composition](#6-component-communication-and-composition)
7. [React Router v6 and multi-page SPA navigation](#7-react-router-v6-and-multi-page-spa-navigation)
8. [Teacher viva cheat sheet](#8-teacher-viva-cheat-sheet)
9. [Rough edges — the "what would you fix" answer](#9-rough-edges--the-what-would-you-fix-answer)

---

## 1. React architecture and the mental model

### 1.1 Declarative UI vs imperative DOM manipulation

#### The analogy

Imperative programming is giving a taxi driver turn-by-turn directions: left here, right at the
lights, mind the roadworks. You're responsible for every step, and if the road layout changes you have
to notice and re-plan.

Declarative programming is telling the driver the destination. *"Airport, terminal 2."* How to get
there is their problem, and if a road is closed they reroute without asking you.

React is the second one. You never say "find the badge element, change its text, swap the class,
remove the old icon node." You say "given this supplier's trust band, the UI looks like *this*," and
React figures out what to change in the DOM.

#### The code

`src/entities/trust/ui/TrustBand.jsx:36-45` — the compact trust badge. Nothing here touches the DOM:

```jsx
if (compact) {
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold tracking-wide border ${meta.colorClass}`}>
      <span className="material-symbols-outlined text-sm font-semibold leading-none" data-fill={trust.band === 'verified' || trust.band === 'audited' ? 'true' : 'false'}>
        {meta.icon}
      </span>
      <span>{meta.label}</span>
    </span>
  )
}
```

The imperative equivalent — what you'd write in vanilla JS to keep a badge in sync — is roughly:

```js
// NOT in the codebase. This is what React saves you from.
const badge = document.querySelector('#trust-badge')
badge.className = 'inline-flex items-center ... ' + meta.colorClass
const icon = badge.querySelector('.material-symbols-outlined')
icon.textContent = meta.icon
icon.setAttribute('data-fill', band === 'verified' ? 'true' : 'false')
badge.querySelector('.label').textContent = meta.label
// ...and now do it all again, correctly, in every other place a band appears
```

#### Why we did it this way

The imperative version has a failure mode the declarative version structurally cannot have:
**divergence**. Every mutation is an opportunity to update three of the four things that needed
updating. Miss one, and the badge says "Verified" in green while the icon still shows an hourglass.

In a normal app that's a cosmetic bug. In this one it's a lie about whether a supplier is
trustworthy — and `docs/CLAUDE.md` invariant 5 requires colour, icon and text to always agree, because
that redundancy is what makes the badge readable to a colour-blind user. Declarative rendering makes
"they agree" a property of the source code rather than a property of the update sequence.

The second reason is that `TrustBand` is used in five different places. Imperatively, that's five
update paths to keep in sync. Declaratively it's one function, called five times.

#### Viva question

> **Q: What does it mean to say React is declarative, and why does it matter here?**
>
> **A:** Declarative means we describe what the UI should look like for a given state and let React
> compute the DOM operations, instead of writing the mutation steps ourselves. It matters in Supify
> because a trust badge has to keep its colour, icon and text in agreement — declarative rendering makes
> that a guarantee of the code rather than something we have to remember on every update path.

---

### 1.2 JSX and its rules

#### The analogy

JSX is a phrasebook. You're writing JavaScript, but for the bits that describe UI you get to speak
something that looks like HTML, and a translator (Babel, via Vite's React plugin) converts it back
into JavaScript function calls before the browser ever sees it. The browser doesn't know JSX exists.

#### The code

`src/shared/ui/Toast.jsx:18-32` uses nearly every JSX rule at once:

```jsx
return (
  <div className="fixed bottom-6 right-6 z-50 animate-bounce-short">
    <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border-2 shadow-xl ${bgStyles}`}>
      <span className="material-symbols-outlined text-xl" data-fill="true">
        {icons[type] || 'info'}
      </span>
      <span className="font-button text-button text-sm">{message}</span>
      {onClose && (
        <button onClick={onClose} className="opacity-80 hover:opacity-100 ml-2">
          <span className="material-symbols-outlined text-sm">close</span>
        </button>
      )}
    </div>
  </div>
)
```

The rules on display:

| Rule | Where you can see it |
| --- | --- |
| **One root element** | Everything is wrapped in the outer `<div>` |
| **`className`, not `class`** | Every element — `class` is a reserved JS word |
| **`camelCase` event props** | `onClick`, not `onclick` |
| **`{}` escapes to JavaScript** | `{message}`, `{icons[type] \|\| 'info'}` |
| **Template literals for dynamic classes** | `` className={`... ${bgStyles}`} `` |
| **Tags must close** | `<img ... />`, `<div ... />` — no bare `<br>` |
| **`data-*` passes through as-is** | `data-fill="true"` — the one attribute family that keeps its dashes |

When you need siblings without a wrapper div, use a **Fragment**. `ClaimRow.jsx:80-87` uses the short
form `<>...</>` to inject two elements into a flex row without adding a layout box:

```jsx
{validity && (
  <>
    <span>·</span>
    <span className={new Date(claim.validUntil).getTime() < Date.now() ? 'text-error font-semibold' : 'text-brand-teal'}>
      {validity}
    </span>
  </>
)}
```

#### Why we did it this way

The "one root element" rule isn't arbitrary — a JSX expression compiles to a single
`React.createElement(...)` call, and a JavaScript function can only return one value. Fragments exist
precisely so you can satisfy that constraint without polluting the DOM with wrapper divs, which
matters enormously inside CSS Grid and Flexbox layouts where an extra div becomes an unwanted grid
item.

The `data-fill` attribute is the interesting one here. Material Symbols is a variable font, and
`styles.css:62-65` targets `[data-fill="true"]` to switch the `FILL` axis from 0 to 1. Because JSX
passes `data-*` attributes through untouched, we can drive a font-variation axis declaratively from a
prop — solid icons for established facts, outline for pending ones — using one font file and zero
JavaScript.

#### Viva question

> **Q: Why must a JSX expression return a single root element, and how do you return siblings?**
>
> **A:** JSX compiles to a single `React.createElement()` call and a JavaScript function can only
> return one value, so multiple roots have nothing to compile to. You return siblings with a Fragment
> — `<>...</>` — which groups them for React without rendering a wrapper element into the DOM.

---

### 1.3 The Virtual DOM and reconciliation

#### The analogy

Imagine proofreading a 300-page manuscript. The slow way is to reprint the whole book after every
correction. The fast way is to keep a copy of the previous draft, diff it against the new one, and
only reprint the pages that actually changed.

The Virtual DOM is that previous draft. It's a plain JavaScript object tree describing what the UI
should look like. When state changes, React builds a new tree, compares it to the old one
(**reconciliation**), computes the minimal set of real DOM operations, and applies only those.

This matters because real DOM writes are expensive — they can trigger layout recalculation and repaint
— while comparing JavaScript objects is cheap.

#### The code

`src/features/discovery/ui/SearchScreen.jsx:282-286` — the results grid. When a filter changes and 40
suppliers become 12:

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
  {suppliers.map((supplier) => (
    <SupplierCard key={supplier.id} supplier={supplier} onOpen={onOpenSupplier} />
  ))}
</div>
```

React does *not* wipe the grid and rebuild 12 cards. It diffs old children against new by `key`, and
for any supplier present in both lists it keeps the existing DOM node and patches only what differs.
Cards that survived a filter change are never touched.

#### Why we did it this way

You don't opt into the Virtual DOM — it's how React works. But you can help or hinder it, and this
codebase does both.

**Helps:** stable `key={supplier.id}` lets React match old and new children correctly (see §3).

**Helps:** `auto-rows-fr` on the grid means rows are equal height regardless of content, so a
re-render with different suppliers doesn't shift the layout of neighbouring cards.

**Hinders:** the loading state at `SearchScreen.jsx:276-280` is a small centred spinner box, while the
loaded state is a full grid. Swapping between them replaces the whole subtree and jolts the page.
`docs/CLAUDE.md`'s definition of done asks for "loading states match final layout — no layout shift on
content arrival," which would mean rendering skeleton cards in the same grid. That's a real gap, and a
good thing to volunteer if asked what you'd improve.

#### Viva question

> **Q: What is the Virtual DOM and what problem does it solve?**
>
> **A:** It's an in-memory JavaScript object tree describing the intended UI; on each update React
> builds a new tree, diffs it against the previous one, and applies only the minimal real DOM changes.
> It solves the cost problem of direct DOM manipulation — comparing JS objects is cheap, while DOM
> writes can force layout and repaint.

---

## 2. Components, props and state

### 2.1 Function components

#### The analogy

A component is a recipe. Give it ingredients (props) and it produces a dish (UI). The same
ingredients always produce the same dish — it's a function, not a process with a memory. Any memory it
*does* need is explicitly declared with hooks.

#### The code

`src/shared/ui/Modal.jsx:1-23`, in full — the smallest complete component in the codebase:

```jsx
export function Modal({ isOpen, onClose, title, children, maxWidth = 'max-w-lg' }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fadeIn">
      <div className="fixed inset-0" onClick={onClose}></div>
      <div className={`relative z-10 w-full ${maxWidth} bg-surface-card border-2 border-primary rounded-2xl p-lg shadow-2xl overflow-hidden max-h-[90vh] flex flex-col`}>
        <div className="flex justify-between items-center pb-md border-b border-hairline mb-md">
          <h3 className="font-title-lg text-title-lg text-primary font-bold">{title}</h3>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full flex items-center justify-center text-primary hover:bg-surface-variant transition-colors"
          >
            <span className="material-symbols-outlined text-lg">close</span>
          </button>
        </div>
        <div className="overflow-y-auto flex-grow pr-1">
          {children}
        </div>
      </div>
    </div>
  )
}
```

Every component in this project is a function. There is not a single `class extends React.Component`
anywhere.

#### Why we did it this way

Three concrete reasons, in order of how much they actually matter day to day:

1. **No `this`.** Class components require binding methods in the constructor or using arrow-function
   class fields, and a forgotten bind produces a runtime error that says nothing useful about the
   cause. Functions close over their values. The whole category disappears.
2. **Hooks compose; lifecycle methods don't.** In a class, subscribing to something means splitting the
   logic across `componentDidMount`, `componentDidUpdate` and `componentWillUnmount`. In a function
   it's one `useEffect` with its cleanup sitting inline, right next to the setup it undoes.
3. **Less ceremony.** `Modal` is 23 lines. The class version needs a `render()` method, a class
   declaration, and `this.props` on every access, for zero additional capability.

Note `maxWidth = 'max-w-lg'` — a default parameter in the destructuring. The component works when
called with four props and is configurable when called with five.

#### Viva question

> **Q: Why does this project use function components rather than class components?**
>
> **A:** Function components remove `this`-binding entirely and let related logic live together in
> hooks instead of being split across three lifecycle methods. They're also the direction React itself
> has gone — hooks only work in functions, so class components can't use most modern React APIs.

---

### 2.2 Props are read-only

#### The analogy

Props are a delivery. The courier hands you a parcel; you can open it, read the label, and decide what
to do with the contents — but you cannot reach back into the depot and change what was sent. If you
want something different delivered, you have to ask the sender.

In React terms: a child never mutates its props. It calls a callback and asks the parent to change
its own state, which produces a new render with new props.

#### The code

`src/entities/claim/ui/ClaimRow.jsx:10-16` — destructuring with defaults, then deriving new values
rather than mutating the input:

```jsx
export function ClaimRow({ claim, isOpen = false, onToggle = null, onOpenEvidence = null }) {
  const date = claim.verifiedAt
    ? `Established ${formatDate(claim.verifiedAt)}`
    : 'Not yet independently established'

  const validity = claim.validUntil
    ? `Attestation ${new Date(claim.validUntil).getTime() < Date.now() ? 'lapsed' : 'valid until'} ${formatDate(claim.validUntil)}`
    : null
```

`claim.verifiedAt` is read. `claim` is never written to. `date` and `validity` are new local constants
derived from it.

And the immutable state update in `App.jsx:42-44` — the pattern for "change one field":

```jsx
const handleChange = (field, val) => {
  setFormData((prev) => ({ ...prev, [field]: val }))
}
```

*(that one is `OnboardingScreen.jsx:42-44`)*

Spread the previous object into a new one, override the single changed key. Never
`formData[field] = val`.

#### Why we did it this way

React decides whether to re-render by comparing references. If you mutate an object in place, the
reference doesn't change, React concludes nothing happened, and your UI silently fails to update.
Creating a new object is what makes the change *visible* to React.

There's a second reason specific to this project. `ClaimRow` receives claim data that ultimately came
from the API. If a component could mutate it, the same claim object rendered in two places could
diverge — one showing "verified", one showing "under review" — which is precisely the drift that
invariant 9 (*never render trust outside the entity components*) exists to prevent. Read-only props
make drift structurally impossible rather than merely discouraged.

The defaults matter too. `isOpen = false, onToggle = null, onOpenEvidence = null` means `ClaimRow`
renders correctly with just a `claim` — which is exactly how `VerificationTaskDetail.jsx:95` calls it,
as a read-only display with no interaction.

#### Viva question

> **Q: Why can't a component modify its own props?**
>
> **A:** Props belong to the parent, and React detects change by comparing references — mutating a prop
> in place changes the value without changing the reference, so React sees nothing and skips the
> re-render. The correct flow is for the child to call a callback so the parent updates its state,
> which produces new props on the next render.

---

### 2.3 State is reactive memory

#### The analogy

Props are what you were told. State is what you remember.

A supplier card is told which supplier to render (prop). The search screen remembers which filters are
active and whether it's still loading (state). When memory changes, the component re-renders; when it
merely reads something, it doesn't.

#### The code

`src/features/verification-dashboard/ui/VerificationDashboard.jsx:11-19` — seven pieces of state, each
one a distinct question the component has to remember the answer to:

```jsx
const [activeStep, setActiveStep] = useState(2)
const [tasks, setTasks] = useState([])
const [activeTab, setActiveTab] = useState('run')
const [selectedTask, setSelectedTask] = useState(null)
const [approvedState, setApprovedState] = useState(false)

// The supplier being verified (loaded dynamically)
const [verifySupplier, setVerifySupplier] = useState(null)
const [supplierLoading, setSupplierLoading] = useState(true)
```

#### Why we did it this way

The design decision worth defending here is **not combining these into one state object**. It would be
tempting to write `useState({ activeStep: 2, tasks: [], activeTab: 'run', ... })`. Keeping them
separate is better because:

- Each setter is independent. Switching tabs doesn't require spreading the other six fields.
- The dependency arrays elsewhere in the file can name exactly what they depend on.
- Reading the list tells you precisely what this screen remembers.

Notice the **initial values are semantically chosen**, not defaulted to `null` out of habit:

- `tasks` starts as `[]` so `tasks.filter(...)` at line 122 works on the very first render — no
  optional chaining, no guard.
- `verifySupplier` starts as `null` because "not loaded" is genuinely different from "loaded but
  empty", and the loading guard at line 72 tests exactly that.
- `supplierLoading` starts `true`, not `false`, because the component *is* loading from the moment it
  mounts. Starting it `false` would flash the empty state for one frame before the effect runs.

That last one is a real bug class — the "flash of wrong content" — and it's avoided by one carefully
chosen initial value.

#### Viva question

> **Q: What's the difference between props and state?**
>
> **A:** Props are passed in from a parent and are read-only inside the component; state is owned by
> the component itself and changing it via its setter triggers a re-render. A rough rule: if the
> component needs to remember it across renders and change it itself, it's state — otherwise it's a
> prop.

---

## 3. List rendering and keys

#### The analogy

Keys are name tags at a conference. If everyone wears a name tag, the organiser can tell at a glance
that Priya left and Sam arrived, and only update those two seats. Without tags, all the organiser
knows is "there were 12 people, now there are 11" — so they re-seat the entire room, and anyone who'd
half-filled in a form loses it.

Array index as a key is a name tag that reads "person #3." When someone leaves, everyone behind them
gets a new number, and the organiser concludes that eight people changed identity.

#### The code

`src/features/discovery/ui/SearchScreen.jsx:282-286`:

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
  {suppliers.map((supplier) => (
    <SupplierCard key={supplier.id} supplier={supplier} onOpen={onOpenSupplier} />
  ))}
</div>
```

Three more from the same pattern family:

```jsx
// SearchScreen.jsx:100-118 — an inline literal array, keyed on a stable id string
{[
  { id: '', label: 'All' },
  { id: 'verified', label: 'Verified' },
  { id: 'audited', label: 'Audited' },
  { id: 'basic', label: 'Basic' },
  { id: 'unverified', label: 'Unverified' },
].map((b) => (
  <button key={b.id} onClick={() => updateParams({ band: b.id })} className={/* ... */}>
    {b.label}
  </button>
))}

// SupplierProfile.jsx:207-215 — keyed on the claim's domain key
{supplier.claims.map((claim) => (
  <ClaimRow
    key={claim.key}
    claim={claim}
    isOpen={activeClaimKey === claim.key}
    onToggle={() => handleToggleClaim(claim.key)}
    onOpenEvidence={(c) => setSelectedClaim(c)}
  />
))}

// ComparisonScreen.jsx:121-126 — nested maps, each level independently keyed
{rows.map((row) => (
  <div className="queue-row" style={tableColumns} key={row.label}>
    <div><strong>{row.label}</strong></div>
    {selected.map((supplier) => <div key={supplier.id}>{row.render(supplier)}</div>)}
  </div>
))}
```

#### Why we did it this way

`key={supplier.id}` uses the domain identifier — `"aravind-fasteners"`, `"kalyani-textiles"` — because
it is stable across every reorder, filter and sort this screen can perform.

That stability is load-bearing here. The sort dropdown reorders the whole array by rating, lead time
or MOQ. With stable keys, React sees the same five components in a new order and **moves the existing
DOM nodes**. With index keys, React would see position 0 change from Aravind to Kalyani and patch
every card's contents in place — more DOM work, and any internal state (a focused element, a scroll
position, a CSS transition mid-flight) would attach to the wrong supplier.

Nested maps matter too. In `ComparisonScreen`, the outer map is keyed on `row.label` and the inner on
`supplier.id`. Keys only need to be unique **among siblings**, not globally, so this is correct — and
also necessary, because both loops are generating sibling sets.

> ⚠️ **One place this codebase gets it wrong.** `ClaimRow.jsx:112-118` keys evidence items by array
> index:
>
> ```jsx
> {claim.evidence.map((item, idx) => (
>   <div key={idx} className="flex justify-between items-center ...">
> ```
>
> Today it's harmless — the evidence list is static and never reordered. It becomes a bug the moment
> evidence can be added, removed or sorted. `item.label` would be a better key. Know this one; "show me
> a place where your own keys are wrong" is a favourite examiner move.
>
> By contrast, `VerificationDashboard.jsx:191-192` keys a stepper on `idx`, and that one is genuinely
> fine — the array is a hardcoded literal of four fixed steps that can never reorder.

#### Viva question

> **Q: Why does React need a `key` on list items, and why is the array index usually a bad one?**
>
> **A:** The key is how React matches elements between renders so it can move existing DOM nodes
> instead of rebuilding them, and preserve any state attached to them. An index is bad because it
> describes position rather than identity — insert or reorder an item and every subsequent key now
> points at a different object, so React patches the wrong nodes.

---

## 4. Conditional rendering

#### The analogy

A ternary is a fork in the road: one way or the other, always exactly one. `&&` is a side door: you
only go through it if it's unlocked, otherwise you carry straight on. And `return null` is deciding
not to leave the house at all.

#### The code

**Ternary — two mutually exclusive branches.** `SupplierCard.jsx:37-51`:

```jsx
{isVerified ? (
  <span className="inline-flex items-center gap-1 px-3 py-1.5 bg-on-primary text-primary rounded-full text-xs font-bold shadow-sm">
    <span className={`material-symbols-outlined text-sm ${textColorClass}`} data-fill="true">
      verified
    </span>
    Verified
  </span>
) : (
  <span className="inline-flex items-center gap-1 px-3 py-1.5 bg-surface-card text-primary rounded-full text-xs font-bold border border-hairline shadow-sm">
    <span className="material-symbols-outlined text-sm text-brand-ochre" data-fill="false">
      hourglass_empty
    </span>
    {supplier.trust?.band === 'basic' ? 'Basic Standing' : 'Unverified'}
  </span>
)}
```

Note the nested ternary in the `else` branch. That's the maximum acceptable nesting — a third level
belongs in a lookup map.

**Three-way ternary chain.** `SearchScreen.jsx:276-301` — the loading / results / empty triad:

```jsx
{loading ? (
  <div className="p-12 text-center bg-surface-card rounded-2xl border border-hairline text-body-muted">
    <span className="material-symbols-outlined text-4xl animate-spin mb-2">progress_activity</span>
    <p>Scanning verified supplier records...</p>
  </div>
) : suppliers.length > 0 ? (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
    {suppliers.map((supplier) => (
      <SupplierCard key={supplier.id} supplier={supplier} onOpen={onOpenSupplier} />
    ))}
  </div>
) : (
  <div className="p-12 text-center bg-surface-card border-2 border-dashed border-hairline rounded-2xl flex flex-col items-center gap-3">
    <span className="material-symbols-outlined text-5xl text-brand-coral">search_off</span>
    <h3 className="font-title-lg text-title-lg text-primary font-bold">No suppliers match your current filters</h3>
    {/* ... */}
  </div>
)}
```

**Short-circuit `&&` — render or don't.** `App.jsx:125-131`:

```jsx
{toast && (
  <Toast
    message={toast.message}
    type={toast.type}
    onClose={() => setToast(null)}
  />
)}
```

And `SearchScreen.jsx:66` for the verification-guard banner:

```jsx
{isSelectToVerifyPrompt && (
  <div className="bg-brand-mint/25 border-2 border-brand-teal/30 rounded-2xl p-4 md:p-5 ...">
```

**Early return `null` — the component opts out entirely.** `Modal.jsx:2`, `Toast.jsx:2`,
`TrustBand.jsx:29`, `TrustPanel.jsx:11`:

```jsx
export function Modal({ isOpen, onClose, title, children, maxWidth = 'max-w-lg' }) {
  if (!isOpen) return null
  // ...
```

**Lookup maps instead of `switch`.** `ClaimRow.jsx:19-52` — six claim states, each with an icon, a
colour set and a badge label:

```jsx
const stateConfig = {
  verified:        { icon: 'check_circle',      bgClass: 'bg-brand-mint/20 text-brand-teal border-brand-teal/30', badge: 'Verified' },
  under_review:    { icon: 'hourglass_empty',   bgClass: 'bg-brand-ochre/20 text-primary border-brand-ochre/40',  badge: 'Under Review' },
  needs_more_info: { icon: 'help_outline',      bgClass: 'bg-brand-ochre/20 text-primary border-brand-ochre/40',  badge: 'Needs Info' },
  submitted:       { icon: 'pending',           bgClass: 'bg-surface-variant text-on-surface-variant border-hairline', badge: 'Submitted' },
  revoked:         { icon: 'cancel',            bgClass: 'bg-error-container text-on-error-container border-error/30', badge: 'Revoked' },
  expired:         { icon: 'schedule',          bgClass: 'bg-error-container text-on-error-container border-error/30', badge: 'Expired' },
}

const config = stateConfig[claim.state] || stateConfig.submitted
```

#### Why we did it this way

**Why `&&` for the toast and a ternary for the badge.** The toast has no alternative state — either
there's a message or the screen is unchanged. The badge always renders *something*; the only question
is which. Matching the operator to the shape of the decision makes the intent readable without
comment.

**The `&&` trap, and why it doesn't bite here.** `{count && <X/>}` renders a literal `0` when `count`
is zero, because `0` is falsy but still a valid React child. This codebase dodges it by only using
`&&` with genuine objects and booleans — `toast`, `isSelectToVerifyPrompt`, `selectedTask`,
`isOpen`. `ClaimRow.jsx:108` is the one to look at closely:

```jsx
{isOpen && claim.evidence && claim.evidence.length > 0 && (
```

That final `.length > 0` is deliberate. `claim.evidence.length &&` would have printed a bare `0` on
screen for any claim with no evidence.

**Why lookup maps rather than `switch`.** This is invariant 7 from `docs/CLAUDE.md`: *never hardcode a
claim type.* A `switch (claim.state)` grows a branch per state and turns adding a certification type
into a code change. A lookup object keyed on state means the mapping is data — it could be moved into
the API response tomorrow with no JSX edits. The `|| stateConfig.submitted` fallback is invariant 4:
an unknown state renders as an explicit designed state, never as a blank.

The same pattern appears in `TrustBand.jsx:1-26` (`bandMeta`), `Toast.jsx:4-16` (`icons`, `bgStyles`),
and `SupplierCard.jsx:4-20` (`bgHeaderClass`, `textColorClass`).

In `SupplierCard` there's an extra reason: Tailwind's compiler scans your source for literal class
strings. A computed `` `bg-${supplier.themeColor}` `` produces a class that never appears in the
source text, so Tailwind purges it from the build and the card renders with no background. The lookup
map keeps every class name literal.

#### Viva question

> **Q: When do you use `&&` versus a ternary for conditional rendering, and what's the classic bug with `&&`?**
>
> **A:** Use `&&` when the alternative is rendering nothing, and a ternary when you're choosing between
> two things to render. The classic bug is `{items.length && <List/>}` — when the array is empty the
> expression evaluates to `0`, which React renders as a visible zero, so you write
> `items.length > 0 &&` instead.

---

## 5. The React hooks toolkit

### 5.1 `useState` — reactive memory

#### The analogy

A whiteboard in a meeting room with a rule attached: whenever anyone rubs something out and writes
something new, everyone in the room re-reads the whole board. You can't quietly amend a corner. Any
change is announced.

#### The code

**Basic form** — `src/shared/ui/Header.jsx:4`:

```jsx
const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
```

**Lazy initialiser** — `src/features/supplier-onboarding/ui/OnboardingScreen.jsx:14-31`. Note the
*function* passed to `useState`, not a value:

```jsx
const [formData, setFormData] = useState(() => {
  try {
    const saved = localStorage.getItem('supify_supplier_onboarding_draft')
    if (saved) return JSON.parse(saved)
  } catch (e) {}
  return {
    legalName: 'Narmada Advanced Custom Fabrication Private Limited',
    tradeName: 'Narmada Fabrication',
    location: 'Indore, Madhya Pradesh, India',
    category: 'Sheet-metal fabrication',
    website: 'https://narmadafabrication.example.com',
    capacity: '50,000 units / month',
    moq: '100 units',
    leadTime: '21-28 Days',
    gstNumber: '23AAECA9082G1ZP',
    isoCertUploaded: true,
  }
})
```

**Lazy initialiser, function reference form** — `SupplierProfile.jsx:9-15, 26`:

```jsx
function readShortlist() {
  try {
    return JSON.parse(localStorage.getItem(SHORTLIST_KEY)) || []
  } catch {
    return []
  }
}

// ...
const [shortlist, setShortlist] = useState(readShortlist)   // note: no parentheses
```

**Functional update** — `OnboardingScreen.jsx:42-44` and `ComparisonScreen.jsx:60-62`:

```jsx
const handleChange = (field, val) => {
  setFormData((prev) => ({ ...prev, [field]: val }))
}

function retry() {
  setRetryToken((token) => token + 1)
}
```

#### Why we did it this way

**The lazy initialiser is not a style choice.** `useState(readShortlist())` — with parentheses — would
call `readShortlist()` on *every single render*, hitting `localStorage` and running `JSON.parse` dozens
of times, and React would throw all but the first result away. Passing the function itself means React
calls it exactly once, on mount. In `OnboardingScreen` this matters more than usual, because that
component re-renders on every keystroke.

**The functional update is about correctness, not elegance.** `setFormData({...formData, [field]: val})`
reads `formData` from the closure of the render in which the handler was created. If two updates queue
in the same tick, the second one reads a stale snapshot and silently discards the first. `(prev) => ...`
asks React for the current value at the moment the update is applied.

**The `retryToken` pattern is worth stealing.** `ComparisonScreen` needs a way to re-run a `useEffect`
on demand. You can't call an effect directly. So it keeps a counter in state, lists it in the
dependency array (`:36`), and increments it to force a re-run. It's a state variable whose *value* is
meaningless and whose *change* is the entire point.

#### Viva question

> **Q: What's the difference between `useState(expensiveCall())` and `useState(expensiveCall)`?**
>
> **A:** The first invokes the function on every render and discards the result after the first, which
> in `OnboardingScreen` would mean parsing `localStorage` on every keystroke. The second passes the
> function itself as a lazy initialiser, so React calls it only once on mount.

---

### 5.2 `useEffect` — synchronising with the outside world

#### The analogy

A standing order at a shop. "Whenever my order number changes, fetch the new item; and if I cancel,
tear up the order so nothing arrives after I've left." Setup runs when the dependencies change;
cleanup runs before the next setup and once more on unmount.

The common misreading is "run this after render." The accurate reading is "keep this external thing in
sync with these values." External means anything outside React: the network, `localStorage`, the
document title, a timer, a subscription.

#### The code

**Fetch on dependency change** — `src/features/discovery/ui/SearchScreen.jsx:19-40`:

```jsx
useEffect(() => {
  setLoading(true)
  supplierRepository
    .search({ query, band, region, industry, sortBy })
    .then((data) => {
      let res = data
      if (extraFilter === 'iso_9001') {
        res = res.filter((s) => s.claims.some((c) => c.key.includes('iso') || c.label.includes('ISO')))
      } else if (extraFilter === 'lead_time_fast') {
        res = res.filter((s) => {
          const num = parseInt(s.leadTime) || 99
          return num <= 14
        })
      }
      setSuppliers(res)
      setLoading(false)
    })
    .catch(() => {
      setSuppliers([])
      setLoading(false)
    })
}, [query, band, region, industry, sortBy, extraFilter])
```

**Fetch with cancellation** — `src/features/comparison/ui/ComparisonScreen.jsx:21-36`. This is the
better pattern of the two:

```jsx
useEffect(() => {
  let cancelled = false
  async function loadSuppliers() {
    setHasError(false)
    try {
      const results = await supplierRepository.search({})
      if (!cancelled) setSuppliers(results)
    } catch {
      if (!cancelled) setHasError(true)
    }
  }
  loadSuppliers()
  return () => {
    cancelled = true
  }
}, [retryToken])
```

**Write-through to localStorage** — `OnboardingScreen.jsx:35-40`:

```jsx
useEffect(() => {
  try {
    localStorage.setItem('supify_supplier_onboarding_draft', JSON.stringify(formData))
    setSavedStatus('Draft saved locally just now')
  } catch (e) {}
}, [formData])
```

**Run once on mount** — `VerificationDashboard.jsx:52-54`:

```jsx
useEffect(() => {
  supplierRepository.getVerificationQueue().then(setTasks)
}, [])
```

#### Why we did it this way

**Dependency arrays are the whole game.**

| Array | Meaning | Example |
| --- | --- | --- |
| omitted | after *every* render | — (not used here; it's an infinite-loop machine) |
| `[]` | once on mount | `VerificationDashboard.jsx:54` |
| `[a, b]` | whenever `a` or `b` changes | `SearchScreen.jsx:40` |

**How the infinite loop happens, concretely.** An effect that calls `setSuppliers` causes a re-render.
If the array is omitted, the effect runs again after that render, calls `setSuppliers` again, and the
browser locks up. The six-item array in `SearchScreen` is what makes it terminate: the effect only
re-runs when a filter actually changes, and setting `suppliers` isn't a filter.

**Why `ComparisonScreen`'s `cancelled` flag matters.** Imagine the user navigates away 50 ms into a
200 ms request. Without the flag, the promise resolves after unmount and calls `setSuppliers` on a
component that no longer exists. The cleanup function flips `cancelled` to `true`, and the resolution
handler checks it before touching state. This also prevents the **race condition** where an old, slow
request resolves *after* a newer one and overwrites fresh data with stale data.

`SearchScreen` has no such guard. With filters changing on every keystroke and 200 ms of simulated
latency, overlapping requests are guaranteed, and the last-to-resolve wins rather than the
last-to-be-requested. This is the single most impactful fix available in the codebase.

**Why `[formData]` is the right dependency for autosave.** Because `handleChange` builds a *new object*
every time, `formData`'s reference changes on every keystroke, so the effect fires on every keystroke.
That's not accidental — it's invariant 12, *never lose a supplier's work*. The `try/catch` with an
empty body is deliberate: `localStorage` throws in Safari private mode, and failing to save a draft
must never crash the form.

**StrictMode.** `src/main.jsx:9` wraps the app in `<StrictMode>`, which in development mounts every
component twice to surface missing cleanup. So every effect here runs twice in dev and once in
production. `ComparisonScreen` handles it correctly. `SearchScreen` fires two identical requests. That
double-invocation is a feature — it's React telling you your effect isn't idempotent.

> ⚠️ **A real bug in `App.jsx:21-26`** that this section is the right place to expose:
>
> ```jsx
> const showToast = (message, type = 'success') => {
>   setToast({ message, type })
>   setTimeout(() => {
>     setToast(null)
>   }, 4000)
> }
> ```
>
> No cleanup, and no cancellation of a previous timer. Fire a toast at t=0 and another at t=3s: the
> first timer still fires at t=4s and clears the *second* toast, which got one second of life instead
> of four. The fix is a `useRef` holding the timeout id with a `clearTimeout` before each new one — see
> §5.5, where this is the perfect use case for the hook this codebase doesn't use.

#### Viva question

> **Q: What does the dependency array do, and how do you avoid an infinite loop?**
>
> **A:** It tells React which values the effect depends on, so the effect re-runs only when one of them
> changes — omitting it entirely means "after every render." The loop happens when an effect with no
> dependency array sets state, since that re-render retriggers the effect; you fix it by listing the
> real inputs, as `SearchScreen` does with its six filter values.

---

### 5.3 `useMemo` — caching a computed value

#### The analogy

Working out your monthly expenses. If nothing in the spreadsheet changed since yesterday, you don't
add up 400 rows again — you look at yesterday's total. `useMemo` is that: a remembered answer that's
only recalculated when its inputs change.

#### The code

`src/features/comparison/ui/ComparisonScreen.jsx:38-48` — two memos, one feeding the other:

```jsx
const idsParam = searchParams.get('ids') || ''

const selectedIds = useMemo(
  () => new Set(idsParam.split(',').filter(Boolean)),
  [idsParam],
)

const selected = useMemo(
  () => (suppliers || []).filter((supplier) => selectedIds.has(supplier.id)),
  [suppliers, selectedIds],
)
```

#### Why we did it this way

The first memo is about **referential identity**, not CPU time. `new Set(...)` is cheap — splitting a
short string costs nothing. But it returns a *brand new object every time it runs*. Without the memo,
every render produces a fresh `Set` with a different reference, which would invalidate the second
memo's `[suppliers, selectedIds]` dependency on every render, making it useless. And it would break
`toggleId`'s `useCallback` too, for the same reason.

So memo #1 exists to stabilise the reference that memo #2 and the callback depend on. **That's the
most common real reason to reach for `useMemo`** — not raw speed, but keeping a reference stable so
that downstream memoisation actually works. A memo chain is only as stable as its weakest link.

The second memo is the one that saves actual work: filtering the supplier list against the selected
set. With five fixtures it's trivial; with 5,000 suppliers and a render on every checkbox toggle, it's
not.

Choosing a `Set` over an array is deliberate too — `selectedIds.has(supplier.id)` is O(1), where
`selectedIds.includes(...)` would be O(n), turning the filter into O(n×m).

**When not to use `useMemo`.** It isn't free: React stores the value and the dependency array, and
compares the array on every render. For a cheap calculation whose result isn't a dependency of
anything else, that bookkeeping costs more than the calculation. `ComparisonScreen.jsx:77-86` builds
`tableColumns` and the `rows` array on every render with no memo at all, and that's the right call —
nothing downstream depends on their identity.

#### Viva question

> **Q: Why is `selectedIds` wrapped in `useMemo` when building a `Set` is already cheap?**
>
> **A:** Because `new Set()` returns a new reference every render, and both the `selected` memo and the
> `toggleId` callback list it as a dependency — without memoisation they'd be invalidated on every
> render and their own memoisation would be pointless. The memo is there to stabilise the reference,
> not to save the cost of the computation.

---

### 5.4 `useCallback` — caching a function

#### The analogy

Same idea as `useMemo`, but the thing being remembered is a function rather than a value. It's the
difference between handing someone your phone number written on a fresh scrap of paper every time you
meet — same digits, different piece of paper — and giving them a business card they can keep. Same
information; only the second one lets them notice nothing changed.

#### The code

`src/features/comparison/ui/ComparisonScreen.jsx:50-58`:

```jsx
const toggleId = useCallback((supplierId) => {
  const next = new Set(selectedIds)
  if (next.has(supplierId)) next.delete(supplierId)
  else next.add(supplierId)
  const updated = new URLSearchParams(searchParams)
  if (next.size > 0) updated.set('ids', [...next].join(','))
  else updated.delete('ids')
  setSearchParams(updated)
}, [searchParams, selectedIds, setSearchParams])
```

Passed down to each row at `:102`:

```jsx
{(suppliers || []).map((supplier) => (
  <SupplierPick key={supplier.id} supplier={supplier} checked={selectedIds.has(supplier.id)} onToggle={toggleId} />
))}
```

#### Why we did it this way

A function declared inside a component body is recreated on every render. Normally nobody cares. It
matters when the function is passed to a child, because a new reference makes the child's props
"change" even though nothing meaningful did.

`toggleId` goes to every `SupplierPick` in the list. Wrapping it means the reference is stable while
`searchParams` and `selectedIds` are unchanged.

**The honest caveat:** `SupplierPick` is *not* wrapped in `React.memo`, so it re-renders regardless.
Right now `useCallback` here buys nothing measurable. It's correct, defensive, and currently inert.
Own that in a viva rather than over-claiming — "it's the right shape for when `SupplierPick` gets
memoised, and it costs a dependency-array comparison in the meantime" is a much stronger answer than
pretending it's an optimisation.

Note also that the update is **immutable throughout**: `new Set(selectedIds)` copies before mutating,
`new URLSearchParams(searchParams)` copies before setting. Neither the state nor the URL object is
touched in place.

And the interesting design decision — `toggleId` doesn't call `setState` at all. It calls
`setSearchParams`. The selection *is* the URL. There's no local copy to drift out of sync, and the
comparison set is shareable by construction (invariant 11).

#### Viva question

> **Q: What's the difference between `useMemo` and `useCallback`?**
>
> **A:** `useMemo` caches the *result* of calling a function; `useCallback` caches the *function
> itself*. `useCallback(fn, deps)` is exactly equivalent to `useMemo(() => fn, deps)` — it's a
> convenience wrapper for the common case of passing a stable handler to a child component.

---

### 5.5 `useRef` — a box that doesn't trigger re-renders

> **This hook does not appear anywhere in the Supify codebase.** Zero uses across all of `src/`. What
> follows explains the concept honestly and shows the two places where it should be used. Do not claim
> in a viva that Supify uses `useRef`.

#### The analogy

A sticky note on your monitor versus a slide in a presentation. Change the slide and the whole room
re-reads it — that's state. Change the sticky note and nobody re-reads anything; it's just there when
you next look — that's a ref.

`useRef` gives you a mutable box, `{ current: ... }`, that survives across renders and does **not**
trigger a re-render when you change it. Two jobs: holding a DOM node, and holding a mutable value that
isn't part of the visual output.

#### The code (what it would look like here)

**Use case 1 — fixing the toast timer bug from §5.2.** `App.jsx:21-26` currently leaks timers:

```jsx
// CURRENT — src/app/App.jsx:21-26. Buggy: a second toast within 4s is cut short.
const showToast = (message, type = 'success') => {
  setToast({ message, type })
  setTimeout(() => {
    setToast(null)
  }, 4000)
}
```

```jsx
// PROPOSED — not in the codebase.
const toastTimer = useRef(null)

const showToast = (message, type = 'success') => {
  if (toastTimer.current) clearTimeout(toastTimer.current)
  setToast({ message, type })
  toastTimer.current = setTimeout(() => setToast(null), 4000)
}

useEffect(() => () => clearTimeout(toastTimer.current), [])
```

The timeout id has to persist across renders but must never *cause* one — which is the definition of a
ref. Putting it in `useState` would re-render the whole app shell every time a toast started.

**Use case 2 — focus management in `Modal`.** `Modal.jsx` currently has no focus handling, which is an
accessibility gap flagged in the project guide:

```jsx
// PROPOSED — not in the codebase.
export function Modal({ isOpen, onClose, title, children }) {
  const closeButtonRef = useRef(null)

  useEffect(() => {
    if (isOpen) closeButtonRef.current?.focus()
  }, [isOpen])

  if (!isOpen) return null

  return (
    /* ... */
    <button ref={closeButtonRef} onClick={onClose}>
      <span className="material-symbols-outlined text-lg">close</span>
    </button>
    /* ... */
  )
}
```

#### Why it's absent, and why that's a gap

Supify's UI is almost entirely driven by data flowing down from the repository layer, so there was
rarely a reason to reach for an escape hatch out of the React model. That's healthy — `useRef` for DOM
access should be a last resort, not a habit.

But two genuine needs went unmet as a result. The toast timer is a real bug caused by not having a
place to stash a mutable id. And `docs/CLAUDE.md`'s definition of done requires "fully keyboard
operable," which for a modal means moving focus in on open, trapping it while open, and returning it
to the trigger on close. All three need refs.

#### Viva question

> **Q: When would you use `useRef` instead of `useState`?**
>
> **A:** When you need a value that persists across renders but must not cause one — a timeout id, a
> previous value, a DOM node. In this codebase the toast timer in `App.jsx` is exactly that case:
> it currently leaks timers because there's nowhere to store the id and cancel it.

---

### 5.6 Custom hooks — packaging stateful logic

> **No custom hooks are defined in this codebase either.** What follows is the pattern and the
> refactor this code is asking for. Again: don't claim one exists.

#### The analogy

Once you've explained the same thing three times, you write it down and hand out copies. A custom hook
is that document — it's not a new React feature, just a function whose name starts with `use` and that
calls other hooks, so stateful logic can be extracted and reused the same way you'd extract any
ordinary function.

#### The code (the refactor this code is asking for)

**The duplication.** Three screens contain the same shape: a loading flag, a data slot, an error slot,
and an effect that fetches and guards against unmount. `SearchScreen.jsx:8-40`,
`ComparisonScreen.jsx:17-36`, `SupplierProfile.jsx:23-40` and
`VerificationTaskDetail.jsx:14-38` all reimplement it.

**The extraction** (would live at `src/shared/hooks/useAsyncData.js`):

```jsx
// PROPOSED — not in the codebase.
import { useEffect, useState } from 'react'

export function useAsyncData(loader, deps) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [retryToken, setRetryToken] = useState(0)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    loader()
      .then((result) => { if (!cancelled) { setData(result); setLoading(false) } })
      .catch((err)   => { if (!cancelled) { setError(err);   setLoading(false) } })
    return () => { cancelled = true }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, retryToken])

  return { data, loading, error, retry: () => setRetryToken((t) => t + 1) }
}
```

**The call site.** `SupplierProfile.jsx:23-40` — eighteen lines — collapses to two:

```jsx
// PROPOSED — not in the codebase.
const { data: supplier, loading } = useAsyncData(
  () => supplierRepository.getById(supplierId),
  [supplierId],
)
```

#### Why we did it this way (or rather, why we didn't)

The screens were built one at a time, each solving its own fetch. By the time the third appeared, the
pattern was visible but the code was working. That's the ordinary way duplication accumulates, and
it's worth naming honestly rather than pretending the design was deliberate.

The cost is concrete and measurable. `ComparisonScreen` got cancellation and a retry button;
`SearchScreen` got neither. The same logic, implemented four times, produced four different quality
levels. A custom hook would have given all four screens the best version — including the race-condition
guard that `SearchScreen` most needs.

**The rules, for the viva:**

1. The name must start with `use`. This isn't cosmetic — the linter uses it to decide whether hook
   rules apply inside the function.
2. A custom hook may call other hooks; a plain function may not.
3. Each call gets **its own independent state**. Two components calling `useAsyncData` do not share
   data. Hooks reuse *logic*, not *state* — that's what Context is for.

#### Viva question

> **Q: What makes a function a custom hook, and do two components calling it share state?**
>
> **A:** It's a function whose name begins with `use` and which calls other hooks — the naming
> convention is what lets React's linter enforce the rules of hooks inside it. Each call site gets
> completely independent state; custom hooks share logic, not data, which is what Context exists for.

---

### 5.7 The Rules of Hooks

Two rules, and both have the same underlying cause.

**1. Only call hooks at the top level.** Never inside a condition, loop, or nested function.

**2. Only call hooks from React function components or other custom hooks.**

**Why.** React doesn't know your hooks' names. It tracks them **by call order** — first `useState` in
this component gets slot 0, second gets slot 1, and so on, on every render. Put a hook behind an `if`
and the order shifts between renders, so slot 1 now returns the value that belonged to slot 2. Your
state silently swaps.

`Modal.jsx` demonstrates the correct handling of the awkward case — an early return *before* any hook:

```jsx
export function Modal({ isOpen, onClose, title, children, maxWidth = 'max-w-lg' }) {
  if (!isOpen) return null       // ← safe: no hooks in this component at all
```

`Modal` calls no hooks, so returning early is fine. But `VerificationDashboard.jsx:72-81` shows the
pattern you must follow when hooks *are* involved — **all seven `useState` calls and both `useEffect`
calls happen first (lines 11-54), and only then** does the loading guard return early:

```jsx
if (supplierLoading || !verifySupplier) {
  return (
    <main className="flex-grow w-full max-w-container-max mx-auto px-lg py-16 flex flex-col items-center justify-center text-center">
      <span className="material-symbols-outlined text-5xl text-brand-teal animate-spin mb-3">
        progress_activity
      </span>
      <p className="text-body-muted font-medium">Loading verification dossier...</p>
    </main>
  )
}
```

Hooks above, guards below. That ordering is not stylistic.

---

## 6. Component communication and composition

### 6.1 Lifting state up

#### The analogy

Two children argue over whose turn it is with a toy. Neither can settle it, because neither can see
the other's position. The parent holds the rota, and both children ask the parent. The shared fact
lives at the lowest point from which everyone who needs it can see it.

#### The code

`src/app/App.jsx:18-26` — the toast and the auth modal both live in the root component, because
multiple unrelated features need them:

```jsx
export default function App() {
  const navigate = useNavigate()
  const location = useLocation()
  const [toast, setToast] = useState(null)
  const [authModalMode, setAuthModalMode] = useState(null) // null | 'login' | 'signup'

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
    setTimeout(() => {
      setToast(null)
    }, 4000)
  }
```

`showToast` is handed to the three routes that need it (`App.jsx:65-119`):

```jsx
<Route
  path="/suppliers/:supplierId"
  element={
    <SupplierProfile
      onBack={() => handleNavigate('/search')}
      onShowToast={showToast}
      onOpenVerification={(id) => handleNavigate(`/verification?supplier=${id}`)}
    />
  }
/>
```

And `authModalMode` is opened from the `Header` (`App.jsx:38`) but rendered by `App` (`:134-138`):

```jsx
<Header
  currentPath={location.pathname}
  onNavigate={handleNavigate}
  onOpenAuth={(mode) => setAuthModalMode(mode)}
/>

{/* ... */}

<Modal
  isOpen={!!authModalMode}
  onClose={() => setAuthModalMode(null)}
  title={authModalMode === 'login' ? 'Log In to Supify' : 'Create Supify Account'}
>
```

#### Why we did it this way

Toasts are triggered from four different places — approving a supplier, approving a task, toggling a
shortlist, completing an onboarding step — and they all need to render in the same fixed position,
one at a time. If each feature owned its own toast state you'd get two overlapping toasts in the
bottom-right corner and no way to coordinate them. So the state goes to the lowest common ancestor,
which is `App`.

The `Header`/`Modal` split is the clearer illustration of the principle. The header *knows when the
user wants to log in*. The modal *renders the form*. They're siblings — neither can reach the other.
The state that connects them therefore belongs to their parent, and `!!authModalMode` doubles as both
the "which mode" value and the "is it open" boolean.

Note the callback naming: `onNavigate`, `onShowToast`, `onOpenAuth`, `onOpenVerification`, `onToggle`,
`onOpenSupplier`. The `on*` prefix marks a prop as "a thing you call to ask the parent to do
something", which makes the direction of data flow legible at a glance — data flows down, events flow
up.

#### Viva question

> **Q: What does "lifting state up" mean, and why does the toast live in `App.jsx`?**
>
> **A:** It means moving shared state to the lowest common ancestor of every component that needs it,
> so there's a single source of truth. The toast lives in `App` because four different features trigger
> it and it renders in one fixed position — per-feature toast state would let two render at once with
> no way to coordinate.

---

### 6.2 Composition via `children`

#### The analogy

A picture frame doesn't care what picture goes in it. It handles the edges, the glass and the hook on
the wall, and the picture is supplied by whoever hangs it. `children` is the gap in the frame.

The alternative — a frame that takes `imageUrl`, `caption`, `borderWidth` props — has to be modified
every time you want to frame something new.

#### The code

**`Modal` — the generic shell.** `src/shared/ui/Modal.jsx:1, 17-19`:

```jsx
export function Modal({ isOpen, onClose, title, children, maxWidth = 'max-w-lg' }) {
  // ...
        <div className="overflow-y-auto flex-grow pr-1">
          {children}
        </div>
```

`Modal` owns the backdrop, the blur, the centring, the header row, the close button, the max height
and the scroll behaviour. It knows nothing about what's inside it.

**The caller supplies the content.** `App.jsx:134-172` — an entire login form passed as children:

```jsx
<Modal
  isOpen={!!authModalMode}
  onClose={() => setAuthModalMode(null)}
  title={authModalMode === 'login' ? 'Log In to Supify' : 'Create Supify Account'}
>
  <form
    onSubmit={(e) => {
      e.preventDefault()
      setAuthModalMode(null)
      showToast(`Welcome back to Supify!`)
    }}
    className="flex flex-col gap-4 text-sm"
  >
    <div>
      <label className="block text-xs font-bold text-primary mb-1">Work Email</label>
      <input required type="email" placeholder="procurement@enterprise.com" className="..." />
    </div>
    {/* ... */}
    <button type="submit" className="...">
      {authModalMode === 'login' ? 'Log In' : 'Sign Up Free'}
    </button>
  </form>
</Modal>
```

**`ProtectedRoute` — the same pattern as a gate.** `src/app/ProtectedRoute.jsx:4-20`:

```jsx
export function ProtectedRoute({ requiredRole, children }) {
  const session = useContext(UserRoleContext)

  if (session.role === requiredRole) return children

  return (
    <main className="page">
      <div className="empty-state">
        <span aria-hidden="true">⊘</span>
        <h2>{roleLabels[requiredRole]} access required</h2>
        <p>You are currently acting as {roleLabels[session.role]}. Switch your active role to open this console.</p>
        <button className="button" onClick={() => session.setRole(requiredRole)}>
          Continue as {roleLabels[requiredRole]}
        </button>
      </div>
    </main>
  )
}
```

`children` is returned *unchanged* when the check passes, and replaced entirely when it fails. The
guarded component doesn't know it's being guarded.

#### Why we did it this way

**The alternative is worse in a specific way.** A `Modal` with `formFields`, `submitLabel` and
`onSubmit` props works until someone needs a modal containing a table. Then you add a `variant` prop.
Then a modal with a table *and* a form. Every new use case is a change to the shared component, and
the shared component slowly becomes a union of every screen that ever used it.

With `children`, `Modal` has been written once and will never need to change. The evidence inspector
in `SupplierProfile.jsx:237-297` and the task review modal in `VerificationDashboard.jsx:422-488`
have completely different contents, and both could use the same shell without touching it.

**The prop-drilling comparison.** Prop drilling is passing a prop through components that don't use
it, purely to reach a descendant. Composition often dissolves the problem: instead of
`<Modal contentProps={...}>` threading data down, you build the content *where the data already is*
and hand the finished element to `Modal`. The data never travels.

Supify does have a small amount of genuine drilling — `onShowToast` goes from `App` into
`SupplierProfile` and `OnboardingScreen`. At one level deep that's fine. If it needed to reach four
levels, Context would be the answer.

#### Viva question

> **Q: What is the `children` prop and how does it differ from prop drilling?**
>
> **A:** `children` is whatever JSX a caller nests inside a component's tags, letting the component act
> as a generic container that knows nothing about its contents — `Modal` owns the backdrop and header
> while the caller supplies the body. It avoids prop drilling because the content is built where its
> data already lives, so nothing has to be threaded down through intermediate components.

---

### 6.3 Context — for when drilling genuinely hurts

#### The analogy

Props are handing a note person to person down a line. Context is the public address system: the
speaker announces once, and anyone in the building who's listening hears it, no matter how far from
the stage.

The cost is that it's harder to trace. With props, you can follow a value up the tree by reading the
code. With Context, the value could come from anywhere above you.

#### The code

**Creating and providing** — `src/entities/user/model/UserRoleContext.jsx`, in full:

```jsx
import { createContext, useState } from 'react'

export const UserRoleContext = createContext(null)

export const roleLabels = {
  buyer: 'Buyer',
  supplier: 'Supplier',
  verifier: 'Verifier',
}

const roles = Object.keys(roleLabels)

export function UserRoleProvider({ children }) {
  const [role, setRole] = useState('buyer')

  function cycleRole() {
    setRole((current) => roles[(roles.indexOf(current) + 1) % roles.length])
  }

  return (
    <UserRoleContext.Provider value={{ role, setRole, cycleRole }}>
      {children}
    </UserRoleContext.Provider>
  )
}
```

**Mounting the provider** — `src/main.jsx:8-16`:

```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <UserRoleProvider>
        <App />
      </UserRoleProvider>
    </BrowserRouter>
  </StrictMode>,
)
```

**Consuming** — `src/app/ProtectedRoute.jsx:5`:

```jsx
const session = useContext(UserRoleContext)
```

#### Why we did it this way

The user's active role is the textbook Context case. It's needed by the header (to show the role
switcher), by route guards (to decide access) and potentially by any console screen — components
scattered across the tree with no useful common ancestor other than the root. Threading `role` and
`setRole` through every intermediate component would be noise in a dozen files that don't care.

Note that `UserRoleProvider` wraps `<App />` **inside** `<BrowserRouter>`. Order matters: anything that
needs routing hooks must be inside the router, and anything that needs role must be inside the
provider. Nesting the provider inside the router gives both to everything below.

> ⚠️ **Honest status: this Context is effectively dead code.** The provider is mounted, but its only
> consumer is `ProtectedRoute`, and `ProtectedRoute` is imported by nothing — no route in `App.jsx`
> uses it. The role-switching UI described in the README was removed during the tactile redesign
> (commits `a2fbc28`, `fe0ac48`) and the guard was never re-wired. So Supify *demonstrates* Context
> correctly and *uses* it nowhere. Say that plainly if asked; it's a much better answer than
> implying the app has working role-based access control.

#### Viva question

> **Q: When should you reach for Context instead of props?**
>
> **A:** When a value is needed by many components at different depths and threading it through
> intermediates adds noise without meaning — auth, theme, locale, or the active user role here. For
> anything passing one or two levels, props are clearer, because Context makes a value's origin harder
> to trace.

---

### 6.4 Inversion of control — letting the parent decide navigation

Worth its own short section, because `SupplierCard` does something subtle.

#### The code

`src/entities/supplier/ui/SupplierCard.jsx:77-85`:

```jsx
<Link
  to={`/suppliers/${supplier.id}`}
  onClick={onOpen ? (e) => { e.preventDefault(); onOpen(supplier.id); } : undefined}
  className="block"
>
  <h3 className={`font-title-lg text-lg font-bold text-primary mb-1 line-clamp-1 transition-colors cursor-pointer ${textColorClass}`}>
    {supplier.tradeName}
  </h3>
</Link>
```

And the parent supplying the override, `App.jsx:46-49`:

```jsx
<Route
  path="/search"
  element={<SearchScreen onOpenSupplier={(id) => handleNavigate(`/suppliers/${id}`)} />}
/>
```

…where `handleNavigate` adds scroll-to-top behaviour (`App.jsx:28-31`):

```jsx
const handleNavigate = (path) => {
  navigate(path)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
```

#### Why we did it this way

The card is always a real `<Link>` with a real `href`. That means middle-click opens a new tab,
right-click offers "copy link address", and a crawler can follow it — all the things you lose when you
fake navigation with an `onClick` on a `<div>`.

But when a parent passes `onOpen`, the click handler calls `e.preventDefault()` and delegates instead.
`SearchScreen` uses this to route through `handleNavigate`, which scrolls to the top — without it, you
click a supplier at the bottom of the grid and land halfway down the profile page.

The `onOpen ? ... : undefined` ternary is what makes the component work in both worlds: give it a
callback and it delegates, give it nothing and it's a plain link. The same pattern appears at
`SupplierCard.jsx:120-126` and `SupplierProfile.jsx:145-152`.

---

## 7. React Router v6 and multi-page SPA navigation

### 7.1 SPA vs traditional multi-page

#### The analogy

A traditional multi-page site is a theatre that strikes the entire set between scenes — lights up,
everything carted off, new set built, lights down. Correct, but everyone sits in the dark for a while
and any prop an actor was holding is gone.

An SPA is a revolving stage. The building, the lights and the crew stay exactly as they are; only the
scenery rotates. Faster, and anything you were holding is still in your hand.

#### The code

`src/main.jsx:8-16` — the *entire* application mounts into one DOM node, once:

```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <UserRoleProvider>
        <App />
      </UserRoleProvider>
    </BrowserRouter>
  </StrictMode>,
)
```

And `index.html:13-16` — the complete server-delivered document. Note that there is no content in it:

```html
<body class="bg-background text-on-background font-body-md antialiased min-h-screen flex flex-col selection:bg-brand-pink selection:text-white">
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
```

#### Why we did it this way

**Three concrete wins visible in this app.**

1. **Persistent shell.** `App.jsx:35-39` renders `<Header>` *outside* `<Routes>`. Navigate from
   Landing to Search to a profile and the header is never unmounted — no flicker, no re-render, and
   the mobile drawer keeps its open/closed state across navigation. In an MPA the header is rebuilt
   from scratch on every page.

2. **State survives navigation.** The toast in `App.jsx:125` lives above the routes. Approve a supplier
   on `/verification`, get navigated elsewhere, and the toast is still on screen finishing its four
   seconds. A full page load would kill it mid-sentence.

3. **No white flash.** Route changes swap a React subtree. There's no network round trip for HTML, no
   re-parse, no re-execution of the bundle. With `SIMULATED_LATENCY_MS = 200` on the data layer, the
   *data* takes 200 ms — but the layout, header and loading state appear instantly.

**The trade-off, stated honestly:** the initial bundle is larger, and the server must be configured to
return `index.html` for *any* path, or a hard refresh on `/suppliers/aravind-fasteners` produces a real
404 from the web server before React ever loads. Vite's dev server handles this automatically;
production hosting needs an explicit rewrite rule.

#### Viva question

> **Q: What's the difference between an SPA and a traditional multi-page application?**
>
> **A:** An MPA requests a fresh HTML document from the server for every navigation, discarding all
> client state; an SPA loads once and swaps components client-side, so the shell and state persist.
> In Supify that's why the header never re-mounts and a toast fired on one route survives the
> navigation to another.

---

### 7.2 `BrowserRouter`, `Routes`, `Route`

#### The analogy

`BrowserRouter` is the receptionist who knows what floor you're on and can move you without leaving the
building. `Routes` is the directory board. Each `Route` is one line on that board: *this address →
that office.*

#### The code

**The router, at the top** — `main.jsx:10-14`. It must wrap everything that uses routing hooks,
because it's what provides the location context they read from.

**The route table** — `src/app/App.jsx:41-122`, abridged to show the shape:

```jsx
<Routes>
  <Route path="/" element={<LandingScreen onNavigate={handleNavigate} />} />
  <Route path="/search"   element={<SearchScreen onOpenSupplier={(id) => handleNavigate(`/suppliers/${id}`)} />} />
  <Route path="/solutions" element={<SearchScreen onOpenSupplier={(id) => handleNavigate(`/suppliers/${id}`)} />} />
  <Route path="/discovery" element={<SearchScreen onOpenSupplier={(id) => handleNavigate(`/suppliers/${id}`)} />} />
  <Route path="/compare"  element={<ComparisonScreen />} />
  <Route
    path="/suppliers/:supplierId"
    element={
      <SupplierProfile
        onBack={() => handleNavigate('/search')}
        onShowToast={showToast}
        onOpenVerification={(id) => handleNavigate(`/verification?supplier=${id}`)}
      />
    }
  />
  <Route path="/verification"   element={<VerificationDashboard onOpenSupplier={...} onShowToast={showToast} />} />
  <Route path="/verify"         element={<VerificationDashboard onOpenSupplier={...} onShowToast={showToast} />} />
  <Route path="/verifier/queue" element={<VerificationDashboard onOpenSupplier={...} onShowToast={showToast} />} />
  <Route path="/verifier/task/:taskId" element={<VerificationTaskDetail />} />
  <Route path="/supplier"            element={<OnboardingScreen onShowToast={showToast} onNavigate={handleNavigate} />} />
  <Route path="/supplier/onboarding" element={<OnboardingScreen onShowToast={showToast} onNavigate={handleNavigate} />} />
  <Route path="*" element={<NotFound />} />
</Routes>
```

#### Why we did it this way

**`element={<Component />}` is a v6 change worth knowing.** React Router v5 used
`component={Component}` or a render prop. v6 takes an actual JSX element, which is why props can be
passed inline — `element={<SupplierProfile onShowToast={showToast} />}`. In v5 that required a render
prop and a closure. This is the single most likely v5-vs-v6 exam question.

**Aliases exist for good reasons.** `/search`, `/solutions` and `/discovery` all render `SearchScreen`
because the nav label says "Solutions", earlier links said `/search`, and the internal vocabulary says
"discovery". Three spellings of one idea, and none of them 404s. Same for
`/verification` · `/verify` · `/verifier/queue`.

**The catch-all must be last in the source,** but not for the reason most people assume. React Router
v6 ranks routes by specificity and picks the best match regardless of source order — `path="*"` is the
lowest-ranked pattern, so it only wins when nothing else matches. Source order is convention and
readability, not mechanics. That's a genuine v5→v6 behavioural change: in v5, `<Switch>` matched the
*first* match in order, so order was load-bearing.

> ⚠️ Two dead links exist. `VerificationTaskDetail.jsx:64, 75` link to `/verify/queue`, and
> `VerificationQueue.jsx:87` links to `/verify/tasks/${task.id}`. The registered routes are
> `/verifier/queue` and `/verifier/task/:taskId`. Both are leftovers from the pre-redesign route
> table, and `/verify/queue` currently resolves to the 404.

#### Viva question

> **Q: What changed between React Router v5 and v6 in how you declare a route?**
>
> **A:** v5 used `component={X}` or a render prop and matched the first match in source order inside a
> `<Switch>`; v6 uses `element={<X />}`, which lets you pass props inline, and `<Routes>` picks the
> best match by specificity rather than by order. That's why `path="*"` in `App.jsx` works as a
> catch-all without depending on where it sits.

---

### 7.3 Dynamic routes and `useParams`

#### The analogy

A hotel corridor. `/suppliers/:supplierId` is the rule "any door on this corridor is a guest room."
You don't write one route per room. You write one route with a wildcard segment, and when someone
walks through door 204, the room finds out it's 204 by asking.

#### The code

**Declaring the parameter** — `App.jsx:63`:

```jsx
<Route path="/suppliers/:supplierId" element={/* ... */} />
```

**Reading it** — `src/features/supplier-profile/ui/SupplierProfile.jsx:18-21, 30-40`:

```jsx
export function SupplierProfile({ supplierId: propSupplierId = null, onBack = null, onShowToast = null, onOpenVerification = null }) {
  const params = useParams()
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const supplierId = propSupplierId || params.supplierId

  // ...

  useEffect(() => {
    if (!supplierId) return
    setLoading(true)
    supplierRepository.getById(supplierId).then((data) => {
      setSupplier(data)
      setLoading(false)
    }).catch(() => {
      setSupplier(null)
      setLoading(false)
    })
  }, [supplierId])
```

**Second example** — `VerificationTaskDetail.jsx:14, 20-38`:

```jsx
const { taskId } = useParams()

useEffect(() => {
  let cancelled = false
  async function loadTask() {
    setStatus('loading')
    setDecision(null)
    try {
      const result = await supplierRepository.getVerificationTask(taskId)
      if (cancelled) return
      setTask(result)
      setStatus(result ? 'ready' : 'missing')
    } catch {
      if (!cancelled) setStatus('error')
    }
  }
  loadTask()
  return () => { cancelled = true }
}, [taskId, retryToken])
```

#### Why we did it this way

**`supplierId` in the dependency array is the load-bearing detail.** React Router reuses the same
component instance when you navigate from `/suppliers/aravind-fasteners` to
`/suppliers/kalyani-textiles` — the route pattern didn't change, so there's no unmount and no
remount. Only the param changed. If the effect had `[]` as its dependency array, the page would keep
showing Aravind's data under Kalyani's URL. Listing `supplierId` is what makes the param change
trigger a refetch.

**The `propSupplierId || params.supplierId` fallback** makes the component usable in two contexts: as
a route (reads the URL) or embedded inside another screen with an explicit prop. Props win when
present, which is the right precedence — an explicit instruction should override an ambient one.

**Three outcomes, three renders.** `VerificationTaskDetail` models this properly with a `status`
string rather than two booleans: `'loading'` | `'ready'` | `'missing'` | `'error'`. `SupplierProfile`
does it with a `loading` flag plus a `null` check (`:42-64`), rendering a *"Supplier Record Not
Found"* state with a route back to search. Crucially, an unknown `:supplierId` does **not** hit the
404 route — the route matched fine, the *record* didn't exist. Route-not-found and record-not-found
are different failures and get different screens.

#### Viva question

> **Q: How do you read a URL parameter in React Router v6, and why must it be in the effect's dependency array?**
>
> **A:** You declare the segment with a colon — `path="/suppliers/:supplierId"` — and read it with
> `useParams()`. It must be in the dependency array because navigating between two suppliers reuses the
> same mounted component rather than remounting it, so without the dependency the effect never re-runs
> and you'd render the previous supplier's data.

---

### 7.4 Query parameters and `useSearchParams`

#### The analogy

The route is the street address; the query string is the note pinned to the door — *"filtered to
verified suppliers in textiles, sorted by lead time."* Same building, different instructions on
arrival. And because it's written on the door rather than remembered in your head, you can photograph
it and send it to someone else.

#### The code

**The API is deliberately shaped like `useState`** — `SearchScreen.jsx:7, 11-16`:

```jsx
const [searchParams, setSearchParams] = useSearchParams()

const query = searchParams.get('q') || ''
const band = searchParams.get('band') || ''
const region = searchParams.get('region') || 'All Regions'
const industry = searchParams.get('industry') || 'All Industries'
const sortBy = searchParams.get('sort') || 'relevance'
const isSelectToVerifyPrompt = searchParams.get('prompt') === 'select_to_verify'
```

**Writing back, with defaults stripped** — `SearchScreen.jsx:42-54`:

```jsx
function updateParams(next) {
  const updated = new URLSearchParams(searchParams)
  // Remove prompt parameter on user interaction
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

**Driving an input from the URL** — `SearchScreen.jsx:129-135`. The text field is a controlled
component whose source of truth is the query string:

```jsx
<input
  className="w-full pl-10 pr-4 py-3 bg-background border border-hairline rounded-lg ..."
  placeholder="Search by name, material, capability, or keyword..."
  type="text"
  value={query}
  onChange={(e) => updateParams({ q: e.target.value })}
/>
```

**A deep-linkable disclosure** — `SupplierProfile.jsx:28, 79-87`:

```jsx
const activeClaimKey = searchParams.get('claim')

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

**Reading a param to drive a guard** — `VerificationDashboard.jsx:7-9`:

```jsx
const [searchParams] = useSearchParams()
const navigate = useNavigate()
const supplierIdParam = searchParams.get('supplier')
```

#### Why we did it this way

This is invariant 11 from `docs/CLAUDE.md`, and it's described there as "the most frequently broken
rule in the list, because component state is always the easier path":

> **Anything shareable belongs in the URL.** Search queries, filters, sort, pagination, active tab,
> selected claim, comparison set. If a user might bookmark it, send it to a colleague, or reach it with
> the back button, it is URL state — not component state.

Four things you get for free by obeying it:

1. **Shareable.** `/search?q=fasteners&band=verified` in Slack reproduces your exact results.
2. **Bookmarkable.** Save a filtered view; it still works next week.
3. **Back button works correctly.** Each `setSearchParams` pushes a history entry, so Back steps
   through your filter history. Opening a claim then pressing Back *closes the claim* instead of
   leaving the page — which is exactly what users expect and almost never get from a disclosure widget.
4. **Reload-safe.** F5 on a filtered search keeps the filters.

The `updateParams` default-stripping is a small thing that matters. Without it, selecting "All
Regions" would append `?region=All%20Regions` — a URL that says nothing but looks like it says
something. Stripping defaults means the URL length is proportional to how much you've actually
narrowed.

`useSearchParams` returning a `[value, setter]` pair is a deliberate API design: it reads exactly like
`useState`, so URL state is a drop-in replacement for component state. That's what makes obeying
invariant 11 cheap enough that people actually do it.

> ⚠️ `SearchScreen`'s two chip filters — ISO 9001 and Lead Time < 14 days — are held in ordinary
> component state (`extraFilter`, `:17`) rather than the URL. They look shareable but aren't. A small
> inconsistency with invariant 11, and a fair thing to be asked about.

#### Viva question

> **Q: Why are Supify's search filters stored in the URL instead of component state?**
>
> **A:** Because filters are shareable, bookmarkable state — putting them in the query string means a
> URL fully describes a result set, so it survives reload, works with the back button, and can be sent
> to a colleague. `useSearchParams` has the same `[value, setter]` shape as `useState`, so it costs
> essentially nothing to do it the right way.

---

### 7.5 `useNavigate` — programmatic navigation

#### The analogy

`<Link>` is a signpost: the user reads it and decides to walk. `useNavigate` is picking someone up and
putting them somewhere — used when *code* makes the decision, not the user. Redirect after submit,
bounce after a failed guard, move on after a wizard step.

#### The code

**With scroll restoration** — `App.jsx:28-31`:

```jsx
const handleNavigate = (path) => {
  navigate(path)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
```

**As a guard redirect, with `replace`** — `VerificationDashboard.jsx:25-28`:

```jsx
if (!supplierIdParam) {
  onShowToast?.('Please select a supplier from Solutions first to verify.', 'info')
  navigate('/search?prompt=select_to_verify', { replace: true })
  return
}
```

**After a wizard completes** — `OnboardingScreen.jsx:46-58`:

```jsx
const handleNext = () => {
  if (currentStep < 4) {
    setCurrentStep(currentStep + 1)
    if (onShowToast) onShowToast(`Step ${currentStep} saved! Moving to Step ${currentStep + 1}.`)
  } else {
    if (onShowToast) onShowToast('Supplier profile submitted! Verification queue review ticket created.')
    if (onNavigate) {
      onNavigate('/search')
    } else {
      navigate('/search')
    }
  }
}
```

#### Why we did it this way

**`{ replace: true }` is the detail to understand.** Default navigation *pushes* onto the history
stack. For a guard redirect that creates a trap:

```
push:     /verification → /search        Back → /verification → guard fires → /search → ...
replace:  /verification ⇒ /search        Back → wherever the user actually came from
```

The user can never escape backwards from a pushed redirect, because going back re-triggers the
condition that redirected them. `replace` swaps the current entry instead of stacking a new one, so
the bounce leaves no trace.

**Why `scrollTo` is manual.** Browsers restore scroll position on history navigation, which is right
for Back and wrong for a fresh click. React Router v6 doesn't handle this for you (v6.4+'s data
routers offer `ScrollRestoration`, but this app uses the plain `BrowserRouter` setup). Without
`handleNavigate`, clicking a supplier at the bottom of the grid lands you halfway down their profile.

**The `onNavigate || navigate` fallback** in `OnboardingScreen` again lets the component work both as a
route and as an embedded child — parent's navigation wins when supplied, local `useNavigate` otherwise.

#### Viva question

> **Q: When would you use `useNavigate` instead of `<Link>`, and what does `replace: true` do?**
>
> **A:** Use `<Link>` when the user decides to navigate and `useNavigate` when code decides — after a
> form submits, or when a guard rejects access. `replace: true` swaps the current history entry instead
> of pushing a new one, which stops a redirect from trapping the user in a back-button loop.

---

### 7.6 `<Link>` vs `<button onClick>`

A short but frequently-examined distinction.

`src/app/NotFound.jsx:10` and `SupplierCard.jsx:113-119` use `<Link>`:

```jsx
<Link className="button" to="/search">Go to discovery</Link>
```

```jsx
<Link
  to={`/verification?supplier=${supplier.id}`}
  className="font-button text-[11px] font-bold text-brand-teal bg-brand-mint/20 ..."
>
  <span className="material-symbols-outlined text-xs">verified</span>
  Verify
</Link>
```

`Header.jsx:32-44` uses buttons calling `onNavigate`:

```jsx
{navItems.map((item) => (
  <button
    key={item.label}
    onClick={() => handleNav(item.path)}
    className={/* ... */}
  >
    {item.label}
  </button>
))}
```

**The rule:** `<Link>` renders a real `<a href>`, so it supports middle-click-to-new-tab, right-click
→ copy address, keyboard activation as a link, and crawlers. `<button onClick={navigate}>` supports
none of those.

**So why does the header use buttons?** Because `handleNav` (`Header.jsx:13-16`) does two things —
closes the mobile drawer *and* navigates — and delegates to `App`'s `handleNavigate`, which adds
smooth scroll-to-top. It's a pragmatic choice, but it's a genuine accessibility regression: those nav
items should be `<Link>`s with an `onClick` that closes the drawer, which is exactly the pattern
`SupplierCard.jsx:77-85` already uses elsewhere in the codebase. Good thing to volunteer when asked
what you'd improve.

---

### 7.7 Navigation guards and protected routes

Supify implements guarding **two different ways**, and knowing both — including which one actually
runs — is the strongest answer available on this topic.

#### Approach A — the wrapper component (written, not wired)

`src/app/ProtectedRoute.jsx:4-20` is the classic composition guard. It reads role from Context and
either returns `children` untouched or replaces them with an access-required screen:

```jsx
export function ProtectedRoute({ requiredRole, children }) {
  const session = useContext(UserRoleContext)

  if (session.role === requiredRole) return children

  return (
    <main className="page">
      <div className="empty-state">
        <span aria-hidden="true">⊘</span>
        <h2>{roleLabels[requiredRole]} access required</h2>
        <p>You are currently acting as {roleLabels[session.role]}. Switch your active role to open this console.</p>
        <button className="button" onClick={() => session.setRole(requiredRole)}>
          Continue as {roleLabels[requiredRole]}
        </button>
      </div>
    </main>
  )
}
```

It's designed to be used like this:

```jsx
// PROPOSED — this wiring does not exist in App.jsx.
<Route
  path="/verifier/queue"
  element={
    <ProtectedRoute requiredRole="verifier">
      <VerificationQueue />
    </ProtectedRoute>
  }
/>
```

Two things to notice. It **fails informatively** — it tells you what role you currently hold and
offers a one-click switch, rather than silently bouncing you somewhere. And it guards by
*substitution*: the protected component never renders, so its effects never run and it never fetches
data the user isn't entitled to.

> ⚠️ `ProtectedRoute` is imported by **no file**. No route in `App.jsx` wraps anything in it. It is
> correct, complete, and dead.

#### Approach B — the effect-based redirect (live, and the one that runs)

`src/features/verification-dashboard/ui/VerificationDashboard.jsx:24-49` guards on *data
preconditions* rather than identity:

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

And the receiving end, `SearchScreen.jsx:16, 66-88` — the redirect carries a flag that becomes an
explanatory banner:

```jsx
const isSelectToVerifyPrompt = searchParams.get('prompt') === 'select_to_verify'

// ...

{isSelectToVerifyPrompt && (
  <div className="bg-brand-mint/25 border-2 border-brand-teal/30 rounded-2xl p-4 md:p-5 flex items-center justify-between gap-4 shadow-sm animate-fadeIn">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-xl bg-brand-teal text-on-primary flex items-center justify-center flex-shrink-0 shadow-sm">
        <span className="material-symbols-outlined text-xl" data-fill="true">verified</span>
      </div>
      <div>
        <h3 className="font-title-md text-sm md:text-base font-bold text-primary">
          Select a Supplier to Run Verification
        </h3>
        <p className="text-xs text-on-surface-variant">
          Browse our verified partner solutions below and click <strong className="text-brand-teal font-bold">"Verify"</strong> on any card to view their live audit run.
        </p>
      </div>
    </div>
    <button onClick={() => updateParams({})} className="text-primary hover:bg-black/5 p-1.5 rounded-lg transition-colors">
      <span className="material-symbols-outlined text-sm">close</span>
    </button>
  </div>
)}
```

#### Why we did it this way

**Three branches, all handled.** No supplier selected → bounce with an instruction. Supplier selected
but absent from the registry → different message, different destination. Fetch threw → bounce
silently, having already reset the loading flag. Nothing leaves the user on a blank screen.

**The handoff through the URL is the clever bit.** The guard could have just called `navigate('/search')`
and left the user wondering why they moved. Instead it appends `?prompt=select_to_verify`, which
`SearchScreen` translates into a banner that explains what happened and what to do next. Two
components that never import each other, coordinating through the URL — which is the same mechanism
the filters use, applied to a different problem.

**And the banner self-destructs.** `updateParams` deletes `prompt` on *any* filter interaction
(`SearchScreen.jsx:45`), so the instruction vanishes the moment the user starts working. It's present
exactly as long as it's useful.

**Trade-off worth stating:** an effect-based guard runs *after* the first render, so there's a frame
where the protected component mounts before redirecting. Here that's invisible because the loading
state renders first (`:72-81`). A wrapper guard like `ProtectedRoute` prevents the mount entirely,
which is strictly better for anything genuinely sensitive. Approach A is the better tool for identity;
Approach B is fine for "you haven't picked a supplier yet."

#### Viva question

> **Q: How does Supify stop a user reaching `/verification` without choosing a supplier?**
>
> **A:** `VerificationDashboard` runs an effect on mount that checks for the `?supplier=` query
> parameter, and if it's missing it shows a toast and calls
> `navigate('/search?prompt=select_to_verify', { replace: true })`. `SearchScreen` reads that `prompt`
> flag and renders an explanatory banner, so the redirect arrives with a reason attached rather than
> dumping the user somewhere unexplained.

---

### 7.8 404 catch-all routing

#### The analogy

The last line of a switchboard script: *"if the caller asked for nobody who works here, don't hang up
— tell them, and offer the directory."*

#### The code

**The route** — `App.jsx:121`, the final entry in `<Routes>`:

```jsx
<Route path="*" element={<NotFound />} />
```

**The screen** — `src/app/NotFound.jsx`, in full:

```jsx
import { Link } from 'react-router-dom'

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

#### Why we did it this way

**`path="*"` is a wildcard that matches any path,** and in v6 it is ranked lowest by the matching
algorithm, so it only wins when no other route matched. Putting it last in the source is convention
for readability — unlike v5's `<Switch>`, where first-match-wins made source order mechanically
load-bearing.

**Without it, an unmatched route renders nothing at all.** Not an error — just the header and empty
space below it, which looks like a broken app rather than a wrong address. The catch-all converts
silence into a designed state, which is invariant 4 again: *never render an unknown state as neutral*.

**Note what it offers.** Not "go home" — `/search`, the place a lost buyer most likely wanted. A 404
should route people forward, not just acknowledge the mistake.

**Route-level 404 vs record-level not-found.** These are different and this codebase handles them
separately:

| Situation | Route matched? | What renders |
| --- | --- | --- |
| `/nonsense` | No | `NotFound` via `path="*"` |
| `/suppliers/does-not-exist` | **Yes** | "Supplier Record Not Found" inside `SupplierProfile.jsx:53-64` |
| `/verifier/task/VT-9999` | **Yes** | `status === 'missing'` branch, `VerificationTaskDetail.jsx:57-68` |

The route pattern `/suppliers/:supplierId` matches *any* value in that segment, so the router is
perfectly happy. It's the repository that returns `null`. Conflating the two would give the user a
"page not found" for a page that very much exists.

> ⚠️ `NotFound` is styled with `.page`, `.empty-state` and `.button` — none of which are defined in
> `styles.css` or generated by Tailwind. The 404 renders as unstyled HTML. The routing is correct;
> the CSS was lost in the redesign.

#### Viva question

> **Q: How do you implement a 404 route in React Router v6, and why isn't `/suppliers/bad-id` a 404?**
>
> **A:** You add `<Route path="*" element={<NotFound />} />`, which v6 ranks lowest so it matches only
> when nothing else does. `/suppliers/bad-id` isn't a 404 because the route pattern matched perfectly —
> the *record* is missing, not the page, so `SupplierProfile` renders its own "record not found" state
> with a route back to search.

---

## 8. Teacher viva cheat sheet

Ten high-frequency questions with answers short enough to actually say out loud.

---

**1. What is the Virtual DOM and why does React use it?**

An in-memory JavaScript object tree representing the intended UI; on each update React builds a new
tree, diffs it against the previous one, and applies only the minimal real DOM changes. It's used
because comparing JavaScript objects is cheap while DOM writes can force layout recalculation and
repaint.

---

**2. Difference between props and state?**

Props are passed in from a parent and are read-only inside the component; state is owned by the
component and changing it through its setter triggers a re-render. If the component needs to remember
a value and change it itself, it's state — otherwise it's a prop.

---

**3. Why does React need keys in lists, and why is the index a bad key?**

Keys are how React matches elements between renders, so it can move existing DOM nodes instead of
rebuilding them and preserve any state attached to them. An index describes position rather than
identity, so inserting or reordering shifts every subsequent key onto a different item and React
patches the wrong nodes — Supify uses `key={supplier.id}` because it survives the sort dropdown
reordering the whole list.

---

**4. Explain `useEffect`'s dependency array and how infinite loops happen.**

The array lists the values the effect depends on, so it re-runs only when one of them changes;
omitting the array entirely means "after every render." The loop happens when an effect with no
dependency array calls `setState`, because that re-render retriggers the effect — `SearchScreen`
avoids it by listing its six filter values, none of which the effect itself modifies.

---

**5. `useMemo` vs `useCallback`?**

`useMemo` caches the *result* of calling a function; `useCallback` caches the *function itself*, and
`useCallback(fn, deps)` is literally equivalent to `useMemo(() => fn, deps)`. In `ComparisonScreen`,
`useMemo` stabilises the `selectedIds` Set and `useCallback` stabilises the `toggleId` handler passed
to every row.

---

**6. What is lifting state up, with an example from this project?**

Moving shared state to the lowest common ancestor of every component that needs it, so there's one
source of truth. The toast lives in `App.jsx` because four separate features trigger it and it renders
in one fixed position — if each owned its own, two could render at once with no way to coordinate.

---

**7. What is the `children` prop and why is it better than more props?**

`children` is whatever JSX the caller nests inside a component's tags, letting the component be a
generic container that knows nothing about its contents. `Modal` owns the backdrop, header and scroll
behaviour and never needs modification, whereas a `Modal` taking `formFields` and `submitLabel` props
would need a new prop for every screen that ever used it.

---

**8. What changed from React Router v5 to v6?**

v5 used `component={X}` or a render prop and matched the first match in source order inside
`<Switch>`; v6 uses `element={<X />}`, which lets you pass props inline, and `<Routes>` selects the
best match by specificity rather than by order. That's why `path="*"` in `App.jsx` reliably acts as a
catch-all.

---

**9. How do you read a route param versus a query param?**

Route params come from a `:name` segment in the path and are read with `useParams()` — Supify uses it
for `/suppliers/:supplierId`. Query params come from the string after `?` and are read with
`useSearchParams()`, which returns a `[value, setter]` pair like `useState` — used for
`/verification?supplier=id` and every search filter.

---

**10. Why do Supify's filters live in the URL instead of component state?**

Because filters are shareable state: putting them in the query string means the URL fully describes a
result set, so it survives reload, works with the back button, and can be pasted to a colleague. The
project treats this as a hard rule — anything a user might bookmark or send belongs in the URL, not in
`useState`.

---

### Bonus: the three questions that catch people out

**"Show me somewhere your own code breaks a rule you just stated."**
`ClaimRow.jsx:112` keys evidence items by array index. It's safe today because that list is static and
never reordered, but it would break the moment evidence can be added or sorted — `item.label` would be
the correct key.

**"Your `SearchScreen` effect has no cleanup. What's the consequence?"**
Filters change on every keystroke and the repository has 200 ms of simulated latency, so requests
overlap and the *last to resolve* wins rather than the last requested — a classic race condition.
`ComparisonScreen.jsx:21-36` shows the fix: a `cancelled` flag set by the effect's cleanup function,
checked before every `setState`.

**"You said `useCallback` is an optimisation. Is it optimising anything here?"**
Not currently — `SupplierPick` isn't wrapped in `React.memo`, so it re-renders regardless of whether
`toggleId`'s reference is stable. It's the correct shape for when that memoisation is added, and until
then it costs a dependency comparison per render.

---

## 9. Rough edges — the "what would you fix" answer

Every one of these is verified against the code. Having a ranked list ready is worth more than any
amount of praise for what works.

| # | Issue | Location | Fix |
| --- | --- | --- | --- |
| 1 | No request cancellation → race condition | `SearchScreen.jsx:19-40` | Add the `cancelled` flag pattern from `ComparisonScreen.jsx:21-36` |
| 2 | Toast timer never cleared; second toast cut short | `App.jsx:21-26` | `useRef` for the timeout id + `clearTimeout` before each new one |
| 3 | Trust score computed client-side | `SupplierCard.jsx:25-27`, `VerificationDashboard.jsx:84-86` | Violates invariant 2 — `overall_score` must come from the server |
| 4 | Evidence list keyed by index | `ClaimRow.jsx:112` | Key on `item.label` |
| 5 | Modals don't trap focus or close on Escape | `Modal.jsx`, both inline modals | `useRef` + a focus-trap effect + an Escape key handler |
| 6 | `ProtectedRoute` written but never imported | `app/ProtectedRoute.jsx` | Wire it into the verifier routes, or delete it |
| 7 | Same fetch logic duplicated four times | Four screens | Extract `useAsyncData` (see §5.6) |
| 8 | `onShowToast` missing from effect deps | `VerificationDashboard.jsx:49` | Add it, or wrap `showToast` in `useCallback` upstream |
| 9 | Header nav uses `<button>` instead of `<Link>` | `Header.jsx:32-44` | Loses middle-click and copy-link-address |
| 10 | Chip filters in state, not URL | `SearchScreen.jsx:17` | Inconsistent with invariant 11 — move to the query string |
| 11 | Loading state doesn't match final layout | `SearchScreen.jsx:276-280` | Render skeleton cards in the grid to stop layout shift |
| 12 | Dead internal links | `VerificationTaskDetail.jsx:64,75`, `VerificationQueue.jsx:87` | `/verify/queue` and `/verify/tasks/:id` match no route |

The first three are the ones to lead with. Number 1 is a real user-visible bug under realistic
conditions, number 2 is reproducible in about ten seconds, and number 3 is a documented invariant
violation you can name by number.

---

*For the business problem, trust model, workflows and design system behind all of this, see
`SUPIFY_PROJECT_GUIDE.md`.*
