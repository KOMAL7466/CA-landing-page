import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
import time
from datetime import datetime, timedelta
import json
import random

load_dotenv()
logger = logging.getLogger(__name__)

class ChatModel:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # ========== BUILT-IN KNOWLEDGE BASE ==========
        self.knowledge_base = {
            "gst": {
                "keywords": ["gst", "goods and services tax", "gst rate", "gst filing"],
                "response": """📊 **GST (Goods and Services Tax)**

**What is GST?**
GST is a comprehensive indirect tax levied on the supply of goods and services in India. It has replaced multiple cascading taxes like VAT, Service Tax, Excise Duty, etc.

**Key GST Rates:**
• 0% - Essential items (food grains, milk, etc.)
• 5% - Household necessities (sugar, tea, coffee)
• 12% - Computers, processed food
• 18% - Most services, AC, fridge
• 28% - Luxury items, sin goods

**GST Registration Threshold:**
• ₹20 lakhs for goods (₹10 lakhs for special category states)
• ₹20 lakhs for services

**Filing Due Dates:**
• GSTR-1: 11th of next month
• GSTR-3B: 20th of next month
• Annual Return: 31st December

💡 *Note: Rates and rules may change. Consult your CA for current rates.*"""
            },
            
            "itr": {
                "keywords": ["itr", "income tax return", "file itr", "tax filing", "income tax"],
                "response": """📄 **Income Tax Return (ITR) Filing**

**What is ITR?**
ITR is a form used to declare your income, investments, and taxes paid to the Income Tax Department.

**Types of ITR Forms:**
• **ITR-1 (Sahaj):** For salaried individuals (income up to ₹50 lakhs)
• **ITR-2:** For individuals/HUF not having business income
• **ITR-3:** For business/profession income
• **ITR-4 (Sugam):** Presumptive business income

**Due Dates:**
• 31st July - For individuals (non-audit)
• 31st October - With audit
• 31st December - Transfer pricing cases

**Documents Required:**
• Form 16 (for salaried)
• Bank statements
• Investment proofs (80C, 80D)
• TDS certificates

**Penalty for Late Filing:**
• Up to ₹5,000 (if filed after due date but before Dec 31)
• Up to ₹10,000 (if filed after Dec 31)

💡 *Always verify current due dates with your CA.*"""
            },
            
            "tax_saving": {
                "keywords": ["tax saving", "save tax", "tax planning", "tax deduction", "80c", "80d"],
                "response": """💰 **Tax Saving Tips (Section 80C, 80D, etc.)**

**Section 80C (Maximum ₹1.5 lakhs):**
• PPF (Public Provident Fund)
• ELSS Mutual Funds (3-year lock-in)
• Life Insurance Premium
• EPF/VPF
• Sukanya Samriddhi Yojana
• Tax-saving FDs (5-year lock-in)
• Home Loan Principal repayment

**Section 80D (Health Insurance):**
• Self + Family: Up to ₹25,000
• Senior Citizens: Up to ₹50,000
• Preventive Health Check-up: Up to ₹5,000

**Other Deductions:**
• **80E:** Education Loan Interest (no limit)
• **80EEA:** Home Loan Interest (first-time buyers) - ₹1.5 lakhs
• **80G:** Donations to specified funds
• **80TTA:** Savings Account Interest - ₹10,000
• **80TTB:** Senior Citizens - ₹50,000

**HRA Exemption:**
If you live in rented accommodation and get HRA

**NPS (National Pension System):**
• Additional ₹50,000 deduction under 80CCD(1B)

💡 *Plan early in the financial year for maximum benefits!*"""
            },
            
            "audit": {
                "keywords": ["audit", "statutory audit", "tax audit", "internal audit", "audit requirements"],
                "response": """🔍 **Audit Requirements in India**

**Types of Audit:**

1. **Statutory Audit** (Companies Act)
   • Mandatory for all companies
   • Conducted by Chartered Accountant
   • Financial statements verification
   • Due date: 30th September

2. **Tax Audit** (Income Tax Act)
   • Turnover > ₹1 crore (business)
   • Gross receipts > ₹50 lakhs (profession)
   • Presumptive taxation cases > ₹2 crore
   • Due date: 30th September
   • Report in Form 3CA/3CB and 3CD

3. **Internal Audit**
   • Voluntary (but recommended)
   • Checks internal controls
   • Operational efficiency

4. **GST Audit**
   • Turnover > ₹5 crore
   • Annual return filing
   • Reconciliation of GSTR-1 and GSTR-3B

**Audit Process:**
• Planning & Risk Assessment
• Internal Control Testing
• Substantive Procedures
• Evidence Collection
• Reporting

**Penalties for Non-Audit:**
• ₹1.5 lakhs or 0.5% of turnover (whichever less)

💡 *Audit ensures compliance and builds trust!*"""
            },
            
            "tds": {
                "keywords": ["tds", "tax deducted at source", "tds rate", "tds return", "form 16", "form 16a"],
                "response": """📋 **TDS (Tax Deducted at Source)**

**What is TDS?**
TDS is a mechanism where tax is deducted at the time of payment itself.

**Common TDS Rates:**

| Section | Payment Type | TDS Rate |
|---------|--------------|----------|
| 192 | Salary | As per slab |
| 193 | Interest on Securities | 10% |
| 194A | Interest (other than securities) | 10% |
| 194C | Contract payments | 1-2% |
| 194H | Commission/Brokerage | 5% |
| 194I | Rent | 2-10% |
| 194J | Professional/Technical fees | 10% |

**TDS Return Forms:**
• **Form 24Q:** Salary
• **Form 26Q:** Non-salary
• **Form 27Q:** Non-resident

**Important Dates:**
• TDS Payment: 7th of next month
• TDS Return: 31st May/July/October/January (quarterly)

**Forms for Deductee:**
• **Form 16:** Salary TDS (annual)
• **Form 16A:** Non-salary TDS (quarterly)

💡 *Always verify TDS is correctly deducted and deposited!*"""
            },
            
            "balance_sheet": {
                "keywords": ["balance sheet", "financial statement", "assets", "liabilities", "equity"],
               "response": """📊 **Balance Sheet Basics**

**What is a Balance Sheet?**
A balance sheet shows a company's financial position at a specific point in time.

**The Fundamental Equation:** } 

**Components:**

**1. ASSETS (What company owns)**
• **Current Assets:** Cash, Inventory, Debtors, Investments (<1 year)
• **Fixed Assets:** Property, Plant, Equipment
• **Intangible Assets:** Patents, Trademarks, Goodwill

**2. LIABILITIES (What company owes)**
• **Current Liabilities:** Creditors, Short-term loans, Provisions
• **Long-term Liabilities:** Bank loans, Debentures, Bonds

**3. SHAREHOLDERS' EQUITY**
• Share Capital
• Reserves & Surplus
• Retained Earnings

**Key Ratios to Check:**
• **Current Ratio:** Current Assets / Current Liabilities (>1.5 is good)
• **Debt-to-Equity:** Total Debt / Shareholders' Equity (<2 is good)
• **Working Capital:** Current Assets - Current Liabilities

💡 *A healthy balance sheet shows strong liquidity and manageable debt!*"""
            },
            
            "profit_loss": {
                "keywords": ["profit and loss", "p&l", "income statement", "revenue", "expenses", "net profit"],
                "response": """📈 **Profit & Loss Account**

**What is P&L?**
The P&L shows company's financial performance over a period (monthly/quarterly/annually).

**Structure:**

**INCOME (Revenue)**
• Sales Revenue
• Other Income (Interest, Dividend)

**EXPENSES**
• Cost of Goods Sold
• Operating Expenses:
  - Salary & Wages
  - Rent
  - Utilities
  - Depreciation
  - Administrative Costs
• Finance Costs (Interest)
• Tax Expenses

**The Bottom Line:**

**Important Metrics:**
• **Gross Profit Margin:** Gross Profit / Revenue × 100
• **Net Profit Margin:** Net Profit / Revenue × 100
• **Operating Ratio:** Operating Expenses / Revenue × 100

💡 *Consistent profit growth indicates a healthy business!*"""
            },
            
            "startup": {
                "keywords": ["startup", "business registration", "company registration", "incorporation", "startup india"],
                "response": """🚀 **Startup Registration & Compliance**

**Business Structure Options:**

| Type | Features | Best For |
|------|----------|----------|
| **Sole Proprietorship** | Single owner, unlimited liability | Freelancers, small shops |
| **Partnership** | 2-20 partners, unlimited liability | Small businesses |
| **LLP** | Limited liability, less compliance | Professional services |
| **Private Limited** | Limited liability, funding eligible | Funded startups, scalability |

**Registration Process (Private Limited):**
1. DIN (Director Identification Number)
2. DSC (Digital Signature Certificate)
3. Name approval (RUN form)
4. SPICe+ form filing
5. PAN & TAN application
6. Bank account opening

**Startup India Recognition:**
• Tax exemption for 3 years
• Angel tax exemption
• IPR benefits
• Easy compliance

**Basic Compliances:**
• Annual ROC filing
• Income Tax Return
• GST Return (if applicable)
• Board Meetings (4 per year)
• Annual General Meeting

💡 *Choose structure based on your funding and scalability needs!*"""
            },
            
            "default": {
                "response": """🤝 **CA Assistant Here!**

I can help you with:

📌 **Taxation**
• GST registration & filing
• Income Tax Returns (ITR)
• TDS compliance
• Tax planning

📊 **Accounting**
• Bookkeeping
• Financial statements
• Balance sheet analysis
• Profit & Loss accounts

🔍 **Audit**
• Statutory audit
• Tax audit
• Internal audit
• GST audit

🏢 **Business Setup**
• Company registration
• LLP formation
• Startup compliance
• Business advisory

💡 **What would you like to know more about?**

Try asking:
• "What is GST?"
• "How to save tax?"
• "ITR filing process"
• "Audit requirements"
• "TDS rates"
• "Balance sheet basics"
• "Startup registration"
• "Tax planning tips"
"""
            }
        }
        
        # Initialize Gemini (as fallback)
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
                logger.info("Gemini model initialized as fallback")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.model = None
        else:
            self.model = None
            
        self.quota_reset_time = None
    
    def find_best_response(self, message: str) -> str:
        """Find best response from knowledge base"""
        message_lower = message.lower()
        
        # Check each category
        for category, data in self.knowledge_base.items():
            if category == "default":
                continue
            
            # Check if any keyword matches
            for keyword in data.get("keywords", []):
                if keyword in message_lower:
                    return data["response"]
        
        # Check for specific question patterns
        if any(word in message_lower for word in ["what is", "explain", "meaning", "define"]):
            return self.knowledge_base["default"]["response"]
        
        # Default response
        return self.knowledge_base["default"]["response"]
    
    async def get_response(self, message: str) -> str:
        """Get response - first try knowledge base, then Gemini"""
        
        # First, try built-in knowledge base
        kb_response = self.find_best_response(message)
        
        # If it's not the default response, return it
        if kb_response != self.knowledge_base["default"]["response"]:
            logger.info("Using knowledge base response")
            return kb_response
        
        # If no model, return default
        if not self.model:
            return kb_response
        
        # Check quota cooldown
        if self.quota_reset_time and datetime.now() < self.quota_reset_time:
            wait_minutes = int((self.quota_reset_time - datetime.now()).total_seconds() / 60)
            return f"⏳ **Daily Limit Reached**\n\nThe AI assistant has reached its daily request limit. This resets automatically every 24 hours.\n\n⏱️ **Approximate wait time: {wait_minutes} minutes**\n\nIn the meantime, try asking about:\n• GST basics\n• Tax saving tips\n• ITR filing\n• Audit requirements\n• TDS rates"
        
        # Try Gemini as fallback
        try:
            prompt = f"""You are a professional Chartered Accountant assistant with 15+ years experience in Indian taxation, audit, and accounting.

Question: {message}

Provide accurate, helpful information. If you're not sure, say so. Include relevant section numbers where applicable.

Keep response professional but friendly. End with a relevant follow-up question."""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_str = str(e)
            
            # Handle quota errors
            if "429" in error_str or "quota" in error_str.lower():
                import re
                retry_match = re.search(r'retry[_\s]?delay[_\s]?[:\s]+(\d+)', error_str.lower())
                if retry_match:
                    retry_seconds = int(retry_match.group(1))
                    self.quota_reset_time = datetime.now() + timedelta(seconds=retry_seconds)
                
                return self.knowledge_base["default"]["response"]
            
            logger.error(f"Gemini error: {e}")
            return kb_response
    
    def get_daily_limit(self):
        return "~1,000"