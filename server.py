import json, os, sys, datetime, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

def R(id,title,client,program,stage,cand="",l1=0,note="",stale=False):
    return dict(id=id,title=title,client=client,program=program,stage=stage,candidate=cand,l1=l1,note=note,stale=stale)

SEED = [
 R("inf","Informatica PowerCenter Migration Architect / Lead","Sallie Mae","Informatica","Rate discussion","Chiranjeevi",0,"Rate discussion with HR"),
 R("snow","Snowflake Integration Engineer / Senior Engineer (Openflow, dbt & Native Snowflake)","Sallie Mae","Informatica","Open","",0,"One L2 select rejected by HR on articulation (Fri)"),
 R("mule","MuleSoft Integration Architect / Senior Developer","Sallie Mae","Informatica","Finalized","Ankit"),
 R("pm","Project Manager / PO-Infra","Mizuho","MCP-Bruce","L2 Scheduling","Noriel",1,"Noriel L1 selected by Muso; L2 with Usha to be scheduled Monday"),
 R("tal","Technical Architect Lead","Mizuho","MCP-Bruce","Finalized","Shreyas"),
 R("azure","Azure DevOps Engineer","Mizuho","MCP-Bruce","Open"),
 R("eng","Engagement Lead / PM","Sallie Mae","Informatica","Finalized","Alex"),
 R("engtk","Engagement Lead - Tokyo","","","L1 Shortlisted","",1,"1 L1 shortlisting from Shankar Sir on Friday"),
 R("alation","Data Governance Alation Analyst (Staff Aug)","Sallie Mae","Staff Aug","Joined","Arvind"),
 R("snowsql","Data Analyst Snowflake SQL (Staff Aug)","Sallie Mae","Staff Aug","Joined","Bharath"),
 R("sai","Senior AI Engineer","Mizuho","MCP-Bruce","L1 Shortlisted","",3,"3 L1 shortlisted, L2 TBS",True),
 R("be","Backend Python Engineer","Mizuho","MCP-Bruce","L1 Shortlisted","",3,"3 L1 shortlisted, L2 TBS",True),
]
if not os.listdir(DATA):
    json.dump(SEED, open(os.path.join(DATA, datetime.date.today().isoformat() + ".json"), "w"), indent=1)

def days(): return sorted(f[:-5] for f in os.listdir(DATA) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", f))
def load(d): return json.load(open(os.path.join(DATA, d + ".json")))

class H(BaseHTTPRequestHandler):
    def send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path == "/api/all": return self.send(200, {d: load(d) for d in days()})
        if self.path in ("/", "/index.html"):
            return self.send(200, open(os.path.join(ROOT, "index.html"), "rb").read(), "text/html; charset=utf-8")
        self.send(404, {"error": "not found"})
    def do_PUT(self):
        m = re.fullmatch(r"/api/day/(\d{4}-\d{2}-\d{2})", self.path)
        if not m: return self.send(404, {"error": "bad path"})
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        json.dump(body, open(os.path.join(DATA, m.group(1) + ".json"), "w"), indent=1)
        self.send(200, {"ok": True})
    def log_message(self, *a): pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
print(f"Dashboard on http://localhost:{port}", flush=True)
ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
