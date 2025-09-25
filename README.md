# 📦 AI Agents Policy Adherence

This tool analyzes policy documents and generates deterministic Python code to enforce operational policies when invoking AI agent tools.

## 🚀 Features

The workflow consists of two main steps:

**step 1**:  
Takes a policy document in Markdown format and an OpenAPI specification describing the available tools. For each tool, it generates a JSON file containing associated policies and examples of both compliance and violations.  
These files can be reviewed and edited manually before proceeding to Step 2.  
The OpenAPI document should describe agent tools and optionally include *read-only* tools that might be used to enforce policies. It’s important that each tool has:
- A proper `operation_id` matching the tool name
- A detailed description
- Clearly defined input parameters and return types
- Well-documented data models

**step 2**:  
Uses the output from Step 1 and the OpenAPI spec to generate Python code that enforces each tool’s policies.

---

## 🐍 Requirements

- Python 3.12+
- `pip`

---

## 🛠 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/IBM/tool_guard.git
   cd tool_guard
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**

   Copy the `.env.example` to `.env` and fill in your environment variables. 
   Replace required keys with your actual API keys.

## ▶️ Usage

Run main() in `tests/run_tau2_airline.py` for generating tool guards for the tau-bench airline domain.


