import{createOpenAI}from"@ai-sdk/openai";import{generateText}from"ai";
const I="nexus-research";
const M=process.env.OPENROUTER_MODEL??"anthropic/claude-sonnet-4-5";
const log=(m)=>console.log("["+new Date().toISOString()+"]["+I+"] "+m);
const or=createOpenAI({baseURL:"https://openrouter.ai/api/v1",apiKey:process.env.OPENROUTER_API_KEY??"",headers:{"HTTP-Referer":"https://nexus-capital.ai","X-Title":I}});

const TOPICS=[
  "best passive income online 2026 with AI automation",
  "crypto trading bots DeFi yield that actually work",
  "monetize AI agents for recurring revenue",
  "highest commission affiliate niches 2026",
  "digital products vs micro-SaaS for solo founder",
  "AI freelance skills highest hourly rate 2026",
  "crypto yield farming staking opportunities now",
  "build and sell AI micro-SaaS in 30 days",
  "dropshipping with AI automation 2026",
  "newsletter and content income with AI tools"
];

let cycle=0;
const findings=[];

async function getMarketSnapshot(){
  try{
    const r=await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&price_change_percentage=24h");
    const data=await r.json();
    // Fix: ensure data is an array before mapping
    if(!Array.isArray(data)) return "Market data unavailable";
    return data.map(c=>c.symbol.toUpperCase()+": $"+c.current_price+" ("+c.price_change_percentage_24h?.toFixed(1)+"%)").join(", ");
  }catch(e){ return "Market data unavailable"; }
}

async function research(topic,marketSnap){
  const{text}=await generateText({model:or(M),max_tokens:700,
    prompt:"You are NEXUS Capital research AI for Alejandro building automated income.\n\nCurrent market: "+marketSnap+"\n\nTOPIC: "+topic+"\n\nFormat EXACTLY:\nSCORE: [1-10]/10\nSTARTUP_COST: [$]\nTIME_TO_FIRST_$: [weeks]\nMONTHLY_POTENTIAL: [$X-$Y]\nAUTOMATION: [fully/semi/manual]\nSTEP_1: [action today]\nSTEP_2: [action this week]\nSTEP_3: [action this month]\nRISK: [one sentence]\nVERDICT: [2 honest sentences - worth it for Alejandro right now or not]"});
  const score=parseInt((text.match(/SCORE:\s*(\d+)/)||["","5"])[1])||5;
  return{text,score};
}

async function masterReport(){
  const top=[...findings].sort((a,b)=>b.score-a.score);
  const{text}=await generateText({model:or(M),max_tokens:900,
    prompt:"You are NEXUS Capital chief strategist for Alejandro (solo founder, AI-native, wants automated income, already has APEX trading agent + research agent live on Railway).\n\nCompleted research:\n"+top.map((f,i)=>"[RANK #"+(i+1)+" SCORE "+f.score+"/10]\n"+f.topic+"\n"+f.text.substring(0,300)).join("\n---\n")+"\n\nCreate actionable plan:\n1. TOP 5 OPPORTUNITIES ranked for Alejandro specifically\n2. POWER COMBO: best 2-3 to stack together\n3. 30-DAY SPRINT: week by week what to build\n4. THIS WEEK: one thing to start TODAY for money within 7 days"});
  log("\n"+"=".repeat(60));
  log("NEXUS MASTER OPPORTUNITY REPORT:");
  log(text);
  log("=".repeat(60));
}

async function run(){
  cycle++;
  const topic=TOPICS[(cycle-1)%TOPICS.length];
  log("━".repeat(55));
  log("RESEARCH CYCLE #"+cycle+" | "+topic);
  try{
    const snap=await getMarketSnapshot();
    log("MARKET: "+snap);
    const{text,score}=await research(topic,snap);
    findings.push({topic,text,score});
    log("SCORE: "+score+"/10\n"+text);
    log("COVERED: "+findings.length+"/"+TOPICS.length);
    if(findings.length>0&&findings.length%TOPICS.length===0){
      log("ALL TOPICS DONE - generating NEXUS MASTER REPORT...");
      await masterReport();
    }
  }catch(e){log("ERR: "+e.message);}
}

log("▶ NEXUS RESEARCH AGENT v2 ONLINE - bug fixed");
log("Scanning "+TOPICS.length+" income opportunities every 15min");
run();
setInterval(run,900000);