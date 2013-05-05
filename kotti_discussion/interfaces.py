from zope.interface import Interface

class IDiscussion(Interface):
    """ Marker interface for discussion """

class IComment(Interface):
    """ Marker interface for comment inside Discussion """

class ICommentable(Interface):
    """ Adds comments to comment """



