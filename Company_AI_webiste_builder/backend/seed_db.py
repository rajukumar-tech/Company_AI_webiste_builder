# seed_db.py
from db import engine, SessionLocal
from models import Base, Page, Job, Application, Portfolio, BlogPost, Testimonial, Analytics

def create_tables():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

def seed_data():
    db = SessionLocal()
    try:
        # Seed Pages
        if not db.query(Page).filter_by(name="home").first():
            print("Seeding company pages...")
            db.add(Page(
                name="home",
                content={
                    "title": "Mastersolis Infotech",
                    "hero": "AI-powered digital transformation",
                    "tagline": "Automate. Analyze. Accelerate."
                }
            ))
            db.add(Page(
                name="about",
                content={
                    "mission": "Empower organizations using intelligent automation and insights.",
                    "vision": "To be the trusted AI partner for global enterprises.",
                    "values": ["Innovation", "Integrity", "Customer-first"],
                    "team": [
                        {"name": "Asha Patel", "role": "CEO"},
                        {"name": "Rajan Kumar", "role": "CTO"},
                        {"name": "Nisha Rao", "role": "Design Lead"}
                    ]
                }
            ))

        # Seed Services Page
        if not db.query(Page).filter_by(name="services").first():
            db.add(Page(
                name="services",
                content={
                    "services": [
                        {"title": "AI Chatbots", "desc": "Smart assistants for customer engagement"},
                        {"title": "Automation Ops", "desc": "Optimize workflows with automation"},
                        {"title": "Data Analytics", "desc": "Turn data into actionable insights"}
                    ]
                }
            ))

        # Seed Projects
        if not db.query(Page).filter_by(name="projects").first():
            db.add(Page(
                name="projects",
                content={
                    "projects": [
                        {"title": "SupportBot", "summary": "Reduced support workload by 40%"},
                        {"title": "ResumeAI", "summary": "AI resume screening system"},
                        {"title": "DataDash", "summary": "Business intelligence dashboards"}
                    ]
                }
            ))

        # Seed Jobs
        if db.query(Job).count() == 0:
            print("Seeding job listings...")
            db.add(Job(title="Frontend Developer", skills="React, CSS, HTML", description="Build web interfaces"))
            db.add(Job(title="Backend Engineer", skills="Python, Flask, PostgreSQL", description="Develop APIs and services"))

        # Seed Blog Posts
        if db.query(BlogPost).count() == 0:
            print("Seeding blog posts...")
            db.add(BlogPost(title="Harnessing AI for SMEs", content="AI drives business growth...", summary="AI adoption in small enterprises."))
            db.add(BlogPost(title="5 Automation Wins", content="How automation boosts productivity...", summary="Business automation success stories."))

        # Seed Testimonials
        if db.query(Testimonial).count() == 0:
            print("Seeding testimonials...")
            db.add(Testimonial(client="GreenMart", quote="Mastersolis helped us scale effortlessly!", author="Priya S."))
            db.add(Testimonial(client="TechHive", quote="Top-notch AI integration.", author="Aarav N."))

        # Seed Analytics
        if db.query(Analytics).count() == 0:
            db.add(Analytics(key="site_metrics", value={
                "visitors": 1420,
                "applications": 5,
                "popular_pages": ["home", "careers", "projects"]
            }))

        db.commit()
        print("✅ Seeding completed successfully.")
    except Exception as e:
        db.rollback()
        print("❌ Error during seeding:", e)
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_data()
