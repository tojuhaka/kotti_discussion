import colander
import datetime

from kotti.views.edit import AddFormView
from kotti.views.edit import ContentSchema
from kotti.views.edit import EditFormView
from kotti.views.util import template_api

from kotti.interfaces import IDocument

from kotti_discussion import _
from kotti_discussion.utils import get_avatar_image
from kotti_discussion.interfaces import ICommentable, IDiscussion
from kotti_discussion.resources import Discussion, Comment
from kotti_discussion.adapters import CommentableDiscussion, CommentableDocument

from deform import Button
from deform import Form
from deform.widget import TextAreaWidget
from pyramid.view import view_config


class DiscussionSchema(ContentSchema):
    body = colander.SchemaNode(colander.String())


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


class MessageSchema(colander.MappingSchema):
    message = colander.SchemaNode(colander.String(),
                                  widget=TextAreaWidget(cols=200, rows=5),
                                  title=_("Message"))


@view_config(name='view_comments',
                     renderer='templates/view_comments.pt')
def view_comments(context, request):
    """ View for comments """
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

    adapter = request.registry.queryAdapter(context, ICommentable)
    comments = []
    try:
        comments = adapter.get_comments()
    except AttributeError:
        pass

    return {
        'comments': comments,
        'form': rendered_form,
        'api': template_api(context, request),  # this bounds context and request variables to the api in the template
        'body': context.body,  # this can be called directly in the template as example_text
        'gravatar_url': get_avatar_image('tojuhaka@gmail.com')
    }


def view_discussion(context, request):
    return dict()


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

    # TODO: USE MULTI ADAPTER
    config.registry.registerAdapter(CommentableDocument, (IDocument,), ICommentable)
    config.registry.registerAdapter(CommentableDiscussion, (IDiscussion,), ICommentable)

    from kotti.views.slots import assign_slot
    config.scan(__name__)
    assign_slot('view_comments', 'belowcontent')
