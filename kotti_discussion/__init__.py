from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_discussion')


def kotti_configure(settings):
    settings['kotti.includes'] += ' kotti_discussion.views'
    settings['kotti.available_types'] += ' kotti_discussion.resources.Comment'
    settings['kotti.fanstatic.view_needed'] += ' kotti_discussion.fanstatic.kotti_discussion_group'
