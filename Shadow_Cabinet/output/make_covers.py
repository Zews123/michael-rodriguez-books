#!/usr/bin/env python3
"""
Professional book cover generator for "The Shadow Cabinet"
Canvas-design skill: meticulous, master-level craftsmanship
6"x9" at 300 DPI = 1800x2700 px
"""
import sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

W, H = 1800, 2700

BASKERVILLE       = '/System/Library/Fonts/Supplemental/Baskerville.ttc'
HN                = '/System/Library/Fonts/HelveticaNeue.ttc'
COURIER           = '/System/Library/Fonts/Courier.ttc'
GEORGIA_ITALIC    = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'

def fnt(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

def text_height(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[3] - b[1]

def text_width(draw, text, font, tracking=0):
    if tracking == 0:
        b = draw.textbbox((0, 0), text, font=font)
        return b[2] - b[0]
    total = sum(draw.textbbox((0,0),c,font=font)[2]-draw.textbbox((0,0),c,font=font)[0]
                for c in text) + tracking * (len(text)-1)
    return total

def draw_centered(draw, text, y, font, fill, img_w=W):
    b = draw.textbbox((0, 0), text, font=font)
    x = (img_w - (b[2]-b[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return b[3] - b[1]

def draw_tracked(draw, text, cx, y, font, fill, tracking=0):
    if not text: return 0
    chars = list(text)
    widths = [draw.textbbox((0,0),c,font=font)[2]-draw.textbbox((0,0),c,font=font)[0] for c in chars]
    total_w = sum(widths) + tracking * (len(chars)-1)
    x = cx - total_w // 2
    for i, c in enumerate(chars):
        draw.text((x, y), c, font=font, fill=fill)
        x += widths[i] + tracking
    b = draw.textbbox((0,0), chars[0], font=font)
    return b[3]-b[1]


# ════════════════════════════════════════════════════════════════════════════
# COVER 1: "THE LONG CORRIDOR"
# ════════════════════════════════════════════════════════════════════════════
def make_cover1():
    img = Image.new('RGB', (W, H), (10, 14, 23))
    draw = ImageDraw.Draw(img)

    cx, vx = W//2, W//2
    vy = int(H * 0.34)

    # ── Wall gradient: bright center-left and center-right → dark edges ──
    for px in range(W):
        t = abs(px - cx) / cx          # 0 at center, 1 at edge
        shade = int(16 + 58 * (1-t)**1.5)
        r, g, b = int(shade*0.84), int(shade*0.86), shade
        draw.line([(px, 0), (px, H)], fill=(r, g, b), width=1)

    # ── Polished marble floor (bright center corridor) ────────────────────
    for y in range(vy, H):
        t = (y - vy) / (H - vy)
        hw = int((W//2) * t)
        shade = int(22 + 72 * t**0.55)
        r,g,b = int(shade*0.85), int(shade*0.87), shade
        draw.line([(cx-hw, y), (cx+hw, y)], fill=(r,g,b), width=1)

    # Floor grout
    for row in range(1,22):
        frac = (row/22)**1.5
        ty = int(vy + (H-vy)*frac)
        hw = int((W//2)*(ty-vy)/(H-vy))
        draw.line([(cx-hw,ty),(cx+hw,ty)], fill=(18,22,30), width=2)
    for vl in range(1,14):
        t = vl/14
        draw.line([(int(W*t),H),(vx,vy)], fill=(18,22,30), width=1)

    # ── Ceiling ───────────────────────────────────────────────────────────
    for y in range(vy):
        t = 1 - y/vy
        v = int(12 + 40*(1-t)**1.2)
        draw.line([(0,y),(W,y)], fill=(v,v,v+2), width=1)
    for row in range(1,10):
        frac = (row/10)**1.5
        ty = int(vy - vy*frac)
        hw = int((W//2)*(vy-ty)/vy)
        draw.line([(cx-hw,ty),(cx+hw,ty)], fill=(18,18,22), width=1)

    # ── Columns (7 pairs, perspective recession) ──────────────────────────
    for ci in range(7):
        frac = ((ci+0.5)/7)**1.1
        col_floor = int(vy + (H-vy)*frac)
        lxc = int((W//2)*frac)           # column x-center on left side
        col_w = max(5, int(W*0.055*(1-frac*0.68)))
        bright = int(42 + 100*(1-frac)**0.75)
        shadow = max(10, bright-35)

        # left column
        clx = lxc - col_w//2
        draw.rectangle([clx, vy, clx+int(col_w*0.78), col_floor], fill=(bright,bright+2,bright+6))
        draw.rectangle([clx+int(col_w*0.78), vy, clx+col_w, col_floor], fill=(shadow,shadow,shadow+2))
        ch = max(12, int(col_w*0.55))
        draw.rectangle([clx-ch//3,vy,clx+col_w+ch//3,vy+ch], fill=(bright+12,bright+14,bright+18))
        bh = max(8, int(col_w*0.4))
        draw.rectangle([clx-bh//4,col_floor-bh,clx+col_w+bh//4,col_floor], fill=(bright-8,bright-6,bright))

        # right column (mirror)
        rrx = W - lxc - col_w//2
        draw.rectangle([rrx+int(col_w*0.22),vy,rrx+col_w,col_floor], fill=(bright,bright+2,bright+6))
        draw.rectangle([rrx,vy,rrx+int(col_w*0.22),col_floor], fill=(shadow,shadow,shadow+2))
        draw.rectangle([rrx-ch//3,vy,rrx+col_w+ch//3,vy+ch], fill=(bright+12,bright+14,bright+18))
        draw.rectangle([rrx-bh//4,col_floor-bh,rrx+col_w+bh//4,col_floor], fill=(bright-8,bright-6,bright))

    # ── Overhead ceiling light strip ──────────────────────────────────────
    for y in range(0, vy):
        t = y/vy
        sv = int(90*(1-t)**0.7)
        draw.rectangle([cx-28,y,cx+28,y+1], fill=(sv+35,sv+25,sv+8))

    # ── Warm amber glow (door at vanishing point) ─────────────────────────
    for radius in range(500, 0, -4):
        t = 1 - radius/500
        gv = t**2.0
        r = min(255, int(10+200*gv))
        g = min(255, int(14+100*gv))
        b = max(0, int(23-18*gv))
        draw.ellipse([vx-radius, vy-int(radius*0.55), vx+radius, vy+int(radius*0.42)],
                     fill=(r,g,b))

    # Door
    dw, dh = 88, 220
    dx, dy = vx-dw//2, vy-int(dh*0.62)
    draw.rectangle([dx-12,dy-5,dx+dw+12,dy+dh+5], fill=(6,4,2))
    for ddy in range(dh):
        t = ddy/dh
        bv = int(255*(1-t*0.28))
        draw.rectangle([dx,dy+ddy,dx+dw,dy+ddy+1],
                       fill=(bv, int(bv*0.58), int(bv*0.15)))
    # Ajar shadow
    draw.polygon([(dx,dy),(dx+dw//3,dy),(dx+dw//5,dy+dh),(dx,dy+dh)],
                 fill=(10,6,2))

    # ── Smooth gradient: bottom text zone → pure bg ───────────────────────
    text_start = int(H*0.50)
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    ov_draw = ImageDraw.Draw(overlay)
    for y in range(text_start, H):
        t = (y-text_start)/(H-text_start)
        a = int(255*min(1.0, t*1.55))
        ov_draw.line([(0,y),(W,y)], fill=(10,14,23,a))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # ── Film grain (subtle) ───────────────────────────────────────────────
    rng = random.Random(42)
    for _ in range(W*H//22):
        gx,gy = rng.randint(0,W-1), rng.randint(0,H-1)
        gv = rng.randint(0,18)
        px = img.getpixel((gx,gy))
        img.putpixel((gx,gy),(min(255,px[0]+gv),min(255,px[1]+gv),min(255,px[2]+gv)))
    draw = ImageDraw.Draw(img)

    # ── TYPOGRAPHY ────────────────────────────────────────────────────────
    gold = (212, 175, 55)
    silver = (160, 165, 176)
    white = (255, 255, 255)

    ty = int(H*0.555)
    f_the = fnt(BASKERVILLE, 64, index=1)
    draw_tracked(draw, "T H E", cx, ty, f_the, gold, tracking=18)
    ty += text_height(draw,"THE",f_the) + 24

    f_title = fnt(BASKERVILLE, 152, index=1)
    draw_tracked(draw,"S H A D O W", cx, ty, f_title, gold, tracking=22)
    ty += text_height(draw,"SHADOW",f_title) + 18
    draw_tracked(draw,"C A B I N E T", cx, ty, f_title, gold, tracking=20)
    ty += text_height(draw,"CABINET",f_title) + 58

    f_sub = fnt(GEORGIA_ITALIC, 52, index=0)
    draw_centered(draw,"Conspiracy, Power, and the", ty, f_sub, silver)
    ty += text_height(draw,"Conspiracy",f_sub)+14
    draw_centered(draw,"Architecture of Hidden Control", ty, f_sub, silver)
    ty += text_height(draw,"Architecture",f_sub) + 68

    # Gold ornamental divider ──◆──
    div_cx, div_y = cx, ty
    draw.line([(div_cx-265,div_y+14),(div_cx-24,div_y+14)], fill=gold, width=2)
    draw.line([(div_cx+24,div_y+14),(div_cx+265,div_y+14)], fill=gold, width=2)
    ds = 10
    draw.polygon([(div_cx,div_y+4),(div_cx+ds,div_y+14),(div_cx,div_y+24),(div_cx-ds,div_y+14)], fill=gold)

    # Author
    f_auth = fnt(BASKERVILLE, 58, index=0)
    auth_y = H - 190
    draw_tracked(draw,"M I C H A E L", cx, auth_y, f_auth, white, tracking=14)
    auth_y += text_height(draw,"MICHAEL",f_auth)+18
    draw_tracked(draw,"R O D R I G U E Z", cx, auth_y, f_auth, white, tracking=14)

    img.save('/Users/zews/Book/Shadow_Cabinet/output/Cover_1_Corridor_v3.png', 'PNG', dpi=(300,300))
    print('Saved Cover 1')


# ════════════════════════════════════════════════════════════════════════════
# COVER 2: "THE REDACTED FILE"
# ════════════════════════════════════════════════════════════════════════════
def make_cover2():
    parchment = (245, 240, 232)
    img = Image.new('RGB', (W, H), parchment)
    draw = ImageDraw.Draw(img)

    # Ruled lines
    for y in range(0, H, 72):
        draw.line([(120,y),(W-120,y)], fill=(224,216,204), width=1)

    # Seal watermark
    scx, scy, sr = W//2, int(H*0.38), 310
    sc = (215,206,192)
    draw.ellipse([(scx-sr,scy-sr),(scx+sr,scy+sr)], outline=sc, width=2)
    draw.ellipse([(scx-sr+22,scy-sr+22),(scx+sr-22,scy+sr-22)], outline=sc, width=2)
    for a in range(0,360,30):
        rad = math.radians(a)
        x1=scx+int((sr-22)*math.cos(rad)); y1=scy+int((sr-22)*math.sin(rad))
        x2=scx+int((sr-55)*math.cos(rad)); y2=scy+int((sr-55)*math.sin(rad))
        draw.line([(x1,y1),(x2,y2)], fill=sc, width=1)
    draw.line([(scx-80,scy),(scx+80,scy)], fill=sc, width=2)
    draw.line([(scx,scy-100),(scx,scy+100)], fill=sc, width=2)
    for a in range(0,360,72):
        rad=math.radians(a)
        x=scx+int(50*math.cos(rad)); y=scy+int(50*math.sin(rad))
        draw.ellipse([(x-5,y-5),(x+5,y+5)], fill=sc)

    # CLASSIFIED stamp
    stamp_img = Image.new('RGBA', (610,185),(0,0,0,0))
    sd = ImageDraw.Draw(stamp_img)
    fs = fnt(HN,90,index=1)
    sd.rectangle([4,4,606,181], outline=(196,69,54,38), width=4)
    sd.text((28,22),"CLASSIFIED",font=fs,fill=(196,69,54,42))
    stamp_rot = stamp_img.rotate(15,expand=True,resample=Image.BICUBIC)
    img.paste(stamp_rot,(W-590,35),stamp_rot)

    near_black=(26,26,26); dark_grey=(58,58,58); cx=W//2

    # THE
    f_the=fnt(BASKERVILLE,74,index=1)
    ty=int(H*0.30)
    draw_tracked(draw,"T H E",cx,ty,f_the,near_black,tracking=22)
    ty+=text_height(draw,"THE",f_the)+30

    # SHADOW with redaction bar
    f_lg=fnt(BASKERVILLE,170,index=1)
    shadow_text="S H A D O W"
    shadow_bw=text_width(draw,shadow_text,f_lg,tracking=22)
    shadow_x=cx-shadow_bw//2
    shadow_h=text_height(draw,"SHADOW",f_lg)
    draw_tracked(draw,shadow_text,cx,ty,f_lg,(78,78,78),tracking=22)
    # Redaction bar
    bpad=28
    by1=ty+int(shadow_h*0.07); by2=ty+int(shadow_h*0.93)
    bx1=shadow_x-bpad; bx2=shadow_x+shadow_bw+bpad
    draw.rectangle([bx1,by1,bx2-10,by2],fill=(0,0,0))
    rng2=random.Random(7)
    for ddy in range(by1,by2,3):
        off=rng2.randint(-4,4)
        draw.line([(bx2-14+off,ddy),(bx2+off,ddy)],fill=(0,0,0),width=3)
    ty+=shadow_h+26

    # CABINET
    draw_tracked(draw,"C A B I N E T",cx,ty,f_lg,near_black,tracking=22)
    ty+=text_height(draw,"CABINET",f_lg)+78

    # Subtitle Courier
    f_sub=fnt(COURIER,52,index=0)
    draw_centered(draw,"Conspiracy, Power, and the",ty,f_sub,dark_grey)
    ty+=text_height(draw,"Conspiracy",f_sub)+14
    draw_centered(draw,"Architecture of Hidden Control_",ty,f_sub,dark_grey)

    # Author
    f_auth=fnt(BASKERVILLE,60,index=0)
    auth_y=H-215
    draw_tracked(draw,"MICHAEL RODRIGUEZ",cx,auth_y,f_auth,near_black,tracking=20)

    # DECLASSIFIED box
    f_dec=fnt(COURIER,35,index=0)
    dec_text="DECLASSIFIED"
    dw2=text_width(draw,dec_text,f_dec)
    dx2=cx-dw2//2
    dec_y=H-125
    draw.rectangle([dx2-14,dec_y-7,dx2+dw2+14,dec_y+46],outline=(100,80,70),width=2)
    draw.text((dx2,dec_y),dec_text,font=f_dec,fill=(100,80,70))

    draw.line([(120,60),(W-120,60)],fill=(200,190,178),width=1)
    draw.line([(120,H-60),(W-120,H-60)],fill=(200,190,178),width=1)

    img.save('/Users/zews/Book/Shadow_Cabinet/output/Cover_2_Redacted_v3.png','PNG',dpi=(300,300))
    print('Saved Cover 2')


# ════════════════════════════════════════════════════════════════════════════
# COVER 3: "THE ARCHITECTURE OF POWER"
# ════════════════════════════════════════════════════════════════════════════
def make_cover3():
    img = Image.new('RGB', (W, H), (13,17,23))
    draw = ImageDraw.Draw(img)

    photo_h = int(H * 0.52)   # photo zone

    # Sky gradient: overexposed top → dark at photo bottom
    for y in range(photo_h):
        t = y/photo_h
        if t < 0.18:   v = int(240 - t*160)
        elif t < 0.55: v = int(211 - (t-0.18)*310)
        else:          v = int(96  - (t-0.55)*240)
        v = max(13, min(255,v))
        img.paste((v,v,v+2),[0,y,W,y+1])

    # Columns (7, low-angle perspective)
    configs=[
        (0.00,0.115,0.00,0.05),(0.13,0.100,0.02,0.02),(0.25,0.090,0.04,0.00),
        (0.37,0.085,0.055,0.00),(0.50,0.085,0.055,0.00),(0.62,0.090,0.04,0.00),
        (0.74,0.100,0.02,-0.02),(0.88,0.115,0.00,-0.05)
    ]
    bbot = photo_h
    for bxf,bwf,topf,_ in configs:
        bx=int(W*bxf); bw=int(W*bwf); ty2=int(H*topf)
        for xoff in range(bw):
            t2=xoff/bw
            bright=int(52+105*math.sin(math.pi*t2)**0.65)
            for y in range(ty2,bbot):
                vt=(y-ty2)/(bbot-ty2)
                v=max(12,int(bright*(1-vt*0.38)))
                img.putpixel((bx+xoff,y),(v,v,v+1))
        # Capital
        cph=max(22,int(bw*0.55)); cpe=int(bw*0.14)
        draw.rectangle([bx-cpe,ty2,bx+bw+cpe,ty2+cph],fill=(168,168,170))
        draw.rectangle([bx-cpe//2,ty2+cph,bx+bw+cpe//2,ty2+cph+cph//2],fill=(148,148,150))
        # Base
        bh2=max(18,int(bw*0.38)); be=int(bw*0.1)
        draw.rectangle([bx-be,bbot-bh2,bx+bw+be,bbot],fill=(155,155,157))

    # Entablature
    enth=int(H*0.055)
    draw.rectangle([0,0,W,enth],fill=(185,185,187))
    draw.rectangle([0,enth,W,enth+int(enth*0.38)],fill=(168,168,170))

    # Overexposed top 14%
    for y in range(int(H*0.14)):
        alpha=int(255*(1-y/(H*0.14))**1.4)
        for x in range(W):
            px=img.getpixel((x,y))
            img.putpixel((x,y),tuple(min(255,int(c+(255-c)*alpha/255)) for c in px))

    # Documentary grain (photo zone only)
    rng=random.Random(99)
    for _ in range(W*photo_h//12):
        gx=rng.randint(0,W-1); gy=rng.randint(0,photo_h-1)
        gv=rng.randint(0,35)
        px=img.getpixel((gx,gy))
        img.putpixel((gx,gy),(min(255,px[0]+gv//5),min(255,px[1]+gv//5),min(255,px[2]+gv//5)))

    draw=ImageDraw.Draw(img)

    # Red triangle annotation
    red=(196,30,36)
    tcx=int(W*0.5); tty=int(H*0.07); tby=int(H*0.41); tw=int(W*0.20)
    pts=[(tcx,tty),(tcx-tw,tby),(tcx+tw,tby)]
    draw.line([pts[0],pts[1]],fill=red,width=4)
    draw.line([pts[0],pts[2]],fill=red,width=4)
    draw.line([pts[1],pts[2]],fill=red,width=4)
    for pt in pts:
        draw.ellipse([(pt[0]-8,pt[1]-8),(pt[0]+8,pt[1]+8)],fill=red)

    # Hard-cut black band
    band_y=photo_h
    draw.rectangle([0,band_y,W,H],fill=(0,0,0))
    draw.line([(0,band_y),(W,band_y)],fill=red,width=4)

    # TYPOGRAPHY in black band
    white=(255,255,255); silver=(176,181,191); lm=100

    f_auth_sm=fnt(HN,44,index=0)
    auth_y=band_y+58
    draw.text((lm,auth_y),"MICHAEL RODRIGUEZ",font=f_auth_sm,fill=(195,200,210))

    f_title=fnt(HN,168,index=1)
    ty3=auth_y+text_height(draw,"M",f_auth_sm)+32
    draw.text((lm,ty3),"THE SHADOW",font=f_title,fill=white)
    ty3+=text_height(draw,"THE SHADOW",f_title)+12
    draw.text((lm,ty3),"CABINET",font=f_title,fill=white)
    ty3+=text_height(draw,"CABINET",f_title)+38

    f_sub=fnt(HN,50,index=7)
    draw.text((lm,ty3),"Conspiracy, Power, and the",font=f_sub,fill=silver)
    ty3+=text_height(draw,"Conspiracy",f_sub)+12
    draw.text((lm,ty3),"Architecture of Hidden Control",font=f_sub,fill=silver)

    img.save('/Users/zews/Book/Shadow_Cabinet/output/Cover_3_Architecture_v3.png','PNG',dpi=(300,300))
    print('Saved Cover 3')


# ════════════════════════════════════════════════════════════════════════════
# COVER 4: "POWER STRUCTURE"
# ════════════════════════════════════════════════════════════════════════════
def make_cover4():
    img=Image.new('RGB',(W,H),(0,0,0))
    draw=ImageDraw.Draw(img)

    # Giant ghost SHADOW text
    f_giant=fnt(HN,530,index=4)
    charcoal=(24,24,24)
    gb=draw.textbbox((0,0),"SHADOW",font=f_giant)
    gw=gb[2]-gb[0]; gh=gb[3]-gb[1]
    gx=(W-gw)//2-25; gy=(H-gh)//2-60
    draw.text((gx,gy),"SHADOW",font=f_giant,fill=charcoal)

    # Network
    teal_muted=(45,74,62); teal_node=(61,139,110); teal_bright=(91,191,160)
    rng=random.Random(7)
    nm_yt=int(H*0.12); nm_yb=int(H*0.80); nm_x=90
    nodes=[(rng.randint(nm_x,W-nm_x),rng.randint(nm_yt,nm_yb)) for _ in range(44)]
    drawn=set()
    for i,(nx,ny) in enumerate(nodes):
        dists=sorted([(math.hypot(nx-ox,ny-oy),j) for j,(ox,oy) in enumerate(nodes) if j!=i])
        for dist,j in dists[:3]:
            if dist<430 and (min(i,j),max(i,j)) not in drawn:
                drawn.add((min(i,j),max(i,j)))
                draw.line([(nx,ny),nodes[j]],fill=teal_muted,width=1)
    for i,(nx,ny) in enumerate(nodes):
        r=rng.choice([3,4,4,5,6,7])
        draw.ellipse([(nx-r,ny-r),(nx+r,ny+r)],fill=teal_node)
        if i%7==0:
            draw.ellipse([(nx-r-3,ny-r-3),(nx+r+3,ny+r+3)],outline=teal_bright,width=1)

    # Author top
    off_white=(232,232,232); cx=W//2; lm=95
    f_auth=fnt(HN,46,index=10)
    auth_y=95
    draw_tracked(draw,"MICHAEL RODRIGUEZ",cx,auth_y,f_auth,(210,210,210),tracking=14)
    line_y=auth_y+text_height(draw,"M",f_auth)+22
    draw.line([(lm,line_y),(W-lm,line_y)],fill=teal_muted,width=1)

    # Title block lower third
    ty=int(H*0.625)
    f_sm=fnt(HN,90,index=1)
    f_lg=fnt(HN,175,index=1)
    draw.text((lm,ty),"THE",font=f_sm,fill=off_white)
    ty+=text_height(draw,"THE",f_sm)+10
    draw.text((lm,ty),"SHADOW",font=f_lg,fill=teal_bright)
    ty+=text_height(draw,"SHADOW",f_lg)+10
    draw.text((lm,ty),"CABINET",font=f_lg,fill=off_white)
    ty+=text_height(draw,"CABINET",f_lg)+42

    f_sub=fnt(HN,48,index=7)
    draw.text((lm,ty),"Conspiracy, Power, and the",font=f_sub,fill=teal_node)
    ty+=text_height(draw,"Conspiracy",f_sub)+12
    draw.text((lm,ty),"Architecture of Hidden Control",font=f_sub,fill=teal_node)

    img.save('/Users/zews/Book/Shadow_Cabinet/output/Cover_4_Network_v3.png','PNG',dpi=(300,300))
    print('Saved Cover 4')


if __name__=='__main__':
    covers = sys.argv[1:] if len(sys.argv)>1 else ['all']
    if 'all' in covers or '1' in covers:
        print('Generating Cover 1...')
        make_cover1()
    if 'all' in covers or '2' in covers:
        print('Generating Cover 2...')
        make_cover2()
    if 'all' in covers or '3' in covers:
        print('Generating Cover 3...')
        make_cover3()
    if 'all' in covers or '4' in covers:
        print('Generating Cover 4...')
        make_cover4()
    print('Done.')
