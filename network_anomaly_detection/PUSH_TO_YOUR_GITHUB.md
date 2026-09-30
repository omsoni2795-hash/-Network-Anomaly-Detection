# Push to GitHub - Commands for omsoni2795-hash

## ✅ Your GitHub Account: https://github.com/omsoni2795-hash

---

## 🚀 Step-by-Step Instructions:

### **Step 1: Create Repository on GitHub**

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name:** `network-anomaly-detection`
   - **Description:** `ML system for detecting previously unseen network attacks using Isolation Forest, One-Class SVM, and Autoencoder`
   - **Visibility:** Public (recommended for portfolio) or Private
   - **❌ DO NOT** check "Initialize with README" (we already have one)
3. Click **"Create repository"**

---

### **Step 2: Push Your Code**

After creating the repository, run these commands in your terminal:

```bash
# Navigate to your project
cd /c/Users/OM\ SONI/OneDrive/Desktop/learndepth/network_anomaly_detection

# Add remote repository
git remote add origin https://github.com/omsoni2795-hash/network-anomaly-detection.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

### **Step 3: Authentication**

When prompted for credentials:

**Username:** omsoni2795-hash

**Password:** Use a Personal Access Token (NOT your GitHub password)

#### **How to get a Personal Access Token:**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name: `network-anomaly-detection`
4. Expiration: 90 days (or your preference)
5. Select scopes: ✅ **repo** (all checkboxes under repo)
6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)
8. Use this token as your password when pushing

---

## 📱 Alternative: Use GitHub CLI (Easier)

```bash
# Install GitHub CLI if you haven't: https://cli.github.com/

# Login (opens browser)
gh auth login

# Create repository and push
gh repo create network-anomaly-detection --public --source=. --push
```

---

## 🎯 After Pushing Successfully:

Your repository will be live at:
**https://github.com/omsoni2795-hash/network-anomaly-detection**

---

## 📊 What Will Be Visible:

### ✅ **On GitHub:**
- Complete source code (18 files)
- All documentation (README, guides, reports)
- requirements.txt for easy setup
- Professional project structure

### ❌ **NOT on GitHub (excluded by .gitignore):**
- Large CSV data files (5+ MB)
- Trained model files (.pkl, .keras)
- Python cache files

**Why?** Users can generate data and train models themselves using your code!

---

## 🌟 Make Your Repo Stand Out:

### **1. Add Topics (on GitHub):**
Click "⚙️ Settings" → "Topics" and add:
- `machine-learning`
- `anomaly-detection`
- `network-security`
- `cybersecurity`
- `python`
- `streamlit`
- `deep-learning`
- `intrusion-detection`

### **2. Add a Preview Image:**
- Take a screenshot of your Streamlit dashboard
- Upload to repo as `preview.png`
- GitHub will show it automatically

### **3. Pin the Repository:**
- Go to your profile: https://github.com/omsoni2795-hash
- Click "Customize your pins"
- Pin this project to showcase it!

---

## 🔧 Troubleshooting:

### **"remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/omsoni2795-hash/network-anomaly-detection.git
```

### **"Authentication failed"**
- Make sure you're using a Personal Access Token, not your password
- Token must have `repo` scope enabled

### **"fatal: couldn't find remote ref main"**
```bash
git branch -M main
git push -u origin main
```

---

## ✨ Ready to Go!

1. Create the repository on GitHub
2. Run the push commands above
3. Your ML project will be live!

**Your future repo URL:** https://github.com/omsoni2795-hash/network-anomaly-detection

🎉 **Good luck with your GitHub upload!**
