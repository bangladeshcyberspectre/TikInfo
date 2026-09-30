#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════╗
# ║       TikInfo Pro v3                             ║
# ║       Bangladesh Cyber Spectre                   ║
# ║       CEO: Ochena Gamer                          ║
# ╚══════════════════════════════════════════════════╝
# pip install cloudscraper requests colorama

import sys, os, re, json, time
from datetime import datetime

# ── dependency check ──────────────────────────────────
def check_deps():
    missing = []
    for pkg in ["cloudscraper","requests","colorama"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"\n[!] Missing: {', '.join(missing)}")
        print(f"[*] Run: pip install {' '.join(missing)}")
        sys.exit(1)

check_deps()

import cloudscraper
import requests
from colorama import Fore, Style, init
init(autoreset=True)

R  = Fore.RED;   C  = Fore.CYAN
G  = Fore.GREEN; Y  = Fore.YELLOW
W  = Fore.WHITE; M  = Fore.MAGENTA
DIM = Style.DIM; RS = Style.RESET_ALL
B   = Style.BRIGHT

def clear(): os.system("cls" if os.name=="nt" else "clear")

def banner():
    clear()
    print(f"""
{R}{B}████████╗██╗██╗  ██╗    ██╗███╗   ██╗███████╗ ██████╗
╚══██╔══╝██║██║ ██╔╝    ██║████╗  ██║██╔════╝██╔═══██╗
   ██║   ██║█████╔╝     ██║██╔██╗ ██║█████╗  ██║   ██║
   ██║   ██║██╔═██╗     ██║██║╚██╗██║██╔══╝  ██║   ██║
   ██║   ██║██║  ██╗    ██║██║ ╚████║██║     ╚██████╔╝
   ╚═╝   ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝{RS}
{C}  ┌────────────────────────────────────────────────┐
  │ {W}{B}TikTok OSINT + Ban Vulnerability Analyzer  {RS}{C} │
  │ {Y}Team : Bangladesh Cyber Spectre             {C} │
  │ {Y}CEO  : Ochena Gamer                        {C} │
  │ {G}v3   : Cloudflare Bypass Edition           {C} │
  └────────────────────────────────────────────────┘{RS}
""")

def section(t):
    print(f"\n{C}  {'═'*50}")
    print(f"  ║  {W}{B}{t:<46}{RS}{C}  ║")
    print(f"  {'═'*50}{RS}")

def row(k, v, color=W):
    print(f"  {DIM}{k:<22}{RS} {color}{v}{RS}")

def divider(lbl=""):
    if lbl:
        print(f"\n  {C}── {lbl} {'─'*max(0,42-len(lbl))}{RS}")
    else:
        print(f"  {DIM}{'─'*50}{RS}")

def step(m): print(f"  {Y}⟳  {m}...{RS}", flush=True)
def ok(m):   print(f"  {G}[✓] {m}{RS}")
def fail(m): print(f"  {R}[✗] {m}{RS}")

def fmt(n):
    try: n=int(n or 0)
    except: return str(n)
    if n>=1_000_000: return f"{n/1e6:.1f}M"
    if n>=1_000:     return f"{n/1e3:.1f}K"
    return str(n)

def fmt_ts(ts):
    try: return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
    except: return "Unknown"

# ══════════════════════════════════════════════════════
#  SCRAPER SESSION (bypasses TikTok bot detection)
# ══════════════════════════════════════════════════════
def make_scraper():
    sc = cloudscraper.create_scraper(
        browser={"browser":"chrome","platform":"android","mobile":True}
    )
    sc.headers.update({
        "Accept-Language": "en-US,en;q=0.9",
        "Referer":         "https://www.tiktok.com/",
    })
    return sc

# ══════════════════════════════════════════════════════
#  FETCH METHODS
# ══════════════════════════════════════════════════════

def try_tikwm(un, sc):
    """TikWM free API -- most reliable endpoint."""
    step("TikWM API")
    try:
        r = sc.get(
            "https://www.tikwm.com/api/user/info",
            params={"unique_id": un},
            timeout=20
        )
        if r.status_code != 200:
            fail(f"TikWM HTTP {r.status_code}"); return None

        # safe parse
        try: d = r.json()
        except Exception:
            fail("TikWM: response not JSON"); return None

        if d.get("code") == 0 and d.get("data"):
            ok("TikWM success")
            return normalize(d["data"], un)

        fail(f"TikWM code={d.get('code')} msg={d.get('msg','')}")
    except Exception as e:
        fail(f"TikWM: {type(e).__name__}: {e}")
    return None


def try_ssstik(un, sc):
    """ssstik.io scrape -- independent from TikTok API."""
    step("ssstik.io")
    try:
        r = sc.get(
            "https://ssstik.io/en",
            params={"url": f"https://www.tiktok.com/@{un}"},
            timeout=20
        )
        html = r.text
        # extract any profile data present
        data = regex_scrape(html, un)
        if data:
            ok("ssstik partial data")
            return data
        fail("ssstik: no parseable data")
    except Exception as e:
        fail(f"ssstik: {e}")
    return None


def try_tiktok_page(un, sc):
    """Scrape TikTok profile page directly with bypass."""
    step("TikTok page (cloudscraper)")
    try:
        # warm up
        sc.get("https://www.tiktok.com/", timeout=15)
        time.sleep(1)

        r = sc.get(
            f"https://www.tiktok.com/@{un}",
            timeout=25,
            allow_redirects=True
        )

        if r.status_code == 404:
            fail("404 -- user not found"); return None
        if r.status_code != 200:
            fail(f"HTTP {r.status_code}"); return None

        html = r.text

        # try embedded JSON blocks
        for rx in [
            r'<script[^>]+id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>',
            r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
            r'window\[.SIGI_STATE.\]\s*=\s*(\{.+?\})(?:\s*;|</script)',
        ]:
            m = re.search(rx, html, re.DOTALL)
            if not m: continue
            try:
                obj  = json.loads(m.group(1))
                info = deep_find(obj, "userInfo") or \
                       deep_find(obj, "UserModule") or \
                       deep_find(obj, "user")
                if info:
                    ok("TikTok page JSON success")
                    return normalize(info, un)
            except Exception:
                continue

        # regex fallback
        data = regex_scrape(html, un)
        if data:
            ok("TikTok page regex success")
            return data

        fail("page: could not extract data")
    except Exception as e:
        fail(f"page: {type(e).__name__}: {e}")
    return None


def try_rapidapi(un, sc):
    """Free RapidAPI TikTok endpoints (no key needed for some)."""
    step("RapidAPI free tier")
    urls = [
        f"https://tiktok-download-without-watermark.p.rapidapi.com/analysis?url=https://www.tiktok.com/@{un}",
        f"https://tiktok-scraper7.p.rapidapi.com/user/info?unique_id={un}",
    ]
    for url in urls:
        try:
            r = sc.get(url, timeout=12)
            try: d = r.json()
            except: continue
            info = deep_find(d, "userInfo") or \
                   deep_find(d, "user")     or \
                   d.get("data")
            if info:
                ok("RapidAPI success")
                return normalize(info, un)
        except Exception:
            continue
    fail("RapidAPI: no result")
    return None


def try_oembed(un, sc):
    """TikTok oEmbed -- minimal but works."""
    step("oEmbed (minimal)")
    try:
        # Need a valid video URL; use a generic profile URL trick
        r = sc.get(
            "https://www.tiktok.com/oembed",
            params={"url": f"https://www.tiktok.com/@{un}/video/1"},
            timeout=10
        )
        try: d = r.json()
        except: fail("oEmbed not JSON"); return None

        if d.get("author_name") or d.get("author_url"):
            ok("oEmbed partial")
            return {
                "uniqueId":  un,
                "nickname":  d.get("author_name", un),
                "id":        "",
                "signature": "",
                "verified":  False,
                "private":   False,
                "region":    "Unknown",
                "language":  "Unknown",
                "createTime":0,
                "avatarUrl": d.get("thumbnail_url",""),
                "openFavorite": False,
                "roomId":    "",
                "ins_id":    "",
                "twitter_id":"",
                "youtube_id":"",
                "bioLink":   "",
                "commerceUser": False,
                "following": 0,"followers":0,
                "hearts":    0,"videos":   0,
                "digg":      0,"friends":  0,
                "_partial":  True,
            }
        fail("oEmbed: no author data")
    except Exception as e:
        fail(f"oEmbed: {e}")
    return None

# ══════════════════════════════════════════════════════
#  NORMALIZER
# ══════════════════════════════════════════════════════
def normalize(raw, un):
    if not isinstance(raw, dict): return None

    u = raw.get("user", raw)
    s = raw.get("stats", {})

    if not s:
        s = {k: u.get(k, u.get(k.replace("Count","_count"), 0))
             for k in ["followerCount","followingCount",
                       "heartCount","videoCount","diggCount","friendCount"]}

    def av(x):
        if isinstance(x, dict): return x.get("url_list",[""])[0]
        return str(x or "").replace("\\u002F","/").replace("\\/","/")

    bl = u.get("bioLink","")
    if isinstance(bl, dict): bl = bl.get("link","")

    return {
        "uniqueId":     u.get("uniqueId") or u.get("unique_id") or un,
        "nickname":     u.get("nickname",""),
        "id":           str(u.get("id","") or u.get("uid","") or ""),
        "signature":    u.get("signature",""),
        "verified":     bool(u.get("verified",False)),
        "private":      bool(u.get("secret",u.get("privateAccount",False))),
        "region":       u.get("region","Unknown"),
        "language":     u.get("language",""),
        "createTime":   int(u.get("createTime",0) or 0),
        "avatarUrl":    av(u.get("avatarThumb") or u.get("avatar_thumb","")),
        "openFavorite": bool(u.get("openFavorite",False)),
        "roomId":       str(u.get("roomId","") or ""),
        "ins_id":       u.get("ins_id","") or "",
        "twitter_id":   u.get("twitter_id","") or "",
        "youtube_id":   u.get("youtube_channel_id","") or "",
        "bioLink":      bl,
        "commerceUser": bool(u.get("commerceUserInfo") or u.get("isEmbededSeller",False)),
        "following":    int(s.get("followingCount",0) or 0),
        "followers":    int(s.get("followerCount",0)  or 0),
        "hearts":       int(s.get("heartCount",0)     or 0),
        "videos":       int(s.get("videoCount",0)     or 0),
        "digg":         int(s.get("diggCount",0)      or 0),
        "friends":      int(s.get("friendCount",0)    or 0),
        "_partial":     False,
    }

def regex_scrape(html, un):
    p = {}
    rx = {
        "id":        [r'"id"\s*:\s*"(\d{6,})"'],
        "nickname":  [r'"nickname"\s*:\s*"([^"]{1,60})"'],
        "signature": [r'"signature"\s*:\s*"([^"]{0,300})"'],
        "verified":  [r'"verified"\s*:\s*(true|false)'],
        "private":   [r'"secret"\s*:\s*(true|false)'],
        "region":    [r'"region"\s*:\s*"([A-Z]{2})"'],
        "following": [r'"followingCount"\s*:\s*(\d+)'],
        "followers": [r'"followerCount"\s*:\s*(\d+)'],
        "hearts":    [r'"heartCount"\s*:\s*(\d+)'],
        "videos":    [r'"videoCount"\s*:\s*(\d+)'],
        "createTime":[r'"createTime"\s*:\s*(\d{9,10})'],
        "language":  [r'"language"\s*:\s*"([a-z\-]{2,10})"'],
        "roomId":    [r'"roomId"\s*:\s*"?(\d+)"?'],
        "ins_id":    [r'"ins_id"\s*:\s*"([^"]+)"'],
        "twitter_id":[r'"twitter_id"\s*:\s*"([^"]+)"'],
    }
    matched = 0
    for key, patterns in rx.items():
        for pat in patterns:
            m = re.search(pat, html)
            if m:
                v = m.group(1)
                if v in ("true","false"): v = (v=="true")
                elif str(v).isdigit():    v = int(v)
                p[key] = v; matched += 1; break

    if matched < 4: return None

    return {
        "uniqueId":    un,
        "nickname":    str(p.get("nickname", un)),
        "id":          str(p.get("id","")),
        "signature":   str(p.get("signature","")),
        "verified":    p.get("verified",False),
        "private":     p.get("private",False),
        "region":      str(p.get("region","Unknown")),
        "language":    str(p.get("language","")),
        "createTime":  int(p.get("createTime",0)),
        "avatarUrl":   "",
        "openFavorite":False,
        "roomId":      str(p.get("roomId","")),
        "ins_id":      str(p.get("ins_id","")),
        "twitter_id":  str(p.get("twitter_id","")),
        "youtube_id":  "",
        "bioLink":     "",
        "commerceUser":False,
        "following":   int(p.get("following",0)),
        "followers":   int(p.get("followers",0)),
        "hearts":      int(p.get("hearts",0)),
        "videos":      int(p.get("videos",0)),
        "digg":        0,"friends":0,"_partial":False,
    }

def deep_find(obj, key, d=0):
    if d>12: return None
    if isinstance(obj, dict):
        if key in obj and isinstance(obj[key],(dict,)):
            return obj[key]
        for v in obj.values():
            r = deep_find(v, key, d+1)
            if r: return r
    elif isinstance(obj, list):
        for i in obj:
            r = deep_find(i, key, d+1)
            if r: return r
    return None

# ══════════════════════════════════════════════════════
#  MAIN FETCH
# ══════════════════════════════════════════════════════
def fetch(un):
    sc = make_scraper()
    for fn in [try_tikwm, try_tiktok_page, try_rapidapi, try_oembed]:
        try:
            res = fn(un, sc)
            if res: return res
        except Exception as e:
            fail(f"{fn.__name__} crashed: {e}")
    return None

# ══════════════════════════════════════════════════════
#  DISPLAY
# ══════════════════════════════════════════════════════
def show_profile(d, un):
    section("PROFILE INTELLIGENCE")

    divider("IDENTITY")
    row("Username",     "@"+(d.get("uniqueId") or un),          C)
    row("Nickname",     d.get("nickname") or "-",                W)
    row("User ID",      d.get("id") or "Unknown",               Y)
    row("Bio",          d.get("signature") or "(empty)",         DIM)
    row("Verified",
        "✓ YES" if d.get("verified") else "✗ No",
        G if d.get("verified") else DIM)
    row("Account",
        "🔒 Private" if d.get("private") else "🌐 Public",
        R if d.get("private") else G)
    row("Commerce",
        "Yes (Seller)" if d.get("commerceUser") else "No",
        Y if d.get("commerceUser") else DIM)

    divider("REGION & DATES")
    row("Region",     d.get("region") or "Unknown",                           Y)
    row("Language",   d.get("language") or "Unknown",                         W)
    row("Created",    fmt_ts(d.get("createTime",0)),                          G)
    row("Profile URL",f"tiktok.com/@{d.get('uniqueId',un)}",                 C)
    row("Bio Link",   d.get("bioLink") or "None",
        Y if d.get("bioLink") else DIM)

    divider("STATISTICS")
    row("Followers",   fmt(d.get("followers",0)),  R)
    row("Following",   fmt(d.get("following",0)),  W)
    row("Total Likes", fmt(d.get("hearts",0)),     M)
    row("Videos",      fmt(d.get("videos",0)),     Y)
    row("Digg Count",  fmt(d.get("digg",0)),       W)
    row("Friends",     fmt(d.get("friends",0)),    C)

    divider("LINKED ACCOUNTS")
    row("Instagram",  d.get("ins_id")     or "Not linked", G if d.get("ins_id")     else DIM)
    row("Twitter/X",  d.get("twitter_id") or "Not linked", G if d.get("twitter_id") else DIM)
    row("YouTube",    d.get("youtube_id") or "Not linked", G if d.get("youtube_id") else DIM)
    row("Live Room",  d.get("roomId")     or "Not Live",   R if d.get("roomId")     else DIM)

    if d.get("_partial"):
        print(f"\n  {Y}⚠  Partial data -- full fetch blocked by TikTok{RS}")

    print(f"\n  {DIM}Email / Phone / DOB : TikTok encrypted -- not accessible{RS}")

# ══════════════════════════════════════════════════════
#  BAN ANALYSIS
# ══════════════════════════════════════════════════════
def analyze(d):
    vulns = []
    now   = int(time.time())
    ct    = int(d.get("createTime",0) or 0)
    age   = (now-ct)//86400 if ct else 9999
    fol   = int(d.get("followers",0))
    vid   = int(d.get("videos",0))
    hrt   = int(d.get("hearts",0))

    def add(sev,color,w,title,rtype,note):
        vulns.append(dict(sev=sev,color=color,w=w,
                          title=title,rtype=rtype,note=note))

    # Age
    if ct and age < 30:
        add("CRITICAL",R,10,f"Brand New Account ({age} days)","Spam",
            f"Only {age} days old. 5-8 Spam reports from different accounts within 20 minutes = near-certain ban. Easiest target.")
    elif ct and age < 90:
        add("HIGH",Y,7,f"Young Account ({age} days)","Spam",
            f"{age} days old. 10 coordinated Spam reports recommended.")

    # Verified
    if not d.get("verified"):
        add("HIGH",Y,8,"Non-Verified (Easy Target)","Spam",
            "Non-verified accounts ban 3x faster. 8-10 Spam reports within 1 hour = auto-suspension trigger.")
    else:
        add("LOW",C,2,"Verified (Harder Target)","Misinformation",
            "Verified needs 20+ reports. Use Misinformation > Health/Safety category.")

    # Bio link
    if d.get("bioLink"):
        add("HIGH",Y,8,"External Link in Bio",
            "Illegal activities and regulated goods",
            f"Bio: {d['bioLink']} -- Report as Illegal activities > Promoting dangerous organizations.")

    # Follower/content ratio
    if fol > 5000 and vid < 5:
        add("HIGH",Y,7,f"Suspicious Ratio ({fmt(fol)} followers, {vid} videos)",
            "Spam","Bought followers detected. Report as Spam > Fake engagement.")

    # Commerce
    if d.get("commerceUser"):
        add("MEDIUM",M,6,"Commerce/Seller Account",
            "Illegal activities and regulated goods",
            "Commerce violations = faster bans. Report as Illegal activities > Counterfeit goods.")

    # Open favorites
    if d.get("openFavorite"):
        add("MEDIUM",M,5,"Open Favorites",
            "Nudity and sexual activities",
            "Open favorites list exposes collected content. Report for inappropriate content collection.")

    # Region
    reg = d.get("region","")
    if reg and reg not in ("BD","US","GB","IN","PK","CA","AU","DE","FR"):
        add("MEDIUM",M,4,f"Foreign Region ({reg})",
            "Hate speech",
            f"Region {reg}. Cross-border reports prioritized. Use Hate speech > Protected attributes.")

    # Live
    if d.get("roomId"):
        add("HIGH",Y,9,f"CURRENTLY LIVE (Room: {d['roomId']})",
            "Nudity and sexual activities",
            "Account is LIVE RIGHT NOW. Live reports = fastest possible ban (minutes not hours). Report immediately.")

    # Empty bio
    if not str(d.get("signature","")).strip():
        add("LOW",C,3,"Empty Bio (Bot indicator)","Spam",
            "Empty bio strengthens Spam report as bot/fake account evidence.")

    # Engagement anomaly
    if fol > 0 and hrt > fol * 200:
        add("MEDIUM",M,5,"Abnormal Engagement Ratio","Spam",
            f"Heart/follower ratio abnormally high = artificial engagement. Supports Spam report.")

    vulns.sort(key=lambda x: x["w"], reverse=True)
    return vulns

def show_vulns(vulns, un):
    section(f"BAN VULNERABILITY — @{un}")

    if not vulns:
        print(f"  {G}No significant vulnerabilities{RS}"); return

    score  = min(100, sum(v["w"] for v in vulns) * 4)
    sc     = R if score>=70 else Y if score>=40 else G
    filled = int(40*score/100)
    bar    = f"{sc}{'█'*filled}{DIM}{'░'*(40-filled)}{RS}"

    print(f"\n  {W}Ban Score:{RS}")
    print(f"  [{bar}] {sc}{B}{score}%{RS}")
    print(f"  {sc}{'⚠ HIGH — will ban with coordinated reports' if score>=70 else '⚡ MODERATE' if score>=40 else '● LOW'}{RS}")
    print()

    for i,v in enumerate(vulns,1):
        c = v["color"]
        print(f"\n  {c}{B}[{i}] {v['title']}{RS}")
        print(f"  {DIM}Severity  :{RS} {c}{v['sev']}{RS}")
        print(f"  {DIM}Report as :{RS} {Y}{v['rtype']}{RS}")
        print(f"  {DIM}How       :{RS} {W}{v['note']}{RS}")

    divider("ATTACK PLAN")
    best   = vulns[0]["rtype"]
    needed = "5-8" if score>=80 else "10-15" if score>=60 else "20+"
    window = "15 min" if score>=80 else "30 min"

    print(f"""
  {G}Best Report Type   : {Y}{B}{best}{RS}
  {G}Accounts Needed    : {W}{needed} TikTok accounts{RS}
  {G}Time Window        : {W}All within {window}{RS}
  {G}Expected Result    : {W}{'Auto-ban 12-24h' if score>=70 else 'Review triggered 48h'}{RS}

  {C}STEPS:{RS}
  {W}1. Open: tiktok.com/@{un}{RS}
  {W}2. Tap ··· → Report → {Y}{best}{RS}
  {W}3. Repeat from {G}{needed}{W} accounts in {G}{window}{RS}
  {W}4. Also report 2-3 of their recent videos{RS}
  {W}5. Check after {G}24-48 hours{RS}
""")

# ══════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════
def save(un, d, vulns):
    fname = f"tikinfo_{un}_{int(time.time())}.txt"
    with open(fname,"w",encoding="utf-8") as f:
        f.write("TikInfo — Bangladesh Cyber Spectre\n")
        f.write(f"CEO: Ochena Gamer | Target: @{un}\n")
        f.write(f"Date: {datetime.now()}\n{'═'*50}\n\n")
        for k,v in d.items():
            if k.startswith("_"): continue
            if k == "createTime": v = fmt_ts(v)
            elif k in ("followers","following","hearts","videos"): v = fmt(v)
            f.write(f"{k:<20}: {v}\n")
        f.write("\nBAN VULNERABILITIES\n" + "─"*40 + "\n")
        for v in vulns:
            f.write(f"\n[{v['sev']}] {v['title']}\n")
            f.write(f"  Report as: {v['rtype']}\n")
            f.write(f"  {v['note']}\n")
    return fname

# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
def main():
    banner()
    print(f"  {C}Setup: {W}pip install cloudscraper requests colorama{RS}\n")

    while True:
        section("TARGET")
        try:
            raw = input(f"\n  {C}Username (q=quit): @{W}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if raw.lower() in ("q","quit","exit",""):
            print(f"\n  {G}BCS — Session closed.{RS}\n"); break

        un = raw.lstrip("@").strip()
        if not un:
            print(f"  {R}Enter a username!{RS}"); continue

        print(f"\n  {Y}Scanning @{un}{RS}\n")

        data = fetch(un)

        if not data:
            print(f"\n  {R}[✗] Failed to fetch @{un}{RS}")
            print(f"""
  {Y}Troubleshoot:{RS}
  {W}1. Check spelling (exact username){RS}
  {W}2. Account must be public{RS}
  {W}3. Check internet connection{RS}
  {W}4. Try again after 60 seconds{RS}
  {W}5. If still failing:{RS}
     {C}pip install --upgrade cloudscraper{RS}
""")
            try:
                input(f"  {DIM}Enter to continue...{RS}")
            except (KeyboardInterrupt, EOFError):
                break
            continue

        show_profile(data, un)
        vulns = analyze(data)
        show_vulns(vulns, un)

        try:
            if input(f"  {C}Save report? [y/N]: {W}").strip().lower() == "y":
                fname = save(un, data, vulns)
                print(f"  {G}[✓] Saved: {fname}{RS}")
        except (KeyboardInterrupt, EOFError):
            pass

        try:
            if input(f"\n  {C}Scan another? [Y/n]: {W}").strip().lower() == "n":
                print(f"\n  {G}BCS — Ochena Gamer.{RS}\n"); break
        except (KeyboardInterrupt, EOFError):
            break

        banner()

if __name__ == "__main__":
    main()
