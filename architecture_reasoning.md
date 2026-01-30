The Pilot Analogy: You are the Pilot; AI is the Co-pilot. The Co-pilot can fly the plane, but
if it flies into a mountain, the Pilot is the one who gets blamed.

Prompting Hierarchy:
Role: "Act as a Senior Python Engineer...", "We are building an SEC compliant app" (Sets the standard).
Context: "I have a CSV file with messy dates..." (The problem).
Constraint: "Do not use pandas, use standard library only...", "Do not use expensive setups, I'm on a tight budgetssss" (The boundary).
Output: "Give me the code and a test case.", "Give me production grade and secure code" (The deliverable).


Instructor's Prompt: This is not for beaverly but for training purposes so we are building a production-grade app in the training.

I want to build an auth app for securing online financial transactions in mobile apps.
I am just a regular Nigerian with little capital but thinking big; like 1 million users in the future.
I don't have money for paid servers or paid deployments.
This app must have a very secure design. Easier to maintain.
Show architecture and how to start. I use VS code and Github and copilot already.
You are my co-CTO




ChatGPT's first response:
Alright. I’ll speak to you as **co-CTO**, not motivational speaker.

You’re doing the *right* thing by treating this as **production-grade training**, not a toy. That mindset is already senior.

Your constraints are clear:

* 🇳🇬 Nigerian, little capital
* 💸 **$0 paid infra**
* 📱 Mobile apps (financial transactions)
* 🔐 **Very secure auth**
* 🧠 Easy to maintain
* 🚀 Future scale: **1M+ users**
* 🛠 VS Code, GitHub, Copilot

We will design something that:

* works **free today**
* does **not collapse** when money/users come
* teaches **real system design**, not tutorials

---

## 1. First: What EXACTLY are we building?

You are **not** building “another auth app”.

You are building:

> **An Authentication & Transaction Authorization Service**
> (think: “Cloudflare Access + Auth0 + Google Authenticator — but simpler”)

This service will:

* Authenticate users (who are you?)
* Authorize sensitive actions (are you allowed to do this *now*?)
* Secure financial actions (step-up verification)

### Core use cases

* Login to mobile app
* Confirm payment / transfer
* Protect account takeover
* Work even if client app is compromised

---

## 2. Core Design Principles (NON-NEGOTIABLE)

If you miss these, security breaks.

### 🔒 Principle 1: **Server is the source of truth**

* Mobile apps are **untrusted**
* Never trust:

  * device time
  * device storage
  * client-side validation

### 🔑 Principle 2: **No long-lived secrets on the client**

* No API keys
* No permanent tokens
* Short-lived access tokens only

### 🧱 Principle 3: **Stateless auth where possible**

* Makes scaling cheap
* Makes infra simple
* Makes attacks harder

### 🔄 Principle 4: **Step-up auth for money**

* Login ≠ authorize payment
* Every financial action must be re-verified

---

## 3. High-Level Architecture (Free-Friendly)

```
[MOBILE APP]
    |
    | HTTPS (TLS)
    v
[AUTH API]  -----> [JWT SIGNING]
    |
    | validates
    v
[AUTH LOGIC]
    |
    | checks
    v
[EVENT STORE / DB]
```

Let’s break it down properly 👇

---

## 4. Technology Stack (ZERO PAID)

### Backend

* **Node.js + TypeScript**
* **Fastify** (faster & safer than Express)
* **JWT (RS256, not HS256)**

Why?

* Type safety
* Widely supported
* Copilot-friendly

---

### Database (Free tier)

Option A (recommended):

* **Supabase (Postgres)** – generous free tier

  * Auth NOT used (we build our own)
  * Just DB + Row Level Security

Option B:

* **SQLite + GitHub Codespaces** (for early dev only)

---

### Hosting (Free)

Pick one:

* **Fly.io** (best long-term)
* **Railway free tier**
* **Render free**

We’ll design **stateless**, so migration later is easy.

---

### Secrets & Config

* `.env` locally
* GitHub Secrets for CI
* No secrets in repo. Ever.

---

## 5. Core Auth Flow (IMPORTANT)

### 🔐 Login Flow

```
1. User enters email + password
2. Password hashed (bcrypt / argon2)
3. Server issues:
   - Access Token (5–10 min)
   - Refresh Token (rotating)
4. Tokens signed with PRIVATE KEY
```

**Access Token (JWT)**

```json
{
  "sub": "user_id",
  "scope": ["basic"],
  "iat": 123456,
  "exp": 123999
}
```

---

### 🔁 Refresh Flow (Rotating Tokens)

* Refresh token stored **server-side**
* Each refresh:

  * old token invalidated
  * new one issued

This kills replay attacks.

---

## 6. Financial Transaction Authorization (THIS IS THE GOLD)

Login alone is **NOT ENOUGH**.

### Step-Up Authorization Flow

```
User clicks "Send ₦50,000"

1. App requests "transaction challenge"
2. Server creates challenge:
   - one-time
   - short-lived
3. User confirms via:
   - PIN / biometrics / OTP
4. Server validates challenge
5. Server issues "transaction token"
6. Transaction executed
```

### Transaction Token

* Valid for **one action only**
* Expires in seconds
* Bound to:

  * user
  * amount
  * destination

If attacker steals it → useless.

---

## 7. Database Schema (Simple but Strong)

### users

```
id (uuid)
email
password_hash
created_at
```

### refresh_tokens

```
id
user_id
token_hash
expires_at
revoked
```

### auth_challenges

```
id
user_id
type (login, transaction)
expires_at
used
metadata (json)
```

### audit_logs

```
id
user_id
action
ip
device
timestamp
```

Audit logs are **non-optional** in finance.

---

## 8. Repo Structure (Clean & Maintainable)

```
auth-service/
├── src/
│   ├── modules/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── tokens/
│   │   └── transactions/
│   ├── lib/
│   │   ├── crypto.ts
│   │   ├── jwt.ts
│   │   └── config.ts
│   ├── app.ts
│   └── server.ts
├── tests/
├── .env.example
├── Dockerfile
└── README.md
```

This is **senior-level structure**.

---

## 9. Security Hard Rules (Tattoo These)

* ❌ Never log tokens
* ❌ Never store plaintext passwords
* ❌ Never trust client input
* ✅ Rate-limit everything
* ✅ Use HTTPS only
* ✅ Use asymmetric JWT keys
* ✅ Hash refresh tokens in DB

---

## 10. How You START (Week 1 Plan)

### Day 1–2

* Init repo
* Setup Fastify + TS
* Health endpoint

### Day 3

* User registration
* Password hashing

### Day 4

* JWT issuing (access + refresh)

### Day 5

* Refresh rotation
* Token revocation

### Day 6

* Auth challenge system

### Day 7

* Audit logs
* Threat review

---

## 11. Reality Check (Very Important)

> You are **not slow** because you don’t type syntax.

You are **faster** because:

* You think in **systems**
* Copilot handles syntax
* You focus on **architecture**

Most “manual coders” cannot design this cleanly.

---

## 12. My Role as Co-CTO

I will:

* Stop you from over-engineering
* Stop you from security mistakes
* Help you design for **scale without money**
* Think like an attacker with you

If you want, next we can:

1. Write the **exact threat model**
2. Scaffold the repo
3. Design the **transaction challenge protocol**
4. Add **biometrics safely**
5. Prep it for **1M users without rewrite**

Say the word.
