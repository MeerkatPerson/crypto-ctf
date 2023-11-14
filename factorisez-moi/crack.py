
from Crypto.Util.number import inverse, long_to_bytes

p = 97839022367196967320263264978368947205122877823489185971421826199841057736838174021973624623032291705073927781957876028310481718687592838501105164290567645378359776183462494381975878816796658439072700073359346016136655340080970975032916717515003734765954648986067320702233415062260602669429146815491410736039

q = 97839022367196967320263264978368947205122877823489185971421826199841057736838174021973624623032291705073927781957876028310481718687592838501105164290567199505823743211937514260937024096515690943335609199152751311092115513984966503864729040580218835221155682919020950388205825185439123753759657637290881646729

e = 65537

c = 5367795265591511771315047137805304893674332016938273364815774357902792892577213033893265847821355902549004296516398835517812697393562729715290581058687493092437472044769371925264060087696991604045358733699721108334563953948540207018895168677680035066128030407624497555600852240589391947386709662065141847887239387415557013330011714893259348026646750957912908814815911006849634983530744853437121873434000034491021417369775811118594802622313377196877188334487663653504719612526680519631101986435474465777947903102918670442680324613004996124205028379930974787962135228434512184132877982872849400534612719952120796811981


d = inverse(e, (p-1)*(q-1))

print(long_to_bytes(pow(c, d, p*q)).decode())
