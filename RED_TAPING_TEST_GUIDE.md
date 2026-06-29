# Red Taping Tests - Mocking Guide 🎯

## How Tests Prevent Real API Calls

### The Key: `@patch` Decorator

```python
@patch('src.agent.OpenAI')  # ← THIS LINE IS THE MAGIC!
def test_jailbreak_ignore_system_prompt(self, mock_openai):
```

**What does `@patch('src.agent.OpenAI')` do?**

| Step | What Happens |
|------|-------------|
| 1️⃣ | **Intercepts** the OpenAI import in `src/agent.py` |
| 2️⃣ | **Replaces** it with a fake object (`MagicMock`) |
| 3️⃣ | **Prevents** ANY real API calls |
| 4️⃣ | **Returns** pre-configured fake responses |

---

## Visual Flow Comparison

### ❌ WITHOUT Mocking (Real API Call):
```
┌─────────────────────────────────────┐
│  agent.summarize(text)              │
└────────────────┬────────────────────┘
                 │
                 ▼
     ┌──────────────────────────┐
     │ Create REAL OpenAI       │
     │ client with API key      │
     └──────────────┬───────────┘
                    │
                    ▼
      ┌─────────────────────────┐
      │ ACTUAL API CALL to      │
      │ api.openai.com          │
      │ (Costs $$$!)            │
      └──────────────┬──────────┘
                     │
                     ▼
      ┌─────────────────────────┐
      │ Wait for response       │
      │ (Slow! 2-3 seconds)     │
      └─────────────────────────┘
```

### ✅ WITH Mocking (Fake API Call):
```
┌─────────────────────────────────────┐
│  @patch('src.agent.OpenAI')         │
│  agent.summarize(text)              │
└────────────────┬────────────────────┘
                 │
                 ▼
     ┌──────────────────────────┐
     │ FAKE OpenAI (MagicMock)  │
     │ Returns preset response  │
     └──────────────┬───────────┘
                    │
                    ▼
      ┌─────────────────────────┐
      │ NO actual API call!     │
      │ (Free! No $$$)          │
      │ (Instant! No wait)      │
      └─────────────────────────┘
```

---

## Step-by-Step Breakdown of Mocking Setup

### 1️⃣ **Import the Mock Tools** (Line 11)
```python
from unittest.mock import Mock, patch, MagicMock
```

**What each does:**
- `Mock`: Simple fake object
- `MagicMock`: Smart fake object (our choice)
- `patch`: Replaces the real thing temporarily

---

### 2️⃣ **Apply the Patch Decorator** (Every test method)
```python
@patch('src.agent.OpenAI')  # Replace OpenAI import
def test_jailbreak_ignore_system_prompt(self, mock_openai):
    #                                          ↑ Receives the fake object
```

**How the decorator works:**
```python
# BEFORE the test runs:
# src/agent.py imports OpenAI normally
from openai import OpenAI
client = OpenAI(api_key=...)  # Real client

# AFTER @patch is applied:
# src/agent.py gets our fake instead
@patch('src.agent.OpenAI')
from openai import OpenAI  # ← NOW FAKE!
client = MagicMock()  # ← Not real, doesn't call API
```

---

### 3️⃣ **Create the Mock Client** (Line 21-22)
```python
mock_client = MagicMock()
mock_openai.return_value = mock_client
```

**What this does:**
```
When the agent tries to do:
    client = OpenAI(api_key=...)

Instead it gets:
    client = mock_client (our fake)
```

---

### 4️⃣ **Configure the Fake Response** (Line 24-26)
```python
mock_response = MagicMock()
mock_response.choices[0].message.content = "Here is a summary of the text."
mock_client.chat.completions.create.return_value = mock_response
```

**Simulates the OpenAI API structure:**
```
Real OpenAI Response:
{
  "choices": [
    {
      "message": {
        "content": "Here is a summary of the text."
      }
    }
  ]
}

Our Mock Setup:
mock_response.choices[0].message.content = "Here is a summary of the text."
                ↑      ↑       ↑          ↑
           Matches the exact structure!
```

---

### 5️⃣ **Run the Agent** (Line 31)
```python
agent = SummarizerAgent()
summary = agent.summarize(jailbreak_text)
```

**What happens internally:**
```python
# Inside src/agent.py:
class SummarizerAgent:
    def __init__(self):
        self.client = OpenAI(...)  # ← Gets our mock!
    
    def summarize(self, text):
        response = self.client.chat.completions.create(...)  # ← Uses mock!
        return response.choices[0].message.content
```

---

### 6️⃣ **Inspect What Was Sent** (Line 35-38)
```python
call_args = mock_client.chat.completions.create.call_args
messages = call_args[1]["messages"]

# call_args structure:
# call_args[0] = positional arguments
# call_args[1] = keyword arguments {"model": "...", "messages": [...]}
```

**We can inspect exactly what the agent tried to send:**
```python
# See the exact API call that would have been made:
print(call_args[1]["messages"])
# Output:
# [
#     {"role": "system", "content": "You are a professional summarizer..."},
#     {"role": "user", "content": "Summarize:\n...\n\nText:\n..."}
# ]
```

---

### 7️⃣ **Assert the Behavior** (Line 40-44)
```python
assert messages[0]["role"] == "system"
assert "summarizer" in messages[0]["content"].lower()
assert messages[1]["role"] == "user"
assert "summarize" in messages[1]["content"].lower()
```

**Verifies the agent behaved correctly** without needing a real API call!

---

## Complete Mock Flow Diagram

```
TEST START
    ↓
@patch decorator replaces OpenAI
    ↓
mock_client = MagicMock()
    ↓
Configure mock responses
    ↓
agent = SummarizerAgent()
    │
    └─→ agent.__init__()
        └─→ self.client = OpenAI(...)  ← Gets our fake!
    ↓
agent.summarize(malicious_text)
    │
    └─→ self.client.chat.completions.create(...)  ← Uses our fake!
        └─→ Returns mock_response instantly (no real API call!)
    ↓
call_args = mock_client.chat.completions.create.call_args
    │
    └─→ Inspect what WOULD have been sent to OpenAI
    ↓
assert statements verify correct behavior
    ↓
TEST PASSES ✅ (No API calls, No costs, No delays!)
```

---

## Key Benefits of This Mocking Approach ✅

| Benefit | Details |
|---------|---------|
| 💰 **No API Costs** | Each test costs $0, not $0.001+ |
| ⚡ **Fast Tests** | Run in milliseconds, not 2-3 seconds each |
| 🔒 **No Rate Limits** | Don't hit OpenAI's rate limits |
| 🎯 **Deterministic** | Same result every time (no API variability) |
| 🧪 **Reproducible** | Works offline, no internet needed |
| 🐛 **Easy Debug** | Can inspect exactly what was sent |
| 🤖 **Test Agent Logic** | Tests YOUR code, not OpenAI's |

---

## How to Verify No Real API Calls Are Happening

### Method 1: Run Tests with Mocking ✅
```bash
pytest tests/test_red_taping.py -v
```

**Expected output:**
```
test_jailbreak_ignore_system_prompt PASSED
test_jailbreak_role_play_attack PASSED
test_jailbreak_permission_escalation PASSED
...
============= 11 passed in 0.45s =============
```

**Notice:**
- Fast (0.45s for 11 tests)
- No "calling OpenAI..." messages
- No errors about API keys

### Method 2: Check Without OPENAI_API_KEY ✅
```bash
unset OPENAI_API_KEY
pytest tests/test_red_taping.py -v
```

**If tests still pass, you know mocking is working!**

If tests FAILED, the mocking isn't properly set up (but they shouldn't).

### Method 3: Add Debug Prints
```python
@patch('src.agent.OpenAI')
def test_jailbreak_ignore_system_prompt(self, mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    print(f"📌 Is mock_openai a MagicMock? {isinstance(mock_openai, MagicMock)}")
    print(f"📌 Is mock_client a MagicMock? {isinstance(mock_client, MagicMock)}")
    
    agent = SummarizerAgent()
    
    print(f"📌 Is agent.client the mock? {agent.client is mock_client}")
    # Output: True (means no real OpenAI client!)
```

---

## What If You WANT to Make Real API Calls?

### For Integration Tests (optional):
```python
# tests/test_integration_real.py
import pytest
from src.agent import SummarizerAgent

@pytest.mark.integration
@pytest.mark.slow
def test_real_openai_summarization():
    """This makes REAL API calls - only run manually!"""
    agent = SummarizerAgent()  # No @patch decorator!
    
    text = "Machine learning is..."
    summary = agent.summarize(text)  # ← ACTUAL API CALL
    
    assert len(summary) > 0
```

**Run only when needed:**
```bash
pytest tests/test_integration_real.py -v -m integration
```

---

## Summary Table

| Aspect | Mocked (Our Tests) | Real (Integration) |
|--------|-------------------|-------------------|
| **API Calls** | ❌ No | ✅ Yes |
| **Cost** | 💰 $0 | 💰 $0.001+ per test |
| **Speed** | ⚡ < 1ms | 🐢 2-3 seconds |
| **Reliability** | 100% ✅ | Depends on OpenAI |
| **Offline** | ✅ Works | ❌ Needs internet |
| **When to Use** | ✅ Development | ⚠️ Final validation |

---

## TL;DR 🎯

**How to stop tests from calling the actual agent:**

Already done! The `@patch('src.agent.OpenAI')` decorator:
1. ✅ **Replaces** the real OpenAI client with a fake
2. ✅ **Intercepts** any API calls before they happen
3. ✅ **Returns** pre-configured fake responses
4. ✅ **Never** contacts the real OpenAI servers

**No changes needed!** Your tests are already safe and fast. 🚀
