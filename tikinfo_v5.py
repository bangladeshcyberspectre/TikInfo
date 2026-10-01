#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────┐
# │         TikInfo Pro v5 — Bangladesh Cyber Spectre       │
# │         CEO: Ochena Gamer                               │
# │         pip install cloudscraper requests colorama      │
# └─────────────────────────────────────────────────────────┘

import sys, os, re, json, time, math
from datetime import datetime

# ── Dependency check ──────────────────────────────────────
def check_deps():
    missing = []
    for pkg in ["cloudscraper","requests","colorama"]:
        try: __import__(pkg)
        except ImportError: missing.append(pkg)
    if missing:
        print(f"\n[!] Missing: {', '.join(missing)}")
        print(f"[*] Run: pip install {' '.join(missing)}")
        sys.exit(1)
check_deps()

import cloudscraper, requests
from colorama import Fore, Style, init
init(autoreset=True)

R=Fore.RED; C=Fore.CYAN; G=Fore.GREEN; Y=Fore.YELLOW
W=Fore.WHITE; M=Fore.MAGENTA; B=Fore.BLUE
DIM=Style.DIM; RS=Style.RESET_ALL; BRT=Style.BRIGHT

def clear(): os.system("cls" if os.name=="nt" else "clear")

# ══════════════════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════════════════
def banner():
    clear()
    print(f"""
{R}{BRT}  ████████╗██╗██╗  ██╗    ██╗███╗   ██╗███████╗ ██████╗ {RS}
{R}{BRT}     ██║   ██║██║ ██╔╝    ██║████╗  ██║██╔════╝██╔═══██╗{RS}
{Y}{BRT}     ██║   ██║█████╔╝     ██║██╔██╗ ██║█████╗  ██║   ██║{RS}
{Y}{BRT}     ██║   ██║██╔═██╗     ██║██║╚██╗██║██╔══╝  ██║   ██║{RS}
{R}{BRT}     ██║   ██║██║  ██╗    ██║██║ ╚████║██║     ╚██████╔╝{RS}
{R}{BRT}     ╚═╝   ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ {RS}
{C}
  ╔═══════════════════════════════════════════════════════╗
  ║  {W}{BRT}TikTok OSINT + Ban Vulnerability Analyzer  v5{RS}  {C}  ║
  ╠═══════════════════════════════════════════════════════╣
  ║  {Y}Team   : Bangladesh Cyber Spectre{RS}                {C}  ║
  ║  {Y}CEO    : Ochena Gamer{RS}                            {C}  ║
  ║  {G}Status : ONLINE  ●  Smart Analysis Engine{RS}        {C}  ║
  ╚═══════════════════════════════════════════════════════╝{RS}
""")

# ══════════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════════
def section(t):
    w = 57
    print(f"\n{C}  ╔{'═'*w}╗")
    pad = w - len(t) - 2
    print(f"  ║  {W}{BRT}{t}{RS}{' '*max(0,pad)}{C}  ║")
    print(f"  ╚{'═'*w}╝{RS}")

def sub_section(t, color=C):
    pad = max(0, 50 - len(t))
    print(f"\n  {color}┌── {W}{BRT}{t}{RS}{color} {'─'*pad}┐{RS}")

def row(k, v, vc=W, kc=DIM):
    print(f"  {kc}  {k:<26}{RS}{vc}{v}{RS}")

def sep():
    print(f"  {DIM}  {'─'*54}{RS}")

def stp(m):  print(f"\n  {Y}  ⟳  {m}...{RS}", flush=True)
def ok_(m):  print(f"  {G}  [✓] {m}{RS}")
def fail_(m):print(f"  {R}  [✗] {m}{RS}")

def fmt(n):
    try: n=int(n or 0)
    except: return str(n)
    if n>=1_000_000_000: return f"{n/1e9:.2f}B"
    if n>=1_000_000:     return f"{n/1e6:.2f}M"
    if n>=1_000:         return f"{n/1e3:.1f}K"
    return str(n)

def fmt_ts(ts):
    try:    return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
    except: return "Unknown"

def get_age_days(ts):
    try:    return max(0,(int(time.time())-int(ts))//86400)
    except: return 0

def pbar(score, width=38):
    """Colored progress bar based on score."""
    score = max(0, min(100, score))
    filled = int(width * score / 100)
    empty  = width - filled
    if score >= 70:   fc = R
    elif score >= 45: fc = Y
    else:             fc = G
    return f"{fc}{'█'*filled}{DIM}{'░'*empty}{RS}"

# ══════════════════════════════════════════════════════════
#  SCRAPER
# ══════════════════════════════════════════════════════════
def make_scraper():
    sc = cloudscraper.create_scraper(
        browser={"browser":"chrome","platform":"android","mobile":True}
    )
    sc.headers.update({
        "Accept-Language":"en-US,en;q=0.9",
        "Referer":"https://www.tiktok.com/",
    })
    return sc

# ══════════════════════════════════════════════════════════
#  FETCH METHODS
# ══════════════════════════════════════════════════════════
def _safe_json(r):
    try:
        ct = r.headers.get("Content-Type","")
        if "json" not in ct and not r.text.strip().startswith("{"):
            return None
        return r.json()
    except: return None

def try_tikwm(un, sc):
    stp("TikWM API")
    try:
        r = sc.get("https://www.tikwm.com/api/user/info",
                   params={"unique_id":un}, timeout=20)
        d = _safe_json(r)
        if d and d.get("code")==0 and d.get("data"):
            ok_("TikWM success")
            return normalize(d["data"], un)
        fail_(f"TikWM: code={d.get('code') if d else 'no json'}")
    except Exception as e: fail_(f"TikWM: {e}")
    return None

def try_page(un, sc):
    stp("TikTok page scrape")
    try:
        sc.get("https://www.tiktok.com/", timeout=12)
        time.sleep(0.8)
        r = sc.get(f"https://www.tiktok.com/@{un}",
                   timeout=25, allow_redirects=True)
        if r.status_code == 404:
            fail_("User not found (404)"); return None
        if r.status_code != 200:
            fail_(f"HTTP {r.status_code}"); return None
        html = r.text
        for rx in [
            r'<script[^>]+id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>',
            r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
        ]:
            m = re.search(rx, html, re.DOTALL)
            if not m: continue
            try:
                obj = json.loads(m.group(1))
                info = (deep_find(obj,"userInfo") or
                        deep_find(obj,"UserModule") or
                        deep_find(obj,"user"))
                if info:
                    ok_("Page JSON success")
                    return normalize(info, un)
            except: continue
        d = regex_scrape(html, un)
        if d: ok_("Regex extract success"); return d
        fail_("Could not parse page data")
    except Exception as e: fail_(f"Page: {e}")
    return None

def try_oembed(un, sc):
    stp("oEmbed fallback")
    try:
        r = sc.get("https://www.tiktok.com/oembed",
                   params={"url":f"https://www.tiktok.com/@{un}/video/1"},
                   timeout=10)
        d = _safe_json(r)
        if d and d.get("author_name"):
            ok_("oEmbed partial")
            return _empty_profile(un, d.get("author_name",un),
                                  d.get("thumbnail_url",""))
    except Exception as e: fail_(f"oEmbed: {e}")
    return None

def fetch(un):
    sc = make_scraper()
    for fn in [try_tikwm, try_page, try_oembed]:
        try:
            res = fn(un, sc)
            if res: return res
        except Exception as e:
            fail_(f"{fn.__name__}: {e}")
    return None

# ══════════════════════════════════════════════════════════
#  NORMALIZE
# ══════════════════════════════════════════════════════════
def normalize(raw, un):
    if not isinstance(raw, dict): return None
    u = raw.get("user", raw)
    s = raw.get("stats", {})
    if not s:
        s = {k:u.get(k,0) for k in [
            "followerCount","followingCount","heartCount",
            "videoCount","diggCount","friendCount"]}
    def av(x):
        if isinstance(x,dict): return x.get("url_list",[""])[0]
        return str(x or "").replace("\\u002F","/").replace("\\/","/")
    bl = u.get("bioLink","")
    if isinstance(bl,dict): bl=bl.get("link","")
    return {
        "uniqueId":    u.get("uniqueId") or u.get("unique_id") or un,
        "nickname":    u.get("nickname",""),
        "id":          str(u.get("id","") or u.get("uid","") or ""),
        "signature":   u.get("signature",""),
        "verified":    bool(u.get("verified",False)),
        "private":     bool(u.get("secret",u.get("privateAccount",False))),
        "region":      u.get("region","Unknown"),
        "language":    u.get("language",""),
        "createTime":  int(u.get("createTime",0) or 0),
        "avatarUrl":   av(u.get("avatarThumb") or u.get("avatar_thumb","")),
        "openFavorite":bool(u.get("openFavorite",False)),
        "roomId":      str(u.get("roomId","") or ""),
        "ins_id":      u.get("ins_id","") or "",
        "twitter_id":  u.get("twitter_id","") or "",
        "youtube_id":  u.get("youtube_channel_id","") or "",
        "bioLink":     bl,
        "commerceUser":bool(u.get("commerceUserInfo") or
                            u.get("isEmbededSeller",False)),
        "following":   int(s.get("followingCount",0) or 0),
        "followers":   int(s.get("followerCount",0)  or 0),
        "hearts":      int(s.get("heartCount",0)     or 0),
        "videos":      int(s.get("videoCount",0)     or 0),
        "digg":        int(s.get("diggCount",0)      or 0),
        "friends":     int(s.get("friendCount",0)    or 0),
        "_partial":    False,
    }

def _empty_profile(un, name, avatar):
    p = {k:0 for k in ["following","followers","hearts","videos","digg","friends","createTime"]}
    p.update({"uniqueId":un,"nickname":name,"id":"","signature":"",
              "verified":False,"private":False,"region":"Unknown",
              "language":"","avatarUrl":avatar,"openFavorite":False,
              "roomId":"","ins_id":"","twitter_id":"","youtube_id":"",
              "bioLink":"","commerceUser":False,"_partial":True})
    return p

def regex_scrape(html, un):
    p={}
    rx={
        "id":        r'"id"\s*:\s*"(\d{6,})"',
        "nickname":  r'"nickname"\s*:\s*"([^"]{1,60})"',
        "signature": r'"signature"\s*:\s*"([^"]{0,300})"',
        "verified":  r'"verified"\s*:\s*(true|false)',
        "private":   r'"secret"\s*:\s*(true|false)',
        "region":    r'"region"\s*:\s*"([A-Z]{2})"',
        "following": r'"followingCount"\s*:\s*(\d+)',
        "followers": r'"followerCount"\s*:\s*(\d+)',
        "hearts":    r'"heartCount"\s*:\s*(\d+)',
        "videos":    r'"videoCount"\s*:\s*(\d+)',
        "digg":      r'"diggCount"\s*:\s*(\d+)',
        "friends":   r'"friendCount"\s*:\s*(\d+)',
        "createTime":r'"createTime"\s*:\s*(\d{9,10})',
        "roomId":    r'"roomId"\s*:\s*"?(\d+)"?',
        "ins_id":    r'"ins_id"\s*:\s*"([^"]{1,50})"',
        "twitter_id":r'"twitter_id"\s*:\s*"([^"]{1,50})"',
        "bioLink":   r'"link"\s*:\s*"(https?://[^"]+)"',
    }
    matched=0
    for k,pat in rx.items():
        m=re.search(pat,html)
        if m:
            v=m.group(1)
            if v in("true","false"): v=(v=="true")
            elif str(v).isdigit():   v=int(v)
            p[k]=v; matched+=1
    if matched<4: return None
    return {
        "uniqueId":un,"nickname":str(p.get("nickname",un)),
        "id":str(p.get("id","")),"signature":str(p.get("signature","")),
        "verified":p.get("verified",False),"private":p.get("private",False),
        "region":str(p.get("region","Unknown")),
        "language":"","createTime":int(p.get("createTime",0)),
        "avatarUrl":"","openFavorite":False,
        "roomId":str(p.get("roomId","")),
        "ins_id":str(p.get("ins_id","")),
        "twitter_id":str(p.get("twitter_id","")),
        "youtube_id":"","bioLink":str(p.get("bioLink","")),
        "commerceUser":False,
        "following":int(p.get("following",0)),
        "followers":int(p.get("followers",0)),
        "hearts":int(p.get("hearts",0)),
        "videos":int(p.get("videos",0)),
        "digg":int(p.get("digg",0)),
        "friends":int(p.get("friends",0)),
        "_partial":False,
    }

def deep_find(obj,key,d=0):
    if d>12: return None
    if isinstance(obj,dict):
        if key in obj and isinstance(obj[key],dict): return obj[key]
        for v in obj.values():
            r=deep_find(v,key,d+1)
            if r: return r
    elif isinstance(obj,list):
        for i in obj:
            r=deep_find(i,key,d+1)
            if r: return r
    return None

# ══════════════════════════════════════════════════════════
#  DISPLAY PROFILE
# ══════════════════════════════════════════════════════════
def show_profile(d, un):
    section("PROFILE INTELLIGENCE")

    ad = get_age_days(d.get("createTime",0))

    # ── Identity ─────────────────────────────────────────
    sub_section("IDENTITY", C)
    row("Username",     "@"+(d.get("uniqueId") or un),            C)
    row("Nickname",     d.get("nickname")   or "N/A",             W)
    row("User ID",      d.get("id")         or "Unknown",         Y)
    row("Bio",          d.get("signature")  or "(empty)",         DIM)
    row("Bio Link",     d.get("bioLink")    or "None",
        Y if d.get("bioLink") else DIM)
    row("Verified",
        "✓  YES — Blue Checkmark" if d.get("verified") else "✗  Not Verified",
        G if d.get("verified") else DIM)
    row("Account Type",
        "🔒  PRIVATE Account" if d.get("private") else "🌐  PUBLIC Account",
        R if d.get("private") else G)
    row("Commerce/Seller",
        "✓  Yes" if d.get("commerceUser") else "✗  No",
        Y if d.get("commerceUser") else DIM)
    row("Open Favorites",
        "✓  Yes (Public)" if d.get("openFavorite") else "✗  No (Private)",
        M if d.get("openFavorite") else DIM)
    row("Live Status",
        f"🔴  LIVE (Room: {d.get('roomId')})" if d.get("roomId") else "⚫  Not Live",
        R if d.get("roomId") else DIM)

    # ── Region ───────────────────────────────────────────
    sub_section("REGION & ACCOUNT INFO", C)
    row("Region",           d.get("region")   or "Unknown",       Y)
    row("Language",         d.get("language") or "Unknown",       W)
    row("Account Created",  fmt_ts(d.get("createTime",0)),        G)
    row("Account Age",      f"{ad} days" + (" 🆕 NEW" if ad<30 else ""), W)
    row("Profile URL",      f"tiktok.com/@{d.get('uniqueId',un)}",C)

    # ── Stats ────────────────────────────────────────────
    sub_section("STATISTICS", C)
    fol = d.get("followers",0)
    flw = d.get("following",0)
    hrt = d.get("hearts",0)
    vid = d.get("videos",0)
    dig = d.get("digg",0)
    fri = d.get("friends",0)

    row("Followers",        fmt(fol),  R)
    row("Following",        fmt(flw),  W)
    row("Total Likes",      fmt(hrt),  M)
    row("Videos Posted",    fmt(vid),  Y)
    row("Digg Count",       fmt(dig),  W)
    row("Friends",          fmt(fri),  C)

    # Derived stats
    if fol>0 and vid>0:
        avg_likes = hrt // max(vid,1)
        row("Avg Likes/Video", fmt(avg_likes), DIM)
    if fol>0 and flw>0:
        ratio = fol/max(flw,1)
        row("Follow Ratio",  f"{ratio:.1f}x  {'(Organic)' if ratio>1 else '(Follow-for-follow)'}",
            G if ratio>1 else Y)
    if fol>0 and hrt>0:
        eng = (hrt / max(fol,1)) * 100
        row("Engagement Rate", f"{eng:.1f}%  {'(High)' if eng>5 else '(Normal)' if eng>1 else '(Low)'}",
            G if eng>5 else Y if eng>1 else DIM)

    # ── Linked Accounts ──────────────────────────────────
    sub_section("LINKED ACCOUNTS", C)
    row("Instagram",  d.get("ins_id")     or "Not linked", G if d.get("ins_id")     else DIM)
    row("Twitter/X",  d.get("twitter_id") or "Not linked", G if d.get("twitter_id") else DIM)
    row("YouTube",    d.get("youtube_id") or "Not linked", G if d.get("youtube_id") else DIM)

    if d.get("_partial"):
        print(f"\n  {Y}  ⚠  Partial data — TikTok limited the API response{RS}")

    print(f"\n  {DIM}  Note: Email, Phone, DOB = Encrypted by TikTok. Not accessible externally.{RS}\n")

# ══════════════════════════════════════════════════════════
#  BAN ANALYSIS ENGINE v5
#  Based purely on ACCOUNT DATA — no fake keyword guessing
# ══════════════════════════════════════════════════════════

# All TikTok report categories
REPORT_TYPES = [
    "Spam",
    "Nudity and sexual activities",
    "Violent and graphic content",
    "Hate speech",
    "Harassment and bullying",
    "Illegal activities and regulated goods",
    "Dangerous acts and challenges",
    "Misinformation",
    "Minor safety",
    "Intellectual property violations",
    "Scam / Fraud",
]

def score_report_types(d):
    """
    Score each report type (0-100) based on actual account data.
    Returns list of (type, score, reasoning, tips) sorted by score.
    """
    fol   = int(d.get("followers",  0))
    flw   = int(d.get("following",  0))
    hrt   = int(d.get("hearts",     0))
    vid   = int(d.get("videos",     0))
    dig   = int(d.get("digg",       0))
    fri   = int(d.get("friends",    0))
    ct    = int(d.get("createTime", 0))
    ad    = get_age_days(ct)
    ver   = d.get("verified",     False)
    priv  = d.get("private",      False)
    comm  = d.get("commerceUser", False)
    live  = bool(d.get("roomId",""))
    ofav  = d.get("openFavorite", False)
    bio   = d.get("signature","") or ""
    reg   = d.get("region","") or ""
    blink = d.get("bioLink","") or ""

    avg_likes = hrt // max(vid,1) if vid > 0 else 0
    eng_rate  = (hrt / max(fol,1)) if fol > 0 else 0
    fol_ratio = fol / max(flw,1) if flw > 0 else 0
    # Abnormal: very high hearts vs followers (potential fake)
    heart_fol_ratio = hrt / max(fol,1) if fol > 0 else 0

    results = []

    # ── 1. SPAM ──────────────────────────────────────────
    spam_score = 20
    spam_reasons = []
    spam_tips = []

    if ad < 30:
        spam_score += 35
        spam_reasons.append(f"Account only {ad} days old — new accounts ban fast under Spam")
    elif ad < 90:
        spam_score += 15
        spam_reasons.append(f"Young account ({ad} days) — lower trust score")

    if fol > 1000 and vid == 0:
        spam_score += 30
        spam_reasons.append(f"Has {fmt(fol)} followers but ZERO videos — bot pattern")
    elif fol > 5000 and vid < 3:
        spam_score += 25
        spam_reasons.append(f"{fmt(fol)} followers with only {vid} videos — suspicious ratio")

    if heart_fol_ratio > 500 and fol > 100:
        spam_score += 20
        spam_reasons.append(f"Heart/follower ratio {heart_fol_ratio:.0f}x — artificial engagement")

    if flw > 5000 and fol < 100:
        spam_score += 20
        spam_reasons.append(f"Following {fmt(flw)} but only {fmt(fol)} followers — spam follow behavior")

    if not bio.strip():
        spam_score += 10
        spam_reasons.append("Empty bio — common bot/fake account indicator")

    if not ver:
        spam_score += 10
        spam_reasons.append("Non-verified accounts get banned faster under Spam category")

    spam_tips.append("Report as Spam > Fake engagement (if followers look bought)")
    spam_tips.append("Report as Spam > Posting spam content (if posting repetitive content)")
    if ad < 30:
        spam_tips.append("PRIORITY: Very new account — Spam reports hit hardest here")

    results.append({
        "type":    "Spam",
        "score":   min(100, spam_score),
        "reasons": spam_reasons,
        "tips":    spam_tips,
        "color":   R if spam_score>=70 else Y if spam_score>=40 else G,
    })

    # ── 2. NUDITY AND SEXUAL ACTIVITIES ──────────────────
    nudity_score = 5
    nudity_reasons = []
    nudity_tips = []

    if live:
        nudity_score += 40
        nudity_reasons.append("Currently LIVE — live sexual content gets banned within minutes")
        nudity_tips.append("Report the LIVE STREAM directly for fastest action")

    if ofav:
        nudity_score += 20
        nudity_reasons.append("Open favorites — exposes all liked content publicly")
        nudity_tips.append("If any favorited video is sexual, report for collecting inappropriate content")

    if fol > 50000 and eng_rate > 10:
        nudity_score += 15
        nudity_reasons.append("Very high engagement rate on large account — elevated visibility")

    if not nudity_reasons:
        nudity_reasons.append("No direct indicators from account data — need to check videos manually")
        nudity_tips.append("Browse their videos first — if sexual content found, report those videos")
        nudity_tips.append("Profile data alone does not confirm sexual content violation")

    results.append({
        "type":    "Nudity and sexual activities",
        "score":   min(100, nudity_score),
        "reasons": nudity_reasons,
        "tips":    nudity_tips,
        "color":   R if nudity_score>=70 else Y if nudity_score>=40 else DIM,
    })

    # ── 3. VIOLENT AND GRAPHIC CONTENT ───────────────────
    violence_score = 5
    violence_reasons = []
    violence_tips = []

    if live:
        violence_score += 35
        violence_reasons.append("Currently LIVE — live violent content = immediate ban")
        violence_tips.append("Report the live stream directly")

    violence_reasons.append("Cannot detect violent content from profile data alone")
    violence_tips.append("Check their recent videos — if graphic/violent content found, report those videos")
    violence_tips.append("Report video: Violence > Graphic violence or Real-world violence")

    results.append({
        "type":    "Violent and graphic content",
        "score":   min(100, violence_score),
        "reasons": violence_reasons,
        "tips":    violence_tips,
        "color":   R if violence_score>=70 else Y if violence_score>=40 else DIM,
    })

    # ── 4. HATE SPEECH ────────────────────────────────────
    hate_score = 5
    hate_reasons = []
    hate_tips = []

    if reg and reg not in ("US","GB","CA","AU","DE","FR","JP","KR"):
        hate_score += 10
        hate_reasons.append(f"Region: {reg} — some regions have higher hate speech report priority")

    hate_reasons.append("Hate speech cannot be detected from profile data — check video content")
    hate_tips.append("Watch recent videos for hateful language/imagery")
    hate_tips.append("Report as: Hate speech > Attacks based on protected attributes")
    hate_tips.append("Most effective if the account targets a specific group repeatedly")

    results.append({
        "type":    "Hate speech",
        "score":   min(100, hate_score),
        "reasons": hate_reasons,
        "tips":    hate_tips,
        "color":   Y if hate_score>=40 else DIM,
    })

    # ── 5. HARASSMENT AND BULLYING ────────────────────────
    harass_score = 10
    harass_reasons = []
    harass_tips = []

    if fol > 100000:
        harass_score += 15
        harass_reasons.append(f"Large account ({fmt(fol)} followers) — harassment from big accounts gets priority")
    if vid > 500:
        harass_score += 10
        harass_reasons.append(f"High video count ({vid}) — more chances of targeted harassment content")

    harass_reasons.append("Harassment evidence requires checking actual video/comment content")
    harass_tips.append("Most effective when combined with specific harassing video evidence")
    harass_tips.append("Report: Harassment > Threatening violence or Persistent harassment")

    results.append({
        "type":    "Harassment and bullying",
        "score":   min(100, harass_score),
        "reasons": harass_reasons,
        "tips":    harass_tips,
        "color":   Y if harass_score>=40 else DIM,
    })

    # ── 6. ILLEGAL ACTIVITIES ─────────────────────────────
    illegal_score = 10
    illegal_reasons = []
    illegal_tips = []

    if comm:
        illegal_score += 35
        illegal_reasons.append("Commerce/seller account — illegal goods = fast ban")
        illegal_tips.append("Report as: Illegal activities > Counterfeit or regulated goods")

    if blink:
        illegal_score += 25
        illegal_reasons.append(f"Has external bio link ({blink}) — could link to illegal marketplace")
        illegal_tips.append("Report as: Illegal activities > Promoting dangerous organizations")

    illegal_reasons.append("Check their videos/bio for drug sales, weapons, or counterfeit goods")
    illegal_tips.append("Illegal goods accounts get banned very fast when reported")

    results.append({
        "type":    "Illegal activities and regulated goods",
        "score":   min(100, illegal_score),
        "reasons": illegal_reasons,
        "tips":    illegal_tips,
        "color":   R if illegal_score>=70 else Y if illegal_score>=40 else DIM,
    })

    # ── 7. DANGEROUS ACTS ─────────────────────────────────
    danger_score = 5
    danger_reasons = []
    danger_tips = []

    if live:
        danger_score += 30
        danger_reasons.append("Currently LIVE — dangerous stunts on live = quick ban")

    danger_reasons.append("Dangerous act violations need video evidence — cannot detect from profile")
    danger_tips.append("Check videos for: unsafe stunts, dangerous challenges, self-harm")
    danger_tips.append("Report: Dangerous acts > Dangerous activity or Suicide/self-harm")

    results.append({
        "type":    "Dangerous acts and challenges",
        "score":   min(100, danger_score),
        "reasons": danger_reasons,
        "tips":    danger_tips,
        "color":   Y if danger_score>=40 else DIM,
    })

    # ── 8. MISINFORMATION ─────────────────────────────────
    misinfo_score = 10
    misinfo_reasons = []
    misinfo_tips = []

    if ver:
        misinfo_score += 20
        misinfo_reasons.append("Verified account — Misinformation is the strongest report type for verified accounts")
        misinfo_tips.append("PRIORITY for verified accounts: Misinformation > Health/safety misinformation")
    if fol > 100000:
        misinfo_score += 20
        misinfo_reasons.append(f"Large reach ({fmt(fol)} followers) — TikTok prioritizes misinfo on big accounts")

    misinfo_reasons.append("Need to identify specific misleading content in their videos")
    misinfo_tips.append("Most effective against news/health/political content creators")
    misinfo_tips.append("Report: Misinformation > False information about health, safety, or elections")

    results.append({
        "type":    "Misinformation",
        "score":   min(100, misinfo_score),
        "reasons": misinfo_reasons,
        "tips":    misinfo_tips,
        "color":   Y if misinfo_score>=40 else DIM,
    })

    # ── 9. MINOR SAFETY ───────────────────────────────────
    minor_score = 5
    minor_reasons = []
    minor_tips = []

    minor_reasons.append("Minor safety violations require specific evidence — check content")
    minor_tips.append("If account appears to be run by or targeting minors inappropriately")
    minor_tips.append("Report: Minor safety > Sexual exploitation or Grooming")
    minor_tips.append("Highest severity — TikTok responds fastest to minor safety reports")

    results.append({
        "type":    "Minor safety",
        "score":   min(100, minor_score),
        "reasons": minor_reasons,
        "tips":    minor_tips,
        "color":   DIM,
    })

    # ── 10. SCAM / FRAUD ──────────────────────────────────
    scam_score = 10
    scam_reasons = []
    scam_tips = []

    if comm:
        scam_score += 30
        scam_reasons.append("Commerce account — scam/fraud report highly applicable")
        scam_tips.append("Report as: Illegal activities > Scam or Deceptive practices")

    if blink:
        scam_score += 25
        scam_reasons.append("Bio link present — potential scam redirect link")
        scam_tips.append("If bio link leads to scam/phishing site, report immediately")

    if fol > 1000 and vid < 5 and hrt > fol * 50:
        scam_score += 20
        scam_reasons.append("Suspicious follower pattern suggests purchased/fake account (reselling)")

    scam_reasons.append("Check for giveaway scams, impersonation, fake investment content")
    scam_tips.append("Report: Scam > Fake giveaways or Fraudulent financial advice")

    results.append({
        "type":    "Scam / Fraud",
        "score":   min(100, scam_score),
        "reasons": scam_reasons,
        "tips":    scam_tips,
        "color":   R if scam_score>=70 else Y if scam_score>=40 else DIM,
    })

    # ── 11. IP (Intellectual Property) ───────────────────
    ip_score = 5
    ip_reasons = []
    ip_tips = []
    ip_reasons.append("Cannot detect IP violations from profile data")
    ip_tips.append("If account reposts others' content without credit, report as IP violation")
    ip_tips.append("Report: Intellectual property > Copyright infringement")

    results.append({
        "type":    "Intellectual property violations",
        "score":   min(100, ip_score),
        "reasons": ip_reasons,
        "tips":    ip_tips,
        "color":   DIM,
    })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def overall_ban_score(report_scores, d):
    """Calculate overall ban difficulty score."""
    ad  = get_age_days(d.get("createTime",0))
    ver = d.get("verified",False)
    top_score = report_scores[0]["score"] if report_scores else 0

    base = top_score * 0.6

    # Age modifier
    if ad < 30:   base += 25
    elif ad < 90: base += 10

    # Verified modifier
    if ver: base -= 15
    else:   base += 10

    # Live modifier
    if d.get("roomId"): base += 20

    return int(min(100, max(0, base)))

# ══════════════════════════════════════════════════════════
#  DISPLAY VULNERABILITY REPORT
# ══════════════════════════════════════════════════════════
def show_analysis(report_scores, d, un):
    section("BAN VULNERABILITY ANALYSIS")

    ban_score = overall_ban_score(report_scores, d)
    bar       = pbar(ban_score)
    sc        = R if ban_score>=70 else Y if ban_score>=45 else G
    ad        = get_age_days(d.get("createTime",0))

    # Overall score
    sub_section("OVERALL BAN DIFFICULTY SCORE", C)
    print(f"\n  [{bar}] {sc}{BRT} {ban_score}% Bannable{RS}")
    if ban_score >= 80:
        print(f"\n  {R}{BRT}  ⚠  VERY HIGH — This account is highly vulnerable to coordinated reports{RS}")
    elif ban_score >= 60:
        print(f"\n  {R}  ⚠  HIGH — Coordinated reports likely to result in ban{RS}")
    elif ban_score >= 40:
        print(f"\n  {Y}  ⚡  MODERATE — Multiple reports needed, focus on best category{RS}")
    else:
        print(f"\n  {G}  ●  LOW — Account appears clean. Focus on video content violations.{RS}")

    # Quick summary
    sub_section("ACCOUNT WEAKNESS SUMMARY", Y)
    ver = d.get("verified",False)
    row("Verified Status",
        "✓ Verified (Harder to ban)" if ver else "✗ Not Verified (Easier to ban)",
        DIM if ver else R)
    row("Account Age",
        f"{ad} days {'🔴 VERY VULNERABLE' if ad<30 else '🟡 Vulnerable' if ad<90 else '🟢 Established'}",
        R if ad<30 else Y if ad<90 else G)
    row("Currently Live",
        "🔴 YES — Report NOW for fastest ban" if d.get("roomId") else "No",
        R if d.get("roomId") else DIM)
    row("Bio Link",
        f"YES: {d.get('bioLink')} (violation risk)" if d.get("bioLink") else "None",
        Y if d.get("bioLink") else DIM)
    row("Commerce Account",
        "YES — Higher fraud/scam risk" if d.get("commerceUser") else "No",
        Y if d.get("commerceUser") else DIM)
    row("Open Favorites",
        "YES — Content exposure" if d.get("openFavorite") else "No",
        M if d.get("openFavorite") else DIM)
    if int(d.get("followers",0)) > 1000 and int(d.get("videos",0)) < 3:
        row("Follower Pattern",
            f"⚠ Suspicious: {fmt(d.get('followers',0))} followers, {d.get('videos',0)} videos",
            R)

    # All report types
    section("ALL REPORT TYPES — EFFECTIVENESS ANALYSIS")
    print(f"  {DIM}  Each type scored based on actual account data patterns.{RS}\n")

    for i, rpt in enumerate(report_scores, 1):
        sc_val  = rpt["score"]
        color   = rpt["color"]
        rtype   = rpt["type"]
        reasons = rpt["reasons"]
        tips    = rpt["tips"]

        # Effectiveness label
        if sc_val >= 70:   eff = f"{R}{BRT}HIGHLY EFFECTIVE{RS}"
        elif sc_val >= 50: eff = f"{Y}{BRT}EFFECTIVE{RS}"
        elif sc_val >= 30: eff = f"{Y}MODERATE{RS}"
        else:              eff = f"{DIM}LOW / NEEDS VIDEO EVIDENCE{RS}"

        mini_bar = pbar(sc_val, width=20)

        print(f"\n  {color}{BRT}[{i:02d}] {rtype}{RS}")
        print(f"  {DIM}       Score  : {RS}[{mini_bar}] {color}{BRT}{sc_val}%{RS}  {eff}")
        print(f"  {DIM}       Why    :{RS}")
        for r in reasons[:3]:
            print(f"  {DIM}         • {RS}{W}{r}{RS}")
        print(f"  {DIM}       How to report:{RS}")
        for t in tips[:3]:
            print(f"  {DIM}         → {RS}{C}{t}{RS}")

    # Best strategy
    best = report_scores[0]
    second = report_scores[1] if len(report_scores) > 1 else None

    section("OPTIMAL ATTACK STRATEGY")

    needed = "5-8"   if ban_score>=80 else \
             "10-15" if ban_score>=60 else \
             "15-25" if ban_score>=40 else "25+"
    window = "15 min" if ban_score>=80 else \
             "30 min" if ban_score>=60 else "1 hour"
    expected = "Permanent ban within 12-24h"   if ban_score>=75 else \
               "Suspension review within 48h"   if ban_score>=55 else \
               "Review triggered within 72h"    if ban_score>=35 else \
               "May not result in ban without video evidence"

    print(f"""
  {G}  Primary Report Type  : {Y}{BRT}{best['type']}{RS}
  {G}  Accounts Needed      : {W}{needed} different TikTok accounts{RS}
  {G}  All Within           : {W}{window} window for max impact{RS}
  {G}  Expected Result      : {W}{expected}{RS}
""")

    if second and second["score"] >= 30:
        print(f"  {C}  Backup Report Type   : {Y}{second['type']} ({second['score']}%){RS}")

    print(f"""
  {C}  STEP-BY-STEP:{RS}
  {W}  1. Open: {C}tiktok.com/@{un}{RS}
  {W}  2. Tap ··· (top right) → Report{RS}
  {W}  3. Select: {Y}{BRT}{best['type']}{RS}
  {W}  4. Complete + submit from {G}{needed}{W} accounts within {G}{window}{RS}
  {W}  5. Also report 2-3 recent videos (same category){RS}
  {W}  6. Different devices + different IPs = higher weight{RS}
  {W}  7. Accounts with longer history = more trust weight{RS}
  {W}  8. Check status after {G}24-48 hours{RS}
""")

    if d.get("roomId"):
        print(f"  {R}{BRT}  ⚡ ACCOUNT IS LIVE — REPORT NOW FOR FASTEST BAN ⚡{RS}")
        print(f"  {R}     Go to tiktok.com/@{un} and report the LIVE stream directly{RS}\n")

# ══════════════════════════════════════════════════════════
#  SAVE REPORT
# ══════════════════════════════════════════════════════════
def save_report(un, d, report_scores):
    ts    = int(time.time())
    fname = f"tikinfo_{un}_{ts}.txt"
    ban_s = overall_ban_score(report_scores, d)
    with open(fname,"w",encoding="utf-8") as f:
        f.write("╔═══════════════════════════════════════════════════╗\n")
        f.write("║  TikInfo Pro v5 — Bangladesh Cyber Spectre        ║\n")
        f.write("║  CEO: Ochena Gamer                                ║\n")
        f.write("╚═══════════════════════════════════════════════════╝\n\n")
        f.write(f"Target     : @{un}\n")
        f.write(f"Scanned    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Ban Score  : {ban_s}%\n")
        f.write("═"*55 + "\n\n")

        f.write("PROFILE\n" + "─"*40 + "\n")
        for k,v in [
            ("Username",  "@"+(d.get("uniqueId") or un)),
            ("Nickname",  d.get("nickname","N/A")),
            ("User ID",   d.get("id","Unknown")),
            ("Bio",       d.get("signature","(empty)")),
            ("Verified",  "Yes" if d.get("verified") else "No"),
            ("Type",      "Private" if d.get("private") else "Public"),
            ("Region",    d.get("region","Unknown")),
            ("Created",   fmt_ts(d.get("createTime",0))),
            ("Age",       f"{get_age_days(d.get('createTime',0))} days"),
            ("Followers", fmt(d.get("followers",0))),
            ("Following", fmt(d.get("following",0))),
            ("Likes",     fmt(d.get("hearts",0))),
            ("Videos",    fmt(d.get("videos",0))),
            ("Instagram", d.get("ins_id","Not linked")),
            ("Twitter",   d.get("twitter_id","Not linked")),
            ("YouTube",   d.get("youtube_id","Not linked")),
            ("Bio Link",  d.get("bioLink","None")),
            ("Live",      d.get("roomId","Not Live")),
        ]:
            f.write(f"  {k:<16}: {v}\n")

        f.write("\n\nREPORT TYPE ANALYSIS\n" + "─"*40 + "\n")
        for rpt in report_scores:
            f.write(f"\n[{rpt['score']:3d}%] {rpt['type']}\n")
            for r in rpt["reasons"]:
                f.write(f"  • {r}\n")
            for t in rpt["tips"]:
                f.write(f"  → {t}\n")

    return fname

# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════
def main():
    banner()
    print(f"  {C}  Install: {W}pip install cloudscraper requests colorama{RS}\n")

    while True:
        section("ENTER TARGET USERNAME")
        try:
            raw = input(f"\n  {C}  TikTok username (q = quit): {W}@{RS}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if raw.lower() in ("q","quit","exit",""):
            print(f"\n  {G}  Bangladesh Cyber Spectre — Session Closed.{RS}\n")
            break

        un = raw.lstrip("@").strip()
        if not un:
            print(f"  {R}  Please enter a username!{RS}")
            continue

        print(f"\n  {Y}  Scanning @{un} ...{RS}\n")
        data = fetch(un)

        if not data:
            print(f"\n  {R}  [✗] Could not fetch profile for @{un}{RS}")
            print(f"""
  {Y}  Troubleshoot:{RS}
  {W}  1. Check username spelling (exact, case-sensitive){RS}
  {W}  2. Account must be PUBLIC{RS}
  {W}  3. Check internet connection{RS}
  {W}  4. Wait 60s and retry{RS}
  {W}  5. Update: {C}pip install --upgrade cloudscraper{RS}
""")
            try:    input(f"  {DIM}  Press Enter to continue...{RS}")
            except: break
            continue

        # Profile display
        show_profile(data, un)

        # Ban analysis
        report_scores = score_report_types(data)
        show_analysis(report_scores, data, un)

        # Save option
        try:
            if input(f"  {C}  Save full report to file? [y/N]: {W}").strip().lower()=="y":
                fname = save_report(un, data, report_scores)
                print(f"  {G}  [✓] Saved: {fname}{RS}")
        except (KeyboardInterrupt, EOFError):
            pass

        # Continue
        try:
            if input(f"\n  {C}  Scan another account? [Y/n]: {W}").strip().lower()=="n":
                print(f"\n  {G}  Bangladesh Cyber Spectre — CEO: Ochena Gamer{RS}\n")
                break
        except (KeyboardInterrupt, EOFError):
            break

        banner()

if __name__ == "__main__":
    main()
