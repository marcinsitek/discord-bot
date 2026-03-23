# Raport korzystania z AI

Jedynym wykorzystywanym narzędziem opartym o AI w trakcie prac nad projektem był ChatGPT.


Prompt:
```
I am working on a project in python. The main functionalities are the following: 1) retrieve messages from a Discord server using the python library called discord.py, only messages which mention the bot i.e. messages with @ followed by the name of the bot which is uksw_bot, 2) pass the content of the message to an LLM and get an output, 3) send the output of the LLM back to the channel that the bot is connected to, 4) save both the message from the channel and the output of the LLM to postgresql along with the name of the user which sent the message and the timestamp of the message, 5) display the data from the database in a tabular form in a dashboard using streamlit. The structure of the catalogs is: bot/, dashboard/, db/. Is this the best structure?.
```


Odpowiedź:
```
Your current structure is a solid starting point, but it will get messy as the project grows. Right now it’s organized by top-level features, but not by responsibilities or layers, which is what you’ll want long-term.

Let’s walk through it briefly.

🔎 Your current structure
bot/
dashboard/
db/
👍 What’s good

Clear separation between bot and dashboard

Database logic is at least isolated

Easy to understand initially

👎 What will become painful

db/ becomes a dumping ground (models, queries, migrations, config, etc.)

No separation between:

Discord handling

LLM logic

business logic

Harder to test and extend (e.g., adding another interface besides Discord)

✅ Verdict

👉 Your structure is fine for a prototype, but
👉 not ideal for a real project or something you’ll maintain
```

Prompt:
```
How to add a bot to a discord server?
```

Odpowiedź:
```
Adding a bot to a Discord server involves creating the bot in the developer portal and then inviting it with the correct permissions. Here’s a clean step-by-step guide:

🧩 Step 1: Create the bot application

Go to the Discord Developer Portal
👉 https://discord.com/developers/applications

Click “New Application”

Give it a name (e.g., uksw_bot)

Go to “Bot” tab (left sidebar)

Click “Add Bot”

🔑 Step 2: Get the bot token

In the Bot tab:

Click “Reset Token” (or copy existing one)

Save it securely (you’ll use it in your Python code)

⚠️ Never share this token publicly.

🔐 Step 3: Set bot permissions

Still in the Bot tab:

Enable:

MESSAGE CONTENT INTENT (important for reading messages)

Optionally enable:

Server Members Intent (if needed)

🔗 Step 4: Generate invite link

Go to OAuth2 → URL Generator

Select:

✅ bot

Under Bot Permissions, choose:

Send Messages

Read Messages/View Channels

Read Message History

(optional) Mention Everyone

Copy the generated URL

➕ Step 5: Invite bot to your server

Open the generated link in your browser

Select your server

Click Authorize

⚠️ You must:

Be the server owner OR

Have “Manage Server” permission
```

Prompt:
```
How to add torch to requirements.txt file with project dependencies without GPU support?
```

Odpowiedź:
```
To add CPU-only PyTorch to your requirements.txt, you need to be careful—because PyTorch distributes CPU and GPU builds differently than most packages.

✅ The correct way (CPU-only)
Option 1 — Simple (recommended for most cases)

Just add:

torch

👉 By default, pip install torch installs the CPU version unless you explicitly point to CUDA builds.

⚠️ Important nuance

PyTorch hosts some wheels on a separate index. If you want full control and reproducibility, use:

--index-url https://download.pytorch.org/whl/cpu
torch

This guarantees:

No CUDA dependencies

Smaller install

Works on machines without GPU

🧩 If you also use torchvision / torchaudio

Then do:

--index-url https://download.pytorch.org/whl/cpu
torch
torchvision
torchaudio
🔒 Version pinning (better for projects)

For stability, pin versions:

--index-url https://download.pytorch.org/whl/cpu
torch==2.2.2
torchvision==0.17.2
torchaudio==2.2.2

(Adjust versions as needed.)

🚀 Alternative: pip install command → requirements.txt

If you installed PyTorch like this:

pip install torch --index-url https://download.pytorch.org/whl/cpu

Then running:

pip freeze > requirements.txt

will produce something like:

torch==2.x.x

⚠️ But it may not include the index URL, so you might still want to add it manually.

❗ Common mistakes
❌ This installs GPU version (avoid unless needed)
torch==2.x.x+cu118
❌ Mixing default PyPI with CUDA builds

Leads to broken installs on CPU machines

✅ Final recommendation for your project

Use:

--index-url https://download.pytorch.org/whl/cpu
torch

✔ Clean
✔ Reproducible
✔ Works on any machine (including deployment servers)
```

Prompt:
```
What is the differnece between --index-url https://download.pytorch.org/whl/cpu and --extra-index-url https://download.pytorch.org/whl/cpu?
```

Odpowiedź:
```
Good question—this difference is subtle but very important, especially for reproducibility.

🧠 Core idea

Both options tell pip where to look for packages, but they behave differently:

Option	Meaning
--index-url	Primary (and only) package index
--extra-index-url	Additional fallback index
🔍 1. --index-url
--index-url https://download.pytorch.org/whl/cpu

👉 This replaces PyPI entirely.

pip will ONLY search this index

It will NOT look at the default PyPI (https://pypi.org/simple)

If a package isn’t there → installation fails

✅ Use when:

You want strict control

You are installing only packages available in that index

You want to guarantee CPU-only PyTorch

❌ Problem:

PyTorch index does not contain most packages (e.g. streamlit, discord.py)

So this would break:

--index-url https://download.pytorch.org/whl/cpu
torch
streamlit   ❌ may fail
🔍 2. --extra-index-url
--extra-index-url https://download.pytorch.org/whl/cpu

👉 This keeps PyPI as default, and adds PyTorch as a secondary source.

pip searches:

PyPI (default)

Then PyTorch index (if needed)

✅ Use when:

You have a normal project (like yours)

You want PyTorch CPU wheels

You still need regular packages

⚠️ Important subtlety (this trips people up)

Even with --extra-index-url, PyPI is searched first.

So:

If PyPI has a matching torch version → it may install from PyPI

If not → it falls back to PyTorch index

👉 In practice, this usually still installs CPU PyTorch, but it’s less strict

🧪 Real-world behavior for PyTorch
Recommended for most projects:
--extra-index-url https://download.pytorch.org/whl/cpu
torch
streamlit
discord.py
psycopg2-binary

✔ Works with all dependencies
✔ Keeps things simple
```

Prompt:
```
What is the best way to add UML diagrams to a markdown file?
```

Odpowiedź:
```
The “best” way depends on where your Markdown will live (GitHub, local docs, Streamlit, etc.), but there are two clear winners:

🥇 1. Use Mermaid (best overall)
✅ Why it’s usually the best choice

Native support on GitHub, GitLab, Notion

No external files needed

Easy to edit (text-based)

Clean syntax

✏️ Example (class diagram)
```mermaid
classDiagram
    class Bot {
        +run()
        +handle_message()
    }

    class LLMService {
        +generate_response()
    }

    class Database {
        +save_message()
    }

    Bot --> LLMService
    Bot --> Database

---

## ✏️ Example (sequence diagram for your project)

```markdown
```mermaid
sequenceDiagram
    participant User
    participant DiscordBot
    participant LLM
    participant DB

    User->>DiscordBot: @uksw_bot Hello
    DiscordBot->>LLM: Send message
    LLM-->>DiscordBot: Response
    DiscordBot->>DB: Save message + response
    DiscordBot-->>User: Reply

---

## ⚠️ Limitations
- Not full UML spec (simplified)
- Styling is limited
- Some platforms (older Markdown renderers) don’t support it

---

# 🥈 2. Use :contentReference[oaicite:1]{index=1} (most powerful)

## ✅ Why use it
- Full UML support (sequence, class, activity, etc.)
- Industry-standard diagrams
- More precise than Mermaid

---

## ❌ Downsides
- Requires rendering (not native in GitHub Markdown)
- Needs:
  - server OR
  - plugin OR
  - exporting images

---

## ✏️ Example

```markdown
```plantuml
@startuml
User -> Bot : mention
Bot -> LLM : send message
LLM --> Bot : response
Bot -> DB : save data
Bot --> User : reply
@enduml

👉 Usually rendered as an image before embedding.

---

# 🥉 3. Export diagrams as images (most compatible)

Tools:
- :contentReference[oaicite:2]{index=2} (aka diagrams.net)
- :contentReference[oaicite:3]{index=3}

Then:

```markdown
![UML Diagram](./diagram.png)
✅ When to use this

Documentation for non-technical users

PDFs / reports

Platforms without Mermaid support

🧠 Recommendation for YOUR project

Since you're working with:

Python

Git-style structure

likely GitHub

👉 Use Mermaid.

It’s perfect for:

documenting your architecture

showing Discord → LLM → DB flow

quick iteration

🔥 Pro tip (very useful)

For your project, include both:

1. Sequence diagram (behavior)

→ how messages flow

2. Class diagram (structure)

→ bot / services / db layers
```

Prompt:
```
How to add an image to a markdown?
```

Odpowiedź:
```
Adding an image to Markdown is simple, but there are a few useful variations depending on your setup.

🖼️ 1. Basic syntax
![Alt text](image.png)
Example:
![Bot architecture](diagram.png)

Alt text → shown if the image fails to load (also good for accessibility)

Path can be:

local file

URL

🌐 2. Image from URL
![Diagram](https://example.com/image.png)
📁 3. Local images (recommended for projects)

If your structure is:

project/
├── README.md
└── images/
    └── diagram.png

Then:

![Diagram](images/diagram.png)
📂 4. Relative paths (important)
Same folder:
![Diagram](diagram.png)
One folder up:
![Diagram](../images/diagram.png)
🎯 5. Resize / styling (not standard Markdown)

Markdown itself doesn’t support resizing, but you can use HTML:

<img src="images/diagram.png" width="400">
```

Prompt:
```
What does it mean? Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
```

Odpowiedź:
```
That warning comes from the Hugging Face Hub, and it’s basically telling you:

👉 You’re downloading models or data without being logged in.

🧠 What it actually means

When you use libraries like:

transformers

huggingface_hub

they fetch models from the Hugging Face Hub.

If you don’t provide an API token (HF_TOKEN), your requests are:

unauthenticated (anonymous)

rate-limited more strictly

sometimes slower

⚠️ What are the consequences?

Without authentication:

🚫 Lower rate limits (you may get blocked temporarily)

🐢 Slower downloads

🔒 No access to private models

❗ Possible failures in larger projects or CI pipelines

✅ How to fix it
1. Get a token

Go to: https://huggingface.co/settings/tokens

Create a token (usually Read access is enough)

2. Set the token
Option A — Environment variable (recommended)

Linux / macOS:

export HF_TOKEN=your_token_here

Windows (PowerShell):

setx HF_TOKEN "your_token_here"
Option B — Login via CLI
huggingface-cli login

Paste your token → it gets stored locally.

Option C — In Python (less common)
from huggingface_hub import login
login("your_token_here")
🧩 Do you always need this?

👉 No.

You can ignore the warning if:

you’re just testing

downloading small public models

not hitting rate limits

👉 You should fix it if:

building a real app (like your Discord bot)

deploying (server / cloud)

downloading models frequently
```

Prompt:
```
I need a regex which removes all characters between < and >
```

Odpowiedź:
```
You want to remove everything between < and > (including the brackets themselves). Here’s the clean solution:
re.sub(r"<[^>]*>", "", message)
🧠 How it works

< → matches the opening bracket

[^>] → matches any character except >

* → repeats that zero or more times

> → matches the closing bracket

👉 So it removes everything from < up to the next >, inclusive.

✅ Example
import re

text = "Hello <tag>world</tag>!"
clean = re.sub(r"<[^>]*>", "", text)

print(clean)

Output:

Hello world!
✅ Why this is a good approach

✔️ Simple and readable

✔️ Doesn’t rely on greedy/non-greedy behavior

✔️ Stops cleanly at the first >

✔️ Efficient for typical use cases

⚠️ Things to be aware of

It assumes tags are well-formed (i.e., they actually end with >)

Not suitable for parsing complex or nested HTML (but fine for text cleaning)
```
