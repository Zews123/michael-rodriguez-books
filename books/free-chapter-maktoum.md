---
permalink: /books/free-chapter-maktoum/
layout: default
title: "Free Chapter — Maktoum by Michael Rodriguez"
description: "Read the Introduction of Maktoum free — the 2018 yacht interception, the word that means hidden, the family that built Dubai. Get Chapter 1 as EPUB."
canonical_url: "https://michaelrodriguezbooks.com/books/free-chapter-maktoum/"
image: "https://michaelrodriguezbooks.com/assets/images/Maktoum.webp"
date: 2026-05-22
---

<link rel="preload" href="{{ site.baseurl }}/assets/images/Maktoum.webp" as="image" type="image/webp">

<!-- Open Graph -->
<meta property="og:type" content="book">
<meta property="og:title" content="Free Chapter — Maktoum by Michael Rodriguez">
<meta property="og:description" content="Read the Introduction of Maktoum free — the 2018 yacht interception, the family that built Dubai, and the word that means hidden.">
<meta property="og:image" content="https://michaelrodriguezbooks.com/assets/images/Maktoum.webp">
<meta property="og:url" content="https://michaelrodriguezbooks.com/books/free-chapter-maktoum/">

# Maktoum — Free Preview

**Read the full Introduction below.** A princess in the engine room of a yacht. Commandos in international waters. The Arabic word for *hidden*. The family that built Dubai doesn't want you to know what they sealed. Subscribe below to get the Introduction + Chapter 1 free as EPUB.

<img src="{{ site.baseurl }}/assets/images/Maktoum.webp" alt="Maktoum by Michael Rodriguez" width="220" height="340" style="float: right; margin: 0 0 20px 20px; border-radius: 8px;" fetchpriority="high">

---

## INTRODUCTION: The Word That Means Hidden

The night of March 4, 2018. Eighty kilometers off the coast of Goa.

A thirty-two-year-old woman was hiding in the engine room of a sixty-meter American-flagged yacht called the *Nostromo*. The yacht was named after a freighter from a 1979 horror film about something dangerous loose on a ship. The name had not been chosen by accident.

She had not eaten in two days. She had a satellite phone, a fake Irish passport, and a former French naval officer named Hervé Jaubert hiding two decks above her. The plan was simple in the way that desperate plans always are. Sail to Sri Lanka. Switch to a smaller boat. Fly to the United States. Apply for political asylum on landing.

What she did not know — what nobody on the *Nostromo* knew — was that the yacht's electronics had been compromised. Every coordinate broadcast from the navigation system since they left Oman had been read in real time by a listening station in Abu Dhabi. The Indian Coast Guard had been waiting since dawn.

Just after 10 p.m., she heard the explosion of a flashbang grenade on the upper deck. Then footsteps. Then commands shouted in three languages — Hindi, Arabic, English. By the time the soldiers dragged her up the companionway by her hair, she was screaming the only sentence she had rehearsed for this exact moment.

*I claim political asylum. I claim political asylum. I claim political asylum.*

It did not matter. The men on the deck were not Indian. The men on the deck wore the uniforms of an Emirati commando unit that, officially, was not there. They put a black hood over her head and zip-tied her wrists. Then they put her into a Zodiac and drove her, in the dark, to a waiting helicopter.

She had not been on Indian soil. She had not been in international waters either, technically. She had been on a vessel registered in the United States, in waters claimed by three different jurisdictions, in transit between two countries that had not extradited a Maktoum princess in two hundred years.

The reason they wanted her back was both simple and impossible to explain in one paragraph. Her name was Sheikha Latifa bint Mohammed Al Maktoum. Her father was Sheikh Mohammed bin Rashid Al Maktoum, ruler of Dubai, Vice President of the United Arab Emirates, prime minister of a country built on hydrocarbons that increasingly preferred not to discuss hydrocarbons, owner of approximately ninety-nine percent of a holding company called Dubai Holding, and — according to *Forbes* — somewhere between the fourteenth and twenty-second richest royal alive.

This is a book about her family.

It is also a book about a city that should not exist.

And it is a book about a word.

In classical Arabic, *maktoum* is not just a surname. It is a verb form. The root letters — *kaf*, *ta*, *meem* — describe the act of concealing, sealing, withholding. *Maktoum* means *that which is hidden, kept silent, locked away*. When an Arabic-speaking imam delivers the *fatiha* and asks God to forgive sins both visible and *maktoum*, he is asking forgiveness for the ones nobody saw. When a thirteenth-century pearl merchant labeled a chest of pearls *maktoum*, he meant: keep this sealed. Do not open it. The contents are not for daylight.

Eight hundred years later, a man named Maktoum bin Butti led eight hundred Bedouin out of Abu Dhabi to the mouth of a saltwater creek and founded the city that, two centuries later, would build the tallest building on planet earth.

The contents of his chest are about to be opened.

---

<div style="background: linear-gradient(135deg, #1a3c65 0%, #0d253f 100%); padding: 30px; border-radius: 10px; margin: 40px 0; border: 1px solid #c9a227; text-align: center;">
  <h3 style="color: #c9a227; margin-top: 0;">📚 Get Chapter 1 Free</h3>
  <p style="color: #e8e6e3; margin-bottom: 20px;">Subscribe to receive the Introduction + Chapter 1 ("Liwa Oasis") as a free EPUB — and get notified about upcoming investigations.</p>

  <div id="mk-subscribe-form" style="max-width: 480px; margin: 0 auto;">
    <input type="email" id="mk-email" placeholder="your@email.com"
           style="width:100%;padding:12px 16px;border-radius:6px;border:1px solid #c9a227;background:#0d253f;color:#fff;font-size:1rem;margin-bottom:12px;box-sizing:border-box;">
    <button onclick="mkSubscribe()"
            style="width:100%;background:#c9a227;color:#0d0d0d;padding:12px 24px;border-radius:6px;border:0;font-weight:700;font-size:1rem;cursor:pointer;">
      Get Free EPUB →
    </button>
    <p id="mk-msg" style="color:#c9a227;margin-top:12px;display:none;"></p>
  </div>
</div>

<script>
function mkSubscribe() {
  var email = document.getElementById('mk-email').value.trim();
  var msg = document.getElementById('mk-msg');
  if (!email || !email.includes('@')) {
    msg.style.display='block'; msg.textContent='Please enter a valid email address.'; return;
  }
  fetch('https://api.kit.com/v4/subscribers', {
    method: 'POST',
    headers: {'Content-Type':'application/json','X-Kit-Api-Key':'pub_1e4f38e30d10a03027bd9cae4b0cc421'},
    body: JSON.stringify({email_address: email, tags:['maktoum-lead-magnet'], state:'active'})
  }).then(function(r){ return r.json(); }).then(function(d){
    document.getElementById('mk-subscribe-form').innerHTML =
      '<p style="color:#c9a227;font-size:1.1rem;font-weight:700;">✅ Check your inbox! Your free EPUB is on its way.</p>' +
      '<p style="color:#e8e6e3;margin-top:10px;"><a href="{{ site.baseurl }}/assets/downloads/Maktoum_Chapter1.epub" style="color:#c9a227;" download>Click here if the download doesn\'t start automatically →</a></p>';
  }).catch(function(){
    msg.style.display='block'; msg.textContent='Something went wrong. Please try again.';
  });
}
</script>

---

<div style="text-align: center; margin: 40px 0;">
  <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 16px;">Ready for the full investigation?</p>
  <a href="https://www.amazon.com/Maktoum-Hidden-Dynasty-Secrets-Billionaire/dp/B0H1YLCMZD"
     style="background:#ff9900;color:#fff;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:1rem;display:inline-block;margin-right:12px;">
    📦 Buy on Amazon
  </a>
  <a href="{{ site.baseurl }}/books/Maktoum/"
     style="background:#1a3c65;color:#fff;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:1rem;display:inline-block;">
    📖 Book Details →
  </a>
</div>
