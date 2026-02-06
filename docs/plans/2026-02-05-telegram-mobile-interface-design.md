# GTM Context OS -- Telegram Mobile Interface

**Date:** 2026-02-05
**Status:** Design approved

## Problem

Access to the GTM Context OS is currently limited to the desktop -- Claude Code in a terminal. When on the go (trade shows, meetups, between meetings), there's no way to query the knowledge base or capture new information. Insights get lost or delayed until back at a desk.

## Solution

A Telegram bot backed by a Python server on Railway that provides two-way mobile access to the GTM Context OS. Query the knowledge base, capture new contacts and insights, and get call prep briefings -- all from your phone.

## Architecture

```
┌──────────┐     ┌──────────────┐     ┌─────────────┐     ┌────────────┐
│ You on   │────>│  Telegram    │────>│  Bot Server │────>│ Claude API │
│ Phone    │<────│  API         │<────│  (Railway)  │<────│ (Sonnet)   │
└──────────┘     └──────────────┘     └──────┬──────┘     └────────────┘
                                             │
                                     ┌───────┴───────┐
                                     │               │
                              ┌──────▼──────┐ ┌──────▼──────┐
                              │  GTM Context │ │  Clarify    │
                              │  OS (Git)    │ │  REST API   │
                              └──────┬──────┘ └─────────────┘
                                     │
                              ┌──────▼──────┐
                              │  GitHub      │
                              │  Private Repo│
                              └──────┬──────┘
                                     │
                              ┌──────▼──────┐
                              │  Your Mac    │
                              │  (git pull)  │
                              │  + Obsidian  │
                              └─────────────┘
```

### Data Flow

1. You send a message on Telegram from your phone
2. Telegram delivers it to the bot server on Railway via webhook
3. The bot reads relevant files from its local clone of the GTM Context OS
4. It sends those files + your message to Claude Sonnet
5. Claude responds (answer, structured data, or briefing)
6. If files were changed, the bot commits and pushes to GitHub
7. If contact info was captured, the bot creates/updates records in Clarify via REST API
8. Response goes back to you on Telegram
9. When you're at your desk, Obsidian Git plugin auto-pulls the latest changes

## Interaction Modes

### 1. Query Mode (default -- just send a message)

Natural language questions against the knowledge base:

- "What do we know about WSO2?"
- "What's our pricing objection response?"
- "Show me all active accounts"
- "What ICPs have we validated?"

The bot finds relevant files, sends them to Sonnet with the question, and returns the answer.

### 2. Capture Mode (`/capture`)

Add new information on the go:

```
/capture Met Jake Liu from Acme Corp, jake@acme.io,
512-555-1234, interested in Clay workflows
```

Sonnet extracts structured data and:
- Creates or updates account files in the GTM Context OS
- Links to relevant ICPs, services, and objections
- Creates/updates contact and company records in Clarify
- Confirms what it did via Telegram reply

Ideal for trade shows, meetups, and post-meeting notes.

### 3. Prep Mode (`/prep`)

Quick call briefing:

```
/prep WSO2
/prep Mercury Fund
```

Pulls the account file, related ICPs, relevant objections, and recent activity. Returns a concise briefing you can skim before walking into a meeting.

## Tech Stack

| Component | Technology |
|---|---|
| Messaging platform | Telegram (via python-telegram-bot) |
| Bot server | Python on Railway |
| LLM | Claude Sonnet (Anthropic API) |
| Knowledge base storage | GitHub private repo |
| CRM integration | Clarify REST API (OAuth 2.0) |
| Local sync | Obsidian Git plugin (auto-pull) |

## Bot Server Internals

Four main components (~300-400 lines of Python):

1. **Telegram handler** -- Receives messages, routes based on whether it's a plain query, `/capture`, or `/prep`
2. **Knowledge base reader** -- Reads GTM Context OS files from local git clone. Determines which files are relevant to the query (account files, knowledge base nodes, synthesis docs)
3. **Claude Sonnet layer** -- Sends message + relevant context to Sonnet. Returns answer, structured data, or briefing
4. **Writer layer** -- For captures: writes new/updated markdown files, commits and pushes to GitHub. Calls Clarify REST API when contact info is detected

## Costs

| Component | Monthly Cost |
|---|---|
| Railway hosting (Hobby plan) | $5 |
| Claude Sonnet API usage | $5-15 (est.) |
| Telegram | Free |
| **Total new cost** | **~$10-20/mo** |

Added to existing $120/mo (Claude Max $100 + Clarify $20).

## Prerequisites

Before implementation:

- [ ] Anthropic API key (console.anthropic.com -- separate from Max subscription)
- [ ] Telegram bot token (via @BotFather)
- [ ] Railway account (Hobby plan, $5/mo)
- [ ] GTM Context OS pushed to private GitHub repo
- [ ] Clarify OAuth credentials (for REST API access)
- [ ] Obsidian Git plugin installed and configured

## Sync Strategy

**Cloud to GitHub:** Bot commits and pushes after every capture/write operation.

**GitHub to Mac:** Obsidian Git plugin auto-pulls every few minutes. Changes appear in Obsidian automatically.

**Mac to GitHub:** When working locally with Claude Code, changes can be committed and pushed. Obsidian Git plugin can also auto-commit and push.

**Bot stays current:** Bot pulls from GitHub before processing each message to ensure it has the latest knowledge base state.

## Future Considerations (not in v1)

- Voice messages -- Telegram supports voice, could transcribe and process
- Image capture -- Photos of whiteboards or business cards
- Multi-user -- Share the bot with team members
- Scheduled briefings -- Auto-send prep before calendar events
