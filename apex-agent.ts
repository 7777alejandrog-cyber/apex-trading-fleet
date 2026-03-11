import{createOpenAI}from"@ai-sdk/openai";import{generateText}from"ai";
const I=process.env.APEX_INSTANCE_NAME??"apex";
const M=process.env.OPENROUTER_MODEL??"anthropic/claude-sonnet-4-5";
const P=process.env.PAPER_TRADE!=="false";
const log=m=>console.log("["+new Date().toISOString()+"]["+I+"] "+m);
const or=createOpenAI({baseURL:"https://openrouter.ai/api/v1",apiKey:process.env.OPENROUTER_API_KEY??"",headers:{"HTTP-Referer":"https://nexus-capital.ai","X-Title":I}});
async function run(){
  log("CYCLE START | "+M+" | paper="+P);
  const r=await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1&price_change_percentage=24h");
  const c=await r.json();
  const s=c.map(x=>x.symbol+":$"+x.current_price+"("+x.price_change_percentage_24h?.toFixed(1)+"%)").join("\n");
  const{text}=await generateText({model:or(M),prompt:"You are APEX crypto analyst.\n"+s+"\nFind top 2-3 trades. End: CYCLE_COMPLETE."});
  log(text.slice(0,400));
  log("CYCLE END");
}
log("APEX ON | paper="+P);
run().catch(e=>log("ERR:"+e));
setInterval(()=>run().catch(e=>log("ERR:"+e)),1800000);