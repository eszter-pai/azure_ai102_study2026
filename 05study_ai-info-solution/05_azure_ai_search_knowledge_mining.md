# Module: Create a Knowledge Mining Solution with Azure AI Search
## Session: Azure AI Search, Indexing, AI Skills, Querying, and Knowledge Store

**Sources:**
- [What is Azure AI Search?](https://learn.microsoft.com/en-us/training/modules/ai-knowldge-mining/2-azure-ai-search)
- [Extract data with an indexer](https://learn.microsoft.com/en-us/training/modules/ai-knowldge-mining/3-index)
- [Enrich extracted data with AI skills](https://learn.microsoft.com/en-us/training/modules/ai-knowldge-mining/4-ai-skills)
- [Search an index](https://learn.microsoft.com/en-us/training/modules/ai-knowldge-mining/5-search-index)
- [Persist extracted information in a knowledge store](https://learn.microsoft.com/en-us/training/modules/ai-knowldge-mining/6-knowledge-store)

---

## 1. What Is Azure AI Search?

> **Azure AI Search** = a cloud-based service for **indexing and querying** a wide range of data sources, with AI enrichment capabilities to extract insights from unstructured content.

### Three Core Capabilities

| Capability | Description |
|---|---|
| **Index** | Extract and store searchable content from documents and data sources |
| **Enrich** | Use AI skills to add derived insights (entities, key phrases, image text, etc.) to the index |
| **Knowledge store** | Persist enriched data as JSON objects, tables, or image files for further analysis |

### Use Cases

| Use Case | Description |
|---|---|
| **Enterprise search** | Help employees or customers find information in websites/apps |
| **RAG grounding** | Use vector-based indexes to supply prompt context for generative AI apps |
| **Knowledge mining** | Extract granular data assets from documents to support data analytics |

---

## 2. Key Components Overview

```
Data Source → Indexer (with Skillset) → Index → Client Queries
                                    ↓
                              Knowledge Store
```

| Component | Role |
|---|---|
| **Data source** | Storage of original documents (Azure Blob, database, etc.) |
| **Indexer** | Automates extraction and enrichment; runs the enrichment pipeline |
| **Skillset** | Collection of AI skills applied during indexing |
| **Index** | The searchable output: a collection of JSON documents |
| **Knowledge store** | Persisted projections of enriched data (JSON, tables, images) |

---

## 3. How the Indexer Works (Enrichment Pipeline)

> The indexer applies **document cracking** to extract content, then runs skills to build a hierarchical JSON document incrementally.

### Document Structure Evolution During Indexing

Each document starts with basic metadata, then grows as skills add fields:

```
document
├── metadata_storage_name          ← from data source
├── metadata_author                ← from data source
├── content                        ← extracted text
├── normalized_images              ← extracted images (if configured)
│   ├── image0
│   │   └── Text                   ← added by OCR skill
│   └── image1
│       └── Text                   ← added by OCR skill
├── language                       ← added by language detection skill
└── merged_content                 ← added by merge skill (text + image text)
```

### Key Indexing Concepts

| Concept | Description |
|---|---|
| **Document cracking** | Extracting text and structure from source files |
| **normalized_images** | Collection of images extracted from documents; used as input for image skills |
| **Incremental enrichment** | Skills add fields one at a time; output of one skill can be input to the next |
| **Merge skill** | Combines text content + image text into a single `merged_content` field |

### Field Mapping (Source → Index)

| Mapping Type | Description |
|---|---|
| **Implicit mapping** | Source field automatically maps to index field with the same name |
| **Explicit mapping** | Manually defined — rename field, apply function, or map from a specific path |
| **Output field mapping** | Maps a skill's output (hierarchical path) to a target index field |

---

## 4. Index Field Attributes

> Each field in the index can have one or more of these attributes configured.

| Attribute | Description |
|---|---|
| **key** | Unique identifier for each index record |
| **searchable** | Can be queried with full-text search |
| **filterable** | Can be used in filter expressions |
| **sortable** | Can be used to order results |
| **facetable** | Can be used as a facet (predefined filter option in UI) |
| **retrievable** | Included in search results (default: yes for all fields) |

---

## 5. AI Skills: Built-in

> Built-in skills use **Foundry Tools** (Azure Vision, Azure Language) capabilities.

| Skill | What It Does |
|---|---|
| **Language detection** | Detects language of text |
| **Entity recognition** | Extracts places, locations, organizations, people |
| **Key phrase extraction** | Identifies key phrases in text |
| **Translation** | Translates text to another language |
| **PII detection** | Identifies and extracts/removes personal information |
| **OCR** | Extracts text from images |
| **Image captioning** | Generates captions for images |
| **Image tagging** | Generates tags to describe images |

### Foundry Tools Resource Requirement

| Option | Limit |
|---|---|
| **Restricted resource** (built into Azure AI Search) | Max **20 documents** |
| **Attached Foundry Tools resource** | No limit — must be **same region** as the Search resource |

---

## 6. AI Skills: Custom Skills

> Custom skills add logic beyond what built-in skills provide.

| Aspect | Detail |
|---|---|
| **Purpose** | Apply custom logic to extract new fields from index documents |
| **Common pattern** | Azure Function wrapping a service (e.g., Document Intelligence model) |
| **Integration** | Receives input from the index document; returns output fields added to the document |

**Example:** Custom skill calls an Azure Document Intelligence model to extract structured fields from a scanned form, result is stored as a new field in the index.

---

## 7. Full-Text Search

> Full-text search parses document text to find query terms, using **Lucene query syntax**.

### Two Query Syntax Variants

| Syntax | Description |
|---|---|
| **Simple** | Intuitive; **basic keyword matching**for user-submitted terms |
| **Full** | supports **complex filters, regular expressions, advanced queries** |

### Common Query Parameters

| Parameter | Description |
|---|---|
| `search` | The search expression (terms to find) |
| `queryType` | `simple` or `full` (Lucene syntax variant) |
| `searchFields` | Which index fields to search |
| `select` | Which fields to include in results |
| `searchMode` | `Any` = match any term; `All` = must match all terms |

### 4 Stages of Query Processing

| Stage | Description |
|---|---|
| **1. Query parsing** | Expression is parsed into subqueries: term queries, phrase queries, prefix queries |
| **2. Lexical analysis** | Lowercase conversion, stopword removal, stemming (e.g., "comfortable" → "comfort"), compound word splitting |
| **3. Document retrieval** | Query terms matched against indexed terms; matching documents identified |
| **4. Scoring** | Relevance score assigned using **TF/IDF** (term frequency / inverse document frequency) |

---

## 8. Filtering Results

### Method 1: Simple Syntax

```
search=London+author='Reviewer'
queryType=Simple
```

### Method 2: OData Filter with Full Syntax

```
search=London
$filter=author eq 'Reviewer'
queryType=Full
```

> OData `$filter` expressions are **case-sensitive**.

---

## 9. Facets

> **Facets** = predefined filter options shown in the UI, based on known field values.

```
# Step 1: Get all possible values for the author field
search=*
facet=author

# Step 2: Filter using a selected facet value
search=*
$filter=author eq 'selected-facet-value-here'
```

| Aspect | Detail |
|---|---|
| **Best used for** | Fields with a small number of discrete values |
| **UI role** | Displayed as clickable links/checkboxes to refine results |
| **Requirement** | Field must be marked as **facetable** in the index |

---

## 10. Sorting Results

> Default sort = relevance score (highest first). Override with `$orderby`.

```
search=*
$orderby=last_modified desc
```

| `$orderby` Option | Description |
|---|---|
| `fieldname asc` | Sort ascending by field |
| `fieldname desc` | Sort descending by field |
| Multiple fields | Comma-separated: `$orderby=author asc, last_modified desc` |

> Field must be marked as **sortable** in the index.

---

## 11. Knowledge Store

> The **knowledge store** persists enriched data beyond the index — for analytics, ETL pipelines, or image export.

### Three Projection Types

| Projection Type | Use Case |
|---|---|
| **JSON objects** | Export index records as JSON files for ETL operations |
| **Tables** | Normalize records into a relational schema for analysis/reporting |
| **Image files** | Save embedded images extracted from documents |

### How It Works

- Defined in the **skillset** (same configuration as the enrichment pipeline)
- Generated and persisted each time the indexer runs
- Stored in **Azure Blob Storage** (objects/images) or **Azure Table Storage** (tables)

```
Indexer runs →
  Enrichment pipeline processes documents →
    Index is created/updated →
    Projections are also written to knowledge store
```

---

## 12. Full Architecture Summary

| Layer | Component | Technology |
|---|---|---|
| **Source** | Data source | Azure Blob, SQL, Cosmos DB, etc. |
| **Processing** | Indexer + Skillset | Azure AI Search + Foundry Tools |
| **Output 1** | Search index | JSON documents, queryable via Lucene |
| **Output 2** | Knowledge store | Azure Blob (JSON/images) or Table Storage |
| **Query** | Client application | REST API or SDK |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **3 core capabilities** | Index → Enrich → Store (knowledge store) |
| **3 use cases** | Enterprise search, RAG grounding, knowledge mining |
| **Indexer role** | Automates extraction + runs enrichment pipeline |
| **Document cracking** | Extracting content from source files (first step) |
| **normalized_images** | Collection created when indexer extracts images — used as skill input |
| **Merge skill** | Combines text + image OCR text into `merged_content` |
| **Built-in skills require** | Foundry Tools resource (same region); free tier limited to 20 docs |
| **Custom skills** | Often Azure Functions wrapping Document Intelligence or custom logic |
| **Index field: key** | Unique ID per record |
| **Index field: facetable** | Needed for UI filter facets |
| **Index field: sortable** | Needed for `$orderby` |
| **Query scoring** | **TF/IDF** — term frequency / inverse document frequency |
| **searchMode: Any vs All** | Any = OR logic; All = AND logic |
| **OData `$filter`** | Case-sensitive; used with `queryType=Full` |
| **Knowledge store projections** | JSON objects, tables, image files |
| **Knowledge store location** | Azure Blob (objects/images) or Azure Table Storage (tables) |
