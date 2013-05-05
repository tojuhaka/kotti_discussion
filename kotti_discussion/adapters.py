from zope.interface import implements
from kotti_discussion.interfaces import IDiscussion, ICommentable


class CommentableDiscussion(object):
    """ Adds comments to discussion """
    implements(ICommentable)
    __used__for = IDiscussion

    def __init__(self, context):
        self.context = context

    def get_comments(self):
        comments = []
        try:
            comments = self.context.comments
        except AttributeError:
            self.context.comments = []
        return comments
