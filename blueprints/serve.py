from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from exts import db
from model import ServeModel
from .form import Serve_Form
from config import logger
from sqlalchemy import or_

bp = Blueprint("serve", __name__, url_prefix="/serve")


# Administrator Interface - Serve
@bp.route("/adm/serve")
def adm_serve():
    serves = ServeModel.query.all()
    return render_template("adm/adm-serve.html", serves=serves)


# add serve
@bp.route("/adm/serve/add", methods=['GET', 'POST'])
def serve_add():
    if request.method == 'GET':
        return render_template("adm/add_serve.html")
    else:
        form = Serve_Form(request.form)
        if form.validate():
            servename = form.servename.data
            classification = form.classification.data
            obj = form.obj.data
            price = form.price.data
            introduction = form.introduction.data

            serve = ServeModel(servename=servename, classification=classification, obj=obj, price=price,
                               introduction=introduction)
            db.session.add(serve)
            db.session.commit()
            logger.info(f'Add serve: {servename} successfully.')
            return redirect(url_for("serve.adm_serve"))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, add serve failed.')
            return redirect(url_for("serve.serve_add"))

# serve detail
@bp.route("/serve_detial/<int:serve_id>")
def serve_detail(serve_id):
    serve = ServeModel.query.get(serve_id)
    return render_template("adm/serve_detail.html", serve=serve)

# serve edit
@bp.route("/serve_edit/<int:serve_id>", methods=['GET', 'POST'])
def serve_edit(serve_id):
    serve = ServeModel.query.get(serve_id)
    if request.method == 'GET':
        return render_template("adm/serve_edit.html", serve=serve)
    else:
        form = Serve_Form(request.form)
        if form.validate():
            serve.servename = form.servename.data
            serve.classification = form.classification.data
            serve.obj = form.obj.data
            serve.price = form.price.data
            serve.introduction = form.introduction.data

            db.session.commit()
            logger.info(f'Edit serve: {serve.servename} successfully.')
            return redirect(url_for("serve.adm_serve"))
        else:
            flash("The message format is incorrect.")
            logger.warning(f'The message format is incorrect, edit serve failed.')
            return redirect(url_for("serve.serve_edit",serve_id=serve_id))

# serve delete
@bp.route("/serve_delete/<int:serve_id>")
def serve_delete(serve_id):
    ServeModel.query.filter_by(id=serve_id).delete()
    db.session.commit()
    return redirect(url_for("serve.adm_serve"))

# search
@bp.route("/search_adm")
def search_adm():
    query = request.args.get("query")
    serves = ServeModel.query.filter(or_(ServeModel.servename.contains(query),
                                              ServeModel.classification.contains(query),
                                              ServeModel.obj.contains(query),
                                              ServeModel.price.contains(query),))

    return render_template("adm/adm-serve.html", serves=serves)


