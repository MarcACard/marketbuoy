from flask import Blueprint, render_template, redirect, flash, url_for
from application.models import Collection, db, CollectionStats
from application.forms import CollectionForm
from application.opensea import get_collection
from sqlalchemy import exc

collections_bp = Blueprint("collections_bp", __name__, template_folder="templates")


@collections_bp.route("/")
def list_collections():
    collections = Collection.get_all()

    return render_template("collections.html.j2", collections=collections)


@collections_bp.route("/id/<slug>")
def collection_details(slug):
    """Display Page w/ Detailed Collection Data"""
    # TODO: Build Page
    # TODO: Add page Styling

    collection = Collection.query.filter_by(slug=slug).first_or_404()
    stats = CollectionStats.todays_floor(collection.id)

    return render_template(
        "collection_details.html.j2", collection=collection, stats=stats
    )


@collections_bp.route("/id/<name>/edit", methods=["GET", "POST"])
def edit_collection(name):
    """Edit or Refresh Collection Meta Data
    >>ADMIN ONLY<<
    """
    # TODO: Add Form
    # TODO: Limit to Admin User Only
    # TODO: Build Page
    # TODO: Style Page

    return f"Edit Collection: {name}"


@collections_bp.route("/add", methods=["GET", "POST"])
def add_collection():
    """Add a New Collection
    >>ADMIN ONLY<<
    """
    # TODO: Limit Functionality to ADMIN Users only
    # TODO: Clean up and Add Abstractions where necessary
    # TODO: Build Page
    # TODO: Style Page

    form = CollectionForm()

    if form.validate_on_submit():
        data = get_collection(form.slug.data)

        collection = Collection(
            banner_image_url=data["banner_image_url"],
            created_date=data["created_date"],
            description=data["description"],
            name=data["name"],
            slug=data["slug"],
            telegram_url=data["telegram_url"],
            twitter_username=data["twitter_username"],
            instagram_username=data["instagram_username"],
            wiki_url=data["wiki_url"],
            discord_url=data["discord_url"],
            image_url=data["image_url"],
        )

        try:
            db.session.add(collection)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash("Collection Already Exists ", "error")
            return redirect(url_for("collections_bp.add_collection"))

        flash("Collection Successfully Added", "info")
        return redirect(url_for("collections_bp.list_collections"))

    return render_template("add_collection.html.j2", form=form)
