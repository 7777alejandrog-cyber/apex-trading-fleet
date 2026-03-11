import{createOpenAI}from"@ai-sdk/openai";import{generateText}from"ai";
const I=process.env.APEX_INSTANCE_NAME??"apex";
const M=process.env.OPENROUTER_MODEL??"anthropic/claude-sonnet-4-5";
const P=process.env.PAPER_TRADE!=="false";
const WALLET=process.env.COINBASE_WALLET_ADDRESS??"";
const log=m=>console.log("["+new Date().toISOString()+"]["+I+"] "+m);
const or=createOpenAI({baseURL:"https://openrouter.ai/api/v1",apiKey:process.env.OPENROUTER_API_KEY??"",headers:{"HTTP-Referer":"https://nexus-capital.ai","X-Title":I}});

async function rpc(url,method,params){
  const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",method,params,id:1})});
  const d=await r.json();
  if(!d.result)return "0";
  return (Number(BigInt(d.result))/1e18).toFixed(6);
}

async function checkWallet(){
  if(!WALLET){log("WALLET: not configured");return;}
  try{
    const eth=await rpc("https://cloudflare-eth.com","eth_getBalance",[WALLET,"latest"]);
    const base=await rpc("https://mainnet.base.org","eth_getBalance",[WALLET,"latest"]);
    log("WALLET: "+WALLET);
    log("ETH mainnet: "+eth+" ETH | Base: "+base+" ETH");
    const funded=parseFloat(eth)>0||parseFloat(base)>0;
    log("TRADE READY: "+(funded?"YES - wallet funded":"NO - send ETH to "+WALLET+" to enable live trades"));
  }catch(e){log("WALLET ERR: "+e.message);}
}

async function run(){
  log("CYCLE START | "+M+" | paper="+P);
  try{
    const r=await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1&price_change_percentage=24h");
    const c=await r.json();
    const s=c.map(x=>x.symbol.toUpperCase()+":$"+x.current_price.toLocaleString()+"("+x.price_change_percentage_24h?.toFixed(1)+"%)").join("\n");
    const{text}=await generateText({model:or(M),max_tokens:500,prompt:"You are APEX crypto trading AI.\nMarket data:\n"+s+"\n\nGive top 3 trade setups. For each: COIN | LONG or SHORT | reason | confidence%. End with CYCLE_COMPLETE."});
    log("ANALYSIS: "+text);
    log("CYCLE END - next in 30min");
  }catch(e){log("CYCLE ERR: "+e.message);}
}

log("=".repeat(40));
log("APEX ONLINE | paper="+P);
log("wallet="+WALLET.slice(0,10)+"...");
log("model="+M);
log("=".repeat(40));
checkWallet().then(()=>run());
setInterval(run,1800000);