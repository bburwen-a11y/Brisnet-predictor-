# Brisnet-predictor-# BRISNET Past Performance Predictor

A mobile-friendly horse race predictor that runs entirely in your browser. Upload your BRISNET CSV past performances and get instant rankings, best plays, equipment changes, and workout analysis.

## Live Demo

**Open on your iPhone:**
```
https://yourusername.github.io/brisnet-predictor
```

Then tap **Share → Add to Home Screen** for app-like experience.

---

## How to Use

### 1. Get BRISNET Data
- Go to [brisnet.com](https://www.brisnet.com)
- Log in and purchase Ultimate PPs for your track
- Download the **CSV** format (not PDF)

### 2. Upload to Predictor
- Open the predictor (from your home screen or browser)
- Tap **"Upload BRISNET CSV"**
- Select your file from Files or iCloud

### 3. Read the Analysis
The predictor automatically shows:

| Tab | What It Shows |
|-----|---------------|
| **Races** | All races with ranked horses (1st = best) |
| **Best** | Only the strongest betting edges |
| **Changes** | Blinkers on/off, jockey switches, Lasix, layoffs, scratches |
| **Works** | Workout quality rankings (bullet = good, yellow = avg, red = poor) |

### 4. Export Results
- Tap **CSV** to download spreadsheet
- Tap **PDF** to download printable race cards

---

## Features

- **Auto-ranking** — Horses scored 0-100 based on form, class, workouts
- **Best play detection** — Races with strongest edges highlighted in green
- **Head-to-head** — Shows which horses have beaten rivals before
- **Equipment alerts** — Blinkers added, Lasix on/off, weight changes
- **Jockey analysis** — Win % and in-the-money % for each rider
- **Scratch watch** — Flags horses scratched within 45 days
- **Surface switches** — Dirt-to-turf and turf-to-dirt angles flagged

---

## Supported File Formats

| Source | Format | How to Export |
|--------|--------|---------------|
| **BRISNET** | CSV | Ultimate PPs → Download CSV |
| **Equibase** | CSV | Charts → Export CSV |
| **DRF** | CSV | Formulator → Export to Excel |

**Note:** PDF files are NOT supported. Export as CSV for best results.

---

## iPhone Setup (One Time)

1. Open Safari
2. Go to `https://yourusername.github.io/brisnet-predictor`
3. Tap **Share** (square with arrow up)
4. Scroll down, tap **"Add to Home Screen"**
5. Name it **"BRISNET PP"**
6. Tap **Add**

Now it works like a native app — tap the icon and upload your CSV files instantly.

---

## Data Privacy

**100% private.** All processing happens in your browser. No data is uploaded to any server. Your BRISNET files never leave your device.

---

## Troubleshooting

**"File won't upload"**
- Make sure it's a `.csv` file (not PDF)
- Try saving the file to "On My iPhone" first

**"Add to Home Screen" not showing**
- Make sure you open the GitHub Pages link in Safari (not Chrome)
- Scroll down in the Share menu — it's below the fold

**"Predictor won't load"**
- Check your internet connection (first load only)
- After first load, it works offline

---

## Tech Stack

- Pure HTML/CSS/JavaScript — no frameworks
- Runs entirely client-side — no backend
- Responsive design — works on iPhone, iPad, Android, desktop
- Base64 data URLs for offline capability

---

## License

MIT License — free to use, modify, and share.

---

**Built for handicappers who want fast, mobile-friendly race analysis.**
