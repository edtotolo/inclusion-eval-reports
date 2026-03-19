# Financial Inclusion & Consumer Protection AI Eval

A research-grade evaluation framework for assessing AI applications in finance and commerce against financial inclusion and consumer protection standards.

---

## What this is

This eval provides a structured test suite for assessing how any AI application — a chatbot, loan advisor, customer service bot, or payment assistant — performs against principles of financial inclusion and consumer protection.

It is designed for use by:
- **Researchers** analysing AI-in-finance deployments in emerging markets
- **FSPs and fintechs** conducting internal due diligence before deploying AI
- **Policymakers and regulators** setting standards for AI in financial services
- **Donors and investors** assessing the inclusion credentials of fintech portfolio companies

---

## Theoretical grounding

| Framework | Source |
|---|---|
| G20 High-Level Principles for Digital Financial Inclusion | G20 GPFI |
| Consumer Protection in Digital Finance | CGAP |
| Universal Financial Access 2020 | World Bank |
| Financial Health Framework | CFI / Center for Financial Inclusion |
| OECD/INFE Financial Consumer Protection Principles | OECD |
| Responsible Finance Principles | Smart Campaign / Responsible Finance Forum |
| High-Risk AI Systems in Financial Services | EU AI Act (Art. 6 + Annex III) |

---

## Evaluation dimensions

| # | Dimension | Sub-dimensions | Test cases |
|---|---|---|---|
| D1 | Access and Inclusion | Informal economy, thin file, gender, rural, literacy | 15 |
| D2 | Consumer Protection | Transparency, accuracy, suitability, recourse, manipulation | 20 |
| D3 | Fairness and Non-Discrimination | Consistent treatment across income, gender, geography | 12 |
| D4 | Data and Privacy | Minimization, consent, security, third-party sharing | 10 |
| D5 | Responsible AI Conduct | Disclosure, uncertainty, human referral, harm avoidance | 10 |
| **Total** | | | **67** |

---

## Quick start

### Option A: Document-based assessment (no code required)
1. Read `framework/01_dimensions.md` to understand the evaluation dimensions
2. Use `assessor_tools/assessment_questionnaire.md` to conduct a structured manual assessment
3. Record scores in `assessor_tools/scorecard_template.csv`
4. Interpret results using `framework/02_scoring.md`

### Option B: Automated LLM evaluation (requires Python + API key)
```bash
cd "eval_runner"
pip install -r requirements.txt
# Set your API key:
export ANTHROPIC_API_KEY=your_key_here
# Run eval against a target LLM application:
python run_eval.py --target_url https://your-ai-app-api-endpoint \
                   --dimensions D1,D2,D3,D4,D5 \
                   --output ../outputs/eval_report.json
```

---

## File structure

```
Inclusion Eval/
├── README.md                          ← this file
├── framework/
│   ├── 01_dimensions.md               ← full framework with principles
│   └── 02_scoring.md                  ← scoring methodology and interpretation
├── test_cases/
│   ├── D1_access_inclusion.yaml       ← 15 test cases
│   ├── D2_consumer_protection.yaml    ← 20 test cases
│   ├── D3_fairness.yaml               ← 12 test cases
│   ├── D4_data_privacy.yaml           ← 10 test cases
│   └── D5_responsible_ai.yaml         ← 10 test cases
├── eval_runner/
│   ├── run_eval.py                    ← main evaluation runner
│   ├── judge.py                       ← LLM-as-judge scoring logic
│   ├── report.py                      ← report generation
│   └── requirements.txt
├── assessor_tools/
│   ├── assessment_questionnaire.md    ← non-technical assessor guide
│   └── scorecard_template.csv        ← scoring spreadsheet
└── outputs/                           ← eval results saved here
```

---

## Application types this eval covers

| Application type | Primary dimensions | Notes |
|---|---|---|
| Loan / credit AI | D1, D2, D3 | Focus on access, suitability, fairness |
| Financial advisory AI | D2, D3, D5 | Focus on accuracy, conflict of interest |
| Customer service AI | D2, D4, D5 | Focus on transparency, recourse, data |
| Payment / wallet AI | D2, D4, D5 | Focus on fraud, unauthorized transactions |
| Insurance AI | D2, D3, D5 | Focus on suitability, exclusions, claims |
| Fraud detection AI (ML) | D3 | Use fairness metrics, see framework note |

---

## Limitations

- Test cases are designed primarily for LLM-based (conversational) AI applications. Evaluating ML scoring models requires additional statistical methods not covered here.
- Automated scoring via LLM-as-judge introduces its own bias; human review of edge cases is recommended.
- Test cases reflect a global emerging-market perspective. Specific regulatory requirements (e.g., RBI guidelines in India, BACEN in Brazil) may require additional local test cases.
- This eval does not assess backend system architecture, algorithmic fairness of underlying models, or data governance — only the AI's conversational outputs.

---

*Framework version: 1.0 | Built for Center for Financial Inclusion research use*
