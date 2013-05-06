from kotti.events import subscribe
from kotti.events import ObjectEvent


@subscribe()
def document_added(ObjectEvent):
    import pdb; pdb.set_trace()
