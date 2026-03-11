import{createOpenAI}from"@ai-sdk/openai";import{generateText}from"ai";
const I=process.env.APEX_INSTANCE_NAME??"apex";
const M=process.env.OPENROUTER_MODEL??"anthropic/claude-sonnet-4-5";
const P=process.env.PAPER_TRADE!=="false";
const WALLET=process.env.COINBASE_WALLET_ADDRESS??"";
const log=m=>console.log("["+new Date().toISOString()+"]["+I+"] "+m);
const or=createOpenAI({baseURL:"https://openrouter.ai/api/v1",apiKey:process.env.OPENROUTER_API_KEY??"",headers:{"HTTP-Referer":"https://nexus-capital.ai","X-Title":I}});

// Trade log for backtesting / win rate tracking
const tradeLog=[];
let cycleCount=0;

async function getMarketData(){
  // Get top 50 coins with 1h AND 24h price change for trend confluence
  const r=await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&price_change_percentage=1h,24h,7d");
  return await r.json();
}

async function checkWallet(){
  if(!WALLET)return;
  try{
    const r=await fetch("https://mainnet.base.org",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",method:"eth_getBalance",params:[WALLET,"latest"],id:1})});
    const d=await r.json();
    const bal=(Number(BigInt(d.result||"0x0"))/1e18).toFixed(4);
    log("WALLET "+WALLET.slice(0,10)+"... | Base ETH: "+bal);
    log("TRADE READY: "+(parseFloat(bal)>0?"YES":"NO - fund wallet to enable live trades"));
  }catch(e){log("WALLET ERR: "+e.message);}
}

async function run(){
  cycleCount++;
  log("━".repeat(50));
  log("CYCLE #"+cycleCount+" | "+M+" | paper="+P);
  
  const coins=await getMarketData();
  
  // Build rich market context with multi-timeframe data
  const mkd=coins.map(c=>{
    const h1=c.price_change_percentage_1h_in_currency?.toFixed(2)??"?";
    const h24=c.price_change_percentage_24h?.toFixed(2)??"?";
    const d7=c.price_change_percentage_7d_in_currency?.toFixed(2)??"?";
    const vol=c.total_volume>1e9?(c.total_volume/1e9).toFixed(1)+"B":(c.total_volume/1e6).toFixed(0)+"M";
    return c.symbol.toUpperCase()+":$"+c.current_price+" | 1h:"+h1+"% 24h:"+h24+"% 7d:"+d7+"% vol:"+vol;
  }).join("\n");

  const prompt=`You are APEX, a professional crypto trading AI trained on the following risk management principles:

TRADING RULES (MANDATORY):
1. CONFLUENCE REQUIRED: Only signal trades where 1h + 24h + 7d momentum ALL agree on direction
2. TREND ALIGNMENT: Only trade WITH the prevailing trend - never counter-trend
3. RISK/REWARD: Only take setups with minimum 2:1 reward-to-risk ratio
4. POSITION SIZING: Max 2% account risk per trade
5. VOLUME CONFIRMATION: High volume must support the move (not low-volume fakeouts)
6. AVOID: Coins with contradictory timeframe signals (e.g. 1h up but 7d down = skip)

MARKET DATA (1h | 24h | 7d | volume):
${mkd}

TASK: Identify 1-3 HIGH CONFLUENCE setups only. If no clear confluence exists, say "NO TRADE - waiting for confluence."

For each valid trade output EXACTLY:
SIGNAL: [COIN] | [LONG/SHORT] | Entry: ~$[price] | Target: $[target] | Stop: $[stop] | R:R [ratio] | Confidence: [%] | Reason: [confluence factors]

End with: CYCLE_COMPLETE`;

  const{text}=await generateText({model:or(M),max_tokens:600,prompt});
  
  log("ANALYSIS:\n"+text);
  
  // Parse and log signals for backtesting
  const signals=text.match(/SIGNAL:.*$/gm)||[];
  signals.forEach(s=>{
    tradeLog.push({cycle:cycleCount,time:new Date().toISOString(),signal:s,result:"OPEN"});
    log("LOGGED: "+s);
  });
  
  log("SIGNALS THIS CYCLE: "+signals.length);
  log("TOTAL LOGGED TRADES: "+tradeLog.length);
  log("CYCLE #"+cycleCount+" END | next in 30min");
}

log("▶ APEX v2 ONLINE | Graystone Method | paper="+P);
log("wallet="+WALLET.slice(0,10)+"...");
checkWallet().then(()=>run()).catch(e=>log("BOOT ERR: "+e.message));
setInterval(()=>run().catch(e=>log("ERR: "+e.message)),1800000);