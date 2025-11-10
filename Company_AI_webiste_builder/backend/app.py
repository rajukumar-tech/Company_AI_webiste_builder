from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Configure CORS to allow specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Sample data for testing
services = [
    {
        "id": 1,
        "name": "Web Development",
        "description": "Custom web applications built with modern technologies"
    },
    {
        "id": 2,
        "name": "Mobile Development",
        "description": "Native and cross-platform mobile applications"
    },
    {
        "id": 3,
        "name": "Cloud Solutions",
        "description": "Scalable cloud infrastructure and deployments"
    }
]
#
# Endpoints:
# /                      GET  - health
# /api/pages/<pagename>  GET  - get page
# /api/admin/pages/<pagename> POST - create/update page
# /api/jobs              GET/POST - list/add jobs
# /api/apply             POST - apply for job (form-data + resume file)
# /api/portfolio/generate POST - upload resume -> create portfolio
# /api/portfolio/<id>    GET - view generated portfolio HTML
# /api/chatbot           POST - ask question
# /api/ai/seo_analyze    POST - SEO analyze text
# /api/ai/theme          POST - theme suggestion
# /api/resume/parse      POST - parse resume + score
# /api/ai/auto_build     POST - auto-build site from brief
# /api/voice/text        POST - rewrite text for narration
# /api/admin/ensure_seed GET/POST - ensure sample Mastersolis Infotech data exists
# /api/admin/applications GET - list all applications (admin)
#
# Note: For production, replace in-memory DB with persistent DB (Postgres) and add auth.

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, re, json, uuid, datetime
from pathlib import Path

# Optional OpenAI integration:
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = bool(OPENAI_KEY)
if USE_OPENAI:
    try:
        import openai
        openai.api_key = OPENAI_KEY
    except Exception:
        USE_OPENAI = False

app = Flask(__name__)
CORS(app)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# In-memory DB (demo). Keys: pages, jobs, applications, portfolios, faq, themes, blog, testimonials, analytics
DB = {
    "pages": {
        "home": {"title":"Mastersolis Infotech", "hero":"AI-driven digital presence"},
        "about": {"mission":"Empowering AI-driven innovation for modern businesses."}
    },
    "jobs": [],
    "applications": [],
    "portfolios": {},
    "faq": [],
    "themes": {},
    "blog": [],
    "testimonials": [],
    "analytics": {}
}

# ----------------------------
# Helpers
# ----------------------------
def run_openai_completion(prompt, max_tokens=200, temperature=0.7):
    """Run OpenAI Completion (davinci) with fallback stub if key is absent."""
    if not USE_OPENAI:
        # Safe stub response for offline demos
        return "OPENAI_KEY not set — stub response. Prompt head: " + (prompt[:200] + "...")
    try:
        resp = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return resp.choices[0].text.strip()
    except Exception as e:
        return f"OpenAI error: {e}"

def parse_resume_text_simple(text):
    """Very simple regex-based resume parsing for demo. Returns name, email, skills, years."""
    skills = re.findall(r"\b(Python|JavaScript|React|Django|Flask|SQL|Node|HTML|CSS|Java|C\+\+|AWS|Docker|TensorFlow)\b", text, flags=re.I)
    years = re.search(r"(\d+)\s+years?", text, flags=re.I)
    email = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    name = None
    for line in text.splitlines():
        s = line.strip()
        if s and len(s.split()) <= 4 and "@" not in s and not re.search(r"\d", s):
            name = s
            break
    return {
        "name": name or "Unknown",
        "email": email.group(0) if email else None,
        "skills": list({s.lower() for s in skills}),
        "experience_years": int(years.group(1)) if years else 0
    }

def score_resume(parsed, desired_skills=None):
    if not desired_skills:
        desired_skills = []
    desired_lower = [d.strip().lower() for d in desired_skills if d.strip()]
    matched = set(parsed.get("skills", [])) & set(desired_lower)
    skill_score = (len(matched) / max(1, len(desired_lower))) if desired_lower else 0.0
    exp_score = min(parsed.get("experience_years",0) / 5.0, 1.0)
    overall = round((skill_score * 0.7 + exp_score * 0.3) * 100, 1)
    return {"match_percent": overall, "matched_skills": list(matched)}

# ----------------------------
# Basic routes
# ----------------------------
@app.route("/")
def health():
    return jsonify({"message":"AI Website Builder Backend Running", "openai": bool(USE_OPENAI)})

@app.route("/api/pages/<pagename>", methods=["GET"])
def get_page(pagename):
    page = DB["pages"].get(pagename)
    if not page:
        return jsonify({"error":"Page not found"}), 404
    return jsonify(page)

@app.route("/api/admin/pages/<pagename>", methods=["POST"])
def admin_update_page(pagename):
    data = request.get_json() or {}
    DB["pages"][pagename] = data
    # add a simplified FAQ entry for chatbot context
    DB.setdefault("faq", []).append({"q": f"What is on the {pagename} page?", "a": json.dumps(data)})
    return jsonify({"status":"ok", "page": data})

@app.route("/api/jobs", methods=["GET","POST"])
def jobs():
    if request.method == "POST":
        job = request.get_json()
        job['id'] = job.get('id') or str(uuid.uuid4())
        DB.setdefault("jobs", []).append(job)
        return jsonify({"status":"job_added", "job": job})
    return jsonify(DB.get("jobs", []))

@app.route("/api/apply", methods=["POST"])
def apply_job():
    form = request.form.to_dict()
    file = request.files.get("resume")
    saved_path = None
    if file:
        updir = DATA_DIR/"uploads"
        updir.mkdir(exist_ok=True)
        saved_path = str(updir / file.filename)
        file.save(saved_path)
    app_entry = {
        "id": str(uuid.uuid4()),
        "name": form.get("name"),
        "email": form.get("email"),
        "job_title": form.get("job_title"),
        "resume_path": saved_path
    }
    DB.setdefault("applications", []).append(app_entry)
    # parse resume and score (simple)
    parsed = {}
    if saved_path:
        try:
            txt = Path(saved_path).read_text(errors="ignore")
            parsed = parse_resume_text_simple(txt)
        except Exception:
            parsed = {}
    desired_skills = (form.get("desired_skills") or "").split(",") if form.get("desired_skills") else []
    score = score_resume(parsed, desired_skills)
    app_entry['parsed'] = parsed
    app_entry['score'] = score
    # NOTE: Optional: send AI-generated acknowledgment email here (requires SMTP setup)
    return jsonify({"status":"received", "application": app_entry})

# ----------------------------
# Portfolio generator
# ----------------------------
@app.route("/api/portfolio/generate", methods=["POST"])
def portfolio_generate():
    file = request.files.get("resume")
    if not file:
        return jsonify({"error":"Attach resume file (form-data key 'resume')"}), 400
    updir = DATA_DIR/"uploads"
    updir.mkdir(exist_ok=True)
    path = updir / file.filename
    file.save(path)
    text = ""
    try:
        # if it's a text file, read; if binary pdf, still try a text read (may be messy)
        text = path.read_text(errors="ignore")
    except Exception:
        text = ""
    parsed = parse_resume_text_simple(text)
    if USE_OPENAI:
        prompt = f"Create a simple, clean HTML portfolio page for this candidate with name, email, skills, experience and a short intro: {parsed}"
        html = run_openai_completion(prompt, max_tokens=600)
        # sanitize minimal: ensure returned string contains html tag; if not wrap
        if "<html" not in html.lower():
            html = f"<html><body><h1>{parsed.get('name')}</h1><p>Skills: {', '.join(parsed.get('skills',[]))}</p><p>Experience: {parsed.get('experience_years')} years</p></body></html>"
    else:
        html = f"<html><body><h1>{parsed.get('name')}</h1><p>Email: {parsed.get('email') or ''}</p><p>Skills: {', '.join(parsed.get('skills',[]))}</p><p>Experience: {parsed.get('experience_years')} years</p></body></html>"
    pid = str(uuid.uuid4())
    DB.setdefault("portfolios", {})[pid] = {"html": html, "meta": parsed}
    return jsonify({"portfolio_id": pid, "preview_html": html[:800]})

@app.route("/api/portfolio/<pid>", methods=["GET"])
def portfolio_get(pid):
    rec = DB.get("portfolios", {}).get(pid)
    if not rec:
        return jsonify({"error":"Not found"}), 404
    return rec["html"], 200, {"Content-Type":"text/html; charset=utf-8"}

# ----------------------------
# Chatbot (contextual)
# ----------------------------
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json() or {}
    q = data.get("question", "")
    if not q:
        return jsonify({"error":"Provide 'question' in body"}), 400
    # Build limited context from pages and faq
    context = []
    for k,v in list(DB.get("pages", {}).items()):
        context.append(f"Page {k}: {json.dumps(v)}")
    for f in DB.get("faq", [])[-10:]:
        context.append(f"FAQ: Q:{f.get('q')} A:{f.get('a')}")
    context_text = "\n\n".join(context)
    if USE_OPENAI:
        prompt = f"Use the following context to answer concisely to the question.\n\nCONTEXT:\n{context_text}\n\nQUESTION: {q}\n\nAnswer:"
        ans = run_openai_completion(prompt, max_tokens=200)
    else:
        # naive fallback
        basic = "; ".join([f"{k}:{str(list(v.keys())[:3])}" for k,v in DB.get("pages", {}).items()])
        ans = f"Demo-mode answer. Pages summary: {basic}"
    return jsonify({"answer": ans})

# ----------------------------
# SEO analyzer
# ----------------------------
@app.route("/api/ai/seo_analyze", methods=["POST"])
def seo_analyze():
    data = request.get_json() or {}
    content = data.get("content", "")
    if not content:
        return jsonify({"error":"Provide 'content' in JSON body"}), 400
    if USE_OPENAI:
        prompt = f"Analyze this blog content for SEO. Provide 5 keyword suggestions, a short SEO score (0-100), and a one-line meta description. Content:\n\n{content}"
        out = run_openai_completion(prompt, max_tokens=200)
        return jsonify({"analysis": out})
    else:
        words = re.findall(r"\w+", content.lower())
        common = {}
        for w in words:
            if len(w)>4:
                common[w] = common.get(w,0)+1
        top = sorted(common.items(), key=lambda x:-x[1])[:5]
        keywords = [t[0] for t in top]
        score = min(85, 50 + len(top)*5)
        meta = (content[:120] + "...") if len(content)>120 else content
        return jsonify({"keywords": keywords, "score": score, "meta": meta})

# ----------------------------
# Theme customizer
# ----------------------------
@app.route("/api/ai/theme", methods=["POST"])
def theme_customize():
    data = request.get_json() or {}
    tone = data.get("tone", "professional")
    prompt = f"Suggest CSS variables for a {tone} website (JSON: primary, secondary, accent, bg, text, button) and 3 Tailwind class groups for hero, button, card."
    if USE_OPENAI:
        out = run_openai_completion(prompt, max_tokens=200)
        try:
            start = out.find("{")
            j = json.loads(out[start:]) if start != -1 else {"suggestion": out}
            DB.setdefault("themes", {})[tone] = j
            return jsonify({"theme": j})
        except Exception:
            return jsonify({"theme_suggestion": out})
    else:
        j = {"primary":"#0b72ff","secondary":"#0b9eff","accent":"#ffb400","bg":"#ffffff","text":"#111827","button":"#0b72ff"}
        DB.setdefault("themes", {})[tone] = j
        return jsonify({"theme": j})

# ----------------------------
# Resume parse + match
# ----------------------------
@app.route("/api/resume/parse", methods=["POST"])
def resume_parse():
    file = request.files.get("resume")
    desired = (request.form.get("desired_skills") or "").split(",") if request.form.get("desired_skills") else []
    if not file:
        return jsonify({"error":"Attach resume file (key name 'resume')"}), 400
    updir = DATA_DIR/"uploads"
    updir.mkdir(exist_ok=True)
    path = updir / file.filename
    file.save(path)
    text = ""
    try:
        text = path.read_text(errors="ignore")
    except:
        text = ""
    parsed = parse_resume_text_simple(text)
    score = score_resume(parsed, desired)
    return jsonify({"parsed": parsed, "score": score})

# ----------------------------
# AI Auto Website Builder
# ----------------------------
@app.route("/api/ai/auto_build", methods=["POST"])
def ai_auto_build():
    payload = request.get_json() or {}
    brief = payload.get("brief", "")
    if not brief:
        return jsonify({"error":"Provide 'brief' in JSON body"}), 400
    prompt = (
        f"Given this company description: {brief}\n\n"
        "Generate a JSON object with keys: name, tagline, about, services (list of 3), "
        "sample_projects (list of 2 with short desc). Return only valid JSON."
    )
    resp = run_openai_completion(prompt, max_tokens=350) if USE_OPENAI else run_openai_completion(prompt)
    try:
        jtext = resp
        start = jtext.find("{")
        if start != -1:
            jtext = jtext[start:]
        obj = json.loads(jtext)
    except Exception:
        # fallback generation
        obj = {
            "name": "Mastersolis Infotech",
            "tagline": "AI-driven digital presence",
            "about": brief or "We build AI solutions.",
            "services": ["Custom AI Solutions","Web Development","Data Analytics"],
            "sample_projects": [
                {"title":"Project A","desc":"AI automation for retail"},
                {"title":"Project B","desc":"Analytics dashboard deployment"}
            ]
        }
    DB.setdefault("pages", {})["home"] = {"title": obj.get("name"), "hero": obj.get("tagline")}
    DB["pages"]["about"] = {"about": obj.get("about"), "services": obj.get("services")}
    DB["pages"]["projects"] = {"projects": obj.get("sample_projects")}
    return jsonify({"generated": obj})

# ----------------------------
# Voice text (rewrite for narration)
# ----------------------------
@app.route("/api/voice/text", methods=["POST"])
def voice_text():
    data = request.get_json() or {}
    text = data.get("text","")
    if not text:
        return jsonify({"error":"Provide 'text' to convert to speech-friendly form"}), 400
    if USE_OPENAI:
        prompt = f"Rewrite the following text as a short friendly spoken introduction (40-70 words):\n\n{text}"
        out = run_openai_completion(prompt, max_tokens=120)
        return jsonify({"speech_text": out})
    else:
        s = re.sub(r"\s+", " ", text).strip()
        return jsonify({"speech_text": s})

# ----------------------------
# Admin seeding utility (idempotent)
# ----------------------------
def ensure_seed_data():
    """Create sample Mastersolis Infotech data if missing (idempotent)."""
    # Home / About
    DB.setdefault("pages", {})
    if not DB["pages"].get("home"):
        DB["pages"]["home"] = {
            "title": "Mastersolis Infotech",
            "hero": "We build AI-driven digital solutions for businesses",
            "tagline": "Automate. Analyze. Accelerate."
        }
    if not DB["pages"].get("about"):
        DB["pages"]["about"] = {
            "mission": "Empower organizations using intelligent automation and actionable insights.",
            "vision": "To be the trusted AI partner for small and medium enterprises.",
            "values": ["Innovation", "Integrity", "Customer-first"],
            "team": [
                {"name":"Asha Patel","role":"CEO","bio":"Product leader with 10+ years in AI"},
                {"name":"Rajan Kumar","role":"CTO","bio":"ML engineer and cloud architect"},
                {"name":"Nisha Rao","role":"Head of Design","bio":"Design thinker and UX lead"}
            ],
            "milestones": [
                {"year":2022,"event":"Founded"},
                {"year":2023,"event":"Launched first AI automation product"},
                {"year":2024,"event":"Served 100+ SME customers"}
            ]
        }
    # Services
    if not DB["pages"].get("services"):
        DB["pages"]["services"] = {
            "services": [
                {
                    "id": "svc_ai_chat",
                    "title": "AI Chatbots & Virtual Assistants",
                    "desc": "Build intelligent conversational assistants for customer support and sales.",
                    "features": [
                        "24/7 Customer Support Automation",
                        "Multi-language Support",
                        "Natural Language Processing",
                        "Integration with CRM Systems"
                    ],
                    "benefits": [
                        "Reduce Response Time by 45%",
                        "Handle Multiple Queries Simultaneously",
                        "Improve Customer Satisfaction",
                        "Lower Operational Costs"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?ai",
                    "price": "Starting from $499/month",
                    "category": "AI Solutions",
                    "testimonial": {
                        "text": "The chatbot reduced our support tickets by 60% in the first month!",
                        "author": "Sarah Chen",
                        "company": "TechStart Inc."
                    }
                },
                {
                    "id": "svc_auto_ops",
                    "title": "Business Process Automation",
                    "desc": "Transform your operations with intelligent automation and AI-driven workflows.",
                    "features": [
                        "Custom Workflow Automation",
                        "Document Processing & OCR",
                        "Email & Calendar Automation",
                        "Integration with Enterprise Systems"
                    ],
                    "benefits": [
                        "Save 20+ Hours Per Week",
                        "Eliminate Manual Data Entry",
                        "Reduce Error Rates by 99%",
                        "Scale Operations Efficiently"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?automation",
                    "price": "Starting from $999/month"
                },
                {
                    "id": "svc_data_analytics",
                    "title": "Business Intelligence & Analytics",
                    "desc": "Transform raw data into actionable insights with our advanced analytics solutions.",
                    "features": [
                        "Real-time Data Dashboards",
                        "Predictive Analytics",
                        "Custom Report Generation",
                        "Data Visualization"
                    ],
                    "benefits": [
                        "Make Data-Driven Decisions",
                        "Forecast Market Trends",
                        "Optimize Business Processes",
                        "Track KPIs in Real-time"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?data",
                    "price": "Starting from $799/month"
                },
                {
                    "id": "svc_ai_consulting",
                    "title": "AI Strategy Consulting",
                    "desc": "Expert guidance on implementing AI solutions in your business.",
                    "features": [
                        "AI Readiness Assessment",
                        "Technology Stack Planning",
                        "ROI Analysis",
                        "Implementation Roadmap"
                    ],
                    "benefits": [
                        "Clear AI Strategy",
                        "Competitive Advantage",
                        "Risk Mitigation",
                        "Expert Guidance"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?consulting",
                    "price": "Custom Quote",
                    "category": "Consulting",
                    "testimonial": {
                        "text": "Their strategic guidance helped us implement AI across our entire organization.",
                        "author": "Michael Rodriguez",
                        "company": "Global Retail Solutions"
                    }
                },
                {
                    "id": "svc_ai_website",
                    "title": "AI-Powered Website Builder",
                    "desc": "Create and maintain dynamic websites with AI-driven content and personalization.",
                    "features": [
                        "AI Content Generation",
                        "Dynamic Personalization",
                        "SEO Optimization",
                        "Analytics Dashboard",
                        "Mobile-First Design"
                    ],
                    "benefits": [
                        "Launch Website in Days",
                        "Always Fresh Content",
                        "Higher Conversion Rates",
                        "SEO-Optimized Pages",
                        "24/7 AI Updates"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?website",
                    "price": "Starting from $299/month",
                    "category": "Web Solutions",
                    "testimonial": {
                        "text": "Our website traffic increased by 200% after implementing their AI solutions!",
                        "author": "Emily Watson",
                        "company": "Digital First Media"
                    }
                },
                {
                    "id": "svc_ai_marketing",
                    "title": "AI Marketing Automation",
                    "desc": "Transform your marketing with AI-powered campaign optimization and personalization.",
                    "features": [
                        "Smart Campaign Management",
                        "Customer Journey Optimization",
                        "Predictive Analytics",
                        "Multi-channel Automation",
                        "A/B Testing with AI"
                    ],
                    "benefits": [
                        "2x Marketing ROI",
                        "Personalized Customer Experience",
                        "Data-Driven Decisions",
                        "Automated Campaign Optimization",
                        "Real-time Performance Tracking"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?marketing",
                    "price": "Starting from $899/month",
                    "category": "Marketing",
                    "testimonial": {
                        "text": "We saw a 150% increase in conversion rates within 3 months!",
                        "author": "Lisa Thompson",
                        "company": "Growth Marketing Pro"
                    }
                },
                {
                    "id": "svc_ml_models",
                    "title": "Custom ML Model Development",
                    "desc": "Develop and deploy custom machine learning models for your specific needs.",
                    "features": [
                        "Custom Model Development",
                        "Model Training & Optimization",
                        "MLOps Setup",
                        "Performance Monitoring"
                    ],
                    "benefits": [
                        "Tailored AI Solutions",
                        "High Accuracy Models",
                        "Scalable Architecture",
                        "Continuous Improvement"
                    ],
                    "image": "https://source.unsplash.com/random/800x600/?machine-learning",
                    "price": "Starting from $2,499/month",
                    "category": "AI Development",
                    "testimonial": {
                        "text": "Their custom ML models helped us achieve 99.9% accuracy in prediction!",
                        "author": "David Park",
                        "company": "FinTech Solutions"
                    }
                }
            ],
            "categories": [
                "AI Solutions",
                "Consulting",
                "Web Solutions",
                "Marketing",
                "AI Development"
            ],
            "summary": {
                "title": "Transform Your Business with AI",
                "description": "We offer end-to-end AI solutions to help businesses innovate and grow. From chatbots to custom ML models, our services are designed to deliver measurable results.",
                "stats": [
                    {"label": "Clients Served", "value": "100+"},
                    {"label": "Success Rate", "value": "95%"},
                    {"label": "ROI Average", "value": "3x"}
                ]
            }
        }
    # Projects
    if not DB["pages"].get("projects"):
        DB["pages"]["projects"] = {
            "projects": [
                {"id":"prj_1","title":"SupportBot","tags":["chatbot","automation"],"summary":"Reduced support load by 45% for a retail client."},
                {"id":"prj_2","title":"SalesInsights","tags":["analytics","dashboard"],"summary":"Actionable sales dashboards for 20 stores."},
                {"id":"prj_3","title":"ResumeAI","tags":["hr","nlp"],"summary":"Automated resume scoring and ATS formatting service."}
            ]
        }
    # Testimonials & case studies
    DB.setdefault("testimonials", [])
    if not DB["testimonials"]:
        DB["testimonials"] = [
            {"client":"GreenMart","quote":"Mastersolis built our chatbot - response rates improved dramatically.","author":"Priya S."},
            {"client":"TravelCo","quote":"Their analytics platform helped us optimize promotions.","author":"Arjun V."}
        ]
    # Blog posts
    DB.setdefault("blog", [])
    if not DB["blog"]:
        DB["blog"] = [
            {
                "id": "b1",
                "title": "How AI Improves Customer Support",
                "content": """
                In today's digital age, AI-powered customer support is revolutionizing how businesses interact with their customers. Here are key benefits we've observed:

                1. 24/7 Availability
                - Instant responses at any time
                - No wait times or queues
                - Global customer coverage

                2. Consistent Quality
                - Standardized responses
                - No human mood variations
                - Multi-language support

                3. Cost Efficiency
                - Reduced support staff needs
                - Handle multiple queries simultaneously
                - Lower operational costs

                4. Data-Driven Insights
                - Track common issues
                - Identify improvement areas
                - Measure customer satisfaction

                Our clients have seen:
                - 45% reduction in response time
                - 30% cost savings
                - 25% increase in customer satisfaction

                Ready to transform your customer support? Contact us to learn more.
                """,
                "summary": "AI reduces response time and improves CSAT scores dramatically through 24/7 availability and consistent service quality.",
                "date": "2024-11-01"
            },
            {
                "id": "b2",
                "title": "Top 5 Automation Ideas for SMEs",
                "content": """
                Small and Medium Enterprises can benefit greatly from automation. Here are our top 5 recommendations:

                1. Customer Service Automation
                - AI chatbots for common queries
                - Automated email responses
                - Appointment scheduling bots

                2. Invoice Processing
                - Automated data extraction
                - Digital approval workflows
                - Payment reconciliation

                3. Social Media Management
                - Scheduled posts
                - Automated engagement
                - Analytics reporting

                4. Inventory Management
                - Automated stock alerts
                - Purchase order generation
                - Supplier communication

                5. HR Process Automation
                - Resume screening
                - Interview scheduling
                - Onboarding workflows

                Each of these can save 5-10 hours per week for your team. Start small, measure results, and scale what works.
                """,
                "summary": "Practical automation ideas to save time and cost for small and medium businesses.",
                "date": "2024-11-05"
            },
            {
                "id": "b3",
                "title": "The Future of AI in Business",
                "content": """
                As we look towards 2025 and beyond, AI is set to transform business operations in unprecedented ways:

                Key Trends:
                1. Generative AI
                - Content creation
                - Code generation
                - Design automation

                2. Predictive Analytics
                - Sales forecasting
                - Inventory optimization
                - Risk assessment

                3. Process Automation
                - Workflow optimization
                - Document processing
                - Quality control

                4. Intelligent Decision Support
                - Data-driven insights
                - Scenario analysis
                - Real-time recommendations

                The businesses that adapt early will gain significant competitive advantages. Let us help you stay ahead.
                """,
                "summary": "Explore upcoming AI trends and their impact on business operations.",
                "date": "2024-11-08"
            }
        ]
    # Jobs & applications
    DB.setdefault("jobs", [])
    if not DB["jobs"]:
        DB["jobs"] = [
            {
                "id": "job-frontend",
                "title": "Senior Frontend Developer",
                "skills": "React, TypeScript, Tailwind CSS, Next.js",
                "description": """
                We're looking for a Senior Frontend Developer to join our growing team.

                Key Responsibilities:
                - Build responsive, performant user interfaces for our AI-powered applications
                - Collaborate with UX designers and backend engineers
                - Mentor junior developers and contribute to architecture decisions
                
                Requirements:
                - 3+ years of React experience
                - Strong TypeScript skills
                - Experience with modern CSS frameworks (Tailwind preferred)
                - Understanding of web performance optimization
                
                Benefits:
                - Competitive salary
                - Remote work options
                - Learning and development budget
                - Health insurance
                """,
                "location": "Remote / Hybrid",
                "type": "Full-time",
                "salary_range": "$90,000 - $130,000"
            },
            {
                "id": "job-ml",
                "title": "Machine Learning Engineer",
                "skills": "Python, TensorFlow, PyTorch, MLOps, AWS/Azure",
                "description": """
                Join our AI team to build and deploy cutting-edge ML models.

                Key Responsibilities:
                - Design and implement ML models for various use cases
                - Build and maintain ML pipelines
                - Optimize model performance and deployment
                - Collaborate with data scientists and engineers

                Requirements:
                - Masters/PhD in CS, ML, or related field
                - 2+ years ML engineering experience
                - Strong Python and deep learning framework expertise
                - Experience with MLOps and cloud platforms

                Benefits:
                - Competitive compensation
                - Remote work flexibility
                - Conference attendance budget
                - Premium healthcare
                """,
                "location": "Remote / Hybrid",
                "type": "Full-time",
                "salary_range": "$100,000 - $160,000"
            },
            {
                "id": "job-data",
                "title": "Data Engineer",
                "skills": "Python, SQL, Spark, Airflow, AWS",
                "description": """
                We're seeking a Data Engineer to build robust data pipelines.

                Key Responsibilities:
                - Design and implement data pipelines
                - Optimize data warehouse performance
                - Ensure data quality and reliability
                - Support ML team with data needs

                Requirements:
                - 3+ years data engineering experience
                - Expert in SQL and Python
                - Experience with big data tools
                - Strong problem-solving skills

                Benefits:
                - Competitive package
                - Flexible work hours
                - Learning allowance
                - Health benefits
                """,
                "location": "Remote",
                "type": "Full-time",
                "salary_range": "$85,000 - $140,000"
            }
        ]
    DB.setdefault("applications", [])
    if not DB["applications"]:
        DB["applications"] = [
            {"id":"app1","name":"Riya Sharma","email":"riya@example.com","job_title":"Frontend Developer","resume_path":None,"parsed":{"name":"Riya Sharma","skills":["react","flask","python"],"experience_years":3},"score":{"match_percent":82.0}},
            {"id":"app2","name":"Siddharth Rao","email":"sid@example.com","job_title":"Machine Learning Engineer","resume_path":None,"parsed":{"name":"Siddharth Rao","skills":["python","tensorflow","aws"],"experience_years":4},"score":{"match_percent":88.0}}
        ]
    # FAQ
    DB.setdefault("faq", [])
    if not DB["faq"]:
        DB["faq"] = [
            {"q":"What services do you offer?","a":"We offer AI chatbots, automation ops, and data analytics."},
            {"q":"How to contact?","a":"Use the Contact page or email contact@mastersolis.com"}
        ]
    # Analytics
    DB.setdefault("analytics", {})
    DB["analytics"] = {"visitors": 1240, "applications": len(DB.get("applications",[])), "popular_pages":["careers","home","projects"]}
    # Themes
    DB.setdefault("themes", {})
    if not DB["themes"]:
        DB["themes"] = {"default":{"primary":"#0b72ff","accent":"#ffb400","bg":"#ffffff","text":"#0f172a"}}
    # Sample portfolio
    DB.setdefault("portfolios", {})
    if not DB["portfolios"]:
        DB["portfolios"]["sample-portfolio-1"] = {
            "html":"<html><body><h1>Riya Sharma</h1><p>Frontend developer (React, Tailwind)</p></body></html>",
            "meta":{"name":"Riya Sharma","skills":["react","tailwind"],"experience_years":3}
        }
    # Mark seed time
    DB.setdefault("_meta", {})["seeded_at"] = datetime.datetime.utcnow().isoformat()

@app.route("/api/admin/ensure_seed", methods=["GET","POST"])
def api_ensure_seed():
    ensure_seed_data()
    return jsonify({"status":"seeded_or_exists","summary": {
        "pages": list(DB.get("pages",{}).keys()),
        "jobs": len(DB.get("jobs",[])),
        "applications": len(DB.get("applications",[])),
        "blog_posts": len(DB.get("blog",[]))
    }})

# Public blog endpoints
@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Return blog posts list
    return jsonify(DB.get('blog', []))


@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    posts = DB.get('blog', [])
    post = next((p for p in posts if str(p.get('id')) == str(post_id)), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)


# Simple auth/login for admin (demo)
ADMIN_WHITELIST = ["admin1@yourdomain.com", "admin2@yourdomain.com"]
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error":"email and password required"}), 400
    if email not in ADMIN_WHITELIST:
        return jsonify({"error":"not allowed"}), 403
    token = str(uuid.uuid4())
    DB.setdefault('admin_tokens', {})[token] = {"email": email, "created": datetime.datetime.utcnow().isoformat()}
    return jsonify({"token": token})

# Optional admin endpoint to list applications
@app.route("/api/admin/applications", methods=["GET"])
def list_applications():
    return jsonify(DB.get("applications", []))


# Contact form endpoint (public)
@app.route('/api/contact', methods=['POST'])
def contact_submit():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    if not message:
        return jsonify({"error": "Provide 'message' in JSON body"}), 400
    rec = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "message": message,
        "created": datetime.datetime.utcnow().isoformat()
    }
    DB.setdefault('messages', []).append(rec)
    # Optionally, store a lightweight FAQ/context entry for the chatbot
    DB.setdefault('faq', []).append({"q": f"Contact from {name or email}", "a": message})
    return jsonify({"status": "received", "message_id": rec["id"]}), 201


# Admin: list contact messages
@app.route('/api/admin/messages', methods=['GET'])
def admin_list_messages():
    return jsonify(DB.get('messages', []))

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    # Ensure data dir exists
    DATA_DIR.mkdir(exist_ok=True)
    print("Starting AI Website Builder backend. OpenAI enabled:", USE_OPENAI)
    app.run(debug=True, port=5001)
