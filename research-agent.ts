import{createOpenAI}from"@ai-sdk/openai";import{generateText}from"ai";
const I="nexus-research";
const M=process.env.OPENROUTER_MODEL??"anthropic/claude-sonnet-4-5";
const log=(m)=>console.log("["+new Date().toISOString()+"]["+I+"] "+m);
const or=createOpenAI({baseURL:"https://openrouter.ai/api/v1",apiKey:process.env.OPENROUTER_API_KEY??"",headers:{"HTTP-Referer":"https://nexus-capital.ai","X-Title":I}});

const TOPICS=[
  "best passive income streams online 2026 with AI automation",
  "crypto trading bots and DeFi yield that actually work in 2026",
  "how to monetize AI agents and tools for recurring revenue",
  "best high-commission affiliate marketing niches 2026",
  "digital products vs micro-SaaS - best for solo founder automation",
  "freelance skills that can be automated with AI for maximum ROI",
  "best crypto yield farming staking airdrops 2026",
  "how to build and sell AI-powered micro SaaS products fast",
  "dropshipping with AI product research and automated fulfillment 2026",
  "newsletter and content monetization with AI writing tools"
];

let cycle=0;
const findings=[];

async function research(topic){
  const{text}=await generateText({model:or(M),max_tokens:700,
    prompt:"You are NEXUS Capital research AI for an entrepreneur building automated online income. Analyze:\n\nTOPIC: "+topic+"\n\nExact format:\nSCORE: [1-10]/10\nSTARTUP_COST: [be specific]\nTIME_TO_REVENUE: [realistic]\nMONTHLY_POTENTIAL: [$X-$Y realistic]\nAUTOMATION_LEVEL: [fully/semi/manual]\nSTEP_1: [specific first action]\nSTEP_2: [specific second action]\nSTEP_3: [specific third action]\nRISK: [biggest risk in one sentence]\nVERDICT: [honest 2-sentence take]"});
  const score=parseInt((text.match(/SCORE:\s*(\d+)/)||["","5"])[1]);
  return{text,score};
}

async function masterReport(){
  const top=[...findings].sort((a,b)=>b.score-a.score);
  const{text}=await generateText({model:or(M),max_tokens:900,
    prompt:"You are NEXUS Capital chief strategist. Create a prioritized MASTER ACTION PLAN for building automated online income based on completed research:\n\n"+top.map((f,i)=>"[RANK #"+(i+1)+" | SCORE "+f.score+"/10]\nTOPIC: "+f.topic+"\n"+f.text.substring(0,300)).join("\n---\n")+"\n\nOutput a clear plan:\n1. TOP 5 OPPORTUNITIES ranked by automation + income potential\n2. BEST 2-3 COMBINATION to run simultaneously\n3. 30-DAY LAUNCH PLAN with week-by-week actions\n4. TOTAL REALISTIC MONTHLY INCOME if all pursued"});
  log("=".repeat(60));
  log("NEXUS MASTER OPPORTUNITY REPORT:");
  log(text);
  log("=".repeat(60));
}

async function run(){
  cycle++;
  const topic=TOPICS[(cycle-1)%TOPICS.length];
  log("━".repeat(50));
  log("RESEARCH CYCLE #"+cycle+" | "+topic);
  try{
    const{text,score}=await research(topic);
    findings.push({topic,text,score,time:new Date().toISOString()});
    log("SCORE: "+score+"/10");
    log(text);
    log("TOPICS COVERED: "+findings.length+"/"+TOPICS.length);
    if(findings.length>0&&findings.length%TOPICS.length===0){
      log("ALL TOPICS DONE - generating master report...");
      await masterReport();
    }
  }catch(e){log("ERR: "+e.message);}
}

log("▶ NEXUS RESEARCH AGENT v1 ONLINE");
log("Scanning "+TOPICS.length+" income opportunities - report every "+TOPICS.length+" cycles");
run();
setInterval(run,900000);