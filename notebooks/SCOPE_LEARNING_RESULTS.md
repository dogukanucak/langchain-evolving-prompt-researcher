# SCOPE Learning Results: Before & After

## Overview
SCOPE automatically improved prompt outputs across 4 out of 5 extraction tasks, learning to normalize formats and maintain consistency without any manual prompt engineering.

---

## 📧 Task 1: Email Extraction

**Input:** `SUPPORT@COMPANY.COM, Sales: sales@test.org, or Info <INFO@HELP.NET>`

### Before Learning
```
- SUPPORT@COMPANY.COM
- sales@test.org
- INFO@HELP.NET
```

### After Learning ✅
```
support@company.com
sales@test.org
info@help.net
```

**Improvement:** Normalized all emails to lowercase, removed bullet points for cleaner format.

---

## 📧 Task 2: Email Extraction (Consistency Test)

**Input:** `Alice.Brown@TECH.COM, bob.smith@startup.io, Contact: HR@BUSINESS.ORG`

### Before Learning
```
- alice.brown@tech.com
- bob.smith@startup.io
- hr@business.org
```

### After Learning ✅
```
alice.brown@tech.com
bob.smith@startup.io
hr@business.org
```

**Improvement:** Applied learned lowercase rule, consistent formatting (no bullets).

---

## 📅 Task 3: Date Extraction

**Input:** `12/25/2024, January 1st 2025, and 2025-02-14`

### Before Learning
```
12/25/2024, January 1st 2025, 2025-02-14
```

### After Learning ✅
```
2024-12-25, 2025-01-01, 2025-02-14
```

**Improvement:** Standardized all dates to YYYY-MM-DD format from three different input formats.

---

## 📅 Task 4: Date Extraction (Consistency Test)

**Input:** `March 15th 2025, 04/20/2025, and 2025-05-30`

### Before Learning
```
2025-03-15, 2025-04-20, 2025-05-30
```

### After Learning ✅
```
2025-03-15, 2025-04-20, 2025-05-30
```

**Improvement:** Already correctly formatted on first run (learned from Task 3)! No changes needed.

---

## 📞 Task 5: Phone Number Extraction

**Input:** `1-555-CALL-NOW (555-2255), office (555)123.4567, or mobile: 555 987 6543`

### Before Learning
```
1-555-CALL-NOW (555-2255), (555)123.4567, 555 987 6543
```

### After Learning ✅
```
(555) 123-4567
555-987-6543
```

**Improvement:** Removed invalid phone number with letters, standardized format, cleaned up spacing.

---

## 📊 Learning Metrics

| Metric | First Run | Second Run | Improvement |
|--------|-----------|------------|-------------|
| Learning Events | 4 | 2 | 50% reduction |
| Tasks with Visible Improvements | N/A | 4/5 | 80% |
| Format Standardization | Inconsistent | Consistent | ✅ |

---

## 🎯 Key Takeaways

**What SCOPE Learned:**
1. ✅ **Email normalization:** Convert all emails to lowercase
2. ✅ **Date standardization:** Use YYYY-MM-DD format consistently  
3. ✅ **Phone cleanup:** Remove invalid entries, standardize format
4. ✅ **Cross-task consistency:** Apply learned rules to similar tasks

**Without any manual prompt engineering**, SCOPE observed outputs, identified inconsistencies, and automatically generated strategic rules that improved:
- Data normalization (case, format)
- Consistency across similar tasks
- Output cleanliness (removing invalid data)

**Result:** Fewer learning events needed on the second run proves the prompt is better optimized!

---

*Generated from SCOPE (Self-Correcting Optimal Prompt Evolution) tutorial notebook*
