from anratmenu.utils import menu


def get_anrat_context(request):
    return {'mainmenu': menu}
