from zope.interface import implements
from kotti_discussion.interfaces import IDiscussion, ICommentable, IComment
from kotti.interfaces import IDocument


class CommentableDocument(object):
    """ Adds comments to document"""
    implements(ICommentable)
    __used__for = IDocument

    def __init__(self, context):
        self.context = context

    def get_comments(self):
        context = self.context
        return [obj for obj in context.values() if IComment.providedBy(obj)]

class CommentableDiscussion(object):
    """ Adds comments to discussion """
    implements(ICommentable)
    __used__for = IDiscussion

    def __init__(self, context):
        self.context = context

    def get_comments(self):
        context = self.context
        return [i for i in context if IComment.providedBy(context[i])]
