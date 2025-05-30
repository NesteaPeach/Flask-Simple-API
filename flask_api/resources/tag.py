from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_api.db import db
from flask_api.models import TagModel, StoreModel, ItemModel
from flask_api.schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Items", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # this is what u can use if the unique name is set to false
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
        #     abort(400, message="A tag with that name already exists in that store.")
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        # add validation for if store id is matching between them
        if item.store_id == tag.store_id:
            item.tags.remove(tag)
            try:
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError as e:
                abort(500, message=str(e))
            return {"message": "Item removed from tag", "item": item, "tag": tag}
        abort(400, message="The store Id provided is not matching between the item and the tag. "
                           "Make sure the selected tag and item are from the same store.")


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="Deletes a tag if no item is tagged with it.",
                  example={"message": "Tag deleted"})
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400,
                      description="Returned if the tag is assigned to one or more items. "
                                  "In this case the tag is not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            try:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted"}
            except SQLAlchemyError as e:
                abort(500, message=str(e))
        abort(400, message="Could not delete tag. "
                           "Make sure tag is not associated with any items, then try again.")
