import os
from flask import Flask, request, jsonify, send_from_directory
from models import db, Banner, VisionMission, Statistic, Initiative
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "instance", "patilngo.sqlite")
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="/")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/admin")
    def admin_index():
        return app.send_static_file("admin/login.html")

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # BANNERS
    @app.route("/api/banners", methods=["GET"])
    def list_banners():
        banners = Banner.query.order_by(Banner.display_order).all()
        return jsonify([b.to_dict() for b in banners])

    @app.route("/api/banners", methods=["POST"])
    def add_banner():
        if "image" not in request.files:
            return jsonify({"error": "image file is required"}), 400
        image = request.files["image"]
        if image.filename == "" or not allowed_file(image.filename):
            return jsonify({"error": "invalid image"}), 400
        filename = secure_filename(image.filename)
        filename = f"{int(__import__('time').time())}_{filename}"
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(path)
        rel_path = f"/uploads/{filename}"

        title = request.form.get("title", "")
        description = request.form.get("description", "")
        display_order = int(request.form.get("display_order", 0))

        b = Banner(image_url=rel_path, title=title, description=description, display_order=display_order, status=True)
        db.session.add(b)
        db.session.commit()
        return jsonify(b.to_dict()), 201

    @app.route("/api/banners/<int:bid>", methods=["PUT"])
    def update_banner(bid):
        b = Banner.query.get_or_404(bid)
        data = request.form or request.json or {}
        if "title" in data:
            b.title = data.get("title")
        if "description" in data:
            b.description = data.get("description")
        if "display_order" in data:
            try:
                b.display_order = int(data.get("display_order"))
            except:
                pass
        if "status" in data:
            b.status = data.get("status") in ("1", "true", "True", True)
        if "image" in request.files:
            image = request.files["image"]
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filename = f"{int(__import__('time').time())}_{filename}"
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(path)
                b.image_url = f"/uploads/{filename}"
        db.session.commit()
        return jsonify(b.to_dict())

    @app.route("/api/banners/<int:bid>", methods=["DELETE"])
    def delete_banner(bid):
        b = Banner.query.get_or_404(bid)
        db.session.delete(b)
        db.session.commit()
        return jsonify({"message": "deleted"})

    # VISION & MISSION
    @app.route("/api/vision-mission", methods=["GET"])
    def get_vm():
        vm = VisionMission.query.first()
        if not vm:
            return jsonify([])
        return jsonify([vm.to_dict()])

    @app.route("/api/vision-mission", methods=["POST", "PUT"])
    def upsert_vm():
        data = request.get_json() or {}
        vm = VisionMission.query.first()
        if not vm:
            vm = VisionMission()
            db.session.add(vm)
        vm.vision_title = data.get("vision_title", vm.vision_title)
        vm.vision_description = data.get("vision_description", vm.vision_description)
        vm.mission_title = data.get("mission_title", vm.mission_title)
        vm.mission_description = data.get("mission_description", vm.mission_description)
        db.session.commit()
        return jsonify(vm.to_dict())

    # STATISTICS
    @app.route("/api/statistics", methods=["GET"])
    def list_stats():
        stats = Statistic.query.order_by(Statistic.display_order).all()
        return jsonify([s.to_dict() for s in stats])

    @app.route("/api/statistics", methods=["POST"])
    def add_stat():
        data = request.get_json() or {}
        s = Statistic(
            label=data.get("label"),
            value=data.get("value"),
            display_order=data.get("display_order", 0),
            status=data.get("status", "active")
        )
        db.session.add(s)
        db.session.commit()
        return jsonify(s.to_dict()), 201

    @app.route("/api/statistics/<int:sid>", methods=["PUT", "DELETE"])
    def modify_stat(sid):
        s = Statistic.query.get_or_404(sid)
        if request.method == "PUT":
            data = request.get_json() or {}
            s.label = data.get("label", s.label)
            s.value = data.get("value", s.value)
            s.display_order = data.get("display_order", s.display_order)
            s.status = data.get("status", s.status)
            db.session.commit()
            return jsonify(s.to_dict())
        else:
            db.session.delete(s)
            db.session.commit()
            return jsonify({"message": "deleted"})

    # INITIATIVES
    @app.route("/api/initiatives", methods=["GET"])
    def list_inits():
        items = Initiative.query.order_by(Initiative.display_order).all()
        return jsonify([i.to_dict() for i in items])

    @app.route("/api/initiatives", methods=["POST"])
    def add_init():
        image_url = None
        if "image" in request.files:
            image = request.files["image"]
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filename = f"{int(__import__('time').time())}_{filename}"
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(path)
                image_url = f"/uploads/{filename}"

        title = request.form.get("title")
        description = request.form.get("description", "")
        display_order = int(request.form.get("display_order", 0))
        init = Initiative(title=title, description=description, image_url=image_url, display_order=display_order, status="active")
        db.session.add(init)
        db.session.commit()
        return jsonify(init.to_dict()), 201

    @app.route("/api/initiatives/<int:iid>", methods=["PUT", "DELETE"])
    def modify_init(iid):
        it = Initiative.query.get_or_404(iid)
        if request.method == "PUT":
            data = request.form or request.json or {}
            if "title" in data:
                it.title = data.get("title")
            if "description" in data:
                it.description = data.get("description")
            if "display_order" in data:
                try:
                    it.display_order = int(data.get("display_order"))
                except:
                    pass
            if "image" in request.files:
                image = request.files["image"]
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    filename = f"{int(__import__('time').time())}_{filename}"
                    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    image.save(path)
                    it.image_url = f"/uploads/{filename}"
            db.session.commit()
            return jsonify(it.to_dict())
        else:
            db.session.delete(it)
            db.session.commit()
            return jsonify({"message": "deleted"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
