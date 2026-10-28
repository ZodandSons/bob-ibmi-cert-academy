# Section 5 · Bob accounts (≈8% of the exam)

[Exam home](README.md) · [← Section 4](section-4-configuration.md) · Next: [Section 6 Security →](section-6-security.md)

Objectives: **5.1** administer Bobalytics · **5.2** authenticate with API keys ·
**5.3** Enterprise plan features · **5.4** Bobcoins · **5.5** token usage for prompting

---

## 5.1 Administer Bobalytics
- **Access:** bob.ibm.com → **Admin** → **Bobalytics** (Enterprise plan).
- **Views:** the exam guide names **Today** and **Patterns** tabs for activity and trends. The
  current docs list **Metrics, Insights, Today** and **My board**, with a time-range selector,
  a **Teams** dropdown and **Scope** tabs (Organization / Team / User). **Export** downloads CSVs.
- **Key metrics:**
  - **Adoption rate:** average daily active users ÷ licensed seats (active = accepted a
    completion or completed a chat that day).
  - **Bob factor:** % of committed lines of code created by Bob.
  - **Bobcoin spend:** Bobcoins consumed in the period, also as % of budget.
- **Admin visibility limits:** team-level insights **without individual user data**. Users
  are anonymized ("User 1") in team charts. **Admins cannot see a specific user's data** from
  team-level charts. In the user view, each person sees only their own data.

## 5.2 Authenticate with API keys
- API keys authenticate apps and automation **without browser sign-in**: **Bob Shell
  non-interactive runs**, **CI/CD pipelines**, **scheduled jobs**, scripted workflows.
- **Types:**
  | | **General** | **Inference** |
  |---|---|---|
  | Scope | Subscription instance, usable across services | One instance **and team**, inference only |
  | Extra info needed | **Team ID** (Bob Shell: `--team-id <id>`) | None |
  | Typical use | Broader integrations | Bob Shell / CI running prompts |
- **Ownership:** users create, list and revoke their own keys. **Instance admins** can list and
  revoke keys for any user in their instance.
- **The key value is shown only once at creation.** Store it in a secrets manager / CI secret
  (`BOB_API_KEY`), never in code, prompts or chat. Revoke when exposed or unused.
- **In this repo:** [`skills/bob-shell-automation/examples/github-actions.yml`](../../skills/bob-shell-automation/examples/github-actions.yml)
  reads `BOB_API_KEY` from a repository secret. `ci-review.sh` and `batch-convert.sh` refuse to run without it.

## 5.3 Enterprise plan features
- **Team management** with flexible roles; admins invite and manage members by IBMid.
- **Shared Bobcoin allocation:** distribute Bobcoins across individuals and teams; shared
  pools; **spending limits** per team and per member; entitlement and balance tracking.
- **Bobalytics** for adoption, delivery contribution (Bob factor) and Bobcoin consumption.
- **Centralized user and spending management:** seats, limits, organization-wide monitoring.
- **Enterprise authentication:** **SSO with SAML or OIDC** identity providers.
- Also: on-premises / air-gapped deployment options and priority support.

## 5.4 Bobcoins
- **Consumption-based unit** for everything Bob does.
- **Plan allocations (monthly, Oct 2026 pricing page):**
  | Plan | Price | Bobcoins |
  |---|---|---|
  | Free trial (30 days) | free | 50 |
  | Pro | $20/month | 50 |
  | Pro+ | $60/month | 180 |
  | Ultra | $200/month | 1,000 |
  | Enterprise | contact sales | packs |
  Allocations reset each billing cycle. *(Prices change; the concept is what's tested.)*
- **Overage:** individuals pay **$0.50 per Bobcoin**; once enabled it can't be turned off until
  month end.
- **Enterprise packs:** **1,000 Bobcoins for $500** (expire after one year) give supplemental
  capacity from a shared pool. Overage packs cost 10% more.
- **Bobcoins vs tokens:** tokens are what models consume (input + output); Bobcoins combine
  token usage across models and operations into **one predictable cost metric**.

## 5.5 Token usage for prompting
- **Input tokens:** your prompt + **the whole active context** (system prompt, tool
  definitions, MCP tools, rules, skills, messages). **Output tokens:** Bob's response.
- **Consumption factors:** prompt length, conversation context, generated responses.
- **Why later prompts cost more:** the **full active context is processed again with every
  prompt**, so a short question late in a long task uses many more tokens than early on.
- **Token limits** affect context retention (condensation is lossy), response generation
  (space reserved for replies) and cost.
- **Optimize:** concise prompts, only relevant context (`@file:10-20` not whole folders),
  new task per goal, lean rules/MCP. See [4.2](section-4-configuration.md#42-utilize-context-window-management).

---

## Check yourself
<details><summary>1. Which API key type needs a team ID with Bob Shell?</summary>General (<code>--team-id</code>). Inference keys are already scoped to one team.</details>
<details><summary>2. Can an admin open a specific engineer's usage from a team chart in Bobalytics?</summary>No. Team charts are anonymized; individuals see their own data.</details>
<details><summary>3. What does "Bob factor" measure?</summary>The share of committed lines of code created by Bob.</details>
<details><summary>4. Same short question at message 3 vs message 60 of a task: why does the second cost more?</summary>The full active context (now much larger Messages) is re-sent and processed with every prompt.</details>
<details><summary>5. Which Enterprise feature lets you sign in through your company identity provider?</summary>SSO via SAML or OIDC.</details>

**Docs:** [Bobalytics](https://bob.ibm.com/docs/ide/features/bobalytics) ·
[API keys](https://bob.ibm.com/docs/ide/account/api-keys) ·
[Bobcoins](https://bob.ibm.com/docs/ide/account/bobcoins) ·
[Pricing](https://bob.ibm.com/pricing) ·
[Context window management](https://bob.ibm.com/docs/shell/core-concepts/context-window-management)
