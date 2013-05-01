from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

library = Library("kotti_discussion", "static")
kotti_discussion_css = Resource(library, "style.css")
kotti_discussion_group = Group([kotti_discussion_css])
