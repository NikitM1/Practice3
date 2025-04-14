import gettext
import locale
import os

translation=gettext.translation('WCount', 'po', fallback=True)
_, ngettext=translation.gettext, translation.ngettext

DOMAIN = 'ru'

DOMAINS={
    'ru': gettext.translation('WCount','po',fallback=True),
    'en': gettext.NullTranslations()
}

def ngettext(text, textn, n):
    return DOMAINS[DOMAIN].ngettext(text, textn, n)

def _(text):
    return DOMAINS[DOMAIN].gettext(text)

while s:=input(): 
    N=len(s.split())
    print(ngettext('Entered {} word', 'Entered {} words', N).format(N))
    DOMAIN='en'
    print(ngettext('Entered {} word', 'Entered {} words', N).format(N))
    DOMAIN='ru'
