#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────┐
# │          TikInfo Pro v7 — Bangladesh Cyber Spectre                 │
# │          CEO : Ochena Gamer                                        │
# │          Features: OSINT + Video Intel + Cross-Platform +          │
# │                    Shadowban + Bulk Scan + Growth Tracker          │
# └─────────────────────────────────────────────────────────────────────┘

import sys, os, re, json, time, math, hashlib, threading
from datetime import datetime, timezone
from collections import Counter

if sys.version_info[0] < 3:
    print("[!] Python 3 required.")
    sys.exit(1)

import subprocess
PKGS = ["cloudscraper","requests","colorama"]
for _pkg in PKGS:
    try: __import__(_pkg)
    except ImportError:
        subprocess.check_call([sys.executable,"-m","pip","install",_pkg,"--quiet"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import cloudscraper, requests
from colorama import Fore, Style, init
init(autoreset=True)

R=Fore.RED; C=Fore.CYAN; G=Fore.GREEN; Y=Fore.YELLOW
W=Fore.WHITE; M=Fore.MAGENTA; B=Fore.BLUE
DIM=Style.DIM; RS=Style.RESET_ALL; BRT=Style.BRIGHT

def clear(): os.system("cls" if os.name=="nt" else "clear")

# History file for growth tracking
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".tikinfo_history.json")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE,"r") as f: return json.load(f)
    except: pass
    return {}

def save_history(h):
    try:
        with open(HISTORY_FILE,"w") as f: json.dump(h,f)
    except: pass

# ══════════════════════════════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════════════════════════════
def banner():
    clear()
    print(f"""
{R}{BRT}  ████████╗██╗██╗  ██╗    ██╗███╗   ██╗███████╗ ██████╗ {RS}
{R}{BRT}     ██║   ██║██║ ██╔╝    ██║████╗  ██║██╔════╝██╔═══██╗{RS}
{Y}{BRT}     ██║   ██║█████╔╝     ██║██╔██╗ ██║█████╗  ██║   ██║{RS}
{Y}{BRT}     ██║   ██║██╔═██╗     ██║██║╚██╗██║██╔══╝  ██║   ██║{RS}
{R}{BRT}     ██║   ██║██║  ██╗    ██║██║ ╚████║██║     ╚██████╔╝{RS}
{R}{BRT}     ╚═╝   ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ {RS}

{C}  ╔══════════════════════════════════════════════════════════════╗
  ║  {W}{BRT}  TikTok OSINT + Intelligence Analyzer  v7 ULTRA  {RS}  {C}  ║
  ╠══════════════════════════════════════════════════════════════╣
  ║  {Y}Team    : Bangladesh Cyber Spectre{RS}                     {C}  ║
  ║  {Y}CEO     : Ochena Gamer{RS}                                 {C}  ║
  ║  {G}Features: Profile · Videos · Cross-Platform · Shadowban{RS}  {C}║
  ║  {G}         Bulk Scan · Growth Track · Fake % · Worth Est.{RS}  {C}║
  ║  {G}Status  : ONLINE  ●  Real Data Only  ●  Zero Fake{RS}        {C}║
  ╚══════════════════════════════════════════════════════════════╝{RS}
""")

# ══════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════════════════════
def section(t):
    w=61
    print(f"\n{C}  ╔{'═'*w}╗")
    pad=w-len(t)-2
    print(f"  ║  {W}{BRT}{t}{RS}{' '*max(0,pad)}{C}  ║")
    print(f"  ╚{'═'*w}╝{RS}")

def sub_section(t,color=C):
    pad=max(0,52-len(t))
    print(f"\n  {color}┌── {W}{BRT}{t}{RS}{color} {'─'*pad}┐{RS}")

def row(k,v,vc=W,kc=DIM):
    print(f"  {kc}  {k:<28}{RS}{vc}{v}{RS}")

def sep(): print(f"  {DIM}  {'─'*56}{RS}")

def stp(m): print(f"\n  {Y}  ⟳  {m}...{RS}",flush=True)
def ok_(m): print(f"  {G}  [✓] {m}{RS}")
def fail_(m):print(f"  {R}  [✗] {m}{RS}")
def info_(m):print(f"  {C}  [i] {m}{RS}")

def fmt(n):
    try: n=int(n or 0)
    except: return str(n)
    if n>=1_000_000_000: return f"{n/1e9:.2f}B"
    if n>=1_000_000:     return f"{n/1e6:.2f}M"
    if n>=1_000:         return f"{n/1e3:.1f}K"
    return str(n)

def fmt_ts(ts):
    try: return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
    except: return "Unknown"

def get_age_days(ts):
    try: return max(0,(int(time.time())-int(ts))//86400)
    except: return 0

def pbar(score,width=38):
    score=max(0,min(100,score))
    filled=int(width*score/100)
    empty=width-filled
    if score>=70:   fc=R
    elif score>=45: fc=Y
    else:           fc=G
    return f"{fc}{'█'*filled}{DIM}{'░'*empty}{RS}"

def mini_pbar(score,width=20):
    score=max(0,min(100,score))
    filled=int(width*score/100)
    empty=width-filled
    if score>=70:   fc=R
    elif score>=45: fc=Y
    else:           fc=G
    return f"{fc}{'▓'*filled}{DIM}{'░'*empty}{RS}"

# ══════════════════════════════════════════════════════════════════════
#  SCRAPER
# ══════════════════════════════════════════════════════════════════════
def make_scraper():
    sc=cloudscraper.create_scraper(
        browser={"browser":"chrome","platform":"android","mobile":True}
    )
    sc.headers.update({
        "Accept-Language":"en-US,en;q=0.9",
        "Referer":"https://www.tiktok.com/",
    })
    return sc

def _safe_json(r):
    try:
        ct=r.headers.get("Content-Type","")
        if "json" not in ct and not r.text.strip().startswith("{"): return None
        return r.json()
    except: return None

# ══════════════════════════════════════════════════════════════════════
#  PROFILE FETCH
# ══════════════════════════════════════════════════════════════════════
def try_tikwm(un,sc):
    stp("TikWM API — Profile")
    try:
        r=sc.get("https://www.tikwm.com/api/user/info",
                 params={"unique_id":un},timeout=20)
        d=_safe_json(r)
        if d and d.get("code")==0 and d.get("data"):
            ok_("TikWM success")
            return normalize(d["data"],un)
        fail_(f"TikWM: code={d.get('code') if d else 'no json'}")
    except Exception as e: fail_(f"TikWM: {e}")
    return None

def try_page(un,sc):
    stp("TikTok page scrape")
    try:
        sc.get("https://www.tiktok.com/",timeout=12)
        time.sleep(0.8)
        r=sc.get(f"https://www.tiktok.com/@{un}",timeout=25,allow_redirects=True)
        if r.status_code==404: fail_("User not found (404)"); return None
        if r.status_code!=200: fail_(f"HTTP {r.status_code}"); return None
        html=r.text
        for rx in [
            r'<script[^>]+id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>',
            r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
        ]:
            m=re.search(rx,html,re.DOTALL)
            if not m: continue
            try:
                obj=json.loads(m.group(1))
                info=(deep_find(obj,"userInfo") or
                      deep_find(obj,"UserModule") or
                      deep_find(obj,"user"))
                if info:
                    ok_("Page JSON success")
                    return normalize(info,un)
            except: continue
        d=regex_scrape(html,un)
        if d: ok_("Regex extract success"); return d
        fail_("Could not parse page data")
    except Exception as e: fail_(f"Page: {e}")
    return None

def try_oembed(un,sc):
    stp("oEmbed fallback")
    try:
        r=sc.get("https://www.tiktok.com/oembed",
                 params={"url":f"https://www.tiktok.com/@{un}/video/1"},timeout=10)
        d=_safe_json(r)
        if d and d.get("author_name"):
            ok_("oEmbed partial")
            return _empty_profile(un,d.get("author_name",un),d.get("thumbnail_url",""))
    except Exception as e: fail_(f"oEmbed: {e}")
    return None

def fetch(un):
    sc=make_scraper()
    for fn in [try_tikwm,try_page,try_oembed]:
        try:
            res=fn(un,sc)
            if res: return res
        except Exception as e: fail_(f"{fn.__name__}: {e}")
    return None

# ══════════════════════════════════════════════════════════════════════
#  NORMALIZE
# ══════════════════════════════════════════════════════════════════════
def normalize(raw,un):
    if not isinstance(raw,dict): return None
    u=raw.get("user",raw)
    s=raw.get("stats",{})
    if not s:
        s={k:u.get(k,0) for k in ["followerCount","followingCount","heartCount",
                                    "videoCount","diggCount","friendCount"]}
    def av(x):
        if isinstance(x,dict): return x.get("url_list",[""])[0]
        return str(x or "").replace("\\u002F","/").replace("\\/","/")
    bl=u.get("bioLink","")
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
        "avatarLarge": av(u.get("avatarLarger") or u.get("avatar_larger","")),
        "openFavorite":bool(u.get("openFavorite",False)),
        "roomId":      str(u.get("roomId","") or ""),
        "ins_id":      u.get("ins_id","") or "",
        "twitter_id":  u.get("twitter_id","") or "",
        "youtube_id":  u.get("youtube_channel_id","") or "",
        "bioLink":     bl,
        "commerceUser":bool(u.get("commerceUserInfo") or u.get("isEmbededSeller",False)),
        "following":   int(s.get("followingCount",0) or 0),
        "followers":   int(s.get("followerCount",0)  or 0),
        "hearts":      int(s.get("heartCount",0)     or 0),
        "videos":      int(s.get("videoCount",0)     or 0),
        "digg":        int(s.get("diggCount",0)      or 0),
        "friends":     int(s.get("friendCount",0)    or 0),
        "_partial":    False,
    }

def _empty_profile(un,name,avatar):
    p={k:0 for k in ["following","followers","hearts","videos","digg","friends","createTime"]}
    p.update({"uniqueId":un,"nickname":name,"id":"","signature":"",
              "verified":False,"private":False,"region":"Unknown",
              "language":"","avatarUrl":avatar,"avatarLarge":"",
              "openFavorite":False,"roomId":"","ins_id":"","twitter_id":"",
              "youtube_id":"","bioLink":"","commerceUser":False,"_partial":True})
    return p

def regex_scrape(html,un):
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
        "avatarUrl":"","avatarLarge":"","openFavorite":False,
        "roomId":str(p.get("roomId","")),
        "ins_id":str(p.get("ins_id","")),"twitter_id":str(p.get("twitter_id","")),
        "youtube_id":"","bioLink":str(p.get("bioLink","")),"commerceUser":False,
        "following":int(p.get("following",0)),"followers":int(p.get("followers",0)),
        "hearts":int(p.get("hearts",0)),"videos":int(p.get("videos",0)),
        "digg":int(p.get("digg",0)),"friends":int(p.get("friends",0)),
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

# ══════════════════════════════════════════════════════════════════════
#  VIDEO INTEL (NEW)
# ══════════════════════════════════════════════════════════════════════
def fetch_videos(un, sc, count=30):
    stp(f"Fetching last {count} videos via TikWM")
    try:
        videos = []
        cursor = 0
        while len(videos) < count:
            r = sc.get("https://www.tikwm.com/api/user/posts",
                       params={"unique_id": un, "count": min(count,30),
                               "cursor": cursor}, timeout=20)
            d = _safe_json(r)
            if not d or d.get("code") != 0: break
            items = d.get("data", {}).get("videos", [])
            if not items: break
            videos.extend(items)
            if not d.get("data", {}).get("hasMore", False): break
            cursor = d.get("data", {}).get("cursor", 0)
            if cursor == 0: break
        ok_(f"Fetched {len(videos)} videos")
        return videos[:count]
    except Exception as e:
        fail_(f"Video fetch: {e}")
        return []

def analyze_videos(videos):
    if not videos:
        return {}

    plays   = [v.get("play_count",0)  or v.get("playCount",0)  or 0 for v in videos]
    likes   = [v.get("digg_count",0)  or v.get("diggCount",0)  or 0 for v in videos]
    comments= [v.get("comment_count",0) or v.get("commentCount",0) or 0 for v in videos]
    shares  = [v.get("share_count",0)  or v.get("shareCount",0)  or 0 for v in videos]
    times   = [v.get("create_time",0)  or v.get("createTime",0)  or 0 for v in videos]

    # Hashtags
    all_tags = []
    for v in videos:
        title = v.get("title","") or v.get("desc","") or ""
        tags  = re.findall(r'#(\w+)', title)
        all_tags.extend([t.lower() for t in tags])

    # Posting hours
    hours = []
    for ts in times:
        if ts > 0:
            try: hours.append(datetime.fromtimestamp(ts).hour)
            except: pass

    # Days between posts
    sorted_times = sorted([t for t in times if t > 0], reverse=True)
    gaps = []
    for i in range(len(sorted_times)-1):
        gap = (sorted_times[i] - sorted_times[i+1]) / 86400
        gaps.append(gap)

    n = len(videos)
    return {
        "count":        n,
        "total_plays":  sum(plays),
        "total_likes":  sum(likes),
        "total_comments":sum(comments),
        "total_shares": sum(shares),
        "avg_plays":    sum(plays)//max(n,1),
        "avg_likes":    sum(likes)//max(n,1),
        "avg_comments": sum(comments)//max(n,1),
        "avg_shares":   sum(shares)//max(n,1),
        "max_plays":    max(plays) if plays else 0,
        "min_plays":    min(plays) if plays else 0,
        "top_hashtags": Counter(all_tags).most_common(10),
        "peak_hour":    Counter(hours).most_common(1)[0][0] if hours else None,
        "hour_dist":    Counter(hours),
        "avg_gap_days": sum(gaps)/max(len(gaps),1) if gaps else 0,
        "posts_per_week": 7/max(sum(gaps)/max(len(gaps),1),0.1) if gaps else 0,
        "videos":       videos,
        "plays_list":   plays,
        "likes_list":   likes,
    }

def show_video_intel(va, un):
    if not va:
        print(f"\n  {R}  No video data available{RS}")
        return

    section("VIDEO INTELLIGENCE")

    sub_section("PERFORMANCE OVERVIEW", C)
    row("Videos Analyzed",   str(va["count"]),                         Y)
    row("Total Views",        fmt(va["total_plays"]),                   W)
    row("Total Likes",        fmt(va["total_likes"]),                   M)
    row("Total Comments",     fmt(va["total_comments"]),                C)
    row("Total Shares",       fmt(va["total_shares"]),                  G)
    sep()
    row("Avg Views/Video",    fmt(va["avg_plays"]),                     W)
    row("Avg Likes/Video",    fmt(va["avg_likes"]),                     M)
    row("Avg Comments/Video", fmt(va["avg_comments"]),                  C)
    row("Avg Shares/Video",   fmt(va["avg_shares"]),                    G)
    row("Best Video Views",   fmt(va["max_plays"]),                     R)
    row("Lowest Video Views", fmt(va["min_plays"]),                     DIM)

    # Posting pattern
    sub_section("POSTING PATTERN", Y)
    ph = va.get("peak_hour")
    if ph is not None:
        ampm = "AM" if ph < 12 else "PM"
        h12  = ph if ph <= 12 else ph-12
        row("Peak Posting Hour",  f"{h12}:00 {ampm} (UTC)",             Y)
    row("Posts Per Week",     f"{va['posts_per_week']:.1f}",            G)
    row("Avg Gap Between Posts",f"{va['avg_gap_days']:.1f} days",       W)

    # Hour distribution bar
    if va.get("hour_dist"):
        print(f"\n  {C}  Posting Hour Distribution (UTC):{RS}")
        hd = va["hour_dist"]
        mx = max(hd.values()) if hd else 1
        for h in range(0,24,3):
            cnt = sum(hd.get(i,0) for i in range(h,h+3))
            bar_w = int((cnt/mx)*20) if mx > 0 else 0
            ampm = "AM" if h < 12 else "PM"
            h12  = h if h <=12 else h-12
            print(f"  {DIM}  {h12:2d}{ampm} {G}{'█'*bar_w}{DIM}{'░'*(20-bar_w)} {W}{cnt}{RS}")

    # Top Hashtags
    if va.get("top_hashtags"):
        sub_section("TOP HASHTAGS USED", M)
        for i,(tag,cnt) in enumerate(va["top_hashtags"][:10],1):
            bar_w = min(int((cnt/max(va["top_hashtags"][0][1],1))*24),24)
            print(f"  {M}  #{tag:<20}{G}{'█'*bar_w}{DIM}{'░'*(24-bar_w)} {W}{cnt}x{RS}")

    # Recent videos list
    sub_section(f"RECENT {min(va['count'],10)} VIDEOS", C)
    print(f"  {DIM}  {'#':<4}{'Views':<10}{'Likes':<10}{'Cmts':<8}{'Shares':<8}Title{RS}")
    sep()
    for i,v in enumerate(va.get("videos",[])[:10],1):
        plays   = v.get("play_count",0) or v.get("playCount",0) or 0
        likes   = v.get("digg_count",0) or v.get("diggCount",0) or 0
        cmts    = v.get("comment_count",0) or v.get("commentCount",0) or 0
        shrs    = v.get("share_count",0) or v.get("shareCount",0) or 0
        title   = (v.get("title","") or v.get("desc","") or "No title")[:40]
        print(f"  {Y}  {i:<4}{G}{fmt(plays):<10}{M}{fmt(likes):<10}{C}{fmt(cmts):<8}{W}{fmt(shrs):<8}{DIM}{title}{RS}")

# ══════════════════════════════════════════════════════════════════════
#  CROSS-PLATFORM CHECK (NEW)
# ══════════════════════════════════════════════════════════════════════
def check_cross_platform(un, ins_id, twitter_id, youtube_id):
    section("CROSS-PLATFORM INTELLIGENCE")
    sc = make_scraper()

    platforms = [
        ("Instagram",  f"https://www.instagram.com/{ins_id or un}/",  ins_id or un),
        ("Twitter/X",  f"https://twitter.com/{twitter_id or un}",     twitter_id or un),
        ("YouTube",    f"https://www.youtube.com/@{youtube_id or un}",youtube_id or un),
        ("GitHub",     f"https://github.com/{un}",                    un),
        ("Reddit",     f"https://www.reddit.com/user/{un}",           un),
        ("Pinterest",  f"https://www.pinterest.com/{un}/",            un),
        ("Snapchat",   f"https://www.snapchat.com/add/{un}",          un),
        ("LinkedIn",   f"https://www.linkedin.com/in/{un}/",          un),
        ("Twitch",     f"https://www.twitch.tv/{un}",                 un),
        ("Steam",      f"https://steamcommunity.com/id/{un}/",        un),
    ]

    sub_section("USERNAME PRESENCE SCAN", G)
    print(f"  {DIM}  Checking @{un} across platforms...{RS}\n")

    found, notfound, unknown = [], [], []

    for pname, url, check_un in platforms:
        try:
            r = sc.get(url, timeout=8, allow_redirects=True)
            if r.status_code == 200:
                # Extra check — ensure it's not a redirect to 404 page
                if "not found" not in r.text.lower()[:500] and \
                   "doesn't exist" not in r.text.lower()[:500]:
                    found.append((pname, url))
                    print(f"  {G}  [✓] {pname:<14} FOUND   {C}{url}{RS}")
                else:
                    notfound.append(pname)
                    print(f"  {R}  [✗] {pname:<14} Not found{RS}")
            elif r.status_code == 404:
                notfound.append(pname)
                print(f"  {R}  [✗] {pname:<14} Not found (404){RS}")
            else:
                unknown.append(pname)
                print(f"  {DIM}  [?] {pname:<14} HTTP {r.status_code}{RS}")
            time.sleep(0.3)
        except Exception as e:
            unknown.append(pname)
            print(f"  {DIM}  [?] {pname:<14} Timeout/Error{RS}")

    sep()
    print(f"\n  {G}  Found    : {len(found)} platforms")
    print(f"  {R}  Not Found: {len(notfound)} platforms")
    print(f"  {DIM}  Unknown  : {len(unknown)} platforms{RS}")

    # Linked accounts from TikTok profile
    sub_section("LINKED FROM TIKTOK PROFILE", C)
    links = []
    if ins_id:    links.append(("Instagram", f"instagram.com/{ins_id}"))
    if twitter_id:links.append(("Twitter/X", f"twitter.com/{twitter_id}"))
    if youtube_id:links.append(("YouTube",   f"youtube.com/@{youtube_id}"))
    if links:
        for pn, url in links:
            print(f"  {G}  ✓ {pn:<14} {C}{url}{RS}")
    else:
        print(f"  {DIM}  No accounts directly linked in TikTok profile{RS}")

    return found

# ══════════════════════════════════════════════════════════════════════
#  SHADOWBAN CHECK (NEW)
# ══════════════════════════════════════════════════════════════════════
def check_shadowban(un, d):
    section("SHADOWBAN DETECTION")
    sc = make_scraper()

    stp("Checking search visibility")
    shadowban_signals = []
    score = 0

    # Method 1: Search for username
    try:
        r = sc.get("https://www.tiktok.com/api/search/user/full/",
                   params={"keyword":un,"count":10,"offset":0},
                   timeout=15)
        data = _safe_json(r)
        if data:
            users = data.get("user_list",[])
            found_in_search = any(
                u.get("user_info",{}).get("unique_id","").lower()==un.lower()
                for u in users
            )
            if found_in_search:
                ok_("Account visible in search")
            else:
                shadowban_signals.append("Account NOT found in TikTok search results")
                score += 40
                fail_("Account NOT in search results")
    except Exception as e:
        info_(f"Search check failed: {e}")
        score += 10

    # Method 2: TikWM signal analysis
    try:
        r = sc.get("https://www.tikwm.com/api/user/info",
                   params={"unique_id":un},timeout=20)
        d2 = _safe_json(r)
        if d2 and d2.get("code")==0:
            u = d2.get("data",{}).get("user",{})
            stats = d2.get("data",{}).get("stats",{})
            followers = int(stats.get("followerCount",0))
            hearts    = int(stats.get("heartCount",0))
            videos    = int(stats.get("videoCount",0))
            if followers > 1000 and videos > 10:
                avg_plays_expected = followers * 0.1  # 10% view rate estimate
                hpv = hearts // max(videos,1)
                if hpv < (avg_plays_expected * 0.01) and followers > 10000:
                    shadowban_signals.append(f"Extremely low hearts/video vs followers — possible reduced reach")
                    score += 25
    except: pass

    # Method 3: Profile signals
    fol = int(d.get("followers",0))
    hrt = int(d.get("hearts",0))
    vid = int(d.get("videos",0))
    ad  = get_age_days(d.get("createTime",0))

    if fol > 10000 and vid > 20:
        hpv = hrt // max(vid,1)
        expected_min = fol * 0.5
        if hpv < expected_min * 0.01 and fol > 10000:
            shadowban_signals.append(f"Hearts/video ({fmt(hpv)}) very low for {fmt(fol)} followers")
            score += 20

    if ad > 180 and vid > 20 and fol < 100:
        shadowban_signals.append(f"Old account ({ad}d), many videos ({vid}) but very few followers ({fol})")
        score += 30

    # Display results
    sub_section("SHADOWBAN SIGNALS", R if score > 40 else Y if score > 20 else G)

    score = min(100, score)
    bar   = mini_pbar(score, 30)
    sc_c  = R if score >= 60 else Y if score >= 30 else G
    print(f"\n  Shadowban Risk: [{bar}] {sc_c}{BRT}{score}%{RS}\n")

    if shadowban_signals:
        for sig in shadowban_signals:
            print(f"  {R}  ⚠ {sig}{RS}")
    else:
        print(f"  {G}  ✓ No shadowban signals detected{RS}")
        print(f"  {G}  ✓ Account appears to have normal reach{RS}")

    sub_section("WHAT SHADOWBAN MEANS", DIM)
    print(f"  {DIM}  • Videos won't appear on For You Page (FYP) of non-followers")
    print(f"  {DIM}  • Account hidden from search results")
    print(f"  {DIM}  • Hashtag pages won't show account's videos")
    print(f"  {DIM}  • Engagement drops significantly without explanation{RS}")

    return score

# ══════════════════════════════════════════════════════════════════════
#  GROWTH TRACKER (NEW)
# ══════════════════════════════════════════════════════════════════════
def track_growth(un, d, history):
    section("GROWTH TRACKER")

    now     = int(time.time())
    uid_key = un.lower()

    if uid_key in history:
        old      = history[uid_key]
        old_time = old.get("timestamp", 0)
        days_ago = max(1, (now - old_time) // 86400)

        old_fol = old.get("followers", 0)
        old_hrt = old.get("hearts",    0)
        old_vid = old.get("videos",    0)

        new_fol = int(d.get("followers",0))
        new_hrt = int(d.get("hearts",0))
        new_vid = int(d.get("videos",0))

        d_fol = new_fol - old_fol
        d_hrt = new_hrt - old_hrt
        d_vid = new_vid - old_vid

        sub_section(f"CHANGE SINCE LAST SCAN ({days_ago} days ago)", G)

        def diff_row(label, old_v, new_v, diff):
            if diff > 0:   col=G;  sign="↑ +"
            elif diff < 0: col=R;  sign="↓ "
            else:          col=DIM; sign="━ "
            rate = abs(diff) // max(days_ago,1)
            print(f"  {DIM}  {label:<18}{RS}{W}{fmt(old_v):<12}{RS}→  {col}{fmt(new_v):<12}{sign}{fmt(abs(diff))}{DIM}  ({fmt(rate)}/day){RS}")

        print(f"  {DIM}  {'Metric':<18}{'Previous':<12}   {'Current':<12}Change{RS}")
        sep()
        diff_row("Followers", old_fol, new_fol, d_fol)
        diff_row("Hearts",    old_hrt, new_hrt, d_hrt)
        diff_row("Videos",    old_vid, new_vid, d_vid)

        # Growth rate analysis
        if old_fol > 0:
            growth_pct = (d_fol / old_fol) * 100
            sub_section("GROWTH ANALYSIS", Y)
            row("Growth Rate",     f"{growth_pct:+.2f}% in {days_ago} days",
                G if growth_pct > 0 else R)
            if days_ago > 0:
                daily = d_fol / days_ago
                row("Daily Avg Growth", f"{fmt(abs(int(daily)))} followers/day",
                    G if daily > 0 else R)
                projected_30  = int(daily * 30)
                projected_365 = int(daily * 365)
                row("Projected (30d)",  f"{fmt(int(new_fol + projected_30))} followers",  C)
                row("Projected (1yr)",  f"{fmt(int(new_fol + projected_365))} followers", C)

        # Previous scan data
        if "scans" in old:
            sub_section("SCAN HISTORY", DIM)
            scans = old["scans"][-5:]
            for s in scans:
                ts = datetime.fromtimestamp(s["t"]).strftime("%Y-%m-%d")
                print(f"  {DIM}  {ts}  Followers:{fmt(s['f']):<10} Hearts:{fmt(s['h'])}{RS}")
    else:
        print(f"\n  {Y}  First scan for @{un} — data saved for future comparison.{RS}")
        print(f"  {C}  Scan again later to see growth trends.{RS}")

    # Save current data
    scans_hist = history.get(uid_key, {}).get("scans", [])
    scans_hist.append({"t":now,"f":int(d.get("followers",0)),
                       "h":int(d.get("hearts",0)),"v":int(d.get("videos",0))})
    history[uid_key] = {
        "timestamp":  now,
        "followers":  int(d.get("followers",0)),
        "hearts":     int(d.get("hearts",0)),
        "videos":     int(d.get("videos",0)),
        "nickname":   d.get("nickname",""),
        "scans":      scans_hist[-20:],  # keep last 20
    }
    save_history(history)
    ok_("Growth data saved for next comparison")

# ══════════════════════════════════════════════════════════════════════
#  FAKE FOLLOWER ESTIMATE (NEW)
# ══════════════════════════════════════════════════════════════════════
def estimate_fake_followers(d, va=None):
    section("FAKE FOLLOWER & ACCOUNT WORTH ANALYSIS")
    fol  = int(d.get("followers",0))
    hrt  = int(d.get("hearts",0))
    vid  = int(d.get("videos",0))
    flw  = int(d.get("following",0))
    ad   = get_age_days(d.get("createTime",0))
    ver  = d.get("verified",False)

    if fol == 0:
        print(f"\n  {R}  Not enough data to estimate{RS}")
        return

    sub_section("FAKE FOLLOWER ESTIMATION", R)

    # Engagement-based estimate
    if vid > 0:
        hpv    = hrt / vid                          # hearts per video
        # Normal accounts: 2-10% engagement
        # Avg view expectation: followers * 0.1 to 0.5
        expected_eng   = fol * 0.05  # 5% engagement expected
        actual_eng_pct = (hpv / max(fol,1)) * 100

        if actual_eng_pct > 20:
            fake_pct = max(0, min(10, (20 - actual_eng_pct) * -1))
        elif actual_eng_pct > 10:
            fake_pct = 10
        elif actual_eng_pct > 5:
            fake_pct = 20
        elif actual_eng_pct > 2:
            fake_pct = 35
        elif actual_eng_pct > 0.5:
            fake_pct = 55
        else:
            fake_pct = 75
    else:
        # No videos — likely bought followers
        fake_pct = 80 if fol > 1000 else 40

    # Follow ratio adjustment
    if flw > 0:
        ratio = fol / flw
        if ratio < 0.1:   fake_pct = min(fake_pct + 20, 95)  # mass following
        elif ratio > 10:  fake_pct = max(fake_pct - 10, 0)   # organic growth

    # Age adjustment
    if ad < 30 and fol > 10000:  fake_pct = min(fake_pct + 15, 95)
    if ad > 365 and ver:          fake_pct = max(fake_pct - 15, 0)

    real_pct  = 100 - fake_pct
    fake_count= int(fol * fake_pct / 100)
    real_count= fol - fake_count

    # Display
    fake_bar = mini_pbar(fake_pct, 30)
    real_bar = mini_pbar(real_pct, 30)

    print(f"\n  {R}  Fake Followers : [{fake_bar}] {BRT}{fake_pct}%{RS} ≈ {fmt(fake_count)}")
    print(f"  {G}  Real Followers : [{real_bar}] {BRT}{real_pct}%{RS} ≈ {fmt(real_count)}\n")

    if fake_pct >= 70: print(f"  {R}{BRT}  ⚠  HIGH FAKE — Likely purchased followers{RS}")
    elif fake_pct >= 40: print(f"  {Y}  ⚡  MODERATE — Mix of real and fake{RS}")
    else: print(f"  {G}  ✓  LOW FAKE — Mostly organic following{RS}")

    # Video-based engagement if available
    if va and va.get("avg_plays"):
        sub_section("ENGAGEMENT REALITY", Y)
        avg_p = va.get("avg_plays", 0)
        view_ratio = (avg_p / max(fol,1)) * 100
        row("Avg Views/Video",        fmt(avg_p),              W)
        row("View Rate (views/fol)",  f"{view_ratio:.1f}%",
            G if view_ratio > 20 else Y if view_ratio > 5 else R)
        row("Est. Engaged Audience",  fmt(int(fol * view_ratio / 100)),  C)

    # Account Worth Estimate
    sub_section("ACCOUNT MARKET WORTH ESTIMATE", Y)
    # Based on influencer marketing rates
    if real_count >= 1_000_000:
        min_rate = real_count * 0.001   # $0.001 per real follower
        max_rate = real_count * 0.003
    elif real_count >= 100_000:
        min_rate = real_count * 0.002
        max_rate = real_count * 0.005
    elif real_count >= 10_000:
        min_rate = real_count * 0.003
        max_rate = real_count * 0.008
    elif real_count >= 1_000:
        min_rate = real_count * 0.005
        max_rate = real_count * 0.015
    else:
        min_rate = real_count * 0.001
        max_rate = real_count * 0.005

    # Verification bonus
    if ver:
        min_rate *= 1.5
        max_rate *= 2.0

    # Engagement adjustment
    if va and va.get("avg_plays"):
        vr = (va["avg_plays"] / max(real_count,1)) * 100
        if vr > 30: min_rate *= 2; max_rate *= 3
        elif vr > 10: min_rate *= 1.5; max_rate *= 2

    print(f"\n  {Y}  Sponsored Post  : {G}${min_rate:,.0f} – ${max_rate:,.0f} USD{RS}")
    print(f"  {Y}  Per 1K Real Fol : {G}${(min_rate/max(real_count,1)*1000):,.2f} – ${(max_rate/max(real_count,1)*1000):,.2f}{RS}")
    print(f"  {Y}  Account Sell Est: {G}${min_rate*3:,.0f} – ${max_rate*5:,.0f} USD{RS}")
    print(f"\n  {DIM}  Estimates based on influencer market rates (2024){RS}")

# ══════════════════════════════════════════════════════════════════════
#  DISPLAY PROFILE (original preserved)
# ══════════════════════════════════════════════════════════════════════
def show_profile(d, un):
    section("PROFILE INTELLIGENCE")
    ad=get_age_days(d.get("createTime",0))

    sub_section("IDENTITY", C)
    row("Username",     "@"+(d.get("uniqueId") or un),              C)
    row("Nickname",     d.get("nickname")   or "N/A",               W)
    row("User ID",      d.get("id")         or "Unknown",           Y)
    row("Bio",          d.get("signature")  or "(empty)",           DIM)
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

    sub_section("REGION & ACCOUNT INFO", C)
    row("Region",           d.get("region")   or "Unknown",         Y)
    row("Language",         d.get("language") or "Unknown",         W)
    row("Account Created",  fmt_ts(d.get("createTime",0)),          G)
    row("Account Age",      f"{ad} days"+(f" 🆕 NEW ACCOUNT" if ad<30 else ""), W)
    row("Profile URL",      f"tiktok.com/@{d.get('uniqueId',un)}", C)
    if d.get("avatarLarge") or d.get("avatarUrl"):
        row("Avatar URL",   (d.get("avatarLarge") or d.get("avatarUrl",""))[:70],DIM)

    sub_section("STATISTICS", C)
    fol=int(d.get("followers",0)); flw=int(d.get("following",0))
    hrt=int(d.get("hearts",0));    vid=int(d.get("videos",0))
    dig=int(d.get("digg",0));      fri=int(d.get("friends",0))

    row("Followers",        fmt(fol),  R)
    row("Following",        fmt(flw),  W)
    row("Total Likes",      fmt(hrt),  M)
    row("Videos Posted",    fmt(vid),  Y)
    row("Digg Count",       fmt(dig),  W)
    row("Friends",          fmt(fri),  C)

    if fol > 0 and vid > 0:
        row("Avg Likes/Video",fmt(hrt//max(vid,1)), DIM)
    if fol > 0 and flw > 0:
        ratio = fol/max(flw,1)
        row("Follow Ratio", f"{ratio:.1f}x  {'(Organic)' if ratio>1 else '(Follow-for-follow)'}",
            G if ratio>1 else Y)
    if fol > 0 and hrt > 0:
        eng=(hrt/max(fol,1))*100
        row("Engagement Rate",f"{eng:.1f}%  {'(High)' if eng>5 else '(Normal)' if eng>1 else '(Low)'}",
            G if eng>5 else Y if eng>1 else DIM)

    sub_section("LINKED ACCOUNTS", C)
    row("Instagram",  d.get("ins_id")     or "Not linked", G if d.get("ins_id")     else DIM)
    row("Twitter/X",  d.get("twitter_id") or "Not linked", G if d.get("twitter_id") else DIM)
    row("YouTube",    d.get("youtube_id") or "Not linked", G if d.get("youtube_id") else DIM)

    if d.get("_partial"):
        print(f"\n  {Y}  ⚠  Partial data — TikTok limited the API response{RS}")
    print(f"\n  {DIM}  Note: Email, Phone, DOB = Encrypted by TikTok. Not accessible externally.{RS}\n")

# ══════════════════════════════════════════════════════════════════════
#  BAN ANALYSIS ENGINE (original preserved, complete)
# ══════════════════════════════════════════════════════════════════════
def _extract_signals(d):
    fol=int(d.get("followers",0)); flw=int(d.get("following",0))
    hrt=int(d.get("hearts",0));    vid=int(d.get("videos",0))
    dig=int(d.get("digg",0));      fri=int(d.get("friends",0))
    ct=int(d.get("createTime",0)); ad=get_age_days(ct)
    ver=d.get("verified",False);   priv=d.get("private",False)
    comm=d.get("commerceUser",False); live=bool(d.get("roomId",""))
    ofav=d.get("openFavorite",False)
    bio=(d.get("signature","") or "").strip()
    reg=(d.get("region","") or "").upper()
    bl=(d.get("bioLink","") or "").strip()
    ins=bool(d.get("ins_id","")); tw=bool(d.get("twitter_id",""))
    yt=bool(d.get("youtube_id",""))
    avg_lpv=hrt//max(vid,1) if vid>0 else 0
    eng_rate=(hrt/max(fol,1))*100 if fol>0 else 0
    fol_ratio=fol/max(flw,1) if flw>0 else 0
    hf_ratio=hrt/max(fol,1) if fol>0 else 0
    vf_ratio=vid/max(fol,1) if fol>0 else 0
    is_new=ad<30; is_young=30<=ad<90; is_established=ad>=180
    is_bot_pattern=(fol>1000 and vid==0) or (flw>10000 and fol<200) or (hf_ratio>1000 and fol>100)
    is_seller=comm or bool(bl)
    is_suspicious=(fol>5000 and vid<3) or (hf_ratio>500 and fol>100)
    is_influencer=fol>=100000; is_mega=fol>=1_000_000
    empty_bio=len(bio)<3; linked=ins or tw or yt
    high_eng=eng_rate>15; low_eng=eng_rate<1 and fol>1000
    return dict(fol=fol,flw=flw,hrt=hrt,vid=vid,dig=dig,fri=fri,
                ad=ad,ver=ver,priv=priv,comm=comm,live=live,ofav=ofav,
                bio=bio,reg=reg,bl=bl,ins=ins,tw=tw,yt=yt,
                avg_lpv=avg_lpv,eng_rate=eng_rate,fol_ratio=fol_ratio,
                hf_ratio=hf_ratio,vf_ratio=vf_ratio,
                is_new=is_new,is_young=is_young,is_established=is_established,
                is_bot_pattern=is_bot_pattern,is_seller=is_seller,
                is_suspicious=is_suspicious,is_influencer=is_influencer,
                is_mega=is_mega,empty_bio=empty_bio,linked=linked,
                high_eng=high_eng,low_eng=low_eng)

def score_report_types(d):
    s=_extract_signals(d); results=[]
    # ── SPAM ──────────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["is_bot_pattern"]:
        sc+=55
        if s["fol"]>1000 and s["vid"]==0: reasons.append(f"⚠ {fmt(s['fol'])} followers, ZERO videos — clear bot/purchased account")
        elif s["flw"]>10000 and s["fol"]<200: reasons.append(f"⚠ Following {fmt(s['flw'])} people but only {fmt(s['fol'])} followers — spam bot pattern")
        if s["hf_ratio"]>1000: reasons.append(f"⚠ Hearts/follower ratio: {s['hf_ratio']:.0f}x — artificial engagement detected")
    if s["is_new"]: sc+=35; reasons.append(f"⚠ Account only {s['ad']} days old — new accounts are 3x more vulnerable to Spam reports")
    elif s["is_young"]: sc+=18; reasons.append(f"Account age {s['ad']} days — young accounts have lower trust score")
    if s["is_suspicious"] and not s["is_bot_pattern"]: sc+=25; reasons.append(f"Suspicious ratio: {fmt(s['fol'])} followers with only {s['vid']} videos")
    if s["empty_bio"]: sc+=12; reasons.append("Empty bio — bot/fake account strong indicator")
    if s["low_eng"]: sc+=18; reasons.append(f"Extremely low engagement ({s['eng_rate']:.1f}%) on {fmt(s['fol'])} followers — bought followers")
    if s["fol"]>500 and s["flw"]>s["fol"]*10: sc+=20; reasons.append(f"Mass follow behavior: following {fmt(s['flw'])} for {fmt(s['fol'])} followers")
    if not s["ver"]: sc+=8; reasons.append("Unverified account — lower trust weight in TikTok moderation system")
    if not reasons: reasons.append("No strong spam signals detected from profile data"); sc=max(sc,10)
    tips+=["Report: Spam → Fake engagement OR Spam content"]
    if s["is_new"]: tips.append("🔥 PRIORITY: New account — Spam report most effective right now")
    if s["is_bot_pattern"]: tips.append("🔥 Report: Spam → Purchasing followers/likes/comments")
    tips.append("Report 3-5 of their videos as Spam simultaneously for higher weight")
    results.append({"type":"Spam","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else G})
    # ── SCAM ──────────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["comm"]: sc+=45; reasons.append(f"Commerce/seller account — TikTok Shop violations = fast ban")
    if s["bl"]: sc+=30; reasons.append(f"External link in bio: {s['bl'][:50]} — potential scam redirect")
    if s["fol"]>1000 and s["vid"]<5 and s["hrt"]>s["fol"]*50: sc+=25; reasons.append("Suspicious: high hearts, few videos — fake/resold account")
    if s["is_influencer"] and s["empty_bio"]: sc+=15; reasons.append(f"Large account ({fmt(s['fol'])} followers) with empty bio — impersonation risk")
    if s["high_eng"] and s["is_suspicious"]: sc+=20; reasons.append("Abnormally high engagement — fake engagement scam")
    if not reasons: reasons.append("No scam signals — check video content for scam ads"); sc=max(sc,5)
    if s["comm"]: tips.append("🔥 Report: Illegal activities → Scam or Deceptive practices")
    if s["bl"]:   tips.append("🔥 Report: Scam → Phishing or Fraudulent links")
    tips+=["Check videos for: fake giveaways, investment scams, impersonation","Report as: Illegal activities → Scam / Deceptive practices"]
    results.append({"type":"Scam / Fraud","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── HARASSMENT ────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["is_influencer"]: sc+=25; reasons.append(f"Large account ({fmt(s['fol'])} followers) — harassment priority reviewed")
    if s["vid"]>200: sc+=15; reasons.append(f"High video count ({s['vid']}) — more targeting chances")
    if s["high_eng"] and s["is_influencer"]: sc+=15; reasons.append("High engagement + large reach = harassment amplified")
    if s["live"]: sc+=20; reasons.append("Currently LIVE — live harassment = immediate report option")
    if not reasons: reasons.append("No harassment signals — check comment sections"); sc=max(sc,8)
    tips+=["Report: Harassment and bullying → Threatening violence or Unwanted contact","Check if they made videos targeting specific individuals"]
    if s["live"]: tips.append("🔥 Report the LIVE stream directly for fastest action")
    results.append({"type":"Harassment and bullying","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── ILLEGAL ───────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["comm"] and s["bl"]: sc+=55; reasons.append("Commerce account + bio link — likely selling regulated/illegal products")
    elif s["comm"]: sc+=35; reasons.append("Commerce/seller — check for counterfeit goods")
    elif s["bl"]: sc+=25; reasons.append(f"Bio link: {s['bl'][:50]} — could direct to illegal marketplace")
    if s["reg"] in("BD","PK","IN","NG","ID"): sc+=10; reasons.append(f"Region {s['reg']} — higher frequency of illegal goods accounts")
    if not reasons: reasons.append("No illegal activity signals in profile data"); sc=max(sc,5)
    if s["comm"]: tips.append("🔥 Report: Illegal activities → Counterfeit goods / Regulated items")
    tips+=["Check video content for: drugs, weapons, counterfeit goods","Report: Illegal activities → Gambling or Tobacco/alcohol to minors"]
    results.append({"type":"Illegal activities and regulated goods","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── MISINFO ───────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["ver"] and s["is_influencer"]: sc+=40; reasons.append(f"Verified influencer ({fmt(s['fol'])} followers) — misinfo priority")
    elif s["is_influencer"]: sc+=25; reasons.append(f"Large reach ({fmt(s['fol'])} followers)")
    if s["is_mega"]: sc+=20; reasons.append(f"Mega account (1M+ followers) — misinfo spreads fast")
    if s["high_eng"]: sc+=15; reasons.append("High engagement rate — misleading content reaches more people")
    if s["reg"] in("BD","IN","PK","NG","PH"): sc+=10; reasons.append(f"Region {s['reg']} — election/health misinfo frequently reported")
    if not reasons: reasons.append("Misinfo cannot be confirmed from profile data alone"); sc=max(sc,8)
    if s["ver"]: tips.append("🔥 PRIORITY for verified accounts: Misinformation → False health/safety info")
    tips+=["Report: Misinformation → False information about health, elections, or safety","Most effective on news/health/political content creators"]
    results.append({"type":"Misinformation","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── NUDITY ────────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["live"]: sc+=65; reasons.append("🔴 Currently LIVE — live sexual content = ban within minutes"); tips.append("🔥 REPORT THE LIVE STREAM NOW")
    if s["ofav"]: sc+=20; reasons.append("Open favorites — check for inappropriate liked videos")
    if s["high_eng"] and s["fol"]>50000: sc+=15; reasons.append("High engagement on large account")
    if s["empty_bio"] and s["is_suspicious"]: sc+=10; reasons.append("Suspicious account with empty bio — common adult content pattern")
    if not reasons: reasons.append("Cannot confirm sexual content from profile data"); sc=max(sc,5); tips.append("Browse recent videos — if sexual content found, report specific videos")
    tips.append("Report: Nudity and sexual activities → Sexual content or Nudity")
    results.append({"type":"Nudity and sexual activities","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── HATE SPEECH ───────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["is_influencer"]: sc+=20; reasons.append(f"Large account ({fmt(s['fol'])} followers) — hate speech amplified")
    if s["reg"] in("BD","IN","PK","MM","NG"): sc+=15; reasons.append(f"Region {s['reg']} — hate speech reports frequently prioritized")
    if s["high_eng"]: sc+=10; reasons.append("High engagement — hateful content reaching wider audience")
    if s["vid"]>100: sc+=8; reasons.append(f"{s['vid']} videos — higher chance of hate speech content")
    if not reasons: reasons.append("Hate speech cannot be confirmed from profile data"); sc=max(sc,5)
    tips+=["Report: Hate speech → Attacks based on religion, ethnicity, or race","Watch recent videos for hateful language, slurs, or targeted attacks"]
    results.append({"type":"Hate speech","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── VIOLENT ───────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["live"]: sc+=50; reasons.append("🔴 Currently LIVE — real-time violent content = immediate ban trigger"); tips.append("🔥 Report LIVE directly: Profile → Live → Report → Violent content")
    if s["vid"]>100: sc+=10; reasons.append(f"{s['vid']} videos — larger library increases chances")
    if not reasons: reasons.append("Violent content cannot be detected from profile data alone"); sc=max(sc,5); tips.append("Check recent videos for graphic/violent content")
    tips.append("Report: Violent content → Graphic violence or Real-world violence")
    results.append({"type":"Violent and graphic content","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── DANGEROUS ─────────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["live"]: sc+=45; reasons.append("🔴 Currently LIVE — dangerous stunts live = immediate ban risk")
    if s["vid"]>50 and s["high_eng"]: sc+=15; reasons.append("High-engagement creator — dangerous challenge content spreads fast")
    if not reasons: reasons.append("Dangerous acts require video evidence"); sc=max(sc,5); tips.append("Check videos for dangerous challenges, unsafe stunts, or self-harm")
    tips+=["Report: Dangerous acts → Dangerous activity or Challenges","Report: Dangerous acts → Suicide or self-harm content"]
    results.append({"type":"Dangerous acts and challenges","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── MINOR SAFETY ──────────────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["fol"]>0 and s["vid"]>0: sc+=8
    if s["live"]: sc+=20; reasons.append("Currently LIVE — live minor safety violations = fastest TikTok response")
    if not reasons: reasons.append("Minor safety requires specific evidence"); sc=max(sc,5)
    tips+=["HIGHEST SEVERITY: TikTok responds fastest to minor safety reports","Report: Minor safety → Sexual exploitation or Grooming","Only report if you have CLEAR evidence — false reports are penalized"]
    results.append({"type":"Minor safety","score":min(100,sc),"reasons":reasons,"tips":tips,"color":R if sc>=65 else Y if sc>=40 else DIM})
    # ── INTELLECTUAL PROPERTY ─────────────────────────────────────────
    sc=0; reasons=[]; tips=[]
    if s["vid"]>50: sc+=15; reasons.append(f"{s['vid']} videos — higher probability of reposted/stolen content")
    if s["is_influencer"] and not s["linked"]: sc+=10; reasons.append(f"Large account with no linked original platforms")
    if not reasons: reasons.append("IP violations require checking specific video content"); sc=max(sc,5)
    tips+=["Report: Intellectual property → Copyright infringement","If they repost others' videos without credit, report those specific videos","Original creators can submit DMCA directly to TikTok"]
    results.append({"type":"Intellectual property violations","score":min(100,sc),"reasons":reasons,"tips":tips,"color":Y if sc>=40 else DIM})
    results.sort(key=lambda x:x["score"],reverse=True)
    return results

def overall_ban_score(report_scores, d):
    s=_extract_signals(d)
    top=report_scores[0]["score"] if report_scores else 0
    avg_top3=sum(r["score"] for r in report_scores[:3])/3 if len(report_scores)>=3 else top
    base=(top*0.55)+(avg_top3*0.25)
    if s["ad"]==0:              base+=5
    elif s["ad"]<7:             base+=30
    elif s["ad"]<30:            base+=22
    elif s["ad"]<90:            base+=12
    elif s["ad"]<180:           base+=4
    elif s["is_established"]:   base-=8
    if s["ver"]:                base-=18
    else:                       base+=8
    if s["fol"]<100:            base+=15
    elif s["fol"]<1000:         base+=8
    elif s["fol"]<10000:        base+=3
    elif s["fol"]<100000:       base+=0
    elif s["fol"]<1_000_000:    base-=8
    else:                       base-=18
    if s["is_bot_pattern"]:     base+=20
    if s["is_suspicious"]:      base+=12
    if s["empty_bio"]:          base+=6
    if s["low_eng"]:            base+=10
    if s["live"]:               base+=22
    if s["comm"]:               base+=8
    if s["bl"]:                 base+=6
    if s["hf_ratio"]>1000:      base+=15
    elif s["hf_ratio"]>500:     base+=8
    if s["priv"]:               base-=10
    if s["linked"]:             base-=5
    return int(min(99,max(3,base)))

def show_analysis(report_scores, d, un):
    section("BAN VULNERABILITY ANALYSIS")
    ban_score=overall_ban_score(report_scores,d)
    bar=pbar(ban_score); sc=R if ban_score>=70 else Y if ban_score>=45 else G
    ad=get_age_days(d.get("createTime",0))
    sub_section("OVERALL BAN DIFFICULTY SCORE",C)
    print(f"\n  [{bar}] {sc}{BRT} {ban_score}% Bannable{RS}")
    if ban_score>=80: print(f"\n  {R}{BRT}  ⚠  VERY HIGH — Highly vulnerable to coordinated reports{RS}")
    elif ban_score>=60: print(f"\n  {R}  ⚠  HIGH — Coordinated reports likely to result in ban{RS}")
    elif ban_score>=40: print(f"\n  {Y}  ⚡  MODERATE — Multiple reports needed, focus on best category{RS}")
    else: print(f"\n  {G}  ●  LOW — Account appears clean. Focus on video content violations.{RS}")
    sub_section("ACCOUNT WEAKNESS SUMMARY",Y)
    ver=d.get("verified",False)
    row("Verified Status","✓ Verified (Harder to ban)" if ver else "✗ Not Verified (Easier to ban)",DIM if ver else R)
    row("Account Age",f"{ad} days {'🔴 VERY VULNERABLE' if ad<30 else '🟡 Vulnerable' if ad<90 else '🟢 Established'}",R if ad<30 else Y if ad<90 else G)
    row("Currently Live","🔴 YES — Report NOW for fastest ban" if d.get("roomId") else "No",R if d.get("roomId") else DIM)
    row("Bio Link",f"YES: {d.get('bioLink')} (violation risk)" if d.get("bioLink") else "None",Y if d.get("bioLink") else DIM)
    row("Commerce Account","YES — Higher fraud/scam risk" if d.get("commerceUser") else "No",Y if d.get("commerceUser") else DIM)
    row("Open Favorites","YES — Content exposure" if d.get("openFavorite") else "No",M if d.get("openFavorite") else DIM)
    if int(d.get("followers",0))>1000 and int(d.get("videos",0))<3:
        row("Follower Pattern",f"⚠ Suspicious: {fmt(d.get('followers',0))} followers, {d.get('videos',0)} videos",R)
    section("ALL REPORT TYPES — EFFECTIVENESS ANALYSIS")
    print(f"  {DIM}  Each type scored based on actual account data patterns.{RS}\n")
    applicable=[r for r in report_scores if r["score"]>=20]
    low_signal=[r for r in report_scores if r["score"]<20]
    print(f"  {G}  Showing {len(applicable)} applicable + {len(low_signal)} low-signal report types.{RS}\n")
    for i,rpt in enumerate(applicable,1):
        sc_val=rpt["score"]; color=rpt["color"]
        rtype=rpt["type"]; reasons=rpt["reasons"]; tips=rpt["tips"]
        if sc_val>=70:   eff=f"{R}{BRT}⚡ HIGHLY EFFECTIVE{RS}"
        elif sc_val>=50: eff=f"{Y}{BRT}✓ EFFECTIVE{RS}"
        elif sc_val>=35: eff=f"{Y}~ MODERATE{RS}"
        else:            eff=f"{DIM}○ LOW — Needs video evidence{RS}"
        mini_bar=pbar(sc_val,width=22)
        print(f"\n  {color}{BRT}[{i:02d}] {rtype}{RS}")
        print(f"       [{mini_bar}] {color}{BRT}{sc_val}%{RS}  {eff}")
        print(f"  {DIM}       Signals:{RS}")
        for r in reasons[:3]: print(f"  {DIM}         • {RS}{W}{r}{RS}")
        print(f"  {DIM}       How to report:{RS}")
        for t in tips[:3]: print(f"  {DIM}         → {RS}{C}{t}{RS}")
    if low_signal:
        print(f"\n  {DIM}  ── Low signal (< 20%) — needs manual video check ──{RS}")
        for rpt in low_signal: print(f"  {DIM}  [{rpt['score']:2d}%] {rpt['type']}{RS}")
    best=report_scores[0]; second=report_scores[1] if len(report_scores)>1 else None
    section("OPTIMAL ATTACK STRATEGY")
    needed="5-8" if ban_score>=80 else "10-15" if ban_score>=60 else "15-25" if ban_score>=40 else "25+"
    window="15 min" if ban_score>=80 else "30 min" if ban_score>=60 else "1 hour"
    expected="Permanent ban within 12-24h" if ban_score>=75 else "Suspension review within 48h" if ban_score>=55 else "Review triggered within 72h" if ban_score>=35 else "May not result in ban without video evidence"
    print(f"""
  {G}  Primary Report Type  : {Y}{BRT}{best['type']}{RS}
  {G}  Accounts Needed      : {W}{needed} different TikTok accounts{RS}
  {G}  All Within           : {W}{window} window for max impact{RS}
  {G}  Expected Result      : {W}{expected}{RS}
""")
    if second and second["score"]>=30:
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

# ══════════════════════════════════════════════════════════════════════
#  SAVE REPORT (enhanced)
# ══════════════════════════════════════════════════════════════════════
def save_report(un, d, report_scores, va=None, fake_pct=None, shadowban_score=None, cross_found=None):
    ts=int(time.time())
    fname=f"tikinfo_{un}_{ts}.txt"
    ban_s=overall_ban_score(report_scores,d)
    with open(fname,"w",encoding="utf-8") as f:
        f.write("╔═══════════════════════════════════════════════════╗\n")
        f.write("║  TikInfo Pro v7 — Bangladesh Cyber Spectre        ║\n")
        f.write("║  CEO: Ochena Gamer                                ║\n")
        f.write("╚═══════════════════════════════════════════════════╝\n\n")
        f.write(f"Target     : @{un}\n")
        f.write(f"Scanned    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Ban Score  : {ban_s}%\n")
        if fake_pct is not None:   f.write(f"Fake Fol % : ~{fake_pct}%\n")
        if shadowban_score is not None: f.write(f"Shadowban  : {shadowban_score}% risk\n")
        f.write("═"*55+"\n\n")
        f.write("PROFILE\n"+"─"*40+"\n")
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
        if va:
            f.write("\n\nVIDEO INTEL\n"+"─"*40+"\n")
            f.write(f"  Videos Analyzed  : {va.get('count',0)}\n")
            f.write(f"  Total Views      : {fmt(va.get('total_plays',0))}\n")
            f.write(f"  Avg Views/Video  : {fmt(va.get('avg_plays',0))}\n")
            f.write(f"  Avg Likes/Video  : {fmt(va.get('avg_likes',0))}\n")
            f.write(f"  Posts/Week       : {va.get('posts_per_week',0):.1f}\n")
            if va.get("top_hashtags"):
                f.write(f"  Top Hashtags     : {', '.join('#'+t for t,_ in va['top_hashtags'][:5])}\n")
        if cross_found:
            f.write("\n\nCROSS-PLATFORM\n"+"─"*40+"\n")
            for pn,url in cross_found:
                f.write(f"  FOUND: {pn:<14} {url}\n")
        f.write("\n\nREPORT TYPE ANALYSIS\n"+"─"*40+"\n")
        for rpt in report_scores:
            f.write(f"\n[{rpt['score']:3d}%] {rpt['type']}\n")
            for r in rpt["reasons"]: f.write(f"  • {r}\n")
            for t in rpt["tips"]:    f.write(f"  → {t}\n")
    return fname

# ══════════════════════════════════════════════════════════════════════
#  BULK SCAN (NEW)
# ══════════════════════════════════════════════════════════════════════
def bulk_scan():
    section("BULK USERNAME SCAN")
    print(f"  {C}  Enter usernames one per line. Empty line to start scan.{RS}\n")
    usernames = []
    while True:
        try:
            u = input(f"  {Y}  @{RS}").strip().lstrip("@")
            if not u: break
            usernames.append(u)
        except (KeyboardInterrupt, EOFError): break

    if not usernames:
        print(f"  {R}  No usernames entered.{RS}"); return

    print(f"\n  {G}  Scanning {len(usernames)} accounts...{RS}\n")
    results = []
    history = load_history()

    for i, un in enumerate(usernames, 1):
        print(f"\n  {C}  [{i}/{len(usernames)}] Scanning @{un}...{RS}")
        d = fetch(un)
        if not d:
            print(f"  {R}  Failed to fetch @{un}{RS}")
            results.append({"un":un, "status":"failed"})
            continue

        rs = score_report_types(d)
        bs = overall_ban_score(rs, d)
        results.append({
            "un":       un,
            "status":   "ok",
            "followers": int(d.get("followers",0)),
            "videos":    int(d.get("videos",0)),
            "verified":  d.get("verified",False),
            "ban_score": bs,
            "best_type": rs[0]["type"] if rs else "N/A",
        })

        # Save to history
        now = int(time.time())
        history[un.lower()] = {
            "timestamp": now,
            "followers":int(d.get("followers",0)),
            "hearts":   int(d.get("hearts",0)),
            "videos":   int(d.get("videos",0)),
            "nickname": d.get("nickname",""),
        }
        time.sleep(1.5)

    save_history(history)

    # Summary table
    section("BULK SCAN RESULTS")
    print(f"  {DIM}  {'#':<4}{'Username':<22}{'Followers':<12}{'Videos':<8}{'Verified':<10}{'Ban%':<8}Best Report Type{RS}")
    sep()
    results.sort(key=lambda x: x.get("ban_score",0), reverse=True)
    for i,r in enumerate(results,1):
        if r["status"]=="failed":
            print(f"  {R}  {i:<4}{r['un']:<22}FAILED{RS}")
            continue
        vc = R if r["ban_score"]>=70 else Y if r["ban_score"]>=40 else G
        print(f"  {W}  {i:<4}{C}{r['un']:<22}{G}{fmt(r['followers']):<12}{Y}{r['videos']:<8}{M}{'✓' if r['verified'] else '✗':<10}{vc}{r['ban_score']:>3}%{RS}  {DIM}{r['best_type'][:30]}{RS}")

    print(f"\n  {G}  Scan complete. {len([r for r in results if r['status']=='ok'])} of {len(usernames)} successful.{RS}")
    try:
        if input(f"\n  {C}  Save bulk report? [y/N]: {W}").strip().lower()=="y":
            ts=int(time.time())
            fname=f"tikinfo_bulk_{ts}.txt"
            with open(fname,"w",encoding="utf-8") as f:
                f.write("TikInfo Pro v7 — Bulk Scan Report\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for r in results:
                    if r["status"]=="failed":
                        f.write(f"@{r['un']}: FAILED\n")
                    else:
                        f.write(f"@{r['un']}: {r['followers']} followers | Ban:{r['ban_score']}% | {r['best_type']}\n")
            print(f"  {G}  Saved: {fname}{RS}")
    except: pass

# ══════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════════
def main_menu():
    banner()
    print(f"{C}  ╔══════════════════════════════════════════════════════╗{RS}")
    print(f"{C}  ║                   MAIN MENU                         ║{RS}")
    print(f"{C}  ╠══════════════════════════════════════════════════════╣{RS}")
    print(f"{C}  ║{RS} {Y}[1]{RS} Single Account Full Scan          {C}         ║{RS}")
    print(f"{C}  ║{RS}     {DIM}Profile + Videos + Cross-Platform +{RS}           {C}║{RS}")
    print(f"{C}  ║{RS}     {DIM}Shadowban + Growth + Fake% + Worth{RS}            {C}║{RS}")
    print(f"{C}  ║{RS}                                                  {C}║{RS}")
    print(f"{C}  ║{RS} {Y}[2]{RS} Quick Profile Scan                 {C}         ║{RS}")
    print(f"{C}  ║{RS}     {DIM}Profile + Ban Analysis only{RS}                   {C}║{RS}")
    print(f"{C}  ║{RS}                                                  {C}║{RS}")
    print(f"{C}  ║{RS} {Y}[3]{RS} Bulk Scan               {DIM}(multiple users){RS}  {C}║{RS}")
    print(f"{C}  ║{RS} {Y}[4]{RS} Growth History          {DIM}(view saved data){RS} {C}║{RS}")
    print(f"{C}  ║{RS} {Y}[0]{RS} Exit                                 {C}         ║{RS}")
    print(f"{C}  ╚══════════════════════════════════════════════════════╝{RS}\n")

def show_growth_history():
    section("GROWTH HISTORY")
    history = load_history()
    if not history:
        print(f"\n  {Y}  No scan history saved yet. Run a scan first.{RS}")
        return
    print(f"\n  {G}  {len(history)} accounts tracked:{RS}\n")
    print(f"  {DIM}  {'Username':<22}{'Last Scan':<14}{'Followers':<14}{'Scans'}{RS}")
    sep()
    for un, data in sorted(history.items(), key=lambda x:x[1].get("timestamp",0), reverse=True):
        ts  = datetime.fromtimestamp(data.get("timestamp",0)).strftime("%Y-%m-%d")
        fol = fmt(data.get("followers",0))
        cnt = len(data.get("scans",[]))
        print(f"  {C}  @{un:<21}{DIM}{ts:<14}{G}{fol:<14}{Y}{cnt} scans{RS}")

def main():
    history = load_history()
    while True:
        main_menu()
        try:
            choice = input(f"  {C}  Select option: {W}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == "0":
            print(f"\n  {G}  Bangladesh Cyber Spectre — CEO: Ochena Gamer{RS}\n")
            break

        elif choice == "2":
            # Quick scan
            banner()
            section("QUICK PROFILE SCAN")
            try:
                raw = input(f"\n  {C}  TikTok username: {W}@{RS}").strip()
            except (KeyboardInterrupt, EOFError): continue
            un = raw.lstrip("@").strip()
            if not un: continue
            print(f"\n  {Y}  Scanning @{un}...{RS}\n")
            d = fetch(un)
            if not d:
                print(f"  {R}  Could not fetch @{un}{RS}")
                input(f"\n  {DIM}  Press Enter...{RS}")
                continue
            show_profile(d, un)
            rs = score_report_types(d)
            show_analysis(rs, d, un)
            try:
                if input(f"  {C}  Save? [y/N]: {W}").strip().lower()=="y":
                    fname=save_report(un,d,rs)
                    print(f"  {G}  Saved: {fname}{RS}")
            except: pass
            input(f"\n  {DIM}  Press Enter to continue...{RS}")

        elif choice == "3":
            banner()
            bulk_scan()
            input(f"\n  {DIM}  Press Enter to continue...{RS}")

        elif choice == "4":
            banner()
            show_growth_history()
            # Let user pick an account for detailed growth
            try:
                un = input(f"\n  {C}  Enter username for detailed growth (Enter=skip): {W}@{RS}").strip().lstrip("@")
                if un and un.lower() in history:
                    track_growth(un, history[un.lower()], history)
            except (KeyboardInterrupt, EOFError): pass
            input(f"\n  {DIM}  Press Enter to continue...{RS}")

        elif choice == "1":
            # Full scan
            banner()
            section("FULL INTELLIGENCE SCAN")
            try:
                raw = input(f"\n  {C}  TikTok username: {W}@{RS}").strip()
            except (KeyboardInterrupt, EOFError): continue
            un = raw.lstrip("@").strip()
            if not un: continue

            print(f"\n  {Y}  Starting full scan of @{un}...{RS}\n")
            d = fetch(un)
            if not d:
                print(f"\n  {R}  Could not fetch @{un}{RS}")
                print(f"  {Y}  Troubleshoot:{RS}")
                print(f"  {W}  1. Check spelling (exact, case-sensitive){RS}")
                print(f"  {W}  2. Account must be PUBLIC{RS}")
                print(f"  {W}  3. Check internet connection{RS}")
                print(f"  {W}  4. pip install --upgrade cloudscraper{RS}")
                input(f"\n  {DIM}  Press Enter...{RS}")
                continue

            # 1. Profile
            show_profile(d, un)

            # 2. Video Intel
            sc_obj = make_scraper()
            va = None
            try:
                vid_count = int(d.get("videos",0))
                if vid_count > 0 and not d.get("private",False):
                    videos = fetch_videos(un, sc_obj, count=min(30, max(10, vid_count)))
                    if videos:
                        va = analyze_videos(videos)
                        show_video_intel(va, un)
                    else:
                        print(f"\n  {Y}  Video data not available (private or API limit){RS}")
                else:
                    print(f"\n  {Y}  Skipping video intel (no videos or private account){RS}")
            except Exception as e:
                print(f"\n  {R}  Video intel error: {e}{RS}")

            # 3. Cross-platform
            cross_found = []
            try:
                cross_found = check_cross_platform(
                    un,
                    d.get("ins_id",""),
                    d.get("twitter_id",""),
                    d.get("youtube_id","")
                )
            except Exception as e:
                print(f"\n  {R}  Cross-platform error: {e}{RS}")

            # 4. Shadowban
            shadowban_score = 0
            try:
                shadowban_score = check_shadowban(un, d)
            except Exception as e:
                print(f"\n  {R}  Shadowban check error: {e}{RS}")

            # 5. Fake follower + worth
            fake_pct = None
            try:
                # We'll capture fake_pct from estimate function
                fol=int(d.get("followers",0)); hrt=int(d.get("hearts",0))
                vid_c=int(d.get("videos",0));  flw=int(d.get("following",0))
                ad=get_age_days(d.get("createTime",0)); ver=d.get("verified",False)
                if vid_c > 0:
                    hpv=hrt/vid_c
                    actual_eng_pct=(hpv/max(fol,1))*100
                    if actual_eng_pct>20: fake_pct=max(0,10)
                    elif actual_eng_pct>10: fake_pct=10
                    elif actual_eng_pct>5: fake_pct=20
                    elif actual_eng_pct>2: fake_pct=35
                    elif actual_eng_pct>0.5: fake_pct=55
                    else: fake_pct=75
                else:
                    fake_pct=80 if fol>1000 else 40
                estimate_fake_followers(d, va)
            except Exception as e:
                print(f"\n  {R}  Fake follower analysis error: {e}{RS}")

            # 6. Ban analysis
            rs = score_report_types(d)
            show_analysis(rs, d, un)

            # 7. Growth tracking
            try:
                track_growth(un, d, history)
            except Exception as e:
                print(f"\n  {R}  Growth tracker error: {e}{RS}")

            # Save option
            try:
                if input(f"\n  {C}  Save full report? [y/N]: {W}").strip().lower()=="y":
                    fname=save_report(un, d, rs, va, fake_pct, shadowban_score, cross_found)
                    print(f"  {G}  [✓] Saved: {fname}{RS}")
            except (KeyboardInterrupt, EOFError): pass

            try:
                if input(f"\n  {C}  Scan another? [Y/n]: {W}").strip().lower()=="n":
                    print(f"\n  {G}  Bangladesh Cyber Spectre — CEO: Ochena Gamer{RS}\n")
                    break
            except (KeyboardInterrupt, EOFError): break

        else:
            print(f"\n  {R}  Invalid option.{RS}")
            time.sleep(1)

if __name__=="__main__":
    main()
