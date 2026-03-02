# 🚨 SECURITY REMEDIATION GUIDE
## Removing Microdata from Git History

**Status:** URGENT  
**Issue:** World Bank Global Findex microdata (371 KB CSV) is committed to git history  
**Risk:** File is visible in GitHub if repository is public; permanent in commit history

---

## 📋 Quick Summary

The file `data/raw/Findex_Microdata_2025_updateMalawi.csv` was committed in the initial commit (be51b44). Even if you delete the file and push new commits, **it remains permanently in git history and is accessible to anyone with repo access** via:
- `git show <commit>:data/raw/Findex_Microdata_2025_updateMalawi.csv`
- GitHub's commit view
- Network graphs and archive downloads

---

## ✅ Solution: Two Options

### **OPTION A: Quick Fix (Recommended for Small Team)**
Rewrite history locally, force push to reset GitHub.

**Pros:** Completely removes from history  
**Cons:** Rewrites commit hashes (requires team coordination)  
**Time:** ~5 minutes

### **OPTION B: BFG Repo-Cleaner (Safest)**
Professional tool used by GitHub for exactly this purpose.

**Pros:** Cleaner, reversible, widely trusted  
**Cons:** Requires additional tool installation  
**Time:** ~10 minutes

---

## 🔧 OPTION A: Git Filter-Branch (Windows PowerShell)

### Step 1: Backup Current Branch
```powershell
cd c:\Users\DMZ\Desktop\findex-malawi-analysis
git branch backup-before-cleaning
```

### Step 2: Remove File from All Commits
```powershell
# Remove the file from history completely
git filter-branch --tree-filter `
  'if (Test-Path "data/raw/Findex_Microdata_2025_updateMalawi.csv") { Remove-Item "data/raw/Findex_Microdata_2025_updateMalawi.csv" -Force }' `
  -f -- --all
```

### Step 3: Clean Git References
```powershell
# Remove reflogs and clean objects
Remove-Item .git/refs/original -Recurse -Force
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Step 4: Verify Success
```powershell
# Check file is gone from history
git log --all --full-history -- data/raw/Findex_Microdata_2025_updateMalawi.csv
# Should return NOTHING

# Verify repository size decreased
git count-objects -v
```

### Step 5: Force Push to GitHub
```powershell
# ⚠️ WARNING: This rewrites public history. Notify team first!
git push origin --force --all
git push origin --force --tags
```

### Step 6: Cleanup
```powershell
# Delete backup branch once verified safe
git branch -D backup-before-cleaning
```

---

## 🛠️ OPTION B: BFG Repo-Cleaner (Professional)

### Step 1: Install BFG
```powershell
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
# Or use Chocolatey:
choco install bfg
```

### Step 2: Create Clean Repo Clone
```powershell
# BFG works best on a fresh clone
cd c:\temp
git clone --mirror "https://github.com/YOU/findex-malawi-analysis.git" findex-clean.git
cd findex-clean.git
```

### Step 3: Remove the File
```powershell
# Remove file by path
bfg --delete-files "data/raw/Findex_Microdata_2025_updateMalawi.csv" findex-clean.git

# Or remove all CSVs in raw directory
bfg --delete-files "*.csv" --path "data/raw/" findex-clean.git
```

### Step 4: Cleanup
```powershell
cd findex-clean.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Step 5: Push Back
```powershell
git push --mirror https://github.com/YOU/findex-malawi-analysis.git
```

### Step 6: Warn Your Team
Anyone with local clones must do:
```powershell
git fetch --all
git reset --hard origin/main
```

---

## 🔍 Verification Checklist

After cleanup, verify the file is completely removed:

```powershell
# ✅ Should return nothing (file not in history)
git log --all --full-history -- "data/raw/Findex_Microdata_2025_updateMalawi.csv"

# ✅ Should show file is untracked
git status

# ✅ Repository size should decrease noticeably
git count-objects -v

# ✅ File should be in .gitignore (active rule now)
Get-Content .gitignore | Where-Object {$_ -match 'data/raw/\*\.csv'}
```

---

## 📌 Prevention Going Forward

Now that cleanup is done, the updated `.gitignore` and `.gitattributes` prevent future issues:

✅ **data/raw/*.csv** — Raw microdata ignored  
✅ **data/raw/*.xlsx** — Excel files ignored  
✅ **.gitattributes** — Large file warnings in place  
✅ **CONTRIBUTING.md** — Data handling guidelines documented

---

## ⚠️ Important Notes

### For GitHub Public Repositories
- GitHub caches old commits; **flush the cache** by:
  1. Making repo Private temporarily
  2. Wait 5 minutes
  3. Make repo Public again
- OR contact GitHub Support to purge cache

### For Team Repositories
Notify your team:
```
Subject: Repository History Rewritten - Security Fix

The findex-malawi-analysis repository history has been rewritten to remove 
sensitive data files. Please:

1. Delete your local clone
2. Re-clone: git clone https://github.com/...
3. Do NOT push old branches

Questions? Contact: thuwalabrian@gmail.com
```

### Commit Message to Document This

After pushing cleaned history, commit this remediation guide:
```powershell
git add SECURITY_REMEDIATION.md
git commit -m "docs: Add security remediation guide for history cleaning"
git push
```

---

## 🚀 Complete Security Checklist

After completing cleanup, verify all items:

- [ ] Microdata file removed from git history
- [ ] `.gitignore` activated for `data/raw/*.csv`
- [ ] `.gitattributes` created for large file handling
- [ ] `CONTRIBUTING.md` added with data handling guidelines
- [ ] `CODEOWNERS` file created
- [ ] GitHub repository secrets scanned (Settings > Security)
- [ ] No API keys/credentials in any commits
- [ ] Repository size decreased significantly
- [ ] Local clone refreshed from GitHub
- [ ] Team notified of changes (if applicable)
- [ ] README updated with data download instructions

---

## 📞 Need Help?

If something goes wrong:
1. You have a `backup-before-cleaning` branch (Option A)
2. The original mirror is still in `findex-clean.git` (Option B)
3. Contact: thuwalabrian@gmail.com

---

**Last Updated:** March 2, 2026  
**Action Required:** Yes (complete within 24 hours if repo is public)
