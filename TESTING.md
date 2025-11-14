# Quick Test Guide

## Will it work right now?

**Almost!** There are a few quick setup steps, then yes it will work.

## Quick Setup Checklist

1. ✅ **Create `.env` file:**
```bash
cd backend
cp env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

2. ✅ **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. ✅ **Create storage directory:**
```bash
mkdir -p storage/worlds
```

4. ✅ **Run the server:**
```bash
python main.py
```

## Test It Works

### Test 1: Check server starts
```bash
curl http://localhost:8000/
```
Should return: `{"name":"Roblox World Generator API",...}`

### Test 2: Test generation (with API key)
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A small village",
    "world_size": 256,
    "complexity": "low"
  }'
```

Should return a job_id.

### Test 3: Check status
```bash
# Use the job_id from Test 2
curl http://localhost:8000/api/status/YOUR_JOB_ID
```

## Potential Issues & Fixes

### Issue 1: "OPENAI_API_KEY not found"
**Fix:** Make sure `.env` file exists in `backend/` directory with:
```
OPENAI_API_KEY=sk-your-actual-key
```

### Issue 2: "Module not found"
**Fix:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue 3: GPT-4 API error
**Fix:** 
- Check your API key is valid
- Check you have GPT-4 access (not just GPT-3.5)
- The code will automatically fall back to keyword-based parsing if GPT fails

### Issue 4: Storage directory error
**Fix:** Create it manually:
```bash
mkdir -p backend/storage/worlds
```

## What Works Without GPT API?

Even without GPT API, the fallback parser will work for basic prompts:
- "mountain" → generates mountain terrain
- "castle" → generates castle structure
- "village" → generates houses

But GPT-4 gives much better results!

## Expected Behavior

1. **With valid GPT API key:**
   - ✅ Full AI-powered world generation
   - ✅ Complex prompt understanding
   - ✅ Smart structure placement

2. **Without GPT API key (or if it fails):**
   - ✅ Fallback keyword-based generation
   - ✅ Basic terrain types work
   - ✅ Simple structures work
   - ⚠️ Less intelligent placement

## Ready to Go!

Once you have the `.env` file with your API key, it should work immediately! 🚀

