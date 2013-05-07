import colander

from kotti.views.edit import AddFormView
from kotti.views.edit import ContentSchema
from kotti.views.edit import EditFormView
from kotti.views.util import template_api
from kotti.resources import Document

from kotti.interfaces import IDocument

from kotti_discussion import _
from kotti_discussion.utils import get_avatar_image
from kotti_discussion.interfaces import ICommentable
from kotti_discussion.resources import Comment
from kotti_discussion.adapters import CommentableDocument

from kotti_discussion.utils import (
    create_comment_inside,
    get_discussion
)

from deform import Button
from deform import Form
from deform.widget import TextAreaWidget
from pyramid.view import view_config
from zope.interface import alsoProvides, noLongerProvides


#class DiscussionSchema(ContentSchema):
    #body = colander.SchemaNode(colander.String())


#class DiscussionAddForm(AddFormView):
    #schema_factory = DiscussionSchema
    #add = Discussion
    #item_type = _(u"Discussion")


#class DiscussionEditForm(EditFormView):
    #schema_factory = DiscussionSchema


class CommentSchema(ContentSchema):
    message = colander.SchemaNode(colander.String(),
                                  widget=TextAreaWidget(cols=400, rows=5),
                                  title=u"",
                                  name=u"")


class CommentAddForm(AddFormView):
    schema_factory = CommentSchema
    add = Comment
    item_type = _(u"Comment")


class CommentEditForm(EditFormView):
    schema_factory = CommentSchema

from kotti.views.edit import DocumentSchema
class ExtendedDocumentSchema(DocumentSchema):
    enable_comments = colander.SchemaNode(
        colander.Boolean(),
        title=_(u'Enable comments'),
        description=_(u'Check to enable comments')
    )

class ExtendedDocumentAddForm(AddFormView):
    schema_factory = ExtendedDocumentSchema
    item_type = _(u'Document')
    item_class = Document


    def add(self, **appstruct):
        doc = self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
        )

        if appstruct['enable_comments']:
            alsoProvides(doc, ICommentable)
        else:
            noLongerProvides(doc, ICommentable)
        return Document

class ExtendedDocumentEditForm(EditFormView):
    schema_factory = ExtendedDocumentSchema

    def edit(self, **appstruct):
        # TODO: Continue
        import pdb; pdb.set_trace()

class MessageSchema(colander.MappingSchema):
    message = colander.SchemaNode(colander.String(),
                                  widget=TextAreaWidget(cols=400, rows=5,
                                    style="width:40em;",
                                    css_class="comment_message",
                                  ))

@view_config(name='view_discussion',
             renderer='templates/view_discussion.pt')
def view_discussion(context, request):
    """ View for comments """
    try:
        adapter = ICommentable(context)
    except TypeError:
        return dict(comments=None)

    schema = MessageSchema()
    form = Form(schema, bootstrap_form_style='form-vertical',
                buttons=[Button('submit', _('Send message'))])
    rendered_form = None

    if 'submit' in request.POST:
        message = request.POST['message']

        # Put the comment inside discussion if there is one. Create discussion
        # if there isn't one
        discussion = get_discussion(context)
        comment = create_comment_inside(discussion)
        comment.message = message

    # before render change the textarea id
    form['message'].oid = 'kotti_discussion-textarea'
    rendered_form = form.render()

    from kotti_discussion.fanstatic import kotti_discussion_group
    kotti_discussion_group.need()

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


#def view_discussion(context, request):
    #return dict()


def includeme_edit(config):

    #config.add_view(
        #DiscussionEditForm,
        #context=Discussion,
        #name='edit',
        #permission='edit',
        #renderer='kotti:templates/edit/node.pt',
    #)

    #config.add_view(
        #DiscussionAddForm,
        #name='add_discussion',
        #permission='add',
        #renderer='kotti:templates/edit/node.pt',
    #)

    config.add_view(
        ExtendedDocumentAddForm,
        context=Document,
        name=Document.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        ExtendedDocumentEditForm,
        context=Document,
        name='edit',
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
    #config.add_view(
        #view_discussion,
        #context=Discussion,
        #name='view',
        #permission='view',
        #renderer='templates/view_discussion.pt',
    #)

    config.add_static_view('static-kotti_discussion', 'kotti_discussion:static')


def includeme(config):
    includeme_edit(config)
    includeme_view(config)

    config.registry.registerAdapter(CommentableDocument, (IDocument,), ICommentable)

    from kotti.views.slots import assign_slot
    config.scan(__name__)
    assign_slot('view_discussion', 'belowcontent')
