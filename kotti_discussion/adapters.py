from zope.interface import implements
from kotti_discussion.interfaces import ICommentable, IComment
from kotti.interfaces import IDocument
from kotti_discussion.utils import get_discussion
from zope.component import adapts


class CommentableDocument(object):
    """ Adds comments to document"""
    implements(ICommentable)
    adapts(IDocument)

    def __init__(self, context):
        self.context = context

    def get_comments(self):
        discussion = get_discussion(self.context)
        return filter(lambda x: IComment.providedBy(x), discussion.values())
