# Module: Develop AI apps with the Microsoft Foundry SDK
## Session: Microsoft Foundry SDK — Projects, Connections, and Chat Client
**Sources:**
- [What is the Microsoft Foundry SDK?](https://learn.microsoft.com/en-us/training/modules/ai-foundry-sdk/02-azure-ai-foundry-sdk)
- [Work with project connections](https://learn.microsoft.com/en-us/training/modules/ai-foundry-sdk/03-connections)
- [Create a chat client](https://learn.microsoft.com/en-us/training/modules/ai-foundry-sdk/04-chat-client)

---

## 1. What is the Microsoft Foundry SDK?

> The Microsoft Foundry SDK allows developers to write code that **connects to a Microsoft Foundry project**, accesses its resource connections and deployed models, and performs AI operations (e.g., sending prompts and processing responses).

- Microsoft Foundry provides a **REST API** for working with projects and resources
- Multiple **language-specific SDKs** wrap the REST API for easier development

### Azure AI Projects Library

| Language | Package |
|---|---|
| **Python** | `azure-ai-projects` (PyPI) |
| **C# / .NET** | `Azure.AI.Projects` (NuGet) |
| **JavaScript** | `@azure/ai-projects` (npm) |

---

### 1.1 Install the SDK (Python)

```bash
pip install azure-ai-projects
pip install azure-identity
```

> `azure-identity` is required for **authentication** using **DefaultAzureCredential**.

---

### 1.2 Connect to a Project: AIProjectClient

> Every Microsoft Foundry project has a unique **endpoint URL**, found on the project's **Overview** page in the Foundry portal.

**Three endpoints available per project:**

| Endpoint | Used For |
|---|---|
| **Project endpoint** | Access project connections, agents, and models in the Foundry resource |
| **Azure OpenAI Service endpoint** | Azure OpenAI Service APIs in the project's Foundry resource |
| **Foundry Tools endpoint** | Foundry Tools APIs (e.g., Azure Vision, Azure Language) |

**create an AIProjectClient:**

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_endpoint = "https://......"
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint
)
```

> The code must run in an **authenticated Azure session**. Use `az login` (Azure CLI) before running.

---

## 2. Work with Project Connections

> Each Microsoft Foundry project includes **connected resources** connections to external services like **Azure Storage, Azure AI Search, Azure OpenAI, or other Foundry resources**.

- Connections can be defined at the **parent level** (**Foundry resource or Hub**) or at the **project level**
- The SDK lets you retrieve and use these connections programmatically

---

### 2.1 The connections Property

> The `AIProjectClient` object exposes a `connections` property with two key methods:

| Method | What It Does |
|---|---|
| `connections.list()` | Returns all connections in the project. Filter by type using optional `connection_type` parameter (e.g., `ConnectionType.AZURE_OPEN_AI`) |
| `connections.get(connection_name, include_credentials)` | Returns a single named connection. If `include_credentials=True` (default), returns credentials (e.g., API key) needed to connect |

> Connection objects include **connection-specific properties and credentials** to use the associated resource.

---

### 2.2 Code — List All Connections

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_endpoint = "https://....."
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint,
)

# List all connections
connections = project_client.connections
for connection in connections.list():
    print(f"{connection.name} ({connection.type})")
```

---

## 3. Create a Chat Client

> A common AI application scenario: connect to a generative AI model and use prompts in a **chat-based dialog**.

### 3.1 Two Ways to Connect to a Model

| Approach | How |
|---|---|
| **Direct (Azure OpenAI SDK)** | Connect using key-based or Microsoft Entra ID authentication |
| **Via Foundry SDK** (**recommended**) | Get a project client → get an authenticated OpenAI chat client from it |

**Why use the Foundry SDK approach:**
- Easier to manage models deployed in your project
- Switch between models by simply **changing the deployment name parameter**
- Works with **any model** deployed in the Foundry resource (including non-OpenAI models e.g., Microsoft Phi)

---

### 3.2 get_openai_client() Method

> The `AIProjectClient` method `get_openai_client()` returns an authenticated **OpenAI chat client** **for any model** deployed in the project's Foundry resource.

**Required packages:**

```bash
pip install azure-ai-projects
pip install azure-identity
pip install openai
```

---

### 3.3 Full Chat Client Example

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import AzureOpenAI

# Connect to the project
project_endpoint = "https://......"
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint,
)

# Get an authenticated OpenAI chat client
chat_client = project_client.get_openai_client(api_version="2024-10-21")

# Send a prompt and get a response
user_prompt = input("Enter a question:")

response = chat_client.chat.completions.create(
    model=your_model_deployment_name,          # name of your deployed model
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_prompt}
    ]
)

print(response.choices[0].message.content)
```

---

### 3.4 Message Roles Explained

| Role | Set By | Purpose |
|---|---|---|
| `system` | Developer | Sets the assistant's behavior and persona (hidden from end user) |
| `user` | End user | The question or prompt from the user |
| `assistant` | Model | The model's response (used in multi-turn conversations) |

---

## 4. SDK Workflow Summary

```
1. Install packages
   pip install azure-ai-projects azure-identity openai

2. Authenticate
   az login  (Azure CLI)

3. Create AIProjectClient
   AIProjectClient(credential=DefaultAzureCredential(), endpoint=project_endpoint)

4. (Optional) List or retrieve connections
   project_client.connections.list()
   project_client.connections.get("connection_name")

5. Get chat client
   chat_client = project_client.get_openai_client(api_version="...")

6. Send prompts and process responses
   chat_client.chat.completions.create(model=..., messages=[...])
```

---

## 5. Quick Reference

### Key Classes and Methods

| Class / Method | Purpose |
|---|---|
| `AIProjectClient` | Main entry point — connects to a Foundry project |
| `AIProjectClient.connections.list()` | List all resource connections in the project |
| `AIProjectClient.connections.get()` | Get a specific connection with optional credentials |
| `AIProjectClient.get_openai_client()` | Get an authenticated OpenAI chat client |
| `chat.completions.create()` | Send a prompt to a deployed model and get a response |
| `DefaultAzureCredential()` | Handles Azure authentication automatically |

### Required Python Packages

| Package | Purpose |
|---|---|
| `azure-ai-projects` | Core Foundry SDK: **project client and connections** |
| `azure-identity` | Authentication via `DefaultAzureCredential` |
| `openai` | OpenAI client used for chat completions |

### Exam Tips

| Concept | Key Point |
|---|---|
| **AIProjectClient** | The central SDK object; requires project endpoint + credentials |
| **Project endpoint** | Found on the project Overview page in Foundry portal |
| **connections.list()** | Lists all connected resources; filterable by type |
| **connections.get()** | Returns a named connection with credentials by default |
| **get_openai_client()** | Returns a chat client that works with ANY model in the Foundry resource |
| **DefaultAzureCredential** | Handles auth automatically; requires `az login` session |
| **model parameter** | Set to your deployment name — easy to switch between models |
| **system role** | Developer-set instructions; not visible to end users |
