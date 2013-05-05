from kotti.resources import Content
from zope.interface import implements
from kotti_discussion.interfaces import IDiscussion, IComment, ICommentable

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode

from kotti_discussion import _
from kotti.interfaces import IDefaultWorkflow


class Discussion(Content):
    """This is your content type."""
    implements(IDiscussion, IDefaultWorkflow, ICommentable)

    # add your columns
    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    example_text = Column('example_text', Unicode(256))

    # change the type info to your needs
    type_info = Content.type_info.copy(
        name=u'Discussion',
        title=_(u'Discussion'),
        add_view=u'add_discussion',
        addable_to=[u''],
        )

    # adjust the __init__ method according to your columns
    def __init__(self, example_text=u'', **kwargs):
        super(Discussion, self).__init__(**kwargs)
        self.example_text = example_text

    @property
    def comments(self):
        return [self[i] for i in self]

class Comment(Content):
    """This is your content type."""
    implements(IComment)

    # add your columns
    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    message = Column('message', Unicode(256))
    creator = Column('creator', Unicode(256))


    # change the type info to your needs
    type_info = Content.type_info.copy(
        name=u'Comment',
        title=_(u'Comment'),
        add_view=u'add_comment',
        addable_to=[u'Discussion'],
        )

    # adjust the __init__ method according to your columns
    def __init__(self, message=u'',creator=u'', **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.message = message
