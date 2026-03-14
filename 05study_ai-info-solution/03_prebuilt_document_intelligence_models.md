# Module: Use Prebuilt Document Intelligence Models
## Session: Prebuilt Models, General/Read/Layout Models, and Financial/ID/Tax Models

**Sources:**
- [Understand prebuilt models](https://learn.microsoft.com/en-us/training/modules/use-prebuilt-form-recognizer-models/2-understand-prebuilt-models?pivots=python)
- [Use the General Document, Read, and Layout models](https://learn.microsoft.com/en-us/training/modules/use-prebuilt-form-recognizer-models/3-use-general-document-read-layout-models)
- [Use financial, ID, and tax models](https://learn.microsoft.com/en-us/training/modules/use-prebuilt-form-recognizer-models/4-use-financial-id-tax-models)

---

## 1. What Are Prebuilt Models?

> **Prebuilt models** = models already trained by Microsoft on large datasets of common form types.

- Extract data from common forms and documents **out of the box**
- Accurate and reliable for their intended form types
- If your form is unique or industry-specific, a **custom model** may give better results (but requires training time and data)

---

## 2. All Prebuilt Models

### Specific Form Type Models

| Model | What It Extracts |
|---|---|
| **Invoice** | Customer name, PO number, dates, vendor/customer details, billing/shipping addresses, totals, line items |
| **Receipt** | Merchant details, totals, tax, tip, date/time, line items (name, qty, unit price, total) |
| **US Tax** | Unified model for W-2, 1098, 1099, 1040 forms |
| **ID Document** | Names, DOB, sex, nationality, document number, MRZ, endorsements (US drivers licenses + international passports) |
| **Business Card** | Names, addresses, email, website, phone numbers |
| **Health Insurance Card** | Fields from health insurance cards |
| **Marriage Certificate** | Information from marriage certificates |
| **Credit/Debit Card** | Common bank card fields |
| **Mortgage Documents** | Closing disclosure, Form 1003, Form 1004, Form 1005, Form 1008 |
| **Bank Statement** | Account info, beginning/ending balances, transaction details |
| **Pay Stub** | Wages, hours, deductions, net pay |
| **Check** | Payee, amount, date, and other check fields |

### General / Structural Models

| Model | What It Extracts |
|---|---|
| **Read** | Text + detected languages; classifies handwritten vs printed |
| **General Document** | Text, key-value pairs, entities, selection marks, tables |
| **Layout** | Text, structure (tables with bounding boxes, selection marks) |

---

## 3. Features Across Prebuilt Models

| Feature | Description | Models With It |
|---|---|---|
| **Text extraction** | Lines of text + words from handwritten and printed text | **All** models |
| **Key-value pairs** | Label → value pairs (e.g., `Weight: 31 kg`) | Most models |
| **Entities** | Complex data structures: people, locations, dates, etc. | **General Document only** |
| **Selection marks** | Radio buttons, checkboxes | Several models |
| **Tables** | Full table extraction including merged cells, headings | Many models |
| **Fields** | Fixed, named fields specific to a form type | Specific form models (e.g., Invoice, Receipt) |

---

## 4. Input Requirements

| Requirement | Value |
|---|---|
| **Supported formats** | JPEG, PNG, BMP, TIFF, PDF (+ Office files for Read model) |
| **Max file size** | 500 MB (standard tier) / 4 MB (free tier) |
| **Image dimensions** | 50 × 50 px minimum → 10,000 × 10,000 px maximum |
| **PDF page dimensions** | Less than 17 × 17 inches (A3) |
| **PDF protection** | Must NOT be password-protected |
| **Multi-page PDF/TIFF (standard)** | Up to 2,000 pages analyzed |
| **Multi-page PDF/TIFF (free)** | First 2 pages only |

> Tip: Submit **text-embedded PDFs** when possible — eliminates character recognition errors.

---

## 5. Calling Prebuilt Models (Python)

> Calls are **asynchronous**: submit the document → poll for the result.

```python
poller = document_analysis_client.begin_analyze_document(
    "prebuilt-layout",
    AnalyzeDocumentRequest(url_source=docUrl)
)
result: AnalyzeResult = poller.result()
```

| Parameter | Description |
|---|---|
| First arg | Model ID string (e.g., `"prebuilt-layout"`, `"prebuilt-invoice"`, `"prebuilt-read"`) |
| `url_source` | URL of the document to analyze |
| `poller.result()` | Blocks until analysis is complete; returns `AnalyzeResult` |

### Common Model ID Strings

| Model | Model ID String |
|---|---|
| Read | `"prebuilt-read"` |
| General Document | `"prebuilt-document"` |
| Layout | `"prebuilt-layout"` |
| Invoice | `"prebuilt-invoice"` |
| Receipt | `"prebuilt-receipt"` |
| ID Document | `"prebuilt-idDocument"` |
| Business Card | `"prebuilt-businessCard"` |
| US Tax | `"prebuilt-tax.us"` |

---

## 6. The Read Model

> Extracts **text and language** from documents with unpredictable structures.

| Feature | Detail |
|---|---|
| **Text extraction** | Printed and handwritten text |
| **Language detection** | Detects language of each text line |
| **Classification** | Identifies handwritten vs printed |
| **Page range** | Use `pages` parameter for multi-page PDF/TIFF |
| **Best for** | Documents with no fixed or predictable structure |

> Supports more languages for **printed** text than for **handwritten** text.

---

## 7. The General Document Model

> Extends Read by adding **key-value pairs, entities, selection marks, and tables**.

- Works on **structured, semi-structured, and unstructured** documents
- **Only prebuilt model that supports entity extraction**
- Entity extraction runs across the **whole document** (not just key-value pairs)
- A single piece of text may return **both** a key-value pair and an entity

### Entity Types (General Document Only)

| Entity Type | Examples |
|---|---|
| `Person` | Person's name |
| `PersonType` | Job title or role |
| `Location` | Buildings, geographic features, geopolitical entities |
| `Organization` | Companies, government bodies, clubs, bands |
| `Event` | Social gatherings, historical events, anniversaries |
| `Product` | Objects bought and sold |
| `Skill` | A capability belonging to a person |
| `Address` | Mailing address |
| `Phone number` | Mobile and landline numbers |
| `Email` | Email addresses |
| `URL` | Webpage addresses |
| `IP Address` | Network addresses |
| `DateTime` | Calendar dates and times |
| `Quantity` | Numerical measurements with units |

---

## 8. The Layout Model

> Extracts **text + rich structural information**: tables, selection marks, bounding boxes.

| Feature | Detail |
|---|---|
| **Text** | Full text extraction |
| **Tables** | Handles complex tables: merged cells, headers, incomplete rows/columns, angled documents |
| **Selection marks** | Extracted with bounding box, confidence score, and selected/not-selected status |
| **Table cells include** | Content text, bounding box, header flag, row/column index |
| **Best for** | Documents where structure and layout matter, not just content |

---

## 9. The Invoice Model

> Extracts fields commonly found on invoices, both **header fields** and **line item fields**.

### Header Fields

| Field | Description |
|---|---|
| Customer name + reference ID | Who is being billed |
| Purchase order number | PO reference |
| Invoice date + due date | Dates |
| Vendor details | Name, tax ID, physical address |
| Customer details | Similar to vendor |
| Billing + shipping addresses | Where to send |
| Total tax, invoice total, amount due | Financial totals |

### Line Item Fields (per purchased item)

| Field | Description |
|---|---|
| Description + product code | What was purchased |
| Unit price | Price per unit |
| Quantity | How many units |
| Tax | Tax on the line |
| Line total | Unit price × quantity |

---

## 10. The Receipt Model

> Similar to Invoice but records **amounts paid** (not charged).

### Fields Extracted

| Category | Fields |
|---|---|
| **Merchant** | Name, phone number, address |
| **Transaction** | Date and time |
| **Amounts** | Receipt total, tax, tip |
| **Line items** | Item name, quantity, unit price, total price |

> In **v3.0+**, supports single-page **hotel receipt** processing with extra fields: arrival and departure dates.

---

## 11. The ID Document Model

> Trained on **US drivers licenses** and **international passports** (biographical page only).

| Field Category | Fields |
|---|---|
| **Personal** | First/last name, sex, date of birth, nationality |
| **Document** | Country/region issued, document number, machine readable zone (MRZ) |
| **Additional** | Endorsements, restrictions, vehicle classifications |

> **Visas and other travel documents are not supported**, biographical passport pages only.

> **Data sensitivity warning:** ID data is personal and covered by data protection laws. Ensure you have the individual's permission and comply with legal requirements.

---

## 12. The Business Card Model

> Extracts contact information from business cards — handles unusual fonts and graphic design.

| Field | Examples |
|---|---|
| Names | First and last name |
| Addresses | Postal address |
| Contact | Email, website |
| Phone numbers | Various types (mobile, work, fax) |

---

## 13. Choosing the Right Model

| Scenario | Best Model |
|---|---|
| Unknown document structure, just need text | **Read** |
| Unknown structure + need entities, key-value pairs, tables | **General Document** |
| Need rich table/layout structure | **Layout** |
| Supplier/customer invoices | **Invoice** |
| Store receipts / hotel receipts | **Receipt** |
| US drivers license or international passport | **ID Document** |
| Contact exchange cards | **Business Card** |
| W-2, 1099, 1040 tax forms | **US Tax** |
| Bank statements | **Bank Statement** |
| Payslips | **Pay Stub** |
| Custom/unique industry form | **Custom model** (train your own) |

---

## Quick Reference — Exam Tips

| Key Fact | Detail |
|---|---|
| **Only model with entity extraction** | **General Document** — and only one |
| **Read model base** | Used internally by ALL other prebuilt models for text extraction |
| **Layout model strength** | Tables with merged cells, angled documents, selection marks |
| **File formats** | JPEG, PNG, BMP, TIFF, PDF (+ Office files for Read) |
| **Max file size** | 500 MB standard / 4 MB free |
| **Max pages analyzed** | 2,000 pages (standard) / 2 pages (free) |
| **PDF best practice** | Use text-embedded PDFs to avoid OCR errors |
| **Python async pattern** | `begin_analyze_document()` → `poller.result()` |
| **Hotel receipts** | Supported in Receipt model v3.0+ (extra fields: arrival/departure dates) |
| **Passport limitation** | Only biographical pages — not visas or travel docs |
| **US Tax model** | Single unified model for W-2, 1098, 1099, and 1040 |
| **Custom vs prebuilt** | Prebuilt = no training needed; Custom = needed for unique/industry forms |
