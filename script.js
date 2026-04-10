
  window.addEventListener('scroll',()=>{
    document.getElementById('mainNav').classList.toggle('solid',scrollY>60);
  });
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in');}),{threshold:.12});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

  document.getElementById('wlForm').addEventListener('submit',e=>{
    e.preventDefault();
    const b=e.target.querySelector('button');
    b.textContent='✓ You\'re on the list!';
    b.style.background='#2a6b35';
    b.disabled=true;
  });

  const ci=document.getElementById('chatInput');
  ci.addEventListener('input',()=>{ci.style.height='auto';ci.style.height=Math.min(ci.scrollHeight,120)+'px';});
  ci.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}});

  let hist=[];
  const SYS=`You are Kobo, an AI financial coach built specifically for young Nigerian professionals aged 22–35. You are sharp, warm, empathetic, and unpretentious — a knowledgeable friend, not a bank.

Key traits:
- You deeply understand Nigerian financial culture: black tax (supporting family), esusu (cooperative savings), aso-ebi (event clothing obligations), Detty December (festive spending season), multiple income streams, NYSC, side hustles
- You're comfortable with Pidgin English and Naija slang. Respond in Pidgin if the user does — otherwise use warm, clear English
- You NEVER shame people about their spending
- Use ₦ (Naira) for all amounts
- Responses: concise (2–3 short paragraphs), conversational, specific and actionable
- Use emojis naturally but sparingly
- You know: PiggyVest, Cowrywise, Kuda, Carbon, Palmcredit, Opay, Moniepoint, Mono, Flutterwave, Paystack
- Kobo's MVP is the AI financial coach. Full app (in development) connects to Nigerian banks via Mono API to predict balance 14 days ahead with 85%+ accuracy. You don't have the user's real data in this demo
- Typical salary range: ₦150k–₦1.5M/month
- Common Nigerian expense categories: rent, transport, food, subscriptions (Netflix/DSTV/Spotify), data, clothing (aso-ebi), black tax, esusu, church/tithe, informal loans

When someone says they're broke before payday: validate it, identify the most likely cause, give 2–3 specific steps.
When asked if they can afford something: give a direct answer with a naira number.
When asked to build a budget: split into needs/wants/savings practically for Lagos life.
Be the coach that makes them move from reactive to predictive.`;

  async function sendMsg(){
    const txt=ci.value.trim(); if(!txt)return;
    addMsg('usr',txt); ci.value=''; ci.style.height='auto';
    hist.push({role:'user',content:txt});
    document.getElementById('typingDots').classList.add('show');
    document.getElementById('sendBtn').disabled=true;
    scrollChat();

    setTimeout(() => {
      let reply = "I hear you! To give you the best advice, I'd need to look at your full transaction history. But generally, the best way to stop running out of money is to automatically save toward your fixed expenses the day your salary lands.";
      const lowerTxt = txt.toLowerCase();
      
      if (lowerTxt.includes("budget") && lowerTxt.includes("350")) {
        reply = "Okay so ₦350k. In Lagos, try this: ₦175k (50%) for fixed needs like rent/transport. ₦105k (30%) for yourself (flexing). ₦70k (20%) saved/invested immediately on payday. Would you like me to auto-save the ₦70k next payday?";
      } else if (lowerTxt.includes("dinner")) {
        reply = "Looking at your current trajectory, you have ₦3,400 \"safe to spend\" before your next payday. A nice dinner out is fine, but try to keep it under ₦2,500 so you're not stressed next week.";
      } else if (lowerTxt.includes("25th") || lowerTxt.includes("run out")) {
        reply = "The salary trap! 😩 It happens because we usually pay bills and flex first, then save whatever's left (which is usually nothing). Next month, let's reverse it. We'll secure your savings and fixed costs on Day 1.";
      } else if (lowerTxt.includes("detty december")) {
        reply = "Ah, Detty December! The earlier you start, the less you feel it. If we auto-save ₦25,000 every month starting now, you'll have ₦200,000 ready by November without taking loans.";
      } else if (lowerTxt.includes("emergency") || lowerTxt.includes("lagos")) {
        reply = "For a young professional in Lagos, aiming for 3 to 6 months of your absolute basic living expenses is key. If your bare minimum to survive is ₦150k/month, a full emergency fund is ₦450k-₦900k.";
      } else if (lowerTxt.includes("subscription") || lowerTxt.includes("forgetting")) {
        reply = "You're not alone! I've scanned your spending patterns and found 3 recurring charges (Netflix, Spotify, and a generic ₦4,500 charge). I can send you a WhatsApp nudge 48 hours before they renew so you can cancel them if needed. Want me to turn that on?";
      } else if (lowerTxt.includes("family") || lowerTxt.includes("30k")) {
        reply = "Black tax is real. Easiest fix: Treat that ₦30k like a fixed utility bill (like electricity). Set up an auto-transfer to your family's account on the exact day you get paid. You won't even see the money, so you won't plan your life around it.";
      }
      
      hist.push({role:'assistant',content:reply});
      document.getElementById('typingDots').classList.remove('show');
      addMsg('bot',reply);
      scrollChat();
      document.getElementById('sendBtn').disabled=false;
    }, 1200 + Math.random() * 800);
  }

  function usePrompt(el){ci.value=el.textContent;sendMsg();}

  function addMsg(role,text){
    const w=document.getElementById('chatMsgs');
    const d=document.createElement('div'); d.className=`cmsg ${role}`;
    const wh=document.createElement('div'); wh.className='cmsg-who';
    wh.textContent=role==='bot'?'Kobo':'You';
    const b=document.createElement('div'); b.className='cmsg-bub'; b.textContent=text;
    d.appendChild(wh); d.appendChild(b); w.appendChild(d); scrollChat();
  }

  function scrollChat(){const w=document.getElementById('chatMsgs');w.scrollTop=w.scrollHeight;}
