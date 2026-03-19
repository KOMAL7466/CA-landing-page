# CA-related keywords for basic classification
CA_KEYWORDS = [
    'invoice', 'receipt', 'tax', 'gst', 'income', 
    'expense', 'audit', 'balance sheet', 'profit',
    'loss', 'financial', 'statement', 'account',
    'revenue', 'expenditure', 'asset', 'liability',
    'depreciation', 'dividend', 'interest', 'salary',
    'trading', 'p&l', 'profit & loss', 'balance sheet'
]

def is_ca_related(text: str) -> bool:
    """Check if document contains CA-related keywords"""
    if not text:
        return False
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CA_KEYWORDS)

def classify_document(text: str) -> dict:
    """Classify document type"""
    text_lower = text.lower()
    
    # Simple rule-based classification (can be replaced with ML later)
    if any(word in text_lower for word in ['invoice', 'bill', 'receipt']):
        return {"type": "invoice", "confidence": 0.8}
    elif any(word in text_lower for word in ['balance sheet', 'assets', 'liabilities']):
        return {"type": "balance_sheet", "confidence": 0.8}
    elif any(word in text_lower for word in ['tax', 'gst', 'itr']):
        return {"type": "tax_document", "confidence": 0.7}
    else:
        return {"type": "unknown", "confidence": 0.3}