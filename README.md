# 🎨 Automatic JSON Data Updater

This repository automatically updates `hello.json` with wallpaper data based on time zones using GitHub Actions.

## 🕒 Time-Based Data Switching

The system automatically switches between two data sources:

### 🇮🇳 **FREE Data** (Indian Time)
- **When**: Indian Standard Time (IST) 6:00 AM - 8:00 PM
- **Source**: `Free.json`
- **Content**: All free wallpapers (17,462 items)

### 🇺🇸 **PAID Data** (USA Time) 
- **When**: USA Eastern Time (EST) 9:00 AM - 9:00 PM
- **Source**: `paid.json`
- **Content**: Premium wallpapers with multiple categories (17,462 items)

### 📅 **Priority Logic**
1. If current time falls within Indian business hours → **FREE**
2. Else if current time falls within USA business hours → **PAID**
3. Otherwise → **FREE** (default)

## 🤖 Automation

### GitHub Actions Workflow
- **Runs**: Every 2 hours automatically
- **File**: `.github/workflows/auto-update-json.yml`
- **Actions**:
  1. Checks current time zones
  2. Determines appropriate data source
  3. Updates `DATA_SOURCE` in `update_hello.py`
  4. Runs the update script
  5. Commits changes automatically

### Manual Control
You can also manually control the data source:

1. Edit `update_hello.py`
2. Change line 17: `DATA_SOURCE = "free"` or `DATA_SOURCE = "paid"`
3. Run: `python3 update_hello.py`

## 📁 Files

- `hello.json` - Main JSON file that gets updated
- `Free.json` - Source data for free wallpapers
- `paid.json` - Source data for paid wallpapers  
- `update_hello.py` - Python script that handles the updating
- `.github/workflows/auto-update-json.yml` - GitHub Actions workflow

## 🔄 How It Works

1. **Time Detection**: Workflow calculates current IST and EST times
2. **Source Selection**: Chooses appropriate data source based on time
3. **Change Detection**: Only updates if data source needs to change
4. **File Update**: Modifies Python script and runs it
5. **Auto Commit**: Commits changes with descriptive message
6. **Cleanup**: Removes backup files to keep repo clean

## 🚀 Getting Started

1. Push this repository to GitHub
2. The workflow will automatically start running every 2 hours
3. Check the "Actions" tab to see workflow runs
4. Your `hello.json` will be automatically updated based on time zones!

## 📊 Monitoring

- Check the **Actions** tab in GitHub to see workflow runs
- Each run shows a summary of what was updated and why
- Commit messages include timestamp and reason for change

---

**Note**: The system prioritizes Indian time over USA time when both conditions are met. 