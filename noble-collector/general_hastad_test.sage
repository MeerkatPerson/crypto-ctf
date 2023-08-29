from Crypto.Util.number import bytes_to_long, long_to_bytes

names = ['ROD EARNEST ANDREW MCINTYRE',
         'MARION SHELBY BRICE MONTOYA',
         'HAZEL YVONNE ABIGAIL PRINCE']

base = ' ' * len(names[0])

n = [26731676081242473261672073372787551729307870220772542234767643029756287555198429726019800957188135784488730420157016444644369935481191477694193313664984329503896857229865347255729672565019771619654034607885834085227987304787265329882675932596823681124400256217494034908908522256962226872061076664009152321805868144779485360425499300890801155126386663617951800099925633913450834549921820941491019256503598352594086665835074701099949505891322020125863805994397239129719850149694756616703131133654014378455520051664558965718744158807569257289495527291927649810872001354118060010123626483754484194674658994792163628487321, 27343155606276861808519345171598518808104065722330660877615507069973928115749699727640573105733676216427681867088351584121584389018754537084466839171734766578219160803351245620843637925072710000896849690364839391005346961250315101594674583712045699342302859453575267976276170713126867963590409757819086246511805481619007727816192466327917934538452198751043133600811988627670341877635984188732339117397268915568939671855190568748651990476801322769072204354000504126463000062756996159151369984613678629296894569657870414170788557086634315158953604256571645276541991385271801343453852052513984715452251168898558991386987, 18741210160129016919027051709195306572122256104284190588152061570146061220004705294924407652723840322738857342110972676342039805846209543534901549461029611129002789391675105256003185101681308678006973067523389930857854399656804828981481818501641807881264750334877875398364824400983154642959468424282062241400359583452771220603670238740144965780134469654688088566881637000906235059560929752661494024981965598520180451038825458760341310137971487367137318032167804295405319849317581857312219504488475520741051864191710371310437749985559416208794774561845429752849802444010638485977030383421273508852575939436498263439581]

c = [877663598257965366546769868863156926085433823093373341927660056921718684741108981030685370897203606397141548876892113121980513100012292277943435499226556217320597200966407658719691766912775453136345386138805865676373075230203782361058708318381925206151202900594065172659312166515164177439340398880007619686757, 877663598257788398669550541490249947671201163543658215568503678126853996375121005683845826967192555984965177924311290187471540695060217277907975873817192769188479252911530155162516779107852289973616465082026668913104315853453769170693144761740397639635947862818157636573955400694354252394572904683975181414757, 877663598257613342219433891622375189701725798040969752040357021050838455618379678722089501027881636058899306745056642895653112534509469732661355319913915084909895329600259020213708594902592587766777379972938031770430460838951979512170601952416235506628123526525325260961780468397051635827481525975671623201125]

N = n[0]*n[1]*n[2]

T = []
T.append(crt([1, 0, 0], n))
T.append(crt([0, 1, 0], n))
T.append(crt([0, 0, 1], n))

# Base message: "Dear      flag{c00l}"
#               "Dear Toto flag{c00l}"


for bytelen in range(256):

    exp = 8*bytelen

    b = [(pow(2, exp))*(bytes_to_long(x.encode()) -
                        bytes_to_long(base.encode())) for x in names]

    P.<x> = PolynomialRing(Zmod(N))

    # construct g(x)
    g = 0
    for i in range(3):
        g += (i+1)*T[i]*((x + b[i])^3 - c[i])

    # g(x) has to be monic polynomial in order to use coppersmith approach
    g = g.monic()

    # coppersmith method in Sage
    M = g.small_roots()

    if (M):
        # and we get the message
        print(long_to_bytes(int(M[0])).decode())
