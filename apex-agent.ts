import{createOpenAI}from"@ai-sdk/openai";import{generateText}from"ai";
const I=process.env.APEX_INSTANCE_NAME??"apex";
const M=process.env.OPENROUTER_MODEL??"anthropic/claude-sonnet-4-5";
const P=process.env.PAPER_TRADE!=="false";
const WALLET=process.env.COINBASE_WALLET_ADDRESS??"";
const log=m=>console.log("["+new Date().toISOString()+"]["+I+"] "+m);
const or=createOpenAI({baseURL:"https://openrouter.ai/api/v1",apiKey:process.env.OPENROUTER_API_KEY??"",headers:{"HTTP-Referer":"https://nexus-capital.ai","X-Title":I}});

async function checkWallet(){
  if(!WALLET){log("WALLET: not configured");return;}
  try{
    // Check ETH balance on mainnet via public RPC
    const res=await fetch("https://cloudflare-eth.com",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",method:"eth_getBalance",params:[WALLET,"latest"],id:1})});
    const d=await res.json();
    const wei=BigInt(d.result);
    const eth=(Number(wei)/1e18).toFixed(6);
    log("WALLET: "+WALLET);
    log("WALLET ETH BALANCE: "+eth+" ETH");
    // Also check Base
    const res2=await fetch("https://mainnet.base.org",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",method:"eth_getBalance",params:[WALLET,"latest"],id:1})});
    const d2=await res2.json();
    const wei2=BigInt(d2.result);
    const base=(Number(wei2)/1e18).toFixed(6);
    log("WALLET BASE BALANCE: "+base+" ETH");
    log("WALLET STATUS: "+(Number(eth)>0||Number(base)>0?"FUNDED - READY TO TRADE":"UNFUNDED - add ETH to enable live trades"));
  }catch(e){log("WALLET CHECK ERR: "+e);}
}

async function run(){
  log("CYCLE START | "+M+" | paper="+P);
  const r=await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1&price_change_percentage=24h");
  const c=await r.json();
  const s=c.map(x=>x.symbol+":$"+x.current_price+"("+x.price_change_percentage_24h?.toFixed(1)+"%)").join("\n");
  const{text}=await generateText({model:or(M),prompt:"You are APEX crypto analyst. Top 30 coins:\n"+s+"\nFind top 2-3 high-confidence trades. For each give: coin, direction (LONG/SHORT), reason, confidence 0-100. End with CYCLE_COMPLETE."});
  log("ANALYSIS:\n"+text.slice(0,600));
  log("CYCLE END");
}

log("APEX ON | paper="+P+" | wallet="+WALLET.slice(0,10)+"...");
checkWallet().then(()=>run()).catch(e=>log("ERR:"+e));
setInterval(()=>run().catch(e=>log("ERR:"+e)),1800000);