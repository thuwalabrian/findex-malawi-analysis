# Data Dictionary: Findex Malawi 2024 Analysis

**Project:** Financial Inclusion in Malawi  
**Dataset:** World Bank Global Findex 2024 - Malawi Microdata  
**Sample Size:** 1,000 adults (age 15+)  
**Reference:** Global Findex Codebook 2024

---

## Table of Contents
- [Core Variables](#core-variables)
- [Demographic Variables](#demographic-variables)
- [Financial Inclusion Indicators](#financial-inclusion-indicators)
- [Barrier Variables](#barrier-variables)
- [Digital Financial Services](#digital-financial-services)
- [Derived Variables](#derived-variables)

---

## Core Variables

### Survey Administration

| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `year` | Survey year | 2024 | Fixed |
| `economy` | Country name | "Malawi" | Fixed |
| `economycode` | ISO country code | "MWI" | Fixed |
| `regionwb` | World Bank region | "Sub-Saharan Africa" | Fixed |
| `wpid_random` | Anonymous respondent ID | Numeric | Unique identifier |
| `wgt` | Survey weight | Float (>0) | **Use for all population estimates** |
| `pop_adult` | Adult population | Numeric | National estimate |

---

## Demographic Variables

### Gender
| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `female` | Gender | 1 = Female<br>2 = Male | Binary classification |

### Age
| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `age` | Age in years | 15-99 | Continuous variable |

### Education
| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `educ` | Highest education level | 1 = Primary or less<br>2 = Secondary<br>3 = Tertiary or more | Ordinal scale |

### Income
| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `inc_q` | Income quintile | 1 = Poorest 20%<br>2 = Second 20%<br>3 = Middle 20%<br>4 = Fourth 20%<br>5 = Richest 20% | Within-country quintiles |

### Employment
| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `emp_in` | Workforce status | 1 = In workforce<br>2 = Out of workforce | Includes formal & informal |

### Residence
| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `urbanicity` | Urban/Rural | 1 = Rural<br>2 = Urban | Based on national definition |

---

## Financial Inclusion Indicators

### Account Ownership (Constructed Variables)

**Important:** These are pre-calculated by World Bank and include skip logic adjustments.

| Variable | Description | Coding | Calculation Notes |
|----------|-------------|--------|-------------------|
| `account` | Has any financial account | 0 = No<br>1 = Yes | Includes bank OR mobile money |
| `account_fin` | Has bank/formal account | 0 = No<br>1 = Yes | Bank, credit union, microfinance, post office |
| `account_mob` | Has mobile money account | 0 = No<br>1 = Yes | Used mobile money in past 12 months |
| `dig_account` | Has digital account | 0 = No<br>1 = Yes | Either account_fin or account_mob |

### Financial Behaviors (Constructed)

| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `saved` | Saved money (any method) | 0 = No<br>1 = Yes | Formal or informal |
| `borrowed` | Borrowed money (any source) | 0 = No<br>1 = Yes | Past 12 months |
| `anydigpayment` | Made/received digital payment | 0 = No<br>1 = Yes | Any digital transaction |
| `merchantpay_dig` | Made digital merchant payment | 0 = No<br>1 = Yes | Paid business digitally |

---

## Barrier Variables

### Bank Account Barriers (fin11a-f)

**Asked to:** Respondents without a bank account  
**Question:** "Why don't you have an account at a bank or similar financial institution?"  
**Coding:** 1 = Yes (reason applies), 2 = No, 3 = Don't know, 4 = Refused, . = Not asked

| Variable | Description | Analysis Recoding |
|----------|-------------|-------------------|
| `fin11a` | Too far away | Distance barrier |
| `fin11b` | Too expensive (fees) | Cost barrier |
| `fin11c` | Lack necessary documentation | Documentation barrier |
| `fin11d` | Lack trust in financial institutions | Trust barrier |
| `fin11e` | Religious reasons | Religious barrier |
| `fin11f` | Family member already has account | Family proxy |
| `fin11_1` | Lack of money | Economic barrier |
| `fin11_2` | No need for account | Demand barrier |

### Mobile Money Barriers (fin14a-e)

**Asked to:** Respondents in Sub-Saharan Africa without mobile money  
**Question:** "Why don't you use mobile money services?"  
**Coding:** 1 = Yes, 2 = No, 3 = Don't know, 4 = Refused, . = Not asked

| Variable | Description | Analysis Recoding |
|----------|-------------|-------------------|
| `fin14a` | Agents/vendors too far away | Distance barrier |
| `fin14b` | Too expensive (transaction fees) | Cost barrier |
| `fin14c` | Lack necessary documentation | Documentation barrier |
| `fin14d` | Lack of money to use service | **Primary economic barrier** |
| `fin14e` | Worry about security/fraud | Security/trust barrier |

---

## Digital Financial Services

### Digital Connectivity

| Variable | Description | Coding | Notes |
|----------|-------------|--------|-------|
| `internet_use` | Used internet in past 12 months | 0 = No<br>1 = Yes | Any device |
| `con1` | Owns mobile phone | 1 = Yes<br>2 = No | Personal or household |

### Digital Payments

| Variable | Description | Coding | Asked To |
|----------|-------------|--------|----------|
| `fin25e2` | Used card/phone for in-store purchase | 1 = Yes<br>2 = No | Account holders only |
| `fin34a` | Received wages into bank account | 1 = Yes<br>2 = No | Wage earners |
| `fin34b` | Received wages via mobile money | 1 = Yes<br>2 = No | Wage earners |
| `fin34c` | Received wages in cash | 1 = Yes<br>2 = No | Wage earners |

### Saving Methods

| Variable | Description | Coding | Asked To |
|----------|-------------|--------|----------|
| `fin17a` | Saved at financial institution | 1 = Yes<br>2 = No | All respondents |
| `fin17b` | Saved using mobile money | 1 = Yes<br>2 = No | Mobile money users |
| `fin17c` | Saved using savings club | 1 = Yes<br>2 = No | All respondents |

### Borrowing Sources

| Variable | Description | Coding | Asked To |
|----------|-------------|--------|----------|
| `fin22a` | Borrowed from financial institution | 1 = Yes<br>2 = No | All respondents |
| `fin22b` | Borrowed from family/friends | 1 = Yes<br>2 = No | All respondents |
| `fin22c` | Borrowed from savings club | 1 = Yes<br>2 = No | Savings club members |

---

## Derived Variables

### Created in Analysis (Notebook 04)

| Variable | Description | Derivation | Range |
|----------|-------------|------------|-------|
| `barrier_distance` | Any distance barrier | fin11a=1 OR fin14a=1 | 0/1 |
| `barrier_cost` | Any cost barrier | fin11b=1 OR fin14b=1 | 0/1 |
| `barrier_document` | Any documentation barrier | fin11c=1 OR fin14c=1 | 0/1 |
| `barrier_trust` | Any trust/security barrier | fin11f=1 OR fin14e=1 | 0/1 |

| `barrier_no_money` | Lack of money barrier | fin11d=1 OR fin14d=1 | 0/1 |

---

## Important Coding Notes

### 1. **Missing Values Are Structural**
- Not all questions are asked to all respondents
- Questions follow skip logic based on previous answers
- Example: Mobile money questions only asked if respondent doesn't have mobile money
- **Do NOT treat missing as "No"** — check codebook for eligibility

### 2. **Binary vs. Response Coding**
- **Constructed variables** (account, saved, etc.): 0 = No, 1 = Yes
- **Questionnaire variables** (fin17a, fin22a, etc.): 1 = Yes, 2 = No
- **Always check before analysis!**

### 3. **Survey Weights**
- Variable: `wgt`
- Purpose: Expand sample to population level
- **Must use** for all percentage calculations
- Formula: `weighted_mean = sum(values * weights) / sum(weights)`

### 4. **Variable Naming Convention**
- `fin##` = Financial inclusion questions
- `con##` = Digital connectivity questions  
- `fh#` = Financial health questions
- `account_*` = Constructed account indicators
- `barrier_*` = Analysis-created composite barriers

---

## Sample Analytical Examples

### Calculate National Account Ownership
```python
import numpy as np
national_rate = np.average(df['account'], weights=df['wgt'])
print(f"Account ownership: {national_rate * 100:.1f}%")
```

### Gender Comparison (Proper Recoding)
```python
# Create binary female variable
df['is_female'] = (df['female'] == 1).astype(int)

# Compare
female_rate = np.average(df[df['is_female']==1]['account'], 
                         weights=df[df['is_female']==1]['wgt'])
male_rate = np.average(df[df['is_female']==0]['account'], 
                       weights=df[df['is_female']==0]['wgt'])
gap = (male_rate - female_rate) * 100
print(f"Gender gap: {gap:.1f} percentage points")
```

### Barrier Analysis (Questionnaire Variables)
```python
# Recode: 1=Yes → 1, 2=No → 0, others → NaN
valid_mask = df['fin14d'].isin([1, 2])
barrier_rate = np.average(
    (df.loc[valid_mask, 'fin14d'] == 1).astype(int),
    weights=df.loc[valid_mask, 'wgt']
)
print(f"Lack of money barrier: {barrier_rate * 100:.1f}%")
```

---

## Data Quality Checks

### Recommended Validations

✅ **Survey weights:**
- Sum of weights ≈ adult population
- No zero or negative weights
- No missing weights

✅ **Sample size:**
- N = 1,000 (Malawi)
- Check no duplicate `wpid_random`

✅ **Variable ranges:**
- Binary variables only have 0/1
- Categorical variables within expected ranges
- No unexpected values

✅ **Missing patterns:**
- Check skip logic makes sense
- High missingness expected for conditional questions
- Demographic variables should have minimal missing

---

## References

1. **Global Findex Codebook 2024**  
   World Bank Group  
   [Available in data/raw/ directory]

2. **Methodology Documentation**  
   Demirgüç-Kunt et al. (2024)  
   [https://www.worldbank.org/globalfindex](https://www.worldbank.org/globalfindex)

3. **Questionnaire**  
   Gallup World Poll 2024  
   [Available from World Bank on request]

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | February 2026 | Initial data dictionary created |

---

## Contact

For questions about variable definitions or data quality:
- **Data Source:** World Bank Global Findex Team
- **Analysis:** Brian Thuwala (thuwalabrian@gmail.com)

---

**Note:** This data dictionary supplements the official Global Findex codebook and focuses on variables used in this specific analysis. Always refer to the official codebook for authoritative definitions.
