# Module: Integrate Custom Tools into Your Agent
## Session: Why Custom Tools, Tool Options & How to Implement Them
**Sources:**
- [Why use custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/2-why-use-custom-tools)
- [Options for implementing custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/3-custom-tool-options)
- [How to integrate custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/4-how-use-custom-tools)

---

## 1. Why Use Custom Tools?

> Custom tools connects it to external systems, data, and business logic specific to your needs.

**3 core benefits:**

| Benefit | Description |
|---|---|
| **Enhanced productivity** | Automate repetitive tasks and streamline workflows specific to your use case |
| **Improved accuracy** | Provide precise and consistent outputs, reducing human error |
| **Tailored solutions** | Address specific business needs and optimize processes |



### How an Agent Uses a Custom Tool (Example: Weather Tool)

```
1. User asks: "What are the ski conditions at the resort?"
         ↓
2. Agent determines it has a tool that can fetch meteorological data via API
         ↓
3. Agent calls the tool → tool returns weather report
         ↓
4. Agent informs the user using the tool's result
```

---

## 2. Common Scenarios for Custom Tools

| Industry | Scenario | Tool Does | Outcome |
|---|---|---|---|
| **Retail / Customer support** | Connect agent to **CRM system (customer relationship system)** | Retrieve order history, process refunds, provide shipping status | Faster query resolution, reduced support workload |
| **Manufacturing** | Link agent to **inventory management system** | Check stock levels, predict restocking needs, place orders automatically | Streamlined inventory, optimized supply chain |
| **Healthcare** | Integrate scheduling tool with **patient records** | Suggest appointment slots, send reminders, access patient data | Reduced admin burden, better patient experience |
| **IT / Helpdesk** | Connect agent to **ticketing + knowledge base** | Troubleshoot issues, escalate complex problems, track ticket statuses | Faster resolution, reduced downtime |
| **Education** | Connect agent to **LMS (learning management system)** | Recommend courses, track student progress, answer course questions | Enhanced learning, increased student engagement |

---

## 3. Custom Tool Options in Foundry Agent Service

> Foundry Agent Service supports **4 custom tool types**, each suited to different integration scenarios.

| Tool Type | What It Is | Best For |
|---|---|---|
| **Custom function (Function calling)** | Describe custom function structure to the agent; agent calls it dynamically based on user intent | **Custom logic/workflows** in code; any programming language |
| **Azure Functions** | Serverless, **event-driven** functions with triggers and bindings | Event-driven workloads; minimal infrastructure overhead |
| **OpenAPI Specification tools** | Connect agent to external APIs using an **OpenAPI 3.0 spec** | Standardized API integrations; public or internal REST APIs |
| **Azure Logic Apps** | **Low-code/no-code workflow** automation | Connecting apps, data, and services without heavy coding |

### Key Concepts

| Concept | Definition |
|---|---|
| **Triggers** (Azure Functions) | Determine **when** a function executes (e.g., HTTP request, queue message) |
| **Bindings** (Azure Functions) | Facilitate **connections to input/output data sources** (simplify wiring) |
| **OpenAPI 3.0** | Standard spec format that describes HTTP APIs; enables automated and scalable API integration |
| **Auth types (OpenAPI)** | Three supported: **anonymous**, **API key**, **managed identity** |

---

## 4. How to Implement Custom Tools

### 4.1 Function Calling

> **Function calling** = define a Python function + register it with the agent using the SDK. The agent **dynamically calls** it when the user prompt requires it.

**Step 1: Define the function**

```python
import json

def recent_snowfall(location: str) -> str:
    """
    Fetches recent snowfall totals for a given location.
    :param location: The city name.
    :return: Snowfall details as a JSON string.
    """
    mock_snow_data = {"Seattle": "0 inches", "Denver": "2 inches"}
    snow = mock_snow_data.get(location, "Data not available.")
    return json.dumps({"location": location, "snowfall": snow})
```

**Step 2: Register the function with the agent**

```python
# Define a function tool for the model to use
function_tool = FunctionTool(
    name="recent_snowfall",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "The city name to check snowfall for."},
        },
        "required": ["location"],
        "additionalProperties": False
    },
    description="Get recent snowfall totals for a given location.",
    strict=True,
)

tools: list[Tool] = [function_tool]

agent = project_client.agents.create_version(
    name="snowfall-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions="You are a weather assistant tracking snowfall. Use the provided functions to answer questions.",
        tools=tools,
    )
)
```

> The agent now **automatically calls** `recent_snowfall` when the user asks about snowfall.

---

### 4.2 Azure Functions Integration

> **Azure Functions** = serverless compute; agent communicates via **storage queues** (input queue → function → output queue).

**Register an Azure Function as a tool:**

```python
tool = AzureFunctionTool(
    azure_function=AzureFunctionDefinition(
        input_binding=AzureFunctionBinding(
            storage_queue=AzureFunctionStorageQueue(
                queue_name="STORAGE_INPUT_QUEUE_NAME",
                queue_service_endpoint="STORAGE_QUEUE_SERVICE_ENDPOINT",
            )
        ),
        output_binding=AzureFunctionBinding(
            storage_queue=AzureFunctionStorageQueue(
                queue_name="STORAGE_OUTPUT_QUEUE_NAME",
                queue_service_endpoint="STORAGE_QUEUE_SERVICE_ENDPOINT",
            )
        ),
        function=AzureFunctionDefinitionFunction(
            name="queue_trigger",
            description="Get weather for a given location",
            parameters={
                "type": "object",
                "properties": {"location": {"type": "string", "description": "location to determine weather for"}},
            },
        ),
    )
)

agent = project_client.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions="You are a helpful weather assistant. Use the provided Azure Function to get weather information.",
        tools=[tool],
    ),
)
```

**Azure Function communication flow:**
```
Agent → puts message on INPUT QUEUE → Azure Function executes → puts result on OUTPUT QUEUE → Agent reads result
```

---

### 4.3 OpenAPI Specification Integration

> **OpenAPI tools** = agent connects to any HTTP API using a standard JSON/YAML spec file. No custom SDK code needed for the API itself.

**Step 1: Create the OpenAPI JSON spec file (e.g., `weather_openapi.json`)**

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "get weather data",
    "description": "Retrieves current weather data for a location.",
    "version": "v1.0.0"
  },
  "servers": [{ "url": "https://wttr.in" }],
  "paths": {
    "/{location}": {
      "get": {
        "description": "Get weather information for a specific location",
        "operationId": "GetCurrentWeather",
        "parameters": [
          {
            "name": "location",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          },
          {
            "name": "format",
            "in": "query",
            "required": true,
            "schema": { "type": "string", "default": "j1" }
          }
        ],
        "responses": {
          "200": { "description": "Successful response" },
          "404": { "description": "Location not found" }
        }
      }
    }
  }
}
```

**Step 2: Register the OpenAPI tool with the agent**

```python
from azure.ai.projects.models import OpenApiTool, OpenApiAnonymousAuthDetails

with open(weather_asset_file_path, "r") as f:
    openapi_weather = cast(dict[str, Any], jsonref.loads(f.read()))

tool = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="get_weather",
        spec=openapi_weather,
        description="Retrieve weather information for a location.",
        auth=OpenApiAnonymousAuthDetails(),
    )
)

agent = project_client.agents.create_version(
    agent_name="openapi-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions="You are a weather assistant. Use the API to fetch weather data.",
        tools=[openapi_tool],
    ),
)
```

---

## 5. Declarative Nature of Custom Tools (Key Concept)

> You do **NOT** write code that explicitly calls your custom tool functions, the **agent itself decides** when and how to call them.

| What You Do | What the Agent Does |
|---|---|
| Define functions with meaningful names | Reads the name and description |
| Document parameters clearly | Understands what input is needed |
| Register the tool with the agent | Can see the tool is available |
| — | **Figures out when to call the function** based on user prompts |

> This is the **declarative** pattern, describe the capability, let the agent decide when to use it.

---

## 6. Quick Reference

### Custom Tool Options Summary

| Tool | Code Required | Hosting | Best For |
|---|---|---|---|
| **Custom function** | Yes (define + register via SDK) | In-process (your code) | Custom logic, data retrieval, any language |
| **Azure Functions** | Deploy a function + register via SDK | Serverless (Azure) | Event-driven workflows, queue-based processing |
| **OpenAPI Spec** | Provide spec JSON + register via SDK | External API | Public/internal REST APIs with OpenAPI 3.0 spec |
| **Azure Logic Apps** | Low-code/no-code | Azure Logic Apps | Workflow automation, connecting apps/data/services |

### OpenAPI Authentication Types

| Auth Type | When to Use |
|---|---|
| **Anonymous** | Public APIs with no auth required |
| **API key** | APIs that require a key in headers/query |
| **Managed identity** | Azure-hosted APIs using Entra ID |

### Exam Tips

| Concept | Key Point |
|---|---|
| **Why custom tools** | Productivity (automate), Accuracy (consistent), Tailored (business-specific) |
| **Agent tool invocation** | Agent **autonomously decides** when to call a tool — declarative, not explicit |
| **Function calling** | Define function → register via `FunctionTool` → agent calls it dynamically |
| **Azure Functions** | Serverless; uses storage queues for input/output binding |
| **OpenAPI Spec tools** | Uses **OpenAPI 3.0** standard; 3 auth types: anonymous, API key, managed identity |
| **Azure Logic Apps** | Low-code/no-code; connects apps, data, and services |
| **Triggers** | Determine **when** an Azure Function executes |
| **Bindings** | Simplify connections to **input/output data** in Azure Functions |
| **Declarative pattern** | Provide meaningful names + documented parameters → agent "figures out" when to call |
| **Can mix tool types** | Use any combination of custom tools in one agent |
