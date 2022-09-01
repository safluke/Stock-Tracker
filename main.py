import requests
import pywhatkit
#Note: Pywhatkit has been modified to allow the group message function.

STOCK = "ETH"
COMPANY_NAME = "Ethereum"
NUMBER = ""
VOLATILITY=0.0
top_three=[]
change= None

# Use https://www.alphavantage.co
# check Stock Price fluctuation.
def check_price():
    global change, VOLATILITY
    parameters= {
        "function":"CRYPTO_INTRADAY",
        "symbol":STOCK,
        "market":"USD",
        "interval":"60min",
        "apikey":""
        }
    
    url = 'https://www.alphavantage.co/query?'
    r = requests.get(url, params=parameters)
    data = r.json()["Time Series Crypto (60min)"]
    
    # can check:'1. open', '2. high','3. low','4. close,'5. volume'
    currentdata=data[list(data.keys())[0]]["1. open"]
    previousdata=data[list(data.keys())[1]]["1. open"]
    
    change =(-float(previousdata)+float(currentdata))/float(currentdata)
    if abs(change) >= VOLATILITY:
        get_news()


# Use https://newsapi.org
#get top 3 news related to stock
def get_news():
    global top_three
    parameters= {
        "currencies":STOCK,
        "filter":"hot",
        "auth_token":""
        }
    
    url = 'https://cryptopanic.com/api/v1/posts/?'
    r = requests.get(url, params=parameters)
    data = r.json()["results"][:3]
    
    
    top_three=[]
    for news in range(len(data)):
        top_three.append(data[news]["title"])
    send_msg()
    
    

# Send a message to watsapp group chat
def send_msg():
    global top_three, change, COMPANY_NAME, STOCK
    
    if change >=0:
        message= [f"{STOCK}: UP {change}% \nHeadline: {article}\n" for article in top_three]
    
    if change <0:
        message= [f"{STOCK}:DOWN {change}% \nHeadline: {article}\n" for article in top_three]   
    
    message = "".join([str(headline) for headline in message])
    
    #print (message)
    pywhatkit.sendwhatmsg_to_group_instantly(NUMBER,message)
    
check_price()

