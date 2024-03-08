#Option Strategy Web Applet
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__,static_folder="static")
host = 'http://127.0.0.1:5000/'


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/strategies.html', methods=['GET'])
def strats():
    delta = request.args.get('delta')
    gamma = request.args.get('gamma')
    theta = request.args.get('theta')
    vega = request.args.get('vega')
    net = request.args.get('net')
    Strategies = get_strats(delta,gamma,theta,vega,net)
    return render_template('strategies.html',Strategies=Strategies,greeks=[delta,gamma,theta,vega,net])

@app.route('/strategy.html',methods=['GET'])
def strat():
    return render_template('strategy.html',strategy=strategy(request.args.get('strategy')))


def get_strats(delta,gamma,theta,vega,net):
    strats = []
    if delta == 'Long':
        strats.extend(strategies['ldelta'])
    elif delta == 'Neutral':
        strats.extend(strategies['ndelta'])
    elif delta == 'Short':
        strats.extend(strategies['sdelta'])
    else:
        strats = [y for x in strategies.values() for y in x]

    if gamma == 'Long':
        strats = list(set(strats) & set(strategies['lgamma']))
    elif gamma == 'Neutral':
        strats = list(set(strats) & set(strategies['ngamma']))
    elif gamma == 'Short':
        strats = list(set(strats) & set(strategies['sgamma']))

    if theta == 'Long':
        strats = list(set(strats) & set(strategies['ltheta']))
    elif theta == 'Neutral':
        strats = list(set(strats) & set(strategies['ntheta']))
    elif theta == 'Short':
        strats = list(set(strats) & set(strategies['stheta']))
    
    if vega == 'Long':
        strats = list(set(strats) & set(strategies['lvega']))
    elif vega == 'Neutral':
        strats = list(set(strats) & set(strategies['nvega']))
    elif vega == 'Short':
        strats = list(set(strats) & set(strategies['svega']))
    
    if net == 'Credit':
        strats = list(set(strats) & set(strategies['credit']))
    elif net == 'Debit':
        strats = list(set(strats) & set(strategies['debit']))

    
    strats = list(set(strats))
    strats.sort(key=lambda x: order[x])
    for c,i in enumerate(strats):
        strats[c] = [i,descriptions[i]]

    return strats

def strategy(name):
    return [name,descriptions[name]]


strategies = {
    'ldelta':['Long Call','Short Put','Bull Call Spread','Bull Put Spread'],
    'lgamma':['Long Call','Long Put','Long Straddle','Long Strangle','Reverse Iron Butterfly','Reverse Iron Condor','Short Call Butterfly','Short Call Condor','Short Put Butterfly','Short Put Condor'],
    'ltheta':['Short Call','Short Put','Iron Butterfly','Iron Condor','Long Call Butterfly','Long Call Condor','Long Put Butterfly','Long Put Condor','Short Straddle','Short Strangle'],
    'lvega':['Long Call','Long Put','Long Straddle','Long Strangle','Reverse Iron Butterfly','Reverse Iron Condor','Short Call Butterfly','Short Put Butterfly','Short Call Condor','Short Put Condor'],
    'ndelta':['Iron Butterfly','Iron Condor','Long Call Butterfly','Long Call Condor','Long Put Butterfly','Long Put Condor','Long Strangle','Long Straddle','Reverse Iron Butterfly','Reverse Iron Condor','Short Call Butterfly','Short Call Condor','Short Put Butterfly','Short Put Condor','Short Strangle','Short Straddle'],
    'ngamma':['Bull Call Spread','Bull Put Spread','Bear Call Spread','Bear Put Spread'],
    'ntheta':['Bull Call Spread','Bull Put Spread','Bear Call Spread','Bear Put Spread'],
    'nvega':['Bull Call Spread','Bull Put Spread','Bear Call Spread','Bear Put Spread'],
    'sdelta':['Short Call','Long Put','Bear Call Spread','Bear Put Spread'],
    'sgamma':['Short Call','Short Put','Iron Butterfly','Iron Condor','Long Call Butterfly','Long Call Condor','Long Put Butterfly','Long Put Condor','Short Straddle','Short Strangle'],
    'stheta':['Long Call','Long Put','Long Straddle','Long Strangle','Reverse Iron Butterfly','Reverse Iron Condor','Short Call Butterfly','Short Call Condor','Short Put Butterfly','Short Put Condor'],
    'svega':['Short Call','Short Put','Iron Butterfly','Iron Condor','Long Call Butterfly','Long Call Condor','Long Put Butterfly','Long Put Condor','Short Straddle','Short Strangle'],
    'credit':['Short Call','Short Put','Bull Put Spread','Bear Call Spread','Short Straddle','Short Strangle','Short Call Butterfly','Short Put Butterfly','Iron Butterfly','Short Call Condor','Short Put Condor','Iron Condor'],
    'debit':['Long Call','Long Put','Bull Call Spread','Bear Put Spread','Long Straddle','Long Strangle','Long Call Butterfly','Long Put Butterfly','Reverse Iron Butterfly','Long Call Condor','Long Put Condor','Reverse Iron Condor']
}

descriptions = {
    'Long Call':"Buying a single call option. Limited risk with unliimited potential profit. Bullish. Net debit.",
    'Long Put':"Buying a single put option. Limited risk with unlimited potential profit. Bearish. Net debit.",
    'Short Call':"Selling a single call option. Unlimited risk with limited potenital profit. Bearish. Net credit.",
    'Short Put':"Selling a single put option. Unlimited risk with limited potenital profit. Bullish. Net credit.",
    'Bull Call Spread':"Simple bullish spread made with calls. Limited risk with limited potential profit. Net debit.",
    'Bull Put Spread':"Simple bullish spread made with puts. Limited risk with limited potential profit. Net credit.",
    'Bear Call Spread':"Simple bearish spread made with calls. Limited risk with limited potential profit. Net credit.",
    'Bear Put Spread':"Simple bearish spread made with puts. Limited risk with limited potential profit. Net debit.",
    'Long Straddle':"A non-directional, two legged strategy made by buying a call and a put an the same strike price. Profits when there is significant price movement. Limited risk with unlimited potential profit. Net debit.",
    'Short Straddle':"A non-directional, two legged strategy made by selling a call and a put at the same strike price. Profits when there is little price movement. Unlimited risk with limited potential profit. Net credit.",
    'Long Strangle':"A non-directional, two legged strategy made by buying a calls and a put. Profits when there is significant price movement. Limited risk with unlimited potential profit. Net debit.",
    'Short Strangle':"A non-directional, two legged strategy made by selling a call and a put. Profits when there is little price movement. Unlimited risk with limited potential profit. Net credit.",
    'Long Call Butterfly':"A non-directional, three legged strategy made with calls. Profits when there is little price movement. Limited risk with limited potential profit. Net debit",
    'Long Put Butterfly':"A non-directional, three legged strategy made with puts. Profits when there is little price movement. Limited risk with limited potential profit. Net debit",
    'Short Call Butterfly':"A non-directional, three legged strategy made with calls. Profits when there is significant price movement. Limited risk with limited potential profit. Net credit.",
    'Short Put Butterfly':"A non-directional, three legged strategy made with puts. Profits when there is significant price movement. Limited risk with limited potential profit. Net credit.",
    'Iron Butterfly':"A non-directional, four legged strategy made with both calls and puts. Profits when there is little price movement. Limited risk with limited potential profit. Net Credit",
    'Reverse Iron Butterfly':"A non-directional, four legged strategy made with both calls and puts. Profits when there is significiant price movement. Limited risk with limited potential profit. Net Debit",
    'Long Call Condor':"A non-directional, four legged strategy made with calls. Profits when there is little price movement. Limited risk with limited potential profit. Net debit.",
    'Long Put Condor':"A non-directional, four legged strategy made with puts. Profits when there is significant price movement. Limited risk with limited potential profit. Net debit.",
    'Short Call Condor':"A non-directional, four legged strategy made with calls. Profits when there is little price movement. Limited risk with limited potential profit. Net credit.",
    'Short Put Condor':"A non-directional, four legged strategy made with puts. Profits when there is little price movement. Limited risk with limited potential profit. Net credit.",
    'Iron Condor':"A non-directional, four legged strategy made with both calls and puts. Profits when there is little price movement. Limited risk with limited potential profit. Net credit.",
    'Reverse Iron Condor':"A non-directional, four legged strategy made with both calls and puts. Profits when there is significant price movement. Limited risk with limited potential profit. Net debit."
}

order = {i:c for c,i in enumerate(descriptions.keys())}

if __name__ == "__main__":
    app.run(debug=True)
    