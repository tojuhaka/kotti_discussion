import colander
import datetime

from kotti.views.edit import AddFormView
from kotti.views.edit import ContentSchema
from kotti.views.edit import EditFormView
from kotti.views.util import template_api

from kotti_discussion import _
from kotti_discussion.resources import Discussion, Comment

from deform import Button
from deform import Form
from deform.widget import TextAreaWidget


class DiscussionSchema(ContentSchema):
    example_text = colander.SchemaNode(colander.String())


class DiscussionAddForm(AddFormView):
    schema_factory = DiscussionSchema
    add = Discussion
    item_type = _(u"Discussion")


class DiscussionEditForm(EditFormView):
    schema_factory = DiscussionSchema


class CommentSchema(ContentSchema):
    message = colander.SchemaNode(colander.String(),
                                       widget=TextAreaWidget(cols=40, rows=5))

class CommentAddForm(AddFormView):
    schema_factory = CommentSchema
    add = Comment
    item_type = _(u"Comment")


class CommentEditForm(EditFormView):
    schema_factory = CommentSchema


def view_discussion(context, request):
    class MessageSchema(colander.MappingSchema):

        message = colander.SchemaNode(colander.String(),
            widget=TextAreaWidget(cols=200, rows=5), title=_("Message"))

    schema = MessageSchema()
    form = Form(schema, buttons=[Button('submit', _('Send message'))])
    rendered_form = None

    if 'submit' in request.POST:
        message = request.POST['message']

        # Create comment inside discussion
        comment = Comment(
            title=u'comment',
            description=u'comment for discussion',
            tags=[],
            creation_date=datetime.datetime.now(),
            creator=u'testi',
            message=message
        )
        from kotti.util import title_to_name
        _id = title_to_name(comment.title, blacklist=context.keys())
        context[_id] = comment

    rendered_form = form.render()

    return {
        'form': rendered_form,
        'api': template_api(context, request),  # this bounds context and request variables to the api in the template
        'example_text': context.example_text,  # this can be called directly in the template as example_text
    }


def includeme_edit(config):

    config.add_view(
        DiscussionEditForm,
        context=Discussion,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        DiscussionAddForm,
        name='add_discussion',
        permission='add',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        CommentEditForm,
        context=Comment,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        CommentAddForm,
        name='add_comment',
        permission='add',
        renderer='kotti:templates/edit/node.pt',
    )


def includeme_view(config):

    config.add_view(
        view_discussion,
        context=Discussion,
        name='view',
        permission='view',
        renderer='templates/view.pt',
    )

    config.add_static_view('static-kotti_discussion', 'kotti_discussion:static')


def includeme(config):
    includeme_edit(config)
    includeme_view(config)
