import gettext

# _podir=os.path.join(os.path.dirname(__file__), 'po')
translation=gettext.translation('WCount', 'po', fallback=True)
_, ngettext=translation.gettext, translation.ngettext

while s:=input(): print(_(f'Entered {len(s.split())} word(s)'))

