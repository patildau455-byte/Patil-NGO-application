from app import create_app
from models import db, Banner, VisionMission, Statistic, Initiative

app = create_app()
with app.app_context():
    db.create_all()

    if not VisionMission.query.first():
        vm = VisionMission(
            vision_title="Our Vision",
            vision_description="Empower communities through education and support",
            mission_title="Our Mission",
            mission_description="Provide access to education, healthcare and sustainable projects"
        )
        db.session.add(vm)

    if not Statistic.query.first():
        db.session.add_all([
            Statistic(label="Children Educated", value="10000+", display_order=1),
            Statistic(label="Families Helped", value="5000+", display_order=2),
            Statistic(label="Projects Completed", value="25+", display_order=3)
        ])

    if not Initiative.query.first():
        db.session.add_all([
            Initiative(title="Education for All", description="Tuition & materials for underprivileged children", image_url=None, display_order=1),
            Initiative(title="Health Camps", description="Free medical camps in rural areas", image_url=None, display_order=2)
        ])

    db.session.commit()
    print("Seeded DB")
