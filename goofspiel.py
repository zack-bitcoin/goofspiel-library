import hashlib
import random
import pprint
from json import dumps as package, loads as unpackage
def hash_(x): return hashlib.sha256(package(x, sort_keys=True)).hexdigest()
def guess(n):
    pair=[n, random.random()]
    h=hash_(pair)
    out=[pair, h]
    print('guess, salt, and hash: ' +str(out))
    print('only share the hash for now')
    return out
def confirm(l):
    if type(l) != list: return False
    h=l[1]
    pair=l[0]
    return h==hash_(pair)
def ask_card_share_hash(txt): return guess(int(raw_input(txt)))[0][0]
def partner_draws_card_from_hand(DB, txt): return partner_draws_card(DB, txt, True)
def partner_draws_card(DB, txt, from_hand=False):
    c=False
    deck=DB['your_hand']
    other_hash=raw_input('partner\'s hash: ')
    while not c:
        print('(type "back" with quote marks \'"\' to re-enter your partner\'s hash)')
        trio=input(txt)
        if trio=='back':
            return partner_draws_card(DB, txt, from_hand)
        c=confirm(trio) and ((trio[0][0] in deck) or (not from_hand)) and other_hash==trio[1]
    return trio[0][0]
def draw_card_from_deck(DB):#distributed random number generation
    my_random=ask_card_share_hash('draw card from deck on the table (choose a random number): ')
    your_random=partner_draws_card(DB, 'partner\'s guess, salt, and hash for confirmation: ')
    card=(my_random+your_random)%len(DB['deck'])+1
    print('drew a '+str(card)+' from the deck')
    DB['deck'].remove(card)
    return card
def draw_card_from_hand(DB):
    my_card=0
    while my_card not in DB['my_hand']:
        my_card=ask_card_share_hash('what card will you play?')
        if my_card not in DB['my_hand']:
            print('you already spent that card')
    return my_card
def game(size=13):
    f=lambda: range(1, size)
    DB={'deck':f(), 'my_hand':f(), 'your_hand':f(), 
        'my_points':0, 'your_points':0}
    while len(DB['deck'])>0:
        card=draw_card_from_deck(DB)
        my_card=draw_card_from_hand(DB)
        your_card=partner_draws_card_from_hand(DB, 'partner\'s list of 3 number for confirmation')
        if my_card>your_card: DB['my_points']+=card
        if my_card<your_card: DB['your_points']+=card
        DB['my_hand'].remove(my_card)
        DB['your_hand'].remove(your_card)
        pprint.pprint(DB)
    m=DB['my_points']
    y=DB['your_points']
    if m>y: print('you won!')
    if m==y: print('a draw')
    if m<y: print('you lost')
game()
