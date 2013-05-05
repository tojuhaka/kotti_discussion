from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_discussion')


from kotti_discussion.interfaces import IDiscussion, ICommentable
from zope.interface import implements

class CommentableDiscussion(object):
    implements(ICommentable)
    __used__for = IDiscussion

    def __init__(self, context):
        self.context = context

    def get_comments(self):
        import pdb; pdb.set_trace()
        return self.context.comments


def kotti_configure(settings):
    settings['kotti.includes'] += ' kotti_discussion.views'
    settings['kotti.available_types'] += ' kotti_discussion.resources.Discussion'
    settings['kotti.available_types'] += ' kotti_discussion.resources.Comment'
    settings['kotti.fanstatic.view_needed'] += ' kotti_discussion.fanstatic.kotti_discussion_group'
