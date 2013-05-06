import urllib
import hashlib
from kotti_discussion.resources import Discussion, Comment
from kotti_discussion.interfaces import IDiscussion
from kotti.util import title_to_name
import datetime


def get_avatar_image(email):
    # mystery-man
    default = "mm"
    size = 40

    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d': default, 's': str(size)})

    return gravatar_url


def get_discussion(obj):
        discussions = filter(lambda x: IDiscussion.providedBy(x),
                             obj.values())
        try:
            discussion = discussions.pop()
        except IndexError:
            discussion = _create_discussion_inside(obj)
        return discussion


def _create_discussion_inside(obj):
        discussion = Discussion(
            title=u'discussion',
            description=u'discussion for comments',
            tags=[],
            creation_date=datetime.datetime.now()
        )
        _id = title_to_name(discussion.title, blacklist=obj.keys())
        obj[_id] = discussion

        return obj[_id]


def create_comment_inside(obj):
        comment = Comment(
            title=u'comment',
            description=u'comment for discussion',
            tags=[],
            creation_date=datetime.datetime.now(),
            # TODO: Current user
            creator=u'TODOCURRENTUSER',
            message=u''
        )
        _id = title_to_name(comment.title, blacklist=obj.keys())
        obj[_id] = comment

        return obj[_id]
