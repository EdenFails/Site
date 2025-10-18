# Made for personal use
# Will likely have issues if users try shorten at same time
# not huge security implementations
# I KNOW BASE85 ISNT ENCRYPTION!
# i just dont want to see raw old urls in my sqlite db
# AI made the word list and helped integrate the port listening stuff cos i never touched that
# url validator is simple but found on reddit - better solutions exist but this is fine for me


from urllib.parse import urlparse
import random # duhh
import time # for sleep n shit
import base64  #not encryption but just not plain text, all i wanted as its for personal use... If you doing this for others should probably encrypt
import sqlite3 #database
from urllib.parse import urlparse, urlunparse
import asyncio
from aiohttp import web

words = [
    "apple","anchor","angel","ant","arch","arrow","atom","autumn","axis","badge","baker","balance","band",
    "bank","barrel","base","basket","beach","beam","bear","beetle","berry","blade","blink","block","bloom",
    "boat","bolt","bone","book","boot","bottle","box","brain","branch","brick","bridge","breeze","brush",
    "bubble","bucket","bug","bunny","burst","butter","button","cable","cactus","cake","camera","candle",
    "canyon","car","card","cargo","carrot","castle","cat","chain","chalk","cherry","chest","chip","circle",
    "cloud","clover","coal","coat","cobble","coin","color","comet","compass","cookie","copper","coral",
    "cotton","crab","craft","crane","cream","creek","crystal","cube","cup","curve","cushion","cycle",
    "daisy","dance","dart","data","dawn","day","delta","desert","diamond","dice","dirt","dish","dog",
    "doll","door","dot","dream","drift","drum","dust","eagle","earth","echo","edge","ember","engine",
    "event","fabric","falcon","feather","field","film","filter","fin","fire","fish","flame","flash",
    "flower","fog","forest","frame","frog","frost","fruit","fuel","galaxy","gate","gear","gem","ghost",
    "giant","glass","globe","glow","goat","gold","grain","grass","gravity","green","grid","grove","guard",
    "guest","guitar","hammer","hand","harbor","hawk","heart","hill","honey","hook","hope","horn","horse",
    "house","ice","idea","image","ink","iron","island","jacket","jade","jewel","jungle","key","kite",
    "knife","lake","lamp","laser","leaf","legend","lemon","level","light","lion","lock","logic","loop",
    "lotus","machine","magic","magnet","map","marble","mask","meadow","metal","meter","mist","model",
    "moss","motion","mountain","mouse","music","nail","nebula","nest","net","night","north","note",
    "nova","oasis","ocean","oil","orbit","owl","page","paint","palace","panda","paper","park","path",
    "pearl","pen","pencil","pepper","petal","phase","phoenix","photo","piano","pillar","pilot","pine",
    "pixel","planet","plasma","plate","plume","pocket","pond","pool","power","prairie","pulse","pump",
    "puzzle","quartz","quest","rabbit","raccoon","rain","raven","ray","reef","ribbon","ridge","ring",
    "river","robot","rock","rocket","rose","route","saber","sail","sand","scale","scar","scene","scope",
    "sea","seed","shadow","shape","shell","ship","shoe","signal","silver","sky","smoke","snake","snow",
    "soap","solar","sound","space","spark","sphere","spider","spike","spirit","spring","square","stack",
    "star","steam","steel","stone","storm","stream","street","sun","surf","swallow","sword","table",
    "tail","tiger","torch","tower","track","train","tree","tribe","trunk","tunnel","valley","vapor",
    "vault","vine","vision","voice","volt","water","wave","wheel","whisper","wild","wind","wing","wire",
    "wolf","wood","word","world","wren","zone","zebra","zero","zenith","zephyr","zinc","amber","azure",
    "beacon","blaze","brisk","calm","clever","cool","crisp","daring","deep","eager","faint","fast",
    "fearless","fierce","gentle","giant","golden","grand","happy","harsh","humble","icy","kind","lazy",
    "light","lively","lucky","mighty","noble","peaceful","pure","quick","quiet","rapid","rare","sharp",
    "silent","simple","smart","smooth","soft","swift","tiny","vast","vivid","wild","young","bold",
    "urban","rural","ancient","bright","fresh","solid","prime","cosmic","stellar","atomic","sonic",
    "lunar","solar","neon","quantum","digital","cyber","fusion","static","signal","nova","pulse","orbit",
    "zen","frosty","shadowy","mystic","crimson","onyx","sapphire","emerald","jade","ruby","amber",
    "air","ale","arc","art","ash","aqua","bee","bin","bit","bow","bug","bun","cap","car","cat",
    "cup","day","dew","dig","dot","ear","egg","elf","fan","fig","fog","fun","gem","gin","gum","hat",
    "ice","ink","ivy","jam","jar","jet","kid","kit","log","map","mix","mud","net","oak","owl","peg",
    "pin","pot","ray","rib","rod","sea","sky","sun","tap","tip","top","toy","van","wax","web","win",
    "yak","zip","ace","bag","bar","bat","bay","bid","bud","bus","cal","cob","cot","cub","cut","dim",
    "dip","doc","dry","end","elk","fan","fin","fit","gap","gas","gel","got","gut","hip","hog","jog",
    "lap","lid","lot","mat","mop","nip","nut","odd","oil","pad","pan","pet","pie","pun","rat","rig",
    "sad","sap","see","set","sip","sit","vet",
    "ant","arm","ask","bag","ban","bat","bed","bee","beg","bin","bit","bud","bun","bus","cab","can",
    "cap","car","cat","cob","cod","cot","cub","cup","cut","dam","day","dew","dig","dip","dog","dot",
    "dry","dub","ear","eat","eel","egg","elf","elk","elm","end","fan","far","fat","fig","fin","fir",
    "fit","fog","fox","fun","gap","gas","gel","gem","gig","got","gum","gut","hat","hen","her","hip",
    "hog","hop","ice","ink","jam","jet","job","jog","joy","jug","key","kit","lab","lad","lap","law",
    "lid","log","lot","mad","man","map","mat","may","mop","mud","net","new","nip","nod","not","oak",
    "oar","odd","off","oil","old","one","orb","owl","pad","pal","pan","pat","paw","peg","pen","pet",
    "pie","pin","pit","pot","pub","pun","rag","ram","rat","red","rig","rip","rod","rot","rub","rum",
    "run","sad","sap","sat","saw","sea","see","set","sip","sit","sun","tab","tap","tar","tip","top",
    "toy","van","vet","wag","war","wax","web","win","yak","zip","ace","add","ado","age","ago","air",
    "ale","all","and","ant","any","ape","ark","arm","art","ash","ask","awe","axe","aye","bag","ban",
    "bar","bat","bay","bed","bee","beg","bet","bid","bin","bit","bog","boo","bow","box","bud","bug",
    "bun","bus","but","buy","cab","cad","can","cap","car","cat","cob","cod","cog","cot","cow","cub",
    "cup","cur","cut","dab","dad","dam","day","den","dew","did","dig","dim","dip","dog","don","dot",
    "dry","dub","dug","ear","eat","eel","egg","elf","elk","elm","end","eon","era","eve","eye","fan",
    "far","fat","fed","fee","few","fig","fin","fir","fit","fog","fox","fun","gap","gas","gel","gem",
    "get","gig","god","got","gum","gun","gut","guy","gym","had","ham","has","hat","haw","hay","hem",
    "her","hey","hid","him","hip","his","hit","hog","hop","hot","how","hub","hug","hum","ice","icy",
    "ink","inn","ion","jam","jar","jaw","jet","job","jog","joy","jug","key","kid","kit","lab","lad",
    "lag","lap","law","lay","led","leg","let","lid","lie","log","lot","mad","man","map","mat","may",
    "men","met","mix","mob","mom","mud","mug","net","new","nip","nod","not","now","oak","oar","odd",
    "off","oil","old","one","orb","ore","our","out","owl","pad","pal","pan","pat","paw","pay","peg",
    "pen","pet","pie","pin","pit","pod","pot","pub","pun","rag","ram","ran","rap","rat","raw","red",
    "rib","rig","rip","rob","rod","rot","row","rub","rug","rum","run","sad","sap","sat","saw","say",
    "sea","see","set","sew","she","shy","sip","sit","six","ski","sky","sly","son","sun","tab","tad",
    "tag","tan","tap","tar","tax","tea","tie","tip","toe","top","toy","try","tub","tug","van","vet",
    "vow","wag","war","wax","way","web","win","wit","woe","yak","yam","yaw","yay","yen","yes","yet",
    "you","zip","zoo"
]
# ai generated list of random words to use for end of url


max_requests = 3
rate_window_seconds = 60
ip_limits = {} # { "ip": [timestamps...] }
def check_rate_limit(ip): # simple ratelimiter

    now = time.time()
    timestamps = []

    for t in ip_limits.get(ip, []): # get all time stamps
        if (now - t < rate_window_seconds): # if timestamp isnt to old
            timestamps.append(t) # add to list to use
    if (len(timestamps) >= max_requests): 
        return False# block if they hit their limit
    timestamps.append(now)
    ip_limits[ip] = timestamps
    return True


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

def ConvertUrl(val,Connection:sqlite3.Connection,Cursor:sqlite3.Cursor):
    b85 = base64.b85encode(val.encode()).decode() # i know its not encryption, just didnt want plain text... for personal use so ehh

    res = Cursor.execute("SELECT newurlvar FROM urlshortvar WHERE oldurlvar = ?",(b85,)) # stop sql injection
    exists = res.fetchone()
    if(exists):
        return exists[0] # returns the converted url if it exists
    else:
        res = None
        # convert url
        while(True): # break if its unique
            EndUrl = ""
            EndUrl = "-".join(random.choice(words) for egg in range(6))
            res = Cursor.execute("SELECT newurlvar FROM urlshortvar WHERE newurlvar = ?",(EndUrl,))
            exists = res.fetchone()
            if (not exists):
                Cursor.execute("INSERT INTO urlshortvar (oldurlvar,newurlvar) VALUES (?,?) ",(b85,EndUrl,)) # insert old url and new url 
                Connection.commit() 
                return EndUrl
            else:
                time.sleep(0.1)
              
def DeleteExpired(Connection:sqlite3.Connection,Cursor:sqlite3.Cursor): # used on start up then eventually i am going to make it check every 3 hrs if server been on long enough that is
    try:
        Cursor.execute("DELETE FROM urlshortvar WHERE creationdate < datetime('now', '-3 months', 'localtime')")
        Connection.commit() # Use this to delete old urls
        return True
    except Exception as e:
        print("Error caught: ", e)
        return False

async def handle(request):
    ip = request.remote
    if(check_rate_limit(ip)):
       
        url_to_shorten = request.match_info.get('tail', '')
        
        print("Received URL:", url_to_shorten)

        # turns out this was needed 
        # probabably shouldnt be allowing all sites but ehh
        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        
        if (not uri_validator(url_to_shorten)): # simple url validator found on reddit
            return web.Response(text="Not Valid Url", headers=headers)
        
        Connection = sqlite3.connect("youdbnamehere.db")
        Cursor = Connection.cursor()
        Cursor.execute("""
        CREATE TABLE IF NOT EXISTS urlshort(
            oldurlvar TEXT UNIQUE,
            newurlvar TEXT UNIQUE,
            creationdate TEXT DEFAULT (datetime('now', 'localtime'))
        )""")
        Connection.commit()
        
        short = ConvertUrl(url_to_shorten, Connection, Cursor)
        return web.Response(text=f"http://send.call-your.dad/short/{short}", headers=headers)

async def redirect_short(request):
    fivewords = request.match_info.get('short', '')
    headers = {"Access-Control-Allow-Origin": "*"}

    Connection = sqlite3.connect("youdbnamehere.db")
    try:
        Cursor = Connection.cursor()
        res = Cursor.execute("SELECT oldurl FROM urlshort WHERE newurl = ?", (fivewords,))
        row = res.fetchone()
        if (row):
            original_b85 = row[0]
            original_url = base64.b85decode(original_b85.encode()).decode()
            print("URL Found:",original_url)
            raise web.HTTPFound(original_url)
        else:
            print("Short URL not found for",fivewords)
            return web.Response(text="Short URL not found", headers=headers)
    finally:
        Connection.close()



async def main(): # ai helped sort the async port listening stuff since i never really touched that
    Connection = sqlite3.connect("youdbnamehere.db")
    Cursor = Connection.cursor()
    Cursor.execute("""
    CREATE TABLE IF NOT EXISTS urlshort(
        oldurlvar TEXT UNIQUE,
        newurlvar TEXT UNIQUE,
        creationdate TEXT DEFAULT (datetime('now', 'localtime'))
    )""")               
    Connection.commit()                   # this is only good for small usages, if to many people try shorten url at same time will likely cause error cos sqlite lock it down temporarily
    DeleteExpired(Connection, Cursor)     # not an issue for me though as its a small project only really for myself


    app = web.Application()
    app['db_conn'] = Connection
    app['db_cursor'] = Cursor
    app.router.add_route('*', '/send/{tail:.*}', handle)
    app.router.add_route('*', '/short/{short}', redirect_short)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=x) # set as an open port
    await site.start()
    print("Listening on port x...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
