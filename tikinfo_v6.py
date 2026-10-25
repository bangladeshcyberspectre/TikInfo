#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────┐
# │         TikInfo Pro v6 — Bangladesh Cyber Spectre       │
# │         CEO: Ochena Gamer                               │
# └─────────────────────────────────────────────────────────┘

import sys, os, re, json, time, math
from datetime import datetime

# ── Python version check ───────────────────────────────────
if sys.version_info[0] < 3:
    print("\n[!] Python 3 required. You are running Python 2.")
    print("[*] In Termux run:\n")
    print("    pkg install python")
    print("    python tikinfo_v6.py\n")
    print("[!] Do NOT use 'python2' or 'pip' — use 'python' and 'pip' after")
    print("    running: pkg install python\n")
    sys.exit(1)

# ── Auto-install dependencies ─────────────────────────────
import subprocess

def _install(pkg):
    """Install using the same python executable that is running this script."""
    print(f"[*] Installing {pkg}...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"[✓] {pkg} installed")
        return True
    except Exception as e:
        print(f"[✗] Failed to install {pkg}: {e}")
        return False

PKGS = ["cloudscraper", "requests", "colorama"]
for _pkg in PKGS:
    try:
        __import__(_pkg)
    except ImportError:
        if not _install(_pkg):
            print(f"\n[!] Could not auto-install {_pkg}.")
            print(f"    Manually run: python -m pip install {_pkg}")
            sys.exit(1)

# re-import after install
try:
    __import__("cloudscraper")
    __import__("requests")
    __import__("colorama")
except ImportError as e:
    print(f"[!] Import still failing after install: {e}")
    print("    Try: pkg install python && python -m pip install cloudscraper requests colorama")
    sys.exit(1)

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
  ║  {W}{BRT}TikTok OSINT + Ban Vulnerability Analyzer  v6{RS}  {C}  ║
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
#  BAN ANALYSIS ENGINE v6
#  Dynamic scoring — real account data, no fake fixed values
# ══════════════════════════════════════════════════════════

def _extract_signals(d):
    """Extract all signals from account data."""
    fol  = int(d.get("followers",  0))
    flw  = int(d.get("following",  0))
    hrt  = int(d.get("hearts",     0))
    vid  = int(d.get("videos",     0))
    dig  = int(d.get("digg",       0))
    fri  = int(d.get("friends",    0))
    ct   = int(d.get("createTime", 0))
    ad   = get_age_days(ct)
    ver  = d.get("verified",     False)
    priv = d.get("private",      False)
    comm = d.get("commerceUser", False)
    live = bool(d.get("roomId",""))
    ofav = d.get("openFavorite", False)
    bio  = (d.get("signature","") or "").strip()
    reg  = (d.get("region","")    or "").upper()
    bl   = (d.get("bioLink","")   or "").strip()
    ins  = bool(d.get("ins_id",""))
    tw   = bool(d.get("twitter_id",""))
    yt   = bool(d.get("youtube_id",""))

    # Derived metrics
    avg_lpv    = hrt  // max(vid, 1) if vid   > 0 else 0
    eng_rate   = (hrt  / max(fol, 1)) * 100 if fol > 0 else 0
    fol_ratio  = fol   / max(flw, 1) if flw   > 0 else 0
    hf_ratio   = hrt   / max(fol, 1) if fol   > 0 else 0    # hearts per follower
    vf_ratio   = vid   / max(fol, 1) if fol   > 0 else 0    # videos per follower

    # Account type classification
    is_new        = ad < 30
    is_young      = 30 <= ad < 90
    is_established= ad >= 180
    is_bot_pattern= (fol > 1000  and vid == 0) or \
                    (flw > 10000 and fol < 200) or \
                    (hf_ratio > 1000 and fol > 100)
    is_seller     = comm or bool(bl)
    is_suspicious = (fol > 5000 and vid < 3) or \
                    (hf_ratio > 500 and fol > 100)
    is_influencer = fol >= 100000
    is_mega       = fol >= 1_000_000
    empty_bio     = len(bio) < 3
    linked        = ins or tw or yt
    high_eng      = eng_rate > 15
    low_eng       = eng_rate < 1 and fol > 1000

    return dict(
        fol=fol, flw=flw, hrt=hrt, vid=vid, dig=dig, fri=fri,
        ad=ad, ver=ver, priv=priv, comm=comm, live=live, ofav=ofav,
        bio=bio, reg=reg, bl=bl, ins=ins, tw=tw, yt=yt,
        avg_lpv=avg_lpv, eng_rate=eng_rate, fol_ratio=fol_ratio,
        hf_ratio=hf_ratio, vf_ratio=vf_ratio,
        is_new=is_new, is_young=is_young, is_established=is_established,
        is_bot_pattern=is_bot_pattern, is_seller=is_seller,
        is_suspicious=is_suspicious, is_influencer=is_influencer,
        is_mega=is_mega, empty_bio=empty_bio, linked=linked,
        high_eng=high_eng, low_eng=low_eng,
    )

def score_report_types(d):
    s = _extract_signals(d)
    results = []

    # ── 1. SPAM ──────────────────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["is_bot_pattern"]:
        sc += 55
        if s["fol"] > 1000 and s["vid"] == 0:
            reasons.append(f"⚠ {fmt(s['fol'])} followers, ZERO videos — clear bot/purchased account")
        elif s["flw"] > 10000 and s["fol"] < 200:
            reasons.append(f"⚠ Following {fmt(s['flw'])} people but only {fmt(s['fol'])} followers — spam bot pattern")
        if s["hf_ratio"] > 1000:
            reasons.append(f"⚠ Hearts/follower ratio: {s['hf_ratio']:.0f}x — artificial engagement detected")

    if s["is_new"]:
        sc += 35
        reasons.append(f"⚠ Account only {s['ad']} days old — new accounts are 3x more vulnerable to Spam reports")
    elif s["is_young"]:
        sc += 18
        reasons.append(f"Account age {s['ad']} days — young accounts have lower trust score")

    if s["is_suspicious"] and not s["is_bot_pattern"]:
        sc += 25
        reasons.append(f"Suspicious ratio: {fmt(s['fol'])} followers with only {s['vid']} videos")

    if s["empty_bio"]:
        sc += 12
        reasons.append("Empty bio — bot/fake account strong indicator")

    if s["low_eng"]:
        sc += 18
        reasons.append(f"Extremely low engagement ({s['eng_rate']:.1f}%) on {fmt(s['fol'])} followers — bought followers")

    if s["fol"] > 500 and s["flw"] > s["fol"] * 10:
        sc += 20
        reasons.append(f"Mass follow behavior: following {fmt(s['flw'])} for {fmt(s['fol'])} followers")

    if not s["ver"]:
        sc += 8
        reasons.append("Unverified account — lower trust weight in TikTok moderation system")

    if not reasons:
        reasons.append("No strong spam signals detected from profile data")
        sc = max(sc, 10)

    tips.append("Report: Spam → Fake engagement OR Spam content")
    if s["is_new"]:     tips.append("🔥 PRIORITY: New account — Spam report most effective right now")
    if s["is_bot_pattern"]: tips.append("🔥 Report: Spam → Purchasing followers/likes/comments")
    tips.append("Report 3-5 of their videos as Spam simultaneously for higher weight")

    results.append({"type":"Spam","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else G})

    # ── 2. SCAM / FRAUD ──────────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["comm"]:
        sc += 45
        reasons.append(f"Commerce/seller account — TikTok Shop violations = fast ban")
    if s["bl"]:
        sc += 30
        reasons.append(f"External link in bio: {s['bl'][:50]} — potential scam redirect")
    if s["fol"] > 1000 and s["vid"] < 5 and s["hrt"] > s["fol"] * 50:
        sc += 25
        reasons.append("Suspicious pattern: high hearts, few videos — fake/resold account")
    if s["is_influencer"] and s["empty_bio"]:
        sc += 15
        reasons.append(f"Large account ({fmt(s['fol'])} followers) with empty bio — impersonation risk")
    if s["high_eng"] and s["is_suspicious"]:
        sc += 20
        reasons.append("Abnormally high engagement on suspicious account — fake engagement scam")

    if not reasons:
        reasons.append("No scam signals in profile — check video content for scam ads")
        sc = max(sc, 5)

    if s["comm"]: tips.append("🔥 Report: Illegal activities → Scam or Deceptive practices")
    if s["bl"]:   tips.append("🔥 Report: Scam → Phishing or Fraudulent links")
    tips.append("Check videos for: fake giveaways, investment scams, impersonation")
    tips.append("Report as: Illegal activities → Scam / Deceptive practices")

    results.append({"type":"Scam / Fraud","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 3. HARASSMENT AND BULLYING ────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["is_influencer"]:
        sc += 25
        reasons.append(f"Large account ({fmt(s['fol'])} followers) — harassment from big accounts gets priority review")
    if s["vid"] > 200:
        sc += 15
        reasons.append(f"High video count ({s['vid']}) — more chances of targeting specific users")
    if s["high_eng"] and s["is_influencer"]:
        sc += 15
        reasons.append("High engagement + large reach = harassment amplified to many people")
    if s["live"]:
        sc += 20
        reasons.append("Currently LIVE — live harassment/bullying = immediate report option")

    if not reasons:
        reasons.append("No harassment signals in profile data — check comment sections and video content")
        sc = max(sc, 8)

    tips.append("Report: Harassment and bullying → Threatening violence or Unwanted contact")
    tips.append("Check if they made videos targeting specific individuals")
    if s["live"]: tips.append("🔥 Report the LIVE stream directly for fastest action")
    tips.append("Screenshot evidence of harassment before reporting")

    results.append({"type":"Harassment and bullying","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 4. ILLEGAL ACTIVITIES ─────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["comm"] and s["bl"]:
        sc += 55
        reasons.append("Commerce account + bio link — likely selling regulated/illegal products")
    elif s["comm"]:
        sc += 35
        reasons.append("Commerce/seller account — check for counterfeit goods or illegal items")
    elif s["bl"]:
        sc += 25
        reasons.append(f"Bio link: {s['bl'][:50]} — could direct to illegal marketplace")

    if s["reg"] in ("BD","PK","IN","NG","ID"):
        sc += 10
        reasons.append(f"Region {s['reg']} — higher frequency of counterfeit/illegal goods accounts")

    if not reasons:
        reasons.append("No illegal activity signals in profile data")
        sc = max(sc, 5)

    if s["comm"]: tips.append("🔥 Report: Illegal activities → Counterfeit goods / Regulated items")
    tips.append("Check video content for: drugs, weapons, counterfeit goods")
    tips.append("Report: Illegal activities → Gambling or Tobacco/alcohol to minors")

    results.append({"type":"Illegal activities and regulated goods","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 5. MISINFORMATION ─────────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["ver"] and s["is_influencer"]:
        sc += 40
        reasons.append(f"Verified influencer ({fmt(s['fol'])} followers) — misinfo from verified accounts gets priority")
    elif s["is_influencer"]:
        sc += 25
        reasons.append(f"Large reach ({fmt(s['fol'])} followers) — TikTok prioritizes misinfo on big accounts")
    if s["is_mega"]:
        sc += 20
        reasons.append(f"Mega account (1M+ followers) — misinfo can spread fast, TikTok acts quickly")
    if s["high_eng"]:
        sc += 15
        reasons.append("High engagement rate — misleading content reaches more people faster")
    if s["reg"] in ("BD","IN","PK","NG","PH"):
        sc += 10
        reasons.append(f"Region {s['reg']} — election/health misinfo frequently reported here")

    if not reasons:
        reasons.append("Misinfo cannot be confirmed from profile data alone — check video content")
        sc = max(sc, 8)

    if s["ver"]: tips.append("🔥 PRIORITY for verified accounts: Misinformation → False health/safety info")
    tips.append("Report: Misinformation → False information about health, elections, or safety")
    tips.append("Most effective on news/health/political content creators")

    results.append({"type":"Misinformation","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 6. NUDITY / SEXUAL ACTIVITIES ────────────────────
    sc = 0
    reasons, tips = [], []

    if s["live"]:
        sc += 65
        reasons.append("🔴 Currently LIVE — live sexual content = ban within minutes")
        tips.append("🔥 REPORT THE LIVE STREAM NOW — Go to profile → tap Live → Report")
    if s["ofav"]:
        sc += 20
        reasons.append("Open favorites — publicly liked content visible, check for inappropriate videos")
    if s["high_eng"] and s["fol"] > 50000:
        sc += 15
        reasons.append("High engagement on large account — adult content spreads fast")
    if s["empty_bio"] and s["is_suspicious"]:
        sc += 10
        reasons.append("Suspicious account with empty bio — common pattern for adult content accounts")

    if not reasons:
        reasons.append("Cannot confirm sexual content from profile data — check videos manually")
        sc = max(sc, 5)
        tips.append("Browse recent videos — if sexual content found, report those specific videos")

    tips.append("Report: Nudity and sexual activities → Sexual content or Nudity")
    tips.append("Always report the specific violating VIDEO, not just the profile")

    results.append({"type":"Nudity and sexual activities","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 7. HATE SPEECH ────────────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["is_influencer"]:
        sc += 20
        reasons.append(f"Large account ({fmt(s['fol'])} followers) — hate speech amplified to many people")
    if s["reg"] in ("BD","IN","PK","MM","NG"):
        sc += 15
        reasons.append(f"Region {s['reg']} — hate speech reports frequently prioritized in this region")
    if s["high_eng"]:
        sc += 10
        reasons.append("High engagement — hateful content reaching wider audience")
    if s["vid"] > 100:
        sc += 8
        reasons.append(f"{s['vid']} videos posted — higher chance of hate speech content in library")

    if not reasons:
        reasons.append("Hate speech cannot be confirmed from profile data — check video content")
        sc = max(sc, 5)

    tips.append("Report: Hate speech → Attacks based on religion, ethnicity, or race")
    tips.append("Watch recent videos for hateful language, slurs, or targeted attacks")
    tips.append("Most effective when reporting specific videos with clear hate speech")

    results.append({"type":"Hate speech","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 8. VIOLENT / GRAPHIC CONTENT ─────────────────────
    sc = 0
    reasons, tips = [], []

    if s["live"]:
        sc += 50
        reasons.append("🔴 Currently LIVE — real-time violent content = immediate ban trigger")
        tips.append("🔥 Report the LIVE directly: Profile → Live → Report → Violent content")
    if s["vid"] > 100:
        sc += 10
        reasons.append(f"{s['vid']} videos — larger content library increases chances of violent content")

    if not reasons:
        reasons.append("Violent content cannot be detected from profile data alone")
        sc = max(sc, 5)
        tips.append("Check recent videos — if graphic/violent content found, report those videos")

    tips.append("Report: Violent content → Graphic violence or Real-world violence")
    tips.append("Report specific videos for more impact than just the account")

    results.append({"type":"Violent and graphic content","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 9. DANGEROUS ACTS ─────────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["live"]:
        sc += 45
        reasons.append("🔴 Currently LIVE — dangerous stunts live = immediate ban risk")
    if s["vid"] > 50 and s["high_eng"]:
        sc += 15
        reasons.append("High-engagement content creator — dangerous challenge content spreads fast")

    if not reasons:
        reasons.append("Dangerous acts require video evidence — cannot detect from profile")
        sc = max(sc, 5)
        tips.append("Check videos for dangerous challenges, unsafe stunts, or self-harm content")

    tips.append("Report: Dangerous acts → Dangerous activity or Challenges")
    tips.append("Report: Dangerous acts → Suicide or self-harm content")
    if s["live"]: tips.append("🔥 Report the LIVE stream directly")

    results.append({"type":"Dangerous acts and challenges","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 10. MINOR SAFETY ──────────────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["fol"] > 0 and s["vid"] > 0:
        sc += 8
    if s["live"]:
        sc += 20
        reasons.append("Currently LIVE — live minor safety violations = fastest TikTok response")

    if not reasons:
        reasons.append("Minor safety requires specific evidence — cannot confirm from profile data")
        sc = max(sc, 5)

    tips.append("HIGHEST SEVERITY: TikTok responds fastest to minor safety reports")
    tips.append("Report: Minor safety → Sexual exploitation or Grooming")
    tips.append("Only report if you have CLEAR evidence — false reports are penalized")
    if s["live"]: tips.append("🔥 If minor safety violation is happening LIVE — report immediately")

    results.append({"type":"Minor safety","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":R if sc>=65 else Y if sc>=40 else DIM})

    # ── 11. INTELLECTUAL PROPERTY ─────────────────────────
    sc = 0
    reasons, tips = [], []

    if s["vid"] > 50:
        sc += 15
        reasons.append(f"{s['vid']} videos — higher probability of reposted/stolen content")
    if s["is_influencer"] and not s["linked"]:
        sc += 10
        reasons.append(f"Large account ({fmt(s['fol'])} followers) with no linked original platforms")

    if not reasons:
        reasons.append("IP violations require checking specific video content")
        sc = max(sc, 5)

    tips.append("Report: Intellectual property → Copyright infringement")
    tips.append("If they repost others' videos without credit, report those specific videos")
    tips.append("Original creators can submit DMCA directly to TikTok for faster action")

    results.append({"type":"Intellectual property violations","score":min(100,sc),"reasons":reasons,"tips":tips,
                    "color":Y if sc>=40 else DIM})

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def overall_ban_score(report_scores, d):
    """
    Dynamic ban score calculation.
    Uses weighted combination of actual account signals.
    Result varies significantly per account — not fixed.
    """
    s = _extract_signals(d)

    # Start from top report score (weighted 55%)
    top = report_scores[0]["score"] if report_scores else 0
    avg_top3 = sum(r["score"] for r in report_scores[:3]) / 3 if len(report_scores) >= 3 else top
    base = (top * 0.55) + (avg_top3 * 0.25)

    # ── Account age factor ────────────────────────────────
    if s["ad"] == 0:                base += 5   # unknown age
    elif s["ad"] < 7:               base += 30  # brand new
    elif s["ad"] < 30:              base += 22  # very new
    elif s["ad"] < 90:              base += 12  # young
    elif s["ad"] < 180:             base += 4   # growing
    elif s["is_established"]:       base -= 8   # established, harder

    # ── Verification factor ───────────────────────────────
    if s["ver"]:                    base -= 18  # verified = much harder
    else:                           base += 8

    # ── Follower size factor ──────────────────────────────
    if s["fol"] < 100:              base += 15  # tiny = easy
    elif s["fol"] < 1000:           base += 8
    elif s["fol"] < 10000:          base += 3
    elif s["fol"] < 100000:         base += 0
    elif s["fol"] < 1_000_000:      base -= 8   # big = TikTok protects
    else:                           base -= 18  # mega = very hard

    # ── Bot/suspicious pattern ────────────────────────────
    if s["is_bot_pattern"]:         base += 20
    if s["is_suspicious"]:          base += 12
    if s["empty_bio"]:              base += 6
    if s["low_eng"]:                base += 10

    # ── Live bonus ────────────────────────────────────────
    if s["live"]:                   base += 22

    # ── Commerce/seller ───────────────────────────────────
    if s["comm"]:                   base += 8
    if s["bl"]:                     base += 6

    # ── Engagement anomaly ────────────────────────────────
    if s["hf_ratio"] > 1000:        base += 15
    elif s["hf_ratio"] > 500:       base += 8

    # ── Private account ───────────────────────────────────
    if s["priv"]:                   base -= 10  # private = TikTok hides

    # ── Linked accounts ───────────────────────────────────
    if s["linked"]:                 base -= 5   # legit creator

    return int(min(99, max(3, base)))

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

    # Split into applicable and low-signal
    applicable  = [r for r in report_scores if r["score"] >= 20]
    low_signal  = [r for r in report_scores if r["score"] <  20]

    print(f"  {G}  Showing {len(applicable)} applicable + {len(low_signal)} low-signal report types.{RS}\n")

    for i, rpt in enumerate(applicable, 1):
        sc_val  = rpt["score"]
        color   = rpt["color"]
        rtype   = rpt["type"]
        reasons = rpt["reasons"]
        tips    = rpt["tips"]

        if sc_val >= 70:   eff = f"{R}{BRT}⚡ HIGHLY EFFECTIVE{RS}"
        elif sc_val >= 50: eff = f"{Y}{BRT}✓ EFFECTIVE{RS}"
        elif sc_val >= 35: eff = f"{Y}~ MODERATE{RS}"
        else:              eff = f"{DIM}○ LOW — Needs video evidence{RS}"

        mini_bar = pbar(sc_val, width=22)

        print(f"\n  {color}{BRT}[{i:02d}] {rtype}{RS}")
        print(f"       [{mini_bar}] {color}{BRT}{sc_val}%{RS}  {eff}")
        print(f"  {DIM}       Signals:{RS}")
        for r in reasons[:3]:
            print(f"  {DIM}         • {RS}{W}{r}{RS}")
        print(f"  {DIM}       How to report:{RS}")
        for t in tips[:3]:
            print(f"  {DIM}         → {RS}{C}{t}{RS}")

    if low_signal:
        print(f"\n  {DIM}  ── Low signal (< 20%) — needs manual video check ──{RS}")
        for rpt in low_signal:
            print(f"  {DIM}  [{rpt['score']:2d}%] {rpt['type']}{RS}")

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
